# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.Connection import Connection
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class SequenceTimer(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    sequence_connections: list[Connection] = dataclasses.field(default_factory=list)
    start_time: float = dataclasses.field(default=0.0)
    max_time: float = dataclasses.field(default=0.0)
    loop_start_time: float = dataclasses.field(default=0.0)
    is_autostart: bool = dataclasses.field(default=False)
    is_loop: bool = dataclasses.field(default=False)
    take_external_time: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SQTR'

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xef\\\x94\xe9')  # 0xef5c94e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        array = self.sequence_connections
        data.write(struct.pack(">L", len(array)))
        for item in array:
            item.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8\xbd!u')  # 0xb8bd2175
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_time))

        data.write(b'\x03\xe7\xb2\xb4')  # 0x3e7b2b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_time))

        data.write(b'\xac\xf9\xca_')  # 0xacf9ca5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.loop_start_time))

        data.write(b'B\xc6\xe2\xb2')  # 0x42c6e2b2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_autostart))

        data.write(b'\xc0\x8d\x1b\x93')  # 0xc08d1b93
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_loop))

        data.write(b"'\xb3\xb0\x82")  # 0x27b3b082
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.take_external_time))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            sequence_connections=[Connection.from_json(item) for item in data['sequence_connections']],
            start_time=data['start_time'],
            max_time=data['max_time'],
            loop_start_time=data['loop_start_time'],
            is_autostart=data['is_autostart'],
            is_loop=data['is_loop'],
            take_external_time=data['take_external_time'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'sequence_connections': [item.to_json() for item in self.sequence_connections],
            'start_time': self.start_time,
            'max_time': self.max_time,
            'loop_start_time': self.loop_start_time,
            'is_autostart': self.is_autostart,
            'is_loop': self.is_loop,
            'take_external_time': self.take_external_time,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SequenceTimer.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_sequence_connections(data: typing.BinaryIO, property_size: int):
    return [Connection.from_stream(data, property_size) for _ in range(struct.unpack(">L", data.read(4))[0])]


def _decode_start_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_loop_start_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_autostart(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_take_external_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xef5c94e9: ('sequence_connections', _decode_sequence_connections),
    0xb8bd2175: ('start_time', _decode_start_time),
    0x3e7b2b4: ('max_time', _decode_max_time),
    0xacf9ca5f: ('loop_start_time', _decode_loop_start_time),
    0x42c6e2b2: ('is_autostart', _decode_is_autostart),
    0xc08d1b93: ('is_loop', _decode_is_loop),
    0x27b3b082: ('take_external_time', _decode_take_external_time),
}
