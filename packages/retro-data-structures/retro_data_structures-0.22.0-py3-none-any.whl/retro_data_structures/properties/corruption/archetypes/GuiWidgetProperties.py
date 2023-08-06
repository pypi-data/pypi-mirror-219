# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class GuiWidgetProperties(BaseProperty):
    gui_label: str = dataclasses.field(default='')
    controller_number: int = dataclasses.field(default=1)
    is_locked: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b's\x93\x94\x07')  # 0x73939407
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.gui_label.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdb\x7fJ\xa2')  # 0xdb7f4aa2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.controller_number))

        data.write(b'\xde\xe70\xf5')  # 0xdee730f5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_locked))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_label=data['gui_label'],
            controller_number=data['controller_number'],
            is_locked=data['is_locked'],
        )

    def to_json(self) -> dict:
        return {
            'gui_label': self.gui_label,
            'controller_number': self.controller_number,
            'is_locked': self.is_locked,
        }


def _decode_gui_label(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_controller_number(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_is_locked(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x73939407: ('gui_label', _decode_gui_label),
    0xdb7f4aa2: ('controller_number', _decode_controller_number),
    0xdee730f5: ('is_locked', _decode_is_locked),
}
