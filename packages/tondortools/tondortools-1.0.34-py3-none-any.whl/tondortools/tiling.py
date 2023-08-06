import json
import logging
import math
import os
import glob
import calendar
import shutil
import copy
import subprocess


from datetime import datetime
from datetime import timedelta
from pathlib import Path
from shutil import copytree
from tempfile import mkdtemp
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, validator, root_validator, Field

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from shapely.geometry import Point

import osgeo.gdal as gdal
import ogr

log = logging.getLogger(__name__)

@dataclass
class Tile:
    name: str
    epsg: int
    count: int

@dataclass
class Services:
    sub: List[str] = field(default_factory=list)
    dst: List[str] = field(default_factory=list)
    parcel_id: str = field(default_factory=str)
    FOI: List[str] = field(default_factory=list)


@dataclass
class DataObject:
    tiles: List[Tile]
    services: Dict[str, Services]
    pixel: Dict[str, int]
    kult_conversion_table_name: Optional[str]
    conversion_table_original_column: Optional[str]
    conversion_table_target_column: Optional[str]
    classification_support_data: Optional[Path]
    min_parcel : int

    def get_service_info(self, service_name):
        for serivce_item_name, serive_attribute in self.services.items():
            if serivce_item_name == service_name:
                return serive_attribute

    def get_tile_info(self, tile_name):
        if self.tiles is not None:
            for tile_name_item in self.tiles:
                if tile_name_item.name == tile_name:
                    return tile_name_item
        else:
            return None

class DataObjectModel(BaseModel):
    tiles: Optional[List[Tile]]
    services: Dict[str, Services]
    pixel: Dict[str, int] =  Field({})
    kult_conversion_table_name : Optional[str]
    conversion_table_original_column: Optional[str]
    conversion_table_target_column: Optional[str]
    classification_support_data: Optional[Path]
    min_parcel: int = Field(2000)

    @validator('services', pre=True)
    def convert_to_services_objects(cls, value):
        return {k: Services(**v) for k, v in value.items()}

def open_json(path: Union[Path, str]):
    with open(path, 'r') as file:
        return json.load(file)

class Config(BaseModel):
    tiles: Optional[List]
    services: dict

def create_object(config_path):
    # Parsing the JSON data and creating the object
    parsed_object = DataObjectModel.parse_obj(open_json(config_path))
    data_object = DataObject(**parsed_object.dict())
    return data_object

#############################################################
#############################################################
def split_parcels(input_gpkg, eotiled_gpkg_output_filename, output_dir, subtiles_count=10):
    do_split_save_gpkg(input_gpkg, eotiled_gpkg_output_filename, output_dir, subtiles_count)
    log.info(f"Done splitting parcels for {input_gpkg}")


#############################################################
def compile_service_in_input_tiled_filename(service, project, environment, yearmonth, tile_name, subfolder_type=None):
    if subfolder_type is not None:
        service_filename = f"{str(service).upper()}_{project}_{environment}_{yearmonth}_{tile_name}_{subfolder_type}.gpkg"
    else:
        service_filename = f"{str(service).upper()}_{project}_{environment}_{yearmonth}_{tile_name}.gpkg"
    return service_filename

def compile_service_in_output_tiled_filename(service, project, environment, yearmonth, tile_name, subfolder_type=None):
    if subfolder_type is not None:
        service_filename = f"{str(service).upper()}_{project}_{environment}_{yearmonth}_{subfolder_type}_{tile_name}.gpkg"
    else:
        service_filename = f"{str(service).upper()}_{project}_{environment}_{yearmonth}_{tile_name}.gpkg"
    return service_filename

def compile_service_project_env_time_sub_folder_relpath(parent_folder, service, project, environment, analysis_time, subfolder_type= None):
    if subfolder_type is not None:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time), str(subfolder_type).upper())
    else:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time))
    return service_folder


def compile_output_dir(parent_folder, service_name, environment, project, analysis_time, tilename, sub_dir=None):
    parent_output_folder = Path(parent_folder).joinpath("output")
    output_dir = compile_service_project_env_time_sub_folder_relpath(parent_output_folder, service_name, project, environment, analysis_time, sub_dir)
    output_dir_tile = output_dir.joinpath(tilename)
    return output_dir_tile


