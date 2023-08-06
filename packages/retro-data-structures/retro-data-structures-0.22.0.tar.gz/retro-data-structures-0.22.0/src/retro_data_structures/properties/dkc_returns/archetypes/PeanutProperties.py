# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.DebrisPropertiesOrientationEnum import DebrisPropertiesOrientationEnum
from retro_data_structures.properties.dkc_returns.archetypes.PeanutMaterialEffects import PeanutMaterialEffects
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct17 import UnknownStruct17
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class PeanutProperties(BaseProperty):
    sort_position_in_world: bool = dataclasses.field(default=False)
    initial_direction: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=1.0))
    speed: float = dataclasses.field(default=5.0)
    spin_speed: Vector = dataclasses.field(default_factory=lambda: Vector(x=-1.0, y=-1.0, z=-1.0))
    lifetime: float = dataclasses.field(default=2.0)
    fade_out_start_percentage: float = dataclasses.field(default=80.0)
    gravity: float = dataclasses.field(default=25.0)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    created_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    bounce_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    particle_system1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_system1_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    particle_system1_uses_global_translation: bool = dataclasses.field(default=False)
    particle_system1_uses_global_orientation: bool = dataclasses.field(default=False)
    particle_system1_wait_for_particles_to_die: bool = dataclasses.field(default=True)
    particle_system1_orientation: DebrisPropertiesOrientationEnum = dataclasses.field(default_factory=DebrisPropertiesOrientationEnum)
    bounce_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    bounce_particle_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    bounce_effect_transform: UnknownStruct17 = dataclasses.field(default_factory=UnknownStruct17)
    peanut_burn_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    peanut_kill_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    peanut_deflection_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    stun_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    fixed_bounce_speed_x: float = dataclasses.field(default=1.0)
    fixed_bounce_speed_y: float = dataclasses.field(default=1.0)
    num_material_effects: int = dataclasses.field(default=0)
    material_effects1: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects2: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects3: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects4: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects5: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects6: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects7: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)
    material_effects8: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00"')  # 34 properties

        data.write(b'\x97\xabv)')  # 0x97ab7629
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sort_position_in_world))

        data.write(b'\x01\xa0\xdf\xe6')  # 0x1a0dfe6
        data.write(b'\x00\x0c')  # size
        self.initial_direction.to_stream(data)

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'^\xb1~\x07')  # 0x5eb17e07
        data.write(b'\x00\x0c')  # size
        self.spin_speed.to_stream(data)

        data.write(b'2\xdcg\xf6')  # 0x32dc67f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lifetime))

        data.write(b'cS\xc4\t')  # 0x6353c409
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_start_percentage))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x93\xf8\xe0\xb0')  # 0x93f8e0b0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.created_sound))

        data.write(b'\xf1\x92Uv')  # 0xf1925576
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_sound))

        data.write(b'G\x8d\n\xa3')  # 0x478d0aa3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.particle_system1))

        data.write(b'\x19\xa6\xf7\x1f')  # 0x19a6f71f
        data.write(b'\x00\x0c')  # size
        self.particle_system1_scale.to_stream(data)

        data.write(b';\x03\xa0\x1e')  # 0x3b03a01e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_translation))

        data.write(b'\xdb\x1f\xa6\x1c')  # 0xdb1fa61c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_orientation))

        data.write(b';\xdd/\xed')  # 0x3bdd2fed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_wait_for_particles_to_die))

        data.write(b'\xf5\xddF\x90')  # 0xf5dd4690
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.particle_system1_orientation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!|7\xc2')  # 0x217c37c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_particle_effect))

        data.write(b'`\xd6\xbf\x8e')  # 0x60d6bf8e
        data.write(b'\x00\x0c')  # size
        self.bounce_particle_scale.to_stream(data)

        data.write(b'\xceY\xeb\xff')  # 0xce59ebff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bounce_effect_transform.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9;\x1a/')  # 0xe93b1a2f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.peanut_burn_effect))

        data.write(b'q\xd4\x94\xf4')  # 0x71d494f4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.peanut_kill_effect))

        data.write(b'\xbd\x1aB\xaf')  # 0xbd1a42af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.peanut_deflection_effect))

        data.write(b'\x08\x00\x0e\xc9')  # 0x8000ec9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stun_sound))

        data.write(b'\x9b\xd9C&')  # 0x9bd94326
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_bounce_speed_x))

        data.write(b'P\x85\x90\x83')  # 0x50859083
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_bounce_speed_y))

        data.write(b'\x05\xa7\x97y')  # 0x5a79779
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_material_effects))

        data.write(b'\xe8\xd2k\xae')  # 0xe8d26bae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1\xaa\xc6\xee')  # 0xd1aac6ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x82\xa2.')  # 0xc682a22e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3[\x9cn')  # 0xa35b9c6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4s\xf8\xae')  # 0xb473f8ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\x0bU\xee')  # 0x8d0b55ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a#1.')  # 0x9a23312e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\xb9)n')  # 0x46b9296e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            sort_position_in_world=data['sort_position_in_world'],
            initial_direction=Vector.from_json(data['initial_direction']),
            speed=data['speed'],
            spin_speed=Vector.from_json(data['spin_speed']),
            lifetime=data['lifetime'],
            fade_out_start_percentage=data['fade_out_start_percentage'],
            gravity=data['gravity'],
            model=data['model'],
            created_sound=data['created_sound'],
            bounce_sound=data['bounce_sound'],
            particle_system1=data['particle_system1'],
            particle_system1_scale=Vector.from_json(data['particle_system1_scale']),
            particle_system1_uses_global_translation=data['particle_system1_uses_global_translation'],
            particle_system1_uses_global_orientation=data['particle_system1_uses_global_orientation'],
            particle_system1_wait_for_particles_to_die=data['particle_system1_wait_for_particles_to_die'],
            particle_system1_orientation=DebrisPropertiesOrientationEnum.from_json(data['particle_system1_orientation']),
            bounce_particle_effect=data['bounce_particle_effect'],
            bounce_particle_scale=Vector.from_json(data['bounce_particle_scale']),
            bounce_effect_transform=UnknownStruct17.from_json(data['bounce_effect_transform']),
            peanut_burn_effect=data['peanut_burn_effect'],
            peanut_kill_effect=data['peanut_kill_effect'],
            peanut_deflection_effect=data['peanut_deflection_effect'],
            stun_sound=data['stun_sound'],
            fixed_bounce_speed_x=data['fixed_bounce_speed_x'],
            fixed_bounce_speed_y=data['fixed_bounce_speed_y'],
            num_material_effects=data['num_material_effects'],
            material_effects1=PeanutMaterialEffects.from_json(data['material_effects1']),
            material_effects2=PeanutMaterialEffects.from_json(data['material_effects2']),
            material_effects3=PeanutMaterialEffects.from_json(data['material_effects3']),
            material_effects4=PeanutMaterialEffects.from_json(data['material_effects4']),
            material_effects5=PeanutMaterialEffects.from_json(data['material_effects5']),
            material_effects6=PeanutMaterialEffects.from_json(data['material_effects6']),
            material_effects7=PeanutMaterialEffects.from_json(data['material_effects7']),
            material_effects8=PeanutMaterialEffects.from_json(data['material_effects8']),
        )

    def to_json(self) -> dict:
        return {
            'sort_position_in_world': self.sort_position_in_world,
            'initial_direction': self.initial_direction.to_json(),
            'speed': self.speed,
            'spin_speed': self.spin_speed.to_json(),
            'lifetime': self.lifetime,
            'fade_out_start_percentage': self.fade_out_start_percentage,
            'gravity': self.gravity,
            'model': self.model,
            'created_sound': self.created_sound,
            'bounce_sound': self.bounce_sound,
            'particle_system1': self.particle_system1,
            'particle_system1_scale': self.particle_system1_scale.to_json(),
            'particle_system1_uses_global_translation': self.particle_system1_uses_global_translation,
            'particle_system1_uses_global_orientation': self.particle_system1_uses_global_orientation,
            'particle_system1_wait_for_particles_to_die': self.particle_system1_wait_for_particles_to_die,
            'particle_system1_orientation': self.particle_system1_orientation.to_json(),
            'bounce_particle_effect': self.bounce_particle_effect,
            'bounce_particle_scale': self.bounce_particle_scale.to_json(),
            'bounce_effect_transform': self.bounce_effect_transform.to_json(),
            'peanut_burn_effect': self.peanut_burn_effect,
            'peanut_kill_effect': self.peanut_kill_effect,
            'peanut_deflection_effect': self.peanut_deflection_effect,
            'stun_sound': self.stun_sound,
            'fixed_bounce_speed_x': self.fixed_bounce_speed_x,
            'fixed_bounce_speed_y': self.fixed_bounce_speed_y,
            'num_material_effects': self.num_material_effects,
            'material_effects1': self.material_effects1.to_json(),
            'material_effects2': self.material_effects2.to_json(),
            'material_effects3': self.material_effects3.to_json(),
            'material_effects4': self.material_effects4.to_json(),
            'material_effects5': self.material_effects5.to_json(),
            'material_effects6': self.material_effects6.to_json(),
            'material_effects7': self.material_effects7.to_json(),
            'material_effects8': self.material_effects8.to_json(),
        }


