# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.archetypes.SavedStateID import SavedStateID
from retro_data_structures.properties.corruption.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class Door(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    object_id: SavedStateID = dataclasses.field(default_factory=SavedStateID)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0xee808240: bool = dataclasses.field(default=False)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0x1b46b39b: bool = dataclasses.field(default=True)
    unknown_0x7ab4846d: bool = dataclasses.field(default=True)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    shell_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    blue_shell_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    shell_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=1.0, b=1.0, a=0.0))
    burn_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    orbit_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    is_open: bool = dataclasses.field(default=False)
    is_locked: bool = dataclasses.field(default=False)
    is_shield_down: bool = dataclasses.field(default=False)
    is_invulnerable: bool = dataclasses.field(default=False)
    open_animation_time: float = dataclasses.field(default=0.5)
    close_animation_time: float = dataclasses.field(default=0.5)
    close_delay: float = dataclasses.field(default=0.5)
    shield_fade_out_time: float = dataclasses.field(default=0.5)
    shield_fade_in_time: float = dataclasses.field(default=0.5)
    morph_ball_tunnel: bool = dataclasses.field(default=False)
    alt_scannable: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)
    locked_scannable: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DOOR'

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
        data.write(b'\x00\x1c')  # 28 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\xd9\xa7]')  # 0x16d9a75d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.object_id.to_stream(data)
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

        data.write(b'\xee\x80\x82@')  # 0xee808240
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xee808240))

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

        data.write(b'\x1bF\xb3\x9b')  # 0x1b46b39b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1b46b39b))

        data.write(b'z\xb4\x84m')  # 0x7ab4846d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7ab4846d))

        data.write(b'@D\xd9\xe5')  # 0x4044d9e5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\x0c\xc2q')  # 0xb20cc271
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shell_model))

        data.write(b'\xae[!\x14')  # 0xae5b2114
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.blue_shell_model))

        data.write(b'G\xb4\xe8c')  # 0x47b4e863
        data.write(b'\x00\x10')  # size
        self.shell_color.to_stream(data)

        data.write(b'%\x89\xc3\xf0')  # 0x2589c3f0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.burn_texture))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85\x01\x15\xe4')  # 0x850115e4
        data.write(b'\x00\x0c')  # size
        self.orbit_offset.to_stream(data)

        data.write(b'\xa1\xdf\xfa\xd2')  # 0xa1dffad2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_open))

        data.write(b'\xde\xe70\xf5')  # 0xdee730f5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_locked))

        data.write(b'2\x1f\xae[')  # 0x321fae5b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_shield_down))

        data.write(b'\x98R\xc4\xb5')  # 0x9852c4b5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_invulnerable))

        data.write(b' \x07\xb7\x1d')  # 0x2007b71d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.open_animation_time))

        data.write(b'\xf1\xa5\r)')  # 0xf1a50d29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.close_animation_time))

        data.write(b'\x06\xdc\xf1\x18')  # 0x6dcf118
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.close_delay))

        data.write(b']\xcf\nd')  # 0x5dcf0a64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shield_fade_out_time))

        data.write(b'\xcd\xcaY+')  # 0xcdca592b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shield_fade_in_time))

        data.write(b'\xcc\x00\x9f5')  # 0xcc009f35
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.morph_ball_tunnel))

        data.write(b"\x9e\xc6'\x12")  # 0x9ec62712
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.alt_scannable.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'qw\xaf\xcc')  # 0x7177afcc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.locked_scannable.to_stream(data)
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
            object_id=SavedStateID.from_json(data['object_id']),
            collision_box=Vector.from_json(data['collision_box']),
            collision_offset=Vector.from_json(data['collision_offset']),
            unknown_0xee808240=data['unknown_0xee808240'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            unknown_0x1b46b39b=data['unknown_0x1b46b39b'],
            unknown_0x7ab4846d=data['unknown_0x7ab4846d'],
            animation_information=AnimationParameters.from_json(data['animation_information']),
            shell_model=data['shell_model'],
            blue_shell_model=data['blue_shell_model'],
            shell_color=Color.from_json(data['shell_color']),
            burn_texture=data['burn_texture'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            orbit_offset=Vector.from_json(data['orbit_offset']),
            is_open=data['is_open'],
            is_locked=data['is_locked'],
            is_shield_down=data['is_shield_down'],
            is_invulnerable=data['is_invulnerable'],
            open_animation_time=data['open_animation_time'],
            close_animation_time=data['close_animation_time'],
            close_delay=data['close_delay'],
            shield_fade_out_time=data['shield_fade_out_time'],
            shield_fade_in_time=data['shield_fade_in_time'],
            morph_ball_tunnel=data['morph_ball_tunnel'],
            alt_scannable=ScannableParameters.from_json(data['alt_scannable']),
            locked_scannable=ScannableParameters.from_json(data['locked_scannable']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'object_id': self.object_id.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'unknown_0xee808240': self.unknown_0xee808240,
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'unknown_0x1b46b39b': self.unknown_0x1b46b39b,
            'unknown_0x7ab4846d': self.unknown_0x7ab4846d,
            'animation_information': self.animation_information.to_json(),
            'shell_model': self.shell_model,
            'blue_shell_model': self.blue_shell_model,
            'shell_color': self.shell_color.to_json(),
            'burn_texture': self.burn_texture,
            'actor_information': self.actor_information.to_json(),
            'orbit_offset': self.orbit_offset.to_json(),
            'is_open': self.is_open,
            'is_locked': self.is_locked,
            'is_shield_down': self.is_shield_down,
            'is_invulnerable': self.is_invulnerable,
            'open_animation_time': self.open_animation_time,
            'close_animation_time': self.close_animation_time,
            'close_delay': self.close_delay,
            'shield_fade_out_time': self.shield_fade_out_time,
            'shield_fade_in_time': self.shield_fade_in_time,
            'morph_ball_tunnel': self.morph_ball_tunnel,
            'alt_scannable': self.alt_scannable.to_json(),
            'locked_scannable': self.locked_scannable.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_object_id(data: typing.BinaryIO, property_size: int):
    return SavedStateID.from_stream(data, property_size)


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0xee808240(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0x1b46b39b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7ab4846d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_shell_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_blue_shell_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shell_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_burn_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_orbit_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_is_open(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_locked(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_shield_down(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_invulnerable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_open_animation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_close_animation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_close_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shield_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shield_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morph_ball_tunnel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_alt_scannable(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


def _decode_locked_scannable(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x16d9a75d: ('object_id', _decode_object_id),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xee808240: ('unknown_0xee808240', _decode_unknown_0xee808240),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x1b46b39b: ('unknown_0x1b46b39b', _decode_unknown_0x1b46b39b),
    0x7ab4846d: ('unknown_0x7ab4846d', _decode_unknown_0x7ab4846d),
    0x4044d9e5: ('animation_information', _decode_animation_information),
    0xb20cc271: ('shell_model', _decode_shell_model),
    0xae5b2114: ('blue_shell_model', _decode_blue_shell_model),
    0x47b4e863: ('shell_color', _decode_shell_color),
    0x2589c3f0: ('burn_texture', _decode_burn_texture),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x850115e4: ('orbit_offset', _decode_orbit_offset),
    0xa1dffad2: ('is_open', _decode_is_open),
    0xdee730f5: ('is_locked', _decode_is_locked),
    0x321fae5b: ('is_shield_down', _decode_is_shield_down),
    0x9852c4b5: ('is_invulnerable', _decode_is_invulnerable),
    0x2007b71d: ('open_animation_time', _decode_open_animation_time),
    0xf1a50d29: ('close_animation_time', _decode_close_animation_time),
    0x6dcf118: ('close_delay', _decode_close_delay),
    0x5dcf0a64: ('shield_fade_out_time', _decode_shield_fade_out_time),
    0xcdca592b: ('shield_fade_in_time', _decode_shield_fade_in_time),
    0xcc009f35: ('morph_ball_tunnel', _decode_morph_ball_tunnel),
    0x9ec62712: ('alt_scannable', _decode_alt_scannable),
    0x7177afcc: ('locked_scannable', _decode_locked_scannable),
}
