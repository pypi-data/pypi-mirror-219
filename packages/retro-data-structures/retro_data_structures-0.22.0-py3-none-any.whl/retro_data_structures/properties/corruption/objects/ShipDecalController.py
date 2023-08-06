# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.ShipDecalControllerStruct import ShipDecalControllerStruct


@dataclasses.dataclass()
class ShipDecalController(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    ship_decal_controller_struct_0x15fbdf30: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0x59b4b241: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xb663308d: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0x7640ad4c: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0x9b6ede52: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xea024af3: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xa3b7ee26: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xc7b1dd81: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xd7c6638e: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0x124974e5: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xf8cfa987: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xa77487d5: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)
    ship_decal_controller_struct_0xe590a13e: ShipDecalControllerStruct = dataclasses.field(default_factory=ShipDecalControllerStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPDC'

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

        data.write(b'\x15\xfb\xdf0')  # 0x15fbdf30
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0x15fbdf30.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\xb4\xb2A')  # 0x59b4b241
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0x59b4b241.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6c0\x8d')  # 0xb663308d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xb663308d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v@\xadL')  # 0x7640ad4c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0x7640ad4c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9bn\xdeR')  # 0x9b6ede52
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0x9b6ede52.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea\x02J\xf3')  # 0xea024af3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xea024af3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\xb7\xee&')  # 0xa3b7ee26
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xa3b7ee26.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7\xb1\xdd\x81')  # 0xc7b1dd81
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xc7b1dd81.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7\xc6c\x8e')  # 0xd7c6638e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xd7c6638e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12It\xe5')  # 0x124974e5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0x124974e5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xcf\xa9\x87')  # 0xf8cfa987
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xf8cfa987.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7t\x87\xd5')  # 0xa77487d5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xa77487d5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x90\xa1>')  # 0xe590a13e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_decal_controller_struct_0xe590a13e.to_stream(data)
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
            ship_decal_controller_struct_0x15fbdf30=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0x15fbdf30']),
            ship_decal_controller_struct_0x59b4b241=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0x59b4b241']),
            ship_decal_controller_struct_0xb663308d=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xb663308d']),
            ship_decal_controller_struct_0x7640ad4c=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0x7640ad4c']),
            ship_decal_controller_struct_0x9b6ede52=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0x9b6ede52']),
            ship_decal_controller_struct_0xea024af3=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xea024af3']),
            ship_decal_controller_struct_0xa3b7ee26=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xa3b7ee26']),
            ship_decal_controller_struct_0xc7b1dd81=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xc7b1dd81']),
            ship_decal_controller_struct_0xd7c6638e=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xd7c6638e']),
            ship_decal_controller_struct_0x124974e5=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0x124974e5']),
            ship_decal_controller_struct_0xf8cfa987=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xf8cfa987']),
            ship_decal_controller_struct_0xa77487d5=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xa77487d5']),
            ship_decal_controller_struct_0xe590a13e=ShipDecalControllerStruct.from_json(data['ship_decal_controller_struct_0xe590a13e']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'ship_decal_controller_struct_0x15fbdf30': self.ship_decal_controller_struct_0x15fbdf30.to_json(),
            'ship_decal_controller_struct_0x59b4b241': self.ship_decal_controller_struct_0x59b4b241.to_json(),
            'ship_decal_controller_struct_0xb663308d': self.ship_decal_controller_struct_0xb663308d.to_json(),
            'ship_decal_controller_struct_0x7640ad4c': self.ship_decal_controller_struct_0x7640ad4c.to_json(),
            'ship_decal_controller_struct_0x9b6ede52': self.ship_decal_controller_struct_0x9b6ede52.to_json(),
            'ship_decal_controller_struct_0xea024af3': self.ship_decal_controller_struct_0xea024af3.to_json(),
            'ship_decal_controller_struct_0xa3b7ee26': self.ship_decal_controller_struct_0xa3b7ee26.to_json(),
            'ship_decal_controller_struct_0xc7b1dd81': self.ship_decal_controller_struct_0xc7b1dd81.to_json(),
            'ship_decal_controller_struct_0xd7c6638e': self.ship_decal_controller_struct_0xd7c6638e.to_json(),
            'ship_decal_controller_struct_0x124974e5': self.ship_decal_controller_struct_0x124974e5.to_json(),
            'ship_decal_controller_struct_0xf8cfa987': self.ship_decal_controller_struct_0xf8cfa987.to_json(),
            'ship_decal_controller_struct_0xa77487d5': self.ship_decal_controller_struct_0xa77487d5.to_json(),
            'ship_decal_controller_struct_0xe590a13e': self.ship_decal_controller_struct_0xe590a13e.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0x15fbdf30(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0x59b4b241(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xb663308d(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0x7640ad4c(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0x9b6ede52(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xea024af3(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xa3b7ee26(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xc7b1dd81(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xd7c6638e(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0x124974e5(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xf8cfa987(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xa77487d5(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


def _decode_ship_decal_controller_struct_0xe590a13e(data: typing.BinaryIO, property_size: int):
    return ShipDecalControllerStruct.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x15fbdf30: ('ship_decal_controller_struct_0x15fbdf30', _decode_ship_decal_controller_struct_0x15fbdf30),
    0x59b4b241: ('ship_decal_controller_struct_0x59b4b241', _decode_ship_decal_controller_struct_0x59b4b241),
    0xb663308d: ('ship_decal_controller_struct_0xb663308d', _decode_ship_decal_controller_struct_0xb663308d),
    0x7640ad4c: ('ship_decal_controller_struct_0x7640ad4c', _decode_ship_decal_controller_struct_0x7640ad4c),
    0x9b6ede52: ('ship_decal_controller_struct_0x9b6ede52', _decode_ship_decal_controller_struct_0x9b6ede52),
    0xea024af3: ('ship_decal_controller_struct_0xea024af3', _decode_ship_decal_controller_struct_0xea024af3),
    0xa3b7ee26: ('ship_decal_controller_struct_0xa3b7ee26', _decode_ship_decal_controller_struct_0xa3b7ee26),
    0xc7b1dd81: ('ship_decal_controller_struct_0xc7b1dd81', _decode_ship_decal_controller_struct_0xc7b1dd81),
    0xd7c6638e: ('ship_decal_controller_struct_0xd7c6638e', _decode_ship_decal_controller_struct_0xd7c6638e),
    0x124974e5: ('ship_decal_controller_struct_0x124974e5', _decode_ship_decal_controller_struct_0x124974e5),
    0xf8cfa987: ('ship_decal_controller_struct_0xf8cfa987', _decode_ship_decal_controller_struct_0xf8cfa987),
    0xa77487d5: ('ship_decal_controller_struct_0xa77487d5', _decode_ship_decal_controller_struct_0xa77487d5),
    0xe590a13e: ('ship_decal_controller_struct_0xe590a13e', _decode_ship_decal_controller_struct_0xe590a13e),
}
