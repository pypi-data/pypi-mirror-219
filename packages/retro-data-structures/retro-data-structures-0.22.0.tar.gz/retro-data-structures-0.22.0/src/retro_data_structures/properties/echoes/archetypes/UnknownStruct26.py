# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct26(BaseProperty):
    effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    portal_open_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xb6\x8cm\x96')  # 0xb68c6d96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.effect))

        data.write(b'\x1af\xbe\xd7')  # 0x1a66bed7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.portal_open_sound))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x98\x01*')  # 0x1598012a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_info.to_stream(data, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            effect=data['effect'],
            portal_open_sound=data['portal_open_sound'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            beam_info=PlasmaBeamInfo.from_json(data['beam_info']),
        )

    def to_json(self) -> dict:
        return {
            'effect': self.effect,
            'portal_open_sound': self.portal_open_sound,
            'projectile_damage': self.projectile_damage.to_json(),
            'beam_info': self.beam_info.to_json(),
        }

    def _dependencies_for_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.effect)

    def _dependencies_for_portal_open_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.portal_open_sound)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_beam_info(self, asset_manager):
        yield from self.beam_info.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_effect, "effect", "AssetId"),
            (self._dependencies_for_portal_open_sound, "portal_open_sound", "int"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_beam_info, "beam_info", "PlasmaBeamInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct26.{field_name} ({field_type}): {e}"
                )


def _decode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_portal_open_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb68c6d96: ('effect', _decode_effect),
    0x1a66bed7: ('portal_open_sound', _decode_portal_open_sound),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0x1598012a: ('beam_info', _decode_beam_info),
}
