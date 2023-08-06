# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.UnknownStruct66 import UnknownStruct66


@dataclasses.dataclass()
class WorldTransitionChoiceRelay(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    num_choices: int = dataclasses.field(default=1)
    unknown_struct66: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0x6bb71e37: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0xfec7caa2: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0xa277e9cb: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0x37073d5e: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0x53e746a0: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0xc6979235: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0xea870072: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0x7ff7d4e7: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)
    unknown_0x7db5008c: UnknownStruct66 = dataclasses.field(default_factory=UnknownStruct66)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'WTCR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptWorldTeleporter.rso']

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
        data.write(b'\x00\x03')  # 3 properties
        num_properties_written = 3

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\xb2\xa4\x9b')  # 0x58b2a49b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_choices))

        data.write(b'\x0fWe\xc9')  # 0xf5765c9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct66.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if self.unknown_0x6bb71e37 != default_override.get('unknown_0x6bb71e37', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'k\xb7\x1e7')  # 0x6bb71e37
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x6bb71e37.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0xfec7caa2 != default_override.get('unknown_0xfec7caa2', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'\xfe\xc7\xca\xa2')  # 0xfec7caa2
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xfec7caa2.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0xa277e9cb != default_override.get('unknown_0xa277e9cb', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'\xa2w\xe9\xcb')  # 0xa277e9cb
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xa277e9cb.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x37073d5e != default_override.get('unknown_0x37073d5e', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'7\x07=^')  # 0x37073d5e
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x37073d5e.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x53e746a0 != default_override.get('unknown_0x53e746a0', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'S\xe7F\xa0')  # 0x53e746a0
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x53e746a0.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0xc6979235 != default_override.get('unknown_0xc6979235', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'\xc6\x97\x925')  # 0xc6979235
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xc6979235.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0xea870072 != default_override.get('unknown_0xea870072', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'\xea\x87\x00r')  # 0xea870072
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xea870072.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x7ff7d4e7 != default_override.get('unknown_0x7ff7d4e7', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'\x7f\xf7\xd4\xe7')  # 0x7ff7d4e7
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x7ff7d4e7.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x7db5008c != default_override.get('unknown_0x7db5008c', UnknownStruct66()):
            num_properties_written += 1
            data.write(b'}\xb5\x00\x8c')  # 0x7db5008c
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x7db5008c.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.write(struct.pack(">H", num_properties_written))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            num_choices=data['num_choices'],
            unknown_struct66=UnknownStruct66.from_json(data['unknown_struct66']),
            unknown_0x6bb71e37=UnknownStruct66.from_json(data['unknown_0x6bb71e37']),
            unknown_0xfec7caa2=UnknownStruct66.from_json(data['unknown_0xfec7caa2']),
            unknown_0xa277e9cb=UnknownStruct66.from_json(data['unknown_0xa277e9cb']),
            unknown_0x37073d5e=UnknownStruct66.from_json(data['unknown_0x37073d5e']),
            unknown_0x53e746a0=UnknownStruct66.from_json(data['unknown_0x53e746a0']),
            unknown_0xc6979235=UnknownStruct66.from_json(data['unknown_0xc6979235']),
            unknown_0xea870072=UnknownStruct66.from_json(data['unknown_0xea870072']),
            unknown_0x7ff7d4e7=UnknownStruct66.from_json(data['unknown_0x7ff7d4e7']),
            unknown_0x7db5008c=UnknownStruct66.from_json(data['unknown_0x7db5008c']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'num_choices': self.num_choices,
            'unknown_struct66': self.unknown_struct66.to_json(),
            'unknown_0x6bb71e37': self.unknown_0x6bb71e37.to_json(),
            'unknown_0xfec7caa2': self.unknown_0xfec7caa2.to_json(),
            'unknown_0xa277e9cb': self.unknown_0xa277e9cb.to_json(),
            'unknown_0x37073d5e': self.unknown_0x37073d5e.to_json(),
            'unknown_0x53e746a0': self.unknown_0x53e746a0.to_json(),
            'unknown_0xc6979235': self.unknown_0xc6979235.to_json(),
            'unknown_0xea870072': self.unknown_0xea870072.to_json(),
            'unknown_0x7ff7d4e7': self.unknown_0x7ff7d4e7.to_json(),
            'unknown_0x7db5008c': self.unknown_0x7db5008c.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_num_choices(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_struct66(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0x6bb71e37(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0xfec7caa2(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0xa277e9cb(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0x37073d5e(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0x53e746a0(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0xc6979235(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0xea870072(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0x7ff7d4e7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


def _decode_unknown_0x7db5008c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct66.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x58b2a49b: ('num_choices', _decode_num_choices),
    0xf5765c9: ('unknown_struct66', _decode_unknown_struct66),
    0x6bb71e37: ('unknown_0x6bb71e37', _decode_unknown_0x6bb71e37),
    0xfec7caa2: ('unknown_0xfec7caa2', _decode_unknown_0xfec7caa2),
    0xa277e9cb: ('unknown_0xa277e9cb', _decode_unknown_0xa277e9cb),
    0x37073d5e: ('unknown_0x37073d5e', _decode_unknown_0x37073d5e),
    0x53e746a0: ('unknown_0x53e746a0', _decode_unknown_0x53e746a0),
    0xc6979235: ('unknown_0xc6979235', _decode_unknown_0xc6979235),
    0xea870072: ('unknown_0xea870072', _decode_unknown_0xea870072),
    0x7ff7d4e7: ('unknown_0x7ff7d4e7', _decode_unknown_0x7ff7d4e7),
    0x7db5008c: ('unknown_0x7db5008c', _decode_unknown_0x7db5008c),
}
