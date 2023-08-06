# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct269(BaseProperty):
    move: bool = dataclasses.field(default=True)
    roll: bool = dataclasses.field(default=True)
    ground_pound: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xad\xd74\xc9')  # 0xadd734c9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.move))

        data.write(b'\xa7\x11T\xc2')  # 0xa71154c2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.roll))

        data.write(b'\xd2SE\xe8')  # 0xd25345e8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ground_pound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            move=data['move'],
            roll=data['roll'],
            ground_pound=data['ground_pound'],
        )

    def to_json(self) -> dict:
        return {
            'move': self.move,
            'roll': self.roll,
            'ground_pound': self.ground_pound,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xadd734c9, 0xa71154c2, 0xd25345e8)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct269]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(21))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct269(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_roll(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xadd734c9: ('move', _decode_move),
    0xa71154c2: ('roll', _decode_roll),
    0xd25345e8: ('ground_pound', _decode_ground_pound),
}
