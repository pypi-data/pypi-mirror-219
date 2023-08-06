# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class PlayerStateChange(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    item_to_change: int = dataclasses.field(default=0)
    capacity_increase: int = dataclasses.field(default=1)
    amount: int = dataclasses.field(default=1)
    command: int = dataclasses.field(default=0)
    command_action: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PSCH'

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

        data.write(b'J4\x91\xbd')  # 0x4a3491bd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.item_to_change))

        data.write(b'(\xc7\x1bT')  # 0x28c71b54
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.capacity_increase))

        data.write(b'\x94\xaf\x14E')  # 0x94af1445
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.amount))

        data.write(b'\x94\xbaW7')  # 0x94ba5737
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.command))

        data.write(b'6=\x98\xa4')  # 0x363d98a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.command_action))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            item_to_change=data['item_to_change'],
            capacity_increase=data['capacity_increase'],
            amount=data['amount'],
            command=data['command'],
            command_action=data['command_action'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'item_to_change': self.item_to_change,
            'capacity_increase': self.capacity_increase,
            'amount': self.amount,
            'command': self.command,
            'command_action': self.command_action,
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
                    f"Error finding dependencies for PlayerStateChange.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_item_to_change(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_capacity_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_command(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_command_action(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x4a3491bd: ('item_to_change', _decode_item_to_change),
    0x28c71b54: ('capacity_increase', _decode_capacity_increase),
    0x94af1445: ('amount', _decode_amount),
    0x94ba5737: ('command', _decode_command),
    0x363d98a4: ('command_action', _decode_command_action),
}
