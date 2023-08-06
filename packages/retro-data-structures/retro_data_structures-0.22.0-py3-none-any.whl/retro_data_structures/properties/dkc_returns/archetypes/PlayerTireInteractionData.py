# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerTireInteractionData(BaseProperty):
    pre_tire_jump_buffer: float = dataclasses.field(default=0.10000000149011612)
    pre_tire_jump_buffer_sd: float = dataclasses.field(default=0.20000000298023224)
    programmatic_turn_speed: float = dataclasses.field(default=450.0)
    bump_into_tire_wall_min_speed: float = dataclasses.field(default=3.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'>eA\x0c')  # 0x3e65410c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_tire_jump_buffer))

        data.write(b'xM\x14?')  # 0x784d143f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_tire_jump_buffer_sd))

        data.write(b'\xcf\x03\xcb\x0c')  # 0xcf03cb0c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.programmatic_turn_speed))

        data.write(b':2\xdf\xcb')  # 0x3a32dfcb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bump_into_tire_wall_min_speed))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            pre_tire_jump_buffer=data['pre_tire_jump_buffer'],
            pre_tire_jump_buffer_sd=data['pre_tire_jump_buffer_sd'],
            programmatic_turn_speed=data['programmatic_turn_speed'],
            bump_into_tire_wall_min_speed=data['bump_into_tire_wall_min_speed'],
        )

    def to_json(self) -> dict:
        return {
            'pre_tire_jump_buffer': self.pre_tire_jump_buffer,
            'pre_tire_jump_buffer_sd': self.pre_tire_jump_buffer_sd,
            'programmatic_turn_speed': self.programmatic_turn_speed,
            'bump_into_tire_wall_min_speed': self.bump_into_tire_wall_min_speed,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x3e65410c, 0x784d143f, 0xcf03cb0c, 0x3a32dfcb)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerTireInteractionData]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerTireInteractionData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_pre_tire_jump_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pre_tire_jump_buffer_sd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_programmatic_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bump_into_tire_wall_min_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3e65410c: ('pre_tire_jump_buffer', _decode_pre_tire_jump_buffer),
    0x784d143f: ('pre_tire_jump_buffer_sd', _decode_pre_tire_jump_buffer_sd),
    0xcf03cb0c: ('programmatic_turn_speed', _decode_programmatic_turn_speed),
    0x3a32dfcb: ('bump_into_tire_wall_min_speed', _decode_bump_into_tire_wall_min_speed),
}
