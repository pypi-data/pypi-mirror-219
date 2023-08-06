# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Misc(BaseProperty):
    ai_burn_damage: float = dataclasses.field(default=0.25)
    unknown_0x4848f444: float = dataclasses.field(default=5.0)
    max_absorbed_phazon_shots: int = dataclasses.field(default=5)
    unknown_0x3ae5d1fa: float = dataclasses.field(default=0.75)

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

        data.write(b'\xf8\xf9\xbf3')  # 0xf8f9bf33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ai_burn_damage))

        data.write(b'HH\xf4D')  # 0x4848f444
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4848f444))

        data.write(b'\x1eq\x02"')  # 0x1e710222
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_absorbed_phazon_shots))

        data.write(b':\xe5\xd1\xfa')  # 0x3ae5d1fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3ae5d1fa))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ai_burn_damage=data['ai_burn_damage'],
            unknown_0x4848f444=data['unknown_0x4848f444'],
            max_absorbed_phazon_shots=data['max_absorbed_phazon_shots'],
            unknown_0x3ae5d1fa=data['unknown_0x3ae5d1fa'],
        )

    def to_json(self) -> dict:
        return {
            'ai_burn_damage': self.ai_burn_damage,
            'unknown_0x4848f444': self.unknown_0x4848f444,
            'max_absorbed_phazon_shots': self.max_absorbed_phazon_shots,
            'unknown_0x3ae5d1fa': self.unknown_0x3ae5d1fa,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf8f9bf33, 0x4848f444, 0x1e710222, 0x3ae5d1fa)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Misc]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHlLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return Misc(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_ai_burn_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4848f444(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_absorbed_phazon_shots(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3ae5d1fa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8f9bf33: ('ai_burn_damage', _decode_ai_burn_damage),
    0x4848f444: ('unknown_0x4848f444', _decode_unknown_0x4848f444),
    0x1e710222: ('max_absorbed_phazon_shots', _decode_max_absorbed_phazon_shots),
    0x3ae5d1fa: ('unknown_0x3ae5d1fa', _decode_unknown_0x3ae5d1fa),
}