def locate_gpkg(parent_folder, service_name, environment, project, analysis_time, tile_name, subfolder_type= None):

    gpkg_filename = compile_service_in_input_tiled_filename(service_name, project, environment, analysis_time, tile_name, subfolder_type)

    parent_input_folder = Path(parent_folder).joinpath("input")
    gpkg_parentpath = compile_service_project_env_time_sub_folder_relpath(parent_input_folder, service_name, project, environment, analysis_time, subfolder_type)
    gpkg_filepath = Path(gpkg_parentpath).joinpath(f"{gpkg_filename}.gpkg")

    if not gpkg_filepath.exists():
        raise Exception(f"{gpkg_filepath} doesnot exist")
    else:
        log.debug(f"{gpkg_filepath} found for spliting")

    return gpkg_filepath

def locate_gpkg_tool(parent_folder, service_name, environment, project, analysis_time, tilename, subfolder_type= None):

    eodata_tilename = return_eodata_tilename(tilename)
    gpkg_folder = compile_output_dir(parent_folder, str(service_name).lower(), str(environment).upper(), str(project).upper(),
                                     str(analysis_time), str(eodata_tilename).upper(), sub_dir=subfolder_type)

   #
    gpkg_basename = compile_service_in_output_tiled_filename(service_name, str(project).upper(), environment, analysis_time, tilename,
                                                             subfolder_type)
    gpkg_filepath = gpkg_folder.joinpath(gpkg_basename)

    #
    gpkg_nodata_basename = gpkg_basename.replace(".gpkg", "_NODATA.txt")
    gpkg_subtile_nodata_filepath = gpkg_folder.joinpath(gpkg_nodata_basename)

    gpkg_nodata_basename = gpkg_nodata_basename.replace(tilename, eodata_tilename)
    gpkg_nodata_filepath = gpkg_folder.joinpath(gpkg_nodata_basename)


    if gpkg_filepath.exists():
        log.info(f"{gpkg_filepath} exists")
        return gpkg_filepath

    if gpkg_subtile_nodata_filepath.exists():
        log.info(f"{gpkg_subtile_nodata_filepath} exists")
        return gpkg_subtile_nodata_filepath

    if gpkg_nodata_filepath.exists():
        log.info(f"{gpkg_nodata_filepath} found.")
        return gpkg_nodata_filepath

    else:
        raise Exception(f"{gpkg_filepath} {gpkg_nodata_filepath} not found")
#############################################################
#############################################################

def return_eodata_tilename(tilename):
    if "-" in tilename:
        eodata_tilename = tilename.split("-")[0]
        return eodata_tilename
    else:
        return tilename

def get_tile_list(tile_gpkgfilepath, gpkg_parcel_column):
    master_df = gpd.read_file(str(tile_gpkgfilepath))
    return master_df[gpkg_parcel_column].to_list()

def compile_service_project_env_time_sub_folder_relpath(parent_folder, service, project, environment, analysis_time, subfolder_type= None):
    if subfolder_type is not None:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time), str(subfolder_type).upper())
    else:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time))
    return service_folder


def compile_output_dir(parent_folder, service_name, environment, project, analysis_time, tilename, sub_dir=None):
    parent_output_folder = Path(parent_folder).joinpath("output")
    output_dir = compile_service_project_env_time_sub_folder_relpath(parent_output_folder, service_name, project, environment, analysis_time, sub_dir)
    output_dir_tile = output_dir.joinpath(tilename)
    return output_dir_tile

###############################################################################
def get_gpkg_epsg(gpkg_path):
    source = ogr.Open(str(gpkg_path), update=False)
    layer = source.GetLayer()
    epsg = layer.GetSpatialRef().GetAuthorityCode(None)
    source = None
    layer = None
    return epsg



