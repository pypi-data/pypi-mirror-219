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
from retro_data_structures.properties.corruption.archetypes.PlayerActorStruct import PlayerActorStruct
from retro_data_structures.properties.corruption.archetypes.ShadowProjection import ShadowProjection
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class PlayerActor(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    mass: float = dataclasses.field(default=1.0)
    gravity: float = dataclasses.field(default=0.0)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    no_model: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    is_loop: bool = dataclasses.field(default=True)
    immovable: bool = dataclasses.field(default=True)
    is_solid: bool = dataclasses.field(default=True)
    empty_suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    empty_suit_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    varia_suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    varia_suit_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    varia_suit_grapple_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    varia_suit_grapple_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    stage01_suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    stage01_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    stage02_suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    stage02_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    stage03_suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    stage03_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    stage03_acid_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    stage03_acid_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    stage04_suit_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    stage04_skin_rule: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    player_actor_struct_0x1098d091: PlayerActorStruct = dataclasses.field(default_factory=PlayerActorStruct)
    player_actor_struct_0xc7385390: PlayerActorStruct = dataclasses.field(default_factory=PlayerActorStruct)
    flags_player_actor: int = dataclasses.field(default=16388)  # Flagset
    render_gun_override: int = dataclasses.field(default=0)
    unknown_struct510: ShadowProjection = dataclasses.field(default_factory=ShadowProjection)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00"')  # 34 properties

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

        data.write(b'@^R\x86')  # 0x405e5286
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_model))

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
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

        data.write(b'\x84c\x97\xa8')  # 0x846397a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.empty_suit_model))

        data.write(b'hZL\x01')  # 0x685a4c01
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.empty_suit_skin_rule))

        data.write(b'\x984\xec\xc9')  # 0x9834ecc9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.varia_suit_model))

        data.write(b'\x18\x8b\x89`')  # 0x188b8960
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.varia_suit_skin_rule))

        data.write(b'\x13J\x81\xe3')  # 0x134a81e3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.varia_suit_grapple_model))

        data.write(b'J\xbf\x03\x0c')  # 0x4abf030c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.varia_suit_grapple_skin_rule))

        data.write(b'\x9b\xf00\xdc')  # 0x9bf030dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage01_suit_model))

        data.write(b'\x98\x12c\xd3')  # 0x981263d3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage01_skin_rule))

        data.write(b'\x8a\x8dZ\xa5')  # 0x8a8d5aa5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage02_suit_model))

        data.write(b'\xe4sF\x08')  # 0xe4734608
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage02_skin_rule))

        data.write(b'3v\x81M')  # 0x3376814d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage03_suit_model))

        data.write(b'y|\xa7~')  # 0x797ca77e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage03_skin_rule))

        data.write(b'\x0e\xbe\xc4@')  # 0xebec440
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage03_acid_model))

        data.write(b'\xbc\tR\xd8')  # 0xbc0952d8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage03_acid_rule))

        data.write(b'\xa8w\x8eW')  # 0xa8778e57
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage04_suit_model))

        data.write(b'\x1c\xb1\r\xbe')  # 0x1cb10dbe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stage04_skin_rule))

        data.write(b'\x10\x98\xd0\x91')  # 0x1098d091
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_actor_struct_0x1098d091.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc78S\x90')  # 0xc7385390
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_actor_struct_0xc7385390.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3Py\x98')  # 0x33507998
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_player_actor))

        data.write(b'\xb6\x83(@')  # 0xb6832840
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_gun_override))

        data.write(b'\xa2\x1bQZ')  # 0xa21b515a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct510.to_stream(data)
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
            no_model=data['no_model'],
            animation=AnimationParameters.from_json(data['animation']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            is_loop=data['is_loop'],
            immovable=data['immovable'],
            is_solid=data['is_solid'],
            empty_suit_model=data['empty_suit_model'],
            empty_suit_skin_rule=data['empty_suit_skin_rule'],
            varia_suit_model=data['varia_suit_model'],
            varia_suit_skin_rule=data['varia_suit_skin_rule'],
            varia_suit_grapple_model=data['varia_suit_grapple_model'],
            varia_suit_grapple_skin_rule=data['varia_suit_grapple_skin_rule'],
            stage01_suit_model=data['stage01_suit_model'],
            stage01_skin_rule=data['stage01_skin_rule'],
            stage02_suit_model=data['stage02_suit_model'],
            stage02_skin_rule=data['stage02_skin_rule'],
            stage03_suit_model=data['stage03_suit_model'],
            stage03_skin_rule=data['stage03_skin_rule'],
            stage03_acid_model=data['stage03_acid_model'],
            stage03_acid_rule=data['stage03_acid_rule'],
            stage04_suit_model=data['stage04_suit_model'],
            stage04_skin_rule=data['stage04_skin_rule'],
            player_actor_struct_0x1098d091=PlayerActorStruct.from_json(data['player_actor_struct_0x1098d091']),
            player_actor_struct_0xc7385390=PlayerActorStruct.from_json(data['player_actor_struct_0xc7385390']),
            flags_player_actor=data['flags_player_actor'],
            render_gun_override=data['render_gun_override'],
            unknown_struct510=ShadowProjection.from_json(data['unknown_struct510']),
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
            'no_model': self.no_model,
            'animation': self.animation.to_json(),
            'actor_information': self.actor_information.to_json(),
            'is_loop': self.is_loop,
            'immovable': self.immovable,
            'is_solid': self.is_solid,
            'empty_suit_model': self.empty_suit_model,
            'empty_suit_skin_rule': self.empty_suit_skin_rule,
            'varia_suit_model': self.varia_suit_model,
            'varia_suit_skin_rule': self.varia_suit_skin_rule,
            'varia_suit_grapple_model': self.varia_suit_grapple_model,
            'varia_suit_grapple_skin_rule': self.varia_suit_grapple_skin_rule,
            'stage01_suit_model': self.stage01_suit_model,
            'stage01_skin_rule': self.stage01_skin_rule,
            'stage02_suit_model': self.stage02_suit_model,
            'stage02_skin_rule': self.stage02_skin_rule,
            'stage03_suit_model': self.stage03_suit_model,
            'stage03_skin_rule': self.stage03_skin_rule,
            'stage03_acid_model': self.stage03_acid_model,
            'stage03_acid_rule': self.stage03_acid_rule,
            'stage04_suit_model': self.stage04_suit_model,
            'stage04_skin_rule': self.stage04_skin_rule,
            'player_actor_struct_0x1098d091': self.player_actor_struct_0x1098d091.to_json(),
            'player_actor_struct_0xc7385390': self.player_actor_struct_0xc7385390.to_json(),
            'flags_player_actor': self.flags_player_actor,
            'render_gun_override': self.render_gun_override,
            'unknown_struct510': self.unknown_struct510.to_json(),
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


def _decode_no_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_is_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_immovable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_solid(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_empty_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_empty_suit_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_varia_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_varia_suit_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_varia_suit_grapple_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_varia_suit_grapple_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage01_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage01_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage02_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage02_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage03_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage03_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage03_acid_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage03_acid_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage04_suit_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stage04_skin_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_player_actor_struct_0x1098d091(data: typing.BinaryIO, property_size: int):
    return PlayerActorStruct.from_stream(data, property_size)


def _decode_player_actor_struct_0xc7385390(data: typing.BinaryIO, property_size: int):
    return PlayerActorStruct.from_stream(data, property_size)


def _decode_flags_player_actor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_render_gun_override(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_struct510(data: typing.BinaryIO, property_size: int):
    return ShadowProjection.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0x75dbb375: ('mass', _decode_mass),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x405e5286: ('no_model', _decode_no_model),
    0xa3d63f44: ('animation', _decode_animation),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xc08d1b93: ('is_loop', _decode_is_loop),
    0x1e32523e: ('immovable', _decode_immovable),
    0x1d8dd846: ('is_solid', _decode_is_solid),
    0x846397a8: ('empty_suit_model', _decode_empty_suit_model),
    0x685a4c01: ('empty_suit_skin_rule', _decode_empty_suit_skin_rule),
    0x9834ecc9: ('varia_suit_model', _decode_varia_suit_model),
    0x188b8960: ('varia_suit_skin_rule', _decode_varia_suit_skin_rule),
    0x134a81e3: ('varia_suit_grapple_model', _decode_varia_suit_grapple_model),
    0x4abf030c: ('varia_suit_grapple_skin_rule', _decode_varia_suit_grapple_skin_rule),
    0x9bf030dc: ('stage01_suit_model', _decode_stage01_suit_model),
    0x981263d3: ('stage01_skin_rule', _decode_stage01_skin_rule),
    0x8a8d5aa5: ('stage02_suit_model', _decode_stage02_suit_model),
    0xe4734608: ('stage02_skin_rule', _decode_stage02_skin_rule),
    0x3376814d: ('stage03_suit_model', _decode_stage03_suit_model),
    0x797ca77e: ('stage03_skin_rule', _decode_stage03_skin_rule),
    0xebec440: ('stage03_acid_model', _decode_stage03_acid_model),
    0xbc0952d8: ('stage03_acid_rule', _decode_stage03_acid_rule),
    0xa8778e57: ('stage04_suit_model', _decode_stage04_suit_model),
    0x1cb10dbe: ('stage04_skin_rule', _decode_stage04_skin_rule),
    0x1098d091: ('player_actor_struct_0x1098d091', _decode_player_actor_struct_0x1098d091),
    0xc7385390: ('player_actor_struct_0xc7385390', _decode_player_actor_struct_0xc7385390),
    0x33507998: ('flags_player_actor', _decode_flags_player_actor),
    0xb6832840: ('render_gun_override', _decode_render_gun_override),
    0xa21b515a: ('unknown_struct510', _decode_unknown_struct510),
}
