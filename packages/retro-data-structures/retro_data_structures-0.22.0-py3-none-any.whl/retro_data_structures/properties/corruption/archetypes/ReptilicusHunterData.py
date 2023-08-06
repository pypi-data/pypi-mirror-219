# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.CattleProd import CattleProd
from retro_data_structures.properties.corruption.archetypes.Chakram import Chakram
from retro_data_structures.properties.corruption.archetypes.EnergyWhip import EnergyWhip
from retro_data_structures.properties.corruption.archetypes.ReptilicusHunterStruct import ReptilicusHunterStruct
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ReptilicusHunterData(BaseProperty):
    use_defense_points: bool = dataclasses.field(default=True)
    disable_terrain_alignment: bool = dataclasses.field(default=True)
    unknown_0xe9553ffa: bool = dataclasses.field(default=False)
    is_initially_cloaked: bool = dataclasses.field(default=False)
    min_visible_time: float = dataclasses.field(default=15.0)
    max_visible_time: float = dataclasses.field(default=20.0)
    unknown_0x11286bd3: float = dataclasses.field(default=40.0)
    unknown_0xb7e53921: float = dataclasses.field(default=2.0)
    unknown_0x5867275b: float = dataclasses.field(default=4.0)
    cloak_time: float = dataclasses.field(default=1.0)
    decloak_time: float = dataclasses.field(default=0.25)
    cloak_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    decloak_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x221c7ec1: float = dataclasses.field(default=2.0)
    unknown_0x41af5eeb: float = dataclasses.field(default=300.0)
    hear_shot_radius: float = dataclasses.field(default=0.0)
    cover_abort_time: float = dataclasses.field(default=10.0)
    unknown_0x164f8ca8: float = dataclasses.field(default=0.0)
    unknown_0xcdf0df4f: float = dataclasses.field(default=1.0)
    unknown_0xf77e2ae2: float = dataclasses.field(default=1.0)
    unknown_0x14239438: float = dataclasses.field(default=1.0)
    unknown_0xe6c24412: float = dataclasses.field(default=7.5)
    heavy_hit_chance: float = dataclasses.field(default=25.0)
    taunt_chance: float = dataclasses.field(default=10.0)
    aggressiveness: float = dataclasses.field(default=10.0)
    reptilicus_hunter_struct_0x9c5e7d6f: ReptilicusHunterStruct = dataclasses.field(default_factory=ReptilicusHunterStruct)
    reptilicus_hunter_struct_0xaa2bee9a: ReptilicusHunterStruct = dataclasses.field(default_factory=ReptilicusHunterStruct)
    reptilicus_hunter_struct_0xe27a4e87: ReptilicusHunterStruct = dataclasses.field(default_factory=ReptilicusHunterStruct)
    cattle_prod: CattleProd = dataclasses.field(default_factory=CattleProd)
    energy_whip: EnergyWhip = dataclasses.field(default_factory=EnergyWhip)
    chakram: Chakram = dataclasses.field(default_factory=Chakram)

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'!~\x94J')  # 0x217e944a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_defense_points))

        data.write(b'\x0c\x81h\x1a')  # 0xc81681a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_terrain_alignment))

        data.write(b'\xe9U?\xfa')  # 0xe9553ffa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe9553ffa))

        data.write(b'\x1c\x89?T')  # 0x1c893f54
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_initially_cloaked))

        data.write(b'6\x9d\x08t')  # 0x369d0874
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_visible_time))

        data.write(b'\x91\xa9\x88\r')  # 0x91a9880d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_visible_time))

        data.write(b'\x11(k\xd3')  # 0x11286bd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x11286bd3))

        data.write(b'\xb7\xe59!')  # 0xb7e53921
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb7e53921))

        data.write(b"Xg'[")  # 0x5867275b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5867275b))

        data.write(b'8\x8b\xc3\x1f')  # 0x388bc31f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_time))

        data.write(b'C\x19\xc8@')  # 0x4319c840
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.decloak_time))

        data.write(b'\x05+\xf6\x17')  # 0x52bf617
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cloak_sound))

        data.write(b'\xfe\x84(y')  # 0xfe842879
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.decloak_sound))

        data.write(b'"\x1c~\xc1')  # 0x221c7ec1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x221c7ec1))

        data.write(b'A\xaf^\xeb')  # 0x41af5eeb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x41af5eeb))

        data.write(b'\x0c\xf8\x87\xf1')  # 0xcf887f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hear_shot_radius))

        data.write(b'\x18\xa9\x87k')  # 0x18a9876b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cover_abort_time))

        data.write(b'\x16O\x8c\xa8')  # 0x164f8ca8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x164f8ca8))

        data.write(b'\xcd\xf0\xdfO')  # 0xcdf0df4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcdf0df4f))

        data.write(b'\xf7~*\xe2')  # 0xf77e2ae2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf77e2ae2))

        data.write(b'\x14#\x948')  # 0x14239438
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x14239438))

        data.write(b'\xe6\xc2D\x12')  # 0xe6c24412
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe6c24412))

        data.write(b'X<\x1b\x1e')  # 0x583c1b1e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.heavy_hit_chance))

        data.write(b'\xa7\x7fb\x12')  # 0xa77f6212
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_chance))

        data.write(b'\x95y\xb1\xf2')  # 0x9579b1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aggressiveness))

        data.write(b'\x9c^}o')  # 0x9c5e7d6f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.reptilicus_hunter_struct_0x9c5e7d6f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa+\xee\x9a')  # 0xaa2bee9a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.reptilicus_hunter_struct_0xaa2bee9a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2zN\x87')  # 0xe27a4e87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.reptilicus_hunter_struct_0xe27a4e87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x87\xb1\ni')  # 0x87b10a69
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cattle_prod.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7T\x8e\x97')  # 0xd7548e97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_whip.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xa5\x8c1')  # 0x19a58c31
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.chakram.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            use_defense_points=data['use_defense_points'],
            disable_terrain_alignment=data['disable_terrain_alignment'],
            unknown_0xe9553ffa=data['unknown_0xe9553ffa'],
            is_initially_cloaked=data['is_initially_cloaked'],
            min_visible_time=data['min_visible_time'],
            max_visible_time=data['max_visible_time'],
            unknown_0x11286bd3=data['unknown_0x11286bd3'],
            unknown_0xb7e53921=data['unknown_0xb7e53921'],
            unknown_0x5867275b=data['unknown_0x5867275b'],
            cloak_time=data['cloak_time'],
            decloak_time=data['decloak_time'],
            cloak_sound=data['cloak_sound'],
            decloak_sound=data['decloak_sound'],
            unknown_0x221c7ec1=data['unknown_0x221c7ec1'],
            unknown_0x41af5eeb=data['unknown_0x41af5eeb'],
            hear_shot_radius=data['hear_shot_radius'],
            cover_abort_time=data['cover_abort_time'],
            unknown_0x164f8ca8=data['unknown_0x164f8ca8'],
            unknown_0xcdf0df4f=data['unknown_0xcdf0df4f'],
            unknown_0xf77e2ae2=data['unknown_0xf77e2ae2'],
            unknown_0x14239438=data['unknown_0x14239438'],
            unknown_0xe6c24412=data['unknown_0xe6c24412'],
            heavy_hit_chance=data['heavy_hit_chance'],
            taunt_chance=data['taunt_chance'],
            aggressiveness=data['aggressiveness'],
            reptilicus_hunter_struct_0x9c5e7d6f=ReptilicusHunterStruct.from_json(data['reptilicus_hunter_struct_0x9c5e7d6f']),
            reptilicus_hunter_struct_0xaa2bee9a=ReptilicusHunterStruct.from_json(data['reptilicus_hunter_struct_0xaa2bee9a']),
            reptilicus_hunter_struct_0xe27a4e87=ReptilicusHunterStruct.from_json(data['reptilicus_hunter_struct_0xe27a4e87']),
            cattle_prod=CattleProd.from_json(data['cattle_prod']),
            energy_whip=EnergyWhip.from_json(data['energy_whip']),
            chakram=Chakram.from_json(data['chakram']),
        )

    def to_json(self) -> dict:
        return {
            'use_defense_points': self.use_defense_points,
            'disable_terrain_alignment': self.disable_terrain_alignment,
            'unknown_0xe9553ffa': self.unknown_0xe9553ffa,
            'is_initially_cloaked': self.is_initially_cloaked,
            'min_visible_time': self.min_visible_time,
            'max_visible_time': self.max_visible_time,
            'unknown_0x11286bd3': self.unknown_0x11286bd3,
            'unknown_0xb7e53921': self.unknown_0xb7e53921,
            'unknown_0x5867275b': self.unknown_0x5867275b,
            'cloak_time': self.cloak_time,
            'decloak_time': self.decloak_time,
            'cloak_sound': self.cloak_sound,
            'decloak_sound': self.decloak_sound,
            'unknown_0x221c7ec1': self.unknown_0x221c7ec1,
            'unknown_0x41af5eeb': self.unknown_0x41af5eeb,
            'hear_shot_radius': self.hear_shot_radius,
            'cover_abort_time': self.cover_abort_time,
            'unknown_0x164f8ca8': self.unknown_0x164f8ca8,
            'unknown_0xcdf0df4f': self.unknown_0xcdf0df4f,
            'unknown_0xf77e2ae2': self.unknown_0xf77e2ae2,
            'unknown_0x14239438': self.unknown_0x14239438,
            'unknown_0xe6c24412': self.unknown_0xe6c24412,
            'heavy_hit_chance': self.heavy_hit_chance,
            'taunt_chance': self.taunt_chance,
            'aggressiveness': self.aggressiveness,
            'reptilicus_hunter_struct_0x9c5e7d6f': self.reptilicus_hunter_struct_0x9c5e7d6f.to_json(),
            'reptilicus_hunter_struct_0xaa2bee9a': self.reptilicus_hunter_struct_0xaa2bee9a.to_json(),
            'reptilicus_hunter_struct_0xe27a4e87': self.reptilicus_hunter_struct_0xe27a4e87.to_json(),
            'cattle_prod': self.cattle_prod.to_json(),
            'energy_whip': self.energy_whip.to_json(),
            'chakram': self.chakram.to_json(),
        }


