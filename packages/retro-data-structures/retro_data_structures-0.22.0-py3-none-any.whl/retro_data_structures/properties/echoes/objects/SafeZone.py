# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EchoParameters import EchoParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.SafeZoneStructA import SafeZoneStructA
from retro_data_structures.properties.echoes.archetypes.SafeZoneStructB import SafeZoneStructB
from retro_data_structures.properties.echoes.archetypes.TriggerInfo import TriggerInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class SafeZone(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    trigger: TriggerInfo = dataclasses.field(default_factory=TriggerInfo)
    deactivate_on_enter: bool = dataclasses.field(default=False)
    deactivate_on_exit: bool = dataclasses.field(default=False)
    activation_time: float = dataclasses.field(default=0.15000000596046448)
    deactivation_time: float = dataclasses.field(default=0.15000000596046448)
    lifetime: float = dataclasses.field(default=0.0)
    random_lifetime_offset: float = dataclasses.field(default=0.0)
    impact_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    filter_sound_effects: bool = dataclasses.field(default=True)
    unknown_0x414379ea: int = dataclasses.field(default=300)
    ignore_cinematic_camera: bool = dataclasses.field(default=False)
    normal_safe_zone_struct: SafeZoneStructB = dataclasses.field(default_factory=SafeZoneStructB)
    energized_safe_zone_struct: SafeZoneStructB = dataclasses.field(default_factory=SafeZoneStructB)
    supercharged_safe_zone_struct: SafeZoneStructB = dataclasses.field(default_factory=SafeZoneStructB)
    normal_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    inside_fade_start: float = dataclasses.field(default=3.0)
    inside_fade_time: float = dataclasses.field(default=2.0)
    unknown_0x6c14904c: float = dataclasses.field(default=0.25)
    flash_time: float = dataclasses.field(default=1.0)
    flash_brightness: float = dataclasses.field(default=0.5)
    flash_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    safezone_shape: int = dataclasses.field(default=0)
    mobile: bool = dataclasses.field(default=False)
    generate_mobile_light: bool = dataclasses.field(default=False)
    mobile_light_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0xe71b43e1: Color = dataclasses.field(default_factory=lambda: Color(r=0.7372549772262573, g=1.0, b=1.0, a=0.24705900251865387))
    unknown_0x9f638987: float = dataclasses.field(default=0.20000000298023224)
    safe_zone_struct_a_0x8a09f99a: SafeZoneStructA = dataclasses.field(default_factory=SafeZoneStructA)
    safe_zone_struct_a_0xafb855b8: SafeZoneStructA = dataclasses.field(default_factory=SafeZoneStructA)
    echo_parameters: EchoParameters = dataclasses.field(default_factory=EchoParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SAFE'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ScriptSafeZone.rel']

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00 ')  # 32 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\xa2t\x11')  # 0x77a27411
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.trigger.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d3F_')  # 0x8d33465f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.deactivate_on_enter))

        data.write(b'\x1cE9\x86')  # 0x1c453986
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.deactivate_on_exit))

        data.write(b'\xea\xd3\xe2.')  # 0xead3e22e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_time))

        data.write(b'\xb5\xcd\xf1\x96')  # 0xb5cdf196
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deactivation_time))

        data.write(b'2\xdcg\xf6')  # 0x32dc67f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lifetime))

        data.write(b'\xde\x16\x9d\xb0')  # 0xde169db0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_lifetime_offset))

        data.write(b'\x9b\xe4\xbb\xd8')  # 0x9be4bbd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.impact_effect))

        data.write(b'\x82!\x18\xb4')  # 0x822118b4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.filter_sound_effects))

        data.write(b'ACy\xea')  # 0x414379ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x414379ea))

        data.write(b'b\xba\xc4`')  # 0x62bac460
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_cinematic_camera))

        data.write(b'\xb4\xa2\x93\xc7')  # 0xb4a293c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_safe_zone_struct.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda\xe8\xc1N')  # 0xdae8c14e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energized_safe_zone_struct.to_stream(data, default_override={'shell1_animated_horiz_rate': 0.03999999910593033, 'shell1_animated_vert_rate': 0.0, 'shell1_scale_horiz': 4.0, 'shell1_scale_vert': 2.0, 'shell2_scale_horiz': 10.0, 'shell2_scale_vert': 12.0, 'shell_color': Color(r=1.0, g=0.7372549772262573, b=0.3921569883823395, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'dq\xd6C')  # 0x6471d643
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.supercharged_safe_zone_struct.to_stream(data, default_override={'shell1_animated_horiz_rate': 0.03999999910593033, 'shell1_animated_vert_rate': 0.0, 'shell1_scale_horiz': 4.0, 'shell1_scale_vert': 2.0, 'shell2_scale_horiz': 10.0, 'shell2_scale_vert': 12.0, 'shell_color': Color(r=1.0, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\xe2\xb1\x88')  # 0xeee2b188
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_damage.to_stream(data, default_override={'di_weapon_type': 20})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\xa1<\xa0')  # 0x78a13ca0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data, default_override={'di_weapon_type': 18})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08\xcc\xff\xd0')  # 0x8ccffd0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.inside_fade_start))

        data.write(b'\x7f\xeb\xbf\xe7')  # 0x7febbfe7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.inside_fade_time))

        data.write(b'l\x14\x90L')  # 0x6c14904c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6c14904c))

        data.write(b'H\xb4\xb8e')  # 0x48b4b865
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_time))

        data.write(b'E/xv')  # 0x452f7876
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_brightness))

        data.write(b'O\xaa\xc8\x96')  # 0x4faac896
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flash_sound))

        data.write(b'\xd5\x86\x9b\x0b')  # 0xd5869b0b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.safezone_shape))

        data.write(b'"*%\x8e')  # 0x222a258e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.mobile))

        data.write(b'l\x90\xe3\x96')  # 0x6c90e396
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.generate_mobile_light))

        data.write(b'\xa7\x96>\x03')  # 0xa7963e03
        data.write(b'\x00\x0c')  # size
        self.mobile_light_offset.to_stream(data)

        data.write(b'\xe7\x1bC\xe1')  # 0xe71b43e1
        data.write(b'\x00\x10')  # size
        self.unknown_0xe71b43e1.to_stream(data)

        data.write(b'\x9fc\x89\x87')  # 0x9f638987
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9f638987))

        data.write(b'\x8a\t\xf9\x9a')  # 0x8a09f99a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.safe_zone_struct_a_0x8a09f99a.to_stream(data, default_override={'enabled': False, 'mode': 1, 'color': Color(r=0.7372549772262573, g=1.0, b=1.0, a=0.0), 'color_rate': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf\xb8U\xb8')  # 0xafb855b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.safe_zone_struct_a_0xafb855b8.to_stream(data, default_override={'enabled': False, 'mode': 1, 'color': Color(r=0.0, g=0.09803900122642517, b=0.0, a=0.0), 'color_rate': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Dv\xbe\xd8')  # 0x4476bed8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.echo_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            trigger=TriggerInfo.from_json(data['trigger']),
            deactivate_on_enter=data['deactivate_on_enter'],
            deactivate_on_exit=data['deactivate_on_exit'],
            activation_time=data['activation_time'],
            deactivation_time=data['deactivation_time'],
            lifetime=data['lifetime'],
            random_lifetime_offset=data['random_lifetime_offset'],
            impact_effect=data['impact_effect'],
            filter_sound_effects=data['filter_sound_effects'],
            unknown_0x414379ea=data['unknown_0x414379ea'],
            ignore_cinematic_camera=data['ignore_cinematic_camera'],
            normal_safe_zone_struct=SafeZoneStructB.from_json(data['normal_safe_zone_struct']),
            energized_safe_zone_struct=SafeZoneStructB.from_json(data['energized_safe_zone_struct']),
            supercharged_safe_zone_struct=SafeZoneStructB.from_json(data['supercharged_safe_zone_struct']),
            normal_damage=DamageInfo.from_json(data['normal_damage']),
            damage_info=DamageInfo.from_json(data['damage_info']),
            inside_fade_start=data['inside_fade_start'],
            inside_fade_time=data['inside_fade_time'],
            unknown_0x6c14904c=data['unknown_0x6c14904c'],
            flash_time=data['flash_time'],
            flash_brightness=data['flash_brightness'],
            flash_sound=data['flash_sound'],
            safezone_shape=data['safezone_shape'],
            mobile=data['mobile'],
            generate_mobile_light=data['generate_mobile_light'],
            mobile_light_offset=Vector.from_json(data['mobile_light_offset']),
            unknown_0xe71b43e1=Color.from_json(data['unknown_0xe71b43e1']),
            unknown_0x9f638987=data['unknown_0x9f638987'],
            safe_zone_struct_a_0x8a09f99a=SafeZoneStructA.from_json(data['safe_zone_struct_a_0x8a09f99a']),
            safe_zone_struct_a_0xafb855b8=SafeZoneStructA.from_json(data['safe_zone_struct_a_0xafb855b8']),
            echo_parameters=EchoParameters.from_json(data['echo_parameters']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'trigger': self.trigger.to_json(),
            'deactivate_on_enter': self.deactivate_on_enter,
            'deactivate_on_exit': self.deactivate_on_exit,
            'activation_time': self.activation_time,
            'deactivation_time': self.deactivation_time,
            'lifetime': self.lifetime,
            'random_lifetime_offset': self.random_lifetime_offset,
            'impact_effect': self.impact_effect,
            'filter_sound_effects': self.filter_sound_effects,
            'unknown_0x414379ea': self.unknown_0x414379ea,
            'ignore_cinematic_camera': self.ignore_cinematic_camera,
            'normal_safe_zone_struct': self.normal_safe_zone_struct.to_json(),
            'energized_safe_zone_struct': self.energized_safe_zone_struct.to_json(),
            'supercharged_safe_zone_struct': self.supercharged_safe_zone_struct.to_json(),
            'normal_damage': self.normal_damage.to_json(),
            'damage_info': self.damage_info.to_json(),
            'inside_fade_start': self.inside_fade_start,
            'inside_fade_time': self.inside_fade_time,
            'unknown_0x6c14904c': self.unknown_0x6c14904c,
            'flash_time': self.flash_time,
            'flash_brightness': self.flash_brightness,
            'flash_sound': self.flash_sound,
            'safezone_shape': self.safezone_shape,
            'mobile': self.mobile,
            'generate_mobile_light': self.generate_mobile_light,
            'mobile_light_offset': self.mobile_light_offset.to_json(),
            'unknown_0xe71b43e1': self.unknown_0xe71b43e1.to_json(),
            'unknown_0x9f638987': self.unknown_0x9f638987,
            'safe_zone_struct_a_0x8a09f99a': self.safe_zone_struct_a_0x8a09f99a.to_json(),
            'safe_zone_struct_a_0xafb855b8': self.safe_zone_struct_a_0xafb855b8.to_json(),
            'echo_parameters': self.echo_parameters.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_trigger(self, asset_manager):
        yield from self.trigger.dependencies_for(asset_manager)

    def _dependencies_for_impact_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.impact_effect)

    def _dependencies_for_normal_safe_zone_struct(self, asset_manager):
        yield from self.normal_safe_zone_struct.dependencies_for(asset_manager)

    def _dependencies_for_energized_safe_zone_struct(self, asset_manager):
        yield from self.energized_safe_zone_struct.dependencies_for(asset_manager)

    def _dependencies_for_supercharged_safe_zone_struct(self, asset_manager):
        yield from self.supercharged_safe_zone_struct.dependencies_for(asset_manager)

    def _dependencies_for_normal_damage(self, asset_manager):
        yield from self.normal_damage.dependencies_for(asset_manager)

    def _dependencies_for_damage_info(self, asset_manager):
        yield from self.damage_info.dependencies_for(asset_manager)

    def _dependencies_for_flash_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.flash_sound)

    def _dependencies_for_safe_zone_struct_a_0x8a09f99a(self, asset_manager):
        yield from self.safe_zone_struct_a_0x8a09f99a.dependencies_for(asset_manager)

    def _dependencies_for_safe_zone_struct_a_0xafb855b8(self, asset_manager):
        yield from self.safe_zone_struct_a_0xafb855b8.dependencies_for(asset_manager)

    def _dependencies_for_echo_parameters(self, asset_manager):
        yield from self.echo_parameters.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_trigger, "trigger", "TriggerInfo"),
            (self._dependencies_for_impact_effect, "impact_effect", "AssetId"),
            (self._dependencies_for_normal_safe_zone_struct, "normal_safe_zone_struct", "SafeZoneStructB"),
            (self._dependencies_for_energized_safe_zone_struct, "energized_safe_zone_struct", "SafeZoneStructB"),
            (self._dependencies_for_supercharged_safe_zone_struct, "supercharged_safe_zone_struct", "SafeZoneStructB"),
            (self._dependencies_for_normal_damage, "normal_damage", "DamageInfo"),
            (self._dependencies_for_damage_info, "damage_info", "DamageInfo"),
            (self._dependencies_for_flash_sound, "flash_sound", "int"),
            (self._dependencies_for_safe_zone_struct_a_0x8a09f99a, "safe_zone_struct_a_0x8a09f99a", "SafeZoneStructA"),
            (self._dependencies_for_safe_zone_struct_a_0xafb855b8, "safe_zone_struct_a_0xafb855b8", "SafeZoneStructA"),
            (self._dependencies_for_echo_parameters, "echo_parameters", "EchoParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SafeZone.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_trigger(data: typing.BinaryIO, property_size: int):
    return TriggerInfo.from_stream(data, property_size)


def _decode_deactivate_on_enter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_deactivate_on_exit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_activation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deactivation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_lifetime_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impact_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_filter_sound_effects(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x414379ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ignore_cinematic_camera(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_normal_safe_zone_struct(data: typing.BinaryIO, property_size: int):
    return SafeZoneStructB.from_stream(data, property_size)


def _decode_energized_safe_zone_struct(data: typing.BinaryIO, property_size: int):
    return SafeZoneStructB.from_stream(data, property_size, default_override={'shell1_animated_horiz_rate': 0.03999999910593033, 'shell1_animated_vert_rate': 0.0, 'shell1_scale_horiz': 4.0, 'shell1_scale_vert': 2.0, 'shell2_scale_horiz': 10.0, 'shell2_scale_vert': 12.0, 'shell_color': Color(r=1.0, g=0.7372549772262573, b=0.3921569883823395, a=0.0)})


def _decode_supercharged_safe_zone_struct(data: typing.BinaryIO, property_size: int):
    return SafeZoneStructB.from_stream(data, property_size, default_override={'shell1_animated_horiz_rate': 0.03999999910593033, 'shell1_animated_vert_rate': 0.0, 'shell1_scale_horiz': 4.0, 'shell1_scale_vert': 2.0, 'shell2_scale_horiz': 10.0, 'shell2_scale_vert': 12.0, 'shell_color': Color(r=1.0, g=0.0, b=0.0, a=0.0)})


def _decode_normal_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 20})


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 18})


