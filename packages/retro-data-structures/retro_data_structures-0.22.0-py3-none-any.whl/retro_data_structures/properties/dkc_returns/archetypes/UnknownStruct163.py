# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct163(BaseProperty):
    initial_duration: float = dataclasses.field(default=0.25)
    show_title_duration: float = dataclasses.field(default=0.25)
    show_buttons_duration: float = dataclasses.field(default=0.25)
    unknown: float = dataclasses.field(default=0.25)

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

        data.write(b'\x08\xe6\xc4/')  # 0x8e6c42f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_duration))

        data.write(b'\xd8J\xc0\xf5')  # 0xd84ac0f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.show_title_duration))

        data.write(b'\x1c\\0;')  # 0x1c5c303b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.show_buttons_duration))

        data.write(b'\xf0\xc5\x1c\x84')  # 0xf0c51c84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_duration=data['initial_duration'],
            show_title_duration=data['show_title_duration'],
            show_buttons_duration=data['show_buttons_duration'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'initial_duration': self.initial_duration,
            'show_title_duration': self.show_title_duration,
            'show_buttons_duration': self.show_buttons_duration,
            'unknown': self.unknown,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8e6c42f, 0xd84ac0f5, 0x1c5c303b, 0xf0c51c84)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct163]:
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

    return UnknownStruct163(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_initial_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_show_title_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_show_buttons_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8e6c42f: ('initial_duration', _decode_initial_duration),
    0xd84ac0f5: ('show_title_duration', _decode_show_title_duration),
    0x1c5c303b: ('show_buttons_duration', _decode_show_buttons_duration),
    0xf0c51c84: ('unknown', _decode_unknown),
}
