# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class TransitionScreen(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    transition_type: enums.TransitionType = dataclasses.field(default=enums.TransitionType.Unknown1)
    unknown_0x5106feb9: bool = dataclasses.field(default=False)
    unknown_0x49469271: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'TRSC'

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

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\xe8iX')  # 0xf5e86958
        data.write(b'\x00\x04')  # size
        self.transition_type.to_stream(data)

        data.write(b'Q\x06\xfe\xb9')  # 0x5106feb9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5106feb9))

        data.write(b'IF\x92q')  # 0x49469271
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x49469271))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            transition_type=enums.TransitionType.from_json(data['transition_type']),
            unknown_0x5106feb9=data['unknown_0x5106feb9'],
            unknown_0x49469271=data['unknown_0x49469271'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'transition_type': self.transition_type.to_json(),
            'unknown_0x5106feb9': self.unknown_0x5106feb9,
            'unknown_0x49469271': self.unknown_0x49469271,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_transition_type(data: typing.BinaryIO, property_size: int):
    return enums.TransitionType.from_stream(data)


def _decode_unknown_0x5106feb9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x49469271(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf5e86958: ('transition_type', _decode_transition_type),
    0x5106feb9: ('unknown_0x5106feb9', _decode_unknown_0x5106feb9),
    0x49469271: ('unknown_0x49469271', _decode_unknown_0x49469271),
}
