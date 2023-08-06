# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MaterialSoundPair import MaterialSoundPair
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class KongSlideData(BaseProperty):
    slope_detection_angle: float = dataclasses.field(default=20.0)
    slide_no_jump_angle: float = dataclasses.field(default=70.0)
    slide_detection_angle: float = dataclasses.field(default=54.0)
    scramble_detection_angle: float = dataclasses.field(default=20.0)
    scramble_speed: float = dataclasses.field(default=4.0)
    tar_scramble_speed: float = dataclasses.field(default=4.0)
    slide_breaking_speed: float = dataclasses.field(default=7.0)
    max_slide_speed: float = dataclasses.field(default=15.0)
    scramble_recovery_acceleration: float = dataclasses.field(default=40.0)
    slide_speedup_acceleration: float = dataclasses.field(default=40.0)
    slide_slowdown_acceleration: float = dataclasses.field(default=20.0)
    planar_slide_recovery_speed: float = dataclasses.field(default=0.10000000149011612)
    slide_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    slide_sound_ratio_change_factor: float = dataclasses.field(default=0.5)
    slide_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    slide_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    slide_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    num_material_sounds: int = dataclasses.field(default=0)
    material_sound0: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound1: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound2: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound3: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound4: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound5: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound6: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound7: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound8: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)
    material_sound9: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x1c')  # 28 properties

        data.write(b'N}\xef~')  # 0x4e7def7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slope_detection_angle))

        data.write(b'\x18\xaa\\t')  # 0x18aa5c74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_no_jump_angle))

        data.write(b'e\x91\xa3\xa9')  # 0x6591a3a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_detection_angle))

        data.write(b'\x8f\x7f\xddo')  # 0x8f7fdd6f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scramble_detection_angle))

        data.write(b'C\x84\x99\x00')  # 0x43849900
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scramble_speed))

        data.write(b'\x8e~\xa4\xfc')  # 0x8e7ea4fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tar_scramble_speed))

        data.write(b'\x8f;\x93(')  # 0x8f3b9328
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_breaking_speed))

        data.write(b'Ln\xc5\x11')  # 0x4c6ec511
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_slide_speed))

        data.write(b's5\x08M')  # 0x7335084d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scramble_recovery_acceleration))

        data.write(b'v\x00\xa6\xc5')  # 0x7600a6c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_speedup_acceleration))

        data.write(b'\x8fs\xe7=')  # 0x8f73e73d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_slowdown_acceleration))

        data.write(b'\xce\x00x\x90')  # 0xce007890
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.planar_slide_recovery_speed))

        data.write(b'+y\xea\x93')  # 0x2b79ea93
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.slide_sound))

        data.write(b'\xba0\xaa\xca')  # 0xba30aaca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_sound_ratio_change_factor))

        data.write(b'\xd9\xcaP\xc2')  # 0xd9ca50c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84\x95\x1e\xc7')  # 0x84951ec7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jxR_')  # 0x6a78525f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7\xc1\x91A')  # 0xd7c19141
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_material_sounds))

        data.write(b'Wm\x99F')  # 0x576d9946
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8?/\xa7')  # 0xb83f2fa7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'R\xb9\xf2\xc5')  # 0x52b9f2c5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\xebD$')  # 0xbdeb4424
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\xc5N@')  # 0x5cc54e40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\x97\xf8\xa1')  # 0xb397f8a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x11%\xc3')  # 0x591125c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6C\x93"')  # 0xb6439322
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@<7J')  # 0x403c374a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xafn\x81\xab')  # 0xaf6e81ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            slope_detection_angle=data['slope_detection_angle'],
            slide_no_jump_angle=data['slide_no_jump_angle'],
            slide_detection_angle=data['slide_detection_angle'],
            scramble_detection_angle=data['scramble_detection_angle'],
            scramble_speed=data['scramble_speed'],
            tar_scramble_speed=data['tar_scramble_speed'],
            slide_breaking_speed=data['slide_breaking_speed'],
            max_slide_speed=data['max_slide_speed'],
            scramble_recovery_acceleration=data['scramble_recovery_acceleration'],
            slide_speedup_acceleration=data['slide_speedup_acceleration'],
            slide_slowdown_acceleration=data['slide_slowdown_acceleration'],
            planar_slide_recovery_speed=data['planar_slide_recovery_speed'],
            slide_sound=data['slide_sound'],
            slide_sound_ratio_change_factor=data['slide_sound_ratio_change_factor'],
            slide_sound_low_pass_filter=Spline.from_json(data['slide_sound_low_pass_filter']),
            slide_sound_pitch=Spline.from_json(data['slide_sound_pitch']),
            slide_sound_volume=Spline.from_json(data['slide_sound_volume']),
            num_material_sounds=data['num_material_sounds'],
            material_sound0=MaterialSoundPair.from_json(data['material_sound0']),
            material_sound1=MaterialSoundPair.from_json(data['material_sound1']),
            material_sound2=MaterialSoundPair.from_json(data['material_sound2']),
            material_sound3=MaterialSoundPair.from_json(data['material_sound3']),
            material_sound4=MaterialSoundPair.from_json(data['material_sound4']),
            material_sound5=MaterialSoundPair.from_json(data['material_sound5']),
            material_sound6=MaterialSoundPair.from_json(data['material_sound6']),
            material_sound7=MaterialSoundPair.from_json(data['material_sound7']),
            material_sound8=MaterialSoundPair.from_json(data['material_sound8']),
            material_sound9=MaterialSoundPair.from_json(data['material_sound9']),
        )

    def to_json(self) -> dict:
        return {
            'slope_detection_angle': self.slope_detection_angle,
            'slide_no_jump_angle': self.slide_no_jump_angle,
            'slide_detection_angle': self.slide_detection_angle,
            'scramble_detection_angle': self.scramble_detection_angle,
            'scramble_speed': self.scramble_speed,
            'tar_scramble_speed': self.tar_scramble_speed,
            'slide_breaking_speed': self.slide_breaking_speed,
            'max_slide_speed': self.max_slide_speed,
            'scramble_recovery_acceleration': self.scramble_recovery_acceleration,
            'slide_speedup_acceleration': self.slide_speedup_acceleration,
            'slide_slowdown_acceleration': self.slide_slowdown_acceleration,
            'planar_slide_recovery_speed': self.planar_slide_recovery_speed,
            'slide_sound': self.slide_sound,
            'slide_sound_ratio_change_factor': self.slide_sound_ratio_change_factor,
            'slide_sound_low_pass_filter': self.slide_sound_low_pass_filter.to_json(),
            'slide_sound_pitch': self.slide_sound_pitch.to_json(),
            'slide_sound_volume': self.slide_sound_volume.to_json(),
            'num_material_sounds': self.num_material_sounds,
            'material_sound0': self.material_sound0.to_json(),
            'material_sound1': self.material_sound1.to_json(),
            'material_sound2': self.material_sound2.to_json(),
            'material_sound3': self.material_sound3.to_json(),
            'material_sound4': self.material_sound4.to_json(),
            'material_sound5': self.material_sound5.to_json(),
            'material_sound6': self.material_sound6.to_json(),
            'material_sound7': self.material_sound7.to_json(),
            'material_sound8': self.material_sound8.to_json(),
            'material_sound9': self.material_sound9.to_json(),
        }


