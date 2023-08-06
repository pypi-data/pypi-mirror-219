import logging
import os
import datetime
import mimetypes
import pystac

from abc import ABC, abstractmethod

from pystac.extensions.datacube import HorizontalSpatialDimension, TemporalDimension, Dimension, \
    VerticalSpatialDimension, Variable

from stac_cat_utils.utils import collection_to_assets, is_datacube_compliant, cube_extend, is_key_unique, remove_empty_key

logger = logging.getLogger('StacCatalogGenerator')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class STACABC(ABC):
    @abstractmethod
    def add_stac_element(self, element):
        pass


class STACCollection(pystac.Collection, STACABC):
    def add_stac_element(self, element):
        if isinstance(element, pystac.Asset):
            self.add_asset(element.title, element)
        elif isinstance(element, pystac.Item):
            self.add_item(element)
        elif isinstance(element, pystac.Collection):
            self.add_child(element)
        if len(list(self.get_all_items())):
            self.update_extent_from_items()

    def make_datacube_compliant(self):
        col_cube_compliance = is_datacube_compliant(self)
        if not col_cube_compliance[0]:
            logger.error(f'{self} is not Datacube compliant')
            return
        bands = list(set([v['name'] for v in col_cube_compliance[1]]))
        col_bbox = self.extent.spatial.bboxes[0]
        col_temp = self.extent.temporal.to_dict()
        cube_collection = cube_extend(self, 'dimensions')
        cube_collection.dimensions = {
            **cube_collection.dimensions,
            'x': HorizontalSpatialDimension({
                'type': 'spatial', 'axis': 'x', 'extent': [col_bbox[0], col_bbox[2]], 'reference_system': 4326
            }),
            'y': HorizontalSpatialDimension({
                'type': 'spatial', 'axis': 'y', 'extent': [col_bbox[1], col_bbox[3]], 'reference_system': 4326
            }),
            'time': TemporalDimension({'type': 'temporal', 'extent': col_temp}),
            'spectral': Dimension({'type': 'bands', 'values': bands})
        }

    def add_temporal_dimension(
        self, name, extent, values=None, step=None, description=None, replace=False
    ):
        if not extent:
            logger.error('A Temporal Dimension MUST specify an extent')
            return
        cube_collection = cube_extend(self, 'dimensions')
        if is_key_unique(cube_collection, name) or replace:
            cube_collection.dimensions = {
                **cube_collection.dimensions,
                f'{name}': TemporalDimension(remove_empty_key({
                    'type': 'temporal',
                    'extent': extent,
                    'step': step,
                    'description': description,
                    'values': values
                }))
            }

    def add_horizontal_dimension(
        self, name, axis, extent=None, values=None, step=None, unit=None, description=None, reference_system=4326
    ):
        if not extent or axis not in ['x', 'y']:
            logger.error('A Vertical Dimension MUST specify an extent and an axis between "x" and "y".')
            return
        cube_collection = cube_extend(self, 'dimensions')
        if is_key_unique(cube_collection, name):
            cube_collection.dimensions = {
                **cube_collection.dimensions,
                f'{name}': HorizontalSpatialDimension(remove_empty_key({
                    'type': 'spatial',
                    'axis': axis,
                    'extent': extent,
                    'values': values,
                    'step': step,
                    'unit': unit,
                    'description': description,
                    'reference_system': reference_system,
                }))
            }

    def add_vertical_dimension(
        self, name, extent=None, values=None, step=None, unit=None, description=None, reference_system=4326
    ):
        if not extent and not values:
            logger.error('A Vertical Dimension MUST specify an extent or values. It MAY also specify both.')
            return
        cube_collection = cube_extend(self, 'dimensions')
        if is_key_unique(cube_collection, name):
            cube_collection.dimensions = {
                **cube_collection.dimensions,
                f'{name}': VerticalSpatialDimension(remove_empty_key({
                    'type': 'spatial',
                    'axis': 'z',
                    'extent': extent,
                    'values': values,
                    'step': step,
                    'unit': unit,
                    'description': description,
                    'reference_system': reference_system,
                }))
            }

    def add_additional_dimension(
        self, name, type=None, extent=None, values=None, step=None, unit=None, description=None, reference_system=4326
    ):
        if not type or (not extent and not values):
            logger.error('type is required')
            return
        cube_collection = cube_extend(self, 'dimensions')
        if is_key_unique(cube_collection, name):
            cube_collection.dimensions = {
                **cube_collection.dimensions,
                f'{name}': Dimension(remove_empty_key({
                    'type': type,
                    'extent': extent,
                    'values': values,
                    'step': step,
                    'unit': unit,
                    'description': description,
                    'reference_system': reference_system,
                }))
            }

    def add_dimension_variable(
        self, name, type=None, dimensions=None, description=None, extent=None, values=None, unit=None
    ):
        if not type or type not in ['data', 'auxiliary']:
            logger.error('type is required')
            return
        cube_collection = cube_extend(self, 'dimensions')
        cube_collection = cube_extend(cube_collection, 'variables')

        if is_key_unique(cube_collection, name):
            cube_collection.variables = {
                **cube_collection.variables,
                f'{name}': Variable(remove_empty_key({
                    'type': type,
                    'dimensions': dimensions,
                    'extent': extent,
                    'values': values,
                    'unit': unit,
                    'description': description,
                }))
            }


class STACItem(pystac.Item, STACABC):
    def add_stac_element(self, element):
        if isinstance(element, pystac.Asset):
            self.add_asset(element.title, element)
        elif isinstance(element, pystac.Item):
            self.assets = {**self.assets, **element.assets}
        else:
            self.assets = {**self.assets, **collection_to_assets(element)}


class STACCatalog(pystac.Catalog, STACABC):
    def add_stac_element(self, element):
        if isinstance(element, pystac.Item):
            self.add_item(element)
        elif isinstance(element, pystac.Collection):
            self.add_child(element)

    def make_datacube_compliant(self):
        for collection in self.get_all_collections():
            try:
                collection.make_datacube_compliant()
            except Exception:
                continue


MEDIA_TYPES = {
    '.json': pystac.MediaType.JSON,
    '.txt': pystac.MediaType.TEXT,
    '.text': pystac.MediaType.TEXT,
    '.pdf': pystac.MediaType.PDF,
    '.xml': pystac.MediaType.XML,
    '.htm': pystac.MediaType.HTML,
    '.html': pystac.MediaType.HTML,
    '.yaml': 'text/yaml',
    '.yml': 'text/yaml',
    '.csv': 'text/csv',
}


def _get_file_creation_date(path):
    c_time = os.path.getctime(path)
    return datetime.datetime.fromtimestamp(c_time)


def create_generic_asset(href):
    _, extension = os.path.splitext(href)
    file_dt_creation = _get_file_creation_date(href)
    if extension.lower() in MEDIA_TYPES:
        file_media_type = MEDIA_TYPES[extension.lower()]
    else:
        file_media_type = mimetypes.guess_type(href)
    file_asset = pystac.Asset(href=href,
                              title=href,
                              media_type=file_media_type,
                              extra_fields={'Creation': file_dt_creation.strftime('%Y-%m-%d %H:%M')},
                              roles=['data'])
    return file_asset
