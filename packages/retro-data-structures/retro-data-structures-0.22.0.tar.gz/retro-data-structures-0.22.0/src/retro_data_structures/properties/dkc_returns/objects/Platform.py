# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.dkc_returns.archetypes.PlatformMotionProperties import PlatformMotionProperties
from retro_data_structures.properties.dkc_returns.archetypes.ShadowData import ShadowData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct245 import UnknownStruct245
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class Platform(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    shadow_data: ShadowData = dataclasses.field(default_factory=ShadowData)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xf203bc81: bool = dataclasses.field(default=False)
    motion_properties: PlatformMotionProperties = dataclasses.field(default_factory=PlatformMotionProperties)
    unknown_0x24fdeea1: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.15000000596046448, z=0.0))
    random_animation_offset: float = dataclasses.field(default=0.0)
    animation_time_scale: float = dataclasses.field(default=1.0)
    unknown_0x6b5e87a7: float = dataclasses.field(default=1800.0)
    look_at_velocity: float = dataclasses.field(default=30.0)
    render_push: float = dataclasses.field(default=0.0)
    unknown_0x981c2921: float = dataclasses.field(default=0.0)
    unknown_0xb5b16553: bool = dataclasses.field(default=False)
    unknown_0x58ee3422: bool = dataclasses.field(default=False)
    unknown_0xbe04e10b: bool = dataclasses.field(default=False)
    can_take_damage: bool = dataclasses.field(default=False)
    unknown_0x47e9cc80: bool = dataclasses.field(default=False)
    unknown_struct245: UnknownStruct245 = dataclasses.field(default_factory=UnknownStruct245)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PLAT'

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
        data.write(b'\x00\x19')  # 25 properties

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

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
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

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

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

        data.write(b'\xf2\x03\xbc\x81')  # 0xf203bc81
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf203bc81))

        data.write(b'\n\x9d\xbf\x91')  # 0xa9dbf91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xfd\xee\xa1')  # 0x24fdeea1
        data.write(b'\x00\x0c')  # size
        self.unknown_0x24fdeea1.to_stream(data)

        data.write(b'\xbfi\xc0>')  # 0xbf69c03e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_animation_offset))

        data.write(b'\xbeQ>+')  # 0xbe513e2b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_time_scale))

        data.write(b'k^\x87\xa7')  # 0x6b5e87a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6b5e87a7))

        data.write(b'=\xc7W3')  # 0x3dc75733
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_at_velocity))

        data.write(b'\xaaq\x962')  # 0xaa719632
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.render_push))

        data.write(b'\x98\x1c)!')  # 0x981c2921
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x981c2921))

        data.write(b'\xb5\xb1eS')  # 0xb5b16553
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb5b16553))

        data.write(b'X\xee4"')  # 0x58ee3422
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x58ee3422))

        data.write(b'\xbe\x04\xe1\x0b')  # 0xbe04e10b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbe04e10b))

        data.write(b'\x1f\xa9*\xc4')  # 0x1fa92ac4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_take_damage))

        data.write(b'G\xe9\xcc\x80')  # 0x47e9cc80
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x47e9cc80))

        data.write(b"\xa1\x17'D")  # 0xa1172744
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct245.to_stream(data)
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
            model=data['model'],
            animation=AnimationParameters.from_json(data['animation']),
            shadow_data=ShadowData.from_json(data['shadow_data']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            collision_model=data['collision_model'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            unknown_0xf203bc81=data['unknown_0xf203bc81'],
            motion_properties=PlatformMotionProperties.from_json(data['motion_properties']),
            unknown_0x24fdeea1=Vector.from_json(data['unknown_0x24fdeea1']),
            random_animation_offset=data['random_animation_offset'],
            animation_time_scale=data['animation_time_scale'],
            unknown_0x6b5e87a7=data['unknown_0x6b5e87a7'],
            look_at_velocity=data['look_at_velocity'],
            render_push=data['render_push'],
            unknown_0x981c2921=data['unknown_0x981c2921'],
            unknown_0xb5b16553=data['unknown_0xb5b16553'],
            unknown_0x58ee3422=data['unknown_0x58ee3422'],
            unknown_0xbe04e10b=data['unknown_0xbe04e10b'],
            can_take_damage=data['can_take_damage'],
            unknown_0x47e9cc80=data['unknown_0x47e9cc80'],
            unknown_struct245=UnknownStruct245.from_json(data['unknown_struct245']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'model': self.model,
            'animation': self.animation.to_json(),
            'shadow_data': self.shadow_data.to_json(),
            'actor_information': self.actor_information.to_json(),
            'collision_model': self.collision_model,
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'unknown_0xf203bc81': self.unknown_0xf203bc81,
            'motion_properties': self.motion_properties.to_json(),
            'unknown_0x24fdeea1': self.unknown_0x24fdeea1.to_json(),
            'random_animation_offset': self.random_animation_offset,
            'animation_time_scale': self.animation_time_scale,
            'unknown_0x6b5e87a7': self.unknown_0x6b5e87a7,
            'look_at_velocity': self.look_at_velocity,
            'render_push': self.render_push,
            'unknown_0x981c2921': self.unknown_0x981c2921,
            'unknown_0xb5b16553': self.unknown_0xb5b16553,
            'unknown_0x58ee3422': self.unknown_0x58ee3422,
            'unknown_0xbe04e10b': self.unknown_0xbe04e10b,
            'can_take_damage': self.can_take_damage,
            'unknown_0x47e9cc80': self.unknown_0x47e9cc80,
            'unknown_struct245': self.unknown_struct245.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_shadow_data(data: typing.BinaryIO, property_size: int):
    return ShadowData.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xf203bc81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_motion_properties(data: typing.BinaryIO, property_size: int):
    return PlatformMotionProperties.from_stream(data, property_size)


def _decode_unknown_0x24fdeea1(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_random_animation_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation_time_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6b5e87a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_at_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_render_push(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x981c2921(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb5b16553(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x58ee3422(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbe04e10b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_take_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x47e9cc80(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct245(data: typing.BinaryIO, property_size: int):
    return UnknownStruct245.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc27ffa8f: ('model', _decode_model),
    0xa3d63f44: ('animation', _decode_animation),
    0xbf81c83e: ('shadow_data', _decode_shadow_data),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0xf203bc81: ('unknown_0xf203bc81', _decode_unknown_0xf203bc81),
    0xa9dbf91: ('motion_properties', _decode_motion_properties),
    0x24fdeea1: ('unknown_0x24fdeea1', _decode_unknown_0x24fdeea1),
    0xbf69c03e: ('random_animation_offset', _decode_random_animation_offset),
    0xbe513e2b: ('animation_time_scale', _decode_animation_time_scale),
    0x6b5e87a7: ('unknown_0x6b5e87a7', _decode_unknown_0x6b5e87a7),
    0x3dc75733: ('look_at_velocity', _decode_look_at_velocity),
    0xaa719632: ('render_push', _decode_render_push),
    0x981c2921: ('unknown_0x981c2921', _decode_unknown_0x981c2921),
    0xb5b16553: ('unknown_0xb5b16553', _decode_unknown_0xb5b16553),
    0x58ee3422: ('unknown_0x58ee3422', _decode_unknown_0x58ee3422),
    0xbe04e10b: ('unknown_0xbe04e10b', _decode_unknown_0xbe04e10b),
    0x1fa92ac4: ('can_take_damage', _decode_can_take_damage),
    0x47e9cc80: ('unknown_0x47e9cc80', _decode_unknown_0x47e9cc80),
    0xa1172744: ('unknown_struct245', _decode_unknown_struct245),
}
