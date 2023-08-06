# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class MysteryFlyerData(BaseProperty):
    shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    shot_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    hover_speed: float = dataclasses.field(default=10.0)
    hover_height: float = dataclasses.field(default=2.0)
    separation_distance: float = dataclasses.field(default=5.0)
    unknown: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'Q%;\xa3')  # 0x51253ba3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shot_projectile))

        data.write(b'\xce\xa3\x018')  # 0xcea30138
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shot_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84^\xf4\x89')  # 0x845ef489
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_speed))

        data.write(b'\xc7Y\x98\xaa')  # 0xc75998aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_height))

        data.write(b"\x01U\x9f'")  # 0x1559f27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.separation_distance))

        data.write(b'_?\xff\xd6')  # 0x5f3fffd6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            shot_projectile=data['shot_projectile'],
            shot_damage=DamageInfo.from_json(data['shot_damage']),
            hover_speed=data['hover_speed'],
            hover_height=data['hover_height'],
            separation_distance=data['separation_distance'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'shot_projectile': self.shot_projectile,
            'shot_damage': self.shot_damage.to_json(),
            'hover_speed': self.hover_speed,
            'hover_height': self.hover_height,
            'separation_distance': self.separation_distance,
            'unknown': self.unknown,
        }

    def _dependencies_for_shot_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shot_projectile)

    def _dependencies_for_shot_damage(self, asset_manager):
        yield from self.shot_damage.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_shot_projectile, "shot_projectile", "AssetId"),
            (self._dependencies_for_shot_damage, "shot_damage", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for MysteryFlyerData.{field_name} ({field_type}): {e}"
                )


def _decode_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shot_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_hover_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_separation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x51253ba3: ('shot_projectile', _decode_shot_projectile),
    0xcea30138: ('shot_damage', _decode_shot_damage),
    0x845ef489: ('hover_speed', _decode_hover_speed),
    0xc75998aa: ('hover_height', _decode_hover_height),
    0x1559f27: ('separation_distance', _decode_separation_distance),
    0x5f3fffd6: ('unknown', _decode_unknown),
}
