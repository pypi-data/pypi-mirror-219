# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Chakram(BaseProperty):
    chakram_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    energy_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    trail_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    static_geometry_collision_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    in_flight_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    player_impact_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    hyper_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    speed: float = dataclasses.field(default=50.0)
    unknown_0x508c48d7: float = dataclasses.field(default=50.0)
    spin_rate: float = dataclasses.field(default=720.0)
    fade_out_time: float = dataclasses.field(default=0.5)
    visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC']}, default=default_asset_id)
    stun_time: float = dataclasses.field(default=1.0)
    unknown_0x2f79b3d0: float = dataclasses.field(default=20.0)
    unknown_0x11cc7b58: float = dataclasses.field(default=60.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'f\xabW\xa4')  # 0x66ab57a4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.chakram_model))

        data.write(b'\x14\x144p')  # 0x14143470
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.energy_effect))

        data.write(b'6\xee\xe7\x91')  # 0x36eee791
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.trail_effect))

        data.write(b'R\xf8\x9b\xf7')  # 0x52f89bf7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.static_geometry_collision_effect))

        data.write(b'\x1a\t()')  # 0x1a092829
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.in_flight_sound))

        data.write(b'\xe3:\x99m')  # 0xe33a996d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.player_impact_sound))

        data.write(b'\xdfd\xc6z')  # 0xdf64c67a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xda\xbf\x84')  # 0xb3dabf84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'P\x8cH\xd7')  # 0x508c48d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x508c48d7))

        data.write(b'\x8bJ\xf5\xc4')  # 0x8b4af5c4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spin_rate))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xe9\xc8\xe2\xbd')  # 0xe9c8e2bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect))

        data.write(b'~\x19#\x95')  # 0x7e192395
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_time))

        data.write(b'/y\xb3\xd0')  # 0x2f79b3d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2f79b3d0))

        data.write(b'\x11\xcc{X')  # 0x11cc7b58
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x11cc7b58))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            chakram_model=data['chakram_model'],
            energy_effect=data['energy_effect'],
            trail_effect=data['trail_effect'],
            static_geometry_collision_effect=data['static_geometry_collision_effect'],
            in_flight_sound=data['in_flight_sound'],
            player_impact_sound=data['player_impact_sound'],
            caud=data['caud'],
            damage=DamageInfo.from_json(data['damage']),
            hyper_damage=DamageInfo.from_json(data['hyper_damage']),
            speed=data['speed'],
            unknown_0x508c48d7=data['unknown_0x508c48d7'],
            spin_rate=data['spin_rate'],
            fade_out_time=data['fade_out_time'],
            visor_effect=data['visor_effect'],
            stun_time=data['stun_time'],
            unknown_0x2f79b3d0=data['unknown_0x2f79b3d0'],
            unknown_0x11cc7b58=data['unknown_0x11cc7b58'],
        )

    def to_json(self) -> dict:
        return {
            'chakram_model': self.chakram_model,
            'energy_effect': self.energy_effect,
            'trail_effect': self.trail_effect,
            'static_geometry_collision_effect': self.static_geometry_collision_effect,
            'in_flight_sound': self.in_flight_sound,
            'player_impact_sound': self.player_impact_sound,
            'caud': self.caud,
            'damage': self.damage.to_json(),
            'hyper_damage': self.hyper_damage.to_json(),
            'speed': self.speed,
            'unknown_0x508c48d7': self.unknown_0x508c48d7,
            'spin_rate': self.spin_rate,
            'fade_out_time': self.fade_out_time,
            'visor_effect': self.visor_effect,
            'stun_time': self.stun_time,
            'unknown_0x2f79b3d0': self.unknown_0x2f79b3d0,
            'unknown_0x11cc7b58': self.unknown_0x11cc7b58,
        }


def _decode_chakram_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_energy_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_trail_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_static_geometry_collision_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_in_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_player_impact_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_hyper_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x508c48d7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spin_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stun_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2f79b3d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x11cc7b58(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x66ab57a4: ('chakram_model', _decode_chakram_model),
    0x14143470: ('energy_effect', _decode_energy_effect),
    0x36eee791: ('trail_effect', _decode_trail_effect),
    0x52f89bf7: ('static_geometry_collision_effect', _decode_static_geometry_collision_effect),
    0x1a092829: ('in_flight_sound', _decode_in_flight_sound),
    0xe33a996d: ('player_impact_sound', _decode_player_impact_sound),
    0xdf64c67a: ('caud', _decode_caud),
    0x337f9524: ('damage', _decode_damage),
    0xb3dabf84: ('hyper_damage', _decode_hyper_damage),
    0x6392404e: ('speed', _decode_speed),
    0x508c48d7: ('unknown_0x508c48d7', _decode_unknown_0x508c48d7),
    0x8b4af5c4: ('spin_rate', _decode_spin_rate),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xe9c8e2bd: ('visor_effect', _decode_visor_effect),
    0x7e192395: ('stun_time', _decode_stun_time),
    0x2f79b3d0: ('unknown_0x2f79b3d0', _decode_unknown_0x2f79b3d0),
    0x11cc7b58: ('unknown_0x11cc7b58', _decode_unknown_0x11cc7b58),
}
