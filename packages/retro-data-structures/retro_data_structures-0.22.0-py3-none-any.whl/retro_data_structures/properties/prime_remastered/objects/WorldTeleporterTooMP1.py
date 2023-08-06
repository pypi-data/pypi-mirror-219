# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime_remastered.archetypes.AnimSetMP1 import AnimSetMP1
from retro_data_structures.properties.prime_remastered.archetypes.VectorMP1 import VectorMP1
from retro_data_structures.properties.prime_remastered.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime_remastered.core.PooledString import PooledString
import uuid


@dataclasses.dataclass()
class WorldTeleporterTooMP1(BaseProperty):
    world: AssetId = dataclasses.field(metadata={'asset_types': ['ROOM']}, default=default_asset_id)
    area: AssetId = dataclasses.field(metadata={'asset_types': ['ROOM']}, default=default_asset_id)
    animation_information: AnimSetMP1 = dataclasses.field(default_factory=AnimSetMP1)
    player_scale: VectorMP1 = dataclasses.field(default_factory=VectorMP1)
    platform: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    platform_scale: VectorMP1 = dataclasses.field(default_factory=VectorMP1)
    shaft_scale: VectorMP1 = dataclasses.field(default_factory=VectorMP1)
    unk_str: PooledString = dataclasses.field(default_factory=PooledString)
    unk_bool1: bool = dataclasses.field(default=True)
    sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    volume: int = dataclasses.field(default=127)
    upward_elevator: bool = dataclasses.field(default=False)
    text: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    pan: int = dataclasses.field(default=64)
    unk_bool2: bool = dataclasses.field(default=False)
    char_fade_in_time: float = dataclasses.field(default=0.009999999776482582)
    chars_per_second: float = dataclasses.field(default=8.0)
    delay_before_show: float = dataclasses.field(default=0.0)
    show_text_instead_of_cutscene: bool = dataclasses.field(default=False)
    unk_float1: float = dataclasses.field(default=0.0)
    unk_float2: float = dataclasses.field(default=2.0)
    unk_float3: float = dataclasses.field(default=3.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack("<LH", data.read(6))
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
        data.write(b'\x06\x00')  # 6 properties
        num_properties_written = 6

        data.write(b'\x7fQ\x9a\xd4')  # 0xd49a517f
        data.write(b'\x10\x00')  # size
        data.write(self.world.bytes_le)

        data.write(b'l\xfb_\x9a')  # 0x9a5ffb6c
        data.write(b'\x10\x00')  # size
        data.write(self.area.bytes_le)

        data.write(b'r\xee\xeaj')  # 0x6aeaee72
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        data.write(b'yfS\xc2')  # 0xc2536679
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        if self.platform != default_override.get('platform', default_asset_id):
            num_properties_written += 1
            data.write(b'\x8e\x1f\xb3\xa7')  # 0xa7b31f8e
            data.write(b'\x10\x00')  # size
            data.write(self.platform.bytes_le)

        data.write(b'!\xe8\xb5O')  # 0x4fb5e821
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.platform_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        data.write(b'*\xe6:\xbb')  # 0xbb3ae62a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shaft_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        if self.unk_str != default_override.get('unk_str', PooledString()):
            num_properties_written += 1
            data.write(b',N\xd5\xb8')  # 0xb8d54e2c
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.unk_str.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack("<H", after - before - 2))
            data.seek(after)

        if self.unk_bool1 != default_override.get('unk_bool1', True):
            num_properties_written += 1
            data.write(b'\t\x1c\x93\xa6')  # 0xa6931c09
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unk_bool1))

        if self.sound != default_override.get('sound', default_asset_id):
            num_properties_written += 1
            data.write(b'#\xbb\x07T')  # 0x5407bb23
            data.write(b'\x10\x00')  # size
            data.write(self.sound.bytes_le)

        if self.volume != default_override.get('volume', 127):
            num_properties_written += 1
            data.write(b'pR\x95\x82')  # 0x82955270
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<l', self.volume))

        if self.upward_elevator != default_override.get('upward_elevator', False):
            num_properties_written += 1
            data.write(b'\xa7>\xfa\x03')  # 0x3fa3ea7
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.upward_elevator))

        if self.text != default_override.get('text', default_asset_id):
            num_properties_written += 1
            data.write(b'\xe83\x0b\x98')  # 0x980b33e8
            data.write(b'\x10\x00')  # size
            data.write(self.text.bytes_le)

        if self.pan != default_override.get('pan', 64):
            num_properties_written += 1
            data.write(b'\xff5\x8c\x83')  # 0x838c35ff
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<l', self.pan))

        if self.unk_bool2 != default_override.get('unk_bool2', False):
            num_properties_written += 1
            data.write(b'\xad;.\x95')  # 0x952e3bad
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unk_bool2))

        if self.char_fade_in_time != default_override.get('char_fade_in_time', 0.009999999776482582):
            num_properties_written += 1
            data.write(b'\x9d\xf0XU')  # 0x5558f09d
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.char_fade_in_time))

        if self.chars_per_second != default_override.get('chars_per_second', 8.0):
            num_properties_written += 1
            data.write(b'\xe9h\xfc\xee')  # 0xeefc68e9
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.chars_per_second))

        if self.delay_before_show != default_override.get('delay_before_show', 0.0):
            num_properties_written += 1
            data.write(b'\r\xd96\xa9')  # 0xa936d90d
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.delay_before_show))

        if self.show_text_instead_of_cutscene != default_override.get('show_text_instead_of_cutscene', False):
            num_properties_written += 1
            data.write(b'\x03\xa0h\x1b')  # 0x1b68a003
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.show_text_instead_of_cutscene))

        if self.unk_float1 != default_override.get('unk_float1', 0.0):
            num_properties_written += 1
            data.write(b'Ku\xb5S')  # 0x53b5754b
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.unk_float1))

        if self.unk_float2 != default_override.get('unk_float2', 2.0):
            num_properties_written += 1
            data.write(b'\xd4Gs\x97')  # 0x977347d4
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.unk_float2))

        if self.unk_float3 != default_override.get('unk_float3', 3.0):
            num_properties_written += 1
            data.write(b'\x03\xe85\xdc')  # 0xdc35e803
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.unk_float3))

        if num_properties_written != 6:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            world=uuid.UUID(data['world']),
            area=uuid.UUID(data['area']),
            animation_information=AnimSetMP1.from_json(data['animation_information']),
            player_scale=VectorMP1.from_json(data['player_scale']),
            platform=uuid.UUID(data['platform']),
            platform_scale=VectorMP1.from_json(data['platform_scale']),
            shaft_scale=VectorMP1.from_json(data['shaft_scale']),
            unk_str=PooledString.from_json(data['unk_str']),
            unk_bool1=data['unk_bool1'],
            sound=uuid.UUID(data['sound']),
            volume=data['volume'],
            upward_elevator=data['upward_elevator'],
            text=uuid.UUID(data['text']),
            pan=data['pan'],
            unk_bool2=data['unk_bool2'],
            char_fade_in_time=data['char_fade_in_time'],
            chars_per_second=data['chars_per_second'],
            delay_before_show=data['delay_before_show'],
            show_text_instead_of_cutscene=data['show_text_instead_of_cutscene'],
            unk_float1=data['unk_float1'],
            unk_float2=data['unk_float2'],
            unk_float3=data['unk_float3'],
        )

    def to_json(self) -> dict:
        return {
            'world': str(self.world),
            'area': str(self.area),
            'animation_information': self.animation_information.to_json(),
            'player_scale': self.player_scale.to_json(),
            'platform': str(self.platform),
            'platform_scale': self.platform_scale.to_json(),
            'shaft_scale': self.shaft_scale.to_json(),
            'unk_str': self.unk_str.to_json(),
            'unk_bool1': self.unk_bool1,
            'sound': str(self.sound),
            'volume': self.volume,
            'upward_elevator': self.upward_elevator,
            'text': str(self.text),
            'pan': self.pan,
            'unk_bool2': self.unk_bool2,
            'char_fade_in_time': self.char_fade_in_time,
            'chars_per_second': self.chars_per_second,
            'delay_before_show': self.delay_before_show,
            'show_text_instead_of_cutscene': self.show_text_instead_of_cutscene,
            'unk_float1': self.unk_float1,
            'unk_float2': self.unk_float2,
            'unk_float3': self.unk_float3,
        }


