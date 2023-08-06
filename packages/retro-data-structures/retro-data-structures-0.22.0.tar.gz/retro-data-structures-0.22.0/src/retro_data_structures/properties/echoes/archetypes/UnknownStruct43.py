# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData
from retro_data_structures.properties.echoes.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.echoes.archetypes.UnknownStruct42 import UnknownStruct42
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct43(BaseProperty):
    unknown_0xbd80fd94: int = dataclasses.field(default=10)
    max_linear_velocity: float = dataclasses.field(default=20.0)
    max_turn_speed: float = dataclasses.field(default=720.0)
    scanning_turn_speed: float = dataclasses.field(default=20.0)
    unknown_0xe32fcae9: float = dataclasses.field(default=4.0)
    unknown_0xc5e0b92c: float = dataclasses.field(default=10.0)
    unknown_0xc17a8806: float = dataclasses.field(default=20.0)
    unknown_0xe75bae9e: int = dataclasses.field(default=3)
    laser_pulse_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    laser_pulse_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xeda45014: int = dataclasses.field(default=1)
    unknown_0x7dd740fe: int = dataclasses.field(default=3)
    dodge_chance: float = dataclasses.field(default=100.0)
    reset_shield_time: float = dataclasses.field(default=10.0)
    split_destroyed_priority: float = dataclasses.field(default=100.0)
    laser_sweep_turn_speed: float = dataclasses.field(default=45.0)
    laser_sweep_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    laser_sweep_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    unknown_struct42: UnknownStruct42 = dataclasses.field(default_factory=UnknownStruct42)
    sound_laser_sweep: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_laser_charge_up: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_docking: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_scanning: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_light_shield: int = dataclasses.field(default=0)
    sound_dark_shield: int = dataclasses.field(default=0)
    sound_shield_on: int = dataclasses.field(default=0, metadata={'sound': True})
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    light_shield_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    dark_shield_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00\x1d')  # 29 properties

        data.write(b'\xbd\x80\xfd\x94')  # 0xbd80fd94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbd80fd94))

        data.write(b'\x00\xd7O\xc3')  # 0xd74fc3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_linear_velocity))

        data.write(b'\x0b\\<\x1a')  # 0xb5c3c1a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_turn_speed))

        data.write(b'\xa0\xb3\xe1\xbe')  # 0xa0b3e1be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scanning_turn_speed))

        data.write(b'\xe3/\xca\xe9')  # 0xe32fcae9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe32fcae9))

        data.write(b'\xc5\xe0\xb9,')  # 0xc5e0b92c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc5e0b92c))

        data.write(b'\xc1z\x88\x06')  # 0xc17a8806
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc17a8806))

        data.write(b'\xe7[\xae\x9e')  # 0xe75bae9e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe75bae9e))

        data.write(b'Mw\xb7\xaa')  # 0x4d77b7aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.laser_pulse_projectile))

        data.write(b'\xb7c\xeb\x10')  # 0xb763eb10
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.laser_pulse_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xa4P\x14')  # 0xeda45014
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xeda45014))

        data.write(b'}\xd7@\xfe')  # 0x7dd740fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7dd740fe))

        data.write(b'G\xbe2\x98')  # 0x47be3298
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_chance))

        data.write(b'\xd3\xde\xc6\xdc')  # 0xd3dec6dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reset_shield_time))

        data.write(b'\xec\xd9\xd9-')  # 0xecd9d92d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.split_destroyed_priority))

        data.write(b'_\xf0\x06\xd1')  # 0x5ff006d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.laser_sweep_turn_speed))

        data.write(b'\x1b\xd0\x17\xce')  # 0x1bd017ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.laser_sweep_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J7\xc47')  # 0x4a37c437
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.laser_sweep_beam_info.to_stream(data, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xc5\x1f\xe4')  # 0x9ec51fe4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct42.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea0uH')  # 0xea307548
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_laser_sweep))

        data.write(b'7y\xbd\x93')  # 0x3779bd93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_laser_charge_up))

        data.write(b'\xc9\r\xbd\xb4')  # 0xc90dbdb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_docking))

        data.write(b'\xe7rH\x02')  # 0xe7724802
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_scanning))

        data.write(b'\xd4\xa0bs')  # 0xd4a06273
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_light_shield))

        data.write(b'\xaf\xc2\x061')  # 0xafc20631
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_dark_shield))

        data.write(b'/\xf5\xa8\t')  # 0x2ff5a809
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_shield_on))

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xa8\xef;')  # 0x80a8ef3b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.light_shield_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\x1c\x90\xea')  # 0xa21c90ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_shield_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xbd80fd94=data['unknown_0xbd80fd94'],
            max_linear_velocity=data['max_linear_velocity'],
            max_turn_speed=data['max_turn_speed'],
            scanning_turn_speed=data['scanning_turn_speed'],
            unknown_0xe32fcae9=data['unknown_0xe32fcae9'],
            unknown_0xc5e0b92c=data['unknown_0xc5e0b92c'],
            unknown_0xc17a8806=data['unknown_0xc17a8806'],
            unknown_0xe75bae9e=data['unknown_0xe75bae9e'],
            laser_pulse_projectile=data['laser_pulse_projectile'],
            laser_pulse_damage=DamageInfo.from_json(data['laser_pulse_damage']),
            unknown_0xeda45014=data['unknown_0xeda45014'],
            unknown_0x7dd740fe=data['unknown_0x7dd740fe'],
            dodge_chance=data['dodge_chance'],
            reset_shield_time=data['reset_shield_time'],
            split_destroyed_priority=data['split_destroyed_priority'],
            laser_sweep_turn_speed=data['laser_sweep_turn_speed'],
            laser_sweep_damage=DamageInfo.from_json(data['laser_sweep_damage']),
            laser_sweep_beam_info=PlasmaBeamInfo.from_json(data['laser_sweep_beam_info']),
            unknown_struct42=UnknownStruct42.from_json(data['unknown_struct42']),
            sound_laser_sweep=data['sound_laser_sweep'],
            sound_laser_charge_up=data['sound_laser_charge_up'],
            sound_docking=data['sound_docking'],
            sound_scanning=data['sound_scanning'],
            sound_light_shield=data['sound_light_shield'],
            sound_dark_shield=data['sound_dark_shield'],
            sound_shield_on=data['sound_shield_on'],
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
            light_shield_vulnerability=DamageVulnerability.from_json(data['light_shield_vulnerability']),
            dark_shield_vulnerability=DamageVulnerability.from_json(data['dark_shield_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xbd80fd94': self.unknown_0xbd80fd94,
            'max_linear_velocity': self.max_linear_velocity,
            'max_turn_speed': self.max_turn_speed,
            'scanning_turn_speed': self.scanning_turn_speed,
            'unknown_0xe32fcae9': self.unknown_0xe32fcae9,
            'unknown_0xc5e0b92c': self.unknown_0xc5e0b92c,
            'unknown_0xc17a8806': self.unknown_0xc17a8806,
            'unknown_0xe75bae9e': self.unknown_0xe75bae9e,
            'laser_pulse_projectile': self.laser_pulse_projectile,
            'laser_pulse_damage': self.laser_pulse_damage.to_json(),
            'unknown_0xeda45014': self.unknown_0xeda45014,
            'unknown_0x7dd740fe': self.unknown_0x7dd740fe,
            'dodge_chance': self.dodge_chance,
            'reset_shield_time': self.reset_shield_time,
            'split_destroyed_priority': self.split_destroyed_priority,
            'laser_sweep_turn_speed': self.laser_sweep_turn_speed,
            'laser_sweep_damage': self.laser_sweep_damage.to_json(),
            'laser_sweep_beam_info': self.laser_sweep_beam_info.to_json(),
            'unknown_struct42': self.unknown_struct42.to_json(),
            'sound_laser_sweep': self.sound_laser_sweep,
            'sound_laser_charge_up': self.sound_laser_charge_up,
            'sound_docking': self.sound_docking,
            'sound_scanning': self.sound_scanning,
            'sound_light_shield': self.sound_light_shield,
            'sound_dark_shield': self.sound_dark_shield,
            'sound_shield_on': self.sound_shield_on,
            'ing_possession_data': self.ing_possession_data.to_json(),
            'light_shield_vulnerability': self.light_shield_vulnerability.to_json(),
            'dark_shield_vulnerability': self.dark_shield_vulnerability.to_json(),
        }

    def _dependencies_for_laser_pulse_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.laser_pulse_projectile)

    def _dependencies_for_laser_pulse_damage(self, asset_manager):
        yield from self.laser_pulse_damage.dependencies_for(asset_manager)

    def _dependencies_for_laser_sweep_damage(self, asset_manager):
        yield from self.laser_sweep_damage.dependencies_for(asset_manager)

    def _dependencies_for_laser_sweep_beam_info(self, asset_manager):
        yield from self.laser_sweep_beam_info.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct42(self, asset_manager):
        yield from self.unknown_struct42.dependencies_for(asset_manager)

    def _dependencies_for_sound_laser_sweep(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_laser_sweep)

    def _dependencies_for_sound_laser_charge_up(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_laser_charge_up)

    def _dependencies_for_sound_docking(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_docking)

    def _dependencies_for_sound_scanning(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_scanning)

    def _dependencies_for_sound_shield_on(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_shield_on)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def _dependencies_for_light_shield_vulnerability(self, asset_manager):
        yield from self.light_shield_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_dark_shield_vulnerability(self, asset_manager):
        yield from self.dark_shield_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_laser_pulse_projectile, "laser_pulse_projectile", "AssetId"),
            (self._dependencies_for_laser_pulse_damage, "laser_pulse_damage", "DamageInfo"),
            (self._dependencies_for_laser_sweep_damage, "laser_sweep_damage", "DamageInfo"),
            (self._dependencies_for_laser_sweep_beam_info, "laser_sweep_beam_info", "PlasmaBeamInfo"),
            (self._dependencies_for_unknown_struct42, "unknown_struct42", "UnknownStruct42"),
            (self._dependencies_for_sound_laser_sweep, "sound_laser_sweep", "int"),
            (self._dependencies_for_sound_laser_charge_up, "sound_laser_charge_up", "int"),
            (self._dependencies_for_sound_docking, "sound_docking", "int"),
            (self._dependencies_for_sound_scanning, "sound_scanning", "int"),
            (self._dependencies_for_sound_shield_on, "sound_shield_on", "int"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
            (self._dependencies_for_light_shield_vulnerability, "light_shield_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_dark_shield_vulnerability, "dark_shield_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct43.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0xbd80fd94(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_linear_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scanning_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe32fcae9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc5e0b92c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc17a8806(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe75bae9e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_laser_pulse_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_laser_pulse_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0})


def _decode_unknown_0xeda45014(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7dd740fe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dodge_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reset_shield_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_split_destroyed_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_laser_sweep_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_laser_sweep_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0})


def _decode_laser_sweep_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})


