# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class FishCloudModifier(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown: bool = dataclasses.field(default=False)
    rotate: bool = dataclasses.field(default=False)
    influence_distance: float = dataclasses.field(default=8.0)
    influence_priority: float = dataclasses.field(default=0.4000000059604645)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FSHM'

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea-L\xa8')  # 0xea2d4ca8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\x921\t\xd6')  # 0x923109d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rotate))

        data.write(b'xd\xad\x0e')  # 0x7864ad0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.influence_distance))

        data.write(b'\xab\xa2\xd9\xed')  # 0xaba2d9ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.influence_priority))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown=data['unknown'],
            rotate=data['rotate'],
            influence_distance=data['influence_distance'],
            influence_priority=data['influence_priority'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown': self.unknown,
            'rotate': self.rotate,
            'influence_distance': self.influence_distance,
            'influence_priority': self.influence_priority,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rotate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_influence_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_influence_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xea2d4ca8: ('unknown', _decode_unknown),
    0x923109d6: ('rotate', _decode_rotate),
    0x7864ad0e: ('influence_distance', _decode_influence_distance),
    0xaba2d9ed: ('influence_priority', _decode_influence_priority),
}
