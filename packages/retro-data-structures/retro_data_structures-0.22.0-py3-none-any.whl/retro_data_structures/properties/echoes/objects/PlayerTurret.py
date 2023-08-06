# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerTurret(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_player_turret: int = dataclasses.field(default=1)
    unknown_0x17cd8b2a: float = dataclasses.field(default=90.0)
    unknown_0x1473dad2: float = dataclasses.field(default=90.0)
    unknown_0x3650ce75: float = dataclasses.field(default=90.0)
    unknown_0x78520e6e: float = dataclasses.field(default=0.0)
    damage_angle: float = dataclasses.field(default=30.0)
    horiz_speed: float = dataclasses.field(default=30.0)
    vert_speed: float = dataclasses.field(default=30.0)
    fire_rate: float = dataclasses.field(default=1.0)
    weapon_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    weapon_effect: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    unknown_0xe7234f72: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x3e2f7afb: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x7cabd1f1: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x7ef976eb: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x035459fd: int = dataclasses.field(default=0, metadata={'sound': True})

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PLRT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ScriptPlayerTurret.rel']

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\xad\xef\xa6')  # 0xeeadefa6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_player_turret))

        data.write(b'\x17\xcd\x8b*')  # 0x17cd8b2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x17cd8b2a))

        data.write(b'\x14s\xda\xd2')  # 0x1473dad2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1473dad2))

        data.write(b'6P\xceu')  # 0x3650ce75
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3650ce75))

        data.write(b'xR\x0en')  # 0x78520e6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x78520e6e))

        data.write(b'\xa3\x9a]r')  # 0xa39a5d72
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_angle))

        data.write(b'\xfb.2\xdb')  # 0xfb2e32db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horiz_speed))

        data.write(b'\x1b<\x86\x83')  # 0x1b3c8683
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_speed))

        data.write(b'\xc6\xe4\x8f\x18')  # 0xc6e48f18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fire_rate))

        data.write(b'\x8e_~\x96')  # 0x8e5f7e96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapon_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc43`\xa7')  # 0xc43360a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.weapon_effect))

        data.write(b'\xa9\x9d=\xbe')  # 0xa99d3dbe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.wpsc))

        data.write(b'\xe7#Or')  # 0xe7234f72
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe7234f72))

        data.write(b'>/z\xfb')  # 0x3e2f7afb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x3e2f7afb))

        data.write(b'|\xab\xd1\xf1')  # 0x7cabd1f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7cabd1f1))

        data.write(b'~\xf9v\xeb')  # 0x7ef976eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7ef976eb))

        data.write(b'\x03TY\xfd')  # 0x35459fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x035459fd))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            flags_player_turret=data['flags_player_turret'],
            unknown_0x17cd8b2a=data['unknown_0x17cd8b2a'],
            unknown_0x1473dad2=data['unknown_0x1473dad2'],
            unknown_0x3650ce75=data['unknown_0x3650ce75'],
            unknown_0x78520e6e=data['unknown_0x78520e6e'],
            damage_angle=data['damage_angle'],
            horiz_speed=data['horiz_speed'],
            vert_speed=data['vert_speed'],
            fire_rate=data['fire_rate'],
            weapon_damage=DamageInfo.from_json(data['weapon_damage']),
            weapon_effect=data['weapon_effect'],
            wpsc=data['wpsc'],
            unknown_0xe7234f72=data['unknown_0xe7234f72'],
            unknown_0x3e2f7afb=data['unknown_0x3e2f7afb'],
            unknown_0x7cabd1f1=data['unknown_0x7cabd1f1'],
            unknown_0x7ef976eb=data['unknown_0x7ef976eb'],
            unknown_0x035459fd=data['unknown_0x035459fd'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_player_turret': self.flags_player_turret,
            'unknown_0x17cd8b2a': self.unknown_0x17cd8b2a,
            'unknown_0x1473dad2': self.unknown_0x1473dad2,
            'unknown_0x3650ce75': self.unknown_0x3650ce75,
            'unknown_0x78520e6e': self.unknown_0x78520e6e,
            'damage_angle': self.damage_angle,
            'horiz_speed': self.horiz_speed,
            'vert_speed': self.vert_speed,
            'fire_rate': self.fire_rate,
            'weapon_damage': self.weapon_damage.to_json(),
            'weapon_effect': self.weapon_effect,
            'wpsc': self.wpsc,
            'unknown_0xe7234f72': self.unknown_0xe7234f72,
            'unknown_0x3e2f7afb': self.unknown_0x3e2f7afb,
            'unknown_0x7cabd1f1': self.unknown_0x7cabd1f1,
            'unknown_0x7ef976eb': self.unknown_0x7ef976eb,
            'unknown_0x035459fd': self.unknown_0x035459fd,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_weapon_damage(self, asset_manager):
        yield from self.weapon_damage.dependencies_for(asset_manager)

    def _dependencies_for_weapon_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.weapon_effect)

    def _dependencies_for_wpsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc)

    def _dependencies_for_unknown_0xe7234f72(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0xe7234f72)

    def _dependencies_for_unknown_0x3e2f7afb(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0x3e2f7afb)

    def _dependencies_for_unknown_0x7cabd1f1(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0x7cabd1f1)

    def _dependencies_for_unknown_0x7ef976eb(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0x7ef976eb)

    def _dependencies_for_unknown_0x035459fd(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.unknown_0x035459fd)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_weapon_damage, "weapon_damage", "DamageInfo"),
            (self._dependencies_for_weapon_effect, "weapon_effect", "AssetId"),
            (self._dependencies_for_wpsc, "wpsc", "AssetId"),
            (self._dependencies_for_unknown_0xe7234f72, "unknown_0xe7234f72", "int"),
            (self._dependencies_for_unknown_0x3e2f7afb, "unknown_0x3e2f7afb", "int"),
            (self._dependencies_for_unknown_0x7cabd1f1, "unknown_0x7cabd1f1", "int"),
            (self._dependencies_for_unknown_0x7ef976eb, "unknown_0x7ef976eb", "int"),
            (self._dependencies_for_unknown_0x035459fd, "unknown_0x035459fd", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PlayerTurret.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_player_turret(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x17cd8b2a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1473dad2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3650ce75(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x78520e6e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horiz_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fire_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_weapon_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_weapon_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xe7234f72(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3e2f7afb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7cabd1f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7ef976eb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x035459fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xeeadefa6: ('flags_player_turret', _decode_flags_player_turret),
    0x17cd8b2a: ('unknown_0x17cd8b2a', _decode_unknown_0x17cd8b2a),
    0x1473dad2: ('unknown_0x1473dad2', _decode_unknown_0x1473dad2),
    0x3650ce75: ('unknown_0x3650ce75', _decode_unknown_0x3650ce75),
    0x78520e6e: ('unknown_0x78520e6e', _decode_unknown_0x78520e6e),
    0xa39a5d72: ('damage_angle', _decode_damage_angle),
    0xfb2e32db: ('horiz_speed', _decode_horiz_speed),
    0x1b3c8683: ('vert_speed', _decode_vert_speed),
    0xc6e48f18: ('fire_rate', _decode_fire_rate),
    0x8e5f7e96: ('weapon_damage', _decode_weapon_damage),
    0xc43360a7: ('weapon_effect', _decode_weapon_effect),
    0xa99d3dbe: ('wpsc', _decode_wpsc),
    0xe7234f72: ('unknown_0xe7234f72', _decode_unknown_0xe7234f72),
    0x3e2f7afb: ('unknown_0x3e2f7afb', _decode_unknown_0x3e2f7afb),
    0x7cabd1f1: ('unknown_0x7cabd1f1', _decode_unknown_0x7cabd1f1),
    0x7ef976eb: ('unknown_0x7ef976eb', _decode_unknown_0x7ef976eb),
    0x35459fd: ('unknown_0x035459fd', _decode_unknown_0x035459fd),
}
