# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAttackBounceData import PlayerAttackBounceData


@dataclasses.dataclass()
class PlayerJumpHeights(BaseProperty):
    minimum_jump_height: float = dataclasses.field(default=2.0)
    maximum_jump_height: float = dataclasses.field(default=4.5)
    attack_bounce_data: PlayerAttackBounceData = dataclasses.field(default_factory=PlayerAttackBounceData)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'yz\xa5Q')  # 0x797aa551
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_jump_height))

        data.write(b'8m\x9a\xd7')  # 0x386d9ad7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_jump_height))

        data.write(b'\x95\x83\xee\x9a')  # 0x9583ee9a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_bounce_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            minimum_jump_height=data['minimum_jump_height'],
            maximum_jump_height=data['maximum_jump_height'],
            attack_bounce_data=PlayerAttackBounceData.from_json(data['attack_bounce_data']),
        )

    def to_json(self) -> dict:
        return {
            'minimum_jump_height': self.minimum_jump_height,
            'maximum_jump_height': self.maximum_jump_height,
            'attack_bounce_data': self.attack_bounce_data.to_json(),
        }


def _decode_minimum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_bounce_data(data: typing.BinaryIO, property_size: int):
    return PlayerAttackBounceData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x797aa551: ('minimum_jump_height', _decode_minimum_jump_height),
    0x386d9ad7: ('maximum_jump_height', _decode_maximum_jump_height),
    0x9583ee9a: ('attack_bounce_data', _decode_attack_bounce_data),
}
