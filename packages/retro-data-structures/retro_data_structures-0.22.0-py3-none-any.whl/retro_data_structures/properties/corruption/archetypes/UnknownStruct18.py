# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct18(BaseProperty):
    column_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    column_trail_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    visor_effect_electric: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    unknown_0x01299e29: int = dataclasses.field(default=6)
    unknown_0x442bddab: int = dataclasses.field(default=6)
    column_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    cross_bar_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    column_damage_radius: float = dataclasses.field(default=3.0)
    initial_speed: float = dataclasses.field(default=35.0)
    acceleration: float = dataclasses.field(default=5.0)
    apex_shockwave_volume: float = dataclasses.field(default=1.0)
    unknown_0x4032c58a: float = dataclasses.field(default=2.5)
    unknown_0x8b6e162f: float = dataclasses.field(default=5.0)
    unknown_0x966b2697: float = dataclasses.field(default=9.0)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'L(\xcd\x13')  # 0x4c28cd13
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.column_effect))

        data.write(b'2\xa1=\xfd')  # 0x32a13dfd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.column_trail_effect))

        data.write(b'W\xf7\xef\xf9')  # 0x57f7eff9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc))

        data.write(b'\xfd\x13/p')  # 0xfd132f70
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect_electric))

        data.write(b'\x01)\x9e)')  # 0x1299e29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x01299e29))

        data.write(b'D+\xdd\xab')  # 0x442bddab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x442bddab))

        data.write(b'70OH')  # 0x37304f48
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.column_damage.to_stream(data, default_override={'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5R\x8a\x8d')  # 0xc5528a8d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cross_bar_damage.to_stream(data, default_override={'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'KY\xe5\x90')  # 0x4b59e590
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.column_damage_radius))

        data.write(b'\xcb\x14\xd9|')  # 0xcb14d97c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\xc6\xa6\xb7$')  # 0xc6a6b724
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.apex_shockwave_volume))

        data.write(b'@2\xc5\x8a')  # 0x4032c58a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4032c58a))

        data.write(b'\x8bn\x16/')  # 0x8b6e162f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8b6e162f))

        data.write(b'\x96k&\x97')  # 0x966b2697
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x966b2697))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            column_effect=data['column_effect'],
            column_trail_effect=data['column_trail_effect'],
            elsc=data['elsc'],
            visor_effect_electric=data['visor_effect_electric'],
            unknown_0x01299e29=data['unknown_0x01299e29'],
            unknown_0x442bddab=data['unknown_0x442bddab'],
            column_damage=DamageInfo.from_json(data['column_damage']),
            cross_bar_damage=DamageInfo.from_json(data['cross_bar_damage']),
            column_damage_radius=data['column_damage_radius'],
            initial_speed=data['initial_speed'],
            acceleration=data['acceleration'],
            apex_shockwave_volume=data['apex_shockwave_volume'],
            unknown_0x4032c58a=data['unknown_0x4032c58a'],
            unknown_0x8b6e162f=data['unknown_0x8b6e162f'],
            unknown_0x966b2697=data['unknown_0x966b2697'],
        )

    def to_json(self) -> dict:
        return {
            'column_effect': self.column_effect,
            'column_trail_effect': self.column_trail_effect,
            'elsc': self.elsc,
            'visor_effect_electric': self.visor_effect_electric,
            'unknown_0x01299e29': self.unknown_0x01299e29,
            'unknown_0x442bddab': self.unknown_0x442bddab,
            'column_damage': self.column_damage.to_json(),
            'cross_bar_damage': self.cross_bar_damage.to_json(),
            'column_damage_radius': self.column_damage_radius,
            'initial_speed': self.initial_speed,
            'acceleration': self.acceleration,
            'apex_shockwave_volume': self.apex_shockwave_volume,
            'unknown_0x4032c58a': self.unknown_0x4032c58a,
            'unknown_0x8b6e162f': self.unknown_0x8b6e162f,
            'unknown_0x966b2697': self.unknown_0x966b2697,
        }


def _decode_column_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_column_trail_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_elsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_visor_effect_electric(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x01299e29(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x442bddab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_column_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_cross_bar_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_column_damage_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_apex_shockwave_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4032c58a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8b6e162f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x966b2697(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4c28cd13: ('column_effect', _decode_column_effect),
    0x32a13dfd: ('column_trail_effect', _decode_column_trail_effect),
    0x57f7eff9: ('elsc', _decode_elsc),
    0xfd132f70: ('visor_effect_electric', _decode_visor_effect_electric),
    0x1299e29: ('unknown_0x01299e29', _decode_unknown_0x01299e29),
    0x442bddab: ('unknown_0x442bddab', _decode_unknown_0x442bddab),
    0x37304f48: ('column_damage', _decode_column_damage),
    0xc5528a8d: ('cross_bar_damage', _decode_cross_bar_damage),
    0x4b59e590: ('column_damage_radius', _decode_column_damage_radius),
    0xcb14d97c: ('initial_speed', _decode_initial_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0xc6a6b724: ('apex_shockwave_volume', _decode_apex_shockwave_volume),
    0x4032c58a: ('unknown_0x4032c58a', _decode_unknown_0x4032c58a),
    0x8b6e162f: ('unknown_0x8b6e162f', _decode_unknown_0x8b6e162f),
    0x966b2697: ('unknown_0x966b2697', _decode_unknown_0x966b2697),
}
