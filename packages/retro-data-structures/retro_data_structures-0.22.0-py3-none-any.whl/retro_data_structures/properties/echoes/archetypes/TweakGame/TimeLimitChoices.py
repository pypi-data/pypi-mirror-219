# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class TimeLimitChoices(BaseProperty):
    time_limit0: float = dataclasses.field(default=0.0)
    time_limit1: float = dataclasses.field(default=3.0)
    time_limit2: float = dataclasses.field(default=5.0)
    time_limit3: float = dataclasses.field(default=10.0)
    time_limit4: float = dataclasses.field(default=20.0)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'w\x9e\x8f\xf4')  # 0x779e8ff4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_limit0))

        data.write(b'\xbc\xc2\\Q')  # 0xbcc25c51
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_limit1))

        data.write(b':V.\xff')  # 0x3a562eff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_limit2))

        data.write(b'\xf1\n\xfdZ')  # 0xf10afd5a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_limit3))

        data.write(b'\xec\x0f\xcd\xe2')  # 0xec0fcde2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_limit4))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            time_limit0=data['time_limit0'],
            time_limit1=data['time_limit1'],
            time_limit2=data['time_limit2'],
            time_limit3=data['time_limit3'],
            time_limit4=data['time_limit4'],
        )

    def to_json(self) -> dict:
        return {
            'time_limit0': self.time_limit0,
            'time_limit1': self.time_limit1,
            'time_limit2': self.time_limit2,
            'time_limit3': self.time_limit3,
            'time_limit4': self.time_limit4,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x779e8ff4, 0xbcc25c51, 0x3a562eff, 0xf10afd5a, 0xec0fcde2)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[TimeLimitChoices]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return TimeLimitChoices(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_time_limit0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_limit1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_limit2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_limit3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_limit4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x779e8ff4: ('time_limit0', _decode_time_limit0),
    0xbcc25c51: ('time_limit1', _decode_time_limit1),
    0x3a562eff: ('time_limit2', _decode_time_limit2),
    0xf10afd5a: ('time_limit3', _decode_time_limit3),
    0xec0fcde2: ('time_limit4', _decode_time_limit4),
}
