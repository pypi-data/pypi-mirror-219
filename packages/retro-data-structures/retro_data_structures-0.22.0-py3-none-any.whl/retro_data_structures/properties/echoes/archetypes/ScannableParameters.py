# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScannableParameters(BaseProperty):
    scannable_info0: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\xb9N\x9b\xe7')  # 0xb94e9be7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info0))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scannable_info0=data['scannable_info0'],
        )

    def to_json(self) -> dict:
        return {
            'scannable_info0': self.scannable_info0,
        }

    def _dependencies_for_scannable_info0(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info0)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_scannable_info0, "scannable_info0", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScannableParameters.{field_name} ({field_type}): {e}"
                )


_FAST_FORMAT = None
_FAST_IDS = (0xb94e9be7)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ScannableParameters]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(10))
    if (dec[0]) != _FAST_IDS:
        data.seek(before)
        return None

    return ScannableParameters(
        dec[2],
    )


def _decode_scannable_info0(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb94e9be7: ('scannable_info0', _decode_scannable_info0),
}
