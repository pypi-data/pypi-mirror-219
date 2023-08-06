# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class FirstPersonCamera(BaseProperty):
    unknown_0xba5eb7f5: float = dataclasses.field(default=60.0)
    camera_elevation: float = dataclasses.field(default=0.0)
    unknown_0xb400ebd6: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xfd26b7b9: float = dataclasses.field(default=4.0)
    unknown_0x97b14dc6: float = dataclasses.field(default=73.0)
    unknown_0xeb59925a: float = dataclasses.field(default=0.30000001192092896)
    unknown_0xa1d73380: float = dataclasses.field(default=4.0)
    unknown_0xc8e8344a: float = dataclasses.field(default=73.0)
    unknown_0xd40c480e: float = dataclasses.field(default=10.0)
    unknown_0x7960c3a0: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xba^\xb7\xf5')  # 0xba5eb7f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xba5eb7f5))

        data.write(b'\rA\xe3\xba')  # 0xd41e3ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_elevation))

        data.write(b'\xb4\x00\xeb\xd6')  # 0xb400ebd6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb400ebd6))

        data.write(b'\xfd&\xb7\xb9')  # 0xfd26b7b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfd26b7b9))

        data.write(b'\x97\xb1M\xc6')  # 0x97b14dc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x97b14dc6))

        data.write(b'\xebY\x92Z')  # 0xeb59925a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xeb59925a))

        data.write(b'\xa1\xd73\x80')  # 0xa1d73380
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa1d73380))

        data.write(b'\xc8\xe84J')  # 0xc8e8344a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc8e8344a))

        data.write(b'\xd4\x0cH\x0e')  # 0xd40c480e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd40c480e))

        data.write(b'y`\xc3\xa0')  # 0x7960c3a0
        data.write(b'\x00\x0c')  # size
        self.unknown_0x7960c3a0.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xba5eb7f5=data['unknown_0xba5eb7f5'],
            camera_elevation=data['camera_elevation'],
            unknown_0xb400ebd6=data['unknown_0xb400ebd6'],
            unknown_0xfd26b7b9=data['unknown_0xfd26b7b9'],
            unknown_0x97b14dc6=data['unknown_0x97b14dc6'],
            unknown_0xeb59925a=data['unknown_0xeb59925a'],
            unknown_0xa1d73380=data['unknown_0xa1d73380'],
            unknown_0xc8e8344a=data['unknown_0xc8e8344a'],
            unknown_0xd40c480e=data['unknown_0xd40c480e'],
            unknown_0x7960c3a0=Vector.from_json(data['unknown_0x7960c3a0']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xba5eb7f5': self.unknown_0xba5eb7f5,
            'camera_elevation': self.camera_elevation,
            'unknown_0xb400ebd6': self.unknown_0xb400ebd6,
            'unknown_0xfd26b7b9': self.unknown_0xfd26b7b9,
            'unknown_0x97b14dc6': self.unknown_0x97b14dc6,
            'unknown_0xeb59925a': self.unknown_0xeb59925a,
            'unknown_0xa1d73380': self.unknown_0xa1d73380,
            'unknown_0xc8e8344a': self.unknown_0xc8e8344a,
            'unknown_0xd40c480e': self.unknown_0xd40c480e,
            'unknown_0x7960c3a0': self.unknown_0x7960c3a0.to_json(),
        }


def _decode_unknown_0xba5eb7f5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb400ebd6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfd26b7b9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x97b14dc6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xeb59925a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa1d73380(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc8e8344a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd40c480e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7960c3a0(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xba5eb7f5: ('unknown_0xba5eb7f5', _decode_unknown_0xba5eb7f5),
    0xd41e3ba: ('camera_elevation', _decode_camera_elevation),
    0xb400ebd6: ('unknown_0xb400ebd6', _decode_unknown_0xb400ebd6),
    0xfd26b7b9: ('unknown_0xfd26b7b9', _decode_unknown_0xfd26b7b9),
    0x97b14dc6: ('unknown_0x97b14dc6', _decode_unknown_0x97b14dc6),
    0xeb59925a: ('unknown_0xeb59925a', _decode_unknown_0xeb59925a),
    0xa1d73380: ('unknown_0xa1d73380', _decode_unknown_0xa1d73380),
    0xc8e8344a: ('unknown_0xc8e8344a', _decode_unknown_0xc8e8344a),
    0xd40c480e: ('unknown_0xd40c480e', _decode_unknown_0xd40c480e),
    0x7960c3a0: ('unknown_0x7960c3a0', _decode_unknown_0x7960c3a0),
}
