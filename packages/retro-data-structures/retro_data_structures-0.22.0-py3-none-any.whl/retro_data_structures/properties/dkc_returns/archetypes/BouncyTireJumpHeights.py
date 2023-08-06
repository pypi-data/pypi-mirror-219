# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class BouncyTireJumpHeights(BaseProperty):
    min_jump_height: float = dataclasses.field(default=4.640200138092041)
    max_jump_height: float = dataclasses.field(default=7.640200138092041)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'"9\x8aO')  # 0x22398a4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_jump_height))

        data.write(b'q\x9f\x92\xab')  # 0x719f92ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_jump_height))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            min_jump_height=data['min_jump_height'],
            max_jump_height=data['max_jump_height'],
        )

    def to_json(self) -> dict:
        return {
            'min_jump_height': self.min_jump_height,
            'max_jump_height': self.max_jump_height,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x22398a4f, 0x719f92ab)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[BouncyTireJumpHeights]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return BouncyTireJumpHeights(
        dec[2],
        dec[5],
    )


def _decode_min_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x22398a4f: ('min_jump_height', _decode_min_jump_height),
    0x719f92ab: ('max_jump_height', _decode_max_jump_height),
}
