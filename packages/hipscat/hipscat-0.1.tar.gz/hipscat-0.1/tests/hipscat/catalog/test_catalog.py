"""Tests of catalog functionality"""

import os

import pandas.testing
import pytest

from hipscat.catalog import Catalog, CatalogType, PartitionInfo
from hipscat.pixel_tree.pixel_node_type import PixelNodeType


def test_catalog_load(catalog_info, catalog_pixels):
    catalog = Catalog(catalog_info, catalog_pixels)
    assert len(catalog.get_pixels()) == catalog_pixels.shape[0]
    assert catalog.catalog_name == catalog_info.catalog_name
    for _, pixel in catalog_pixels.iterrows():
        order = pixel[PartitionInfo.METADATA_ORDER_COLUMN_NAME]
        pixel = pixel[PartitionInfo.METADATA_PIXEL_COLUMN_NAME]
        assert (order, pixel) in catalog.pixel_tree
        assert catalog.pixel_tree[(order, pixel)].node_type == PixelNodeType.LEAF


def test_catalog_load_wrong_catalog_info(base_catalog_info, catalog_pixels):
    with pytest.raises(TypeError):
        Catalog(base_catalog_info, catalog_pixels)


def test_catalog_wrong_catalog_type(catalog_info, catalog_pixels):
    catalog_info.catalog_type = CatalogType.INDEX
    with pytest.raises(ValueError):
        Catalog(catalog_info, catalog_pixels)


def test_different_pixel_input_types(catalog_info, catalog_pixels):
    partition_info = PartitionInfo(catalog_pixels)
    catalog = Catalog(catalog_info, partition_info)
    assert len(catalog.get_pixels()) == catalog_pixels.shape[0]
    for _, pixel in catalog_pixels.iterrows():
        order = pixel[PartitionInfo.METADATA_ORDER_COLUMN_NAME]
        pixel = pixel[PartitionInfo.METADATA_PIXEL_COLUMN_NAME]
        assert (order, pixel) in catalog.pixel_tree
        assert catalog.pixel_tree[(order, pixel)].node_type == PixelNodeType.LEAF


def test_wrong_pixel_input_type(catalog_info):
    with pytest.raises(TypeError):
        Catalog(catalog_info, "test")
    with pytest.raises(TypeError):
        Catalog._get_pixel_tree_from_pixels("test")
    with pytest.raises(TypeError):
        Catalog._get_partition_info_from_pixels("test")


def test_get_pixels(catalog_info, catalog_pixels):
    catalog = Catalog(catalog_info, catalog_pixels)
    pixels = catalog.get_pixels()
    pandas.testing.assert_frame_equal(pixels, catalog_pixels)


def test_load_catalog_small_sky(small_sky_dir):
    """Instantiate a catalog with 1 pixel"""
    cat = Catalog.read_from_hipscat(small_sky_dir)

    assert cat.catalog_name == "small_sky"
    assert len(cat.get_pixels()) == 1


def test_load_catalog_small_sky_order1(small_sky_order1_dir):
    """Instantiate a catalog with 4 pixels"""
    cat = Catalog.read_from_hipscat(small_sky_order1_dir)

    assert cat.catalog_name == "small_sky_order1"
    assert len(cat.get_pixels()) == 4


def test_empty_directory(tmp_path):
    """Test loading empty or incomplete data"""
    ## Path doesn't exist
    with pytest.raises(FileNotFoundError):
        Catalog.read_from_hipscat(os.path.join("path", "empty"))

    catalog_path = os.path.join(tmp_path, "empty")
    os.makedirs(catalog_path, exist_ok=True)

    ## Path exists but there's nothing there
    with pytest.raises(FileNotFoundError):
        Catalog.read_from_hipscat(catalog_path)

    ## catalog_info file exists - getting closer
    file_name = os.path.join(catalog_path, "catalog_info.json")
    with open(file_name, "w", encoding="utf-8") as metadata_file:
        metadata_file.write('{"catalog_name":"empty", "catalog_type":"source"}')

    with pytest.raises(FileNotFoundError):
        Catalog.read_from_hipscat(catalog_path)

    ## partition_info file exists - enough to create a catalog
    file_name = os.path.join(catalog_path, "partition_info.csv")
    with open(file_name, "w", encoding="utf-8") as metadata_file:
        metadata_file.write("foo")

    catalog = Catalog.read_from_hipscat(catalog_path)
    assert catalog.catalog_name == "empty"
