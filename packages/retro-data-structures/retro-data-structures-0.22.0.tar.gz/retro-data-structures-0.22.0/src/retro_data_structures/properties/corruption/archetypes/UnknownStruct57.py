# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct56 import UnknownStruct56
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct57(BaseProperty):
    samus_gun_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    min_roll_time: float = dataclasses.field(default=4.0)
    max_roll_time: float = dataclasses.field(default=6.0)
    min_attack_time: float = dataclasses.field(default=3.0)
    max_attack_time: float = dataclasses.field(default=5.0)
    min_attack_distance: float = dataclasses.field(default=5.0)
    max_attack_distance: float = dataclasses.field(default=100.0)
    unknown_0xce471a01: float = dataclasses.field(default=1.0)
    attack_turn_threshold: float = dataclasses.field(default=70.0)
    unknown_0x4113ffd8: float = dataclasses.field(default=0.6499999761581421)
    beam_tracking_speed: float = dataclasses.field(default=9.0)
    unknown_struct56: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56)
    beam_attack: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    beam_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xe32082d1: float = dataclasses.field(default=80.0)
    unknown_0xb71164a2: float = dataclasses.field(default=80.0)
    unknown_0x3dc59b72: float = dataclasses.field(default=20.0)
    unknown_0xba9eb1d2: float = dataclasses.field(default=72.0)
    unknown_0xf0397134: float = dataclasses.field(default=90.0)
    unknown_0x5dae4176: float = dataclasses.field(default=30.0)
    radial_melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    unknown_0xe0c37dfa: float = dataclasses.field(default=14.0)

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'!n\xd1\xad')  # 0x216ed1ad
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.samus_gun_model))

        data.write(b'\xb8\xba\xa8\xc0')  # 0xb8baa8c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_roll_time))

        data.write(b'\xe9C\x13\x9d')  # 0xe943139d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_roll_time))

        data.write(b'.\xdf3h')  # 0x2edf3368
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_time))

        data.write(b'}y+\x8c')  # 0x7d792b8c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_time))

        data.write(b'\xfb\x82^\xaa')  # 0xfb825eaa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_distance))

        data.write(b'\xba\x95a,')  # 0xba95612c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_distance))

        data.write(b'\xceG\x1a\x01')  # 0xce471a01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xce471a01))

        data.write(b'\xaf,\xb0\xa3')  # 0xaf2cb0a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_turn_threshold))

        data.write(b'A\x13\xff\xd8')  # 0x4113ffd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4113ffd8))

        data.write(b'-\x8a\x93R')  # 0x2d8a9352
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_tracking_speed))

        data.write(b'\x84`RY')  # 0x84605259
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\x96r\xf5')  # 0x889672f5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' *\xfa\xa4')  # 0x202afaa4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3 \x82\xd1')  # 0xe32082d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe32082d1))

        data.write(b'\xb7\x11d\xa2')  # 0xb71164a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb71164a2))

        data.write(b'=\xc5\x9br')  # 0x3dc59b72
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3dc59b72))

        data.write(b'\xba\x9e\xb1\xd2')  # 0xba9eb1d2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xba9eb1d2))

        data.write(b'\xf09q4')  # 0xf0397134
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf0397134))

        data.write(b']\xaeAv')  # 0x5dae4176
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5dae4176))

        data.write(b'_\x11\x89;')  # 0x5f11893b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radial_melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xfa\x9bb')  # 0xf3fa9b62
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.elsc))

        data.write(b'\xe0\xc3}\xfa')  # 0xe0c37dfa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe0c37dfa))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            samus_gun_model=data['samus_gun_model'],
            min_roll_time=data['min_roll_time'],
            max_roll_time=data['max_roll_time'],
            min_attack_time=data['min_attack_time'],
            max_attack_time=data['max_attack_time'],
            min_attack_distance=data['min_attack_distance'],
            max_attack_distance=data['max_attack_distance'],
            unknown_0xce471a01=data['unknown_0xce471a01'],
            attack_turn_threshold=data['attack_turn_threshold'],
            unknown_0x4113ffd8=data['unknown_0x4113ffd8'],
            beam_tracking_speed=data['beam_tracking_speed'],
            unknown_struct56=UnknownStruct56.from_json(data['unknown_struct56']),
            beam_attack=PlasmaBeamInfo.from_json(data['beam_attack']),
            beam_attack_damage=DamageInfo.from_json(data['beam_attack_damage']),
            unknown_0xe32082d1=data['unknown_0xe32082d1'],
            unknown_0xb71164a2=data['unknown_0xb71164a2'],
            unknown_0x3dc59b72=data['unknown_0x3dc59b72'],
            unknown_0xba9eb1d2=data['unknown_0xba9eb1d2'],
            unknown_0xf0397134=data['unknown_0xf0397134'],
            unknown_0x5dae4176=data['unknown_0x5dae4176'],
            radial_melee_damage=DamageInfo.from_json(data['radial_melee_damage']),
            elsc=data['elsc'],
            unknown_0xe0c37dfa=data['unknown_0xe0c37dfa'],
        )

    def to_json(self) -> dict:
        return {
            'samus_gun_model': self.samus_gun_model,
            'min_roll_time': self.min_roll_time,
            'max_roll_time': self.max_roll_time,
            'min_attack_time': self.min_attack_time,
            'max_attack_time': self.max_attack_time,
            'min_attack_distance': self.min_attack_distance,
            'max_attack_distance': self.max_attack_distance,
            'unknown_0xce471a01': self.unknown_0xce471a01,
            'attack_turn_threshold': self.attack_turn_threshold,
            'unknown_0x4113ffd8': self.unknown_0x4113ffd8,
            'beam_tracking_speed': self.beam_tracking_speed,
            'unknown_struct56': self.unknown_struct56.to_json(),
            'beam_attack': self.beam_attack.to_json(),
            'beam_attack_damage': self.beam_attack_damage.to_json(),
            'unknown_0xe32082d1': self.unknown_0xe32082d1,
            'unknown_0xb71164a2': self.unknown_0xb71164a2,
            'unknown_0x3dc59b72': self.unknown_0x3dc59b72,
            'unknown_0xba9eb1d2': self.unknown_0xba9eb1d2,
            'unknown_0xf0397134': self.unknown_0xf0397134,
            'unknown_0x5dae4176': self.unknown_0x5dae4176,
            'radial_melee_damage': self.radial_melee_damage.to_json(),
            'elsc': self.elsc,
            'unknown_0xe0c37dfa': self.unknown_0xe0c37dfa,
        }


