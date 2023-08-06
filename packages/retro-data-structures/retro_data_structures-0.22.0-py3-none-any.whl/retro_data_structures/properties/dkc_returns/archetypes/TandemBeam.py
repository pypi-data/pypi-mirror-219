# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class TandemBeam(BaseProperty):
    tandem_beam_type: enums.TandemBeamType = dataclasses.field(default=enums.TandemBeamType.Unknown1)
    maximum_beam_time: float = dataclasses.field(default=10.0)
    activation_spline: Spline = dataclasses.field(default_factory=Spline)
    beam_width: float = dataclasses.field(default=0.25)
    beam_default_length: float = dataclasses.field(default=5.0)
    beam_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    beam_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    beam_telegraph_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    beam_telegraph_length: float = dataclasses.field(default=1.0)
    beam_scroll_direction: enums.BeamScrollDirection = dataclasses.field(default=enums.BeamScrollDirection.Unknown1)
    beam_scroll_speed: float = dataclasses.field(default=0.0)
    beam_texture_uv_flip_speed: float = dataclasses.field(default=0.0625)
    alternate_beam_texture_v_coordinate: bool = dataclasses.field(default=True)
    number_of_beam_texture_u_slots: int = dataclasses.field(default=4)
    beam_texture_u0: float = dataclasses.field(default=0.0)
    beam_texture_u1: float = dataclasses.field(default=0.5)
    beam_texture_u2: float = dataclasses.field(default=0.25)
    beam_texture_u3: float = dataclasses.field(default=0.75)

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

        data.write(b'\xd0E\xa1\x94')  # 0xd045a194
        data.write(b'\x00\x04')  # size
        self.tandem_beam_type.to_stream(data)

        data.write(b'\xb8\xd6-\xdf')  # 0xb8d62ddf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_beam_time))

        data.write(b'\x92p\x8c~')  # 0x92708c7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.activation_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9V\xf3y')  # 0xb956f379
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_width))

        data.write(b'g\xa0\x8f\x89')  # 0x67a08f89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_default_length))

        data.write(b'\x0c\xd0\x1c\x0e')  # 0xcd01c0e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_sound))

        data.write(b'\xc6\xf2)\xc6')  # 0xc6f229c6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_texture))

        data.write(b'\x1b$\x8c3')  # 0x1b248c33
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_telegraph_texture))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaaz\xe2\xed')  # 0xaa7ae2ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_telegraph_length))

        data.write(b'\xa5\xa3\xefc')  # 0xa5a3ef63
        data.write(b'\x00\x04')  # size
        self.beam_scroll_direction.to_stream(data)

        data.write(b'\xab\xf9\xf6\xfd')  # 0xabf9f6fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_scroll_speed))

        data.write(b'\xdbd\xab\xe3')  # 0xdb64abe3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_uv_flip_speed))

        data.write(b'\x82\x05D#')  # 0x82054423
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.alternate_beam_texture_v_coordinate))

        data.write(b'\xad\xd9\xa3\xb6')  # 0xadd9a3b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_beam_texture_u_slots))

        data.write(b'\xe4\x07#\xff')  # 0xe40723ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u0))

        data.write(b'/[\xf0Z')  # 0x2f5bf05a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u1))

        data.write(b'\xa9\xcf\x82\xf4')  # 0xa9cf82f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u2))

        data.write(b'b\x93QQ')  # 0x62935151
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            tandem_beam_type=enums.TandemBeamType.from_json(data['tandem_beam_type']),
            maximum_beam_time=data['maximum_beam_time'],
            activation_spline=Spline.from_json(data['activation_spline']),
            beam_width=data['beam_width'],
            beam_default_length=data['beam_default_length'],
            beam_sound=data['beam_sound'],
            beam_texture=data['beam_texture'],
            beam_telegraph_texture=data['beam_telegraph_texture'],
            damage=DamageInfo.from_json(data['damage']),
            beam_telegraph_length=data['beam_telegraph_length'],
            beam_scroll_direction=enums.BeamScrollDirection.from_json(data['beam_scroll_direction']),
            beam_scroll_speed=data['beam_scroll_speed'],
            beam_texture_uv_flip_speed=data['beam_texture_uv_flip_speed'],
            alternate_beam_texture_v_coordinate=data['alternate_beam_texture_v_coordinate'],
            number_of_beam_texture_u_slots=data['number_of_beam_texture_u_slots'],
            beam_texture_u0=data['beam_texture_u0'],
            beam_texture_u1=data['beam_texture_u1'],
            beam_texture_u2=data['beam_texture_u2'],
            beam_texture_u3=data['beam_texture_u3'],
        )

    def to_json(self) -> dict:
        return {
            'tandem_beam_type': self.tandem_beam_type.to_json(),
            'maximum_beam_time': self.maximum_beam_time,
            'activation_spline': self.activation_spline.to_json(),
            'beam_width': self.beam_width,
            'beam_default_length': self.beam_default_length,
            'beam_sound': self.beam_sound,
            'beam_texture': self.beam_texture,
            'beam_telegraph_texture': self.beam_telegraph_texture,
            'damage': self.damage.to_json(),
            'beam_telegraph_length': self.beam_telegraph_length,
            'beam_scroll_direction': self.beam_scroll_direction.to_json(),
            'beam_scroll_speed': self.beam_scroll_speed,
            'beam_texture_uv_flip_speed': self.beam_texture_uv_flip_speed,
            'alternate_beam_texture_v_coordinate': self.alternate_beam_texture_v_coordinate,
            'number_of_beam_texture_u_slots': self.number_of_beam_texture_u_slots,
            'beam_texture_u0': self.beam_texture_u0,
            'beam_texture_u1': self.beam_texture_u1,
            'beam_texture_u2': self.beam_texture_u2,
            'beam_texture_u3': self.beam_texture_u3,
        }


