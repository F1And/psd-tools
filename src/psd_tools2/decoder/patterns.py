"""
Patterns structure.
"""
from __future__ import absolute_import, unicode_literals
import attr
import io
import logging

from psd_tools2.constants import ColorMode
from psd_tools2.decoder.base import BaseElement, ListElement
from psd_tools2.validators import in_
from psd_tools2.utils import (
    read_fmt, write_fmt, read_length_block, write_length_block, is_readable,
    write_bytes, read_unicode_string, write_unicode_string,
    read_pascal_string, write_pascal_string,
)

logger = logging.getLogger(__name__)


class Patterns(ListElement):
    """
    List of Pattern structure. See
    :py:class:`~psd_tools2.decoder.patterns.Pattern`.
    """
    @classmethod
    def read(cls, fp, **kwargs):
        items = []
        while is_readable(fp, 4):
            data = read_length_block(fp, padding=4)
            with io.BytesIO(data) as f:
                items.append(Pattern.read(f))
        return cls(items)

    def write(self, fp, **kwargs):
        written = 0
        for item in self:
            written += write_length_block(fp, lambda f: item.write(f),
                                          padding=4)
        return written


@attr.s
class Pattern(BaseElement):
    """
    Pattern structure.

    .. py:attribute:: version
    .. py:attribute:: image_mode
    .. py:attribute:: point
    .. py:attribute:: name
    .. py:attribute:: pattern_id
    .. py:attribute:: color_table
    .. py:attribute:: data
    """
    version = attr.ib(default=1, type=int)
    image_mode = attr.ib(default=ColorMode, converter=ColorMode,
                         validator=in_(ColorMode))
    point = attr.ib(default=None)
    name = attr.ib(default='', type=str)
    pattern_id = attr.ib(default='', type=str)
    color_table = attr.ib(default=None)
    data = attr.ib(default=None)

    @classmethod
    def read(cls, fp, **kwargs):
        version = read_fmt('I', fp)[0]
        assert version == 1, 'Invalid version %d' % (version)
        image_mode = ColorMode(read_fmt('I', fp)[0])
        point = read_fmt('2h', fp)
        name = read_unicode_string(fp)
        pattern_id = read_pascal_string(fp, encoding='ascii', padding=1)
        color_table = None
        if image_mode == ColorMode.INDEXED:
            color_table = [read_fmt("3B", fp) for i in range(256)]
            read_fmt('4x', fp)

        data = VirtualMemoryArrayList.read(fp)
        return cls(version, image_mode, point, name, pattern_id, color_table,
                   data)

    def write(self, fp, **kwargs):
        written = write_fmt(fp, '2I', self.version, self.image_mode.value)
        written += write_fmt(fp, '2h', *self.point)
        written += write_unicode_string(fp, self.name)
        written += write_pascal_string(fp, self.pattern_id, encoding='ascii',
                                       padding=1)
        if self.color_table:
            for row in self.color_table:
                written += write_fmt(fp, '3B', *row)
            written += write_fmt(fp, '4x')
        written += self.data.write(fp)
        return written


@attr.s
class VirtualMemoryArrayList(BaseElement):
    """
    VirtualMemoryArrayList structure.

    .. py:attribute:: version
    .. py:attribute:: rectangle
    .. py:attribute:: channels
    """
    version = attr.ib(default=3, type=int)
    rectangle = attr.ib(default=None)
    channels = attr.ib(default=None)

    @classmethod
    def read(cls, fp, **kwargs):
        version = read_fmt('I', fp)[0]
        assert version == 3, 'Invalid version %d' % (version)

        data = read_length_block(fp)
        with io.BytesIO(data) as f:
            rectangle = read_fmt('4I', f)
            num_channels = read_fmt('I', f)[0]
            channels = []
            for _ in range(num_channels + 2):
                channels.append(VirtualMemoryArray.read(f))

        return cls(version, rectangle, channels)

    def write(self, fp, **kwargs):
        written = write_fmt(fp, 'I', self.version)
        return written + write_length_block(fp, lambda f: self._write_body(f))

    def _write_body(self, fp):
        written = write_fmt(fp, '4I', *self.rectangle)
        written += write_fmt(fp, 'I', len(self.channels) - 2)
        for channel in self.channels:
            written += channel.write(fp)
        return written


@attr.s
class VirtualMemoryArray(BaseElement):
    """
    VirtualMemoryArrayList structure.

    .. py:attribute:: is_written
    .. py:attribute:: depth
    .. py:attribute:: rectangle
    .. py:attribute:: pixel_depth
    .. py:attribute:: compression
    .. py:attribute:: data
    """
    is_written = attr.ib(default=0)
    depth = attr.ib(default=None)
    rectangle = attr.ib(default=None)
    pixel_depth = attr.ib(default=None)
    compression = attr.ib(default=None)
    data = attr.ib(default=b'')

    @classmethod
    def read(cls, fp, **kwargs):
        is_written = read_fmt('I', fp)[0]
        if is_written == 0:
            return cls(is_written=is_written)
        length = read_fmt('I', fp)[0]
        if length == 0:
            return cls(is_written=is_written)
        depth = read_fmt('I', fp)[0]
        rectangle = read_fmt('4I', fp)
        pixel_depth, compression = read_fmt('HB', fp)
        data = fp.read(length - 23)
        return cls(
            is_written, depth, rectangle, pixel_depth, compression, data
        )

    def write(self, fp, **kwargs):
        written = write_fmt(fp, 'I', self.is_written)
        if self.is_written == 0:
            return written
        if self.depth is None:
            written += write_fmt(fp, 'I', 0)
            return written

        return written + write_length_block(fp, lambda f: self._write_body(f))

    def _write_body(self, fp):
        written = write_fmt(fp, 'I', self.depth)
        written += write_fmt(fp, '4I', *self.rectangle)
        written += write_fmt(fp, 'HB', self.pixel_depth, self.compression)
        written += write_bytes(fp, self.data)
        return written
