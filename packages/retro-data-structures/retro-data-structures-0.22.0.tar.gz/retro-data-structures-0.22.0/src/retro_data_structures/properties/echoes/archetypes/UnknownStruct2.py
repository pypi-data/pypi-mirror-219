# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    enabled: bool = dataclasses.field(default=False)
    chance: float = dataclasses.field(default=0.0)
    modifier: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b")\xc7}'")  # 0x29c77d27
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enabled))

        data.write(b'z{3\x0e')  # 0x7a7b330e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chance))

        data.write(b'\xed-To')  # 0xed2d546f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.modifier))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            enabled=data['enabled'],
            chance=data['chance'],
            modifier=data['modifier'],
        )

    def to_json(self) -> dict:
        return {
            'enabled': self.enabled,
            'chance': self.chance,
            'modifier': self.modifier,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x29c77d27, 0x7a7b330e, 0xed2d546f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct2]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(27))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct2(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x29c77d27: ('enabled', _decode_enabled),
    0x7a7b330e: ('chance', _decode_chance),
    0xed2d546f: ('modifier', _decode_modifier),
}
