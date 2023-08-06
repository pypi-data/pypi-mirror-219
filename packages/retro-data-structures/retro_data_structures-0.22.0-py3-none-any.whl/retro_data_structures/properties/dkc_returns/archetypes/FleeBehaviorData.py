# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class FleeBehaviorData(BaseProperty):
    flee_after_stunned: bool = dataclasses.field(default=False)
    stop_fleeing_at_bounds: bool = dataclasses.field(default=True)
    flee_time: float = dataclasses.field(default=1.0)

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

        data.write(b'|\x1eF[')  # 0x7c1e465b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flee_after_stunned))

        data.write(b'\xdd\x07\x95F')  # 0xdd079546
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stop_fleeing_at_bounds))

        data.write(b'\x8b3\x92b')  # 0x8b339262
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flee_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flee_after_stunned=data['flee_after_stunned'],
            stop_fleeing_at_bounds=data['stop_fleeing_at_bounds'],
            flee_time=data['flee_time'],
        )

    def to_json(self) -> dict:
        return {
            'flee_after_stunned': self.flee_after_stunned,
            'stop_fleeing_at_bounds': self.stop_fleeing_at_bounds,
            'flee_time': self.flee_time,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x7c1e465b, 0xdd079546, 0x8b339262)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FleeBehaviorData]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(24))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return FleeBehaviorData(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_flee_after_stunned(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stop_fleeing_at_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_flee_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7c1e465b: ('flee_after_stunned', _decode_flee_after_stunned),
    0xdd079546: ('stop_fleeing_at_bounds', _decode_stop_fleeing_at_bounds),
    0x8b339262: ('flee_time', _decode_flee_time),
}
