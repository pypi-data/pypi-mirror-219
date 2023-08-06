# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class KongGroundPoundData(BaseProperty):
    ground_pound_box_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=30.0, y=30.0, z=30.0))
    min_delay_between_slaps: float = dataclasses.field(default=0.10000000149011612)
    delay_between_same_hand_slaps: float = dataclasses.field(default=1.0)
    delay_horizontal_movement_after_slap: float = dataclasses.field(default=1.0)
    delay_jumping_after_slap: float = dataclasses.field(default=0.5)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xdb\xb1>\x19')  # 0xdbb13e19
        data.write(b'\x00\x0c')  # size
        self.ground_pound_box_scale.to_stream(data)

        data.write(b'E\x8f{\x04')  # 0x458f7b04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_delay_between_slaps))

        data.write(b'\xa6\xa1\xcd\x8f')  # 0xa6a1cd8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_between_same_hand_slaps))

        data.write(b'=#>S')  # 0x3d233e53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_horizontal_movement_after_slap))

        data.write(b'\xa4\xab\x00\xa8')  # 0xa4ab00a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_jumping_after_slap))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ground_pound_box_scale=Vector.from_json(data['ground_pound_box_scale']),
            min_delay_between_slaps=data['min_delay_between_slaps'],
            delay_between_same_hand_slaps=data['delay_between_same_hand_slaps'],
            delay_horizontal_movement_after_slap=data['delay_horizontal_movement_after_slap'],
            delay_jumping_after_slap=data['delay_jumping_after_slap'],
        )

    def to_json(self) -> dict:
        return {
            'ground_pound_box_scale': self.ground_pound_box_scale.to_json(),
            'min_delay_between_slaps': self.min_delay_between_slaps,
            'delay_between_same_hand_slaps': self.delay_between_same_hand_slaps,
            'delay_horizontal_movement_after_slap': self.delay_horizontal_movement_after_slap,
            'delay_jumping_after_slap': self.delay_jumping_after_slap,
        }


def _decode_ground_pound_box_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_min_delay_between_slaps(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_between_same_hand_slaps(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_horizontal_movement_after_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_jumping_after_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdbb13e19: ('ground_pound_box_scale', _decode_ground_pound_box_scale),
    0x458f7b04: ('min_delay_between_slaps', _decode_min_delay_between_slaps),
    0xa6a1cd8f: ('delay_between_same_hand_slaps', _decode_delay_between_same_hand_slaps),
    0x3d233e53: ('delay_horizontal_movement_after_slap', _decode_delay_horizontal_movement_after_slap),
    0xa4ab00a8: ('delay_jumping_after_slap', _decode_delay_jumping_after_slap),
}
