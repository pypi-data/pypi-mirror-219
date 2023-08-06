# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.FluidUVMotion import FluidUVMotion
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Color import Color
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Water(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000003: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_1: Vector = dataclasses.field(default_factory=Vector)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: bool = dataclasses.field(default=False)
    display_fluid_surface: bool = dataclasses.field(default=False)
    texture_1: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_2: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_3: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_4: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    reflection_map: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_6: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_5: Vector = dataclasses.field(default_factory=Vector)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    active: bool = dataclasses.field(default=False)
    fluid_type: int = dataclasses.field(default=0)
    unknown_11: bool = dataclasses.field(default=False)
    unknown_12: float = dataclasses.field(default=0.0)
    unnamed_0x00000016: FluidUVMotion = dataclasses.field(default_factory=FluidUVMotion)
    unknown_30: float = dataclasses.field(default=0.0)
    unknown_31: float = dataclasses.field(default=0.0)
    unknown_32: float = dataclasses.field(default=0.0)
    unknown_33: float = dataclasses.field(default=0.0)
    unknown_34: float = dataclasses.field(default=0.0)
    unknown_35: float = dataclasses.field(default=0.0)
    unknown_36: float = dataclasses.field(default=0.0)
    unknown_37: float = dataclasses.field(default=0.0)
    unknown_38: Color = dataclasses.field(default_factory=Color)
    unknown_39: Color = dataclasses.field(default_factory=Color)
    enter_particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_1: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_2: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_3: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_4: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_5: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_40: float = dataclasses.field(default=0.0)
    unknown_41: int = dataclasses.field(default=0)
    unknown_42: float = dataclasses.field(default=0.0)
    unknown_43: float = dataclasses.field(default=0.0)
    unknown_44: float = dataclasses.field(default=0.0)
    unknown_45: float = dataclasses.field(default=0.0)
    unknown_46: float = dataclasses.field(default=0.0)
    unknown_47: float = dataclasses.field(default=0.0)
    heat_wave_height: float = dataclasses.field(default=0.0)
    heat_wave_speed: float = dataclasses.field(default=0.0)
    heat_wave_color: Color = dataclasses.field(default_factory=Color)
    lightmap_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_51: float = dataclasses.field(default=0.0)
    unknown_52: float = dataclasses.field(default=0.0)
    unknown_53: float = dataclasses.field(default=0.0)
    unknown_54: int = dataclasses.field(default=0)
    unknown_55: int = dataclasses.field(default=0)
    do_not_enable___will_crash: bool = dataclasses.field(default=False)
    ignore_0x0000003d: int = dataclasses.field(default=0)
    ignore_0x0000003e: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x20

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000003 = DamageInfo.from_stream(data, property_size)
        unknown_1 = Vector.from_stream(data)
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>?', data.read(1))[0]
        display_fluid_surface = struct.unpack('>?', data.read(1))[0]
        texture_1 = struct.unpack(">L", data.read(4))[0]
        texture_2 = struct.unpack(">L", data.read(4))[0]
        texture_3 = struct.unpack(">L", data.read(4))[0]
        texture_4 = struct.unpack(">L", data.read(4))[0]
        reflection_map = struct.unpack(">L", data.read(4))[0]
        texture_6 = struct.unpack(">L", data.read(4))[0]
        unknown_5 = Vector.from_stream(data)
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        active = struct.unpack('>?', data.read(1))[0]
        fluid_type = struct.unpack('>l', data.read(4))[0]
        unknown_11 = struct.unpack('>?', data.read(1))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000016 = FluidUVMotion.from_stream(data, property_size)
        unknown_30 = struct.unpack('>f', data.read(4))[0]
        unknown_31 = struct.unpack('>f', data.read(4))[0]
        unknown_32 = struct.unpack('>f', data.read(4))[0]
        unknown_33 = struct.unpack('>f', data.read(4))[0]
        unknown_34 = struct.unpack('>f', data.read(4))[0]
        unknown_35 = struct.unpack('>f', data.read(4))[0]
        unknown_36 = struct.unpack('>f', data.read(4))[0]
        unknown_37 = struct.unpack('>f', data.read(4))[0]
        unknown_38 = Color.from_stream(data)
        unknown_39 = Color.from_stream(data)
        enter_particle = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        particle_3 = struct.unpack(">L", data.read(4))[0]
        particle_4 = struct.unpack(">L", data.read(4))[0]
        particle_5 = struct.unpack(">L", data.read(4))[0]
        sound_1 = struct.unpack('>l', data.read(4))[0]
        sound_2 = struct.unpack('>l', data.read(4))[0]
        sound_3 = struct.unpack('>l', data.read(4))[0]
        sound_4 = struct.unpack('>l', data.read(4))[0]
        sound_5 = struct.unpack('>l', data.read(4))[0]
        unknown_40 = struct.unpack('>f', data.read(4))[0]
        unknown_41 = struct.unpack('>l', data.read(4))[0]
        unknown_42 = struct.unpack('>f', data.read(4))[0]
        unknown_43 = struct.unpack('>f', data.read(4))[0]
        unknown_44 = struct.unpack('>f', data.read(4))[0]
        unknown_45 = struct.unpack('>f', data.read(4))[0]
        unknown_46 = struct.unpack('>f', data.read(4))[0]
        unknown_47 = struct.unpack('>f', data.read(4))[0]
        heat_wave_height = struct.unpack('>f', data.read(4))[0]
        heat_wave_speed = struct.unpack('>f', data.read(4))[0]
        heat_wave_color = Color.from_stream(data)
        lightmap_texture = struct.unpack(">L", data.read(4))[0]
        unknown_51 = struct.unpack('>f', data.read(4))[0]
        unknown_52 = struct.unpack('>f', data.read(4))[0]
        unknown_53 = struct.unpack('>f', data.read(4))[0]
        unknown_54 = struct.unpack('>l', data.read(4))[0]
        unknown_55 = struct.unpack('>l', data.read(4))[0]
        do_not_enable___will_crash = struct.unpack('>?', data.read(1))[0]
        ignore_0x0000003d = struct.unpack('>h', data.read(2))[0]
        ignore_0x0000003e = struct.unpack('>h', data.read(2))[0]
        return cls(name, position, scale, unnamed_0x00000003, unknown_1, unknown_2, unknown_3, display_fluid_surface, texture_1, texture_2, texture_3, texture_4, reflection_map, texture_6, unknown_5, unknown_6, unknown_7, unknown_8, active, fluid_type, unknown_11, unknown_12, unnamed_0x00000016, unknown_30, unknown_31, unknown_32, unknown_33, unknown_34, unknown_35, unknown_36, unknown_37, unknown_38, unknown_39, enter_particle, particle_2, particle_3, particle_4, particle_5, sound_1, sound_2, sound_3, sound_4, sound_5, unknown_40, unknown_41, unknown_42, unknown_43, unknown_44, unknown_45, unknown_46, unknown_47, heat_wave_height, heat_wave_speed, heat_wave_color, lightmap_texture, unknown_51, unknown_52, unknown_53, unknown_54, unknown_55, do_not_enable___will_crash, ignore_0x0000003d, ignore_0x0000003e)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00?')  # 63 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000003.to_stream(data)
        self.unknown_1.to_stream(data)
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack('>?', self.display_fluid_surface))
        data.write(struct.pack(">L", self.texture_1))
        data.write(struct.pack(">L", self.texture_2))
        data.write(struct.pack(">L", self.texture_3))
        data.write(struct.pack(">L", self.texture_4))
        data.write(struct.pack(">L", self.reflection_map))
        data.write(struct.pack(">L", self.texture_6))
        self.unknown_5.to_stream(data)
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>l', self.fluid_type))
        data.write(struct.pack('>?', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
        self.unnamed_0x00000016.to_stream(data)
        data.write(struct.pack('>f', self.unknown_30))
        data.write(struct.pack('>f', self.unknown_31))
        data.write(struct.pack('>f', self.unknown_32))
        data.write(struct.pack('>f', self.unknown_33))
        data.write(struct.pack('>f', self.unknown_34))
        data.write(struct.pack('>f', self.unknown_35))
        data.write(struct.pack('>f', self.unknown_36))
        data.write(struct.pack('>f', self.unknown_37))
        self.unknown_38.to_stream(data)
        self.unknown_39.to_stream(data)
        data.write(struct.pack(">L", self.enter_particle))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.particle_3))
        data.write(struct.pack(">L", self.particle_4))
        data.write(struct.pack(">L", self.particle_5))
        data.write(struct.pack('>l', self.sound_1))
        data.write(struct.pack('>l', self.sound_2))
        data.write(struct.pack('>l', self.sound_3))
        data.write(struct.pack('>l', self.sound_4))
        data.write(struct.pack('>l', self.sound_5))
        data.write(struct.pack('>f', self.unknown_40))
        data.write(struct.pack('>l', self.unknown_41))
        data.write(struct.pack('>f', self.unknown_42))
        data.write(struct.pack('>f', self.unknown_43))
        data.write(struct.pack('>f', self.unknown_44))
        data.write(struct.pack('>f', self.unknown_45))
        data.write(struct.pack('>f', self.unknown_46))
        data.write(struct.pack('>f', self.unknown_47))
        data.write(struct.pack('>f', self.heat_wave_height))
        data.write(struct.pack('>f', self.heat_wave_speed))
        self.heat_wave_color.to_stream(data)
        data.write(struct.pack(">L", self.lightmap_texture))
        data.write(struct.pack('>f', self.unknown_51))
        data.write(struct.pack('>f', self.unknown_52))
        data.write(struct.pack('>f', self.unknown_53))
        data.write(struct.pack('>l', self.unknown_54))
        data.write(struct.pack('>l', self.unknown_55))
        data.write(struct.pack('>?', self.do_not_enable___will_crash))
        data.write(struct.pack('>h', self.ignore_0x0000003d))
        data.write(struct.pack('>h', self.ignore_0x0000003e))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000003=DamageInfo.from_json(data['unnamed_0x00000003']),
            unknown_1=Vector.from_json(data['unknown_1']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            display_fluid_surface=data['display_fluid_surface'],
            texture_1=data['texture_1'],
            texture_2=data['texture_2'],
            texture_3=data['texture_3'],
            texture_4=data['texture_4'],
            reflection_map=data['reflection_map'],
            texture_6=data['texture_6'],
            unknown_5=Vector.from_json(data['unknown_5']),
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            active=data['active'],
            fluid_type=data['fluid_type'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unnamed_0x00000016=FluidUVMotion.from_json(data['unnamed_0x00000016']),
            unknown_30=data['unknown_30'],
            unknown_31=data['unknown_31'],
            unknown_32=data['unknown_32'],
            unknown_33=data['unknown_33'],
            unknown_34=data['unknown_34'],
            unknown_35=data['unknown_35'],
            unknown_36=data['unknown_36'],
            unknown_37=data['unknown_37'],
            unknown_38=Color.from_json(data['unknown_38']),
            unknown_39=Color.from_json(data['unknown_39']),
            enter_particle=data['enter_particle'],
            particle_2=data['particle_2'],
            particle_3=data['particle_3'],
            particle_4=data['particle_4'],
            particle_5=data['particle_5'],
            sound_1=data['sound_1'],
            sound_2=data['sound_2'],
            sound_3=data['sound_3'],
            sound_4=data['sound_4'],
            sound_5=data['sound_5'],
            unknown_40=data['unknown_40'],
            unknown_41=data['unknown_41'],
            unknown_42=data['unknown_42'],
            unknown_43=data['unknown_43'],
            unknown_44=data['unknown_44'],
            unknown_45=data['unknown_45'],
            unknown_46=data['unknown_46'],
            unknown_47=data['unknown_47'],
            heat_wave_height=data['heat_wave_height'],
            heat_wave_speed=data['heat_wave_speed'],
            heat_wave_color=Color.from_json(data['heat_wave_color']),
            lightmap_texture=data['lightmap_texture'],
            unknown_51=data['unknown_51'],
            unknown_52=data['unknown_52'],
            unknown_53=data['unknown_53'],
            unknown_54=data['unknown_54'],
            unknown_55=data['unknown_55'],
            do_not_enable___will_crash=data['do_not_enable___will_crash'],
            ignore_0x0000003d=data['ignore_0x0000003d'],
            ignore_0x0000003e=data['ignore_0x0000003e'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000003': self.unnamed_0x00000003.to_json(),
            'unknown_1': self.unknown_1.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'display_fluid_surface': self.display_fluid_surface,
            'texture_1': self.texture_1,
            'texture_2': self.texture_2,
            'texture_3': self.texture_3,
            'texture_4': self.texture_4,
            'reflection_map': self.reflection_map,
            'texture_6': self.texture_6,
            'unknown_5': self.unknown_5.to_json(),
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'active': self.active,
            'fluid_type': self.fluid_type,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unnamed_0x00000016': self.unnamed_0x00000016.to_json(),
            'unknown_30': self.unknown_30,
            'unknown_31': self.unknown_31,
            'unknown_32': self.unknown_32,
            'unknown_33': self.unknown_33,
            'unknown_34': self.unknown_34,
            'unknown_35': self.unknown_35,
            'unknown_36': self.unknown_36,
            'unknown_37': self.unknown_37,
            'unknown_38': self.unknown_38.to_json(),
            'unknown_39': self.unknown_39.to_json(),
            'enter_particle': self.enter_particle,
            'particle_2': self.particle_2,
            'particle_3': self.particle_3,
            'particle_4': self.particle_4,
            'particle_5': self.particle_5,
            'sound_1': self.sound_1,
            'sound_2': self.sound_2,
            'sound_3': self.sound_3,
            'sound_4': self.sound_4,
            'sound_5': self.sound_5,
            'unknown_40': self.unknown_40,
            'unknown_41': self.unknown_41,
            'unknown_42': self.unknown_42,
            'unknown_43': self.unknown_43,
            'unknown_44': self.unknown_44,
            'unknown_45': self.unknown_45,
            'unknown_46': self.unknown_46,
            'unknown_47': self.unknown_47,
            'heat_wave_height': self.heat_wave_height,
            'heat_wave_speed': self.heat_wave_speed,
            'heat_wave_color': self.heat_wave_color.to_json(),
            'lightmap_texture': self.lightmap_texture,
            'unknown_51': self.unknown_51,
            'unknown_52': self.unknown_52,
            'unknown_53': self.unknown_53,
            'unknown_54': self.unknown_54,
            'unknown_55': self.unknown_55,
            'do_not_enable___will_crash': self.do_not_enable___will_crash,
            'ignore_0x0000003d': self.ignore_0x0000003d,
            'ignore_0x0000003e': self.ignore_0x0000003e,
        }

    def _dependencies_for_unnamed_0x00000003(self, asset_manager):
        yield from self.unnamed_0x00000003.dependencies_for(asset_manager)

    def _dependencies_for_texture_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_1)

    def _dependencies_for_texture_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_2)

    def _dependencies_for_texture_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_3)

    def _dependencies_for_texture_4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_4)

    def _dependencies_for_reflection_map(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.reflection_map)

    def _dependencies_for_texture_6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture_6)

    def _dependencies_for_unnamed_0x00000016(self, asset_manager):
        yield from self.unnamed_0x00000016.dependencies_for(asset_manager)

    def _dependencies_for_enter_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.enter_particle)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_particle_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_3)

    def _dependencies_for_particle_4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_4)

    def _dependencies_for_particle_5(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_5)

    def _dependencies_for_sound_1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_1)

    def _dependencies_for_sound_2(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_2)

    def _dependencies_for_sound_3(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_3)

    def _dependencies_for_sound_4(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_4)

    def _dependencies_for_sound_5(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_5)

    def _dependencies_for_lightmap_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.lightmap_texture)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000003, "unnamed_0x00000003", "DamageInfo"),
            (self._dependencies_for_texture_1, "texture_1", "AssetId"),
            (self._dependencies_for_texture_2, "texture_2", "AssetId"),
            (self._dependencies_for_texture_3, "texture_3", "AssetId"),
            (self._dependencies_for_texture_4, "texture_4", "AssetId"),
            (self._dependencies_for_reflection_map, "reflection_map", "AssetId"),
            (self._dependencies_for_texture_6, "texture_6", "AssetId"),
            (self._dependencies_for_unnamed_0x00000016, "unnamed_0x00000016", "FluidUVMotion"),
            (self._dependencies_for_enter_particle, "enter_particle", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_particle_3, "particle_3", "AssetId"),
            (self._dependencies_for_particle_4, "particle_4", "AssetId"),
            (self._dependencies_for_particle_5, "particle_5", "AssetId"),
            (self._dependencies_for_sound_1, "sound_1", "int"),
            (self._dependencies_for_sound_2, "sound_2", "int"),
            (self._dependencies_for_sound_3, "sound_3", "int"),
            (self._dependencies_for_sound_4, "sound_4", "int"),
            (self._dependencies_for_sound_5, "sound_5", "int"),
            (self._dependencies_for_lightmap_texture, "lightmap_texture", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Water.{field_name} ({field_type}): {e}"
                )