def _decode_unknown_struct42(data: typing.BinaryIO, property_size: int):
    return UnknownStruct42.from_stream(data, property_size)


def _decode_sound_laser_sweep(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_laser_charge_up(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_docking(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_scanning(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_light_shield(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_dark_shield(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_shield_on(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_light_shield_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_dark_shield_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbd80fd94: ('unknown_0xbd80fd94', _decode_unknown_0xbd80fd94),
    0xd74fc3: ('max_linear_velocity', _decode_max_linear_velocity),
    0xb5c3c1a: ('max_turn_speed', _decode_max_turn_speed),
    0xa0b3e1be: ('scanning_turn_speed', _decode_scanning_turn_speed),
    0xe32fcae9: ('unknown_0xe32fcae9', _decode_unknown_0xe32fcae9),
    0xc5e0b92c: ('unknown_0xc5e0b92c', _decode_unknown_0xc5e0b92c),
    0xc17a8806: ('unknown_0xc17a8806', _decode_unknown_0xc17a8806),
    0xe75bae9e: ('unknown_0xe75bae9e', _decode_unknown_0xe75bae9e),
    0x4d77b7aa: ('laser_pulse_projectile', _decode_laser_pulse_projectile),
    0xb763eb10: ('laser_pulse_damage', _decode_laser_pulse_damage),
    0xeda45014: ('unknown_0xeda45014', _decode_unknown_0xeda45014),
    0x7dd740fe: ('unknown_0x7dd740fe', _decode_unknown_0x7dd740fe),
    0x47be3298: ('dodge_chance', _decode_dodge_chance),
    0xd3dec6dc: ('reset_shield_time', _decode_reset_shield_time),
    0xecd9d92d: ('split_destroyed_priority', _decode_split_destroyed_priority),
    0x5ff006d1: ('laser_sweep_turn_speed', _decode_laser_sweep_turn_speed),
    0x1bd017ce: ('laser_sweep_damage', _decode_laser_sweep_damage),
    0x4a37c437: ('laser_sweep_beam_info', _decode_laser_sweep_beam_info),
    0x9ec51fe4: ('unknown_struct42', _decode_unknown_struct42),
    0xea307548: ('sound_laser_sweep', _decode_sound_laser_sweep),
    0x3779bd93: ('sound_laser_charge_up', _decode_sound_laser_charge_up),
    0xc90dbdb4: ('sound_docking', _decode_sound_docking),
    0xe7724802: ('sound_scanning', _decode_sound_scanning),
    0xd4a06273: ('sound_light_shield', _decode_sound_light_shield),
    0xafc20631: ('sound_dark_shield', _decode_sound_dark_shield),
    0x2ff5a809: ('sound_shield_on', _decode_sound_shield_on),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0x80a8ef3b: ('light_shield_vulnerability', _decode_light_shield_vulnerability),
    0xa21c90ea: ('dark_shield_vulnerability', _decode_dark_shield_vulnerability),
}
