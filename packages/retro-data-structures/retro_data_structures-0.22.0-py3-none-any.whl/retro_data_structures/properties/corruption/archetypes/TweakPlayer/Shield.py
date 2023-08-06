# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Shield(BaseProperty):
    max_energy: float = dataclasses.field(default=2.0)
    usage_rate: float = dataclasses.field(default=1.5)
    recharge_rate: float = dataclasses.field(default=0.5)
    allows_motion: bool = dataclasses.field(default=True)

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

        data.write(b'\xd4/\xa1\xc1')  # 0xd42fa1c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_energy))

        data.write(b'xxU\xe6')  # 0x787855e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.usage_rate))

        data.write(b']\xad\xd6\xab')  # 0x5dadd6ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recharge_rate))

        data.write(b'Y\xef\xbb4')  # 0x59efbb34
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allows_motion))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            max_energy=data['max_energy'],
            usage_rate=data['usage_rate'],
            recharge_rate=data['recharge_rate'],
            allows_motion=data['allows_motion'],
        )

    def to_json(self) -> dict:
        return {
            'max_energy': self.max_energy,
            'usage_rate': self.usage_rate,
            'recharge_rate': self.recharge_rate,
            'allows_motion': self.allows_motion,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xd42fa1c1, 0x787855e6, 0x5dadd6ab, 0x59efbb34)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Shield]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(37))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return Shield(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_max_energy(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_usage_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recharge_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allows_motion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd42fa1c1: ('max_energy', _decode_max_energy),
    0x787855e6: ('usage_rate', _decode_usage_rate),
    0x5dadd6ab: ('recharge_rate', _decode_recharge_rate),
    0x59efbb34: ('allows_motion', _decode_allows_motion),
}
