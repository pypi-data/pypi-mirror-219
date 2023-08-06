# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct147(BaseProperty):
    hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    board_transition_time: float = dataclasses.field(default=0.25)
    board_rotation: Spline = dataclasses.field(default_factory=Spline)
    visible_time: float = dataclasses.field(default=1.0)
    unknown_0x5aedf7c9: float = dataclasses.field(default=0.05000000074505806)
    transition_out_time: float = dataclasses.field(default=0.5)
    fade_alpha: float = dataclasses.field(default=0.30000001192092896)
    banana_increment_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    banana_reset_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    increment_delay: float = dataclasses.field(default=0.0625)
    strg_0x569bd8a7: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x7affc159: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_0xf7d838f6: float = dataclasses.field(default=0.30000001192092896)
    strg_0x09f666e5: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    text_gradient_start_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    text_gradient_end_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    unknown_0xa5f210ba: bool = dataclasses.field(default=True)
    unknown_0x4038140e: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\x17*\xdd\xb3')  # 0x172addb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.board_transition_time))

        data.write(b'i\xdc\n\x16')  # 0x69dc0a16
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.board_rotation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'W\x04\x89|')  # 0x5704897c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_time))

        data.write(b'Z\xed\xf7\xc9')  # 0x5aedf7c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5aedf7c9))

        data.write(b'^J\x10v')  # 0x5e4a1076
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.transition_out_time))

        data.write(b']\x84\xac\xe2')  # 0x5d84ace2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_alpha))

        data.write(b'[\x92\x8a]')  # 0x5b928a5d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.banana_increment_sound))

        data.write(b'\xd8@Y\x8d')  # 0xd840598d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.banana_reset_sound))

        data.write(b'\xee\xb3\x90i')  # 0xeeb39069
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.increment_delay))

        data.write(b'V\x9b\xd8\xa7')  # 0x569bd8a7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x569bd8a7))

        data.write(b'z\xff\xc1Y')  # 0x7affc159
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x7affc159))

        data.write(b'\xf7\xd88\xf6')  # 0xf7d838f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf7d838f6))

        data.write(b'\t\xf6f\xe5')  # 0x9f666e5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x09f666e5))

        data.write(b'\xf9\xe0\xd0\xfb')  # 0xf9e0d0fb
        data.write(b'\x00\x10')  # size
        self.text_gradient_start_color.to_stream(data)

        data.write(b'\xe0A~\x89')  # 0xe0417e89
        data.write(b'\x00\x10')  # size
        self.text_gradient_end_color.to_stream(data)

        data.write(b'\xf2\xe15\x06')  # 0xf2e13506
        data.write(b'\x00\x10')  # size
        self.text_outline_color.to_stream(data)

        data.write(b'\xa5\xf2\x10\xba')  # 0xa5f210ba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa5f210ba))

        data.write(b'@8\x14\x0e')  # 0x4038140e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4038140e))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hud_frame=data['hud_frame'],
            board_transition_time=data['board_transition_time'],
            board_rotation=Spline.from_json(data['board_rotation']),
            visible_time=data['visible_time'],
            unknown_0x5aedf7c9=data['unknown_0x5aedf7c9'],
            transition_out_time=data['transition_out_time'],
            fade_alpha=data['fade_alpha'],
            banana_increment_sound=data['banana_increment_sound'],
            banana_reset_sound=data['banana_reset_sound'],
            increment_delay=data['increment_delay'],
            strg_0x569bd8a7=data['strg_0x569bd8a7'],
            strg_0x7affc159=data['strg_0x7affc159'],
            unknown_0xf7d838f6=data['unknown_0xf7d838f6'],
            strg_0x09f666e5=data['strg_0x09f666e5'],
            text_gradient_start_color=Color.from_json(data['text_gradient_start_color']),
            text_gradient_end_color=Color.from_json(data['text_gradient_end_color']),
            text_outline_color=Color.from_json(data['text_outline_color']),
            unknown_0xa5f210ba=data['unknown_0xa5f210ba'],
            unknown_0x4038140e=data['unknown_0x4038140e'],
        )

    def to_json(self) -> dict:
        return {
            'hud_frame': self.hud_frame,
            'board_transition_time': self.board_transition_time,
            'board_rotation': self.board_rotation.to_json(),
            'visible_time': self.visible_time,
            'unknown_0x5aedf7c9': self.unknown_0x5aedf7c9,
            'transition_out_time': self.transition_out_time,
            'fade_alpha': self.fade_alpha,
            'banana_increment_sound': self.banana_increment_sound,
            'banana_reset_sound': self.banana_reset_sound,
            'increment_delay': self.increment_delay,
            'strg_0x569bd8a7': self.strg_0x569bd8a7,
            'strg_0x7affc159': self.strg_0x7affc159,
            'unknown_0xf7d838f6': self.unknown_0xf7d838f6,
            'strg_0x09f666e5': self.strg_0x09f666e5,
            'text_gradient_start_color': self.text_gradient_start_color.to_json(),
            'text_gradient_end_color': self.text_gradient_end_color.to_json(),
            'text_outline_color': self.text_outline_color.to_json(),
            'unknown_0xa5f210ba': self.unknown_0xa5f210ba,
            'unknown_0x4038140e': self.unknown_0x4038140e,
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_board_transition_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_board_rotation(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_visible_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5aedf7c9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_transition_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_banana_increment_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_banana_reset_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_increment_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_strg_0x569bd8a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x7affc159(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf7d838f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_strg_0x09f666e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_gradient_start_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_gradient_end_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa5f210ba(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4038140e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0x172addb3: ('board_transition_time', _decode_board_transition_time),
    0x69dc0a16: ('board_rotation', _decode_board_rotation),
    0x5704897c: ('visible_time', _decode_visible_time),
    0x5aedf7c9: ('unknown_0x5aedf7c9', _decode_unknown_0x5aedf7c9),
    0x5e4a1076: ('transition_out_time', _decode_transition_out_time),
    0x5d84ace2: ('fade_alpha', _decode_fade_alpha),
    0x5b928a5d: ('banana_increment_sound', _decode_banana_increment_sound),
    0xd840598d: ('banana_reset_sound', _decode_banana_reset_sound),
    0xeeb39069: ('increment_delay', _decode_increment_delay),
    0x569bd8a7: ('strg_0x569bd8a7', _decode_strg_0x569bd8a7),
    0x7affc159: ('strg_0x7affc159', _decode_strg_0x7affc159),
    0xf7d838f6: ('unknown_0xf7d838f6', _decode_unknown_0xf7d838f6),
    0x9f666e5: ('strg_0x09f666e5', _decode_strg_0x09f666e5),
    0xf9e0d0fb: ('text_gradient_start_color', _decode_text_gradient_start_color),
    0xe0417e89: ('text_gradient_end_color', _decode_text_gradient_end_color),
    0xf2e13506: ('text_outline_color', _decode_text_outline_color),
    0xa5f210ba: ('unknown_0xa5f210ba', _decode_unknown_0xa5f210ba),
    0x4038140e: ('unknown_0x4038140e', _decode_unknown_0x4038140e),
}
