# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.IngSpaceJumpGuardianStruct import IngSpaceJumpGuardianStruct
from retro_data_structures.properties.echoes.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.echoes.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct32(BaseProperty):
    ing_spot_blob_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound: int = dataclasses.field(default=0, metadata={'sound': True})
    ing_space_jump_guardian_struct_0x5e1d1931: IngSpaceJumpGuardianStruct = dataclasses.field(default_factory=IngSpaceJumpGuardianStruct)
    ing_space_jump_guardian_struct_0x6b08e2e5: IngSpaceJumpGuardianStruct = dataclasses.field(default_factory=IngSpaceJumpGuardianStruct)
    ing_space_jump_guardian_struct_0xf223aa76: IngSpaceJumpGuardianStruct = dataclasses.field(default_factory=IngSpaceJumpGuardianStruct)
    ing_space_jump_guardian_struct_0xd0db5f7a: IngSpaceJumpGuardianStruct = dataclasses.field(default_factory=IngSpaceJumpGuardianStruct)
    light_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    light_attenuation: float = dataclasses.field(default=5.0)
    mini_portal_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_mini_portal: int = dataclasses.field(default=0, metadata={'sound': True})
    mini_portal_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    mini_portal_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xccZI\x18')  # 0xcc5a4918
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ing_spot_blob_effect))

        data.write(b'F\xe9\x02\xe8')  # 0x46e902e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound))

        data.write(b'^\x1d\x191')  # 0x5e1d1931
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_space_jump_guardian_struct_0x5e1d1931.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'k\x08\xe2\xe5')  # 0x6b08e2e5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_space_jump_guardian_struct_0x6b08e2e5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2#\xaav')  # 0xf223aa76
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_space_jump_guardian_struct_0xf223aa76.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd0\xdb_z')  # 0xd0db5f7a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_space_jump_guardian_struct_0xd0db5f7a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd>\xfe}')  # 0xbd3efe7d
        data.write(b'\x00\x10')  # size
        self.light_color.to_stream(data)

        data.write(b'\xd2K\x88\x8f')  # 0xd24b888f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.light_attenuation))

        data.write(b'\xa9&\xf8\xa8')  # 0xa926f8a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mini_portal_effect))

        data.write(b'@Q\xfd\x1a')  # 0x4051fd1a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_mini_portal))

        data.write(b'BJm7')  # 0x424a6d37
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mini_portal_projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\x17\th')  # 0x9c170968
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mini_portal_beam_info.to_stream(data, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8fG\x87\xcb')  # 0x8f4787cb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ing_spot_blob_effect=data['ing_spot_blob_effect'],
            sound=data['sound'],
            ing_space_jump_guardian_struct_0x5e1d1931=IngSpaceJumpGuardianStruct.from_json(data['ing_space_jump_guardian_struct_0x5e1d1931']),
            ing_space_jump_guardian_struct_0x6b08e2e5=IngSpaceJumpGuardianStruct.from_json(data['ing_space_jump_guardian_struct_0x6b08e2e5']),
            ing_space_jump_guardian_struct_0xf223aa76=IngSpaceJumpGuardianStruct.from_json(data['ing_space_jump_guardian_struct_0xf223aa76']),
            ing_space_jump_guardian_struct_0xd0db5f7a=IngSpaceJumpGuardianStruct.from_json(data['ing_space_jump_guardian_struct_0xd0db5f7a']),
            light_color=Color.from_json(data['light_color']),
            light_attenuation=data['light_attenuation'],
            mini_portal_effect=data['mini_portal_effect'],
            sound_mini_portal=data['sound_mini_portal'],
            mini_portal_projectile_damage=DamageInfo.from_json(data['mini_portal_projectile_damage']),
            mini_portal_beam_info=PlasmaBeamInfo.from_json(data['mini_portal_beam_info']),
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
        )

    def to_json(self) -> dict:
        return {
            'ing_spot_blob_effect': self.ing_spot_blob_effect,
            'sound': self.sound,
            'ing_space_jump_guardian_struct_0x5e1d1931': self.ing_space_jump_guardian_struct_0x5e1d1931.to_json(),
            'ing_space_jump_guardian_struct_0x6b08e2e5': self.ing_space_jump_guardian_struct_0x6b08e2e5.to_json(),
            'ing_space_jump_guardian_struct_0xf223aa76': self.ing_space_jump_guardian_struct_0xf223aa76.to_json(),
            'ing_space_jump_guardian_struct_0xd0db5f7a': self.ing_space_jump_guardian_struct_0xd0db5f7a.to_json(),
            'light_color': self.light_color.to_json(),
            'light_attenuation': self.light_attenuation,
            'mini_portal_effect': self.mini_portal_effect,
            'sound_mini_portal': self.sound_mini_portal,
            'mini_portal_projectile_damage': self.mini_portal_projectile_damage.to_json(),
            'mini_portal_beam_info': self.mini_portal_beam_info.to_json(),
            'shock_wave_info': self.shock_wave_info.to_json(),
        }

    def _dependencies_for_ing_spot_blob_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ing_spot_blob_effect)

    def _dependencies_for_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound)

    def _dependencies_for_ing_space_jump_guardian_struct_0x5e1d1931(self, asset_manager):
        yield from self.ing_space_jump_guardian_struct_0x5e1d1931.dependencies_for(asset_manager)

    def _dependencies_for_ing_space_jump_guardian_struct_0x6b08e2e5(self, asset_manager):
        yield from self.ing_space_jump_guardian_struct_0x6b08e2e5.dependencies_for(asset_manager)

    def _dependencies_for_ing_space_jump_guardian_struct_0xf223aa76(self, asset_manager):
        yield from self.ing_space_jump_guardian_struct_0xf223aa76.dependencies_for(asset_manager)

    def _dependencies_for_ing_space_jump_guardian_struct_0xd0db5f7a(self, asset_manager):
        yield from self.ing_space_jump_guardian_struct_0xd0db5f7a.dependencies_for(asset_manager)

    def _dependencies_for_mini_portal_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.mini_portal_effect)

    def _dependencies_for_sound_mini_portal(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_mini_portal)

    def _dependencies_for_mini_portal_projectile_damage(self, asset_manager):
        yield from self.mini_portal_projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_mini_portal_beam_info(self, asset_manager):
        yield from self.mini_portal_beam_info.dependencies_for(asset_manager)

    def _dependencies_for_shock_wave_info(self, asset_manager):
        yield from self.shock_wave_info.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_ing_spot_blob_effect, "ing_spot_blob_effect", "AssetId"),
            (self._dependencies_for_sound, "sound", "int"),
            (self._dependencies_for_ing_space_jump_guardian_struct_0x5e1d1931, "ing_space_jump_guardian_struct_0x5e1d1931", "IngSpaceJumpGuardianStruct"),
            (self._dependencies_for_ing_space_jump_guardian_struct_0x6b08e2e5, "ing_space_jump_guardian_struct_0x6b08e2e5", "IngSpaceJumpGuardianStruct"),
            (self._dependencies_for_ing_space_jump_guardian_struct_0xf223aa76, "ing_space_jump_guardian_struct_0xf223aa76", "IngSpaceJumpGuardianStruct"),
            (self._dependencies_for_ing_space_jump_guardian_struct_0xd0db5f7a, "ing_space_jump_guardian_struct_0xd0db5f7a", "IngSpaceJumpGuardianStruct"),
            (self._dependencies_for_mini_portal_effect, "mini_portal_effect", "AssetId"),
            (self._dependencies_for_sound_mini_portal, "sound_mini_portal", "int"),
            (self._dependencies_for_mini_portal_projectile_damage, "mini_portal_projectile_damage", "DamageInfo"),
            (self._dependencies_for_mini_portal_beam_info, "mini_portal_beam_info", "PlasmaBeamInfo"),
            (self._dependencies_for_shock_wave_info, "shock_wave_info", "ShockWaveInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct32.{field_name} ({field_type}): {e}"
                )


