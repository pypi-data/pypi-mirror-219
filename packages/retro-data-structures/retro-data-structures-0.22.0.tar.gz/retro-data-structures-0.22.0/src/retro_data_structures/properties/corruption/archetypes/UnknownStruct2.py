# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.UnknownStruct6 import UnknownStruct6
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    camera_animation_info: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    overload_damage_threshold: float = dataclasses.field(default=100.0)
    open_hatch_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xa4b62aa9: float = dataclasses.field(default=3.0)
    unknown_0xb64ea21c: float = dataclasses.field(default=1.0)
    unknown_0xa13b1ba9: float = dataclasses.field(default=1.0)
    unknown_0xd294848c: float = dataclasses.field(default=0.5)
    unknown_0x9c425325: float = dataclasses.field(default=2.0)
    unknown_0xfa22836a: float = dataclasses.field(default=1.0)
    unknown_0xed410449: float = dataclasses.field(default=8.0)
    unknown_0xf768d625: float = dataclasses.field(default=0.0)
    tentacle_animation_info: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x52806eff: int = dataclasses.field(default=2)
    missile_weapon: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    missile_explode_threshold: float = dataclasses.field(default=100.0)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    missile_explode_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    fire_missile_time: float = dataclasses.field(default=6.75)
    unknown_0xa4166e3c: float = dataclasses.field(default=1.0)
    unknown_0xaa7d527d: float = dataclasses.field(default=50.0)
    unknown_0xf707c050: float = dataclasses.field(default=1.0)
    unknown_0x4128ff6d: float = dataclasses.field(default=0.5)
    unknown_0x3b6218da: float = dataclasses.field(default=0.25)
    unknown_0x71946eec: float = dataclasses.field(default=0.0)
    unknown_0xa184d013: float = dataclasses.field(default=3.5)
    unknown_0x09d9bd17: float = dataclasses.field(default=0.5)
    camera_sequence_duration: float = dataclasses.field(default=8.0)
    min_camera_sequences: int = dataclasses.field(default=1)
    max_camera_sequences: int = dataclasses.field(default=3)
    unknown_0x193c7751: float = dataclasses.field(default=1.5)
    unknown_0x0d55794a: float = dataclasses.field(default=0.0)
    unknown_0x72fb67da: float = dataclasses.field(default=50.0)
    camera_damage_threshold: float = dataclasses.field(default=10.0)
    camera_shock_time: float = dataclasses.field(default=30.0)
    dizzy_state_time: float = dataclasses.field(default=15.0)
    unknown_0x0a072c48: float = dataclasses.field(default=0.6000000238418579)
    unknown_0xdde5ac10: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x8c63f9d0: float = dataclasses.field(default=0.75)
    unknown_0x6b7e5f47: float = dataclasses.field(default=0.5)
    unknown_0x6afe0147: float = dataclasses.field(default=0.75)
    unknown_0x04721a06: float = dataclasses.field(default=0.5)
    unknown_struct6: UnknownStruct6 = dataclasses.field(default_factory=UnknownStruct6)

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
        num_properties_offset = data.tell()
        data.write(b'\x00*')  # 42 properties
        num_properties_written = 42

        data.write(b'\xc1\x07\xa4\x8a')  # 0xc107a48a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_animation_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6\xc4|\xd3')  # 0xa6c47cd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.overload_damage_threshold))

        data.write(b'\x0f\xce\x03\xca')  # 0xfce03ca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.open_hatch_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xb6*\xa9')  # 0xa4b62aa9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa4b62aa9))

        data.write(b'\xb6N\xa2\x1c')  # 0xb64ea21c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb64ea21c))

        data.write(b'\xa1;\x1b\xa9')  # 0xa13b1ba9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa13b1ba9))

        data.write(b'\xd2\x94\x84\x8c')  # 0xd294848c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd294848c))

        data.write(b'\x9cBS%')  # 0x9c425325
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9c425325))

        data.write(b'\xfa"\x83j')  # 0xfa22836a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfa22836a))

        data.write(b'\xedA\x04I')  # 0xed410449
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed410449))

        data.write(b'\xf7h\xd6%')  # 0xf768d625
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf768d625))

        data.write(b'\xa2)\xffj')  # 0xa229ff6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tentacle_animation_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'R\x80n\xff')  # 0x52806eff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x52806eff))

        data.write(b'.\xa3\x1f\x83')  # 0x2ea31f83
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.missile_weapon))

        data.write(b'%\x8c\xfbM')  # 0x258cfb4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{\xec\xdbf')  # 0x7becdb66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.missile_explode_threshold))

        data.write(b'\x87\xaf\xe8\xd8')  # 0x87afe8d8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'=\xfd\x1cO')  # 0x3dfd1c4f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.missile_explode_sound))

        data.write(b'\xb8\xbfV\x1e')  # 0xb8bf561e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fire_missile_time))

        data.write(b'\xa4\x16n<')  # 0xa4166e3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa4166e3c))

        data.write(b'\xaa}R}')  # 0xaa7d527d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaa7d527d))

        data.write(b'\xf7\x07\xc0P')  # 0xf707c050
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf707c050))

        data.write(b'A(\xffm')  # 0x4128ff6d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4128ff6d))

        data.write(b';b\x18\xda')  # 0x3b6218da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b6218da))

        data.write(b'q\x94n\xec')  # 0x71946eec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x71946eec))

        data.write(b'\xa1\x84\xd0\x13')  # 0xa184d013
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa184d013))

        data.write(b'\t\xd9\xbd\x17')  # 0x9d9bd17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x09d9bd17))

        data.write(b'S\xc1\xd0\x89')  # 0x53c1d089
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_sequence_duration))

        data.write(b'0o\xd3\x9a')  # 0x306fd39a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_camera_sequences))

        data.write(b'#*51')  # 0x232a3531
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_camera_sequences))

        data.write(b'\x19<wQ')  # 0x193c7751
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x193c7751))

        data.write(b'\rUyJ')  # 0xd55794a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0d55794a))

        data.write(b'r\xfbg\xda')  # 0x72fb67da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72fb67da))

        data.write(b'\xbd\xb1\x8b/')  # 0xbdb18b2f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_damage_threshold))

        data.write(b'\x0e\x95\x8d\x9e')  # 0xe958d9e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_shock_time))

        data.write(b'%\x1cU\xe3')  # 0x251c55e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dizzy_state_time))

        data.write(b'\n\x07,H')  # 0xa072c48
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a072c48))

        data.write(b'\xdd\xe5\xac\x10')  # 0xdde5ac10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdde5ac10))

        data.write(b'\x8cc\xf9\xd0')  # 0x8c63f9d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8c63f9d0))

        data.write(b'k~_G')  # 0x6b7e5f47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6b7e5f47))

        data.write(b'j\xfe\x01G')  # 0x6afe0147
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6afe0147))

        data.write(b'\x04r\x1a\x06')  # 0x4721a06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x04721a06))

        if self.unknown_struct6 != default_override.get('unknown_struct6', UnknownStruct6()):
            num_properties_written += 1
            data.write(b'\xd8W\x9b\xa3')  # 0xd8579ba3
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unknown_struct6.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if num_properties_written != 42:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack(">H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            camera_animation_info=AnimationParameters.from_json(data['camera_animation_info']),
            overload_damage_threshold=data['overload_damage_threshold'],
            open_hatch_vulnerability=DamageVulnerability.from_json(data['open_hatch_vulnerability']),
            unknown_0xa4b62aa9=data['unknown_0xa4b62aa9'],
            unknown_0xb64ea21c=data['unknown_0xb64ea21c'],
            unknown_0xa13b1ba9=data['unknown_0xa13b1ba9'],
            unknown_0xd294848c=data['unknown_0xd294848c'],
            unknown_0x9c425325=data['unknown_0x9c425325'],
            unknown_0xfa22836a=data['unknown_0xfa22836a'],
            unknown_0xed410449=data['unknown_0xed410449'],
            unknown_0xf768d625=data['unknown_0xf768d625'],
            tentacle_animation_info=AnimationParameters.from_json(data['tentacle_animation_info']),
            unknown_0x52806eff=data['unknown_0x52806eff'],
            missile_weapon=data['missile_weapon'],
            missile_damage=DamageInfo.from_json(data['missile_damage']),
            missile_explode_threshold=data['missile_explode_threshold'],
            part=data['part'],
            missile_explode_sound=data['missile_explode_sound'],
            fire_missile_time=data['fire_missile_time'],
            unknown_0xa4166e3c=data['unknown_0xa4166e3c'],
            unknown_0xaa7d527d=data['unknown_0xaa7d527d'],
            unknown_0xf707c050=data['unknown_0xf707c050'],
            unknown_0x4128ff6d=data['unknown_0x4128ff6d'],
            unknown_0x3b6218da=data['unknown_0x3b6218da'],
            unknown_0x71946eec=data['unknown_0x71946eec'],
            unknown_0xa184d013=data['unknown_0xa184d013'],
            unknown_0x09d9bd17=data['unknown_0x09d9bd17'],
            camera_sequence_duration=data['camera_sequence_duration'],
            min_camera_sequences=data['min_camera_sequences'],
            max_camera_sequences=data['max_camera_sequences'],
            unknown_0x193c7751=data['unknown_0x193c7751'],
            unknown_0x0d55794a=data['unknown_0x0d55794a'],
            unknown_0x72fb67da=data['unknown_0x72fb67da'],
            camera_damage_threshold=data['camera_damage_threshold'],
            camera_shock_time=data['camera_shock_time'],
            dizzy_state_time=data['dizzy_state_time'],
            unknown_0x0a072c48=data['unknown_0x0a072c48'],
            unknown_0xdde5ac10=data['unknown_0xdde5ac10'],
            unknown_0x8c63f9d0=data['unknown_0x8c63f9d0'],
            unknown_0x6b7e5f47=data['unknown_0x6b7e5f47'],
            unknown_0x6afe0147=data['unknown_0x6afe0147'],
            unknown_0x04721a06=data['unknown_0x04721a06'],
            unknown_struct6=UnknownStruct6.from_json(data['unknown_struct6']),
        )

    def to_json(self) -> dict:
        return {
            'camera_animation_info': self.camera_animation_info.to_json(),
            'overload_damage_threshold': self.overload_damage_threshold,
            'open_hatch_vulnerability': self.open_hatch_vulnerability.to_json(),
            'unknown_0xa4b62aa9': self.unknown_0xa4b62aa9,
            'unknown_0xb64ea21c': self.unknown_0xb64ea21c,
            'unknown_0xa13b1ba9': self.unknown_0xa13b1ba9,
            'unknown_0xd294848c': self.unknown_0xd294848c,
            'unknown_0x9c425325': self.unknown_0x9c425325,
            'unknown_0xfa22836a': self.unknown_0xfa22836a,
            'unknown_0xed410449': self.unknown_0xed410449,
            'unknown_0xf768d625': self.unknown_0xf768d625,
            'tentacle_animation_info': self.tentacle_animation_info.to_json(),
            'unknown_0x52806eff': self.unknown_0x52806eff,
            'missile_weapon': self.missile_weapon,
            'missile_damage': self.missile_damage.to_json(),
            'missile_explode_threshold': self.missile_explode_threshold,
            'part': self.part,
            'missile_explode_sound': self.missile_explode_sound,
            'fire_missile_time': self.fire_missile_time,
            'unknown_0xa4166e3c': self.unknown_0xa4166e3c,
            'unknown_0xaa7d527d': self.unknown_0xaa7d527d,
            'unknown_0xf707c050': self.unknown_0xf707c050,
            'unknown_0x4128ff6d': self.unknown_0x4128ff6d,
            'unknown_0x3b6218da': self.unknown_0x3b6218da,
            'unknown_0x71946eec': self.unknown_0x71946eec,
            'unknown_0xa184d013': self.unknown_0xa184d013,
            'unknown_0x09d9bd17': self.unknown_0x09d9bd17,
            'camera_sequence_duration': self.camera_sequence_duration,
            'min_camera_sequences': self.min_camera_sequences,
            'max_camera_sequences': self.max_camera_sequences,
            'unknown_0x193c7751': self.unknown_0x193c7751,
            'unknown_0x0d55794a': self.unknown_0x0d55794a,
            'unknown_0x72fb67da': self.unknown_0x72fb67da,
            'camera_damage_threshold': self.camera_damage_threshold,
            'camera_shock_time': self.camera_shock_time,
            'dizzy_state_time': self.dizzy_state_time,
            'unknown_0x0a072c48': self.unknown_0x0a072c48,
            'unknown_0xdde5ac10': self.unknown_0xdde5ac10,
            'unknown_0x8c63f9d0': self.unknown_0x8c63f9d0,
            'unknown_0x6b7e5f47': self.unknown_0x6b7e5f47,
            'unknown_0x6afe0147': self.unknown_0x6afe0147,
            'unknown_0x04721a06': self.unknown_0x04721a06,
            'unknown_struct6': self.unknown_struct6.to_json(),
        }


