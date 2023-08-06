# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TDamageInfo import TDamageInfo


@dataclasses.dataclass()
class TWeaponDamage(BaseProperty):
    normal: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    charged: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b"\x8a\xc4'\x8a")  # 0x8ac4278a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal.to_stream(data, default_override={'damage_amount': 50.0, 'radius_damage_amount': 25.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9\xac\x01\xd2')  # 0xc9ac01d2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charged.to_stream(data, default_override={'damage_amount': 50.0, 'radius_damage_amount': 25.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            normal=TDamageInfo.from_json(data['normal']),
            charged=TDamageInfo.from_json(data['charged']),
        )

    def to_json(self) -> dict:
        return {
            'normal': self.normal.to_json(),
            'charged': self.charged.to_json(),
        }

    def _dependencies_for_normal(self, asset_manager):
        yield from self.normal.dependencies_for(asset_manager)

    def _dependencies_for_charged(self, asset_manager):
        yield from self.charged.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_normal, "normal", "TDamageInfo"),
            (self._dependencies_for_charged, "charged", "TDamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TWeaponDamage.{field_name} ({field_type}): {e}"
                )


def _decode_normal(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'damage_amount': 50.0, 'radius_damage_amount': 25.0})


def _decode_charged(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'damage_amount': 50.0, 'radius_damage_amount': 25.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8ac4278a: ('normal', _decode_normal),
    0xc9ac01d2: ('charged', _decode_charged),
}
