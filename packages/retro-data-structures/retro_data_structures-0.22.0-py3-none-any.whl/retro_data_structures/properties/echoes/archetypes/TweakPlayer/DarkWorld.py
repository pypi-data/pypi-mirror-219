# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo


@dataclasses.dataclass()
class DarkWorld(BaseProperty):
    damage_grace_period: float = dataclasses.field(default=2.0)
    unknown_0xa4e33ef0: float = dataclasses.field(default=4.0)
    damage_per_second: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    dark_suit_damage_reduction: float = dataclasses.field(default=1.0)
    unknown_0xee452490: float = dataclasses.field(default=0.3499999940395355)
    unknown_0x19275a97: float = dataclasses.field(default=0.5)

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

        data.write(b'I\x85\xbcs')  # 0x4985bc73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_grace_period))

        data.write(b'\xa4\xe3>\xf0')  # 0xa4e33ef0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa4e33ef0))

        data.write(b'\xf9\xbfY\xa2')  # 0xf9bf59a2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_per_second.to_stream(data, default_override={'di_weapon_type': 17})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3;uI')  # 0x333b7549
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dark_suit_damage_reduction))

        data.write(b'\xeeE$\x90')  # 0xee452490
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xee452490))

        data.write(b"\x19'Z\x97")  # 0x19275a97
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x19275a97))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            damage_grace_period=data['damage_grace_period'],
            unknown_0xa4e33ef0=data['unknown_0xa4e33ef0'],
            damage_per_second=DamageInfo.from_json(data['damage_per_second']),
            dark_suit_damage_reduction=data['dark_suit_damage_reduction'],
            unknown_0xee452490=data['unknown_0xee452490'],
            unknown_0x19275a97=data['unknown_0x19275a97'],
        )

    def to_json(self) -> dict:
        return {
            'damage_grace_period': self.damage_grace_period,
            'unknown_0xa4e33ef0': self.unknown_0xa4e33ef0,
            'damage_per_second': self.damage_per_second.to_json(),
            'dark_suit_damage_reduction': self.dark_suit_damage_reduction,
            'unknown_0xee452490': self.unknown_0xee452490,
            'unknown_0x19275a97': self.unknown_0x19275a97,
        }

    def _dependencies_for_damage_per_second(self, asset_manager):
        yield from self.damage_per_second.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_damage_per_second, "damage_per_second", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DarkWorld.{field_name} ({field_type}): {e}"
                )


def _decode_damage_grace_period(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa4e33ef0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_per_second(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 17})


def _decode_dark_suit_damage_reduction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xee452490(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x19275a97(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4985bc73: ('damage_grace_period', _decode_damage_grace_period),
    0xa4e33ef0: ('unknown_0xa4e33ef0', _decode_unknown_0xa4e33ef0),
    0xf9bf59a2: ('damage_per_second', _decode_damage_per_second),
    0x333b7549: ('dark_suit_damage_reduction', _decode_dark_suit_damage_reduction),
    0xee452490: ('unknown_0xee452490', _decode_unknown_0xee452490),
    0x19275a97: ('unknown_0x19275a97', _decode_unknown_0x19275a97),
}