def _decode_camera_animation_info(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_overload_damage_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_open_hatch_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xa4b62aa9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb64ea21c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa13b1ba9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd294848c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9c425325(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfa22836a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed410449(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf768d625(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tentacle_animation_info(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x52806eff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_missile_weapon(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_missile_explode_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_missile_explode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fire_missile_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa4166e3c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xaa7d527d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf707c050(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4128ff6d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3b6218da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x71946eec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa184d013(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x09d9bd17(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_sequence_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_camera_sequences(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_camera_sequences(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x193c7751(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0d55794a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x72fb67da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_damage_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_shock_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dizzy_state_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0a072c48(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdde5ac10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8c63f9d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6b7e5f47(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6afe0147(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x04721a06(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct6(data: typing.BinaryIO, property_size: int):
    return UnknownStruct6.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc107a48a: ('camera_animation_info', _decode_camera_animation_info),
    0xa6c47cd3: ('overload_damage_threshold', _decode_overload_damage_threshold),
    0xfce03ca: ('open_hatch_vulnerability', _decode_open_hatch_vulnerability),
    0xa4b62aa9: ('unknown_0xa4b62aa9', _decode_unknown_0xa4b62aa9),
    0xb64ea21c: ('unknown_0xb64ea21c', _decode_unknown_0xb64ea21c),
    0xa13b1ba9: ('unknown_0xa13b1ba9', _decode_unknown_0xa13b1ba9),
    0xd294848c: ('unknown_0xd294848c', _decode_unknown_0xd294848c),
    0x9c425325: ('unknown_0x9c425325', _decode_unknown_0x9c425325),
    0xfa22836a: ('unknown_0xfa22836a', _decode_unknown_0xfa22836a),
    0xed410449: ('unknown_0xed410449', _decode_unknown_0xed410449),
    0xf768d625: ('unknown_0xf768d625', _decode_unknown_0xf768d625),
    0xa229ff6a: ('tentacle_animation_info', _decode_tentacle_animation_info),
    0x52806eff: ('unknown_0x52806eff', _decode_unknown_0x52806eff),
    0x2ea31f83: ('missile_weapon', _decode_missile_weapon),
    0x258cfb4d: ('missile_damage', _decode_missile_damage),
    0x7becdb66: ('missile_explode_threshold', _decode_missile_explode_threshold),
    0x87afe8d8: ('part', _decode_part),
    0x3dfd1c4f: ('missile_explode_sound', _decode_missile_explode_sound),
    0xb8bf561e: ('fire_missile_time', _decode_fire_missile_time),
    0xa4166e3c: ('unknown_0xa4166e3c', _decode_unknown_0xa4166e3c),
    0xaa7d527d: ('unknown_0xaa7d527d', _decode_unknown_0xaa7d527d),
    0xf707c050: ('unknown_0xf707c050', _decode_unknown_0xf707c050),
    0x4128ff6d: ('unknown_0x4128ff6d', _decode_unknown_0x4128ff6d),
    0x3b6218da: ('unknown_0x3b6218da', _decode_unknown_0x3b6218da),
    0x71946eec: ('unknown_0x71946eec', _decode_unknown_0x71946eec),
    0xa184d013: ('unknown_0xa184d013', _decode_unknown_0xa184d013),
    0x9d9bd17: ('unknown_0x09d9bd17', _decode_unknown_0x09d9bd17),
    0x53c1d089: ('camera_sequence_duration', _decode_camera_sequence_duration),
    0x306fd39a: ('min_camera_sequences', _decode_min_camera_sequences),
    0x232a3531: ('max_camera_sequences', _decode_max_camera_sequences),
    0x193c7751: ('unknown_0x193c7751', _decode_unknown_0x193c7751),
    0xd55794a: ('unknown_0x0d55794a', _decode_unknown_0x0d55794a),
    0x72fb67da: ('unknown_0x72fb67da', _decode_unknown_0x72fb67da),
    0xbdb18b2f: ('camera_damage_threshold', _decode_camera_damage_threshold),
    0xe958d9e: ('camera_shock_time', _decode_camera_shock_time),
    0x251c55e3: ('dizzy_state_time', _decode_dizzy_state_time),
    0xa072c48: ('unknown_0x0a072c48', _decode_unknown_0x0a072c48),
    0xdde5ac10: ('unknown_0xdde5ac10', _decode_unknown_0xdde5ac10),
    0x8c63f9d0: ('unknown_0x8c63f9d0', _decode_unknown_0x8c63f9d0),
    0x6b7e5f47: ('unknown_0x6b7e5f47', _decode_unknown_0x6b7e5f47),
    0x6afe0147: ('unknown_0x6afe0147', _decode_unknown_0x6afe0147),
    0x4721a06: ('unknown_0x04721a06', _decode_unknown_0x04721a06),
    0xd8579ba3: ('unknown_struct6', _decode_unknown_struct6),
}
