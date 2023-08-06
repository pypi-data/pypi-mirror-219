# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Frozen(BaseProperty):
    frozen_timer: float = dataclasses.field(default=18.0)
    frozen_jump_counter: int = dataclasses.field(default=4)
    frozen_damage_threshold: float = dataclasses.field(default=20.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xb3\xf2\x05u')  # 0xb3f20575
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.frozen_timer))

        data.write(b'\xb8Q\xd5O')  # 0xb851d54f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frozen_jump_counter))

        data.write(b'3\xb0@\xbf')  # 0x33b040bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.frozen_damage_threshold))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            frozen_timer=data['frozen_timer'],
            frozen_jump_counter=data['frozen_jump_counter'],
            frozen_damage_threshold=data['frozen_damage_threshold'],
        )

    def to_json(self) -> dict:
        return {
            'frozen_timer': self.frozen_timer,
            'frozen_jump_counter': self.frozen_jump_counter,
            'frozen_damage_threshold': self.frozen_damage_threshold,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xb3f20575, 0xb851d54f, 0x33b040bf)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Frozen]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHlLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return Frozen(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_frozen_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_frozen_jump_counter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_frozen_damage_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb3f20575: ('frozen_timer', _decode_frozen_timer),
    0xb851d54f: ('frozen_jump_counter', _decode_frozen_jump_counter),
    0x33b040bf: ('frozen_damage_threshold', _decode_frozen_damage_threshold),
}
