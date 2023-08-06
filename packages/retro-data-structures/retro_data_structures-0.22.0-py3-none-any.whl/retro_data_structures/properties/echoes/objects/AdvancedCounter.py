# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class AdvancedCounter(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    initial_count: int = dataclasses.field(default=0)
    max_count: int = dataclasses.field(default=10)
    auto_reset: bool = dataclasses.field(default=False)
    counter_condition1: int = dataclasses.field(default=1)
    counter_condition2: int = dataclasses.field(default=2)
    counter_condition3: int = dataclasses.field(default=3)
    counter_condition4: int = dataclasses.field(default=4)
    counter_condition5: int = dataclasses.field(default=5)
    counter_condition6: int = dataclasses.field(default=6)
    counter_condition7: int = dataclasses.field(default=7)
    counter_condition8: int = dataclasses.field(default=8)
    counter_condition9: int = dataclasses.field(default=9)
    counter_condition10: int = dataclasses.field(default=10)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ACNT'

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\x17\x9ao')  # 0xfd179a6f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.initial_count))

        data.write(b'[\x85\x15\x89')  # 0x5b851589
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_count))

        data.write(b'{\xefE\xca')  # 0x7bef45ca
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_reset))

        data.write(b'\x16(\xf2:')  # 0x1628f23a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition1))

        data.write(b'\x04\x9d]\xd4')  # 0x49d5dd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition2))

        data.write(b'\xbc!:\xb1')  # 0xbc213ab1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition3))

        data.write(b'!\xf6\x02\x08')  # 0x21f60208
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition4))

        data.write(b'\x99Jem')  # 0x994a656d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition5))

        data.write(b'\x8b\xff\xca\x83')  # 0x8bffca83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition6))

        data.write(b'3C\xad\xe6')  # 0x3343ade6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition7))

        data.write(b'k \xbd\xb0')  # 0x6b20bdb0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition8))

        data.write(b'\xd3\x9c\xda\xd5')  # 0xd39cdad5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition9))

        data.write(b'\x92\x15\xe8\x13')  # 0x9215e813
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.counter_condition10))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            initial_count=data['initial_count'],
            max_count=data['max_count'],
            auto_reset=data['auto_reset'],
            counter_condition1=data['counter_condition1'],
            counter_condition2=data['counter_condition2'],
            counter_condition3=data['counter_condition3'],
            counter_condition4=data['counter_condition4'],
            counter_condition5=data['counter_condition5'],
            counter_condition6=data['counter_condition6'],
            counter_condition7=data['counter_condition7'],
            counter_condition8=data['counter_condition8'],
            counter_condition9=data['counter_condition9'],
            counter_condition10=data['counter_condition10'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'initial_count': self.initial_count,
            'max_count': self.max_count,
            'auto_reset': self.auto_reset,
            'counter_condition1': self.counter_condition1,
            'counter_condition2': self.counter_condition2,
            'counter_condition3': self.counter_condition3,
            'counter_condition4': self.counter_condition4,
            'counter_condition5': self.counter_condition5,
            'counter_condition6': self.counter_condition6,
            'counter_condition7': self.counter_condition7,
            'counter_condition8': self.counter_condition8,
            'counter_condition9': self.counter_condition9,
            'counter_condition10': self.counter_condition10,
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
                    f"Error finding dependencies for AdvancedCounter.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_initial_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_auto_reset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_counter_condition1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_counter_condition10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xfd179a6f: ('initial_count', _decode_initial_count),
    0x5b851589: ('max_count', _decode_max_count),
    0x7bef45ca: ('auto_reset', _decode_auto_reset),
    0x1628f23a: ('counter_condition1', _decode_counter_condition1),
    0x49d5dd4: ('counter_condition2', _decode_counter_condition2),
    0xbc213ab1: ('counter_condition3', _decode_counter_condition3),
    0x21f60208: ('counter_condition4', _decode_counter_condition4),
    0x994a656d: ('counter_condition5', _decode_counter_condition5),
    0x8bffca83: ('counter_condition6', _decode_counter_condition6),
    0x3343ade6: ('counter_condition7', _decode_counter_condition7),
    0x6b20bdb0: ('counter_condition8', _decode_counter_condition8),
    0xd39cdad5: ('counter_condition9', _decode_counter_condition9),
    0x9215e813: ('counter_condition10', _decode_counter_condition10),
}
