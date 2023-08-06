# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScanInfoSecondaryModel(BaseProperty):
    secondary_static_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    secondary_animated_model: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    secondary_model_locator: str = dataclasses.field(default='')

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\x1fy!\xbc')  # 0x1f7921bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.secondary_static_model))

        data.write(b'\xcd\xd2\x02\xd1')  # 0xcdd202d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_animated_model.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\xa2\xbe\xd8')  # 0x3ea2bed8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.secondary_model_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            secondary_static_model=data['secondary_static_model'],
            secondary_animated_model=AnimationParameters.from_json(data['secondary_animated_model']),
            secondary_model_locator=data['secondary_model_locator'],
        )

    def to_json(self) -> dict:
        return {
            'secondary_static_model': self.secondary_static_model,
            'secondary_animated_model': self.secondary_animated_model.to_json(),
            'secondary_model_locator': self.secondary_model_locator,
        }

    def _dependencies_for_secondary_static_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.secondary_static_model)

    def _dependencies_for_secondary_animated_model(self, asset_manager):
        yield from self.secondary_animated_model.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_secondary_static_model, "secondary_static_model", "AssetId"),
            (self._dependencies_for_secondary_animated_model, "secondary_animated_model", "AnimationParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScanInfoSecondaryModel.{field_name} ({field_type}): {e}"
                )


def _decode_secondary_static_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_secondary_animated_model(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_secondary_model_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1f7921bc: ('secondary_static_model', _decode_secondary_static_model),
    0xcdd202d1: ('secondary_animated_model', _decode_secondary_animated_model),
    0x3ea2bed8: ('secondary_model_locator', _decode_secondary_model_locator),
}
