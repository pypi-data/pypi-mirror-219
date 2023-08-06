# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct96(BaseProperty):
    spawn_as_group: bool = dataclasses.field(default=True)
    unknown: bool = dataclasses.field(default=True)

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

        data.write(b'\x16\x87\x10\xad')  # 0x168710ad
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.spawn_as_group))

        data.write(b'\xbcv\xf3,')  # 0xbc76f32c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            spawn_as_group=data['spawn_as_group'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'spawn_as_group': self.spawn_as_group,
            'unknown': self.unknown,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x168710ad, 0xbc76f32c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct96]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(14))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct96(
        dec[2],
        dec[5],
    )


def _decode_spawn_as_group(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x168710ad: ('spawn_as_group', _decode_spawn_as_group),
    0xbc76f32c: ('unknown', _decode_unknown),
}