def group_polygons_assigngroupid(gdf_input):
    gdf = copy(gdf_input)

    invalid_mask = ~gdf.geometry.is_valid
    gdf.loc[invalid_mask, 'geometry'] = gdf.loc[invalid_mask, 'geometry'].buffer(0)

    # Create a new column to store the group ID for each polygon
    gdf['group_id'] = -1

    group_id = 0
    # Iterate over each row in the GeoDataFrame
    for idx, row in gdf.iterrows():

        # Get the group ID of the current row
        if row['group_id'] != -1:
            row_group_id = row['group_id']
        else:
            row_group_id = group_id
            group_id += 1

        # Find all polygons that touch or intersect the current row's geometry
        neighbors = gdf[gdf.touches(row['geometry']) | gdf.intersects(row['geometry'].buffer(1))]

        # Check if any neighbors have a different group ID
        neighbor_group_ids = neighbors.loc[neighbors['group_id'] != -1, 'group_id']
        if not neighbor_group_ids.empty:
            # Get the unique group IDs of the neighbors
            unique_group_ids = neighbor_group_ids.unique()

            # Assign the current row's group ID to the neighbors with different group IDs
            gdf.loc[neighbors.index, 'group_id'] = row_group_id

            # Update the group ID for all polygons with the unique group IDs
            gdf.loc[gdf['group_id'].isin(unique_group_ids), 'group_id'] = row_group_id

        else:
            # Assign the current row's group ID to the neighbors with the default group ID
            gdf.loc[neighbors.index, 'group_id'] = row_group_id

    grouped_geoms = []
    for unique_group_id in gdf.group_id.unique():
        gdf_group_id = gdf.loc[gdf.group_id == unique_group_id]
        touching_geoms = []
        for idx, row in gdf_group_id.iterrows():
            touching_geoms.append(row)
        grouped_geoms.append(touching_geoms)
    return grouped_geoms


def add_flattened_to_gdf(gdfs, flattened_list):

    gdf_index = 1

    for list_index, list_item in enumerate(flattened_list):
        flattened_list_item_gdf = gpd.GeoDataFrame([flattened_list[list_index]])
        gdfs[gdf_index] = pd.concat([gdfs[gdf_index], flattened_list_item_gdf], ignore_index=True, sort=False)

        gdf_index += 1
        if gdf_index >= len(gdfs) - 1:
            gdf_index = 0
        if len(gdfs[gdf_index+1]) == 0:
            gdf_index = 0
    return gdfs

def split_gdf_nonoverlap(gdf, subtiles_count, min_rows = 2000):
    total_rows = len(gdf)
    if min_rows is None:
        min_rows = total_rows / subtiles_count
    max_rows_per_split = math.ceil(max(min_rows, total_rows / subtiles_count))
    splits = []
    for i in range(subtiles_count):
        start_idx = i * max_rows_per_split
        end_idx = min((i + 1) * max_rows_per_split, total_rows)
        split_gdf = gdf.iloc[start_idx:end_idx]
        splits.append(split_gdf)
    return splits

def split_geodataframe(gdf, subtiles_count, min_rows = 750, split_overlap = False, input_gpkg = None, work_dir=None, parcel_column = 'AZID'):


    if not split_overlap:
        splits = split_gdf_nonoverlap(gdf, subtiles_count, min_rows=min_rows)
        return splits

    else:

        gpkg_ds = ogr.Open(str(input_gpkg), 0)  # 0 for read-only mode
        layer = gpkg_ds.GetLayer(0)  # Replace 0 with the index of the desired layer if there are multiple layers in the GeoPackage

        extent = gdf.total_bounds

        # Define the pixel size
        pixel_size = 20
        # Specify the column to burn into the raster
        column_name = parcel_column

        driver = gdal.GetDriverByName('GTiff')
        rows = int((extent[3] - extent[1]) / pixel_size)
        cols = int((extent[2] - extent[0]) / pixel_size)

        output_raster_path = Path(work_dir).joinpath(f"{Path(input_gpkg).name}.tif")
        output_raster = driver.Create(str(output_raster_path), cols, rows, 1, gdal.GDT_Float32)
        output_raster.SetGeoTransform((extent[0], pixel_size, 0, extent[3], 0, -pixel_size))
        output_raster.SetProjection(gdf.crs.to_wkt())
        gdal.RasterizeLayer(output_raster, [1], layer, options=['ATTRIBUTE=' + column_name, 'ATTRIBUTE=no_touch'])
        rasterized_parcels = np.unique(output_raster.ReadAsArray())
        output_raster = None

        gpkg_parcel_list = gdf[column_name].to_list()
        missing_parcel = set(gpkg_parcel_list).difference(set(rasterized_parcels))


        parcels_gdf_rasterized_parcels = gdf.loc[~gdf[column_name].isin(missing_parcel)]
        parcels_gdf_missing_parcels = gdf.loc[gdf[column_name].isin(missing_parcel)]

        gdfs = split_gdf_nonoverlap(parcels_gdf_rasterized_parcels, subtiles_count=20, min_rows=min_rows)

        group_withid = group_polygons_assigngroupid(parcels_gdf_missing_parcels)

        # Flatten the list of lists into a single list
        flattened_list = [row for sublist in group_withid for row in sublist]

        gdfs_added = add_flattened_to_gdf(gdfs, flattened_list)
        return gdfs_added


