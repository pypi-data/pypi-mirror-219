# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct298(BaseProperty):
    scale_spline: Spline = dataclasses.field(default_factory=Spline)
    auto_start: bool = dataclasses.field(default=True)
    duration: float = dataclasses.field(default=12.0)
    unknown_0x396861d0: float = dataclasses.field(default=12.0)
    max_distance: float = dataclasses.field(default=55.0)
    unknown_0x73bef3cb: int = dataclasses.field(default=4)
    unknown_0xb7074f38: float = dataclasses.field(default=0.0)
    unknown_0x30a1847b: float = dataclasses.field(default=3.0)
    unknown_0x633bdfff: float = dataclasses.field(default=6.0)
    unknown_0xe49d14bc: float = dataclasses.field(default=9.0)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'g"U\xf7')  # 0x672255f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'9ha\xd0')  # 0x396861d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x396861d0))

        data.write(b'%\xb7\xc9\xb2')  # 0x25b7c9b2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_distance))

        data.write(b's\xbe\xf3\xcb')  # 0x73bef3cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x73bef3cb))

        data.write(b'\xb7\x07O8')  # 0xb7074f38
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb7074f38))

        data.write(b'0\xa1\x84{')  # 0x30a1847b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x30a1847b))

        data.write(b'c;\xdf\xff')  # 0x633bdfff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x633bdfff))

        data.write(b'\xe4\x9d\x14\xbc')  # 0xe49d14bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe49d14bc))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scale_spline=Spline.from_json(data['scale_spline']),
            auto_start=data['auto_start'],
            duration=data['duration'],
            unknown_0x396861d0=data['unknown_0x396861d0'],
            max_distance=data['max_distance'],
            unknown_0x73bef3cb=data['unknown_0x73bef3cb'],
            unknown_0xb7074f38=data['unknown_0xb7074f38'],
            unknown_0x30a1847b=data['unknown_0x30a1847b'],
            unknown_0x633bdfff=data['unknown_0x633bdfff'],
            unknown_0xe49d14bc=data['unknown_0xe49d14bc'],
        )

    def to_json(self) -> dict:
        return {
            'scale_spline': self.scale_spline.to_json(),
            'auto_start': self.auto_start,
            'duration': self.duration,
            'unknown_0x396861d0': self.unknown_0x396861d0,
            'max_distance': self.max_distance,
            'unknown_0x73bef3cb': self.unknown_0x73bef3cb,
            'unknown_0xb7074f38': self.unknown_0xb7074f38,
            'unknown_0x30a1847b': self.unknown_0x30a1847b,
            'unknown_0x633bdfff': self.unknown_0x633bdfff,
            'unknown_0xe49d14bc': self.unknown_0xe49d14bc,
        }


def _decode_scale_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x396861d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x73bef3cb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb7074f38(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x30a1847b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x633bdfff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe49d14bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x672255f7: ('scale_spline', _decode_scale_spline),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x8b51e23f: ('duration', _decode_duration),
    0x396861d0: ('unknown_0x396861d0', _decode_unknown_0x396861d0),
    0x25b7c9b2: ('max_distance', _decode_max_distance),
    0x73bef3cb: ('unknown_0x73bef3cb', _decode_unknown_0x73bef3cb),
    0xb7074f38: ('unknown_0xb7074f38', _decode_unknown_0xb7074f38),
    0x30a1847b: ('unknown_0x30a1847b', _decode_unknown_0x30a1847b),
    0x633bdfff: ('unknown_0x633bdfff', _decode_unknown_0x633bdfff),
    0xe49d14bc: ('unknown_0xe49d14bc', _decode_unknown_0xe49d14bc),
}
