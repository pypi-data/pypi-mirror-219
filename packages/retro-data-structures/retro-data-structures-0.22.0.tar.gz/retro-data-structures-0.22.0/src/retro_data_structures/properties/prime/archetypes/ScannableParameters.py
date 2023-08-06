# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScannableParameters(BaseProperty):
    scan_file: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        scan_file = struct.unpack(">L", data.read(4))[0]
        return cls(scan_file)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack(">L", self.scan_file))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_file=data['scan_file'],
        )

    def to_json(self) -> dict:
        return {
            'scan_file': self.scan_file,
        }

    def _dependencies_for_scan_file(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scan_file)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_scan_file, "scan_file", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScannableParameters.{field_name} ({field_type}): {e}"
                )
