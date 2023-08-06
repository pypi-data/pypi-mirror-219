# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class TidalWaveData(BaseProperty):
    adjust_each_frame: bool = dataclasses.field(default=False)
    offset_using: enums.OffsetUsing = dataclasses.field(default=enums.OffsetUsing.Unknown1)
    offset_plane: enums.OffsetPlane = dataclasses.field(default=enums.OffsetPlane.Unknown1)
    offset_u_coord: bool = dataclasses.field(default=True)
    offset_v_coord: bool = dataclasses.field(default=True)
    scale_using: enums.ScaleUsing = dataclasses.field(default=enums.ScaleUsing.Unknown1)
    scale_plane: enums.ScalePlane = dataclasses.field(default=enums.ScalePlane.Unknown1)
    scale_u_coord: bool = dataclasses.field(default=True)
    scale_v_coord: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xb4x?\x01')  # 0xb4783f01
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_each_frame))

        data.write(b'\xd3\x81\xe6>')  # 0xd381e63e
        data.write(b'\x00\x04')  # size
        self.offset_using.to_stream(data)

        data.write(b'u\xa2\x9d\xf1')  # 0x75a29df1
        data.write(b'\x00\x04')  # size
        self.offset_plane.to_stream(data)

        data.write(b'\xcc\xb52\xdb')  # 0xccb532db
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.offset_u_coord))

        data.write(b"'\x82\x89\xd8")  # 0x278289d8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.offset_v_coord))

        data.write(b'*\xc2\x1a\x04')  # 0x2ac21a04
        data.write(b'\x00\x04')  # size
        self.scale_using.to_stream(data)

        data.write(b'\x8c\xe1a\xcb')  # 0x8ce161cb
        data.write(b'\x00\x04')  # size
        self.scale_plane.to_stream(data)

        data.write(b'\n@\xa8\x95')  # 0xa40a895
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scale_u_coord))

        data.write(b'\xe1w\x13\x96')  # 0xe1771396
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scale_v_coord))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            adjust_each_frame=data['adjust_each_frame'],
            offset_using=enums.OffsetUsing.from_json(data['offset_using']),
            offset_plane=enums.OffsetPlane.from_json(data['offset_plane']),
            offset_u_coord=data['offset_u_coord'],
            offset_v_coord=data['offset_v_coord'],
            scale_using=enums.ScaleUsing.from_json(data['scale_using']),
            scale_plane=enums.ScalePlane.from_json(data['scale_plane']),
            scale_u_coord=data['scale_u_coord'],
            scale_v_coord=data['scale_v_coord'],
        )

    def to_json(self) -> dict:
        return {
            'adjust_each_frame': self.adjust_each_frame,
            'offset_using': self.offset_using.to_json(),
            'offset_plane': self.offset_plane.to_json(),
            'offset_u_coord': self.offset_u_coord,
            'offset_v_coord': self.offset_v_coord,
            'scale_using': self.scale_using.to_json(),
            'scale_plane': self.scale_plane.to_json(),
            'scale_u_coord': self.scale_u_coord,
            'scale_v_coord': self.scale_v_coord,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xb4783f01, 0xd381e63e, 0x75a29df1, 0xccb532db, 0x278289d8, 0x2ac21a04, 0x8ce161cb, 0xa40a895, 0xe1771396)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[TidalWaveData]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHLLHLLH?LH?LHLLHLLH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(75))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return TidalWaveData(
        dec[2],
        enums.OffsetUsing(dec[5]),
        enums.OffsetPlane(dec[8]),
        dec[11],
        dec[14],
        enums.ScaleUsing(dec[17]),
        enums.ScalePlane(dec[20]),
        dec[23],
        dec[26],
    )


def _decode_adjust_each_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offset_using(data: typing.BinaryIO, property_size: int):
    return enums.OffsetUsing.from_stream(data)


def _decode_offset_plane(data: typing.BinaryIO, property_size: int):
    return enums.OffsetPlane.from_stream(data)


def _decode_offset_u_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offset_v_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_using(data: typing.BinaryIO, property_size: int):
    return enums.ScaleUsing.from_stream(data)


def _decode_scale_plane(data: typing.BinaryIO, property_size: int):
    return enums.ScalePlane.from_stream(data)


def _decode_scale_u_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_v_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb4783f01: ('adjust_each_frame', _decode_adjust_each_frame),
    0xd381e63e: ('offset_using', _decode_offset_using),
    0x75a29df1: ('offset_plane', _decode_offset_plane),
    0xccb532db: ('offset_u_coord', _decode_offset_u_coord),
    0x278289d8: ('offset_v_coord', _decode_offset_v_coord),
    0x2ac21a04: ('scale_using', _decode_scale_using),
    0x8ce161cb: ('scale_plane', _decode_scale_plane),
    0xa40a895: ('scale_u_coord', _decode_scale_u_coord),
    0xe1771396: ('scale_v_coord', _decode_scale_v_coord),
}
