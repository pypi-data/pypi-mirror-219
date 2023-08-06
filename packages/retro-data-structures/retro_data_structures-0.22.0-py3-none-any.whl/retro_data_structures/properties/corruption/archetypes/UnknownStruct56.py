# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct56(BaseProperty):
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    roll_speed_scale: float = dataclasses.field(default=1.2999999523162842)
    unknown_0x205db165: float = dataclasses.field(default=3.5)
    unknown_0x45515b5e: float = dataclasses.field(default=10.0)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    trail_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    glow_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    wall_collision_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    player_collision_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'`\xacqu')  # 0x60ac7175
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_speed_scale))

        data.write(b' ]\xb1e')  # 0x205db165
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x205db165))

        data.write(b'EQ[^')  # 0x45515b5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x45515b5e))

        data.write(b'\xc9p\x13\xd0')  # 0xc97013d0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xee\xe7\x91')  # 0x36eee791
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.trail_effect))

        data.write(b'\x84[\xd2\xee')  # 0x845bd2ee
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.glow_effect))

        data.write(b'O\xab\xa7\x8a')  # 0x4faba78a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wall_collision_sound))

        data.write(b'\xe9\x00i\xbd')  # 0xe90069bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.player_collision_sound))

        data.write(b'j\xb7\xc2\xf5')  # 0x6ab7c2f5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            animation=AnimationParameters.from_json(data['animation']),
            roll_speed_scale=data['roll_speed_scale'],
            unknown_0x205db165=data['unknown_0x205db165'],
            unknown_0x45515b5e=data['unknown_0x45515b5e'],
            damage_info=DamageInfo.from_json(data['damage_info']),
            trail_effect=data['trail_effect'],
            glow_effect=data['glow_effect'],
            wall_collision_sound=data['wall_collision_sound'],
            player_collision_sound=data['player_collision_sound'],
            caud=data['caud'],
        )

    def to_json(self) -> dict:
        return {
            'animation': self.animation.to_json(),
            'roll_speed_scale': self.roll_speed_scale,
            'unknown_0x205db165': self.unknown_0x205db165,
            'unknown_0x45515b5e': self.unknown_0x45515b5e,
            'damage_info': self.damage_info.to_json(),
            'trail_effect': self.trail_effect,
            'glow_effect': self.glow_effect,
            'wall_collision_sound': self.wall_collision_sound,
            'player_collision_sound': self.player_collision_sound,
            'caud': self.caud,
        }


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_roll_speed_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x205db165(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x45515b5e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_trail_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_glow_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wall_collision_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_player_collision_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa3d63f44: ('animation', _decode_animation),
    0x60ac7175: ('roll_speed_scale', _decode_roll_speed_scale),
    0x205db165: ('unknown_0x205db165', _decode_unknown_0x205db165),
    0x45515b5e: ('unknown_0x45515b5e', _decode_unknown_0x45515b5e),
    0xc97013d0: ('damage_info', _decode_damage_info),
    0x36eee791: ('trail_effect', _decode_trail_effect),
    0x845bd2ee: ('glow_effect', _decode_glow_effect),
    0x4faba78a: ('wall_collision_sound', _decode_wall_collision_sound),
    0xe90069bd: ('player_collision_sound', _decode_player_collision_sound),
    0x6ab7c2f5: ('caud', _decode_caud),
}