def do_split_save_gpkg(input_gpkg, output_gpkg_basename, output_dir,
                       subtiles_count=14, min_parcels = None, split_overlap = False, work_dir=None, parcel_column = 'AZID'):

    logfilepath = output_dir.joinpath("tiling_log.txt")
    logfile = open(logfilepath, "w")
    logfile.write("--------------------------------\n")
    logfile.write("-SUBTILE PARCEL COUNT-\n")
    logfile.write("--------------------------------\n")

    gpkg_filename = Path(input_gpkg).name
    gpkg_ds = ogr.Open(str(input_gpkg))

    # Get the number of parcels
    layer_name = gpkg_ds.GetLayer().GetName()
    feature_count = gpkg_ds.GetLayer().GetFeatureCount()

    # Load the GeoPackage file into a GeoDataFrame
    gdf = gpd.read_file(input_gpkg, layer=layer_name)

    if min_parcels is None:
        # Divide the GeoDataFrame into n equal parts
        gdfs = np.array_split(gdf, subtiles_count)
    else:
        gdfs = split_geodataframe(gdf, subtiles_count, min_parcels, split_overlap, input_gpkg, work_dir, parcel_column)

    gpgk_paths = []
    # Write each subset of data to a new GeoPackage file
    parcel_count = 0
    for gdf_index, gdf_subset in enumerate(gdfs):

        number_of_parcels = len(gdf_subset)
        parcel_count += number_of_parcels

        if number_of_parcels !=0:
            output_file = output_dir.joinpath(output_gpkg_basename.replace(".gpkg", f"-{gdf_index + 1}.gpkg"))
            output_file.unlink(missing_ok=True)
            layer_name = gpkg_filename.replace(".gpkg", f"_{gdf_index+1}.gpkg")
            gdf_subset.to_file(output_file, layer=layer_name, driver='GPKG')
            gpgk_paths.append(output_file)
        else:
            output_file = output_dir.joinpath(output_gpkg_basename.replace(".gpkg", f"-{gdf_index + 1}_NODATA.txt"))
            output_file.unlink(missing_ok=True)
            output_file.write_text("No parcel")
            gpgk_paths.append(output_file)
        logfile.write(f"{output_file} -- {number_of_parcels} \n")
    logfile.write("--------------------------------\n")
    logfile.write(f"PARCEL COUNT = {parcel_count}\n")
    logfile.close()
    return gpgk_paths

class Merge():
    def __init__(self, project, environemt, yearmonth, service, bioregion, classification_support_data=None, sar_type= None):
        self.project = str(project).upper()
        self.environemt = str(environemt).upper()
        self.yearmonth = str(yearmonth)
        self.service = str(service).upper()
        self.sar_type = str(sar_type).upper()
        self.bioregion = str(bioregion).upper()
        self.year = self.yearmonth[0:4]
        self.classification_support_data = classification_support_data

    def get_config_path(self, parent_folder):
        config_path = parent_folder.joinpath("project_info", self.project, f"{self.bioregion}_config.json")
        if config_path.exists():
            log.info(f"{config_path} exists.")
            return config_path
        else:
            raise Exception(f"{config_path} doesnt exists.")

    def set_bioregion_path(self, parent_folder):
        gpkg_filepath = parent_folder.joinpath("tiles", self.project, f"{self.bioregion}_tiles.gpkg")
        if gpkg_filepath.exists():
            log.info(f"{gpkg_filepath} exists.")
            self.region_gpkg = gpkg_filepath
            return gpkg_filepath
        else:
            raise Exception(f"{gpkg_filepath} doesnt exists.")

    def set_epsg(self, template_gpkg):
        epsg = get_gpkg_epsg(template_gpkg)
        self.epsg = epsg


