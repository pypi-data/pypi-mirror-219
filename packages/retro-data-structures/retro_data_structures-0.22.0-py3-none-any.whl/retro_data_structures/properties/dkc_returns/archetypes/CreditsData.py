# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class CreditsData(BaseProperty):
    credits_time: float = dataclasses.field(default=180.0)
    normal_share_lines: int = dataclasses.field(default=4)
    extra_share_per_line: float = dataclasses.field(default=0.25)
    penultimate_share_bonus: float = dataclasses.field(default=0.25)
    pre_penultimate_delay: float = dataclasses.field(default=1.0)
    post_penultimate_delay: float = dataclasses.field(default=2.0)
    final_share_bonus: float = dataclasses.field(default=1.0)
    text_fade_in_time: float = dataclasses.field(default=0.25)
    text_fade_out_time: float = dataclasses.field(default=0.25)
    image_fade_in_time: float = dataclasses.field(default=0.25)
    image_fade_out_time: float = dataclasses.field(default=0.25)
    unknown_struct26_0xba717f32: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0xc344a09a: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0xd834e949: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x917857a0: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x7dfaff15: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0xe60799c8: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x45511f61: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x92b39f39: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unlock_message_total_time: float = dataclasses.field(default=4.0)
    unlock_message_fade_in_time: float = dataclasses.field(default=0.25)
    unlock_message_fade_out_time: float = dataclasses.field(default=0.25)
    unknown_struct26_0xa45e5b13: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unlock_concept_art: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unlock_music: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unlock_diorama: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unlock_message_post_delay: float = dataclasses.field(default=0.25)

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
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'\xc7\xa74\xce')  # 0xc7a734ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.credits_time))

        data.write(b'N\xfel\xde')  # 0x4efe6cde
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.normal_share_lines))

        data.write(b'zT\xcb^')  # 0x7a54cb5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.extra_share_per_line))

        data.write(b'\xfc\xa1Q\\')  # 0xfca1515c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.penultimate_share_bonus))

        data.write(b'\xb1\x13:\x84')  # 0xb1133a84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_penultimate_delay))

        data.write(b'_#\x0cg')  # 0x5f230c67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.post_penultimate_delay))

        data.write(b'\x9a\x9a}\x1f')  # 0x9a9a7d1f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.final_share_bonus))

        data.write(b'\xa0\x91\xf3\x93')  # 0xa091f393
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_fade_in_time))

        data.write(b'\x98\x18jp')  # 0x98186a70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_fade_out_time))

        data.write(b'\xc1\xb9\xee\xf1')  # 0xc1b9eef1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.image_fade_in_time))

        data.write(b';\xc5B\x19')  # 0x3bc54219
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.image_fade_out_time))

        data.write(b'\xbaq\x7f2')  # 0xba717f32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xba717f32.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3D\xa0\x9a')  # 0xc344a09a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xc344a09a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd84\xe9I')  # 0xd834e949
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xd834e949.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91xW\xa0')  # 0x917857a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x917857a0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\xfa\xff\x15')  # 0x7dfaff15
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x7dfaff15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\x07\x99\xc8')  # 0xe60799c8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xe60799c8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'EQ\x1fa')  # 0x45511f61
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x45511f61.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x92\xb3\x9f9')  # 0x92b39f39
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x92b39f39.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb5K\x9d%')  # 0xb54b9d25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_total_time))

        data.write(b'\x8f\xdc\x94\x87')  # 0x8fdc9487
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_fade_in_time))

        data.write(b'\x82\xed\xf3j')  # 0x82edf36a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_fade_out_time))

        data.write(b'\xa4^[\x13')  # 0xa45e5b13
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xa45e5b13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'yX\x9b\xf4')  # 0x79589bf4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_concept_art))

        data.write(b'\n\xf7\x07\xdf')  # 0xaf707df
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_music))

        data.write(b'\\\xe2\xa9\xa9')  # 0x5ce2a9a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_diorama))

        data.write(b'\x99J\xa2}')  # 0x994aa27d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_post_delay))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            credits_time=data['credits_time'],
            normal_share_lines=data['normal_share_lines'],
            extra_share_per_line=data['extra_share_per_line'],
            penultimate_share_bonus=data['penultimate_share_bonus'],
            pre_penultimate_delay=data['pre_penultimate_delay'],
            post_penultimate_delay=data['post_penultimate_delay'],
            final_share_bonus=data['final_share_bonus'],
            text_fade_in_time=data['text_fade_in_time'],
            text_fade_out_time=data['text_fade_out_time'],
            image_fade_in_time=data['image_fade_in_time'],
            image_fade_out_time=data['image_fade_out_time'],
            unknown_struct26_0xba717f32=UnknownStruct26.from_json(data['unknown_struct26_0xba717f32']),
            unknown_struct26_0xc344a09a=UnknownStruct26.from_json(data['unknown_struct26_0xc344a09a']),
            unknown_struct26_0xd834e949=UnknownStruct26.from_json(data['unknown_struct26_0xd834e949']),
            unknown_struct26_0x917857a0=UnknownStruct26.from_json(data['unknown_struct26_0x917857a0']),
            unknown_struct26_0x7dfaff15=UnknownStruct26.from_json(data['unknown_struct26_0x7dfaff15']),
            unknown_struct26_0xe60799c8=UnknownStruct26.from_json(data['unknown_struct26_0xe60799c8']),
            unknown_struct26_0x45511f61=UnknownStruct26.from_json(data['unknown_struct26_0x45511f61']),
            unknown_struct26_0x92b39f39=UnknownStruct26.from_json(data['unknown_struct26_0x92b39f39']),
            unlock_message_total_time=data['unlock_message_total_time'],
            unlock_message_fade_in_time=data['unlock_message_fade_in_time'],
            unlock_message_fade_out_time=data['unlock_message_fade_out_time'],
            unknown_struct26_0xa45e5b13=UnknownStruct26.from_json(data['unknown_struct26_0xa45e5b13']),
            unlock_concept_art=data['unlock_concept_art'],
            unlock_music=data['unlock_music'],
            unlock_diorama=data['unlock_diorama'],
            unlock_message_post_delay=data['unlock_message_post_delay'],
        )

    def to_json(self) -> dict:
        return {
            'credits_time': self.credits_time,
            'normal_share_lines': self.normal_share_lines,
            'extra_share_per_line': self.extra_share_per_line,
            'penultimate_share_bonus': self.penultimate_share_bonus,
            'pre_penultimate_delay': self.pre_penultimate_delay,
            'post_penultimate_delay': self.post_penultimate_delay,
            'final_share_bonus': self.final_share_bonus,
            'text_fade_in_time': self.text_fade_in_time,
            'text_fade_out_time': self.text_fade_out_time,
            'image_fade_in_time': self.image_fade_in_time,
            'image_fade_out_time': self.image_fade_out_time,
            'unknown_struct26_0xba717f32': self.unknown_struct26_0xba717f32.to_json(),
            'unknown_struct26_0xc344a09a': self.unknown_struct26_0xc344a09a.to_json(),
            'unknown_struct26_0xd834e949': self.unknown_struct26_0xd834e949.to_json(),
            'unknown_struct26_0x917857a0': self.unknown_struct26_0x917857a0.to_json(),
            'unknown_struct26_0x7dfaff15': self.unknown_struct26_0x7dfaff15.to_json(),
            'unknown_struct26_0xe60799c8': self.unknown_struct26_0xe60799c8.to_json(),
            'unknown_struct26_0x45511f61': self.unknown_struct26_0x45511f61.to_json(),
            'unknown_struct26_0x92b39f39': self.unknown_struct26_0x92b39f39.to_json(),
            'unlock_message_total_time': self.unlock_message_total_time,
            'unlock_message_fade_in_time': self.unlock_message_fade_in_time,
            'unlock_message_fade_out_time': self.unlock_message_fade_out_time,
            'unknown_struct26_0xa45e5b13': self.unknown_struct26_0xa45e5b13.to_json(),
            'unlock_concept_art': self.unlock_concept_art,
            'unlock_music': self.unlock_music,
            'unlock_diorama': self.unlock_diorama,
            'unlock_message_post_delay': self.unlock_message_post_delay,
        }


