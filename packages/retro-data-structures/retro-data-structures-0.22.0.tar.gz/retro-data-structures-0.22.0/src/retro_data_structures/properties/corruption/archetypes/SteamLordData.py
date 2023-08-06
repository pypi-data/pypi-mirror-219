# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SteamLordData(BaseProperty):
    unknown_0xe9553ffa: bool = dataclasses.field(default=False)
    is_initially_cloaked: bool = dataclasses.field(default=False)
    cloak_time: float = dataclasses.field(default=1.0)
    decloak_time: float = dataclasses.field(default=0.25)
    re_cloak_time: float = dataclasses.field(default=2.0)
    dodge_damage_threshold: float = dataclasses.field(default=10.0)
    dodge_chance: float = dataclasses.field(default=25.0)
    flight_max_speed: float = dataclasses.field(default=10.0)
    flight_acceleration: float = dataclasses.field(default=2.5)
    target_hover_height: float = dataclasses.field(default=5.0)
    repair_hover_height: float = dataclasses.field(default=5.0)
    unknown_0xb35f3997: float = dataclasses.field(default=10.0)
    abort_repair_damage: float = dataclasses.field(default=50.0)
    repair_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    contact_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    elsc_0xbe36e228: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    elsc_0x24a4fc9e: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    unknown_0xe1f030d5: float = dataclasses.field(default=15.0)
    unknown_0xfb72f91e: float = dataclasses.field(default=5.0)
    damage_info_0xfe138b07: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0xaa19d1dc: DamageInfo = dataclasses.field(default_factory=DamageInfo)

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'\xe9U?\xfa')  # 0xe9553ffa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe9553ffa))

        data.write(b'\x1c\x89?T')  # 0x1c893f54
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_initially_cloaked))

        data.write(b'8\x8b\xc3\x1f')  # 0x388bc31f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_time))

        data.write(b'C\x19\xc8@')  # 0x4319c840
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.decloak_time))

        data.write(b';\xcb\xe7\xe2')  # 0x3bcbe7e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.re_cloak_time))

        data.write(b'\x91\xc8\xba\x81')  # 0x91c8ba81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_damage_threshold))

        data.write(b'G\xbe2\x98')  # 0x47be3298
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_chance))

        data.write(b'\xd4\xde\xc6)')  # 0xd4dec629
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_max_speed))

        data.write(b'z+\xb3w')  # 0x7a2bb377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_acceleration))

        data.write(b'p\x13\x0f\xe6')  # 0x70130fe6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_hover_height))

        data.write(b'\xfc\xc4\xe2@')  # 0xfcc4e240
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.repair_hover_height))

        data.write(b'\xb3_9\x97')  # 0xb35f3997
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb35f3997))

        data.write(b'\xeb\xa0\xc5\xf7')  # 0xeba0c5f7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.abort_repair_damage))

        data.write(b'\x9fNj6')  # 0x9f4e6a36
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.repair_effect))

        data.write(b'\r\xe16\xf7')  # 0xde136f7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_visor_effect))

        data.write(b'\xbe6\xe2(')  # 0xbe36e228
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc_0xbe36e228))

        data.write(b'$\xa4\xfc\x9e')  # 0x24a4fc9e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc_0x24a4fc9e))

        data.write(b'\xe1\xf00\xd5')  # 0xe1f030d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe1f030d5))

        data.write(b'\xfbr\xf9\x1e')  # 0xfb72f91e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfb72f91e))

        data.write(b'\xfe\x13\x8b\x07')  # 0xfe138b07
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0xfe138b07.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\x19\xd1\xdc')  # 0xaa19d1dc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0xaa19d1dc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe9553ffa=data['unknown_0xe9553ffa'],
            is_initially_cloaked=data['is_initially_cloaked'],
            cloak_time=data['cloak_time'],
            decloak_time=data['decloak_time'],
            re_cloak_time=data['re_cloak_time'],
            dodge_damage_threshold=data['dodge_damage_threshold'],
            dodge_chance=data['dodge_chance'],
            flight_max_speed=data['flight_max_speed'],
            flight_acceleration=data['flight_acceleration'],
            target_hover_height=data['target_hover_height'],
            repair_hover_height=data['repair_hover_height'],
            unknown_0xb35f3997=data['unknown_0xb35f3997'],
            abort_repair_damage=data['abort_repair_damage'],
            repair_effect=data['repair_effect'],
            contact_visor_effect=data['contact_visor_effect'],
            elsc_0xbe36e228=data['elsc_0xbe36e228'],
            elsc_0x24a4fc9e=data['elsc_0x24a4fc9e'],
            unknown_0xe1f030d5=data['unknown_0xe1f030d5'],
            unknown_0xfb72f91e=data['unknown_0xfb72f91e'],
            damage_info_0xfe138b07=DamageInfo.from_json(data['damage_info_0xfe138b07']),
            damage_info_0xaa19d1dc=DamageInfo.from_json(data['damage_info_0xaa19d1dc']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe9553ffa': self.unknown_0xe9553ffa,
            'is_initially_cloaked': self.is_initially_cloaked,
            'cloak_time': self.cloak_time,
            'decloak_time': self.decloak_time,
            're_cloak_time': self.re_cloak_time,
            'dodge_damage_threshold': self.dodge_damage_threshold,
            'dodge_chance': self.dodge_chance,
            'flight_max_speed': self.flight_max_speed,
            'flight_acceleration': self.flight_acceleration,
            'target_hover_height': self.target_hover_height,
            'repair_hover_height': self.repair_hover_height,
            'unknown_0xb35f3997': self.unknown_0xb35f3997,
            'abort_repair_damage': self.abort_repair_damage,
            'repair_effect': self.repair_effect,
            'contact_visor_effect': self.contact_visor_effect,
            'elsc_0xbe36e228': self.elsc_0xbe36e228,
            'elsc_0x24a4fc9e': self.elsc_0x24a4fc9e,
            'unknown_0xe1f030d5': self.unknown_0xe1f030d5,
            'unknown_0xfb72f91e': self.unknown_0xfb72f91e,
            'damage_info_0xfe138b07': self.damage_info_0xfe138b07.to_json(),
            'damage_info_0xaa19d1dc': self.damage_info_0xaa19d1dc.to_json(),
        }


