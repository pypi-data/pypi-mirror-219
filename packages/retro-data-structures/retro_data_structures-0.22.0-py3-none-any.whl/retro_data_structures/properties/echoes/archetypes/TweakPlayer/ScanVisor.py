# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class ScanVisor(BaseProperty):
    scan_distance: float = dataclasses.field(default=50.0)
    scan_retention: bool = dataclasses.field(default=True)
    scan_freezes_game: bool = dataclasses.field(default=True)
    scan_line_of_sight: bool = dataclasses.field(default=True)
    scan_max_target_distance: float = dataclasses.field(default=100.0)
    scan_max_lock_distance: float = dataclasses.field(default=100.0)
    scan_camera_speed: float = dataclasses.field(default=30.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xb0\xa3.[')  # 0xb0a32e5b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_distance))

        data.write(b'*u\xf2\xb8')  # 0x2a75f2b8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scan_retention))

        data.write(b'\x05\x82\x84\xbb')  # 0x58284bb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scan_freezes_game))

        data.write(b'\x1eT\xf5\xae')  # 0x1e54f5ae
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scan_line_of_sight))

        data.write(b'\xad\xfa\x90\xfc')  # 0xadfa90fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_max_target_distance))

        data.write(b'\xf4\xdb\x84\xa9')  # 0xf4db84a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_max_lock_distance))

        data.write(b'\x8a{$_')  # 0x8a7b245f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_camera_speed))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_distance=data['scan_distance'],
            scan_retention=data['scan_retention'],
            scan_freezes_game=data['scan_freezes_game'],
            scan_line_of_sight=data['scan_line_of_sight'],
            scan_max_target_distance=data['scan_max_target_distance'],
            scan_max_lock_distance=data['scan_max_lock_distance'],
            scan_camera_speed=data['scan_camera_speed'],
        )

    def to_json(self) -> dict:
        return {
            'scan_distance': self.scan_distance,
            'scan_retention': self.scan_retention,
            'scan_freezes_game': self.scan_freezes_game,
            'scan_line_of_sight': self.scan_line_of_sight,
            'scan_max_target_distance': self.scan_max_target_distance,
            'scan_max_lock_distance': self.scan_max_lock_distance,
            'scan_camera_speed': self.scan_camera_speed,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xb0a32e5b, 0x2a75f2b8, 0x58284bb, 0x1e54f5ae, 0xadfa90fc, 0xf4db84a9, 0x8a7b245f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ScanVisor]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLH?LH?LH?LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(61))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return ScanVisor(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_scan_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_retention(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scan_freezes_game(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scan_line_of_sight(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scan_max_target_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_max_lock_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_camera_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb0a32e5b: ('scan_distance', _decode_scan_distance),
    0x2a75f2b8: ('scan_retention', _decode_scan_retention),
    0x58284bb: ('scan_freezes_game', _decode_scan_freezes_game),
    0x1e54f5ae: ('scan_line_of_sight', _decode_scan_line_of_sight),
    0xadfa90fc: ('scan_max_target_distance', _decode_scan_max_target_distance),
    0xf4db84a9: ('scan_max_lock_distance', _decode_scan_max_lock_distance),
    0x8a7b245f: ('scan_camera_speed', _decode_scan_camera_speed),
}