def _decode_credits_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_share_lines(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_extra_share_per_line(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_penultimate_share_bonus(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pre_penultimate_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_post_penultimate_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_final_share_bonus(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_image_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_image_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct26_0xba717f32(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0xc344a09a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0xd834e949(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x917857a0(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x7dfaff15(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0xe60799c8(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x45511f61(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x92b39f39(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unlock_message_total_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_message_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_message_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct26_0xa45e5b13(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unlock_concept_art(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_diorama(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_message_post_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc7a734ce: ('credits_time', _decode_credits_time),
    0x4efe6cde: ('normal_share_lines', _decode_normal_share_lines),
    0x7a54cb5e: ('extra_share_per_line', _decode_extra_share_per_line),
    0xfca1515c: ('penultimate_share_bonus', _decode_penultimate_share_bonus),
    0xb1133a84: ('pre_penultimate_delay', _decode_pre_penultimate_delay),
    0x5f230c67: ('post_penultimate_delay', _decode_post_penultimate_delay),
    0x9a9a7d1f: ('final_share_bonus', _decode_final_share_bonus),
    0xa091f393: ('text_fade_in_time', _decode_text_fade_in_time),
    0x98186a70: ('text_fade_out_time', _decode_text_fade_out_time),
    0xc1b9eef1: ('image_fade_in_time', _decode_image_fade_in_time),
    0x3bc54219: ('image_fade_out_time', _decode_image_fade_out_time),
    0xba717f32: ('unknown_struct26_0xba717f32', _decode_unknown_struct26_0xba717f32),
    0xc344a09a: ('unknown_struct26_0xc344a09a', _decode_unknown_struct26_0xc344a09a),
    0xd834e949: ('unknown_struct26_0xd834e949', _decode_unknown_struct26_0xd834e949),
    0x917857a0: ('unknown_struct26_0x917857a0', _decode_unknown_struct26_0x917857a0),
    0x7dfaff15: ('unknown_struct26_0x7dfaff15', _decode_unknown_struct26_0x7dfaff15),
    0xe60799c8: ('unknown_struct26_0xe60799c8', _decode_unknown_struct26_0xe60799c8),
    0x45511f61: ('unknown_struct26_0x45511f61', _decode_unknown_struct26_0x45511f61),
    0x92b39f39: ('unknown_struct26_0x92b39f39', _decode_unknown_struct26_0x92b39f39),
    0xb54b9d25: ('unlock_message_total_time', _decode_unlock_message_total_time),
    0x8fdc9487: ('unlock_message_fade_in_time', _decode_unlock_message_fade_in_time),
    0x82edf36a: ('unlock_message_fade_out_time', _decode_unlock_message_fade_out_time),
    0xa45e5b13: ('unknown_struct26_0xa45e5b13', _decode_unknown_struct26_0xa45e5b13),
    0x79589bf4: ('unlock_concept_art', _decode_unlock_concept_art),
    0xaf707df: ('unlock_music', _decode_unlock_music),
    0x5ce2a9a9: ('unlock_diorama', _decode_unlock_diorama),
    0x994aa27d: ('unlock_message_post_delay', _decode_unlock_message_post_delay),
}
