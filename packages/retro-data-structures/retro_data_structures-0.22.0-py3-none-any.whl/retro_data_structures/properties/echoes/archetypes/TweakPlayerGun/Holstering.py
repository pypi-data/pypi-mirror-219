# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Holstering(BaseProperty):
    gun_holster_time: float = dataclasses.field(default=0.15000000596046448)
    gun_not_firing_time: float = dataclasses.field(default=30.0)
    gun_holstered_angle: float = dataclasses.field(default=40.0)

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

        data.write(b'~\xe9\x8e\xbb')  # 0x7ee98ebb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_holster_time))

        data.write(b'\xecQ\\\xd5')  # 0xec515cd5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_not_firing_time))

        data.write(b'\x04HW?')  # 0x448573f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_holstered_angle))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gun_holster_time=data['gun_holster_time'],
            gun_not_firing_time=data['gun_not_firing_time'],
            gun_holstered_angle=data['gun_holstered_angle'],
        )

    def to_json(self) -> dict:
        return {
            'gun_holster_time': self.gun_holster_time,
            'gun_not_firing_time': self.gun_not_firing_time,
            'gun_holstered_angle': self.gun_holstered_angle,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x7ee98ebb, 0xec515cd5, 0x448573f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Holstering]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return Holstering(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_gun_holster_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gun_not_firing_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gun_holstered_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7ee98ebb: ('gun_holster_time', _decode_gun_holster_time),
    0xec515cd5: ('gun_not_firing_time', _decode_gun_not_firing_time),
    0x448573f: ('gun_holstered_angle', _decode_gun_holstered_angle),
}