def _decode_samus_gun_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_min_roll_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_roll_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xce471a01(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_turn_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4113ffd8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_tracking_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct56(data: typing.BinaryIO, property_size: int):
    return UnknownStruct56.from_stream(data, property_size)


def _decode_beam_attack(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_beam_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xe32082d1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb71164a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3dc59b72(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xba9eb1d2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf0397134(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5dae4176(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radial_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_elsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xe0c37dfa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x216ed1ad: ('samus_gun_model', _decode_samus_gun_model),
    0xb8baa8c0: ('min_roll_time', _decode_min_roll_time),
    0xe943139d: ('max_roll_time', _decode_max_roll_time),
    0x2edf3368: ('min_attack_time', _decode_min_attack_time),
    0x7d792b8c: ('max_attack_time', _decode_max_attack_time),
    0xfb825eaa: ('min_attack_distance', _decode_min_attack_distance),
    0xba95612c: ('max_attack_distance', _decode_max_attack_distance),
    0xce471a01: ('unknown_0xce471a01', _decode_unknown_0xce471a01),
    0xaf2cb0a3: ('attack_turn_threshold', _decode_attack_turn_threshold),
    0x4113ffd8: ('unknown_0x4113ffd8', _decode_unknown_0x4113ffd8),
    0x2d8a9352: ('beam_tracking_speed', _decode_beam_tracking_speed),
    0x84605259: ('unknown_struct56', _decode_unknown_struct56),
    0x889672f5: ('beam_attack', _decode_beam_attack),
    0x202afaa4: ('beam_attack_damage', _decode_beam_attack_damage),
    0xe32082d1: ('unknown_0xe32082d1', _decode_unknown_0xe32082d1),
    0xb71164a2: ('unknown_0xb71164a2', _decode_unknown_0xb71164a2),
    0x3dc59b72: ('unknown_0x3dc59b72', _decode_unknown_0x3dc59b72),
    0xba9eb1d2: ('unknown_0xba9eb1d2', _decode_unknown_0xba9eb1d2),
    0xf0397134: ('unknown_0xf0397134', _decode_unknown_0xf0397134),
    0x5dae4176: ('unknown_0x5dae4176', _decode_unknown_0x5dae4176),
    0x5f11893b: ('radial_melee_damage', _decode_radial_melee_damage),
    0xf3fa9b62: ('elsc', _decode_elsc),
    0xe0c37dfa: ('unknown_0xe0c37dfa', _decode_unknown_0xe0c37dfa),
}
