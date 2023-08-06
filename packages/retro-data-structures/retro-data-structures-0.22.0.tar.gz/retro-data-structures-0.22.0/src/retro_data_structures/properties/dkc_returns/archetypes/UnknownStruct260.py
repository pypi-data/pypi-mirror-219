# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct260(BaseProperty):
    unknown_0x348c9d90: float = dataclasses.field(default=20.0)
    flight_sound_deceleration_k: float = dataclasses.field(default=1.0)
    flight_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    flight_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    flight_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    flight_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    caud_0xb0c2f5f6: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xbd894993: Spline = dataclasses.field(default_factory=Spline)
    flight_sound2_pitch: Spline = dataclasses.field(default_factory=Spline)
    flight_sound2_volume: Spline = dataclasses.field(default_factory=Spline)
    hit_player_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xc8b23273: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    swoop_interrupted_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'4\x8c\x9d\x90')  # 0x348c9d90
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x348c9d90))

        data.write(b'z}\xf6\xe3')  # 0x7a7df6e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_sound_deceleration_k))

        data.write(b'\xe1\xe6k$')  # 0xe1e66b24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flight_sound))

        data.write(b'\xb4\x13\xc4_')  # 0xb413c45f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xc7FL')  # 0x76c7464c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\xe0Z\xaf')  # 0x10e05aaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xc2\xf5\xf6')  # 0xb0c2f5f6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xb0c2f5f6))

        data.write(b'\xbd\x89I\x93')  # 0xbd894993
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbd894993.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05)\x1e\xf7')  # 0x5291ef7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound2_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'L \xde\xf3')  # 0x4c20def3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound2_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%\x9c\t9')  # 0x259c0939
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hit_player_sound))

        data.write(b'\xc8\xb22s')  # 0xc8b23273
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xc8b23273))

        data.write(b'\xbe_\x11\x8d')  # 0xbe5f118d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.swoop_interrupted_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x348c9d90=data['unknown_0x348c9d90'],
            flight_sound_deceleration_k=data['flight_sound_deceleration_k'],
            flight_sound=data['flight_sound'],
            flight_sound_low_pass_filter=Spline.from_json(data['flight_sound_low_pass_filter']),
            flight_sound_pitch=Spline.from_json(data['flight_sound_pitch']),
            flight_sound_volume=Spline.from_json(data['flight_sound_volume']),
            caud_0xb0c2f5f6=data['caud_0xb0c2f5f6'],
            unknown_0xbd894993=Spline.from_json(data['unknown_0xbd894993']),
            flight_sound2_pitch=Spline.from_json(data['flight_sound2_pitch']),
            flight_sound2_volume=Spline.from_json(data['flight_sound2_volume']),
            hit_player_sound=data['hit_player_sound'],
            caud_0xc8b23273=data['caud_0xc8b23273'],
            swoop_interrupted_sound=data['swoop_interrupted_sound'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x348c9d90': self.unknown_0x348c9d90,
            'flight_sound_deceleration_k': self.flight_sound_deceleration_k,
            'flight_sound': self.flight_sound,
            'flight_sound_low_pass_filter': self.flight_sound_low_pass_filter.to_json(),
            'flight_sound_pitch': self.flight_sound_pitch.to_json(),
            'flight_sound_volume': self.flight_sound_volume.to_json(),
            'caud_0xb0c2f5f6': self.caud_0xb0c2f5f6,
            'unknown_0xbd894993': self.unknown_0xbd894993.to_json(),
            'flight_sound2_pitch': self.flight_sound2_pitch.to_json(),
            'flight_sound2_volume': self.flight_sound2_volume.to_json(),
            'hit_player_sound': self.hit_player_sound,
            'caud_0xc8b23273': self.caud_0xc8b23273,
            'swoop_interrupted_sound': self.swoop_interrupted_sound,
        }


def _decode_unknown_0x348c9d90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound_deceleration_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flight_sound_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flight_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flight_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_caud_0xb0c2f5f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xbd894993(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flight_sound2_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flight_sound2_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_hit_player_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xc8b23273(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_swoop_interrupted_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x348c9d90: ('unknown_0x348c9d90', _decode_unknown_0x348c9d90),
    0x7a7df6e3: ('flight_sound_deceleration_k', _decode_flight_sound_deceleration_k),
    0xe1e66b24: ('flight_sound', _decode_flight_sound),
    0xb413c45f: ('flight_sound_low_pass_filter', _decode_flight_sound_low_pass_filter),
    0x76c7464c: ('flight_sound_pitch', _decode_flight_sound_pitch),
    0x10e05aaf: ('flight_sound_volume', _decode_flight_sound_volume),
    0xb0c2f5f6: ('caud_0xb0c2f5f6', _decode_caud_0xb0c2f5f6),
    0xbd894993: ('unknown_0xbd894993', _decode_unknown_0xbd894993),
    0x5291ef7: ('flight_sound2_pitch', _decode_flight_sound2_pitch),
    0x4c20def3: ('flight_sound2_volume', _decode_flight_sound2_volume),
    0x259c0939: ('hit_player_sound', _decode_hit_player_sound),
    0xc8b23273: ('caud_0xc8b23273', _decode_caud_0xc8b23273),
    0xbe5f118d: ('swoop_interrupted_sound', _decode_swoop_interrupted_sound),
}
