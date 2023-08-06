# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct5(BaseProperty):
    position_percent: float = dataclasses.field(default=0.0)
    texcoord_percent: float = dataclasses.field(default=0.0)
    alpha_percent: float = dataclasses.field(default=0.0)
    color_percent: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'{\xe1N\xe3')  # 0x7be14ee3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.position_percent))

        data.write(b'\xf2\xf3\xf99')  # 0xf2f3f939
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.texcoord_percent))

        data.write(b'N2AX')  # 0x4e324158
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alpha_percent))

        data.write(b'\xdeQ3\x12')  # 0xde513312
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.color_percent))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            position_percent=data['position_percent'],
            texcoord_percent=data['texcoord_percent'],
            alpha_percent=data['alpha_percent'],
            color_percent=data['color_percent'],
        )

    def to_json(self) -> dict:
        return {
            'position_percent': self.position_percent,
            'texcoord_percent': self.texcoord_percent,
            'alpha_percent': self.alpha_percent,
            'color_percent': self.color_percent,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x7be14ee3, 0xf2f3f939, 0x4e324158, 0xde513312)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct5]:
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

    return UnknownStruct5(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_position_percent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_texcoord_percent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alpha_percent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_color_percent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7be14ee3: ('position_percent', _decode_position_percent),
    0xf2f3f939: ('texcoord_percent', _decode_texcoord_percent),
    0x4e324158: ('alpha_percent', _decode_alpha_percent),
    0xde513312: ('color_percent', _decode_color_percent),
}
