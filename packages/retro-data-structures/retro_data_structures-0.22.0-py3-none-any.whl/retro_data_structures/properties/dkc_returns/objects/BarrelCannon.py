# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.BarrelCannonData import BarrelCannonData
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.dkc_returns.archetypes.PlatformMotionProperties import PlatformMotionProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct22 import UnknownStruct22
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class BarrelCannon(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    fsmc: AssetId = dataclasses.field(metadata={'asset_types': ['FSMC']}, default=default_asset_id)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    maximum_splashes: int = dataclasses.field(default=200)
    splash_generation_rate: int = dataclasses.field(default=20)
    render_rain_splashes: bool = dataclasses.field(default=False)
    unknown_0xf203bc81: bool = dataclasses.field(default=False)
    motion_properties: PlatformMotionProperties = dataclasses.field(default_factory=PlatformMotionProperties)
    unknown_0x24fdeea1: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.15000000596046448, z=0.0))
    random_animation_offset: float = dataclasses.field(default=0.0)
    unknown_0x6b5e87a7: float = dataclasses.field(default=1800.0)
    look_at_velocity: float = dataclasses.field(default=30.0)
    barrel_cannon_data: BarrelCannonData = dataclasses.field(default_factory=BarrelCannonData)
    unknown_0xfaf13d08: bool = dataclasses.field(default=False)
    unknown_struct22: UnknownStruct22 = dataclasses.field(default_factory=UnknownStruct22)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'BARL'

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
        data.write(b'\x00\x15')  # 21 properties

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

        data.write(b'\x1b!\xee\xb2')  # 0x1b21eeb2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fsmc))

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

        data.write(b'\xdc\xd5o\xe8')  # 0xdcd56fe8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.maximum_splashes))

        data.write(b'h-\xe1\\')  # 0x682de15c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.splash_generation_rate))

        data.write(b'\xac:\xdd\xa6')  # 0xac3adda6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_rain_splashes))

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

        data.write(b'k^\x87\xa7')  # 0x6b5e87a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6b5e87a7))

        data.write(b'=\xc7W3')  # 0x3dc75733
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_at_velocity))

        data.write(b'\xf0La\xf3')  # 0xf04c61f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.barrel_cannon_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xf1=\x08')  # 0xfaf13d08
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xfaf13d08))

        data.write(b'\xc9\xd2%\xc7')  # 0xc9d225c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct22.to_stream(data)
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
            fsmc=data['fsmc'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            collision_model=data['collision_model'],
            health=HealthInfo.from_json(data['health']),
            maximum_splashes=data['maximum_splashes'],
            splash_generation_rate=data['splash_generation_rate'],
            render_rain_splashes=data['render_rain_splashes'],
            unknown_0xf203bc81=data['unknown_0xf203bc81'],
            motion_properties=PlatformMotionProperties.from_json(data['motion_properties']),
            unknown_0x24fdeea1=Vector.from_json(data['unknown_0x24fdeea1']),
            random_animation_offset=data['random_animation_offset'],
            unknown_0x6b5e87a7=data['unknown_0x6b5e87a7'],
            look_at_velocity=data['look_at_velocity'],
            barrel_cannon_data=BarrelCannonData.from_json(data['barrel_cannon_data']),
            unknown_0xfaf13d08=data['unknown_0xfaf13d08'],
            unknown_struct22=UnknownStruct22.from_json(data['unknown_struct22']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'model': self.model,
            'animation': self.animation.to_json(),
            'fsmc': self.fsmc,
            'actor_information': self.actor_information.to_json(),
            'collision_model': self.collision_model,
            'health': self.health.to_json(),
            'maximum_splashes': self.maximum_splashes,
            'splash_generation_rate': self.splash_generation_rate,
            'render_rain_splashes': self.render_rain_splashes,
            'unknown_0xf203bc81': self.unknown_0xf203bc81,
            'motion_properties': self.motion_properties.to_json(),
            'unknown_0x24fdeea1': self.unknown_0x24fdeea1.to_json(),
            'random_animation_offset': self.random_animation_offset,
            'unknown_0x6b5e87a7': self.unknown_0x6b5e87a7,
            'look_at_velocity': self.look_at_velocity,
            'barrel_cannon_data': self.barrel_cannon_data.to_json(),
            'unknown_0xfaf13d08': self.unknown_0xfaf13d08,
            'unknown_struct22': self.unknown_struct22.to_json(),
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


def _decode_fsmc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_maximum_splashes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_splash_generation_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_render_rain_splashes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf203bc81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_motion_properties(data: typing.BinaryIO, property_size: int):
    return PlatformMotionProperties.from_stream(data, property_size)


def _decode_unknown_0x24fdeea1(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_random_animation_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6b5e87a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_at_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_barrel_cannon_data(data: typing.BinaryIO, property_size: int):
    return BarrelCannonData.from_stream(data, property_size)


def _decode_unknown_0xfaf13d08(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct22(data: typing.BinaryIO, property_size: int):
    return UnknownStruct22.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc27ffa8f: ('model', _decode_model),
    0xa3d63f44: ('animation', _decode_animation),
    0x1b21eeb2: ('fsmc', _decode_fsmc),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xcf90d15e: ('health', _decode_health),
    0xdcd56fe8: ('maximum_splashes', _decode_maximum_splashes),
    0x682de15c: ('splash_generation_rate', _decode_splash_generation_rate),
    0xac3adda6: ('render_rain_splashes', _decode_render_rain_splashes),
    0xf203bc81: ('unknown_0xf203bc81', _decode_unknown_0xf203bc81),
    0xa9dbf91: ('motion_properties', _decode_motion_properties),
    0x24fdeea1: ('unknown_0x24fdeea1', _decode_unknown_0x24fdeea1),
    0xbf69c03e: ('random_animation_offset', _decode_random_animation_offset),
    0x6b5e87a7: ('unknown_0x6b5e87a7', _decode_unknown_0x6b5e87a7),
    0x3dc75733: ('look_at_velocity', _decode_look_at_velocity),
    0xf04c61f3: ('barrel_cannon_data', _decode_barrel_cannon_data),
    0xfaf13d08: ('unknown_0xfaf13d08', _decode_unknown_0xfaf13d08),
    0xc9d225c7: ('unknown_struct22', _decode_unknown_struct22),
}