def _decode_sort_position_in_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_direction(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spin_speed(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_start_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_created_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_particle_system1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_particle_system1_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_particle_system1_uses_global_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_uses_global_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_wait_for_particles_to_die(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_orientation(data: typing.BinaryIO, property_size: int):
    return DebrisPropertiesOrientationEnum.from_stream(data, property_size)


def _decode_bounce_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bounce_particle_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_bounce_effect_transform(data: typing.BinaryIO, property_size: int):
    return UnknownStruct17.from_stream(data, property_size)


def _decode_peanut_burn_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_peanut_kill_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_peanut_deflection_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stun_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fixed_bounce_speed_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_bounce_speed_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_num_material_effects(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_material_effects1(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects2(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects3(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects4(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects5(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects6(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects7(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


def _decode_material_effects8(data: typing.BinaryIO, property_size: int):
    return PeanutMaterialEffects.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97ab7629: ('sort_position_in_world', _decode_sort_position_in_world),
    0x1a0dfe6: ('initial_direction', _decode_initial_direction),
    0x6392404e: ('speed', _decode_speed),
    0x5eb17e07: ('spin_speed', _decode_spin_speed),
    0x32dc67f6: ('lifetime', _decode_lifetime),
    0x6353c409: ('fade_out_start_percentage', _decode_fade_out_start_percentage),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xc27ffa8f: ('model', _decode_model),
    0x93f8e0b0: ('created_sound', _decode_created_sound),
    0xf1925576: ('bounce_sound', _decode_bounce_sound),
    0x478d0aa3: ('particle_system1', _decode_particle_system1),
    0x19a6f71f: ('particle_system1_scale', _decode_particle_system1_scale),
    0x3b03a01e: ('particle_system1_uses_global_translation', _decode_particle_system1_uses_global_translation),
    0xdb1fa61c: ('particle_system1_uses_global_orientation', _decode_particle_system1_uses_global_orientation),
    0x3bdd2fed: ('particle_system1_wait_for_particles_to_die', _decode_particle_system1_wait_for_particles_to_die),
    0xf5dd4690: ('particle_system1_orientation', _decode_particle_system1_orientation),
    0x217c37c2: ('bounce_particle_effect', _decode_bounce_particle_effect),
    0x60d6bf8e: ('bounce_particle_scale', _decode_bounce_particle_scale),
    0xce59ebff: ('bounce_effect_transform', _decode_bounce_effect_transform),
    0xe93b1a2f: ('peanut_burn_effect', _decode_peanut_burn_effect),
    0x71d494f4: ('peanut_kill_effect', _decode_peanut_kill_effect),
    0xbd1a42af: ('peanut_deflection_effect', _decode_peanut_deflection_effect),
    0x8000ec9: ('stun_sound', _decode_stun_sound),
    0x9bd94326: ('fixed_bounce_speed_x', _decode_fixed_bounce_speed_x),
    0x50859083: ('fixed_bounce_speed_y', _decode_fixed_bounce_speed_y),
    0x5a79779: ('num_material_effects', _decode_num_material_effects),
    0xe8d26bae: ('material_effects1', _decode_material_effects1),
    0xd1aac6ee: ('material_effects2', _decode_material_effects2),
    0xc682a22e: ('material_effects3', _decode_material_effects3),
    0xa35b9c6e: ('material_effects4', _decode_material_effects4),
    0xb473f8ae: ('material_effects5', _decode_material_effects5),
    0x8d0b55ee: ('material_effects6', _decode_material_effects6),
    0x9a23312e: ('material_effects7', _decode_material_effects7),
    0x46b9296e: ('material_effects8', _decode_material_effects8),
}
