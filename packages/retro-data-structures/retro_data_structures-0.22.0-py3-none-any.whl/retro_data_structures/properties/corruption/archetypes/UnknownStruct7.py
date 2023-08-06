# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct7(BaseProperty):
    unknown_0x174a5ec9: float = dataclasses.field(default=35.0)
    unknown_0x87c20643: float = dataclasses.field(default=30.0)
    cutting_beams_chance: float = dataclasses.field(default=35.0)
    ground_spin_chance: float = dataclasses.field(default=0.0)

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

        data.write(b'\x17J^\xc9')  # 0x174a5ec9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x174a5ec9))

        data.write(b'\x87\xc2\x06C')  # 0x87c20643
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x87c20643))

        data.write(b"\xc0'\x1d\xc6")  # 0xc0271dc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cutting_beams_chance))

        data.write(b'/Ld\x1f')  # 0x2f4c641f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_spin_chance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x174a5ec9=data['unknown_0x174a5ec9'],
            unknown_0x87c20643=data['unknown_0x87c20643'],
            cutting_beams_chance=data['cutting_beams_chance'],
            ground_spin_chance=data['ground_spin_chance'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x174a5ec9': self.unknown_0x174a5ec9,
            'unknown_0x87c20643': self.unknown_0x87c20643,
            'cutting_beams_chance': self.cutting_beams_chance,
            'ground_spin_chance': self.ground_spin_chance,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x174a5ec9, 0x87c20643, 0xc0271dc6, 0x2f4c641f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct7]:
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

    return UnknownStruct7(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_unknown_0x174a5ec9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x87c20643(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cutting_beams_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_spin_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x174a5ec9: ('unknown_0x174a5ec9', _decode_unknown_0x174a5ec9),
    0x87c20643: ('unknown_0x87c20643', _decode_unknown_0x87c20643),
    0xc0271dc6: ('cutting_beams_chance', _decode_cutting_beams_chance),
    0x2f4c641f: ('ground_spin_chance', _decode_ground_spin_chance),
}
