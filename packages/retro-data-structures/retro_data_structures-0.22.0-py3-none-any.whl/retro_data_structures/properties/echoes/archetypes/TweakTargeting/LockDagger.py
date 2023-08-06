# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class LockDagger(BaseProperty):
    lock_dagger_normal_scale: float = dataclasses.field(default=1.0)
    unknown: float = dataclasses.field(default=0.800000011920929)
    lock_dagger_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    lock_dagger0_angle: float = dataclasses.field(default=0.0)
    lock_dagger1_angle: float = dataclasses.field(default=120.0)
    lock_dagger2_angle: float = dataclasses.field(default=240.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'F\x95P\xe8')  # 0x469550e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_dagger_normal_scale))

        data.write(b'{H\xe6\xf9')  # 0x7b48e6f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'S\xc2\xc9\xfc')  # 0x53c2c9fc
        data.write(b'\x00\x10')  # size
        self.lock_dagger_color.to_stream(data)

        data.write(b'\xa2\x9c\xdf"')  # 0xa29cdf22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_dagger0_angle))

        data.write(b'c\x12\x00\xe2')  # 0x631200e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_dagger1_angle))

        data.write(b'\xfa\xf0f\xe3')  # 0xfaf066e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_dagger2_angle))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            lock_dagger_normal_scale=data['lock_dagger_normal_scale'],
            unknown=data['unknown'],
            lock_dagger_color=Color.from_json(data['lock_dagger_color']),
            lock_dagger0_angle=data['lock_dagger0_angle'],
            lock_dagger1_angle=data['lock_dagger1_angle'],
            lock_dagger2_angle=data['lock_dagger2_angle'],
        )

    def to_json(self) -> dict:
        return {
            'lock_dagger_normal_scale': self.lock_dagger_normal_scale,
            'unknown': self.unknown,
            'lock_dagger_color': self.lock_dagger_color.to_json(),
            'lock_dagger0_angle': self.lock_dagger0_angle,
            'lock_dagger1_angle': self.lock_dagger1_angle,
            'lock_dagger2_angle': self.lock_dagger2_angle,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_lock_dagger_normal_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_dagger_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_lock_dagger0_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_dagger1_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_dagger2_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x469550e8: ('lock_dagger_normal_scale', _decode_lock_dagger_normal_scale),
    0x7b48e6f9: ('unknown', _decode_unknown),
    0x53c2c9fc: ('lock_dagger_color', _decode_lock_dagger_color),
    0xa29cdf22: ('lock_dagger0_angle', _decode_lock_dagger0_angle),
    0x631200e2: ('lock_dagger1_angle', _decode_lock_dagger1_angle),
    0xfaf066e3: ('lock_dagger2_angle', _decode_lock_dagger2_angle),
}
