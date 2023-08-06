# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PuddleControlPhaseData(BaseProperty):
    generation_rate: float = dataclasses.field(default=1.0)
    effect_rate: float = dataclasses.field(default=1.0)
    move_rate: float = dataclasses.field(default=1.0)
    duration: float = dataclasses.field(default=0.0)

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

        data.write(b'#\xe9\x1e\x15')  # 0x23e91e15
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.generation_rate))

        data.write(b'\x82@<\xbd')  # 0x82403cbd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.effect_rate))

        data.write(b'~\xc9\xe6\xd9')  # 0x7ec9e6d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_rate))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            generation_rate=data['generation_rate'],
            effect_rate=data['effect_rate'],
            move_rate=data['move_rate'],
            duration=data['duration'],
        )

    def to_json(self) -> dict:
        return {
            'generation_rate': self.generation_rate,
            'effect_rate': self.effect_rate,
            'move_rate': self.move_rate,
            'duration': self.duration,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x23e91e15, 0x82403cbd, 0x7ec9e6d9, 0x8b51e23f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PuddleControlPhaseData]:
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

    return PuddleControlPhaseData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_generation_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_effect_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x23e91e15: ('generation_rate', _decode_generation_rate),
    0x82403cbd: ('effect_rate', _decode_effect_rate),
    0x7ec9e6d9: ('move_rate', _decode_move_rate),
    0x8b51e23f: ('duration', _decode_duration),
}