def _decode_ing_spot_blob_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ing_space_jump_guardian_struct_0x5e1d1931(data: typing.BinaryIO, property_size: int):
    return IngSpaceJumpGuardianStruct.from_stream(data, property_size)


def _decode_ing_space_jump_guardian_struct_0x6b08e2e5(data: typing.BinaryIO, property_size: int):
    return IngSpaceJumpGuardianStruct.from_stream(data, property_size)


def _decode_ing_space_jump_guardian_struct_0xf223aa76(data: typing.BinaryIO, property_size: int):
    return IngSpaceJumpGuardianStruct.from_stream(data, property_size)


def _decode_ing_space_jump_guardian_struct_0xd0db5f7a(data: typing.BinaryIO, property_size: int):
    return IngSpaceJumpGuardianStruct.from_stream(data, property_size)


def _decode_light_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_light_attenuation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mini_portal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_mini_portal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mini_portal_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_mini_portal_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcc5a4918: ('ing_spot_blob_effect', _decode_ing_spot_blob_effect),
    0x46e902e8: ('sound', _decode_sound),
    0x5e1d1931: ('ing_space_jump_guardian_struct_0x5e1d1931', _decode_ing_space_jump_guardian_struct_0x5e1d1931),
    0x6b08e2e5: ('ing_space_jump_guardian_struct_0x6b08e2e5', _decode_ing_space_jump_guardian_struct_0x6b08e2e5),
    0xf223aa76: ('ing_space_jump_guardian_struct_0xf223aa76', _decode_ing_space_jump_guardian_struct_0xf223aa76),
    0xd0db5f7a: ('ing_space_jump_guardian_struct_0xd0db5f7a', _decode_ing_space_jump_guardian_struct_0xd0db5f7a),
    0xbd3efe7d: ('light_color', _decode_light_color),
    0xd24b888f: ('light_attenuation', _decode_light_attenuation),
    0xa926f8a8: ('mini_portal_effect', _decode_mini_portal_effect),
    0x4051fd1a: ('sound_mini_portal', _decode_sound_mini_portal),
    0x424a6d37: ('mini_portal_projectile_damage', _decode_mini_portal_projectile_damage),
    0x9c170968: ('mini_portal_beam_info', _decode_mini_portal_beam_info),
    0x8f4787cb: ('shock_wave_info', _decode_shock_wave_info),
}
