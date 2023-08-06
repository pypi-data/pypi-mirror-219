# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class TGunResources(BaseProperty):
    power_beam: str = dataclasses.field(default='')
    ice_beam: str = dataclasses.field(default='')
    wave_beam: str = dataclasses.field(default='')
    plasma_beam: str = dataclasses.field(default='')
    phazon_beam: str = dataclasses.field(default='')

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b"'\x051\x8d")  # 0x2705318d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.power_beam.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xc2\x87\x9f')  # 0x7cc2879f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.ice_beam.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"8'e\xb0")  # 0x382765b0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.wave_beam.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb&\x9a\xc8')  # 0xcb269ac8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.plasma_beam.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\x89\x035')  # 0xa3890335
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.phazon_beam.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            power_beam=data['power_beam'],
            ice_beam=data['ice_beam'],
            wave_beam=data['wave_beam'],
            plasma_beam=data['plasma_beam'],
            phazon_beam=data['phazon_beam'],
        )

    def to_json(self) -> dict:
        return {
            'power_beam': self.power_beam,
            'ice_beam': self.ice_beam,
            'wave_beam': self.wave_beam,
            'plasma_beam': self.plasma_beam,
            'phazon_beam': self.phazon_beam,
        }


def _decode_power_beam(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_ice_beam(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_wave_beam(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_plasma_beam(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_phazon_beam(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2705318d: ('power_beam', _decode_power_beam),
    0x7cc2879f: ('ice_beam', _decode_ice_beam),
    0x382765b0: ('wave_beam', _decode_wave_beam),
    0xcb269ac8: ('plasma_beam', _decode_plasma_beam),
    0xa3890335: ('phazon_beam', _decode_phazon_beam),
}
