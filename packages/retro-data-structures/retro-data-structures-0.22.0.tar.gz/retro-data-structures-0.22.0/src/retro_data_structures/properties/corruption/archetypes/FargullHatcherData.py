# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability


@dataclasses.dataclass()
class FargullHatcherData(BaseProperty):
    is_crouching: bool = dataclasses.field(default=False)
    attack_range: float = dataclasses.field(default=20.0)
    min_hatch_time: float = dataclasses.field(default=20.0)
    max_hatch_time: float = dataclasses.field(default=20.0)
    sonic_pulse_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    sonic_pulse_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xa5692479: float = dataclasses.field(default=1.0)
    min_hatch_size: int = dataclasses.field(default=5)
    min_taunt_time: float = dataclasses.field(default=10.0)
    max_taunt_time: float = dataclasses.field(default=20.0)
    taunt_probability: float = dataclasses.field(default=0.5)
    unknown_0x248bc9f9: float = dataclasses.field(default=2.0)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x0c6\xeb\x18')  # 0xc36eb18
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_crouching))

        data.write(b'9\xda\xc8\x1e')  # 0x39dac81e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range))

        data.write(b'\xe2\x95C\xef')  # 0xe29543ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_hatch_time))

        data.write(b'\xf7\x1e\x97\x1d')  # 0xf71e971d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_hatch_time))

        data.write(b'S\x7f\x9fM')  # 0x537f9f4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sonic_pulse_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',tm,')  # 0x2c746d2c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sonic_pulse_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5i$y')  # 0xa5692479
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa5692479))

        data.write(b'\x9f|\xa9\xd1')  # 0x9f7ca9d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_hatch_size))

        data.write(b'\xc3q\x8e\xa0')  # 0xc3718ea0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_taunt_time))

        data.write(b'\xd6\xfaZR')  # 0xd6fa5a52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_taunt_time))

        data.write(b'\xfc\xdc\xaaN')  # 0xfcdcaa4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_probability))

        data.write(b'$\x8b\xc9\xf9')  # 0x248bc9f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x248bc9f9))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_crouching=data['is_crouching'],
            attack_range=data['attack_range'],
            min_hatch_time=data['min_hatch_time'],
            max_hatch_time=data['max_hatch_time'],
            sonic_pulse_vulnerability=DamageVulnerability.from_json(data['sonic_pulse_vulnerability']),
            sonic_pulse_damage=DamageInfo.from_json(data['sonic_pulse_damage']),
            unknown_0xa5692479=data['unknown_0xa5692479'],
            min_hatch_size=data['min_hatch_size'],
            min_taunt_time=data['min_taunt_time'],
            max_taunt_time=data['max_taunt_time'],
            taunt_probability=data['taunt_probability'],
            unknown_0x248bc9f9=data['unknown_0x248bc9f9'],
        )

    def to_json(self) -> dict:
        return {
            'is_crouching': self.is_crouching,
            'attack_range': self.attack_range,
            'min_hatch_time': self.min_hatch_time,
            'max_hatch_time': self.max_hatch_time,
            'sonic_pulse_vulnerability': self.sonic_pulse_vulnerability.to_json(),
            'sonic_pulse_damage': self.sonic_pulse_damage.to_json(),
            'unknown_0xa5692479': self.unknown_0xa5692479,
            'min_hatch_size': self.min_hatch_size,
            'min_taunt_time': self.min_taunt_time,
            'max_taunt_time': self.max_taunt_time,
            'taunt_probability': self.taunt_probability,
            'unknown_0x248bc9f9': self.unknown_0x248bc9f9,
        }


def _decode_is_crouching(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_hatch_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_hatch_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sonic_pulse_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_sonic_pulse_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xa5692479(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_hatch_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_min_taunt_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_taunt_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_taunt_probability(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x248bc9f9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc36eb18: ('is_crouching', _decode_is_crouching),
    0x39dac81e: ('attack_range', _decode_attack_range),
    0xe29543ef: ('min_hatch_time', _decode_min_hatch_time),
    0xf71e971d: ('max_hatch_time', _decode_max_hatch_time),
    0x537f9f4d: ('sonic_pulse_vulnerability', _decode_sonic_pulse_vulnerability),
    0x2c746d2c: ('sonic_pulse_damage', _decode_sonic_pulse_damage),
    0xa5692479: ('unknown_0xa5692479', _decode_unknown_0xa5692479),
    0x9f7ca9d1: ('min_hatch_size', _decode_min_hatch_size),
    0xc3718ea0: ('min_taunt_time', _decode_min_taunt_time),
    0xd6fa5a52: ('max_taunt_time', _decode_max_taunt_time),
    0xfcdcaa4e: ('taunt_probability', _decode_taunt_probability),
    0x248bc9f9: ('unknown_0x248bc9f9', _decode_unknown_0x248bc9f9),
}
