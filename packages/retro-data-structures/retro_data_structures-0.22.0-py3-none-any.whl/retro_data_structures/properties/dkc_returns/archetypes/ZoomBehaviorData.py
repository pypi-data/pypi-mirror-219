# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class ZoomBehaviorData(BaseProperty):
    pullback_spline: Spline = dataclasses.field(default_factory=Spline)
    zoom_by_horizontal_distance: bool = dataclasses.field(default=True)
    zoom_by_vertical_distance: bool = dataclasses.field(default=False)
    vertical_distance_ratio: float = dataclasses.field(default=1.7769999504089355)
    zoom_by_distance_from_ground: bool = dataclasses.field(default=False)
    pullback_spline_from_ground: Spline = dataclasses.field(default_factory=Spline)
    adjust_horizontally: bool = dataclasses.field(default=True)
    adjust_vertically: bool = dataclasses.field(default=True)
    zoom_in_delay: float = dataclasses.field(default=1.5)
    zoom_motion: Convergence = dataclasses.field(default_factory=Convergence)
    horizontal_adjust_motion: Convergence = dataclasses.field(default_factory=Convergence)
    get_max_zoom_from_zoom_spline: bool = dataclasses.field(default=False)
    max_distance_from_target: float = dataclasses.field(default=30.5)

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

        data.write(b'4:\x18\xa7')  # 0x343a18a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pullback_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x82\xaf7\x1e')  # 0x82af371e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.zoom_by_horizontal_distance))

        data.write(b'ov\xec^')  # 0x6f76ec5e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.zoom_by_vertical_distance))

        data.write(b'm\x18\xc3\x18')  # 0x6d18c318
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_distance_ratio))

        data.write(b'\xac\xe2:\xc6')  # 0xace23ac6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.zoom_by_distance_from_ground))

        data.write(b'-\x83\x9eo')  # 0x2d839e6f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pullback_spline_from_ground.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\x8d~\xf2')  # 0xf88d7ef2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_horizontally))

        data.write(b'\x90n\x98\xfa')  # 0x906e98fa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_vertically))

        data.write(b'\rl\x95)')  # 0xd6c9529
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.zoom_in_delay))

        data.write(b'\t/\x7f\xd8')  # 0x92f7fd8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.zoom_motion.to_stream(data, default_override={'convergence_type': enums.ConvergenceType.Unknown1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')\xe0b\x13')  # 0x29e06213
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.horizontal_adjust_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\x1eg\xc8')  # 0xb21e67c8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.get_max_zoom_from_zoom_spline))

        data.write(b'\x05O\x1a\x14')  # 0x54f1a14
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_distance_from_target))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            pullback_spline=Spline.from_json(data['pullback_spline']),
            zoom_by_horizontal_distance=data['zoom_by_horizontal_distance'],
            zoom_by_vertical_distance=data['zoom_by_vertical_distance'],
            vertical_distance_ratio=data['vertical_distance_ratio'],
            zoom_by_distance_from_ground=data['zoom_by_distance_from_ground'],
            pullback_spline_from_ground=Spline.from_json(data['pullback_spline_from_ground']),
            adjust_horizontally=data['adjust_horizontally'],
            adjust_vertically=data['adjust_vertically'],
            zoom_in_delay=data['zoom_in_delay'],
            zoom_motion=Convergence.from_json(data['zoom_motion']),
            horizontal_adjust_motion=Convergence.from_json(data['horizontal_adjust_motion']),
            get_max_zoom_from_zoom_spline=data['get_max_zoom_from_zoom_spline'],
            max_distance_from_target=data['max_distance_from_target'],
        )

    def to_json(self) -> dict:
        return {
            'pullback_spline': self.pullback_spline.to_json(),
            'zoom_by_horizontal_distance': self.zoom_by_horizontal_distance,
            'zoom_by_vertical_distance': self.zoom_by_vertical_distance,
            'vertical_distance_ratio': self.vertical_distance_ratio,
            'zoom_by_distance_from_ground': self.zoom_by_distance_from_ground,
            'pullback_spline_from_ground': self.pullback_spline_from_ground.to_json(),
            'adjust_horizontally': self.adjust_horizontally,
            'adjust_vertically': self.adjust_vertically,
            'zoom_in_delay': self.zoom_in_delay,
            'zoom_motion': self.zoom_motion.to_json(),
            'horizontal_adjust_motion': self.horizontal_adjust_motion.to_json(),
            'get_max_zoom_from_zoom_spline': self.get_max_zoom_from_zoom_spline,
            'max_distance_from_target': self.max_distance_from_target,
        }


def _decode_pullback_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_zoom_by_horizontal_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_zoom_by_vertical_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_vertical_distance_ratio(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_zoom_by_distance_from_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pullback_spline_from_ground(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_adjust_horizontally(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_adjust_vertically(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_zoom_in_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_zoom_motion(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size, default_override={'convergence_type': enums.ConvergenceType.Unknown1})


def _decode_horizontal_adjust_motion(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_get_max_zoom_from_zoom_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_distance_from_target(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x343a18a7: ('pullback_spline', _decode_pullback_spline),
    0x82af371e: ('zoom_by_horizontal_distance', _decode_zoom_by_horizontal_distance),
    0x6f76ec5e: ('zoom_by_vertical_distance', _decode_zoom_by_vertical_distance),
    0x6d18c318: ('vertical_distance_ratio', _decode_vertical_distance_ratio),
    0xace23ac6: ('zoom_by_distance_from_ground', _decode_zoom_by_distance_from_ground),
    0x2d839e6f: ('pullback_spline_from_ground', _decode_pullback_spline_from_ground),
    0xf88d7ef2: ('adjust_horizontally', _decode_adjust_horizontally),
    0x906e98fa: ('adjust_vertically', _decode_adjust_vertically),
    0xd6c9529: ('zoom_in_delay', _decode_zoom_in_delay),
    0x92f7fd8: ('zoom_motion', _decode_zoom_motion),
    0x29e06213: ('horizontal_adjust_motion', _decode_horizontal_adjust_motion),
    0xb21e67c8: ('get_max_zoom_from_zoom_spline', _decode_get_max_zoom_from_zoom_spline),
    0x54f1a14: ('max_distance_from_target', _decode_max_distance_from_target),
}
