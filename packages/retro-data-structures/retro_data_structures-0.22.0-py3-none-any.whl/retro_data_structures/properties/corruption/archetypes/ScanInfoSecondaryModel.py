# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScanInfoSecondaryModel(BaseProperty):
    static_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animated_model: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    model_locator: str = dataclasses.field(default='')

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

        data.write(b'\xb7\xad\xc4\x18')  # 0xb7adc418
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.static_model))

        data.write(b'\xc4\xad\x00\xa7')  # 0xc4ad00a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animated_model.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xa9y\x16')  # 0x24a97916
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.model_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            static_model=data['static_model'],
            animated_model=AnimationParameters.from_json(data['animated_model']),
            model_locator=data['model_locator'],
        )

    def to_json(self) -> dict:
        return {
            'static_model': self.static_model,
            'animated_model': self.animated_model.to_json(),
            'model_locator': self.model_locator,
        }


def _decode_static_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animated_model(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_model_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb7adc418: ('static_model', _decode_static_model),
    0xc4ad00a7: ('animated_model', _decode_animated_model),
    0x24a97916: ('model_locator', _decode_model_locator),
}
