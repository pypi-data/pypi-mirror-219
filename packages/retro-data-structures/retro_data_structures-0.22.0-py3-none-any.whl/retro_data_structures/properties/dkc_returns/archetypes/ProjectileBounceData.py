# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class ProjectileBounceData(BaseProperty):
    unknown_0x96b863c5: int = dataclasses.field(default=1)
    bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x76c79503: float = dataclasses.field(default=1.0)
    bounce_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x8ec68a96: bool = dataclasses.field(default=False)
    unknown_0xec56e80d: float = dataclasses.field(default=1.0)
    unknown_0x8e55276e: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=0.0))

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x96\xb8c\xc5')  # 0x96b863c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x96b863c5))

        data.write(b'\xf1\x92Uv')  # 0xf1925576
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_sound))

        data.write(b'v\xc7\x95\x03')  # 0x76c79503
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76c79503))

        data.write(b'!|7\xc2')  # 0x217c37c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_particle_effect))

        data.write(b'\x8e\xc6\x8a\x96')  # 0x8ec68a96
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8ec68a96))

        data.write(b'\xecV\xe8\r')  # 0xec56e80d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xec56e80d))

        data.write(b"\x8eU'n")  # 0x8e55276e
        data.write(b'\x00\x0c')  # size
        self.unknown_0x8e55276e.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x96b863c5=data['unknown_0x96b863c5'],
            bounce_sound=data['bounce_sound'],
            unknown_0x76c79503=data['unknown_0x76c79503'],
            bounce_particle_effect=data['bounce_particle_effect'],
            unknown_0x8ec68a96=data['unknown_0x8ec68a96'],
            unknown_0xec56e80d=data['unknown_0xec56e80d'],
            unknown_0x8e55276e=Vector.from_json(data['unknown_0x8e55276e']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x96b863c5': self.unknown_0x96b863c5,
            'bounce_sound': self.bounce_sound,
            'unknown_0x76c79503': self.unknown_0x76c79503,
            'bounce_particle_effect': self.bounce_particle_effect,
            'unknown_0x8ec68a96': self.unknown_0x8ec68a96,
            'unknown_0xec56e80d': self.unknown_0xec56e80d,
            'unknown_0x8e55276e': self.unknown_0x8e55276e.to_json(),
        }


def _decode_unknown_0x96b863c5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x76c79503(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x8ec68a96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xec56e80d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8e55276e(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x96b863c5: ('unknown_0x96b863c5', _decode_unknown_0x96b863c5),
    0xf1925576: ('bounce_sound', _decode_bounce_sound),
    0x76c79503: ('unknown_0x76c79503', _decode_unknown_0x76c79503),
    0x217c37c2: ('bounce_particle_effect', _decode_bounce_particle_effect),
    0x8ec68a96: ('unknown_0x8ec68a96', _decode_unknown_0x8ec68a96),
    0xec56e80d: ('unknown_0xec56e80d', _decode_unknown_0xec56e80d),
    0x8e55276e: ('unknown_0x8e55276e', _decode_unknown_0x8e55276e),
}