def _decode_slope_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_no_jump_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scramble_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scramble_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tar_scramble_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_breaking_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_slide_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scramble_recovery_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_speedup_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_slowdown_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_planar_slide_recovery_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_slide_sound_ratio_change_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_sound_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_slide_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_slide_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_num_material_sounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_material_sound0(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound1(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound2(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound3(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound4(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound5(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound6(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound7(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound8(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


def _decode_material_sound9(data: typing.BinaryIO, property_size: int):
    return MaterialSoundPair.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4e7def7e: ('slope_detection_angle', _decode_slope_detection_angle),
    0x18aa5c74: ('slide_no_jump_angle', _decode_slide_no_jump_angle),
    0x6591a3a9: ('slide_detection_angle', _decode_slide_detection_angle),
    0x8f7fdd6f: ('scramble_detection_angle', _decode_scramble_detection_angle),
    0x43849900: ('scramble_speed', _decode_scramble_speed),
    0x8e7ea4fc: ('tar_scramble_speed', _decode_tar_scramble_speed),
    0x8f3b9328: ('slide_breaking_speed', _decode_slide_breaking_speed),
    0x4c6ec511: ('max_slide_speed', _decode_max_slide_speed),
    0x7335084d: ('scramble_recovery_acceleration', _decode_scramble_recovery_acceleration),
    0x7600a6c5: ('slide_speedup_acceleration', _decode_slide_speedup_acceleration),
    0x8f73e73d: ('slide_slowdown_acceleration', _decode_slide_slowdown_acceleration),
    0xce007890: ('planar_slide_recovery_speed', _decode_planar_slide_recovery_speed),
    0x2b79ea93: ('slide_sound', _decode_slide_sound),
    0xba30aaca: ('slide_sound_ratio_change_factor', _decode_slide_sound_ratio_change_factor),
    0xd9ca50c2: ('slide_sound_low_pass_filter', _decode_slide_sound_low_pass_filter),
    0x84951ec7: ('slide_sound_pitch', _decode_slide_sound_pitch),
    0x6a78525f: ('slide_sound_volume', _decode_slide_sound_volume),
    0xd7c19141: ('num_material_sounds', _decode_num_material_sounds),
    0x576d9946: ('material_sound0', _decode_material_sound0),
    0xb83f2fa7: ('material_sound1', _decode_material_sound1),
    0x52b9f2c5: ('material_sound2', _decode_material_sound2),
    0xbdeb4424: ('material_sound3', _decode_material_sound3),
    0x5cc54e40: ('material_sound4', _decode_material_sound4),
    0xb397f8a1: ('material_sound5', _decode_material_sound5),
    0x591125c3: ('material_sound6', _decode_material_sound6),
    0xb6439322: ('material_sound7', _decode_material_sound7),
    0x403c374a: ('material_sound8', _decode_material_sound8),
    0xaf6e81ab: ('material_sound9', _decode_material_sound9),
}
