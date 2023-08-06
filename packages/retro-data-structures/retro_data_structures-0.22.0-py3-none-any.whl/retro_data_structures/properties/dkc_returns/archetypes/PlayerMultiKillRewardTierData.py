# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class PlayerMultiKillRewardTierData(BaseProperty):
    item_to_give: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana)
    bop_threshold: int = dataclasses.field(default=1)
    throw_kill_threshold: int = dataclasses.field(default=1)
    barrel_cannon_kill_threshold: int = dataclasses.field(default=1)
    reward_speed: float = dataclasses.field(default=1.0)
    reward_target_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    reward_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    reward_reveal_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    reward_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xa0.\xf0\xc4')  # 0xa02ef0c4
        data.write(b'\x00\x04')  # size
        self.item_to_give.to_stream(data)

        data.write(b'{|&*')  # 0x7b7c262a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.bop_threshold))

        data.write(b'\xdb(\x9bU')  # 0xdb289b55
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.throw_kill_threshold))

        data.write(b'\xa7~\xfc\x04')  # 0xa77efc04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.barrel_cannon_kill_threshold))

        data.write(b'&X\x95\x8d')  # 0x2658958d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reward_speed))

        data.write(b'8K\xaf6')  # 0x384baf36
        data.write(b'\x00\x0c')  # size
        self.reward_target_scale.to_stream(data)

        data.write(b'\x87\xb5/L')  # 0x87b52f4c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reward_model))

        data.write(b'\xab[\x8c\xaf')  # 0xab5b8caf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reward_reveal_effect))

        data.write(b'\xb4\xa44I')  # 0xb4a43449
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reward_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            item_to_give=enums.PlayerItem.from_json(data['item_to_give']),
            bop_threshold=data['bop_threshold'],
            throw_kill_threshold=data['throw_kill_threshold'],
            barrel_cannon_kill_threshold=data['barrel_cannon_kill_threshold'],
            reward_speed=data['reward_speed'],
            reward_target_scale=Vector.from_json(data['reward_target_scale']),
            reward_model=data['reward_model'],
            reward_reveal_effect=data['reward_reveal_effect'],
            reward_effect=data['reward_effect'],
        )

    def to_json(self) -> dict:
        return {
            'item_to_give': self.item_to_give.to_json(),
            'bop_threshold': self.bop_threshold,
            'throw_kill_threshold': self.throw_kill_threshold,
            'barrel_cannon_kill_threshold': self.barrel_cannon_kill_threshold,
            'reward_speed': self.reward_speed,
            'reward_target_scale': self.reward_target_scale.to_json(),
            'reward_model': self.reward_model,
            'reward_reveal_effect': self.reward_reveal_effect,
            'reward_effect': self.reward_effect,
        }


def _decode_item_to_give(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_bop_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_throw_kill_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_barrel_cannon_kill_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_reward_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reward_target_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_reward_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reward_reveal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reward_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa02ef0c4: ('item_to_give', _decode_item_to_give),
    0x7b7c262a: ('bop_threshold', _decode_bop_threshold),
    0xdb289b55: ('throw_kill_threshold', _decode_throw_kill_threshold),
    0xa77efc04: ('barrel_cannon_kill_threshold', _decode_barrel_cannon_kill_threshold),
    0x2658958d: ('reward_speed', _decode_reward_speed),
    0x384baf36: ('reward_target_scale', _decode_reward_target_scale),
    0x87b52f4c: ('reward_model', _decode_reward_model),
    0xab5b8caf: ('reward_reveal_effect', _decode_reward_reveal_effect),
    0xb4a43449: ('reward_effect', _decode_reward_effect),
}
