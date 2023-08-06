# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SporbNeedle(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    initial_speed: float = dataclasses.field(default=60.0)
    mass: float = dataclasses.field(default=1.0)
    attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    fuse_time: float = dataclasses.field(default=1.5)
    trail_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    explosion_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    launch_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    flight_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    hit_player_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    collision_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    explosion_sound: int = dataclasses.field(default=0, metadata={'sound': True})

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPBN'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Sporb.rel']

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
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

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.model))

        data.write(b'\xcb\x14\xd9|')  # 0xcb14d97c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_speed))

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'f\xdc\xaa\xcb')  # 0x66dcaacb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_damage.to_stream(data, default_override={'di_weapon_type': 9, 'di_damage': 5.0, 'di_knock_back_power': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\xc1K\x87')  # 0x5cc14b87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fuse_time))

        data.write(b'6\xee\xe7\x91')  # 0x36eee791
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.trail_effect))

        data.write(b'\xf8\xb7\xba&')  # 0xf8b7ba26
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.explosion_effect))

        data.write(b'\r\xd6ow')  # 0xdd66f77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.launch_sound))

        data.write(b'\x1b\xc7\xf2\xfc')  # 0x1bc7f2fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flight_sound))

        data.write(b'\xdf\xbd\x90\xe1')  # 0xdfbd90e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.hit_player_sound))

        data.write(b'\x92\xca\xa9}')  # 0x92caa97d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.collision_sound))

        data.write(b'`(\xd1\xcc')  # 0x6028d1cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.explosion_sound))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            model=data['model'],
            initial_speed=data['initial_speed'],
            mass=data['mass'],
            attack_damage=DamageInfo.from_json(data['attack_damage']),
            fuse_time=data['fuse_time'],
            trail_effect=data['trail_effect'],
            explosion_effect=data['explosion_effect'],
            launch_sound=data['launch_sound'],
            flight_sound=data['flight_sound'],
            hit_player_sound=data['hit_player_sound'],
            collision_sound=data['collision_sound'],
            explosion_sound=data['explosion_sound'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'model': self.model,
            'initial_speed': self.initial_speed,
            'mass': self.mass,
            'attack_damage': self.attack_damage.to_json(),
            'fuse_time': self.fuse_time,
            'trail_effect': self.trail_effect,
            'explosion_effect': self.explosion_effect,
            'launch_sound': self.launch_sound,
            'flight_sound': self.flight_sound,
            'hit_player_sound': self.hit_player_sound,
            'collision_sound': self.collision_sound,
            'explosion_sound': self.explosion_sound,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_attack_damage(self, asset_manager):
        yield from self.attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_trail_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.trail_effect)

    def _dependencies_for_explosion_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.explosion_effect)

    def _dependencies_for_launch_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.launch_sound)

    def _dependencies_for_flight_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.flight_sound)

    def _dependencies_for_hit_player_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.hit_player_sound)

    def _dependencies_for_collision_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.collision_sound)

    def _dependencies_for_explosion_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.explosion_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_attack_damage, "attack_damage", "DamageInfo"),
            (self._dependencies_for_trail_effect, "trail_effect", "AssetId"),
            (self._dependencies_for_explosion_effect, "explosion_effect", "AssetId"),
            (self._dependencies_for_launch_sound, "launch_sound", "int"),
            (self._dependencies_for_flight_sound, "flight_sound", "int"),
            (self._dependencies_for_hit_player_sound, "hit_player_sound", "int"),
            (self._dependencies_for_collision_sound, "collision_sound", "int"),
            (self._dependencies_for_explosion_sound, "explosion_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SporbNeedle.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_initial_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 9, 'di_damage': 5.0, 'di_knock_back_power': 2.0})


def _decode_fuse_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_trail_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_explosion_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_launch_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hit_player_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_collision_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_explosion_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xc27ffa8f: ('model', _decode_model),
    0xcb14d97c: ('initial_speed', _decode_initial_speed),
    0x75dbb375: ('mass', _decode_mass),
    0x66dcaacb: ('attack_damage', _decode_attack_damage),
    0x5cc14b87: ('fuse_time', _decode_fuse_time),
    0x36eee791: ('trail_effect', _decode_trail_effect),
    0xf8b7ba26: ('explosion_effect', _decode_explosion_effect),
    0xdd66f77: ('launch_sound', _decode_launch_sound),
    0x1bc7f2fc: ('flight_sound', _decode_flight_sound),
    0xdfbd90e1: ('hit_player_sound', _decode_hit_player_sound),
    0x92caa97d: ('collision_sound', _decode_collision_sound),
    0x6028d1cc: ('explosion_sound', _decode_explosion_sound),
}
