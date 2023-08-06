# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class EchoParameters(BaseProperty):
    is_echo_emitter: bool = dataclasses.field(default=False)
    only_emit_damage: bool = dataclasses.field(default=False)
    num_sound_waves: int = dataclasses.field(default=3)
    space_between_waves: float = dataclasses.field(default=0.20000000298023224)
    wave_line_size: float = dataclasses.field(default=4.0)
    forced_minimum_vis: float = dataclasses.field(default=0.5)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x17\xad\xdf\xc6')  # 0x17addfc6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_echo_emitter))

        data.write(b'\xf5\xdfb\xad')  # 0xf5df62ad
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.only_emit_damage))

        data.write(b'\xd0\x07:\x0c')  # 0xd0073a0c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_sound_waves))

        data.write(b'\xedmg\x82')  # 0xed6d6782
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.space_between_waves))

        data.write(b'\xdb\x19\x0fh')  # 0xdb190f68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wave_line_size))

        data.write(b'\xf8z\x15\xe7')  # 0xf87a15e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forced_minimum_vis))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_echo_emitter=data['is_echo_emitter'],
            only_emit_damage=data['only_emit_damage'],
            num_sound_waves=data['num_sound_waves'],
            space_between_waves=data['space_between_waves'],
            wave_line_size=data['wave_line_size'],
            forced_minimum_vis=data['forced_minimum_vis'],
        )

    def to_json(self) -> dict:
        return {
            'is_echo_emitter': self.is_echo_emitter,
            'only_emit_damage': self.only_emit_damage,
            'num_sound_waves': self.num_sound_waves,
            'space_between_waves': self.space_between_waves,
            'wave_line_size': self.wave_line_size,
            'forced_minimum_vis': self.forced_minimum_vis,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x17addfc6, 0xf5df62ad, 0xd0073a0c, 0xed6d6782, 0xdb190f68, 0xf87a15e7)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[EchoParameters]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LHlLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(54))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return EchoParameters(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_is_echo_emitter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_only_emit_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_num_sound_waves(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_space_between_waves(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wave_line_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forced_minimum_vis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x17addfc6: ('is_echo_emitter', _decode_is_echo_emitter),
    0xf5df62ad: ('only_emit_damage', _decode_only_emit_damage),
    0xd0073a0c: ('num_sound_waves', _decode_num_sound_waves),
    0xed6d6782: ('space_between_waves', _decode_space_between_waves),
    0xdb190f68: ('wave_line_size', _decode_wave_line_size),
    0xf87a15e7: ('forced_minimum_vis', _decode_forced_minimum_vis),
}
