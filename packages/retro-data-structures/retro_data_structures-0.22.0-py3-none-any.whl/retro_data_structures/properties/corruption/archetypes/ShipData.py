# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.Vector2f import Vector2f
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShipData(BaseProperty):
    samus_ship: bool = dataclasses.field(default=False)
    shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    shot_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_shot: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xd5039d33: float = dataclasses.field(default=0.5)
    speed: float = dataclasses.field(default=10.0)
    unknown_0x04c4e40b: bool = dataclasses.field(default=True)
    vector2f: Vector2f = dataclasses.field(default_factory=Vector2f)
    thruster_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x7ebd51de: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    swhc_0x25bd3372: AssetId = dataclasses.field(metadata={'asset_types': ['SWHC']}, default=default_asset_id)
    swhc_0xa32941dc: AssetId = dataclasses.field(metadata={'asset_types': ['SWHC']}, default=default_asset_id)
    part_0x2f335270: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grapple_claw_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_thrust: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x497c0d5e: bool = dataclasses.field(default=True)
    unknown_0xb6eacc28: float = dataclasses.field(default=40.0)
    command_visor_animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b't.\t"')  # 0x742e0922
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.samus_ship))

        data.write(b'Q%;\xa3')  # 0x51253ba3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shot_projectile))

        data.write(b'\xce\xa3\x018')  # 0xcea30138
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shot_damage.to_stream(data, default_override={'di_weapon_type': enums.DI_WeaponType.Friendly, 'di_damage': 50.0, 'di_radius': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2:\x19U')  # 0xc23a1955
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_shot))

        data.write(b'\xd5\x03\x9d3')  # 0xd5039d33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd5039d33))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'\x04\xc4\xe4\x0b')  # 0x4c4e40b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x04c4e40b))

        data.write(b'J\xba\xde\x16')  # 0x4abade16
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vector2f.to_stream(data, default_override={'x': 90.0, 'y': 90.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jCc\x9f')  # 0x6a43639f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.thruster_effect))

        data.write(b'~\xbdQ\xde')  # 0x7ebd51de
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x7ebd51de))

        data.write(b'%\xbd3r')  # 0x25bd3372
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.swhc_0x25bd3372))

        data.write(b'\xa3)A\xdc')  # 0xa32941dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.swhc_0xa32941dc))

        data.write(b'/3Rp')  # 0x2f335270
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x2f335270))

        data.write(b'\xb6\x85\xfe\xee')  # 0xb685feee
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.grapple_claw_effect))

        data.write(b'\xd3\x02>l')  # 0xd3023e6c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_thrust))

        data.write(b'I|\r^')  # 0x497c0d5e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x497c0d5e))

        data.write(b'\xb6\xea\xcc(')  # 0xb6eacc28
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb6eacc28))

        data.write(b'}8\xc0\xbe')  # 0x7d38c0be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command_visor_animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            samus_ship=data['samus_ship'],
            shot_projectile=data['shot_projectile'],
            shot_damage=DamageInfo.from_json(data['shot_damage']),
            sound_shot=data['sound_shot'],
            unknown_0xd5039d33=data['unknown_0xd5039d33'],
            speed=data['speed'],
            unknown_0x04c4e40b=data['unknown_0x04c4e40b'],
            vector2f=Vector2f.from_json(data['vector2f']),
            thruster_effect=data['thruster_effect'],
            part_0x7ebd51de=data['part_0x7ebd51de'],
            swhc_0x25bd3372=data['swhc_0x25bd3372'],
            swhc_0xa32941dc=data['swhc_0xa32941dc'],
            part_0x2f335270=data['part_0x2f335270'],
            grapple_claw_effect=data['grapple_claw_effect'],
            sound_thrust=data['sound_thrust'],
            unknown_0x497c0d5e=data['unknown_0x497c0d5e'],
            unknown_0xb6eacc28=data['unknown_0xb6eacc28'],
            command_visor_animation=AnimationParameters.from_json(data['command_visor_animation']),
        )

    def to_json(self) -> dict:
        return {
            'samus_ship': self.samus_ship,
            'shot_projectile': self.shot_projectile,
            'shot_damage': self.shot_damage.to_json(),
            'sound_shot': self.sound_shot,
            'unknown_0xd5039d33': self.unknown_0xd5039d33,
            'speed': self.speed,
            'unknown_0x04c4e40b': self.unknown_0x04c4e40b,
            'vector2f': self.vector2f.to_json(),
            'thruster_effect': self.thruster_effect,
            'part_0x7ebd51de': self.part_0x7ebd51de,
            'swhc_0x25bd3372': self.swhc_0x25bd3372,
            'swhc_0xa32941dc': self.swhc_0xa32941dc,
            'part_0x2f335270': self.part_0x2f335270,
            'grapple_claw_effect': self.grapple_claw_effect,
            'sound_thrust': self.sound_thrust,
            'unknown_0x497c0d5e': self.unknown_0x497c0d5e,
            'unknown_0xb6eacc28': self.unknown_0xb6eacc28,
            'command_visor_animation': self.command_visor_animation.to_json(),
        }


def _decode_samus_ship(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shot_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': enums.DI_WeaponType.Friendly, 'di_damage': 50.0, 'di_radius': 20.0, 'di_knock_back_power': 5.0})


def _decode_sound_shot(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xd5039d33(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x04c4e40b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_vector2f(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size, default_override={'x': 90.0, 'y': 90.0})


def _decode_thruster_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x7ebd51de(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_swhc_0x25bd3372(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_swhc_0xa32941dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x2f335270(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_grapple_claw_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_thrust(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x497c0d5e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb6eacc28(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_command_visor_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x742e0922: ('samus_ship', _decode_samus_ship),
    0x51253ba3: ('shot_projectile', _decode_shot_projectile),
    0xcea30138: ('shot_damage', _decode_shot_damage),
    0xc23a1955: ('sound_shot', _decode_sound_shot),
    0xd5039d33: ('unknown_0xd5039d33', _decode_unknown_0xd5039d33),
    0x6392404e: ('speed', _decode_speed),
    0x4c4e40b: ('unknown_0x04c4e40b', _decode_unknown_0x04c4e40b),
    0x4abade16: ('vector2f', _decode_vector2f),
    0x6a43639f: ('thruster_effect', _decode_thruster_effect),
    0x7ebd51de: ('part_0x7ebd51de', _decode_part_0x7ebd51de),
    0x25bd3372: ('swhc_0x25bd3372', _decode_swhc_0x25bd3372),
    0xa32941dc: ('swhc_0xa32941dc', _decode_swhc_0xa32941dc),
    0x2f335270: ('part_0x2f335270', _decode_part_0x2f335270),
    0xb685feee: ('grapple_claw_effect', _decode_grapple_claw_effect),
    0xd3023e6c: ('sound_thrust', _decode_sound_thrust),
    0x497c0d5e: ('unknown_0x497c0d5e', _decode_unknown_0x497c0d5e),
    0xb6eacc28: ('unknown_0xb6eacc28', _decode_unknown_0xb6eacc28),
    0x7d38c0be: ('command_visor_animation', _decode_command_visor_animation),
}
