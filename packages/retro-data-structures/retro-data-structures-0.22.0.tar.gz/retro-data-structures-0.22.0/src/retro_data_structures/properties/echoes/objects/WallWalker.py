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
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class WallWalker(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    leg_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    waypoint_approach_distance: float = dataclasses.field(default=2.5)
    floor_turn_speed: float = dataclasses.field(default=1080.0)
    unknown_0xd5c25506: float = dataclasses.field(default=0.4000000059604645)
    visible_distance: float = dataclasses.field(default=40.0)
    explode_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    grenade_explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grenade_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grenade_trail: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grenade_mass: float = dataclasses.field(default=4.0)
    unknown_0xed086ce0: float = dataclasses.field(default=0.5)
    unknown_0x454f16b1: int = dataclasses.field(default=5)
    unknown_0x7f1613b7: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x7050d866: int = dataclasses.field(default=0, metadata={'sound': True})
    projectile_interval: float = dataclasses.field(default=2.0)
    unknown_0x723542bb: float = dataclasses.field(default=5.0)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    camera_shaker_data: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'WLWK'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['WallCrawler.rel', 'WallWalker.rel']

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
        data.write(b'\x00\x17')  # 23 properties

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
        self.patterned.to_stream(data, default_override={'creature_size': 1})
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

        data.write(b'\x9f\x0f\xf8R')  # 0x9f0ff852
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.leg_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's;\xd2|')  # 0x733bd27c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.waypoint_approach_distance))

        data.write(b'\x8eO{)')  # 0x8e4f7b29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_turn_speed))

        data.write(b'\xd5\xc2U\x06')  # 0xd5c25506
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd5c25506))

        data.write(b'\xa7%0\xe8')  # 0xa72530e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_distance))

        data.write(b'\xf6 j\x12')  # 0xf6206a12
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.explode_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\x19\xe0w')  # 0x1319e077
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_explosion))

        data.write(b'\xd2\x07\xff\x0f')  # 0xd207ff0f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_effect))

        data.write(b'+1\xc8\x82')  # 0x2b31c882
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_trail))

        data.write(b'\x9ak\xb4\x7f')  # 0x9a6bb47f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grenade_mass))

        data.write(b'\xed\x08l\xe0')  # 0xed086ce0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed086ce0))

        data.write(b'EO\x16\xb1')  # 0x454f16b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x454f16b1))

        data.write(b'\x7f\x16\x13\xb7')  # 0x7f1613b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7f1613b7))

        data.write(b'pP\xd8f')  # 0x7050d866
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7050d866))

        data.write(b'\xd4\x90<\x98')  # 0xd4903c98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_interval))

        data.write(b'r5B\xbb')  # 0x723542bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x723542bb))

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\xdcM\x11')  # 0x68dc4d11
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part))

        data.write(b'"\xbb\xdd\n')  # 0x22bbdd0a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_shaker_data.to_stream(data)
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
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            leg_vulnerability=DamageVulnerability.from_json(data['leg_vulnerability']),
            waypoint_approach_distance=data['waypoint_approach_distance'],
            floor_turn_speed=data['floor_turn_speed'],
            unknown_0xd5c25506=data['unknown_0xd5c25506'],
            visible_distance=data['visible_distance'],
            explode_damage=DamageInfo.from_json(data['explode_damage']),
            grenade_explosion=data['grenade_explosion'],
            grenade_effect=data['grenade_effect'],
            grenade_trail=data['grenade_trail'],
            grenade_mass=data['grenade_mass'],
            unknown_0xed086ce0=data['unknown_0xed086ce0'],
            unknown_0x454f16b1=data['unknown_0x454f16b1'],
            unknown_0x7f1613b7=data['unknown_0x7f1613b7'],
            unknown_0x7050d866=data['unknown_0x7050d866'],
            projectile_interval=data['projectile_interval'],
            unknown_0x723542bb=data['unknown_0x723542bb'],
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            part=data['part'],
            camera_shaker_data=CameraShakerData.from_json(data['camera_shaker_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'leg_vulnerability': self.leg_vulnerability.to_json(),
            'waypoint_approach_distance': self.waypoint_approach_distance,
            'floor_turn_speed': self.floor_turn_speed,
            'unknown_0xd5c25506': self.unknown_0xd5c25506,
            'visible_distance': self.visible_distance,
            'explode_damage': self.explode_damage.to_json(),
            'grenade_explosion': self.grenade_explosion,
            'grenade_effect': self.grenade_effect,
            'grenade_trail': self.grenade_trail,
            'grenade_mass': self.grenade_mass,
            'unknown_0xed086ce0': self.unknown_0xed086ce0,
            'unknown_0x454f16b1': self.unknown_0x454f16b1,
            'unknown_0x7f1613b7': self.unknown_0x7f1613b7,
            'unknown_0x7050d866': self.unknown_0x7050d866,
            'projectile_interval': self.projectile_interval,
            'unknown_0x723542bb': self.unknown_0x723542bb,
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'part': self.part,
            'camera_shaker_data': self.camera_shaker_data.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_leg_vulnerability(self, asset_manager):
        yield from self.leg_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_explode_damage(self, asset_manager):
        yield from self.explode_damage.dependencies_for(asset_manager)

    def _dependencies_for_grenade_explosion(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_explosion)

    def _dependencies_for_grenade_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_effect)

    def _dependencies_for_grenade_trail(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_trail)

    def _dependencies_for_unknown_0x7f1613b7(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0x7f1613b7)

    def _dependencies_for_unknown_0x7050d866(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0x7050d866)

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_part(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part)

    def _dependencies_for_camera_shaker_data(self, asset_manager):
        yield from self.camera_shaker_data.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_leg_vulnerability, "leg_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_explode_damage, "explode_damage", "DamageInfo"),
            (self._dependencies_for_grenade_explosion, "grenade_explosion", "AssetId"),
            (self._dependencies_for_grenade_effect, "grenade_effect", "AssetId"),
            (self._dependencies_for_grenade_trail, "grenade_trail", "AssetId"),
            (self._dependencies_for_unknown_0x7f1613b7, "unknown_0x7f1613b7", "int"),
            (self._dependencies_for_unknown_0x7050d866, "unknown_0x7050d866", "int"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_part, "part", "AssetId"),
            (self._dependencies_for_camera_shaker_data, "camera_shaker_data", "CameraShakerData"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for WallWalker.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_leg_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_waypoint_approach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd5c25506(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_explode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_grenade_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grenade_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grenade_trail(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grenade_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed086ce0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x454f16b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7f1613b7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7050d866(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_projectile_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x723542bb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_camera_shaker_data(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x9f0ff852: ('leg_vulnerability', _decode_leg_vulnerability),
    0x733bd27c: ('waypoint_approach_distance', _decode_waypoint_approach_distance),
    0x8e4f7b29: ('floor_turn_speed', _decode_floor_turn_speed),
    0xd5c25506: ('unknown_0xd5c25506', _decode_unknown_0xd5c25506),
    0xa72530e8: ('visible_distance', _decode_visible_distance),
    0xf6206a12: ('explode_damage', _decode_explode_damage),
    0x1319e077: ('grenade_explosion', _decode_grenade_explosion),
    0xd207ff0f: ('grenade_effect', _decode_grenade_effect),
    0x2b31c882: ('grenade_trail', _decode_grenade_trail),
    0x9a6bb47f: ('grenade_mass', _decode_grenade_mass),
    0xed086ce0: ('unknown_0xed086ce0', _decode_unknown_0xed086ce0),
    0x454f16b1: ('unknown_0x454f16b1', _decode_unknown_0x454f16b1),
    0x7f1613b7: ('unknown_0x7f1613b7', _decode_unknown_0x7f1613b7),
    0x7050d866: ('unknown_0x7050d866', _decode_unknown_0x7050d866),
    0xd4903c98: ('projectile_interval', _decode_projectile_interval),
    0x723542bb: ('unknown_0x723542bb', _decode_unknown_0x723542bb),
    0xef485db9: ('projectile', _decode_projectile),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0x68dc4d11: ('part', _decode_part),
    0x22bbdd0a: ('camera_shaker_data', _decode_camera_shaker_data),
}
