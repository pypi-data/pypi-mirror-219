# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class CameraFieldOfView(BaseProperty):
    fov_type: int = dataclasses.field(default=2839405128)  # Choice
    unknown_0x69acc94a: int = dataclasses.field(default=0)
    fov_path_object: enums.FOVPathObject = dataclasses.field(default=enums.FOVPathObject.Unknown1)
    desired_fov: float = dataclasses.field(default=60.0)
    unknown_0x972c0e20: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x812cf888: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x19\xea\x15\x1b')  # 0x19ea151b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.fov_type))

        data.write(b'i\xac\xc9J')  # 0x69acc94a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x69acc94a))

        data.write(b'\xd1\xe9\x18\x86')  # 0xd1e91886
        data.write(b'\x00\x04')  # size
        self.fov_path_object.to_stream(data)

        data.write(b'\xca\xfe=\xa7')  # 0xcafe3da7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.desired_fov))

        data.write(b'\x97,\x0e ')  # 0x972c0e20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x972c0e20.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81,\xf8\x88')  # 0x812cf888
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x812cf888.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            fov_type=data['fov_type'],
            unknown_0x69acc94a=data['unknown_0x69acc94a'],
            fov_path_object=enums.FOVPathObject.from_json(data['fov_path_object']),
            desired_fov=data['desired_fov'],
            unknown_0x972c0e20=Spline.from_json(data['unknown_0x972c0e20']),
            unknown_0x812cf888=Spline.from_json(data['unknown_0x812cf888']),
        )

    def to_json(self) -> dict:
        return {
            'fov_type': self.fov_type,
            'unknown_0x69acc94a': self.unknown_0x69acc94a,
            'fov_path_object': self.fov_path_object.to_json(),
            'desired_fov': self.desired_fov,
            'unknown_0x972c0e20': self.unknown_0x972c0e20.to_json(),
            'unknown_0x812cf888': self.unknown_0x812cf888.to_json(),
        }


def _decode_fov_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x69acc94a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_fov_path_object(data: typing.BinaryIO, property_size: int):
    return enums.FOVPathObject.from_stream(data)


def _decode_desired_fov(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x972c0e20(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x812cf888(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x19ea151b: ('fov_type', _decode_fov_type),
    0x69acc94a: ('unknown_0x69acc94a', _decode_unknown_0x69acc94a),
    0xd1e91886: ('fov_path_object', _decode_fov_path_object),
    0xcafe3da7: ('desired_fov', _decode_desired_fov),
    0x972c0e20: ('unknown_0x972c0e20', _decode_unknown_0x972c0e20),
    0x812cf888: ('unknown_0x812cf888', _decode_unknown_0x812cf888),
}
