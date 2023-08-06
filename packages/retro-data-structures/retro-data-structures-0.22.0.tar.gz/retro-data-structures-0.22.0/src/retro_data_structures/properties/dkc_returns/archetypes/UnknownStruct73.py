# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct15 import UnknownStruct15
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct68 import UnknownStruct68
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct71 import UnknownStruct71
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct72 import UnknownStruct72
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct73(BaseProperty):
    camera_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=26.0, y=0.0, z=0.0))
    unknown_struct68: UnknownStruct68 = dataclasses.field(default_factory=UnknownStruct68)
    adjust_vertical_based_on_pullback: bool = dataclasses.field(default=False)
    unknown: bool = dataclasses.field(default=False)
    unknown_struct71: UnknownStruct71 = dataclasses.field(default_factory=UnknownStruct71)
    unknown_struct15: UnknownStruct15 = dataclasses.field(default_factory=UnknownStruct15)
    unknown_struct72: UnknownStruct72 = dataclasses.field(default_factory=UnknownStruct72)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'g\x17\x08\x8c')  # 0x6717088c
        data.write(b'\x00\x0c')  # size
        self.camera_offset.to_stream(data)

        data.write(b'\xd5,\xd4\xfb')  # 0xd52cd4fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct68.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x94z\xa9U')  # 0x947aa955
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_vertical_based_on_pullback))

        data.write(b'\x81x\xa6\x0f')  # 0x8178a60f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b"'\x01w\x1f")  # 0x2701771f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct71.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\xc3\x17\x85')  # 0xc0c31785
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-c\xb0\xf7')  # 0x2d63b0f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct72.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            camera_offset=Vector.from_json(data['camera_offset']),
            unknown_struct68=UnknownStruct68.from_json(data['unknown_struct68']),
            adjust_vertical_based_on_pullback=data['adjust_vertical_based_on_pullback'],
            unknown=data['unknown'],
            unknown_struct71=UnknownStruct71.from_json(data['unknown_struct71']),
            unknown_struct15=UnknownStruct15.from_json(data['unknown_struct15']),
            unknown_struct72=UnknownStruct72.from_json(data['unknown_struct72']),
        )

    def to_json(self) -> dict:
        return {
            'camera_offset': self.camera_offset.to_json(),
            'unknown_struct68': self.unknown_struct68.to_json(),
            'adjust_vertical_based_on_pullback': self.adjust_vertical_based_on_pullback,
            'unknown': self.unknown,
            'unknown_struct71': self.unknown_struct71.to_json(),
            'unknown_struct15': self.unknown_struct15.to_json(),
            'unknown_struct72': self.unknown_struct72.to_json(),
        }


def _decode_camera_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_struct68(data: typing.BinaryIO, property_size: int):
    return UnknownStruct68.from_stream(data, property_size)


def _decode_adjust_vertical_based_on_pullback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct71(data: typing.BinaryIO, property_size: int):
    return UnknownStruct71.from_stream(data, property_size)


def _decode_unknown_struct15(data: typing.BinaryIO, property_size: int):
    return UnknownStruct15.from_stream(data, property_size)


def _decode_unknown_struct72(data: typing.BinaryIO, property_size: int):
    return UnknownStruct72.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6717088c: ('camera_offset', _decode_camera_offset),
    0xd52cd4fb: ('unknown_struct68', _decode_unknown_struct68),
    0x947aa955: ('adjust_vertical_based_on_pullback', _decode_adjust_vertical_based_on_pullback),
    0x8178a60f: ('unknown', _decode_unknown),
    0x2701771f: ('unknown_struct71', _decode_unknown_struct71),
    0xc0c31785: ('unknown_struct15', _decode_unknown_struct15),
    0x2d63b0f7: ('unknown_struct72', _decode_unknown_struct72),
}
