# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct11(BaseProperty):
    shield_charge_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    shield_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xc1d9dbc6: float = dataclasses.field(default=15.0)
    unknown_0x927fc322: float = dataclasses.field(default=30.0)
    shield_charge_speed: float = dataclasses.field(default=40.0)
    shield_explode_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_shield_explode: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x6cb0da5a: float = dataclasses.field(default=50.0)
    unknown_0xc3938663: float = dataclasses.field(default=1.5)
    arm_shield_chance: float = dataclasses.field(default=50.0)
    arm_shield_time: float = dataclasses.field(default=4.0)
    unknown_0xe1b0efa0: float = dataclasses.field(default=1.0)
    arm_shield_explode_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    shield_charge_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    arm_shield_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_0xbf3c59b6: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x78be3b8d: int = dataclasses.field(default=0, metadata={'sound': True})

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'M\xa4\xa8\x94')  # 0x4da4a894
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_charge_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd3O\x13#')  # 0xd34f1323
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1\xd9\xdb\xc6')  # 0xc1d9dbc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc1d9dbc6))

        data.write(b'\x92\x7f\xc3"')  # 0x927fc322
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x927fc322))

        data.write(b'qx$\xb4')  # 0x717824b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shield_charge_speed))

        data.write(b'\xa4\x1fu\xef')  # 0xa41f75ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shield_explode_effect))

        data.write(b'\xe6\xe9.s')  # 0xe6e92e73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_shield_explode))

        data.write(b'l\xb0\xdaZ')  # 0x6cb0da5a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6cb0da5a))

        data.write(b'\xc3\x93\x86c')  # 0xc3938663
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc3938663))

        data.write(b'\x86\\\x10\x9c')  # 0x865c109c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arm_shield_chance))

        data.write(b'\x8bH\xa2\xf8')  # 0x8b48a2f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arm_shield_time))

        data.write(b'\xe1\xb0\xef\xa0')  # 0xe1b0efa0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe1b0efa0))

        data.write(b'\\\xa2\x06\xca')  # 0x5ca206ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.arm_shield_explode_effect))

        data.write(b'\xeb\xf6\x9c\xf0')  # 0xebf69cf0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shield_charge_effect))

        data.write(b'J\xabN\x04')  # 0x4aab4e04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.arm_shield_effect))

        data.write(b'\xbf<Y\xb6')  # 0xbf3c59b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xbf3c59b6))

        data.write(b'x\xbe;\x8d')  # 0x78be3b8d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x78be3b8d))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            shield_charge_damage=DamageInfo.from_json(data['shield_charge_damage']),
            shield_vulnerability=DamageVulnerability.from_json(data['shield_vulnerability']),
            unknown_0xc1d9dbc6=data['unknown_0xc1d9dbc6'],
            unknown_0x927fc322=data['unknown_0x927fc322'],
            shield_charge_speed=data['shield_charge_speed'],
            shield_explode_effect=data['shield_explode_effect'],
            sound_shield_explode=data['sound_shield_explode'],
            unknown_0x6cb0da5a=data['unknown_0x6cb0da5a'],
            unknown_0xc3938663=data['unknown_0xc3938663'],
            arm_shield_chance=data['arm_shield_chance'],
            arm_shield_time=data['arm_shield_time'],
            unknown_0xe1b0efa0=data['unknown_0xe1b0efa0'],
            arm_shield_explode_effect=data['arm_shield_explode_effect'],
            shield_charge_effect=data['shield_charge_effect'],
            arm_shield_effect=data['arm_shield_effect'],
            sound_0xbf3c59b6=data['sound_0xbf3c59b6'],
            sound_0x78be3b8d=data['sound_0x78be3b8d'],
        )

    def to_json(self) -> dict:
        return {
            'shield_charge_damage': self.shield_charge_damage.to_json(),
            'shield_vulnerability': self.shield_vulnerability.to_json(),
            'unknown_0xc1d9dbc6': self.unknown_0xc1d9dbc6,
            'unknown_0x927fc322': self.unknown_0x927fc322,
            'shield_charge_speed': self.shield_charge_speed,
            'shield_explode_effect': self.shield_explode_effect,
            'sound_shield_explode': self.sound_shield_explode,
            'unknown_0x6cb0da5a': self.unknown_0x6cb0da5a,
            'unknown_0xc3938663': self.unknown_0xc3938663,
            'arm_shield_chance': self.arm_shield_chance,
            'arm_shield_time': self.arm_shield_time,
            'unknown_0xe1b0efa0': self.unknown_0xe1b0efa0,
            'arm_shield_explode_effect': self.arm_shield_explode_effect,
            'shield_charge_effect': self.shield_charge_effect,
            'arm_shield_effect': self.arm_shield_effect,
            'sound_0xbf3c59b6': self.sound_0xbf3c59b6,
            'sound_0x78be3b8d': self.sound_0x78be3b8d,
        }

    def _dependencies_for_shield_charge_damage(self, asset_manager):
        yield from self.shield_charge_damage.dependencies_for(asset_manager)

    def _dependencies_for_shield_vulnerability(self, asset_manager):
        yield from self.shield_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_shield_explode_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shield_explode_effect)

    def _dependencies_for_sound_shield_explode(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_shield_explode)

    def _dependencies_for_arm_shield_explode_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.arm_shield_explode_effect)

    def _dependencies_for_shield_charge_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shield_charge_effect)

    def _dependencies_for_arm_shield_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.arm_shield_effect)

    def _dependencies_for_sound_0xbf3c59b6(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xbf3c59b6)

    def _dependencies_for_sound_0x78be3b8d(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x78be3b8d)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_shield_charge_damage, "shield_charge_damage", "DamageInfo"),
            (self._dependencies_for_shield_vulnerability, "shield_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_shield_explode_effect, "shield_explode_effect", "AssetId"),
            (self._dependencies_for_sound_shield_explode, "sound_shield_explode", "int"),
            (self._dependencies_for_arm_shield_explode_effect, "arm_shield_explode_effect", "AssetId"),
            (self._dependencies_for_shield_charge_effect, "shield_charge_effect", "AssetId"),
            (self._dependencies_for_arm_shield_effect, "arm_shield_effect", "AssetId"),
            (self._dependencies_for_sound_0xbf3c59b6, "sound_0xbf3c59b6", "int"),
            (self._dependencies_for_sound_0x78be3b8d, "sound_0x78be3b8d", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct11.{field_name} ({field_type}): {e}"
                )


def _decode_shield_charge_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})