def _decode_inside_fade_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_inside_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6c14904c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_brightness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_safezone_shape(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mobile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_generate_mobile_light(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_mobile_light_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0xe71b43e1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9f638987(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_safe_zone_struct_a_0x8a09f99a(data: typing.BinaryIO, property_size: int):
    return SafeZoneStructA.from_stream(data, property_size, default_override={'enabled': False, 'mode': 1, 'color': Color(r=0.7372549772262573, g=1.0, b=1.0, a=0.0), 'color_rate': 5.0})


def _decode_safe_zone_struct_a_0xafb855b8(data: typing.BinaryIO, property_size: int):
    return SafeZoneStructA.from_stream(data, property_size, default_override={'enabled': False, 'mode': 1, 'color': Color(r=0.0, g=0.09803900122642517, b=0.0, a=0.0), 'color_rate': 5.0})


def _decode_echo_parameters(data: typing.BinaryIO, property_size: int):
    return EchoParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x77a27411: ('trigger', _decode_trigger),
    0x8d33465f: ('deactivate_on_enter', _decode_deactivate_on_enter),
    0x1c453986: ('deactivate_on_exit', _decode_deactivate_on_exit),
    0xead3e22e: ('activation_time', _decode_activation_time),
    0xb5cdf196: ('deactivation_time', _decode_deactivation_time),
    0x32dc67f6: ('lifetime', _decode_lifetime),
    0xde169db0: ('random_lifetime_offset', _decode_random_lifetime_offset),
    0x9be4bbd8: ('impact_effect', _decode_impact_effect),
    0x822118b4: ('filter_sound_effects', _decode_filter_sound_effects),
    0x414379ea: ('unknown_0x414379ea', _decode_unknown_0x414379ea),
    0x62bac460: ('ignore_cinematic_camera', _decode_ignore_cinematic_camera),
    0xb4a293c7: ('normal_safe_zone_struct', _decode_normal_safe_zone_struct),
    0xdae8c14e: ('energized_safe_zone_struct', _decode_energized_safe_zone_struct),
    0x6471d643: ('supercharged_safe_zone_struct', _decode_supercharged_safe_zone_struct),
    0xeee2b188: ('normal_damage', _decode_normal_damage),
    0x78a13ca0: ('damage_info', _decode_damage_info),
    0x8ccffd0: ('inside_fade_start', _decode_inside_fade_start),
    0x7febbfe7: ('inside_fade_time', _decode_inside_fade_time),
    0x6c14904c: ('unknown_0x6c14904c', _decode_unknown_0x6c14904c),
    0x48b4b865: ('flash_time', _decode_flash_time),
    0x452f7876: ('flash_brightness', _decode_flash_brightness),
    0x4faac896: ('flash_sound', _decode_flash_sound),
    0xd5869b0b: ('safezone_shape', _decode_safezone_shape),
    0x222a258e: ('mobile', _decode_mobile),
    0x6c90e396: ('generate_mobile_light', _decode_generate_mobile_light),
    0xa7963e03: ('mobile_light_offset', _decode_mobile_light_offset),
    0xe71b43e1: ('unknown_0xe71b43e1', _decode_unknown_0xe71b43e1),
    0x9f638987: ('unknown_0x9f638987', _decode_unknown_0x9f638987),
    0x8a09f99a: ('safe_zone_struct_a_0x8a09f99a', _decode_safe_zone_struct_a_0x8a09f99a),
    0xafb855b8: ('safe_zone_struct_a_0xafb855b8', _decode_safe_zone_struct_a_0xafb855b8),
    0x4476bed8: ('echo_parameters', _decode_echo_parameters),
}
