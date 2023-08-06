# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class SoundModifierData(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    time: float = dataclasses.field(default=5.0)
    fade_in_time: float = dataclasses.field(default=0.0)
    fade_out_time: float = dataclasses.field(default=0.0)
    auto_start: bool = dataclasses.field(default=False)
    loop: bool = dataclasses.field(default=False)
    loop_platform_contribution: bool = dataclasses.field(default=False)
    invert_platform_contribution: bool = dataclasses.field(default=False)
    volume: Spline = dataclasses.field(default_factory=Spline)
    pan: Spline = dataclasses.field(default_factory=Spline)
    surround_pan: Spline = dataclasses.field(default_factory=Spline)
    pitch: Spline = dataclasses.field(default_factory=Spline)
    low_pass: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SNMD'

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D3Z\xff')  # 0x44335aff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'\xa0\x93\x98E')  # 0xa0939845
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop_platform_contribution))

        data.write(b'V-a"')  # 0x562d6122
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.invert_platform_contribution))

        data.write(b'\xf3\xfb\xe4\x84')  # 0xf3fbe484
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(X\xc9\xf0')  # 0x2858c9f0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pan.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x13\x19\x8f')  # 0x5113198f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surround_pan.to_stream(data)
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

        data.write(b'\xd3\x04\x9e\x04')  # 0xd3049e04
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.low_pass.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            time=data['time'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
            auto_start=data['auto_start'],
            loop=data['loop'],
            loop_platform_contribution=data['loop_platform_contribution'],
            invert_platform_contribution=data['invert_platform_contribution'],
            volume=Spline.from_json(data['volume']),
            pan=Spline.from_json(data['pan']),
            surround_pan=Spline.from_json(data['surround_pan']),
            pitch=Spline.from_json(data['pitch']),
            low_pass=Spline.from_json(data['low_pass']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'time': self.time,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'auto_start': self.auto_start,
            'loop': self.loop,
            'loop_platform_contribution': self.loop_platform_contribution,
            'invert_platform_contribution': self.invert_platform_contribution,
            'volume': self.volume.to_json(),
            'pan': self.pan.to_json(),
            'surround_pan': self.surround_pan.to_json(),
            'pitch': self.pitch.to_json(),
            'low_pass': self.low_pass.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_platform_contribution(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_invert_platform_contribution(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_pan(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_surround_pan(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_low_pass(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x44335aff: ('time', _decode_time),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0xeda47ff6: ('loop', _decode_loop),
    0xa0939845: ('loop_platform_contribution', _decode_loop_platform_contribution),
    0x562d6122: ('invert_platform_contribution', _decode_invert_platform_contribution),
    0xf3fbe484: ('volume', _decode_volume),
    0x2858c9f0: ('pan', _decode_pan),
    0x5113198f: ('surround_pan', _decode_surround_pan),
    0xe727fc4: ('pitch', _decode_pitch),
    0xd3049e04: ('low_pass', _decode_low_pass),
}
