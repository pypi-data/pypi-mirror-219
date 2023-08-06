# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.UnknownStruct50 import UnknownStruct50
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct51(BaseProperty):
    unknown_0xdbd7b020: bool = dataclasses.field(default=False)
    unknown_0xf8ec7014: bool = dataclasses.field(default=False)
    anti_drain_time: float = dataclasses.field(default=2.0)
    unknown_0x363f4a77: float = dataclasses.field(default=30.0)
    is_orbitable: bool = dataclasses.field(default=True)
    hover_speed: float = dataclasses.field(default=3.0)
    attack_delay_time: float = dataclasses.field(default=5.0)
    unknown_0x5a426481: float = dataclasses.field(default=15.0)
    unknown_0x3b846868: float = dataclasses.field(default=25.0)
    unknown_0x809644dc: float = dataclasses.field(default=2.0)
    phazon_drain_amount: float = dataclasses.field(default=10.0)
    unknown_0x0d522c38: float = dataclasses.field(default=1.0)
    launch_projectile_data: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    phazon_drain_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_struct50: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50)
    normal_electric_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0x934e82b5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    starts_prevent_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xf13facaf: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    turn_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'\xdb\xd7\xb0 ')  # 0xdbd7b020
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdbd7b020))

        data.write(b'\xf8\xecp\x14')  # 0xf8ec7014
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf8ec7014))

        data.write(b'H\xd9H+')  # 0x48d9482b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anti_drain_time))

        data.write(b'6?Jw')  # 0x363f4a77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x363f4a77))

        data.write(b'\x82k\xec\x80')  # 0x826bec80
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_orbitable))

        data.write(b'\x84^\xf4\x89')  # 0x845ef489
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_speed))

        data.write(b'+\x810\xb7')  # 0x2b8130b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_delay_time))

        data.write(b'ZBd\x81')  # 0x5a426481
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5a426481))

        data.write(b';\x84hh')  # 0x3b846868
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b846868))

        data.write(b'\x80\x96D\xdc')  # 0x809644dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x809644dc))

        data.write(b'\x033mI')  # 0x3336d49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_drain_amount))

        data.write(b'\rR,8')  # 0xd522c38
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0d522c38))

        data.write(b'P\xaenU')  # 0x50ae6e55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'u\x18\xcdF')  # 0x7518cd46
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.phazon_drain_visor_effect))

        data.write(b'\x97\x9d\x0c\xfa')  # 0x979d0cfa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'b\xaci\x15')  # 0x62ac6915
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_electric_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93N\x82\xb5')  # 0x934e82b5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x934e82b5))

        data.write(b'"\x1a\x90-')  # 0x221a902d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.starts_prevent_effect))

        data.write(b'\xf1?\xac\xaf')  # 0xf13facaf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xf13facaf))

        data.write(b'\xc4\xc3\x94\x03')  # 0xc4c39403
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.turn_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xdbd7b020=data['unknown_0xdbd7b020'],
            unknown_0xf8ec7014=data['unknown_0xf8ec7014'],
            anti_drain_time=data['anti_drain_time'],
            unknown_0x363f4a77=data['unknown_0x363f4a77'],
            is_orbitable=data['is_orbitable'],
            hover_speed=data['hover_speed'],
            attack_delay_time=data['attack_delay_time'],
            unknown_0x5a426481=data['unknown_0x5a426481'],
            unknown_0x3b846868=data['unknown_0x3b846868'],
            unknown_0x809644dc=data['unknown_0x809644dc'],
            phazon_drain_amount=data['phazon_drain_amount'],
            unknown_0x0d522c38=data['unknown_0x0d522c38'],
            launch_projectile_data=LaunchProjectileData.from_json(data['launch_projectile_data']),
            phazon_drain_visor_effect=data['phazon_drain_visor_effect'],
            unknown_struct50=UnknownStruct50.from_json(data['unknown_struct50']),
            normal_electric_damage_info=DamageInfo.from_json(data['normal_electric_damage_info']),
            part_0x934e82b5=data['part_0x934e82b5'],
            starts_prevent_effect=data['starts_prevent_effect'],
            part_0xf13facaf=data['part_0xf13facaf'],
            turn_sound=data['turn_sound'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xdbd7b020': self.unknown_0xdbd7b020,
            'unknown_0xf8ec7014': self.unknown_0xf8ec7014,
            'anti_drain_time': self.anti_drain_time,
            'unknown_0x363f4a77': self.unknown_0x363f4a77,
            'is_orbitable': self.is_orbitable,
            'hover_speed': self.hover_speed,
            'attack_delay_time': self.attack_delay_time,
            'unknown_0x5a426481': self.unknown_0x5a426481,
            'unknown_0x3b846868': self.unknown_0x3b846868,
            'unknown_0x809644dc': self.unknown_0x809644dc,
            'phazon_drain_amount': self.phazon_drain_amount,
            'unknown_0x0d522c38': self.unknown_0x0d522c38,
            'launch_projectile_data': self.launch_projectile_data.to_json(),
            'phazon_drain_visor_effect': self.phazon_drain_visor_effect,
            'unknown_struct50': self.unknown_struct50.to_json(),
            'normal_electric_damage_info': self.normal_electric_damage_info.to_json(),
            'part_0x934e82b5': self.part_0x934e82b5,
            'starts_prevent_effect': self.starts_prevent_effect,
            'part_0xf13facaf': self.part_0xf13facaf,
            'turn_sound': self.turn_sound,
        }


