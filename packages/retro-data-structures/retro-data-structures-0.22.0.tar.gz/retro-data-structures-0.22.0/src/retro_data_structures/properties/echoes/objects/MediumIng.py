# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.CameraShakerData import CameraShakerData
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class MediumIng(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    spawn_mode: int = dataclasses.field(default=0)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    aggressiveness: float = dataclasses.field(default=50.0)
    unknown_0x4d1d840d: float = dataclasses.field(default=4.0)
    min_melee_attack_interval: float = dataclasses.field(default=10.0)
    max_melee_attack_range: float = dataclasses.field(default=20.0)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x636f11e5: float = dataclasses.field(default=10.0)
    mist_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    min_mist_attack_interval: float = dataclasses.field(default=10.0)
    misting_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    min_arm_attack_interval: float = dataclasses.field(default=2.0)
    unknown_0x9d3cfeb0: float = dataclasses.field(default=15.0)
    unknown_0xdc2bc136: float = dataclasses.field(default=30.0)
    min_tentacle_length: float = dataclasses.field(default=5.0)
    max_tentacle_length: float = dataclasses.field(default=40.0)
    arm_attack_time: float = dataclasses.field(default=1.0)
    unknown_0x8f1d597c: float = dataclasses.field(default=0.5)
    attack_tentacle: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_parameters: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    attack_motion: Spline = dataclasses.field(default_factory=Spline)
    camera_shaker_data: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)
    attack_tentacle_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    taunt_chance: float = dataclasses.field(default=25.0)
    double_dash_chance: float = dataclasses.field(default=25.0)
    light_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    light_attenuation: float = dataclasses.field(default=2.0)
    unknown_0xb459c3e9: Spline = dataclasses.field(default_factory=Spline)
    dash_speed: Spline = dataclasses.field(default_factory=Spline)
    ing_spot_blob_fx: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ing_spot_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x0e3d3708: float = dataclasses.field(default=50.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'MING'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['GeomBlobV2.rel', 'MediumIng.rel']

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
        data.write(b'\x00"')  # 34 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'turn_speed': 360.0, 'creature_size': 1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9j\xe3\xdf')  # 0xc96ae3df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.spawn_mode))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95y\xb1\xf2')  # 0x9579b1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aggressiveness))

        data.write(b'M\x1d\x84\r')  # 0x4d1d840d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4d1d840d))

        data.write(b'\xd1\x89\xa7\xaa')  # 0xd189a7aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_melee_attack_interval))

        data.write(b'\xf3\xea-\xef')  # 0xf3ea2def
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_melee_attack_range))

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'co\x11\xe5')  # 0x636f11e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x636f11e5))

        data.write(b'\xd2%D0')  # 0xd2254430
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mist_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\x87\xf4\x12')  # 0xb787f412
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_mist_attack_interval))

        data.write(b'I\xc8\xd0\xc7')  # 0x49c8d0c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misting_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15)I\x00')  # 0x15294900
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_arm_attack_interval))

        data.write(b'\x9d<\xfe\xb0')  # 0x9d3cfeb0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9d3cfeb0))

        data.write(b'\xdc+\xc16')  # 0xdc2bc136
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdc2bc136))

        data.write(b't\xff\xed\x99')  # 0x74ffed99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_tentacle_length))

        data.write(b'5\xe8\xd2\x1f')  # 0x35e8d21f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_tentacle_length))

        data.write(b'\xb95s\xf7')  # 0xb93573f7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arm_attack_time))

        data.write(b'\x8f\x1dY|')  # 0x8f1d597c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f1d597c))

        data.write(b'z\x9f\x82I')  # 0x7a9f8249
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_tentacle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'8\xcf\x13;')  # 0x38cf133b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07g\x06\r')  # 0x767060d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0ek\x1ep')  # 0xe6b1e70
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_shaker_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\x83\xfe\x08')  # 0xf683fe08
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_tentacle_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x7fb\x12')  # 0xa77f6212
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_chance))

        data.write(b'\x9c\xf0\x14s')  # 0x9cf01473
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.double_dash_chance))

        data.write(b'\xbd>\xfe}')  # 0xbd3efe7d
        data.write(b'\x00\x10')  # size
        self.light_color.to_stream(data)

        data.write(b'\xd2K\x88\x8f')  # 0xd24b888f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.light_attenuation))

        data.write(b'\xb4Y\xc3\xe9')  # 0xb459c3e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb459c3e9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2>N\xd0')  # 0x323e4ed0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dash_speed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07\x9b\xc5v')  # 0x79bc576
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ing_spot_blob_fx))

        data.write(b'|\xb6<\xd3')  # 0x7cb63cd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.ing_spot_sound))

        data.write(b'\x0e=7\x08')  # 0xe3d3708
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0e3d3708))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            spawn_mode=data['spawn_mode'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            aggressiveness=data['aggressiveness'],
            unknown_0x4d1d840d=data['unknown_0x4d1d840d'],
            min_melee_attack_interval=data['min_melee_attack_interval'],
            max_melee_attack_range=data['max_melee_attack_range'],
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            unknown_0x636f11e5=data['unknown_0x636f11e5'],
            mist_damage=DamageInfo.from_json(data['mist_damage']),
            min_mist_attack_interval=data['min_mist_attack_interval'],
            misting_vulnerability=DamageVulnerability.from_json(data['misting_vulnerability']),
            min_arm_attack_interval=data['min_arm_attack_interval'],
            unknown_0x9d3cfeb0=data['unknown_0x9d3cfeb0'],
            unknown_0xdc2bc136=data['unknown_0xdc2bc136'],
            min_tentacle_length=data['min_tentacle_length'],
            max_tentacle_length=data['max_tentacle_length'],
            arm_attack_time=data['arm_attack_time'],
            unknown_0x8f1d597c=data['unknown_0x8f1d597c'],
            attack_tentacle=AnimationParameters.from_json(data['attack_tentacle']),
            actor_parameters=ActorParameters.from_json(data['actor_parameters']),
            attack_motion=Spline.from_json(data['attack_motion']),
            camera_shaker_data=CameraShakerData.from_json(data['camera_shaker_data']),
            attack_tentacle_damage=DamageInfo.from_json(data['attack_tentacle_damage']),
            taunt_chance=data['taunt_chance'],
            double_dash_chance=data['double_dash_chance'],
            light_color=Color.from_json(data['light_color']),
            light_attenuation=data['light_attenuation'],
            unknown_0xb459c3e9=Spline.from_json(data['unknown_0xb459c3e9']),
            dash_speed=Spline.from_json(data['dash_speed']),
            ing_spot_blob_fx=data['ing_spot_blob_fx'],
            ing_spot_sound=data['ing_spot_sound'],
            unknown_0x0e3d3708=data['unknown_0x0e3d3708'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'spawn_mode': self.spawn_mode,
            'actor_information': self.actor_information.to_json(),
            'aggressiveness': self.aggressiveness,
            'unknown_0x4d1d840d': self.unknown_0x4d1d840d,
            'min_melee_attack_interval': self.min_melee_attack_interval,
            'max_melee_attack_range': self.max_melee_attack_range,
            'melee_damage': self.melee_damage.to_json(),
            'unknown_0x636f11e5': self.unknown_0x636f11e5,
            'mist_damage': self.mist_damage.to_json(),
            'min_mist_attack_interval': self.min_mist_attack_interval,
            'misting_vulnerability': self.misting_vulnerability.to_json(),
            'min_arm_attack_interval': self.min_arm_attack_interval,
            'unknown_0x9d3cfeb0': self.unknown_0x9d3cfeb0,
            'unknown_0xdc2bc136': self.unknown_0xdc2bc136,
            'min_tentacle_length': self.min_tentacle_length,
            'max_tentacle_length': self.max_tentacle_length,
            'arm_attack_time': self.arm_attack_time,
            'unknown_0x8f1d597c': self.unknown_0x8f1d597c,
            'attack_tentacle': self.attack_tentacle.to_json(),
            'actor_parameters': self.actor_parameters.to_json(),
            'attack_motion': self.attack_motion.to_json(),
            'camera_shaker_data': self.camera_shaker_data.to_json(),
            'attack_tentacle_damage': self.attack_tentacle_damage.to_json(),
            'taunt_chance': self.taunt_chance,
            'double_dash_chance': self.double_dash_chance,
            'light_color': self.light_color.to_json(),
            'light_attenuation': self.light_attenuation,
            'unknown_0xb459c3e9': self.unknown_0xb459c3e9.to_json(),
            'dash_speed': self.dash_speed.to_json(),
            'ing_spot_blob_fx': self.ing_spot_blob_fx,
            'ing_spot_sound': self.ing_spot_sound,
            'unknown_0x0e3d3708': self.unknown_0x0e3d3708,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_melee_damage(self, asset_manager):
        yield from self.melee_damage.dependencies_for(asset_manager)

    def _dependencies_for_mist_damage(self, asset_manager):
        yield from self.mist_damage.dependencies_for(asset_manager)

    def _dependencies_for_misting_vulnerability(self, asset_manager):
        yield from self.misting_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_attack_tentacle(self, asset_manager):
        yield from self.attack_tentacle.dependencies_for(asset_manager)

    def _dependencies_for_actor_parameters(self, asset_manager):
        yield from self.actor_parameters.dependencies_for(asset_manager)

    def _dependencies_for_camera_shaker_data(self, asset_manager):
        yield from self.camera_shaker_data.dependencies_for(asset_manager)

    def _dependencies_for_attack_tentacle_damage(self, asset_manager):
        yield from self.attack_tentacle_damage.dependencies_for(asset_manager)

    def _dependencies_for_ing_spot_blob_fx(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ing_spot_blob_fx)

    def _dependencies_for_ing_spot_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.ing_spot_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_melee_damage, "melee_damage", "DamageInfo"),
            (self._dependencies_for_mist_damage, "mist_damage", "DamageInfo"),
            (self._dependencies_for_misting_vulnerability, "misting_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_attack_tentacle, "attack_tentacle", "AnimationParameters"),
            (self._dependencies_for_actor_parameters, "actor_parameters", "ActorParameters"),
            (self._dependencies_for_camera_shaker_data, "camera_shaker_data", "CameraShakerData"),
            (self._dependencies_for_attack_tentacle_damage, "attack_tentacle_damage", "DamageInfo"),
            (self._dependencies_for_ing_spot_blob_fx, "ing_spot_blob_fx", "AssetId"),
            (self._dependencies_for_ing_spot_sound, "ing_spot_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for MediumIng.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'turn_speed': 360.0, 'creature_size': 1})


def _decode_spawn_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_aggressiveness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4d1d840d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_melee_attack_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_melee_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x636f11e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mist_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_min_mist_attack_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_misting_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_min_arm_attack_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9d3cfeb0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdc2bc136(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_tentacle_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_tentacle_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arm_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f1d597c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_tentacle(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_parameters(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_attack_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_camera_shaker_data(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


def _decode_attack_tentacle_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_taunt_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_double_dash_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_light_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_light_attenuation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb459c3e9(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_dash_speed(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_ing_spot_blob_fx(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_spot_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x0e3d3708(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0xc96ae3df: ('spawn_mode', _decode_spawn_mode),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x9579b1f2: ('aggressiveness', _decode_aggressiveness),
    0x4d1d840d: ('unknown_0x4d1d840d', _decode_unknown_0x4d1d840d),
    0xd189a7aa: ('min_melee_attack_interval', _decode_min_melee_attack_interval),
    0xf3ea2def: ('max_melee_attack_range', _decode_max_melee_attack_range),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x636f11e5: ('unknown_0x636f11e5', _decode_unknown_0x636f11e5),
    0xd2254430: ('mist_damage', _decode_mist_damage),
    0xb787f412: ('min_mist_attack_interval', _decode_min_mist_attack_interval),
    0x49c8d0c7: ('misting_vulnerability', _decode_misting_vulnerability),
    0x15294900: ('min_arm_attack_interval', _decode_min_arm_attack_interval),
    0x9d3cfeb0: ('unknown_0x9d3cfeb0', _decode_unknown_0x9d3cfeb0),
    0xdc2bc136: ('unknown_0xdc2bc136', _decode_unknown_0xdc2bc136),
    0x74ffed99: ('min_tentacle_length', _decode_min_tentacle_length),
    0x35e8d21f: ('max_tentacle_length', _decode_max_tentacle_length),
    0xb93573f7: ('arm_attack_time', _decode_arm_attack_time),
    0x8f1d597c: ('unknown_0x8f1d597c', _decode_unknown_0x8f1d597c),
    0x7a9f8249: ('attack_tentacle', _decode_attack_tentacle),
    0x38cf133b: ('actor_parameters', _decode_actor_parameters),
    0x767060d: ('attack_motion', _decode_attack_motion),
    0xe6b1e70: ('camera_shaker_data', _decode_camera_shaker_data),
    0xf683fe08: ('attack_tentacle_damage', _decode_attack_tentacle_damage),
    0xa77f6212: ('taunt_chance', _decode_taunt_chance),
    0x9cf01473: ('double_dash_chance', _decode_double_dash_chance),
    0xbd3efe7d: ('light_color', _decode_light_color),
    0xd24b888f: ('light_attenuation', _decode_light_attenuation),
    0xb459c3e9: ('unknown_0xb459c3e9', _decode_unknown_0xb459c3e9),
    0x323e4ed0: ('dash_speed', _decode_dash_speed),
    0x79bc576: ('ing_spot_blob_fx', _decode_ing_spot_blob_fx),
    0x7cb63cd3: ('ing_spot_sound', _decode_ing_spot_sound),
    0xe3d3708: ('unknown_0x0e3d3708', _decode_unknown_0x0e3d3708),
}
