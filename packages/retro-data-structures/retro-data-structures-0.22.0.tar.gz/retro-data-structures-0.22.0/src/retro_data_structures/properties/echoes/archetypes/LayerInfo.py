# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class LayerInfo(BaseProperty):
    motion_type: int = dataclasses.field(default=0)
    unknown: float = dataclasses.field(default=0.0)
    rotation: float = dataclasses.field(default=0.0)
    amplitude: float = dataclasses.field(default=-0.0)
    texture_scale: float = dataclasses.field(default=0.0)

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

        data.write(b'\xe9O~\x87')  # 0xe94f7e87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.motion_type))

        data.write(b'<[\x0c\x98')  # 0x3c5b0c98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\x91)T\xe6')  # 0x912954e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation))

        data.write(b'\x89\xe3\xd2\x94')  # 0x89e3d294
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.amplitude))

        data.write(b'\x08\x0ct\x99')  # 0x80c7499
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.texture_scale))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_type=data['motion_type'],
            unknown=data['unknown'],
            rotation=data['rotation'],
            amplitude=data['amplitude'],
            texture_scale=data['texture_scale'],
        )

    def to_json(self) -> dict:
        return {
            'motion_type': self.motion_type,
            'unknown': self.unknown,
            'rotation': self.rotation,
            'amplitude': self.amplitude,
            'texture_scale': self.texture_scale,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xe94f7e87, 0x3c5b0c98, 0x912954e6, 0x89e3d294, 0x80c7499)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[LayerInfo]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return LayerInfo(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_amplitude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_texture_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe94f7e87: ('motion_type', _decode_motion_type),
    0x3c5b0c98: ('unknown', _decode_unknown),
    0x912954e6: ('rotation', _decode_rotation),
    0x89e3d294: ('amplitude', _decode_amplitude),
    0x80c7499: ('texture_scale', _decode_texture_scale),
}
