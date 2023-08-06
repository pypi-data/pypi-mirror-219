# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class MetroidPhazeoidStruct(BaseProperty):
    phase_out_radius: float = dataclasses.field(default=0.8999999761581421)
    push_radius: float = dataclasses.field(default=1.100000023841858)
    push_strength: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x83t\x98\xc3')  # 0x837498c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_out_radius))

        data.write(b'\r\xa4\x86F')  # 0xda48646
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.push_radius))

        data.write(b'\xce\x99[/')  # 0xce995b2f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.push_strength))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            phase_out_radius=data['phase_out_radius'],
            push_radius=data['push_radius'],
            push_strength=data['push_strength'],
        )

    def to_json(self) -> dict:
        return {
            'phase_out_radius': self.phase_out_radius,
            'push_radius': self.push_radius,
            'push_strength': self.push_strength,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x837498c3, 0xda48646, 0xce995b2f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[MetroidPhazeoidStruct]:
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

    return MetroidPhazeoidStruct(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_phase_out_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_push_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_push_strength(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x837498c3: ('phase_out_radius', _decode_phase_out_radius),
    0xda48646: ('push_radius', _decode_push_radius),
    0xce995b2f: ('push_strength', _decode_push_strength),
}
