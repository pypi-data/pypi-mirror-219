# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerCommonData(BaseProperty):
    player: int = dataclasses.field(default=0)
    anim_scale: float = dataclasses.field(default=1.0)
    character_type: PlayerType = dataclasses.field(default_factory=PlayerType)
    ledge_assist_step_up_height: float = dataclasses.field(default=0.949999988079071)
    gravity: float = dataclasses.field(default=55.0)
    terminal_velocity: float = dataclasses.field(default=35.0)
    invulnerable_time: float = dataclasses.field(default=2.0)
    invulnerable_blink_time: float = dataclasses.field(default=0.125)
    damage_knock_back_input_disable_time: float = dataclasses.field(default=0.20000000298023224)
    respawn_render_push_amount: float = dataclasses.field(default=0.0)
    use_terrain_alignment: bool = dataclasses.field(default=True)
    allow_collision_with_mine_cart_tracks: bool = dataclasses.field(default=False)
    allow_death_delete: bool = dataclasses.field(default=False)
    respawn_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    respawn_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x96\xf8\x97\x02')  # 0x96f89702
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.player))

        data.write(b'\x18x\xfa\x08')  # 0x1878fa08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anim_scale))

        data.write(b'\x01>5\xfb')  # 0x13e35fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\x1f\xb5\xce')  # 0xa21fb5ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ledge_assist_step_up_height))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xab\x95f\xa2')  # 0xab9566a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terminal_velocity))

        data.write(b'\xac\x01ZG')  # 0xac015a47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.invulnerable_time))

        data.write(b'H\xbex\x80')  # 0x48be7880
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.invulnerable_blink_time))

        data.write(b'\x97Cc{')  # 0x9743637b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_knock_back_input_disable_time))

        data.write(b'\xb1\x98\xe71')  # 0xb198e731
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_render_push_amount))

        data.write(b'a\x17\xe7\x8f')  # 0x6117e78f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_terrain_alignment))

        data.write(b'\x91{Z\xd5')  # 0x917b5ad5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_collision_with_mine_cart_tracks))

        data.write(b'{61\x00')  # 0x7b363100
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_death_delete))

        data.write(b'.P\xdc\xec')  # 0x2e50dcec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.respawn_sound))

        data.write(b'Ke\x99\x9c')  # 0x4b65999c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.respawn_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            player=data['player'],
            anim_scale=data['anim_scale'],
            character_type=PlayerType.from_json(data['character_type']),
            ledge_assist_step_up_height=data['ledge_assist_step_up_height'],
            gravity=data['gravity'],
            terminal_velocity=data['terminal_velocity'],
            invulnerable_time=data['invulnerable_time'],
            invulnerable_blink_time=data['invulnerable_blink_time'],
            damage_knock_back_input_disable_time=data['damage_knock_back_input_disable_time'],
            respawn_render_push_amount=data['respawn_render_push_amount'],
            use_terrain_alignment=data['use_terrain_alignment'],
            allow_collision_with_mine_cart_tracks=data['allow_collision_with_mine_cart_tracks'],
            allow_death_delete=data['allow_death_delete'],
            respawn_sound=data['respawn_sound'],
            respawn_effect=data['respawn_effect'],
        )

    def to_json(self) -> dict:
        return {
            'player': self.player,
            'anim_scale': self.anim_scale,
            'character_type': self.character_type.to_json(),
            'ledge_assist_step_up_height': self.ledge_assist_step_up_height,
            'gravity': self.gravity,
            'terminal_velocity': self.terminal_velocity,
            'invulnerable_time': self.invulnerable_time,
            'invulnerable_blink_time': self.invulnerable_blink_time,
            'damage_knock_back_input_disable_time': self.damage_knock_back_input_disable_time,
            'respawn_render_push_amount': self.respawn_render_push_amount,
            'use_terrain_alignment': self.use_terrain_alignment,
            'allow_collision_with_mine_cart_tracks': self.allow_collision_with_mine_cart_tracks,
            'allow_death_delete': self.allow_death_delete,
            'respawn_sound': self.respawn_sound,
            'respawn_effect': self.respawn_effect,
        }


def _decode_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_anim_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_character_type(data: typing.BinaryIO, property_size: int):
    return PlayerType.from_stream(data, property_size)


def _decode_ledge_assist_step_up_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terminal_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_invulnerable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_invulnerable_blink_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_knock_back_input_disable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_respawn_render_push_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_terrain_alignment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_collision_with_mine_cart_tracks(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_death_delete(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_respawn_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_respawn_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x96f89702: ('player', _decode_player),
    0x1878fa08: ('anim_scale', _decode_anim_scale),
    0x13e35fb: ('character_type', _decode_character_type),
    0xa21fb5ce: ('ledge_assist_step_up_height', _decode_ledge_assist_step_up_height),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xab9566a2: ('terminal_velocity', _decode_terminal_velocity),
    0xac015a47: ('invulnerable_time', _decode_invulnerable_time),
    0x48be7880: ('invulnerable_blink_time', _decode_invulnerable_blink_time),
    0x9743637b: ('damage_knock_back_input_disable_time', _decode_damage_knock_back_input_disable_time),
    0xb198e731: ('respawn_render_push_amount', _decode_respawn_render_push_amount),
    0x6117e78f: ('use_terrain_alignment', _decode_use_terrain_alignment),
    0x917b5ad5: ('allow_collision_with_mine_cart_tracks', _decode_allow_collision_with_mine_cart_tracks),
    0x7b363100: ('allow_death_delete', _decode_allow_death_delete),
    0x2e50dcec: ('respawn_sound', _decode_respawn_sound),
    0x4b65999c: ('respawn_effect', _decode_respawn_effect),
}