def _decode_unknown_0xdbd7b020(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf8ec7014(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_anti_drain_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x363f4a77(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_orbitable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_hover_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5a426481(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3b846868(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x809644dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_drain_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0d522c38(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_projectile_data(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_phazon_drain_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct50(data: typing.BinaryIO, property_size: int):
    return UnknownStruct50.from_stream(data, property_size)


def _decode_normal_electric_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_part_0x934e82b5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_starts_prevent_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xf13facaf(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_turn_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdbd7b020: ('unknown_0xdbd7b020', _decode_unknown_0xdbd7b020),
    0xf8ec7014: ('unknown_0xf8ec7014', _decode_unknown_0xf8ec7014),
    0x48d9482b: ('anti_drain_time', _decode_anti_drain_time),
    0x363f4a77: ('unknown_0x363f4a77', _decode_unknown_0x363f4a77),
    0x826bec80: ('is_orbitable', _decode_is_orbitable),
    0x845ef489: ('hover_speed', _decode_hover_speed),
    0x2b8130b7: ('attack_delay_time', _decode_attack_delay_time),
    0x5a426481: ('unknown_0x5a426481', _decode_unknown_0x5a426481),
    0x3b846868: ('unknown_0x3b846868', _decode_unknown_0x3b846868),
    0x809644dc: ('unknown_0x809644dc', _decode_unknown_0x809644dc),
    0x3336d49: ('phazon_drain_amount', _decode_phazon_drain_amount),
    0xd522c38: ('unknown_0x0d522c38', _decode_unknown_0x0d522c38),
    0x50ae6e55: ('launch_projectile_data', _decode_launch_projectile_data),
    0x7518cd46: ('phazon_drain_visor_effect', _decode_phazon_drain_visor_effect),
    0x979d0cfa: ('unknown_struct50', _decode_unknown_struct50),
    0x62ac6915: ('normal_electric_damage_info', _decode_normal_electric_damage_info),
    0x934e82b5: ('part_0x934e82b5', _decode_part_0x934e82b5),
    0x221a902d: ('starts_prevent_effect', _decode_starts_prevent_effect),
    0xf13facaf: ('part_0xf13facaf', _decode_part_0xf13facaf),
    0xc4c39403: ('turn_sound', _decode_turn_sound),
}
