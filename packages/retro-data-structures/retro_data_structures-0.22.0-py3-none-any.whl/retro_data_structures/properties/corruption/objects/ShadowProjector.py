# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.ShadowProjection import ShadowProjection
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class ShadowProjector(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    shadow_scale: float = dataclasses.field(default=1.0)
    shadow_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    shadow_height: float = dataclasses.field(default=100.0)
    shadow_alpha: float = dataclasses.field(default=0.5)
    shadow_fade_time: float = dataclasses.field(default=1.0)
    unknown_0xbca8b742: bool = dataclasses.field(default=False)
    unknown_0x606e341c: int = dataclasses.field(default=128)  # Flagset
    unknown_struct510: ShadowProjection = dataclasses.field(default_factory=ShadowProjection)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SHDW'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\x01\x1a9')  # 0x1d011a39
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_scale))

        data.write(b'\xf3q\xedY')  # 0xf371ed59
        data.write(b'\x00\x0c')  # size
        self.shadow_offset.to_stream(data)

        data.write(b'$\xec\x0f\xb0')  # 0x24ec0fb0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_height))

        data.write(b'>,\xd3\x8d')  # 0x3e2cd38d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_alpha))

        data.write(b'\x8c\xcf6\xc0')  # 0x8ccf36c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_fade_time))

        data.write(b'\xbc\xa8\xb7B')  # 0xbca8b742
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbca8b742))

        data.write(b'`n4\x1c')  # 0x606e341c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x606e341c))

        data.write(b'\xa2\x1bQZ')  # 0xa21b515a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct510.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            shadow_scale=data['shadow_scale'],
            shadow_offset=Vector.from_json(data['shadow_offset']),
            shadow_height=data['shadow_height'],
            shadow_alpha=data['shadow_alpha'],
            shadow_fade_time=data['shadow_fade_time'],
            unknown_0xbca8b742=data['unknown_0xbca8b742'],
            unknown_0x606e341c=data['unknown_0x606e341c'],
            unknown_struct510=ShadowProjection.from_json(data['unknown_struct510']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'shadow_scale': self.shadow_scale,
            'shadow_offset': self.shadow_offset.to_json(),
            'shadow_height': self.shadow_height,
            'shadow_alpha': self.shadow_alpha,
            'shadow_fade_time': self.shadow_fade_time,
            'unknown_0xbca8b742': self.unknown_0xbca8b742,
            'unknown_0x606e341c': self.unknown_0x606e341c,
            'unknown_struct510': self.unknown_struct510.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_shadow_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shadow_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_shadow_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shadow_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shadow_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbca8b742(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x606e341c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_struct510(data: typing.BinaryIO, property_size: int):
    return ShadowProjection.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x1d011a39: ('shadow_scale', _decode_shadow_scale),
    0xf371ed59: ('shadow_offset', _decode_shadow_offset),
    0x24ec0fb0: ('shadow_height', _decode_shadow_height),
    0x3e2cd38d: ('shadow_alpha', _decode_shadow_alpha),
    0x8ccf36c0: ('shadow_fade_time', _decode_shadow_fade_time),
    0xbca8b742: ('unknown_0xbca8b742', _decode_unknown_0xbca8b742),
    0x606e341c: ('unknown_0x606e341c', _decode_unknown_0x606e341c),
    0xa21b515a: ('unknown_struct510', _decode_unknown_struct510),
}
