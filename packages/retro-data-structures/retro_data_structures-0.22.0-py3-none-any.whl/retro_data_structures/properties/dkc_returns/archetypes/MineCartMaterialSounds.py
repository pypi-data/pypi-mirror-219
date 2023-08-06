# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MaterialType import MaterialType
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class MineCartMaterialSounds(BaseProperty):
    material: MaterialType = dataclasses.field(default_factory=MaterialType)
    rolling_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rolling_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound2: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rolling_sound2_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound2_pitch: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound2_volume: Spline = dataclasses.field(default_factory=Spline)
    jump_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    land_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xd7.\t\xe1')  # 0xd72e09e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xb1\xad\xd6')  # 0x36b1add6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rolling_sound))

        data.write(b'\xef\xe4y\x8f')  # 0xefe4798f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96\xd4\xf7\x8b')  # 0x96d4f78b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x00\x1e\r')  # 0x15001e0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\xa61\x00')  # 0xe3a63100
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rolling_sound2))

        data.write(b';\x01l\xfa')  # 0x3b016cfa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xc9ZU')  # 0xc95a55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\xfd\xfcs')  # 0x74fdfc73
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xe6`\xaf')  # 0xebe660af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jump_sound))

        data.write(b'\x0e+\x82\xec')  # 0xe2b82ec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.land_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            material=MaterialType.from_json(data['material']),
            rolling_sound=data['rolling_sound'],
            rolling_sound_low_pass_filter=Spline.from_json(data['rolling_sound_low_pass_filter']),
            rolling_sound_pitch=Spline.from_json(data['rolling_sound_pitch']),
            rolling_sound_volume=Spline.from_json(data['rolling_sound_volume']),
            rolling_sound2=data['rolling_sound2'],
            rolling_sound2_low_pass_filter=Spline.from_json(data['rolling_sound2_low_pass_filter']),
            rolling_sound2_pitch=Spline.from_json(data['rolling_sound2_pitch']),
            rolling_sound2_volume=Spline.from_json(data['rolling_sound2_volume']),
            jump_sound=data['jump_sound'],
            land_sound=data['land_sound'],
        )

    def to_json(self) -> dict:
        return {
            'material': self.material.to_json(),
            'rolling_sound': self.rolling_sound,
            'rolling_sound_low_pass_filter': self.rolling_sound_low_pass_filter.to_json(),
            'rolling_sound_pitch': self.rolling_sound_pitch.to_json(),
            'rolling_sound_volume': self.rolling_sound_volume.to_json(),
            'rolling_sound2': self.rolling_sound2,
            'rolling_sound2_low_pass_filter': self.rolling_sound2_low_pass_filter.to_json(),
            'rolling_sound2_pitch': self.rolling_sound2_pitch.to_json(),
            'rolling_sound2_volume': self.rolling_sound2_volume.to_json(),
            'jump_sound': self.jump_sound,
            'land_sound': self.land_sound,
        }


def _decode_material(data: typing.BinaryIO, property_size: int):
    return MaterialType.from_stream(data, property_size)


def _decode_rolling_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rolling_sound_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rolling_sound2_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound2_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound2_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_jump_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_land_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd72e09e1: ('material', _decode_material),
    0x36b1add6: ('rolling_sound', _decode_rolling_sound),
    0xefe4798f: ('rolling_sound_low_pass_filter', _decode_rolling_sound_low_pass_filter),
    0x96d4f78b: ('rolling_sound_pitch', _decode_rolling_sound_pitch),
    0x15001e0d: ('rolling_sound_volume', _decode_rolling_sound_volume),
    0xe3a63100: ('rolling_sound2', _decode_rolling_sound2),
    0x3b016cfa: ('rolling_sound2_low_pass_filter', _decode_rolling_sound2_low_pass_filter),
    0xc95a55: ('rolling_sound2_pitch', _decode_rolling_sound2_pitch),
    0x74fdfc73: ('rolling_sound2_volume', _decode_rolling_sound2_volume),
    0xebe660af: ('jump_sound', _decode_jump_sound),
    0xe2b82ec: ('land_sound', _decode_land_sound),
}
