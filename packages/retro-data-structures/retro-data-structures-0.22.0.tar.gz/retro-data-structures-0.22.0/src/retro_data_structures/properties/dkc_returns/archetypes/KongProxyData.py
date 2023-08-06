# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class KongProxyData(BaseProperty):
    unknown_0x9445eea3: bool = dataclasses.field(default=False)
    unknown_0x80bc66ea: bool = dataclasses.field(default=False)
    unknown_0x30060f67: int = dataclasses.field(default=0)
    unknown_0x2f026a4f: int = dataclasses.field(default=0)
    gravity_multiplier: float = dataclasses.field(default=0.5)
    unknown_0x653fba4a: float = dataclasses.field(default=1.0)
    maximum_run_speed: float = dataclasses.field(default=9.0)
    acceleration: float = dataclasses.field(default=20.0)
    unknown_0x14e317bd: Vector = dataclasses.field(default_factory=lambda: Vector(x=32.0, y=12.0, z=24.0))

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x94E\xee\xa3')  # 0x9445eea3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9445eea3))

        data.write(b'\x80\xbcf\xea')  # 0x80bc66ea
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x80bc66ea))

        data.write(b'0\x06\x0fg')  # 0x30060f67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x30060f67))

        data.write(b'/\x02jO')  # 0x2f026a4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x2f026a4f))

        data.write(b'B\xacB\xea')  # 0x42ac42ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_multiplier))

        data.write(b'e?\xbaJ')  # 0x653fba4a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x653fba4a))

        data.write(b'\x95\n{\x96')  # 0x950a7b96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_run_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x14\xe3\x17\xbd')  # 0x14e317bd
        data.write(b'\x00\x0c')  # size
        self.unknown_0x14e317bd.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x9445eea3=data['unknown_0x9445eea3'],
            unknown_0x80bc66ea=data['unknown_0x80bc66ea'],
            unknown_0x30060f67=data['unknown_0x30060f67'],
            unknown_0x2f026a4f=data['unknown_0x2f026a4f'],
            gravity_multiplier=data['gravity_multiplier'],
            unknown_0x653fba4a=data['unknown_0x653fba4a'],
            maximum_run_speed=data['maximum_run_speed'],
            acceleration=data['acceleration'],
            unknown_0x14e317bd=Vector.from_json(data['unknown_0x14e317bd']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x9445eea3': self.unknown_0x9445eea3,
            'unknown_0x80bc66ea': self.unknown_0x80bc66ea,
            'unknown_0x30060f67': self.unknown_0x30060f67,
            'unknown_0x2f026a4f': self.unknown_0x2f026a4f,
            'gravity_multiplier': self.gravity_multiplier,
            'unknown_0x653fba4a': self.unknown_0x653fba4a,
            'maximum_run_speed': self.maximum_run_speed,
            'acceleration': self.acceleration,
            'unknown_0x14e317bd': self.unknown_0x14e317bd.to_json(),
        }


def _decode_unknown_0x9445eea3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x80bc66ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x30060f67(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2f026a4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_gravity_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x653fba4a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_run_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x14e317bd(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9445eea3: ('unknown_0x9445eea3', _decode_unknown_0x9445eea3),
    0x80bc66ea: ('unknown_0x80bc66ea', _decode_unknown_0x80bc66ea),
    0x30060f67: ('unknown_0x30060f67', _decode_unknown_0x30060f67),
    0x2f026a4f: ('unknown_0x2f026a4f', _decode_unknown_0x2f026a4f),
    0x42ac42ea: ('gravity_multiplier', _decode_gravity_multiplier),
    0x653fba4a: ('unknown_0x653fba4a', _decode_unknown_0x653fba4a),
    0x950a7b96: ('maximum_run_speed', _decode_maximum_run_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x14e317bd: ('unknown_0x14e317bd', _decode_unknown_0x14e317bd),
}
