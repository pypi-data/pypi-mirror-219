# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.UnknownStruct65 import UnknownStruct65


@dataclasses.dataclass()
class WorldTeleporterAttributes(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct65: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xfae81682: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x5f63868c: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x91337a24: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x34b8ea2a: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x01555c79: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xa4decc77: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x4685a368: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xe30e3366: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xee37cd3c: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x4bbc5d32: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x7e51eb61: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xdbda7b6f: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x158a87c7: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xb00117c9: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x85eca19a: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x20673194: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0xc23c5e8b: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x67b7ce85: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)
    unknown_0x1c6020c4: UnknownStruct65 = dataclasses.field(default_factory=UnknownStruct65)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'WTAT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptWorldTeleporterAttributes.rso']

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
        data.write(b'\x00\x0f')  # 15 properties
        num_properties_written = 15

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\x05\xa0\xd1')  # 0xcf05a0d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct65.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xe8\x16\x82')  # 0xfae81682
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xfae81682.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_c\x86\x8c')  # 0x5f63868c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x5f63868c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x913z$')  # 0x91337a24
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x91337a24.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'4\xb8\xea*')  # 0x34b8ea2a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x34b8ea2a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01U\\y')  # 0x1555c79
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x01555c79.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xde\xccw')  # 0xa4decc77
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa4decc77.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\x85\xa3h')  # 0x4685a368
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x4685a368.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x0e3f')  # 0xe30e3366
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xe30e3366.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee7\xcd<')  # 0xee37cd3c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xee37cd3c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'K\xbc]2')  # 0x4bbc5d32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x4bbc5d32.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~Q\xeba')  # 0x7e51eb61
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7e51eb61.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdb\xda{o')  # 0xdbda7b6f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xdbda7b6f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x8a\x87\xc7')  # 0x158a87c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x158a87c7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if self.unknown_0xb00117c9 != default_override.get('unknown_0xb00117c9', UnknownStruct65()):
            num_properties_written += 1
            data.write(b'\xb0\x01\x17\xc9')  # 0xb00117c9
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xb00117c9.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x85eca19a != default_override.get('unknown_0x85eca19a', UnknownStruct65()):
            num_properties_written += 1
            data.write(b'\x85\xec\xa1\x9a')  # 0x85eca19a
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x85eca19a.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x20673194 != default_override.get('unknown_0x20673194', UnknownStruct65()):
            num_properties_written += 1
            data.write(b' g1\x94')  # 0x20673194
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x20673194.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0xc23c5e8b != default_override.get('unknown_0xc23c5e8b', UnknownStruct65()):
            num_properties_written += 1
            data.write(b'\xc2<^\x8b')  # 0xc23c5e8b
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0xc23c5e8b.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x67b7ce85 != default_override.get('unknown_0x67b7ce85', UnknownStruct65()):
            num_properties_written += 1
            data.write(b'g\xb7\xce\x85')  # 0x67b7ce85
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x67b7ce85.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.unknown_0x1c6020c4 != default_override.get('unknown_0x1c6020c4', UnknownStruct65()):
            num_properties_written += 1
            data.write(b'\x1c` \xc4')  # 0x1c6020c4
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_0x1c6020c4.to_stream(data)
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
            unknown_struct65=UnknownStruct65.from_json(data['unknown_struct65']),
            unknown_0xfae81682=UnknownStruct65.from_json(data['unknown_0xfae81682']),
            unknown_0x5f63868c=UnknownStruct65.from_json(data['unknown_0x5f63868c']),
            unknown_0x91337a24=UnknownStruct65.from_json(data['unknown_0x91337a24']),
            unknown_0x34b8ea2a=UnknownStruct65.from_json(data['unknown_0x34b8ea2a']),
            unknown_0x01555c79=UnknownStruct65.from_json(data['unknown_0x01555c79']),
            unknown_0xa4decc77=UnknownStruct65.from_json(data['unknown_0xa4decc77']),
            unknown_0x4685a368=UnknownStruct65.from_json(data['unknown_0x4685a368']),
            unknown_0xe30e3366=UnknownStruct65.from_json(data['unknown_0xe30e3366']),
            unknown_0xee37cd3c=UnknownStruct65.from_json(data['unknown_0xee37cd3c']),
            unknown_0x4bbc5d32=UnknownStruct65.from_json(data['unknown_0x4bbc5d32']),
            unknown_0x7e51eb61=UnknownStruct65.from_json(data['unknown_0x7e51eb61']),
            unknown_0xdbda7b6f=UnknownStruct65.from_json(data['unknown_0xdbda7b6f']),
            unknown_0x158a87c7=UnknownStruct65.from_json(data['unknown_0x158a87c7']),
            unknown_0xb00117c9=UnknownStruct65.from_json(data['unknown_0xb00117c9']),
            unknown_0x85eca19a=UnknownStruct65.from_json(data['unknown_0x85eca19a']),
            unknown_0x20673194=UnknownStruct65.from_json(data['unknown_0x20673194']),
            unknown_0xc23c5e8b=UnknownStruct65.from_json(data['unknown_0xc23c5e8b']),
            unknown_0x67b7ce85=UnknownStruct65.from_json(data['unknown_0x67b7ce85']),
            unknown_0x1c6020c4=UnknownStruct65.from_json(data['unknown_0x1c6020c4']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct65': self.unknown_struct65.to_json(),
            'unknown_0xfae81682': self.unknown_0xfae81682.to_json(),
            'unknown_0x5f63868c': self.unknown_0x5f63868c.to_json(),
            'unknown_0x91337a24': self.unknown_0x91337a24.to_json(),
            'unknown_0x34b8ea2a': self.unknown_0x34b8ea2a.to_json(),
            'unknown_0x01555c79': self.unknown_0x01555c79.to_json(),
            'unknown_0xa4decc77': self.unknown_0xa4decc77.to_json(),
            'unknown_0x4685a368': self.unknown_0x4685a368.to_json(),
            'unknown_0xe30e3366': self.unknown_0xe30e3366.to_json(),
            'unknown_0xee37cd3c': self.unknown_0xee37cd3c.to_json(),
            'unknown_0x4bbc5d32': self.unknown_0x4bbc5d32.to_json(),
            'unknown_0x7e51eb61': self.unknown_0x7e51eb61.to_json(),
            'unknown_0xdbda7b6f': self.unknown_0xdbda7b6f.to_json(),
            'unknown_0x158a87c7': self.unknown_0x158a87c7.to_json(),
            'unknown_0xb00117c9': self.unknown_0xb00117c9.to_json(),
            'unknown_0x85eca19a': self.unknown_0x85eca19a.to_json(),
            'unknown_0x20673194': self.unknown_0x20673194.to_json(),
            'unknown_0xc23c5e8b': self.unknown_0xc23c5e8b.to_json(),
            'unknown_0x67b7ce85': self.unknown_0x67b7ce85.to_json(),
            'unknown_0x1c6020c4': self.unknown_0x1c6020c4.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_struct65(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xfae81682(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x5f63868c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x91337a24(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x34b8ea2a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x01555c79(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xa4decc77(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x4685a368(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xe30e3366(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xee37cd3c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x4bbc5d32(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x7e51eb61(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xdbda7b6f(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x158a87c7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xb00117c9(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x85eca19a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x20673194(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0xc23c5e8b(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x67b7ce85(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


def _decode_unknown_0x1c6020c4(data: typing.BinaryIO, property_size: int):
    return UnknownStruct65.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xcf05a0d1: ('unknown_struct65', _decode_unknown_struct65),
    0xfae81682: ('unknown_0xfae81682', _decode_unknown_0xfae81682),
    0x5f63868c: ('unknown_0x5f63868c', _decode_unknown_0x5f63868c),
    0x91337a24: ('unknown_0x91337a24', _decode_unknown_0x91337a24),
    0x34b8ea2a: ('unknown_0x34b8ea2a', _decode_unknown_0x34b8ea2a),
    0x1555c79: ('unknown_0x01555c79', _decode_unknown_0x01555c79),
    0xa4decc77: ('unknown_0xa4decc77', _decode_unknown_0xa4decc77),
    0x4685a368: ('unknown_0x4685a368', _decode_unknown_0x4685a368),
    0xe30e3366: ('unknown_0xe30e3366', _decode_unknown_0xe30e3366),
    0xee37cd3c: ('unknown_0xee37cd3c', _decode_unknown_0xee37cd3c),
    0x4bbc5d32: ('unknown_0x4bbc5d32', _decode_unknown_0x4bbc5d32),
    0x7e51eb61: ('unknown_0x7e51eb61', _decode_unknown_0x7e51eb61),
    0xdbda7b6f: ('unknown_0xdbda7b6f', _decode_unknown_0xdbda7b6f),
    0x158a87c7: ('unknown_0x158a87c7', _decode_unknown_0x158a87c7),
    0xb00117c9: ('unknown_0xb00117c9', _decode_unknown_0xb00117c9),
    0x85eca19a: ('unknown_0x85eca19a', _decode_unknown_0x85eca19a),
    0x20673194: ('unknown_0x20673194', _decode_unknown_0x20673194),
    0xc23c5e8b: ('unknown_0xc23c5e8b', _decode_unknown_0xc23c5e8b),
    0x67b7ce85: ('unknown_0x67b7ce85', _decode_unknown_0x67b7ce85),
    0x1c6020c4: ('unknown_0x1c6020c4', _decode_unknown_0x1c6020c4),
}