def create_submit_tile_instance(project, environment, yearmonth, service, bioregion, parent_folder, tile_name = None, tool_service = None, gpkg_parcel_column = "sitecode"):
    mi = Merge(project=project, environemt=environment, yearmonth=yearmonth, service=service, bioregion=bioregion, classification_support_data=None)
    mi.set_bioregion_path(parent_folder)

    config_path = mi.get_config_path(parent_folder)
    config = create_object(config_path)

    service_attributes = config.get_service_info(service)
    service_gpkg_dst = service_attributes.dst

    if len(service_gpkg_dst) == 1:
        dst_tool = service_gpkg_dst[0]
    else:
        if tool_service is None:
            raise Exception(f"tool_service is none")
        else:
            if tool_service in service_gpkg_dst:
                dst_tool = tool_service
            else:
                raise Exception(f"{tool_service} not in dst list")

    tilename_dict = {}
    if tile_name is None:
        tilename_list = []
        tile_list = get_tile_list(mi.region_gpkg, gpkg_parcel_column)
        for tile_name in tile_list:
            eodata_tilename = return_eodata_tilename(tile_name)
            for service_gpkg_dst_item in service_gpkg_dst:
                if not service_gpkg_dst_item == tool_service:
                    continue

                sub_dir_tocheck = None
                if service_attributes.sub is not None:
                    if len(service_attributes.sub) > 0:
                        sub_dir_tocheck = service_attributes.sub[0]

                output_dir = compile_output_dir(parent_folder, service_gpkg_dst_item, mi.environemt, mi.project,
                                                mi.yearmonth,
                                                eodata_tilename, sub_dir=sub_dir_tocheck)
            output_dir_filelist = os.listdir(output_dir)
            output_dir_filelist = [i for i in output_dir_filelist if i.endswith('.gpkg') or i.endswith('NODATA.txt')]
            output_dir_filelist_len = len(output_dir_filelist)

            tile_gpkgs = []
            for subtile_count in range(output_dir_filelist_len):
                tilename_list.append(f"{eodata_tilename}-{subtile_count + 1}")
                tile_gpkgs.append(f"{eodata_tilename}-{subtile_count + 1}")
            tilename_dict[eodata_tilename] = tile_gpkgs


    else:
        eodata_tilename = return_eodata_tilename(tile_name)
        for service_gpkg_dst_item in service_gpkg_dst:
            if not service_gpkg_dst_item == tool_service:
                continue

            sub_dir_tocheck = None
            if service_attributes.sub is not None:
                if len(service_attributes.sub) > 0:
                    sub_dir_tocheck = service_attributes.sub[0]

            output_dir = compile_output_dir(parent_folder, service_gpkg_dst_item, mi.environemt, mi.project,
                                            mi.yearmonth,
                                            eodata_tilename, sub_dir=sub_dir_tocheck)
        output_dir_filelist =  os.listdir(output_dir)
        output_dir_filelist  = [i for i in output_dir_filelist if i.endswith('.gpkg') or i.endswith('NODATA.txt')]
        output_dir_filelist_len = len(output_dir_filelist)

        tilename_list = []
        for subtile_count in range(output_dir_filelist_len):
            tilename_list.append(f"{eodata_tilename}-{subtile_count+1}")
        tilename_dict[eodata_tilename] = tilename_list

    return tilename_list, tilename_dict

###############################################################################
###############################################################################

def parcel_centroid(master_df):
    master_df['centroid'] = master_df.geometry.centroid
    return master_df

