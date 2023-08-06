# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.TriggerShape import TriggerShape
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class GroundPoundDetectorData(BaseProperty):
    use_detection_shape_and_ignore_radius: bool = dataclasses.field(default=False)
    trigger_shape: TriggerShape = dataclasses.field(default_factory=TriggerShape)
    detection_vector: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    detection_angle_tolerance: float = dataclasses.field(default=5.0)
    radius: float = dataclasses.field(default=5.0)
    ignore_dk: bool = dataclasses.field(default=False)
    ignore_diddy: bool = dataclasses.field(default=False)
    ignore_rambi: bool = dataclasses.field(default=False)
    use_originator_transform: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xf2\x9d\xb9X')  # 0xf29db958
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_detection_shape_and_ignore_radius))

        data.write(b'\xbb,T\xe1')  # 0xbb2c54e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.trigger_shape.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'E\xa4m\x11')  # 0x45a46d11
        data.write(b'\x00\x0c')  # size
        self.detection_vector.to_stream(data)

        data.write(b'\xbaH\xe8S')  # 0xba48e853
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_angle_tolerance))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'%\xee_\xfb')  # 0x25ee5ffb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_dk))

        data.write(b'b\xa7\x13c')  # 0x62a71363
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_diddy))

        data.write(b'M\xb9\x02a')  # 0x4db90261
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_rambi))

        data.write(b'\x03Z^\x10')  # 0x35a5e10
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_originator_transform))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            use_detection_shape_and_ignore_radius=data['use_detection_shape_and_ignore_radius'],
            trigger_shape=TriggerShape.from_json(data['trigger_shape']),
            detection_vector=Vector.from_json(data['detection_vector']),
            detection_angle_tolerance=data['detection_angle_tolerance'],
            radius=data['radius'],
            ignore_dk=data['ignore_dk'],
            ignore_diddy=data['ignore_diddy'],
            ignore_rambi=data['ignore_rambi'],
            use_originator_transform=data['use_originator_transform'],
        )

    def to_json(self) -> dict:
        return {
            'use_detection_shape_and_ignore_radius': self.use_detection_shape_and_ignore_radius,
            'trigger_shape': self.trigger_shape.to_json(),
            'detection_vector': self.detection_vector.to_json(),
            'detection_angle_tolerance': self.detection_angle_tolerance,
            'radius': self.radius,
            'ignore_dk': self.ignore_dk,
            'ignore_diddy': self.ignore_diddy,
            'ignore_rambi': self.ignore_rambi,
            'use_originator_transform': self.use_originator_transform,
        }


def _decode_use_detection_shape_and_ignore_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_trigger_shape(data: typing.BinaryIO, property_size: int):
    return TriggerShape.from_stream(data, property_size)


def _decode_detection_vector(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_detection_angle_tolerance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_dk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_diddy(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_originator_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf29db958: ('use_detection_shape_and_ignore_radius', _decode_use_detection_shape_and_ignore_radius),
    0xbb2c54e1: ('trigger_shape', _decode_trigger_shape),
    0x45a46d11: ('detection_vector', _decode_detection_vector),
    0xba48e853: ('detection_angle_tolerance', _decode_detection_angle_tolerance),
    0x78c507eb: ('radius', _decode_radius),
    0x25ee5ffb: ('ignore_dk', _decode_ignore_dk),
    0x62a71363: ('ignore_diddy', _decode_ignore_diddy),
    0x4db90261: ('ignore_rambi', _decode_ignore_rambi),
    0x35a5e10: ('use_originator_transform', _decode_use_originator_transform),
}