def _decode_shield_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xc1d9dbc6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x927fc322(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shield_charge_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shield_explode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_shield_explode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6cb0da5a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc3938663(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arm_shield_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arm_shield_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe1b0efa0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arm_shield_explode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shield_charge_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_arm_shield_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0xbf3c59b6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x78be3b8d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4da4a894: ('shield_charge_damage', _decode_shield_charge_damage),
    0xd34f1323: ('shield_vulnerability', _decode_shield_vulnerability),
    0xc1d9dbc6: ('unknown_0xc1d9dbc6', _decode_unknown_0xc1d9dbc6),
    0x927fc322: ('unknown_0x927fc322', _decode_unknown_0x927fc322),
    0x717824b4: ('shield_charge_speed', _decode_shield_charge_speed),
    0xa41f75ef: ('shield_explode_effect', _decode_shield_explode_effect),
    0xe6e92e73: ('sound_shield_explode', _decode_sound_shield_explode),
    0x6cb0da5a: ('unknown_0x6cb0da5a', _decode_unknown_0x6cb0da5a),
    0xc3938663: ('unknown_0xc3938663', _decode_unknown_0xc3938663),
    0x865c109c: ('arm_shield_chance', _decode_arm_shield_chance),
    0x8b48a2f8: ('arm_shield_time', _decode_arm_shield_time),
    0xe1b0efa0: ('unknown_0xe1b0efa0', _decode_unknown_0xe1b0efa0),
    0x5ca206ca: ('arm_shield_explode_effect', _decode_arm_shield_explode_effect),
    0xebf69cf0: ('shield_charge_effect', _decode_shield_charge_effect),
    0x4aab4e04: ('arm_shield_effect', _decode_arm_shield_effect),
    0xbf3c59b6: ('sound_0xbf3c59b6', _decode_sound_0xbf3c59b6),
    0x78be3b8d: ('sound_0x78be3b8d', _decode_sound_0x78be3b8d),
}
