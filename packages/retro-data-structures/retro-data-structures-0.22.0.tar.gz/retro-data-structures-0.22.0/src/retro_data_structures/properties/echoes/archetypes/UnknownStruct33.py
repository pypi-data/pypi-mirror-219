# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct33(BaseProperty):
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    bomb_stun_duration: float = dataclasses.field(default=5.0)
    unknown_0x46aaced3: float = dataclasses.field(default=10.0)
    max_speed: float = dataclasses.field(default=15.0)
    max_wall_speed: float = dataclasses.field(default=7.0)
    ball_pursuit_speed: float = dataclasses.field(default=25.0)
    speed_modifier: float = dataclasses.field(default=2.0)
    turn_speed: float = dataclasses.field(default=360.0)
    blob_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    hit_normal_damage: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    hit_heavy_damage: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    death: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_idle: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_move: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0xb392943a: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x24ecc1e9: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_death: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x7569fdba: float = dataclasses.field(default=100.0)
    unknown_0xd55938d2: float = dataclasses.field(default=0.20000000298023224)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 4.5, 'di_knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X`\xe2K')  # 0x5860e24b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_stun_duration))

        data.write(b'F\xaa\xce\xd3')  # 0x46aaced3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x46aaced3))

        data.write(b'\x82\xdb\x0c\xbe')  # 0x82db0cbe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_speed))

        data.write(b'\xbe\xc6R\xae')  # 0xbec652ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_wall_speed))

        data.write(b'`\n\x86?')  # 0x600a863f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_pursuit_speed))

        data.write(b'8\x8eI\x02')  # 0x388e4902
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed_modifier))

        data.write(b'\x02\x0cx\xbb')  # 0x20c78bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed))

        data.write(b'#g\xf6\x89')  # 0x2367f689
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.blob_effect))

        data.write(b'\xd4s\x15\x8d')  # 0xd473158d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.hit_normal_damage))

        data.write(b'\xcc\xa2\x98\xb4')  # 0xcca298b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.hit_heavy_damage))

        data.write(b'\xb9\x9c\x80\xd3')  # 0xb99c80d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death))

        data.write(b'\xaf8\x96\x8e')  # 0xaf38968e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_idle))

        data.write(b'l\x10\x18T')  # 0x6c101854
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_move))

        data.write(b'\xb3\x92\x94:')  # 0xb392943a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xb392943a))

        data.write(b'$\xec\xc1\xe9')  # 0x24ecc1e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x24ecc1e9))

        data.write(b'\xe1`\xb5\x93')  # 0xe160b593
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_death))

        data.write(b'ui\xfd\xba')  # 0x7569fdba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7569fdba))

        data.write(b'\xd5Y8\xd2')  # 0xd55938d2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd55938d2))

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            damage=DamageInfo.from_json(data['damage']),
            bomb_stun_duration=data['bomb_stun_duration'],
            unknown_0x46aaced3=data['unknown_0x46aaced3'],
            max_speed=data['max_speed'],
            max_wall_speed=data['max_wall_speed'],
            ball_pursuit_speed=data['ball_pursuit_speed'],
            speed_modifier=data['speed_modifier'],
            turn_speed=data['turn_speed'],
            blob_effect=data['blob_effect'],
            hit_normal_damage=data['hit_normal_damage'],
            hit_heavy_damage=data['hit_heavy_damage'],
            death=data['death'],
            sound_idle=data['sound_idle'],
            sound_move=data['sound_move'],
            sound_0xb392943a=data['sound_0xb392943a'],
            sound_0x24ecc1e9=data['sound_0x24ecc1e9'],
            sound_death=data['sound_death'],
            unknown_0x7569fdba=data['unknown_0x7569fdba'],
            unknown_0xd55938d2=data['unknown_0xd55938d2'],
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'damage': self.damage.to_json(),
            'bomb_stun_duration': self.bomb_stun_duration,
            'unknown_0x46aaced3': self.unknown_0x46aaced3,
            'max_speed': self.max_speed,
            'max_wall_speed': self.max_wall_speed,
            'ball_pursuit_speed': self.ball_pursuit_speed,
            'speed_modifier': self.speed_modifier,
            'turn_speed': self.turn_speed,
            'blob_effect': self.blob_effect,
            'hit_normal_damage': self.hit_normal_damage,
            'hit_heavy_damage': self.hit_heavy_damage,
            'death': self.death,
            'sound_idle': self.sound_idle,
            'sound_move': self.sound_move,
            'sound_0xb392943a': self.sound_0xb392943a,
            'sound_0x24ecc1e9': self.sound_0x24ecc1e9,
            'sound_death': self.sound_death,
            'unknown_0x7569fdba': self.unknown_0x7569fdba,
            'unknown_0xd55938d2': self.unknown_0xd55938d2,
            'vulnerability': self.vulnerability.to_json(),
        }

    def _dependencies_for_damage(self, asset_manager):
        yield from self.damage.dependencies_for(asset_manager)

    def _dependencies_for_blob_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.blob_effect)

    def _dependencies_for_hit_normal_damage(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.hit_normal_damage)

    def _dependencies_for_hit_heavy_damage(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.hit_heavy_damage)

    def _dependencies_for_death(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.death)

    def _dependencies_for_sound_idle(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_idle)

    def _dependencies_for_sound_move(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_move)

    def _dependencies_for_sound_0xb392943a(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xb392943a)

    def _dependencies_for_sound_0x24ecc1e9(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x24ecc1e9)

    def _dependencies_for_sound_death(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_death)

    def _dependencies_for_vulnerability(self, asset_manager):
        yield from self.vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_damage, "damage", "DamageInfo"),
            (self._dependencies_for_blob_effect, "blob_effect", "AssetId"),
            (self._dependencies_for_hit_normal_damage, "hit_normal_damage", "AssetId"),
            (self._dependencies_for_hit_heavy_damage, "hit_heavy_damage", "AssetId"),
            (self._dependencies_for_death, "death", "AssetId"),
            (self._dependencies_for_sound_idle, "sound_idle", "int"),
            (self._dependencies_for_sound_move, "sound_move", "int"),
            (self._dependencies_for_sound_0xb392943a, "sound_0xb392943a", "int"),
            (self._dependencies_for_sound_0x24ecc1e9, "sound_0x24ecc1e9", "int"),
            (self._dependencies_for_sound_death, "sound_death", "int"),
            (self._dependencies_for_vulnerability, "vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct33.{field_name} ({field_type}): {e}"
                )


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 4.5, 'di_knock_back_power': 4.0})


