# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.archetypes.StaticGeometryTest import StaticGeometryTest
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color
from retro_data_structures.properties.corruption.core.Spline import Spline
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class Actor(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    mass: float = dataclasses.field(default=1.0)
    gravity: float = dataclasses.field(default=0.0)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    is_loop: bool = dataclasses.field(default=True)
    immovable: bool = dataclasses.field(default=True)
    is_solid: bool = dataclasses.field(default=True)
    is_camera_through: bool = dataclasses.field(default=False)
    render_texture_set: int = dataclasses.field(default=0)
    draws_shadow: bool = dataclasses.field(default=False)
    render_first_sorted: bool = dataclasses.field(default=False)
    scale_animation: bool = dataclasses.field(default=True)
    unknown_0xa09d4a1f: bool = dataclasses.field(default=False)
    is_phaazite: bool = dataclasses.field(default=False)
    unknown_0xaa49b627: float = dataclasses.field(default=1.0)
    use_mod_inca: bool = dataclasses.field(default=False)
    mod_inca_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    mod_inca_amount: Spline = dataclasses.field(default_factory=Spline)
    random_animation_offset: float = dataclasses.field(default=0.0)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    projectile_static_geometry_test: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)
    orbit_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    orbit_offset_local: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ACTR'

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3D\xc0\xb0')  # 0xf344c0b0
        data.write(b'\x00\x0c')  # size
        self.collision_box.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\x8d\x1b\x93')  # 0xc08d1b93
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_loop))

        data.write(b'\x1e2R>')  # 0x1e32523e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.immovable))

        data.write(b'\x1d\x8d\xd8F')  # 0x1d8dd846
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_solid))

        data.write(b'xY\xb5 ')  # 0x7859b520
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_camera_through))

        data.write(b'2\xfa\xb9~')  # 0x32fab97e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_texture_set))

        data.write(b'\x97htF')  # 0x97687446
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.draws_shadow))

        data.write(b'GC)O')  # 0x4743294f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_first_sorted))

        data.write(b'&\x1e\x92\xa4')  # 0x261e92a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scale_animation))

        data.write(b'\xa0\x9dJ\x1f')  # 0xa09d4a1f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa09d4a1f))

        data.write(b'\xf3\xde\x93\x11')  # 0xf3de9311
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_phaazite))

        data.write(b"\xaaI\xb6'")  # 0xaa49b627
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaa49b627))

        data.write(b'\xb50\xd7\xde')  # 0xb530d7de
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_mod_inca))

        data.write(b'\xf8\xdfl\xd2')  # 0xf8df6cd2
        data.write(b'\x00\x10')  # size
        self.mod_inca_color.to_stream(data)

        data.write(b'\xc20\x11\xd9')  # 0xc23011d9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mod_inca_amount.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbfi\xc0>')  # 0xbf69c03e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_animation_offset))

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.projectile))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a\x89(\x18')  # 0x9a892818
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_static_geometry_test.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85\x01\x15\xe4')  # 0x850115e4
        data.write(b'\x00\x0c')  # size
        self.orbit_offset.to_stream(data)

        data.write(b'\xe7?\x12=')  # 0xe73f123d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.orbit_offset_local))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            collision_box=Vector.from_json(data['collision_box']),
            collision_offset=Vector.from_json(data['collision_offset']),
            mass=data['mass'],
            gravity=data['gravity'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            model=data['model'],
            collision_model=data['collision_model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            is_loop=data['is_loop'],
            immovable=data['immovable'],
            is_solid=data['is_solid'],
            is_camera_through=data['is_camera_through'],
            render_texture_set=data['render_texture_set'],
            draws_shadow=data['draws_shadow'],
            render_first_sorted=data['render_first_sorted'],
            scale_animation=data['scale_animation'],
            unknown_0xa09d4a1f=data['unknown_0xa09d4a1f'],
            is_phaazite=data['is_phaazite'],
            unknown_0xaa49b627=data['unknown_0xaa49b627'],
            use_mod_inca=data['use_mod_inca'],
            mod_inca_color=Color.from_json(data['mod_inca_color']),
            mod_inca_amount=Spline.from_json(data['mod_inca_amount']),
            random_animation_offset=data['random_animation_offset'],
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            projectile_static_geometry_test=StaticGeometryTest.from_json(data['projectile_static_geometry_test']),
            orbit_offset=Vector.from_json(data['orbit_offset']),
            orbit_offset_local=data['orbit_offset_local'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'mass': self.mass,
            'gravity': self.gravity,
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'model': self.model,
            'collision_model': self.collision_model,
            'character_animation_information': self.character_animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'is_loop': self.is_loop,
            'immovable': self.immovable,
            'is_solid': self.is_solid,
            'is_camera_through': self.is_camera_through,
            'render_texture_set': self.render_texture_set,
            'draws_shadow': self.draws_shadow,
            'render_first_sorted': self.render_first_sorted,
            'scale_animation': self.scale_animation,
            'unknown_0xa09d4a1f': self.unknown_0xa09d4a1f,
            'is_phaazite': self.is_phaazite,
            'unknown_0xaa49b627': self.unknown_0xaa49b627,
            'use_mod_inca': self.use_mod_inca,
            'mod_inca_color': self.mod_inca_color.to_json(),
            'mod_inca_amount': self.mod_inca_amount.to_json(),
            'random_animation_offset': self.random_animation_offset,
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'projectile_static_geometry_test': self.projectile_static_geometry_test.to_json(),
            'orbit_offset': self.orbit_offset.to_json(),
            'orbit_offset_local': self.orbit_offset_local,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_is_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_immovable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_solid(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_camera_through(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_draws_shadow(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_first_sorted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa09d4a1f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_phaazite(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xaa49b627(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_mod_inca(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_mod_inca_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_mod_inca_amount(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_random_animation_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_projectile_static_geometry_test(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


def _decode_orbit_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_orbit_offset_local(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0x75dbb375: ('mass', _decode_mass),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0xc27ffa8f: ('model', _decode_model),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xc08d1b93: ('is_loop', _decode_is_loop),
    0x1e32523e: ('immovable', _decode_immovable),
    0x1d8dd846: ('is_solid', _decode_is_solid),
    0x7859b520: ('is_camera_through', _decode_is_camera_through),
    0x32fab97e: ('render_texture_set', _decode_render_texture_set),
    0x97687446: ('draws_shadow', _decode_draws_shadow),
    0x4743294f: ('render_first_sorted', _decode_render_first_sorted),
    0x261e92a4: ('scale_animation', _decode_scale_animation),
    0xa09d4a1f: ('unknown_0xa09d4a1f', _decode_unknown_0xa09d4a1f),
    0xf3de9311: ('is_phaazite', _decode_is_phaazite),
    0xaa49b627: ('unknown_0xaa49b627', _decode_unknown_0xaa49b627),
    0xb530d7de: ('use_mod_inca', _decode_use_mod_inca),
    0xf8df6cd2: ('mod_inca_color', _decode_mod_inca_color),
    0xc23011d9: ('mod_inca_amount', _decode_mod_inca_amount),
    0xbf69c03e: ('random_animation_offset', _decode_random_animation_offset),
    0xef485db9: ('projectile', _decode_projectile),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0x9a892818: ('projectile_static_geometry_test', _decode_projectile_static_geometry_test),
    0x850115e4: ('orbit_offset', _decode_orbit_offset),
    0xe73f123d: ('orbit_offset_local', _decode_orbit_offset_local),
}
