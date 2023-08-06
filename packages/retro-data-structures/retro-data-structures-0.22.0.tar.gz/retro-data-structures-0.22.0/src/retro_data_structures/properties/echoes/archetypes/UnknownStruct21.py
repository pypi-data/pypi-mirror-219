# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct21(BaseProperty):
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    projectile_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8f\x8cd\xa0')  # 0x8f8c64a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile_visor_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            projectile_visor_effect=data['projectile_visor_effect'],
        )

    def to_json(self) -> dict:
        return {
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'projectile_visor_effect': self.projectile_visor_effect,
        }

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_projectile_visor_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile_visor_effect)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_projectile_visor_effect, "projectile_visor_effect", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct21.{field_name} ({field_type}): {e}"
                )


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_projectile_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xef485db9: ('projectile', _decode_projectile),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0x8f8c64a0: ('projectile_visor_effect', _decode_projectile_visor_effect),
}
