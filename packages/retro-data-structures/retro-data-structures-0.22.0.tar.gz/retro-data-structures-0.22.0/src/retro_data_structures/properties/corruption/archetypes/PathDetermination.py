# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.PathDeterminationMethodType import PathDeterminationMethodType


@dataclasses.dataclass()
class PathDetermination(BaseProperty):
    path_link_type: enums.PathLinkType = dataclasses.field(default=enums.PathLinkType.Unknown3)
    path_determination_method_type: PathDeterminationMethodType = dataclasses.field(default_factory=PathDeterminationMethodType)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'U\x95B\xab')  # 0x559542ab
        data.write(b'\x00\x04')  # size
        self.path_link_type.to_stream(data)

        data.write(b'API\x0c')  # 0x4150490c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path_determination_method_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            path_link_type=enums.PathLinkType.from_json(data['path_link_type']),
            path_determination_method_type=PathDeterminationMethodType.from_json(data['path_determination_method_type']),
        )

    def to_json(self) -> dict:
        return {
            'path_link_type': self.path_link_type.to_json(),
            'path_determination_method_type': self.path_determination_method_type.to_json(),
        }


def _decode_path_link_type(data: typing.BinaryIO, property_size: int):
    return enums.PathLinkType.from_stream(data)


def _decode_path_determination_method_type(data: typing.BinaryIO, property_size: int):
    return PathDeterminationMethodType.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x559542ab: ('path_link_type', _decode_path_link_type),
    0x4150490c: ('path_determination_method_type', _decode_path_determination_method_type),
}
