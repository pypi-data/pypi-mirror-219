# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class Scan(BaseProperty):
    scan_lock_scale: float = dataclasses.field(default=1.0)
    scan_lock_transition_time: float = dataclasses.field(default=0.30000001192092896)
    scan_lock_translation: float = dataclasses.field(default=1.0)
    unknown: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_lock_locked_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_lock_unlocked_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xa0\x85{n')  # 0xa0857b6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_lock_scale))

        data.write(b'\xa4\xcc\xe3\x0f')  # 0xa4cce30f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_lock_transition_time))

        data.write(b'\x8e\x9b\xfe\xa3')  # 0x8e9bfea3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_lock_translation))

        data.write(b'v\x81\x10\xcd')  # 0x768110cd
        data.write(b'\x00\x10')  # size
        self.unknown.to_stream(data)

        data.write(b'1\x9f\x96k')  # 0x319f966b
        data.write(b'\x00\x10')  # size
        self.scan_lock_locked_color.to_stream(data)

        data.write(b'\xa8\x1f7\x8c')  # 0xa81f378c
        data.write(b'\x00\x10')  # size
        self.scan_lock_unlocked_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_lock_scale=data['scan_lock_scale'],
            scan_lock_transition_time=data['scan_lock_transition_time'],
            scan_lock_translation=data['scan_lock_translation'],
            unknown=Color.from_json(data['unknown']),
            scan_lock_locked_color=Color.from_json(data['scan_lock_locked_color']),
            scan_lock_unlocked_color=Color.from_json(data['scan_lock_unlocked_color']),
        )

    def to_json(self) -> dict:
        return {
            'scan_lock_scale': self.scan_lock_scale,
            'scan_lock_transition_time': self.scan_lock_transition_time,
            'scan_lock_translation': self.scan_lock_translation,
            'unknown': self.unknown.to_json(),
            'scan_lock_locked_color': self.scan_lock_locked_color.to_json(),
            'scan_lock_unlocked_color': self.scan_lock_unlocked_color.to_json(),
        }


def _decode_scan_lock_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_lock_transition_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_lock_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_lock_locked_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_lock_unlocked_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa0857b6e: ('scan_lock_scale', _decode_scan_lock_scale),
    0xa4cce30f: ('scan_lock_transition_time', _decode_scan_lock_transition_time),
    0x8e9bfea3: ('scan_lock_translation', _decode_scan_lock_translation),
    0x768110cd: ('unknown', _decode_unknown),
    0x319f966b: ('scan_lock_locked_color', _decode_scan_lock_locked_color),
    0xa81f378c: ('scan_lock_unlocked_color', _decode_scan_lock_unlocked_color),
}
