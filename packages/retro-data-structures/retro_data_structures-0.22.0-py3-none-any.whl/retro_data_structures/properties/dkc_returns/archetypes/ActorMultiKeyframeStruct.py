# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class ActorMultiKeyframeStruct(BaseProperty):
    unknown: int = dataclasses.field(default=0)
    loop: bool = dataclasses.field(default=False)
    force_secondary: bool = dataclasses.field(default=False)

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

        data.write(b'\xc2\x15\xa2O')  # 0xc215a24f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'\\\xce[\x97')  # 0x5cce5b97
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_secondary))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            loop=data['loop'],
            force_secondary=data['force_secondary'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'loop': self.loop,
            'force_secondary': self.force_secondary,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xc215a24f, 0xeda47ff6, 0x5cce5b97)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ActorMultiKeyframeStruct]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(24))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return ActorMultiKeyframeStruct(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_force_secondary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc215a24f: ('unknown', _decode_unknown),
    0xeda47ff6: ('loop', _decode_loop),
    0x5cce5b97: ('force_secondary', _decode_force_secondary),
}
