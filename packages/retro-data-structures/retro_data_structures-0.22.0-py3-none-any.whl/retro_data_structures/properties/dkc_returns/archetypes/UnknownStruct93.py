# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct93(BaseProperty):
    auto_loop_effect: bool = dataclasses.field(default=False)
    auto_start_effect: bool = dataclasses.field(default=False)
    effect_weight: Spline = dataclasses.field(default_factory=Spline)
    screen_warp_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_0xb883ac66: float = dataclasses.field(default=0.0)
    offset_v: float = dataclasses.field(default=0.0)
    unknown_0xa02bb525: float = dataclasses.field(default=0.0)
    unknown_0x26bfc78b: float = dataclasses.field(default=0.0)
    unknown_0x83f8f585: float = dataclasses.field(default=30.0)
    scale_factor: int = dataclasses.field(default=0)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xc8\xfcI\xd0')  # 0xc8fc49d0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_loop_effect))

        data.write(b'eG\x0f[')  # 0x65470f5b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start_effect))

        data.write(b'`W\x93\x8a')  # 0x6057938a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.effect_weight.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\x96\x98\x9a')  # 0x5e96989a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.screen_warp_texture))

        data.write(b'\xb8\x83\xacf')  # 0xb883ac66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb883ac66))

        data.write(b'>\x17\xde\xc8')  # 0x3e17dec8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.offset_v))

        data.write(b'\xa0+\xb5%')  # 0xa02bb525
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa02bb525))

        data.write(b'&\xbf\xc7\x8b')  # 0x26bfc78b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x26bfc78b))

        data.write(b'\x83\xf8\xf5\x85')  # 0x83f8f585
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x83f8f585))

        data.write(b'\xb2\x80}m')  # 0xb2807d6d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.scale_factor))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            auto_loop_effect=data['auto_loop_effect'],
            auto_start_effect=data['auto_start_effect'],
            effect_weight=Spline.from_json(data['effect_weight']),
            screen_warp_texture=data['screen_warp_texture'],
            unknown_0xb883ac66=data['unknown_0xb883ac66'],
            offset_v=data['offset_v'],
            unknown_0xa02bb525=data['unknown_0xa02bb525'],
            unknown_0x26bfc78b=data['unknown_0x26bfc78b'],
            unknown_0x83f8f585=data['unknown_0x83f8f585'],
            scale_factor=data['scale_factor'],
        )

    def to_json(self) -> dict:
        return {
            'auto_loop_effect': self.auto_loop_effect,
            'auto_start_effect': self.auto_start_effect,
            'effect_weight': self.effect_weight.to_json(),
            'screen_warp_texture': self.screen_warp_texture,
            'unknown_0xb883ac66': self.unknown_0xb883ac66,
            'offset_v': self.offset_v,
            'unknown_0xa02bb525': self.unknown_0xa02bb525,
            'unknown_0x26bfc78b': self.unknown_0x26bfc78b,
            'unknown_0x83f8f585': self.unknown_0x83f8f585,
            'scale_factor': self.scale_factor,
        }


def _decode_auto_loop_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_effect_weight(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_screen_warp_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xb883ac66(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_offset_v(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa02bb525(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x26bfc78b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x83f8f585(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scale_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc8fc49d0: ('auto_loop_effect', _decode_auto_loop_effect),
    0x65470f5b: ('auto_start_effect', _decode_auto_start_effect),
    0x6057938a: ('effect_weight', _decode_effect_weight),
    0x5e96989a: ('screen_warp_texture', _decode_screen_warp_texture),
    0xb883ac66: ('unknown_0xb883ac66', _decode_unknown_0xb883ac66),
    0x3e17dec8: ('offset_v', _decode_offset_v),
    0xa02bb525: ('unknown_0xa02bb525', _decode_unknown_0xa02bb525),
    0x26bfc78b: ('unknown_0x26bfc78b', _decode_unknown_0x26bfc78b),
    0x83f8f585: ('unknown_0x83f8f585', _decode_unknown_0x83f8f585),
    0xb2807d6d: ('scale_factor', _decode_scale_factor),
}