def _decode_use_defense_points(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_terrain_alignment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe9553ffa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_initially_cloaked(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_min_visible_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_visible_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x11286bd3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb7e53921(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5867275b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_decloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cloak_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_decloak_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x221c7ec1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x41af5eeb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hear_shot_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cover_abort_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x164f8ca8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcdf0df4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf77e2ae2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x14239438(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe6c24412(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_heavy_hit_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_taunt_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_aggressiveness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reptilicus_hunter_struct_0x9c5e7d6f(data: typing.BinaryIO, property_size: int):
    return ReptilicusHunterStruct.from_stream(data, property_size)


def _decode_reptilicus_hunter_struct_0xaa2bee9a(data: typing.BinaryIO, property_size: int):
    return ReptilicusHunterStruct.from_stream(data, property_size)


def _decode_reptilicus_hunter_struct_0xe27a4e87(data: typing.BinaryIO, property_size: int):
    return ReptilicusHunterStruct.from_stream(data, property_size)


def _decode_cattle_prod(data: typing.BinaryIO, property_size: int):
    return CattleProd.from_stream(data, property_size)


def _decode_energy_whip(data: typing.BinaryIO, property_size: int):
    return EnergyWhip.from_stream(data, property_size)


def _decode_chakram(data: typing.BinaryIO, property_size: int):
    return Chakram.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x217e944a: ('use_defense_points', _decode_use_defense_points),
    0xc81681a: ('disable_terrain_alignment', _decode_disable_terrain_alignment),
    0xe9553ffa: ('unknown_0xe9553ffa', _decode_unknown_0xe9553ffa),
    0x1c893f54: ('is_initially_cloaked', _decode_is_initially_cloaked),
    0x369d0874: ('min_visible_time', _decode_min_visible_time),
    0x91a9880d: ('max_visible_time', _decode_max_visible_time),
    0x11286bd3: ('unknown_0x11286bd3', _decode_unknown_0x11286bd3),
    0xb7e53921: ('unknown_0xb7e53921', _decode_unknown_0xb7e53921),
    0x5867275b: ('unknown_0x5867275b', _decode_unknown_0x5867275b),
    0x388bc31f: ('cloak_time', _decode_cloak_time),
    0x4319c840: ('decloak_time', _decode_decloak_time),
    0x52bf617: ('cloak_sound', _decode_cloak_sound),
    0xfe842879: ('decloak_sound', _decode_decloak_sound),
    0x221c7ec1: ('unknown_0x221c7ec1', _decode_unknown_0x221c7ec1),
    0x41af5eeb: ('unknown_0x41af5eeb', _decode_unknown_0x41af5eeb),
    0xcf887f1: ('hear_shot_radius', _decode_hear_shot_radius),
    0x18a9876b: ('cover_abort_time', _decode_cover_abort_time),
    0x164f8ca8: ('unknown_0x164f8ca8', _decode_unknown_0x164f8ca8),
    0xcdf0df4f: ('unknown_0xcdf0df4f', _decode_unknown_0xcdf0df4f),
    0xf77e2ae2: ('unknown_0xf77e2ae2', _decode_unknown_0xf77e2ae2),
    0x14239438: ('unknown_0x14239438', _decode_unknown_0x14239438),
    0xe6c24412: ('unknown_0xe6c24412', _decode_unknown_0xe6c24412),
    0x583c1b1e: ('heavy_hit_chance', _decode_heavy_hit_chance),
    0xa77f6212: ('taunt_chance', _decode_taunt_chance),
    0x9579b1f2: ('aggressiveness', _decode_aggressiveness),
    0x9c5e7d6f: ('reptilicus_hunter_struct_0x9c5e7d6f', _decode_reptilicus_hunter_struct_0x9c5e7d6f),
    0xaa2bee9a: ('reptilicus_hunter_struct_0xaa2bee9a', _decode_reptilicus_hunter_struct_0xaa2bee9a),
    0xe27a4e87: ('reptilicus_hunter_struct_0xe27a4e87', _decode_reptilicus_hunter_struct_0xe27a4e87),
    0x87b10a69: ('cattle_prod', _decode_cattle_prod),
    0xd7548e97: ('energy_whip', _decode_energy_whip),
    0x19a58c31: ('chakram', _decode_chakram),
}
