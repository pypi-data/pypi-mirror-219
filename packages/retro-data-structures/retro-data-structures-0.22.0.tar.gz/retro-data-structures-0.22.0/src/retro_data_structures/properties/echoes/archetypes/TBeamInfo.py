# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TWeaponDamage import TWeaponDamage


@dataclasses.dataclass()
class TBeamInfo(BaseProperty):
    cooldown: float = dataclasses.field(default=0.20000000298023224)
    damage_info: TWeaponDamage = dataclasses.field(default_factory=TWeaponDamage)

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

        data.write(b'\x10.\x08_')  # 0x102e085f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cooldown))

        data.write(b'\xfa\xa7\x1e%')  # 0xfaa71e25
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cooldown=data['cooldown'],
            damage_info=TWeaponDamage.from_json(data['damage_info']),
        )

    def to_json(self) -> dict:
        return {
            'cooldown': self.cooldown,
            'damage_info': self.damage_info.to_json(),
        }

    def _dependencies_for_damage_info(self, asset_manager):
        yield from self.damage_info.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_damage_info, "damage_info", "TWeaponDamage"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TBeamInfo.{field_name} ({field_type}): {e}"
                )


def _decode_cooldown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return TWeaponDamage.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x102e085f: ('cooldown', _decode_cooldown),
    0xfaa71e25: ('damage_info', _decode_damage_info),
}
