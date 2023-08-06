# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class TranslationSplines(BaseProperty):
    x_translation: Spline = dataclasses.field(default_factory=Spline)
    y_translation: Spline = dataclasses.field(default_factory=Spline)
    z_translation: Spline = dataclasses.field(default_factory=Spline)

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

        data.write(b'$\xe9\xa0\x9b')  # 0x24e9a09b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_translation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb\xbb\x16z')  # 0xcbbb167a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_translation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!=\xcb\x18')  # 0x213dcb18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_translation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            x_translation=Spline.from_json(data['x_translation']),
            y_translation=Spline.from_json(data['y_translation']),
            z_translation=Spline.from_json(data['z_translation']),
        )

    def to_json(self) -> dict:
        return {
            'x_translation': self.x_translation.to_json(),
            'y_translation': self.y_translation.to_json(),
            'z_translation': self.z_translation.to_json(),
        }


def _decode_x_translation(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_y_translation(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_z_translation(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x24e9a09b: ('x_translation', _decode_x_translation),
    0xcbbb167a: ('y_translation', _decode_y_translation),
    0x213dcb18: ('z_translation', _decode_z_translation),
}
