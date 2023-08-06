# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class CoverPoint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown: int = dataclasses.field(default=1)
    should_crouch: bool = dataclasses.field(default=True)
    horizontal_safe_angle: float = dataclasses.field(default=180.0)
    vertical_safe_angle: float = dataclasses.field(default=90.0)
    lock_time: float = dataclasses.field(default=10.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'COVR'

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96\x9d\xe5\xff')  # 0x969de5ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\x80\x01\xc3\xbe')  # 0x8001c3be
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_crouch))

        data.write(b'FwI\x85')  # 0x46774985
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_safe_angle))

        data.write(b'\xd9\xd7\xaf\xa6')  # 0xd9d7afa6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_safe_angle))

        data.write(b'0\x8e\xdcD')  # 0x308edc44
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_time))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown=data['unknown'],
            should_crouch=data['should_crouch'],
            horizontal_safe_angle=data['horizontal_safe_angle'],
            vertical_safe_angle=data['vertical_safe_angle'],
            lock_time=data['lock_time'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown': self.unknown,
            'should_crouch': self.should_crouch,
            'horizontal_safe_angle': self.horizontal_safe_angle,
            'vertical_safe_angle': self.vertical_safe_angle,
            'lock_time': self.lock_time,
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
                    f"Error finding dependencies for CoverPoint.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_should_crouch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_horizontal_safe_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_safe_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x969de5ff: ('unknown', _decode_unknown),
    0x8001c3be: ('should_crouch', _decode_should_crouch),
    0x46774985: ('horizontal_safe_angle', _decode_horizontal_safe_angle),
    0xd9d7afa6: ('vertical_safe_angle', _decode_vertical_safe_angle),
    0x308edc44: ('lock_time', _decode_lock_time),
}
