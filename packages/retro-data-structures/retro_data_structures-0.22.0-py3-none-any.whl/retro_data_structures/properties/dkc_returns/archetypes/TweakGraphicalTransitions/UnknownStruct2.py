# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    resource_name: str = dataclasses.field(default='')
    alpha_mask_name: str = dataclasses.field(default='')
    draw_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    rendering_type: enums.TweakGraphicalTransitions_UnknownEnum1 = dataclasses.field(default=enums.TweakGraphicalTransitions_UnknownEnum1.Unknown1)
    rotations_per_second: float = dataclasses.field(default=0.0)
    delay_time: float = dataclasses.field(default=0.0)
    display_time: float = dataclasses.field(default=2.0)
    texture_alpha: Spline = dataclasses.field(default_factory=Spline)
    texture_scale: Spline = dataclasses.field(default_factory=Spline)
    separate_alpha_texture_scale: bool = dataclasses.field(default=False)
    alpha_rotations_per_second: float = dataclasses.field(default=0.0)
    alpha_texture_scale: Spline = dataclasses.field(default_factory=Spline)
    vertical_from_center: Spline = dataclasses.field(default_factory=Spline)
    draw_before_models: bool = dataclasses.field(default=True)
    stretch_across_screen: bool = dataclasses.field(default=False)
    pause_timing_for_code: bool = dataclasses.field(default=False)
    pause_time: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'\xd2\x11\xba\xed')  # 0xd211baed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.resource_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2|\x08\xd5')  # 0xe27c08d5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.alpha_mask_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\xa5\x17\x1e')  # 0xe3a5171e
        data.write(b'\x00\x10')  # size
        self.draw_color.to_stream(data)

        data.write(b'\x0b\x91\x85y')  # 0xb918579
        data.write(b'\x00\x04')  # size
        self.rendering_type.to_stream(data)

        data.write(b'\xbe\xfcM\xa4')  # 0xbefc4da4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotations_per_second))

        data.write(b'\x8e\x16\xe0\x12')  # 0x8e16e012
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_time))

        data.write(b'\x1a&\xc1\xcc')  # 0x1a26c1cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.display_time))

        data.write(b'"\xac\x059')  # 0x22ac0539
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.texture_alpha.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\x83_e')  # 0xee835f65
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.texture_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\xd6\xe4\xd2')  # 0xeed6e4d2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.separate_alpha_texture_scale))

        data.write(b'\x02\x15O\xb4')  # 0x2154fb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alpha_rotations_per_second))

        data.write(b'\xe4\xce\x05\x82')  # 0xe4ce0582
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.alpha_texture_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x04\x84\xa7\xea')  # 0x484a7ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vertical_from_center.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\xc31\xb1')  # 0x77c331b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.draw_before_models))

        data.write(b'F\x17s9')  # 0x46177339
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stretch_across_screen))

        data.write(b'\xb1\xe6G.')  # 0xb1e6472e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.pause_timing_for_code))

        data.write(b'k\x08\xf2\xf2')  # 0x6b08f2f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            resource_name=data['resource_name'],
            alpha_mask_name=data['alpha_mask_name'],
            draw_color=Color.from_json(data['draw_color']),
            rendering_type=enums.TweakGraphicalTransitions_UnknownEnum1.from_json(data['rendering_type']),
            rotations_per_second=data['rotations_per_second'],
            delay_time=data['delay_time'],
            display_time=data['display_time'],
            texture_alpha=Spline.from_json(data['texture_alpha']),
            texture_scale=Spline.from_json(data['texture_scale']),
            separate_alpha_texture_scale=data['separate_alpha_texture_scale'],
            alpha_rotations_per_second=data['alpha_rotations_per_second'],
            alpha_texture_scale=Spline.from_json(data['alpha_texture_scale']),
            vertical_from_center=Spline.from_json(data['vertical_from_center']),
            draw_before_models=data['draw_before_models'],
            stretch_across_screen=data['stretch_across_screen'],
            pause_timing_for_code=data['pause_timing_for_code'],
            pause_time=data['pause_time'],
        )

    def to_json(self) -> dict:
        return {
            'resource_name': self.resource_name,
            'alpha_mask_name': self.alpha_mask_name,
            'draw_color': self.draw_color.to_json(),
            'rendering_type': self.rendering_type.to_json(),
            'rotations_per_second': self.rotations_per_second,
            'delay_time': self.delay_time,
            'display_time': self.display_time,
            'texture_alpha': self.texture_alpha.to_json(),
            'texture_scale': self.texture_scale.to_json(),
            'separate_alpha_texture_scale': self.separate_alpha_texture_scale,
            'alpha_rotations_per_second': self.alpha_rotations_per_second,
            'alpha_texture_scale': self.alpha_texture_scale.to_json(),
            'vertical_from_center': self.vertical_from_center.to_json(),
            'draw_before_models': self.draw_before_models,
            'stretch_across_screen': self.stretch_across_screen,
            'pause_timing_for_code': self.pause_timing_for_code,
            'pause_time': self.pause_time,
        }


def _decode_resource_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_alpha_mask_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_draw_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_rendering_type(data: typing.BinaryIO, property_size: int):
    return enums.TweakGraphicalTransitions_UnknownEnum1.from_stream(data)


def _decode_rotations_per_second(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_display_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_texture_alpha(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_texture_scale(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_separate_alpha_texture_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_alpha_rotations_per_second(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alpha_texture_scale(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_vertical_from_center(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_draw_before_models(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stretch_across_screen(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pause_timing_for_code(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pause_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd211baed: ('resource_name', _decode_resource_name),
    0xe27c08d5: ('alpha_mask_name', _decode_alpha_mask_name),
    0xe3a5171e: ('draw_color', _decode_draw_color),
    0xb918579: ('rendering_type', _decode_rendering_type),
    0xbefc4da4: ('rotations_per_second', _decode_rotations_per_second),
    0x8e16e012: ('delay_time', _decode_delay_time),
    0x1a26c1cc: ('display_time', _decode_display_time),
    0x22ac0539: ('texture_alpha', _decode_texture_alpha),
    0xee835f65: ('texture_scale', _decode_texture_scale),
    0xeed6e4d2: ('separate_alpha_texture_scale', _decode_separate_alpha_texture_scale),
    0x2154fb4: ('alpha_rotations_per_second', _decode_alpha_rotations_per_second),
    0xe4ce0582: ('alpha_texture_scale', _decode_alpha_texture_scale),
    0x484a7ea: ('vertical_from_center', _decode_vertical_from_center),
    0x77c331b1: ('draw_before_models', _decode_draw_before_models),
    0x46177339: ('stretch_across_screen', _decode_stretch_across_screen),
    0xb1e6472e: ('pause_timing_for_code', _decode_pause_timing_for_code),
    0x6b08f2f2: ('pause_time', _decode_pause_time),
}
