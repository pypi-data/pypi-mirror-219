# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAlternateSkin import PlayerAlternateSkin
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType
from retro_data_structures.properties.dkc_returns.archetypes.ShadowData import ShadowData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct8 import UnknownStruct8
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class PlayerActor(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    mass: float = dataclasses.field(default=1.0)
    gravity: float = dataclasses.field(default=0.0)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    shadow_data: ShadowData = dataclasses.field(default_factory=ShadowData)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    is_loop: bool = dataclasses.field(default=True)
    unknown_0x87613768: bool = dataclasses.field(default=False)
    unknown_0xe2ddc4c1: str = dataclasses.field(default='')
    is_camera_through: bool = dataclasses.field(default=False)
    render_texture_set: int = dataclasses.field(default=0)
    render_push: float = dataclasses.field(default=0.0)
    render_first_sorted: bool = dataclasses.field(default=False)
    render_in_foreground: bool = dataclasses.field(default=False)
    ignore_fog: bool = dataclasses.field(default=False)
    scale_animation: bool = dataclasses.field(default=True)
    unknown_0xc1b9c601: bool = dataclasses.field(default=False)
    unknown_0x27e50799: bool = dataclasses.field(default=False)
    animation_offset: float = dataclasses.field(default=0.0)
    animation_time_scale: float = dataclasses.field(default=1.0)
    unknown_struct6_0xe1bcef23: PlayerType = dataclasses.field(default_factory=PlayerType)
    unknown_struct6_0x963e45f6: PlayerType = dataclasses.field(default_factory=PlayerType)
    unknown_struct8: UnknownStruct8 = dataclasses.field(default_factory=UnknownStruct8)
    alternate_skins: PlayerAlternateSkin = dataclasses.field(default_factory=PlayerAlternateSkin)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PLAC'

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
        data.write(b'\x00\x1d')  # 29 properties

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

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x81\xc8>')  # 0xbf81c83e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shadow_data.to_stream(data)
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

        data.write(b'\x87a7h')  # 0x87613768
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x87613768))

        data.write(b'\xe2\xdd\xc4\xc1')  # 0xe2ddc4c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xe2ddc4c1.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'xY\xb5 ')  # 0x7859b520
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_camera_through))

        data.write(b'2\xfa\xb9~')  # 0x32fab97e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_texture_set))

        data.write(b'\xaaq\x962')  # 0xaa719632
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.render_push))

        data.write(b'GC)O')  # 0x4743294f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_first_sorted))

        data.write(b'\xa6\xaa\x06\xd5')  # 0xa6aa06d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_in_foreground))

        data.write(b's\xe7\xbf\xe9')  # 0x73e7bfe9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_fog))

        data.write(b'&\x1e\x92\xa4')  # 0x261e92a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scale_animation))

        data.write(b'\xc1\xb9\xc6\x01')  # 0xc1b9c601
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc1b9c601))

        data.write(b"'\xe5\x07\x99")  # 0x27e50799
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x27e50799))

        data.write(b'"\xe0F\xba')  # 0x22e046ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_offset))

        data.write(b'\xbeQ>+')  # 0xbe513e2b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_time_scale))

        data.write(b'\xe1\xbc\xef#')  # 0xe1bcef23
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6_0xe1bcef23.to_stream(data, default_override={'character_type': enums.CharacterType.Unknown6})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96>E\xf6')  # 0x963e45f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6_0x963e45f6.to_stream(data, default_override={'character_type': enums.CharacterType.Unknown6})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'lu\xe2\xea')  # 0x6c75e2ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b".\x98'\xad")  # 0x2e9827ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.alternate_skins.to_stream(data)
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
            collision_box=Vector.from_json(data['collision_box']),
            collision_offset=Vector.from_json(data['collision_offset']),
            mass=data['mass'],
            gravity=data['gravity'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            model=data['model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            shadow_data=ShadowData.from_json(data['shadow_data']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            is_loop=data['is_loop'],
            unknown_0x87613768=data['unknown_0x87613768'],
            unknown_0xe2ddc4c1=data['unknown_0xe2ddc4c1'],
            is_camera_through=data['is_camera_through'],
            render_texture_set=data['render_texture_set'],
            render_push=data['render_push'],
            render_first_sorted=data['render_first_sorted'],
            render_in_foreground=data['render_in_foreground'],
            ignore_fog=data['ignore_fog'],
            scale_animation=data['scale_animation'],
            unknown_0xc1b9c601=data['unknown_0xc1b9c601'],
            unknown_0x27e50799=data['unknown_0x27e50799'],
            animation_offset=data['animation_offset'],
            animation_time_scale=data['animation_time_scale'],
            unknown_struct6_0xe1bcef23=PlayerType.from_json(data['unknown_struct6_0xe1bcef23']),
            unknown_struct6_0x963e45f6=PlayerType.from_json(data['unknown_struct6_0x963e45f6']),
            unknown_struct8=UnknownStruct8.from_json(data['unknown_struct8']),
            alternate_skins=PlayerAlternateSkin.from_json(data['alternate_skins']),
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
            'character_animation_information': self.character_animation_information.to_json(),
            'shadow_data': self.shadow_data.to_json(),
            'actor_information': self.actor_information.to_json(),
            'is_loop': self.is_loop,
            'unknown_0x87613768': self.unknown_0x87613768,
            'unknown_0xe2ddc4c1': self.unknown_0xe2ddc4c1,
            'is_camera_through': self.is_camera_through,
            'render_texture_set': self.render_texture_set,
            'render_push': self.render_push,
            'render_first_sorted': self.render_first_sorted,
            'render_in_foreground': self.render_in_foreground,
            'ignore_fog': self.ignore_fog,
            'scale_animation': self.scale_animation,
            'unknown_0xc1b9c601': self.unknown_0xc1b9c601,
            'unknown_0x27e50799': self.unknown_0x27e50799,
            'animation_offset': self.animation_offset,
            'animation_time_scale': self.animation_time_scale,
            'unknown_struct6_0xe1bcef23': self.unknown_struct6_0xe1bcef23.to_json(),
            'unknown_struct6_0x963e45f6': self.unknown_struct6_0x963e45f6.to_json(),
            'unknown_struct8': self.unknown_struct8.to_json(),
            'alternate_skins': self.alternate_skins.to_json(),
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


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_shadow_data(data: typing.BinaryIO, property_size: int):
    return ShadowData.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_is_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x87613768(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe2ddc4c1(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_is_camera_through(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_render_push(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_render_first_sorted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_in_foreground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_fog(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xc1b9c601(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x27e50799(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_animation_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation_time_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct6_0xe1bcef23(data: typing.BinaryIO, property_size: int):
    return PlayerType.from_stream(data, property_size, default_override={'character_type': enums.CharacterType.Unknown6})


def _decode_unknown_struct6_0x963e45f6(data: typing.BinaryIO, property_size: int):
    return PlayerType.from_stream(data, property_size, default_override={'character_type': enums.CharacterType.Unknown6})


def _decode_unknown_struct8(data: typing.BinaryIO, property_size: int):
    return UnknownStruct8.from_stream(data, property_size)


def _decode_alternate_skins(data: typing.BinaryIO, property_size: int):
    return PlayerAlternateSkin.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0x75dbb375: ('mass', _decode_mass),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xbf81c83e: ('shadow_data', _decode_shadow_data),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xc08d1b93: ('is_loop', _decode_is_loop),
    0x87613768: ('unknown_0x87613768', _decode_unknown_0x87613768),
    0xe2ddc4c1: ('unknown_0xe2ddc4c1', _decode_unknown_0xe2ddc4c1),
    0x7859b520: ('is_camera_through', _decode_is_camera_through),
    0x32fab97e: ('render_texture_set', _decode_render_texture_set),
    0xaa719632: ('render_push', _decode_render_push),
    0x4743294f: ('render_first_sorted', _decode_render_first_sorted),
    0xa6aa06d5: ('render_in_foreground', _decode_render_in_foreground),
    0x73e7bfe9: ('ignore_fog', _decode_ignore_fog),
    0x261e92a4: ('scale_animation', _decode_scale_animation),
    0xc1b9c601: ('unknown_0xc1b9c601', _decode_unknown_0xc1b9c601),
    0x27e50799: ('unknown_0x27e50799', _decode_unknown_0x27e50799),
    0x22e046ba: ('animation_offset', _decode_animation_offset),
    0xbe513e2b: ('animation_time_scale', _decode_animation_time_scale),
    0xe1bcef23: ('unknown_struct6_0xe1bcef23', _decode_unknown_struct6_0xe1bcef23),
    0x963e45f6: ('unknown_struct6_0x963e45f6', _decode_unknown_struct6_0x963e45f6),
    0x6c75e2ea: ('unknown_struct8', _decode_unknown_struct8),
    0x2e9827ad: ('alternate_skins', _decode_alternate_skins),
}
