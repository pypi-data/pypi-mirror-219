# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class InventoryControls(BaseProperty):
    unknown_0x340f912e: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    menu_up: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    menu_down: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    menu_left: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    menu_right: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    menu_select: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x68ea537d: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'4\x0f\x91.')  # 0x340f912e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x340f912e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\x99\t\xc1')  # 0x769909c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.menu_up.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'M\xabi^')  # 0x4dab695e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.menu_down.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7\xca\xe2\xd3')  # 0xc7cae2d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.menu_left.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x95\xf2v')  # 0x1595f276
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.menu_right.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\t\xb3\x8b')  # 0xbf09b38b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.menu_select.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\xeaS}')  # 0x68ea537d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x68ea537d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x340f912e=RevolutionControl.from_json(data['unknown_0x340f912e']),
            menu_up=RevolutionControl.from_json(data['menu_up']),
            menu_down=RevolutionControl.from_json(data['menu_down']),
            menu_left=RevolutionControl.from_json(data['menu_left']),
            menu_right=RevolutionControl.from_json(data['menu_right']),
            menu_select=RevolutionControl.from_json(data['menu_select']),
            unknown_0x68ea537d=RevolutionControl.from_json(data['unknown_0x68ea537d']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x340f912e': self.unknown_0x340f912e.to_json(),
            'menu_up': self.menu_up.to_json(),
            'menu_down': self.menu_down.to_json(),
            'menu_left': self.menu_left.to_json(),
            'menu_right': self.menu_right.to_json(),
            'menu_select': self.menu_select.to_json(),
            'unknown_0x68ea537d': self.unknown_0x68ea537d.to_json(),
        }


def _decode_unknown_0x340f912e(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_menu_up(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_menu_down(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_menu_left(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_menu_right(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_menu_select(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x68ea537d(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x340f912e: ('unknown_0x340f912e', _decode_unknown_0x340f912e),
    0x769909c1: ('menu_up', _decode_menu_up),
    0x4dab695e: ('menu_down', _decode_menu_down),
    0xc7cae2d3: ('menu_left', _decode_menu_left),
    0x1595f276: ('menu_right', _decode_menu_right),
    0xbf09b38b: ('menu_select', _decode_menu_select),
    0x68ea537d: ('unknown_0x68ea537d', _decode_unknown_0x68ea537d),
}
