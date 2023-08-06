# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Factor(BaseProperty):
    power_beam: float = dataclasses.field(default=0.10000000149011612)
    plasma_beam: float = dataclasses.field(default=0.10000000149011612)
    nova_beam: float = dataclasses.field(default=0.10000000149011612)
    phazon_beam: float = dataclasses.field(default=0.10000000149011612)
    missile: float = dataclasses.field(default=0.10000000149011612)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b']b2i')  # 0x5d623269
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.power_beam))

        data.write(b'\xdb\n\x95\x83')  # 0xdb0a9583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.plasma_beam))

        data.write(b';\xd7W\xe2')  # 0x3bd757e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.nova_beam))

        data.write(b'\xf6h\xc2E')  # 0xf668c245
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_beam))

        data.write(b'\x01#L\xd8')  # 0x1234cd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.missile))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            power_beam=data['power_beam'],
            plasma_beam=data['plasma_beam'],
            nova_beam=data['nova_beam'],
            phazon_beam=data['phazon_beam'],
            missile=data['missile'],
        )

    def to_json(self) -> dict:
        return {
            'power_beam': self.power_beam,
            'plasma_beam': self.plasma_beam,
            'nova_beam': self.nova_beam,
            'phazon_beam': self.phazon_beam,
            'missile': self.missile,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x5d623269, 0xdb0a9583, 0x3bd757e2, 0xf668c245, 0x1234cd8)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Factor]:
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

    return Factor(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_power_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_plasma_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_nova_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d623269: ('power_beam', _decode_power_beam),
    0xdb0a9583: ('plasma_beam', _decode_plasma_beam),
    0x3bd757e2: ('nova_beam', _decode_nova_beam),
    0xf668c245: ('phazon_beam', _decode_phazon_beam),
    0x1234cd8: ('missile', _decode_missile),
}
