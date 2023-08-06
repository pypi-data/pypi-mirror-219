# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct270 import UnknownStruct270


@dataclasses.dataclass()
class UnknownStruct271(BaseProperty):
    unknown_struct270: UnknownStruct270 = dataclasses.field(default_factory=UnknownStruct270)
    unknown: float = dataclasses.field(default=2.0)
    collision_offset: float = dataclasses.field(default=0.25)
    sink_speed: float = dataclasses.field(default=3.0)
    rise_speed: float = dataclasses.field(default=3.0)
    kill_threshold: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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

        data.write(b'q\x90f\xeb')  # 0x719066eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct270.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb\xa6\xa1\xd6')  # 0xfba6a1d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xb4\x82\x8a\x9f')  # 0xb4828a9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_offset))

        data.write(b'19\xc1e')  # 0x3139c165
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sink_speed))

        data.write(b'l\xf7\xe7\x07')  # 0x6cf7e707
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rise_speed))

        data.write(b'\xf4\x1aW\xe6')  # 0xf41a57e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.kill_threshold))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct270=UnknownStruct270.from_json(data['unknown_struct270']),
            unknown=data['unknown'],
            collision_offset=data['collision_offset'],
            sink_speed=data['sink_speed'],
            rise_speed=data['rise_speed'],
            kill_threshold=data['kill_threshold'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct270': self.unknown_struct270.to_json(),
            'unknown': self.unknown,
            'collision_offset': self.collision_offset,
            'sink_speed': self.sink_speed,
            'rise_speed': self.rise_speed,
            'kill_threshold': self.kill_threshold,
        }


def _decode_unknown_struct270(data: typing.BinaryIO, property_size: int):
    return UnknownStruct270.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sink_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rise_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_kill_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x719066eb: ('unknown_struct270', _decode_unknown_struct270),
    0xfba6a1d6: ('unknown', _decode_unknown),
    0xb4828a9f: ('collision_offset', _decode_collision_offset),
    0x3139c165: ('sink_speed', _decode_sink_speed),
    0x6cf7e707: ('rise_speed', _decode_rise_speed),
    0xf41a57e6: ('kill_threshold', _decode_kill_threshold),
}
