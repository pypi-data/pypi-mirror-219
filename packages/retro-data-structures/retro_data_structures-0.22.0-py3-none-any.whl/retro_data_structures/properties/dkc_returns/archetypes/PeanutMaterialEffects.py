# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MaterialType import MaterialType
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PeanutMaterialEffects(BaseProperty):
    material: MaterialType = dataclasses.field(default_factory=MaterialType)
    bounce_effect: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    deflection_effect: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xd7.\t\xe1')  # 0xd72e09e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[`!O')  # 0x5b60214f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_effect))

        data.write(b'\xa2r\xad\xe0')  # 0xa272ade0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.deflection_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            material=MaterialType.from_json(data['material']),
            bounce_effect=data['bounce_effect'],
            deflection_effect=data['deflection_effect'],
        )

    def to_json(self) -> dict:
        return {
            'material': self.material.to_json(),
            'bounce_effect': self.bounce_effect,
            'deflection_effect': self.deflection_effect,
        }


def _decode_material(data: typing.BinaryIO, property_size: int):
    return MaterialType.from_stream(data, property_size)


def _decode_bounce_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_deflection_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd72e09e1: ('material', _decode_material),
    0x5b60214f: ('bounce_effect', _decode_bounce_effect),
    0xa272ade0: ('deflection_effect', _decode_deflection_effect),
}
