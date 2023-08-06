# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class DKBarrelGlueData(BaseProperty):
    dk_inside_animation: int = dataclasses.field(default=0)
    diddy_inside_animation: int = dataclasses.field(default=0)
    dk_held_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    diddy_held_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    held_sound_initial_delay: float = dataclasses.field(default=0.0)
    held_sound_random_delay_min: float = dataclasses.field(default=0.0)
    held_sound_random_delay_max: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x1cu\xf2M')  # 0x1c75f24d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dk_inside_animation))

        data.write(b'\x0c\\l\xd8')  # 0xc5c6cd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.diddy_inside_animation))

        data.write(b'\xe8E\xac\x92')  # 0xe845ac92
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dk_held_sound))

        data.write(b'\x16\xad\x04#')  # 0x16ad0423
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.diddy_held_sound))

        data.write(b'\xf8\xe9Ia')  # 0xf8e94961
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.held_sound_initial_delay))

        data.write(b'\x7fT\x97\xb7')  # 0x7f5497b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.held_sound_random_delay_min))

        data.write(b'\x9948V')  # 0x99343856
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.held_sound_random_delay_max))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            dk_inside_animation=data['dk_inside_animation'],
            diddy_inside_animation=data['diddy_inside_animation'],
            dk_held_sound=data['dk_held_sound'],
            diddy_held_sound=data['diddy_held_sound'],
            held_sound_initial_delay=data['held_sound_initial_delay'],
            held_sound_random_delay_min=data['held_sound_random_delay_min'],
            held_sound_random_delay_max=data['held_sound_random_delay_max'],
        )

    def to_json(self) -> dict:
        return {
            'dk_inside_animation': self.dk_inside_animation,
            'diddy_inside_animation': self.diddy_inside_animation,
            'dk_held_sound': self.dk_held_sound,
            'diddy_held_sound': self.diddy_held_sound,
            'held_sound_initial_delay': self.held_sound_initial_delay,
            'held_sound_random_delay_min': self.held_sound_random_delay_min,
            'held_sound_random_delay_max': self.held_sound_random_delay_max,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x1c75f24d, 0xc5c6cd8, 0xe845ac92, 0x16ad0423, 0xf8e94961, 0x7f5497b7, 0x99343856)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DKBarrelGlueData]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHQLHQLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(78))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return DKBarrelGlueData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_dk_inside_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_diddy_inside_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dk_held_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_diddy_held_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_held_sound_initial_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_held_sound_random_delay_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_held_sound_random_delay_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1c75f24d: ('dk_inside_animation', _decode_dk_inside_animation),
    0xc5c6cd8: ('diddy_inside_animation', _decode_diddy_inside_animation),
    0xe845ac92: ('dk_held_sound', _decode_dk_held_sound),
    0x16ad0423: ('diddy_held_sound', _decode_diddy_held_sound),
    0xf8e94961: ('held_sound_initial_delay', _decode_held_sound_initial_delay),
    0x7f5497b7: ('held_sound_random_delay_min', _decode_held_sound_random_delay_min),
    0x99343856: ('held_sound_random_delay_max', _decode_held_sound_random_delay_max),
}
