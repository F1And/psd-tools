from __future__ import absolute_import, unicode_literals
import pytest

from psd_tools.constants import Resource
from psd_tools.psd.image_resources import ImageResources, ImageResource
from IPython.display import display

from ..utils import check_read_write, check_write_read


def test_image_resources_from_to():
    check_read_write(ImageResources, b'\x00\x00\x00\x00')


def test_image_resources_exception():
    with pytest.raises(AssertionError):
        ImageResources.frombytes(b'\x00\x00\x00\x01')


def test_image_resources_dict():
    image_resources = ImageResources.new()
    display(image_resources)
    assert image_resources.get_data(Resource.VERSION_INFO)
    assert image_resources.get_data(Resource.OBSOLETE1) is None
    assert len([1 for key in image_resources
                if key == Resource.VERSION_INFO]) == 1


@pytest.mark.parametrize(['fixture'], [
    (ImageResource(name='', data=b'\x01\x04\x02'), ),
    (ImageResource(name='foo', data=b'\x01\x04\x02'), ),
])
def test_image_resource_from_to(fixture):
    check_write_read(fixture)


def test_image_resource_exception():
    with pytest.raises(AssertionError):
        ImageResource.frombytes(b'\x00\x00\x00\x01')
