# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class MoleCartStruct(BaseProperty):
    spline_input: int = dataclasses.field(default=1306613276)  # Choice
    max_angle: float = dataclasses.field(default=45.0)
    unknown_0x61dd3eb6: float = dataclasses.field(default=45.0)
    fade_in_time: float = dataclasses.field(default=0.5)
    sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x8a939379: Spline = dataclasses.field(default_factory=Spline)
    pitch: Spline = dataclasses.field(default_factory=Spline)
    volume: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'j\x06\xfa\xee')  # 0x6a06faee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.spline_input))

        data.write(b'\xd9cU\x83')  # 0xd9635583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_angle))

        data.write(b'a\xdd>\xb6')  # 0x61dd3eb6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61dd3eb6))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'\xa5]\xac\xf6')  # 0xa55dacf6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound))

        data.write(b'\x8a\x93\x93y')  # 0x8a939379
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x8a939379.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0er\x7f\xc4')  # 0xe727fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xfb\xe4\x84')  # 0xf3fbe484
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            spline_input=data['spline_input'],
            max_angle=data['max_angle'],
            unknown_0x61dd3eb6=data['unknown_0x61dd3eb6'],
            fade_in_time=data['fade_in_time'],
            sound=data['sound'],
            unknown_0x8a939379=Spline.from_json(data['unknown_0x8a939379']),
            pitch=Spline.from_json(data['pitch']),
            volume=Spline.from_json(data['volume']),
        )

    def to_json(self) -> dict:
        return {
            'spline_input': self.spline_input,
            'max_angle': self.max_angle,
            'unknown_0x61dd3eb6': self.unknown_0x61dd3eb6,
            'fade_in_time': self.fade_in_time,
            'sound': self.sound,
            'unknown_0x8a939379': self.unknown_0x8a939379.to_json(),
            'pitch': self.pitch.to_json(),
            'volume': self.volume.to_json(),
        }


def _decode_spline_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61dd3eb6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x8a939379(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6a06faee: ('spline_input', _decode_spline_input),
    0xd9635583: ('max_angle', _decode_max_angle),
    0x61dd3eb6: ('unknown_0x61dd3eb6', _decode_unknown_0x61dd3eb6),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0xa55dacf6: ('sound', _decode_sound),
    0x8a939379: ('unknown_0x8a939379', _decode_unknown_0x8a939379),
    0xe727fc4: ('pitch', _decode_pitch),
    0xf3fbe484: ('volume', _decode_volume),
}
