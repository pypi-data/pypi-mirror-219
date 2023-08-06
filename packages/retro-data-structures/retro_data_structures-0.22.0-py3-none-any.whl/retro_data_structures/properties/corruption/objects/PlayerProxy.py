# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class PlayerProxy(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    proxy_type: enums.ProxyType = dataclasses.field(default=enums.ProxyType.Unknown1)
    unknown_0xd62f2d4e: bool = dataclasses.field(default=False)
    unknown_0x0847909f: bool = dataclasses.field(default=False)
    slave_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PLPX'

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
        data.write(b'\x00\x04')  # 4 properties
        num_properties_written = 4

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96T\xaf\x0e')  # 0x9654af0e
        data.write(b'\x00\x04')  # size
        self.proxy_type.to_stream(data)

        data.write(b'\xd6/-N')  # 0xd62f2d4e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd62f2d4e))

        data.write(b'\x08G\x90\x9f')  # 0x847909f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0847909f))

        if self.slave_offset != default_override.get('slave_offset', Vector(x=0.0, y=0.0, z=0.0)):
            num_properties_written += 1
            data.write(b"\x89'\xb1A")  # 0x8927b141
            data.write(b'\x00\x0c')  # size
            self.slave_offset.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.write(struct.pack(">H", num_properties_written))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            proxy_type=enums.ProxyType.from_json(data['proxy_type']),
            unknown_0xd62f2d4e=data['unknown_0xd62f2d4e'],
            unknown_0x0847909f=data['unknown_0x0847909f'],
            slave_offset=Vector.from_json(data['slave_offset']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'proxy_type': self.proxy_type.to_json(),
            'unknown_0xd62f2d4e': self.unknown_0xd62f2d4e,
            'unknown_0x0847909f': self.unknown_0x0847909f,
            'slave_offset': self.slave_offset.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_proxy_type(data: typing.BinaryIO, property_size: int):
    return enums.ProxyType.from_stream(data)


def _decode_unknown_0xd62f2d4e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0847909f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_slave_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x9654af0e: ('proxy_type', _decode_proxy_type),
    0xd62f2d4e: ('unknown_0xd62f2d4e', _decode_unknown_0xd62f2d4e),
    0x847909f: ('unknown_0x0847909f', _decode_unknown_0x0847909f),
    0x8927b141: ('slave_offset', _decode_slave_offset),
}
