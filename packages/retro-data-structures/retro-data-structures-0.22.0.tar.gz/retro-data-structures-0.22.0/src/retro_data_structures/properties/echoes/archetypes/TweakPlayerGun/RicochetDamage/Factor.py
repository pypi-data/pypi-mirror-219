# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Factor(BaseProperty):
    power_beam: float = dataclasses.field(default=0.10000000149011612)
    dark_beam: float = dataclasses.field(default=0.10000000149011612)
    light_beam: float = dataclasses.field(default=0.10000000149011612)
    annihilator_beam: float = dataclasses.field(default=0.10000000149011612)
    phazon_beam: float = dataclasses.field(default=0.10000000149011612)
    missile: float = dataclasses.field(default=0.10000000149011612)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b']b2i')  # 0x5d623269
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.power_beam))

        data.write(b'OB\x01\x91')  # 0x4f420191
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dark_beam))

        data.write(b'{R\x90I')  # 0x7b529049
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.light_beam))

        data.write(b'P=\xdd\xca')  # 0x503dddca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.annihilator_beam))

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
            dark_beam=data['dark_beam'],
            light_beam=data['light_beam'],
            annihilator_beam=data['annihilator_beam'],
            phazon_beam=data['phazon_beam'],
            missile=data['missile'],
        )

    def to_json(self) -> dict:
        return {
            'power_beam': self.power_beam,
            'dark_beam': self.dark_beam,
            'light_beam': self.light_beam,
            'annihilator_beam': self.annihilator_beam,
            'phazon_beam': self.phazon_beam,
            'missile': self.missile,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x5d623269, 0x4f420191, 0x7b529049, 0x503dddca, 0xf668c245, 0x1234cd8)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Factor]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return Factor(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_power_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dark_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_light_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_annihilator_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d623269: ('power_beam', _decode_power_beam),
    0x4f420191: ('dark_beam', _decode_dark_beam),
    0x7b529049: ('light_beam', _decode_light_beam),
    0x503dddca: ('annihilator_beam', _decode_annihilator_beam),
    0xf668c245: ('phazon_beam', _decode_phazon_beam),
    0x1234cd8: ('missile', _decode_missile),
}