def find_closest_centroidfromsecond(master_df, tiles_df):
    # Convert centroids to numpy arrays
    centroids_1 = np.vstack(master_df['centroid'].apply(lambda p: (p.x, p.y)).values)
    centroids_2 = np.vstack(tiles_df['centroid'].apply(lambda p: (p.x, p.y)).values)

    # Compute the pairwise distances between centroids
    distances = cdist(centroids_1, centroids_2)
    sitecode_geometry_map = dict(zip(tiles_df['sitecode'], tiles_df['geometry']))

    # Find the closest centroid indices for each centroid in the first DataFrame
    closest_indices = np.argmin(distances, axis=1)

    sorted_indices = np.argsort(distances, axis=1)
    second_min_indices = sorted_indices[:, 1]
    third_smallest_indices = sorted_indices[:, 2]
    fourth_smallest_indices = sorted_indices[:, 3]

    master_df_copy = copy.deepcopy(master_df)

    # Create a new column in the first DataFrame with the closest sitecode
    master_df_copy['sitecode1'] = tiles_df.loc[closest_indices, 'sitecode'].values
    master_df_copy['sitecode2'] = tiles_df.loc[second_min_indices, 'sitecode'].values
    master_df_copy['sitecode3'] = tiles_df.loc[third_smallest_indices, 'sitecode'].values
    master_df_copy['sitecode4'] = tiles_df.loc[fourth_smallest_indices, 'sitecode'].values

    master_df_copy['sitecode1_extent'] = master_df_copy['sitecode1'].map(sitecode_geometry_map)
    master_df_copy['sitecode2_extent'] = master_df_copy['sitecode2'].map(sitecode_geometry_map)
    master_df_copy['sitecode3_extent'] = master_df_copy['sitecode3'].map(sitecode_geometry_map)
    master_df_copy['sitecode4_extent'] = master_df_copy['sitecode4'].map(sitecode_geometry_map)


    df_gdf = gpd.GeoDataFrame(master_df_copy, geometry='geometry')
    df_gdf["sitecode_added"] = False

    df_gdf['lies_within_extent'] = df_gdf.apply(lambda row: row['geometry'].within(row['sitecode1_extent']), axis=1)
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode'] = df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode1']
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode_added'] = True

    df_gdf['lies_within_extent'] = df_gdf.apply(lambda row: row['geometry'].within(row['sitecode2_extent']) and not row['sitecode_added'], axis=1)
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode'] = df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode2']
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode_added'] = True

    df_gdf['lies_within_extent'] = df_gdf.apply(lambda row: row['geometry'].within(row['sitecode3_extent']) and not row['sitecode_added'], axis=1)
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode'] = df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode3']
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode_added'] = True

    df_gdf['lies_within_extent'] = df_gdf.apply(lambda row: row['geometry'].within(row['sitecode3_extent']) and not row['sitecode_added'], axis=1)
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode'] = df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode4']
    df_gdf.loc[df_gdf['lies_within_extent'], 'sitecode_added'] = True

    df_gdf['sitecode_extent'] = df_gdf['sitecode'].map(sitecode_geometry_map)
    #df_gdf['within_extent'] = df_gdf.apply(lambda row: row['geometry'].within(row['sitecode_extent']), axis=1)

    for index, row in df_gdf[df_gdf['sitecode_added'] == False].iterrows():
        for index_site, row_site in tiles_df.iterrows():
            if row['geometry'].within(row_site['geometry']):
                row['sitecode'] = row_site['sitecode']
                row['sitecode_added'] = True
                break

    for index, row in df_gdf[df_gdf['sitecode_added'] == False].iterrows():
        for index_site, row_site in tiles_df.iterrows():
            if row['geometry'].intersects(row_site['geometry']):
                row['sitecode'] = row_site['sitecode']
                row['sitecode_added'] = True
                break

    master_df["sitecode"] = df_gdf["sitecode"]
    return master_df

def create_dfs(master_df, tiles_df):

    sub_df_dict = {}
    for tile_index, df_tile_row in tiles_df.iterrows():
        tile_code = df_tile_row.sitecode
        sub_df = master_df.loc[master_df.sitecode == tile_code]
        sub_df_dict[tile_code] = sub_df
    return sub_df_dict

def do_tiling(raw_gpkg_filepath, tile_gpkgfilepath, tile_column):

    # Read the first GPKG file
    master_df = gpd.read_file(str(raw_gpkg_filepath))

    # Read the second GPKG file
    tiles_df = gpd.read_file(str(tile_gpkgfilepath))
    tiles_df["sitecode"] = tiles_df[tile_column].astype(str)

    # Calculate the centroid of each polygon in the first GPKG file
    master_df = parcel_centroid(master_df)

    # Calculate the centroid of each polygon in the second GPKG file
    tiles_df = parcel_centroid(tiles_df)

    invalid_mask = ~master_df.geometry.is_valid
    master_df.loc[invalid_mask, 'geometry'] = master_df.loc[invalid_mask, 'geometry'].buffer(0)
    ##
    # find closest tile
    master_df = find_closest_centroidfromsecond(master_df, tiles_df)

    # remove
    master_df = master_df.drop(columns=['centroid'])


    ##
    # create sub df
    tile_df_dict = create_dfs(master_df, tiles_df)

    return tile_df_dict


