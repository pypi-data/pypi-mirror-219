# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct276(BaseProperty):
    unknown: Spline = dataclasses.field(default_factory=Spline)
    pound_disable_time: float = dataclasses.field(default=5.0)
    launch_delay: float = dataclasses.field(default=4.0)
    target_height: float = dataclasses.field(default=5.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        data.write(b'*\x8f\xd6\xd0')  # 0x2a8fd6d0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xee\x96\x87')  # 0x95ee9687
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pound_disable_time))

        data.write(b'FU\xa9\xc5')  # 0x4655a9c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_delay))

        data.write(b'\xbd\xba\x19\x1e')  # 0xbdba191e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_height))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=Spline.from_json(data['unknown']),
            pound_disable_time=data['pound_disable_time'],
            launch_delay=data['launch_delay'],
            target_height=data['target_height'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown.to_json(),
            'pound_disable_time': self.pound_disable_time,
            'launch_delay': self.launch_delay,
            'target_height': self.target_height,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_pound_disable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2a8fd6d0: ('unknown', _decode_unknown),
    0x95ee9687: ('pound_disable_time', _decode_pound_disable_time),
    0x4655a9c5: ('launch_delay', _decode_launch_delay),
    0xbdba191e: ('target_height', _decode_target_height),
}
