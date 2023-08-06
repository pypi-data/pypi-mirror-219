# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct59(BaseProperty):
    initial_swarm_size: int = dataclasses.field(default=30)
    unknown_0xb3f4ee57: float = dataclasses.field(default=30.0)
    chase_player_speed: float = dataclasses.field(default=4.0)
    char: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    swarm_bot_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    part_0xb64ed093: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x8fe03c41: float = dataclasses.field(default=0.10000000149011612)
    ring_idle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x4d9ed8e1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ring_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    ring_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    bot_contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    visor_impact_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xbe\xa7A8')  # 0xbea74138
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.initial_swarm_size))

        data.write(b'\xb3\xf4\xeeW')  # 0xb3f4ee57
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb3f4ee57))

        data.write(b'\x11i \xb8')  # 0x116920b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_player_speed))

        data.write(b'Ld\xd3\xa6')  # 0x4c64d3a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.char.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xdd\x06\xcc')  # 0xdd06cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swarm_bot_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6N\xd0\x93')  # 0xb64ed093
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xb64ed093))

        data.write(b'\x8f\xe0<A')  # 0x8fe03c41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8fe03c41))

        data.write(b'\xc9\x0c\xda\x8c')  # 0xc90cda8c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ring_idle_effect))

        data.write(b'M\x9e\xd8\xe1')  # 0x4d9ed8e1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x4d9ed8e1))

        data.write(b'!\xdcL5')  # 0x21dc4c35
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ring_projectile))

        data.write(b'\x18\xf9\x18\x80')  # 0x18f91880
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ring_projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\xb5\xa8\xc3')  # 0xfcb5a8c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bot_contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9\xc8\xe2\xbd')  # 0xe9c8e2bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect))

        data.write(b'\x86\xff\xb3\xf6')  # 0x86ffb3f6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_impact_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_swarm_size=data['initial_swarm_size'],
            unknown_0xb3f4ee57=data['unknown_0xb3f4ee57'],
            chase_player_speed=data['chase_player_speed'],
            char=AnimationParameters.from_json(data['char']),
            swarm_bot_vulnerability=DamageVulnerability.from_json(data['swarm_bot_vulnerability']),
            part_0xb64ed093=data['part_0xb64ed093'],
            unknown_0x8fe03c41=data['unknown_0x8fe03c41'],
            ring_idle_effect=data['ring_idle_effect'],
            part_0x4d9ed8e1=data['part_0x4d9ed8e1'],
            ring_projectile=data['ring_projectile'],
            ring_projectile_damage=DamageInfo.from_json(data['ring_projectile_damage']),
            bot_contact_damage=DamageInfo.from_json(data['bot_contact_damage']),
            visor_effect=data['visor_effect'],
            visor_impact_sound=data['visor_impact_sound'],
        )

    def to_json(self) -> dict:
        return {
            'initial_swarm_size': self.initial_swarm_size,
            'unknown_0xb3f4ee57': self.unknown_0xb3f4ee57,
            'chase_player_speed': self.chase_player_speed,
            'char': self.char.to_json(),
            'swarm_bot_vulnerability': self.swarm_bot_vulnerability.to_json(),
            'part_0xb64ed093': self.part_0xb64ed093,
            'unknown_0x8fe03c41': self.unknown_0x8fe03c41,
            'ring_idle_effect': self.ring_idle_effect,
            'part_0x4d9ed8e1': self.part_0x4d9ed8e1,
            'ring_projectile': self.ring_projectile,
            'ring_projectile_damage': self.ring_projectile_damage.to_json(),
            'bot_contact_damage': self.bot_contact_damage.to_json(),
            'visor_effect': self.visor_effect,
            'visor_impact_sound': self.visor_impact_sound,
        }


def _decode_initial_swarm_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb3f4ee57(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_player_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_char(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_swarm_bot_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_part_0xb64ed093(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x8fe03c41(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ring_idle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x4d9ed8e1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ring_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ring_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_bot_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_visor_impact_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbea74138: ('initial_swarm_size', _decode_initial_swarm_size),
    0xb3f4ee57: ('unknown_0xb3f4ee57', _decode_unknown_0xb3f4ee57),
    0x116920b8: ('chase_player_speed', _decode_chase_player_speed),
    0x4c64d3a6: ('char', _decode_char),
    0xdd06cc: ('swarm_bot_vulnerability', _decode_swarm_bot_vulnerability),
    0xb64ed093: ('part_0xb64ed093', _decode_part_0xb64ed093),
    0x8fe03c41: ('unknown_0x8fe03c41', _decode_unknown_0x8fe03c41),
    0xc90cda8c: ('ring_idle_effect', _decode_ring_idle_effect),
    0x4d9ed8e1: ('part_0x4d9ed8e1', _decode_part_0x4d9ed8e1),
    0x21dc4c35: ('ring_projectile', _decode_ring_projectile),
    0x18f91880: ('ring_projectile_damage', _decode_ring_projectile_damage),
    0xfcb5a8c3: ('bot_contact_damage', _decode_bot_contact_damage),
    0xe9c8e2bd: ('visor_effect', _decode_visor_effect),
    0x86ffb3f6: ('visor_impact_sound', _decode_visor_impact_sound),
}
