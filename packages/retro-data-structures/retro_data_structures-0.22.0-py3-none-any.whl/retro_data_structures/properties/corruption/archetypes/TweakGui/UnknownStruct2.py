# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    unknown_0x771ea34d: float = dataclasses.field(default=0.5)
    unknown_0x8f2e1cf9: float = dataclasses.field(default=0.5)
    unknown_0xf4661f64: float = dataclasses.field(default=0.75)
    zoom_window_width: int = dataclasses.field(default=500)
    zoom_window_height: int = dataclasses.field(default=200)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'w\x1e\xa3M')  # 0x771ea34d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x771ea34d))

        data.write(b'\x8f.\x1c\xf9')  # 0x8f2e1cf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f2e1cf9))

        data.write(b'\xf4f\x1fd')  # 0xf4661f64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf4661f64))

        data.write(b'7+^\x8f')  # 0x372b5e8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.zoom_window_width))

        data.write(b'\xfd\n\xea\xcc')  # 0xfd0aeacc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.zoom_window_height))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x771ea34d=data['unknown_0x771ea34d'],
            unknown_0x8f2e1cf9=data['unknown_0x8f2e1cf9'],
            unknown_0xf4661f64=data['unknown_0xf4661f64'],
            zoom_window_width=data['zoom_window_width'],
            zoom_window_height=data['zoom_window_height'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x771ea34d': self.unknown_0x771ea34d,
            'unknown_0x8f2e1cf9': self.unknown_0x8f2e1cf9,
            'unknown_0xf4661f64': self.unknown_0xf4661f64,
            'zoom_window_width': self.zoom_window_width,
            'zoom_window_height': self.zoom_window_height,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x771ea34d, 0x8f2e1cf9, 0xf4661f64, 0x372b5e8f, 0xfd0aeacc)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct2]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct2(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_unknown_0x771ea34d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f2e1cf9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf4661f64(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_zoom_window_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_zoom_window_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x771ea34d: ('unknown_0x771ea34d', _decode_unknown_0x771ea34d),
    0x8f2e1cf9: ('unknown_0x8f2e1cf9', _decode_unknown_0x8f2e1cf9),
    0xf4661f64: ('unknown_0xf4661f64', _decode_unknown_0xf4661f64),
    0x372b5e8f: ('zoom_window_width', _decode_zoom_window_width),
    0xfd0aeacc: ('zoom_window_height', _decode_zoom_window_height),
}