###############################################################################
###############################################################################
###############################################################################


class Tiles():
    row : str
    col : str
    width : str
    height : str
    x_offset : str
    y_offset : str
    xmin : str
    xmax : str
    ymin : str
    ymax : str
    pixel_size : str
    tile_folder: Path
    tile_multiband_composite: Path


def setup_tiles(aoi_xmin, aoi_xmax, aoi_ymin, aoi_ymax, pixel_size, tiles_parentdir, max_tile_size = 3000):

    if not Path(tiles_parentdir).exists():
        os.makedirs(tiles_parentdir)

    # Calculate xmax and ymin based on the pixel size and number of columns and rows
    num_cols = math.ceil((aoi_xmax - aoi_xmin) / pixel_size)
    num_rows = math.ceil((aoi_ymax - aoi_ymin) / pixel_size)
    # Returns a dictionary of tile infos that can be used to cut a large raster into smaller tiles.
    # Each item in the dictionary has properties:
    # row, column, width_pixels, height_pixels, x_offset_pixels, y_offset_pixels, ulx_coordinate, uly_coordinate
    n_tile_cols = math.ceil(num_cols / max_tile_size)
    n_tile_rows = math.ceil(num_rows / max_tile_size)
    log.debug(f"ntiles: {n_tile_rows}, {n_tile_cols}")

    last_col = n_tile_cols - 1
    last_row = n_tile_rows - 1
    tile_infos = []
    for tile_row in range(n_tile_rows):
        tile_height = max_tile_size
        y_offset = tile_row * tile_height
        # Last row is a special case - tile height must be adjusted.
        if tile_row == last_row:
            tile_height = num_rows - (max_tile_size * tile_row)
        log.debug(f"tile_height {tile_height}")
        for tile_col in range(n_tile_cols):
            tile_width = max_tile_size
            x_offset = tile_col * tile_width
            # Last column is a special case - tile width must be adjusted.
            if tile_col == last_col:
                tile_width = num_cols - (max_tile_size * tile_col)

            # tile_ulx and tile_uly are the absolute coordinates of the upper left corner of the tile.
            tile_ulx = aoi_xmin + x_offset * pixel_size
            tile_uly = aoi_ymax - y_offset * pixel_size
            tile_lrx = tile_ulx + tile_width * pixel_size
            tile_lry = tile_uly - tile_height * pixel_size

            tile_work_dir = tiles_parentdir.joinpath("tile_{:03d}_{:03d}".format(
                tile_row + 1, tile_col + 1))
            tile_work_dir.mkdir(parents=True, exist_ok=True)

            tile_multiband_composite = tile_work_dir.joinpath("tile_{:03d}_{:03d}.tif".format(tile_row + 1, tile_col + 1))

            tile_info = Tiles(
                row= tile_row,
                col= tile_col,
                width= tile_width,
                height= tile_height,
                x_offset= x_offset,
                y_offset= y_offset,
                xmin= tile_ulx,
                xmax= tile_lrx,
                ymin= tile_lry,
                ymax= tile_uly,
                pixel_size= pixel_size,
                tile_folder= tile_work_dir,
                tile_multiband_composite = tile_multiband_composite
            )
            tile_infos.append(tile_info)
    return tile_infos

def cut_composite_totile_function(input_data):
    src_filepath = input_data[0]
    tile_extent_path_dict_json = input_data[1]

    tile_infos = json.loads(tile_extent_path_dict_json)

    for tile_name, tile_info in tile_infos.items():
        tile_composite_filepath = Path(tile_info['tile_folder']).joinpath(Path(src_filepath).name)
        if tile_composite_filepath.exists(): continue
        cmd_gdal = ["gdal_translate",
                    "-of", "GTiff",
                    "-co", "COMPRESS=DEFLATE",
                    "-co", "BIGTIFF=YES",
                    "-co", "TILED=YES",
                    "-eco", "-projwin",
                    "{}".format(tile_info['ulx']), "{}".format(tile_info['uly']),
                    "{}".format(tile_info['lrx']), "{}".format(tile_info['lry']),
                    str(src_filepath), str(tile_composite_filepath)]
        cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.debug(f"exit code {cmd_output.returncode} --> {cmd_gdal}")