def _decode_unknown_0xe9553ffa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_initially_cloaked(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_cloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_decloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_re_cloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_damage_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_hover_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_repair_hover_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb35f3997(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_abort_repair_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_repair_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_contact_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_elsc_0xbe36e228(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_elsc_0x24a4fc9e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xe1f030d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfb72f91e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info_0xfe138b07(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0xaa19d1dc(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe9553ffa: ('unknown_0xe9553ffa', _decode_unknown_0xe9553ffa),
    0x1c893f54: ('is_initially_cloaked', _decode_is_initially_cloaked),
    0x388bc31f: ('cloak_time', _decode_cloak_time),
    0x4319c840: ('decloak_time', _decode_decloak_time),
    0x3bcbe7e2: ('re_cloak_time', _decode_re_cloak_time),
    0x91c8ba81: ('dodge_damage_threshold', _decode_dodge_damage_threshold),
    0x47be3298: ('dodge_chance', _decode_dodge_chance),
    0xd4dec629: ('flight_max_speed', _decode_flight_max_speed),
    0x7a2bb377: ('flight_acceleration', _decode_flight_acceleration),
    0x70130fe6: ('target_hover_height', _decode_target_hover_height),
    0xfcc4e240: ('repair_hover_height', _decode_repair_hover_height),
    0xb35f3997: ('unknown_0xb35f3997', _decode_unknown_0xb35f3997),
    0xeba0c5f7: ('abort_repair_damage', _decode_abort_repair_damage),
    0x9f4e6a36: ('repair_effect', _decode_repair_effect),
    0xde136f7: ('contact_visor_effect', _decode_contact_visor_effect),
    0xbe36e228: ('elsc_0xbe36e228', _decode_elsc_0xbe36e228),
    0x24a4fc9e: ('elsc_0x24a4fc9e', _decode_elsc_0x24a4fc9e),
    0xe1f030d5: ('unknown_0xe1f030d5', _decode_unknown_0xe1f030d5),
    0xfb72f91e: ('unknown_0xfb72f91e', _decode_unknown_0xfb72f91e),
    0xfe138b07: ('damage_info_0xfe138b07', _decode_damage_info_0xfe138b07),
    0xaa19d1dc: ('damage_info_0xaa19d1dc', _decode_damage_info_0xaa19d1dc),
}
