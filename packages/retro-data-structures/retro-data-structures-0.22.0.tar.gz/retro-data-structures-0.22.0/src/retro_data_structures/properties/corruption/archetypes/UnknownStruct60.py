# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct60(BaseProperty):
    scale: float = dataclasses.field(default=1.0)
    effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    collision_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b',Q\xa6v')  # 0x2c51a676
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scale))

        data.write(b'\xb6\x8cm\x96')  # 0xb68c6d96
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.effect))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':>\x03\xba')  # 0x3a3e03ba
        data.write(b'\x00\x0c')  # size
        self.collision_size.to_stream(data)

        data.write(b'\xa5]\xac\xf6')  # 0xa55dacf6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scale=data['scale'],
            effect=data['effect'],
            damage=DamageInfo.from_json(data['damage']),
            collision_size=Vector.from_json(data['collision_size']),
            sound=data['sound'],
        )

    def to_json(self) -> dict:
        return {
            'scale': self.scale,
            'effect': self.effect,
            'damage': self.damage.to_json(),
            'collision_size': self.collision_size.to_json(),
            'sound': self.sound,
        }


def _decode_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_collision_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2c51a676: ('scale', _decode_scale),
    0xb68c6d96: ('effect', _decode_effect),
    0x337f9524: ('damage', _decode_damage),
    0x3a3e03ba: ('collision_size', _decode_collision_size),
    0xa55dacf6: ('sound', _decode_sound),
}
