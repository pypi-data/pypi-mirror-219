# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.UnknownStruct11 import UnknownStruct11
from retro_data_structures.properties.corruption.archetypes.UnknownStruct12 import UnknownStruct12
from retro_data_structures.properties.corruption.archetypes.UnknownStruct13 import UnknownStruct13
from retro_data_structures.properties.corruption.archetypes.UnknownStruct14 import UnknownStruct14
from retro_data_structures.properties.corruption.archetypes.UnknownStruct7 import UnknownStruct7


@dataclasses.dataclass()
class AuroraUnit2Data(BaseProperty):
    unknown_0x0a072c48: float = dataclasses.field(default=0.6000000238418579)
    unknown_0xdde5ac10: float = dataclasses.field(default=0.30000001192092896)
    flight_max_speed: float = dataclasses.field(default=20.0)
    flight_acceleration: float = dataclasses.field(default=10.0)
    flight_deceleration: float = dataclasses.field(default=15.0)
    dodge_time: float = dataclasses.field(default=3.0)
    dodge_time_variance: float = dataclasses.field(default=1.0)
    dodge_chance: float = dataclasses.field(default=50.0)
    unknown_0xefd78a41: float = dataclasses.field(default=50.0)
    hover_height: float = dataclasses.field(default=15.0)
    min_follow_distance: float = dataclasses.field(default=20.0)
    max_follow_distance: float = dataclasses.field(default=50.0)
    initial_attack_time: float = dataclasses.field(default=6.0)
    attack_time: float = dataclasses.field(default=5.0)
    attack_time_variance: float = dataclasses.field(default=0.0)
    unknown_0x059b46cf: float = dataclasses.field(default=2.5)
    unknown_0x1aa98d7f: float = dataclasses.field(default=0.0)
    junction_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_struct7: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)
    unknown_struct11: UnknownStruct11 = dataclasses.field(default_factory=UnknownStruct11)
    unknown_struct12: UnknownStruct12 = dataclasses.field(default_factory=UnknownStruct12)
    unknown_struct13: UnknownStruct13 = dataclasses.field(default_factory=UnknownStruct13)
    unknown_struct14: UnknownStruct14 = dataclasses.field(default_factory=UnknownStruct14)

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

        data.write(b'\n\x07,H')  # 0xa072c48
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a072c48))

        data.write(b'\xdd\xe5\xac\x10')  # 0xdde5ac10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdde5ac10))

        data.write(b'\xd4\xde\xc6)')  # 0xd4dec629
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_max_speed))

        data.write(b'z+\xb3w')  # 0x7a2bb377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_acceleration))

        data.write(b'\xdd\x146\x1f')  # 0xdd14361f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_deceleration))

        data.write(b'gb[\xef')  # 0x67625bef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_time))

        data.write(b'4\xb9~\xdb')  # 0x34b97edb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_time_variance))

        data.write(b'G\xbe2\x98')  # 0x47be3298
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_chance))

        data.write(b'\xef\xd7\x8aA')  # 0xefd78a41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xefd78a41))

        data.write(b'\xc7Y\x98\xaa')  # 0xc75998aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_height))

        data.write(b'\x93qj\x88')  # 0x93716a88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_follow_distance))

        data.write(b'\xd2fU\x0e')  # 0xd266550e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_follow_distance))

        data.write(b'Dn\xfc\xad')  # 0x446efcad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_attack_time))

        data.write(b'\xdc\xa1\xe8\xb6')  # 0xdca1e8b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_time))

        data.write(b'\x9f&\x96\x14')  # 0x9f269614
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_time_variance))

        data.write(b'\x05\x9bF\xcf')  # 0x59b46cf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x059b46cf))

        data.write(b'\x1a\xa9\x8d\x7f')  # 0x1aa98d7f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1aa98d7f))

        data.write(b'\xfd\xd2\xfe ')  # 0xfdd2fe20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.junction_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1\x08\xcf\xa0')  # 0xc108cfa0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91P&\x86')  # 0x91502686
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct11.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xadb\xc9\x93')  # 0xad62c993
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct12.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03\xa3\x19\xdf')  # 0x3a319df
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\xd3\xbbW')  # 0x9dd3bb57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x0a072c48=data['unknown_0x0a072c48'],
            unknown_0xdde5ac10=data['unknown_0xdde5ac10'],
            flight_max_speed=data['flight_max_speed'],
            flight_acceleration=data['flight_acceleration'],
            flight_deceleration=data['flight_deceleration'],
            dodge_time=data['dodge_time'],
            dodge_time_variance=data['dodge_time_variance'],
            dodge_chance=data['dodge_chance'],
            unknown_0xefd78a41=data['unknown_0xefd78a41'],
            hover_height=data['hover_height'],
            min_follow_distance=data['min_follow_distance'],
            max_follow_distance=data['max_follow_distance'],
            initial_attack_time=data['initial_attack_time'],
            attack_time=data['attack_time'],
            attack_time_variance=data['attack_time_variance'],
            unknown_0x059b46cf=data['unknown_0x059b46cf'],
            unknown_0x1aa98d7f=data['unknown_0x1aa98d7f'],
            junction_vulnerability=DamageVulnerability.from_json(data['junction_vulnerability']),
            unknown_struct7=UnknownStruct7.from_json(data['unknown_struct7']),
            unknown_struct11=UnknownStruct11.from_json(data['unknown_struct11']),
            unknown_struct12=UnknownStruct12.from_json(data['unknown_struct12']),
            unknown_struct13=UnknownStruct13.from_json(data['unknown_struct13']),
            unknown_struct14=UnknownStruct14.from_json(data['unknown_struct14']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x0a072c48': self.unknown_0x0a072c48,
            'unknown_0xdde5ac10': self.unknown_0xdde5ac10,
            'flight_max_speed': self.flight_max_speed,
            'flight_acceleration': self.flight_acceleration,
            'flight_deceleration': self.flight_deceleration,
            'dodge_time': self.dodge_time,
            'dodge_time_variance': self.dodge_time_variance,
            'dodge_chance': self.dodge_chance,
            'unknown_0xefd78a41': self.unknown_0xefd78a41,
            'hover_height': self.hover_height,
            'min_follow_distance': self.min_follow_distance,
            'max_follow_distance': self.max_follow_distance,
            'initial_attack_time': self.initial_attack_time,
            'attack_time': self.attack_time,
            'attack_time_variance': self.attack_time_variance,
            'unknown_0x059b46cf': self.unknown_0x059b46cf,
            'unknown_0x1aa98d7f': self.unknown_0x1aa98d7f,
            'junction_vulnerability': self.junction_vulnerability.to_json(),
            'unknown_struct7': self.unknown_struct7.to_json(),
            'unknown_struct11': self.unknown_struct11.to_json(),
            'unknown_struct12': self.unknown_struct12.to_json(),
            'unknown_struct13': self.unknown_struct13.to_json(),
            'unknown_struct14': self.unknown_struct14.to_json(),
        }


