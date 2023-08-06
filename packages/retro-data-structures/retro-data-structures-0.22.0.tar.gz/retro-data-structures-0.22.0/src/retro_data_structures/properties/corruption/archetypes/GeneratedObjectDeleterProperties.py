# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class GeneratedObjectDeleterProperties(BaseProperty):
    delete_all_on_attached_object_deletion: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\xc6\x16J\xff')  # 0xc6164aff
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.delete_all_on_attached_object_deletion))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            delete_all_on_attached_object_deletion=data['delete_all_on_attached_object_deletion'],
        )

    def to_json(self) -> dict:
        return {
            'delete_all_on_attached_object_deletion': self.delete_all_on_attached_object_deletion,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xc6164aff)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[GeneratedObjectDeleterProperties]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(7))
    if (dec[0]) != _FAST_IDS:
        data.seek(before)
        return None

    return GeneratedObjectDeleterProperties(
        dec[2],
    )


def _decode_delete_all_on_attached_object_deletion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc6164aff: ('delete_all_on_attached_object_deletion', _decode_delete_all_on_attached_object_deletion),
}