def _decode_tandem_beam_type(data: typing.BinaryIO, property_size: int):
    return enums.TandemBeamType.from_stream(data)


def _decode_maximum_beam_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activation_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_beam_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_default_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_telegraph_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_beam_telegraph_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_scroll_direction(data: typing.BinaryIO, property_size: int):
    return enums.BeamScrollDirection.from_stream(data)


def _decode_beam_scroll_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_uv_flip_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alternate_beam_texture_v_coordinate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_number_of_beam_texture_u_slots(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_beam_texture_u0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_u1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_u2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_u3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd045a194: ('tandem_beam_type', _decode_tandem_beam_type),
    0xb8d62ddf: ('maximum_beam_time', _decode_maximum_beam_time),
    0x92708c7e: ('activation_spline', _decode_activation_spline),
    0xb956f379: ('beam_width', _decode_beam_width),
    0x67a08f89: ('beam_default_length', _decode_beam_default_length),
    0xcd01c0e: ('beam_sound', _decode_beam_sound),
    0xc6f229c6: ('beam_texture', _decode_beam_texture),
    0x1b248c33: ('beam_telegraph_texture', _decode_beam_telegraph_texture),
    0x337f9524: ('damage', _decode_damage),
    0xaa7ae2ed: ('beam_telegraph_length', _decode_beam_telegraph_length),
    0xa5a3ef63: ('beam_scroll_direction', _decode_beam_scroll_direction),
    0xabf9f6fd: ('beam_scroll_speed', _decode_beam_scroll_speed),
    0xdb64abe3: ('beam_texture_uv_flip_speed', _decode_beam_texture_uv_flip_speed),
    0x82054423: ('alternate_beam_texture_v_coordinate', _decode_alternate_beam_texture_v_coordinate),
    0xadd9a3b6: ('number_of_beam_texture_u_slots', _decode_number_of_beam_texture_u_slots),
    0xe40723ff: ('beam_texture_u0', _decode_beam_texture_u0),
    0x2f5bf05a: ('beam_texture_u1', _decode_beam_texture_u1),
    0xa9cf82f4: ('beam_texture_u2', _decode_beam_texture_u2),
    0x62935151: ('beam_texture_u3', _decode_beam_texture_u3),
}
