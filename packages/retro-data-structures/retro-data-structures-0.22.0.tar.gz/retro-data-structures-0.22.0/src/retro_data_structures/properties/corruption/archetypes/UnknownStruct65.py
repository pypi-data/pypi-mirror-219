# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct65(BaseProperty):
    world: AssetId = dataclasses.field(metadata={'asset_types': ['MLVL']}, default=default_asset_id)
    use_skybox: str = dataclasses.field(default='')

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

        data.write(b'1\xec\x14\xbc')  # 0x31ec14bc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.world))

        data.write(b'\xa9\t\xf8\xd3')  # 0xa909f8d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.use_skybox.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            world=data['world'],
            use_skybox=data['use_skybox'],
        )

    def to_json(self) -> dict:
        return {
            'world': self.world,
            'use_skybox': self.use_skybox,
        }


def _decode_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_use_skybox(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x31ec14bc: ('world', _decode_world),
    0xa909f8d3: ('use_skybox', _decode_use_skybox),
}
