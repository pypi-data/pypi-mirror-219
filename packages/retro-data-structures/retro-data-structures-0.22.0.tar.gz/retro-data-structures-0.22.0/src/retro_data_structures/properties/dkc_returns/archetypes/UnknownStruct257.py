# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct256 import UnknownStruct256


@dataclasses.dataclass()
class UnknownStruct257(BaseProperty):
    unknown_0x1b5993a1: bool = dataclasses.field(default=False)
    unknown_0xf57d16e4: bool = dataclasses.field(default=False)
    unknown_0xb646a87e: bool = dataclasses.field(default=True)
    unknown_0x3818a74b: bool = dataclasses.field(default=True)
    unknown_0xb95d2954: bool = dataclasses.field(default=False)
    unknown_0x6551fc4a: bool = dataclasses.field(default=False)
    use_player_knockback: bool = dataclasses.field(default=True)
    use_player_push: bool = dataclasses.field(default=False)
    use_player_hurl: bool = dataclasses.field(default=False)
    anim_scale: float = dataclasses.field(default=1.0)
    unknown_0x626fa43d: float = dataclasses.field(default=1.0)
    unknown_struct256: UnknownStruct256 = dataclasses.field(default_factory=UnknownStruct256)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x1bY\x93\xa1')  # 0x1b5993a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1b5993a1))

        data.write(b'\xf5}\x16\xe4')  # 0xf57d16e4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf57d16e4))

        data.write(b'\xb6F\xa8~')  # 0xb646a87e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb646a87e))

        data.write(b'8\x18\xa7K')  # 0x3818a74b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3818a74b))

        data.write(b'\xb9])T')  # 0xb95d2954
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb95d2954))

        data.write(b'eQ\xfcJ')  # 0x6551fc4a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6551fc4a))

        data.write(b'\x16\x80\xa2T')  # 0x1680a254
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_knockback))

        data.write(b'\xd8\xb8\x84\xad')  # 0xd8b884ad
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_push))

        data.write(b'I:\xdbV')  # 0x493adb56
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_hurl))

        data.write(b'\x18x\xfa\x08')  # 0x1878fa08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anim_scale))

        data.write(b'bo\xa4=')  # 0x626fa43d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x626fa43d))

        data.write(b'\xbc\x98t\x8c')  # 0xbc98748c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct256.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x1b5993a1=data['unknown_0x1b5993a1'],
            unknown_0xf57d16e4=data['unknown_0xf57d16e4'],
            unknown_0xb646a87e=data['unknown_0xb646a87e'],
            unknown_0x3818a74b=data['unknown_0x3818a74b'],
            unknown_0xb95d2954=data['unknown_0xb95d2954'],
            unknown_0x6551fc4a=data['unknown_0x6551fc4a'],
            use_player_knockback=data['use_player_knockback'],
            use_player_push=data['use_player_push'],
            use_player_hurl=data['use_player_hurl'],
            anim_scale=data['anim_scale'],
            unknown_0x626fa43d=data['unknown_0x626fa43d'],
            unknown_struct256=UnknownStruct256.from_json(data['unknown_struct256']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x1b5993a1': self.unknown_0x1b5993a1,
            'unknown_0xf57d16e4': self.unknown_0xf57d16e4,
            'unknown_0xb646a87e': self.unknown_0xb646a87e,
            'unknown_0x3818a74b': self.unknown_0x3818a74b,
            'unknown_0xb95d2954': self.unknown_0xb95d2954,
            'unknown_0x6551fc4a': self.unknown_0x6551fc4a,
            'use_player_knockback': self.use_player_knockback,
            'use_player_push': self.use_player_push,
            'use_player_hurl': self.use_player_hurl,
            'anim_scale': self.anim_scale,
            'unknown_0x626fa43d': self.unknown_0x626fa43d,
            'unknown_struct256': self.unknown_struct256.to_json(),
        }


def _decode_unknown_0x1b5993a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf57d16e4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb646a87e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x3818a74b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb95d2954(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6551fc4a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_player_knockback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_player_push(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_player_hurl(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_anim_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x626fa43d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct256(data: typing.BinaryIO, property_size: int):
    return UnknownStruct256.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1b5993a1: ('unknown_0x1b5993a1', _decode_unknown_0x1b5993a1),
    0xf57d16e4: ('unknown_0xf57d16e4', _decode_unknown_0xf57d16e4),
    0xb646a87e: ('unknown_0xb646a87e', _decode_unknown_0xb646a87e),
    0x3818a74b: ('unknown_0x3818a74b', _decode_unknown_0x3818a74b),
    0xb95d2954: ('unknown_0xb95d2954', _decode_unknown_0xb95d2954),
    0x6551fc4a: ('unknown_0x6551fc4a', _decode_unknown_0x6551fc4a),
    0x1680a254: ('use_player_knockback', _decode_use_player_knockback),
    0xd8b884ad: ('use_player_push', _decode_use_player_push),
    0x493adb56: ('use_player_hurl', _decode_use_player_hurl),
    0x1878fa08: ('anim_scale', _decode_anim_scale),
    0x626fa43d: ('unknown_0x626fa43d', _decode_unknown_0x626fa43d),
    0xbc98748c: ('unknown_struct256', _decode_unknown_struct256),
}
