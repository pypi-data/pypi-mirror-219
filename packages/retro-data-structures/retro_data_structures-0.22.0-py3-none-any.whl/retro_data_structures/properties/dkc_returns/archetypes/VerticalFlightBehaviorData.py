# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class VerticalFlightBehaviorData(BaseProperty):
    apex_pause_time: float = dataclasses.field(default=0.0)
    no_actor_collision: bool = dataclasses.field(default=False)

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

        data.write(b'f\x0e\n0')  # 0x660e0a30
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.apex_pause_time))

        data.write(b';\xb9\x9cx')  # 0x3bb99c78
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.no_actor_collision))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            apex_pause_time=data['apex_pause_time'],
            no_actor_collision=data['no_actor_collision'],
        )

    def to_json(self) -> dict:
        return {
            'apex_pause_time': self.apex_pause_time,
            'no_actor_collision': self.no_actor_collision,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x660e0a30, 0x3bb99c78)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[VerticalFlightBehaviorData]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(17))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return VerticalFlightBehaviorData(
        dec[2],
        dec[5],
    )


def _decode_apex_pause_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_no_actor_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x660e0a30: ('apex_pause_time', _decode_apex_pause_time),
    0x3bb99c78: ('no_actor_collision', _decode_no_actor_collision),
}