def _decode_world(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_area(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimSetMP1.from_stream(data, property_size)


def _decode_player_scale(data: typing.BinaryIO, property_size: int):
    return VectorMP1.from_stream(data, property_size)


def _decode_platform(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_platform_scale(data: typing.BinaryIO, property_size: int):
    return VectorMP1.from_stream(data, property_size)


def _decode_shaft_scale(data: typing.BinaryIO, property_size: int):
    return VectorMP1.from_stream(data, property_size)


def _decode_unk_str(data: typing.BinaryIO, property_size: int):
    return PooledString.from_stream(data, property_size)


def _decode_unk_bool1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<l', data.read(4))[0]


def _decode_upward_elevator(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_text(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_pan(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<l', data.read(4))[0]


def _decode_unk_bool2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_char_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_chars_per_second(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_delay_before_show(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_show_text_instead_of_cutscene(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_unk_float1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_unk_float2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_unk_float3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd49a517f: ('world', _decode_world),
    0x9a5ffb6c: ('area', _decode_area),
    0x6aeaee72: ('animation_information', _decode_animation_information),
    0xc2536679: ('player_scale', _decode_player_scale),
    0xa7b31f8e: ('platform', _decode_platform),
    0x4fb5e821: ('platform_scale', _decode_platform_scale),
    0xbb3ae62a: ('shaft_scale', _decode_shaft_scale),
    0xb8d54e2c: ('unk_str', _decode_unk_str),
    0xa6931c09: ('unk_bool1', _decode_unk_bool1),
    0x5407bb23: ('sound', _decode_sound),
    0x82955270: ('volume', _decode_volume),
    0x3fa3ea7: ('upward_elevator', _decode_upward_elevator),
    0x980b33e8: ('text', _decode_text),
    0x838c35ff: ('pan', _decode_pan),
    0x952e3bad: ('unk_bool2', _decode_unk_bool2),
    0x5558f09d: ('char_fade_in_time', _decode_char_fade_in_time),
    0xeefc68e9: ('chars_per_second', _decode_chars_per_second),
    0xa936d90d: ('delay_before_show', _decode_delay_before_show),
    0x1b68a003: ('show_text_instead_of_cutscene', _decode_show_text_instead_of_cutscene),
    0x53b5754b: ('unk_float1', _decode_unk_float1),
    0x977347d4: ('unk_float2', _decode_unk_float2),
    0xdc35e803: ('unk_float3', _decode_unk_float3),
}
