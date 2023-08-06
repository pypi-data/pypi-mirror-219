# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.SpacePirateWeaponData import SpacePirateWeaponData
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class DarkSamusEchoData(BaseProperty):
    death_explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    death_explosion_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    initial_attack_time: float = dataclasses.field(default=3.0)
    min_attack_time: float = dataclasses.field(default=4.0)
    attack_time_variance: float = dataclasses.field(default=2.0)
    morphball_attack_speed: float = dataclasses.field(default=50.0)
    morphball_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xc3a06ae1: float = dataclasses.field(default=0.699999988079071)
    unknown_0x23e3c3bb: float = dataclasses.field(default=0.30000001192092896)
    min_morphball_attack_duration: float = dataclasses.field(default=5.0)
    max_morphball_attack_duration: float = dataclasses.field(default=20.0)
    unknown_0xd03984cd: float = dataclasses.field(default=135.0)
    unknown_0xe831a7d0: float = dataclasses.field(default=5.0)
    unknown_0xbeb2b793: float = dataclasses.field(default=3.0)
    unknown_0x9d9d3760: float = dataclasses.field(default=3.0)
    morphball_animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    weapon_data: SpacePirateWeaponData = dataclasses.field(default_factory=SpacePirateWeaponData)

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
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'\x06\x87\xc3>')  # 0x687c33e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_explosion))

        data.write(b'\xed\x08\xfcK')  # 0xed08fc4b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_explosion_sound))

        data.write(b'\x8f\x04\x00\xe2')  # 0x8f0400e2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'\xcc\xc7\xa9 ')  # 0xccc7a920
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'Dn\xfc\xad')  # 0x446efcad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_attack_time))

        data.write(b'.\xdf3h')  # 0x2edf3368
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_time))

        data.write(b'\x9f&\x96\x14')  # 0x9f269614
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_time_variance))

        data.write(b'\x99,{H')  # 0x992c7b48
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.morphball_attack_speed))

        data.write(b'v)0\x01')  # 0x76293001
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.morphball_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3\xa0j\xe1')  # 0xc3a06ae1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc3a06ae1))

        data.write(b'#\xe3\xc3\xbb')  # 0x23e3c3bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x23e3c3bb))

        data.write(b'YrE\xa1')  # 0x597245a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_morphball_attack_duration))

        data.write(b'v\xad\x06<')  # 0x76ad063c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_morphball_attack_duration))

        data.write(b'\xd09\x84\xcd')  # 0xd03984cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd03984cd))

        data.write(b'\xe81\xa7\xd0')  # 0xe831a7d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe831a7d0))

        data.write(b'\xbe\xb2\xb7\x93')  # 0xbeb2b793
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbeb2b793))

        data.write(b'\x9d\x9d7`')  # 0x9d9d3760
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9d9d3760))

        data.write(b'&\xb7R\xe1')  # 0x26b752e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.morphball_animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdc\x89\xcc<')  # 0xdc89cc3c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapon_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            death_explosion=data['death_explosion'],
            death_explosion_sound=data['death_explosion_sound'],
            part=data['part'],
            caud=data['caud'],
            initial_attack_time=data['initial_attack_time'],
            min_attack_time=data['min_attack_time'],
            attack_time_variance=data['attack_time_variance'],
            morphball_attack_speed=data['morphball_attack_speed'],
            morphball_attack_damage=DamageInfo.from_json(data['morphball_attack_damage']),
            unknown_0xc3a06ae1=data['unknown_0xc3a06ae1'],
            unknown_0x23e3c3bb=data['unknown_0x23e3c3bb'],
            min_morphball_attack_duration=data['min_morphball_attack_duration'],
            max_morphball_attack_duration=data['max_morphball_attack_duration'],
            unknown_0xd03984cd=data['unknown_0xd03984cd'],
            unknown_0xe831a7d0=data['unknown_0xe831a7d0'],
            unknown_0xbeb2b793=data['unknown_0xbeb2b793'],
            unknown_0x9d9d3760=data['unknown_0x9d9d3760'],
            morphball_animation=AnimationParameters.from_json(data['morphball_animation']),
            weapon_data=SpacePirateWeaponData.from_json(data['weapon_data']),
        )

    def to_json(self) -> dict:
        return {
            'death_explosion': self.death_explosion,
            'death_explosion_sound': self.death_explosion_sound,
            'part': self.part,
            'caud': self.caud,
            'initial_attack_time': self.initial_attack_time,
            'min_attack_time': self.min_attack_time,
            'attack_time_variance': self.attack_time_variance,
            'morphball_attack_speed': self.morphball_attack_speed,
            'morphball_attack_damage': self.morphball_attack_damage.to_json(),
            'unknown_0xc3a06ae1': self.unknown_0xc3a06ae1,
            'unknown_0x23e3c3bb': self.unknown_0x23e3c3bb,
            'min_morphball_attack_duration': self.min_morphball_attack_duration,
            'max_morphball_attack_duration': self.max_morphball_attack_duration,
            'unknown_0xd03984cd': self.unknown_0xd03984cd,
            'unknown_0xe831a7d0': self.unknown_0xe831a7d0,
            'unknown_0xbeb2b793': self.unknown_0xbeb2b793,
            'unknown_0x9d9d3760': self.unknown_0x9d9d3760,
            'morphball_animation': self.morphball_animation.to_json(),
            'weapon_data': self.weapon_data.to_json(),
        }


def _decode_death_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_death_explosion_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_initial_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_time_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morphball_attack_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morphball_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xc3a06ae1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x23e3c3bb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_morphball_attack_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_morphball_attack_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd03984cd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe831a7d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbeb2b793(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9d9d3760(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morphball_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_weapon_data(data: typing.BinaryIO, property_size: int):
    return SpacePirateWeaponData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x687c33e: ('death_explosion', _decode_death_explosion),
    0xed08fc4b: ('death_explosion_sound', _decode_death_explosion_sound),
    0x8f0400e2: ('part', _decode_part),
    0xccc7a920: ('caud', _decode_caud),
    0x446efcad: ('initial_attack_time', _decode_initial_attack_time),
    0x2edf3368: ('min_attack_time', _decode_min_attack_time),
    0x9f269614: ('attack_time_variance', _decode_attack_time_variance),
    0x992c7b48: ('morphball_attack_speed', _decode_morphball_attack_speed),
    0x76293001: ('morphball_attack_damage', _decode_morphball_attack_damage),
    0xc3a06ae1: ('unknown_0xc3a06ae1', _decode_unknown_0xc3a06ae1),
    0x23e3c3bb: ('unknown_0x23e3c3bb', _decode_unknown_0x23e3c3bb),
    0x597245a1: ('min_morphball_attack_duration', _decode_min_morphball_attack_duration),
    0x76ad063c: ('max_morphball_attack_duration', _decode_max_morphball_attack_duration),
    0xd03984cd: ('unknown_0xd03984cd', _decode_unknown_0xd03984cd),
    0xe831a7d0: ('unknown_0xe831a7d0', _decode_unknown_0xe831a7d0),
    0xbeb2b793: ('unknown_0xbeb2b793', _decode_unknown_0xbeb2b793),
    0x9d9d3760: ('unknown_0x9d9d3760', _decode_unknown_0x9d9d3760),
    0x26b752e1: ('morphball_animation', _decode_morphball_animation),
    0xdc89cc3c: ('weapon_data', _decode_weapon_data),
}
