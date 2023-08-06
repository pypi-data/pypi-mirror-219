# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class UnknownStruct272(BaseProperty):
    mode: enums.Mode = dataclasses.field(default=enums.Mode.Unknown1)
    progression: int = dataclasses.field(default=0)

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

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        self.mode.to_stream(data)

        data.write(b'\xef\xa9\x04\xbe')  # 0xefa904be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.progression))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mode=enums.Mode.from_json(data['mode']),
            progression=data['progression'],
        )

    def to_json(self) -> dict:
        return {
            'mode': self.mode.to_json(),
            'progression': self.progression,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xb8f60f9a, 0xefa904be)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct272]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct272(
        enums.Mode(dec[2]),
        dec[5],
    )


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return enums.Mode.from_stream(data)


def _decode_progression(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb8f60f9a: ('mode', _decode_mode),
    0xefa904be: ('progression', _decode_progression),
}
