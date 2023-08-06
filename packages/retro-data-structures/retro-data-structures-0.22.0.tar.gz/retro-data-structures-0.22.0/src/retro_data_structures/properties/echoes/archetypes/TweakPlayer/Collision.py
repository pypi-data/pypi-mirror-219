# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Collision(BaseProperty):
    player_height: float = dataclasses.field(default=2.700000047683716)
    player_radius: float = dataclasses.field(default=0.5)
    step_up_height: float = dataclasses.field(default=1.0)
    step_down_height: float = dataclasses.field(default=0.800000011920929)
    ball_radius: float = dataclasses.field(default=0.699999988079071)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        data.write(b'\xd0\xf3E\xb2')  # 0xd0f345b2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_height))

        data.write(b'j\x88AT')  # 0x6a884154
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_radius))

        data.write(b'\xd95Vt')  # 0xd9355674
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.step_up_height))

        data.write(b'\x88\xea\x81\xdb')  # 0x88ea81db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.step_down_height))

        data.write(b'\x0e/S\x7f')  # 0xe2f537f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_radius))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            player_height=data['player_height'],
            player_radius=data['player_radius'],
            step_up_height=data['step_up_height'],
            step_down_height=data['step_down_height'],
            ball_radius=data['ball_radius'],
        )

    def to_json(self) -> dict:
        return {
            'player_height': self.player_height,
            'player_radius': self.player_radius,
            'step_up_height': self.step_up_height,
            'step_down_height': self.step_down_height,
            'ball_radius': self.ball_radius,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xd0f345b2, 0x6a884154, 0xd9355674, 0x88ea81db, 0xe2f537f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Collision]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return Collision(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_player_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_step_up_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_step_down_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd0f345b2: ('player_height', _decode_player_height),
    0x6a884154: ('player_radius', _decode_player_radius),
    0xd9355674: ('step_up_height', _decode_step_up_height),
    0x88ea81db: ('step_down_height', _decode_step_down_height),
    0xe2f537f: ('ball_radius', _decode_ball_radius),
}
