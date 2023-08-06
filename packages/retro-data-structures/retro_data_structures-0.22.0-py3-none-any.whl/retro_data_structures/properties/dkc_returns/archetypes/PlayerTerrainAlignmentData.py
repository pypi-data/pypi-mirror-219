# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class PlayerTerrainAlignmentData(BaseProperty):
    use_search_box: bool = dataclasses.field(default=False)
    search_box_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    search_radius: float = dataclasses.field(default=1.0499999523162842)
    search_up_offset: float = dataclasses.field(default=0.20000000298023224)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'(\xfd1\x83')  # 0x28fd3183
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_search_box))

        data.write(b'\xb3\x93\x16Q')  # 0xb3931651
        data.write(b'\x00\x0c')  # size
        self.search_box_size.to_stream(data)

        data.write(b'\xed\x9b\xf5\xa3')  # 0xed9bf5a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_radius))

        data.write(b'y"\r\xd6')  # 0x79220dd6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_up_offset))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            use_search_box=data['use_search_box'],
            search_box_size=Vector.from_json(data['search_box_size']),
            search_radius=data['search_radius'],
            search_up_offset=data['search_up_offset'],
        )

    def to_json(self) -> dict:
        return {
            'use_search_box': self.use_search_box,
            'search_box_size': self.search_box_size.to_json(),
            'search_radius': self.search_radius,
            'search_up_offset': self.search_up_offset,
        }


def _decode_use_search_box(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_search_box_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_search_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_search_up_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x28fd3183: ('use_search_box', _decode_use_search_box),
    0xb3931651: ('search_box_size', _decode_search_box_size),
    0xed9bf5a3: ('search_radius', _decode_search_radius),
    0x79220dd6: ('search_up_offset', _decode_search_up_offset),
}
