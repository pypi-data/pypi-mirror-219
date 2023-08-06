# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class GrappleBeam(BaseProperty):
    travel_speed: float = dataclasses.field(default=30.0)
    x_wave_amplitude: float = dataclasses.field(default=0.25)
    z_wave_amplitude: float = dataclasses.field(default=0.125)
    angle_phase_delta: float = dataclasses.field(default=0.875)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x14\x84\x93g')  # 0x14849367
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.travel_speed))

        data.write(b'lno<')  # 0x6c6e6f3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.x_wave_amplitude))

        data.write(b'\x88\xaanA')  # 0x88aa6e41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.z_wave_amplitude))

        data.write(b'*\xab\x8d\xda')  # 0x2aab8dda
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angle_phase_delta))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            travel_speed=data['travel_speed'],
            x_wave_amplitude=data['x_wave_amplitude'],
            z_wave_amplitude=data['z_wave_amplitude'],
            angle_phase_delta=data['angle_phase_delta'],
        )

    def to_json(self) -> dict:
        return {
            'travel_speed': self.travel_speed,
            'x_wave_amplitude': self.x_wave_amplitude,
            'z_wave_amplitude': self.z_wave_amplitude,
            'angle_phase_delta': self.angle_phase_delta,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x14849367, 0x6c6e6f3c, 0x88aa6e41, 0x2aab8dda)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[GrappleBeam]:
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

    return GrappleBeam(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_travel_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_x_wave_amplitude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_z_wave_amplitude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_angle_phase_delta(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x14849367: ('travel_speed', _decode_travel_speed),
    0x6c6e6f3c: ('x_wave_amplitude', _decode_x_wave_amplitude),
    0x88aa6e41: ('z_wave_amplitude', _decode_z_wave_amplitude),
    0x2aab8dda: ('angle_phase_delta', _decode_angle_phase_delta),
}