def _decode_bomb_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x46aaced3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_wall_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_pursuit_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blob_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_hit_normal_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_hit_heavy_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_idle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0xb392943a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x24ecc1e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7569fdba(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd55938d2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x337f9524: ('damage', _decode_damage),
    0x5860e24b: ('bomb_stun_duration', _decode_bomb_stun_duration),
    0x46aaced3: ('unknown_0x46aaced3', _decode_unknown_0x46aaced3),
    0x82db0cbe: ('max_speed', _decode_max_speed),
    0xbec652ae: ('max_wall_speed', _decode_max_wall_speed),
    0x600a863f: ('ball_pursuit_speed', _decode_ball_pursuit_speed),
    0x388e4902: ('speed_modifier', _decode_speed_modifier),
    0x20c78bb: ('turn_speed', _decode_turn_speed),
    0x2367f689: ('blob_effect', _decode_blob_effect),
    0xd473158d: ('hit_normal_damage', _decode_hit_normal_damage),
    0xcca298b4: ('hit_heavy_damage', _decode_hit_heavy_damage),
    0xb99c80d3: ('death', _decode_death),
    0xaf38968e: ('sound_idle', _decode_sound_idle),
    0x6c101854: ('sound_move', _decode_sound_move),
    0xb392943a: ('sound_0xb392943a', _decode_sound_0xb392943a),
    0x24ecc1e9: ('sound_0x24ecc1e9', _decode_sound_0x24ecc1e9),
    0xe160b593: ('sound_death', _decode_sound_death),
    0x7569fdba: ('unknown_0x7569fdba', _decode_unknown_0x7569fdba),
    0xd55938d2: ('unknown_0xd55938d2', _decode_unknown_0xd55938d2),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
}