def _decode_unknown_0x0a072c48(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdde5ac10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_time_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xefd78a41(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_follow_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_follow_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_time_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x059b46cf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1aa98d7f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_junction_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_struct7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


def _decode_unknown_struct11(data: typing.BinaryIO, property_size: int):
    return UnknownStruct11.from_stream(data, property_size)


def _decode_unknown_struct12(data: typing.BinaryIO, property_size: int):
    return UnknownStruct12.from_stream(data, property_size)


def _decode_unknown_struct13(data: typing.BinaryIO, property_size: int):
    return UnknownStruct13.from_stream(data, property_size)


def _decode_unknown_struct14(data: typing.BinaryIO, property_size: int):
    return UnknownStruct14.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa072c48: ('unknown_0x0a072c48', _decode_unknown_0x0a072c48),
    0xdde5ac10: ('unknown_0xdde5ac10', _decode_unknown_0xdde5ac10),
    0xd4dec629: ('flight_max_speed', _decode_flight_max_speed),
    0x7a2bb377: ('flight_acceleration', _decode_flight_acceleration),
    0xdd14361f: ('flight_deceleration', _decode_flight_deceleration),
    0x67625bef: ('dodge_time', _decode_dodge_time),
    0x34b97edb: ('dodge_time_variance', _decode_dodge_time_variance),
    0x47be3298: ('dodge_chance', _decode_dodge_chance),
    0xefd78a41: ('unknown_0xefd78a41', _decode_unknown_0xefd78a41),
    0xc75998aa: ('hover_height', _decode_hover_height),
    0x93716a88: ('min_follow_distance', _decode_min_follow_distance),
    0xd266550e: ('max_follow_distance', _decode_max_follow_distance),
    0x446efcad: ('initial_attack_time', _decode_initial_attack_time),
    0xdca1e8b6: ('attack_time', _decode_attack_time),
    0x9f269614: ('attack_time_variance', _decode_attack_time_variance),
    0x59b46cf: ('unknown_0x059b46cf', _decode_unknown_0x059b46cf),
    0x1aa98d7f: ('unknown_0x1aa98d7f', _decode_unknown_0x1aa98d7f),
    0xfdd2fe20: ('junction_vulnerability', _decode_junction_vulnerability),
    0xc108cfa0: ('unknown_struct7', _decode_unknown_struct7),
    0x91502686: ('unknown_struct11', _decode_unknown_struct11),
    0xad62c993: ('unknown_struct12', _decode_unknown_struct12),
    0x3a319df: ('unknown_struct13', _decode_unknown_struct13),
    0x9dd3bb57: ('unknown_struct14', _decode_unknown_struct14),
}
