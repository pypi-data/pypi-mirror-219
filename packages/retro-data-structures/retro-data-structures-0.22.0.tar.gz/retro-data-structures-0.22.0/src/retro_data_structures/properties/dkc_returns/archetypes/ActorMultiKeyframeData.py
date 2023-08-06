# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.ActorMultiKeyframeStruct import ActorMultiKeyframeStruct


@dataclasses.dataclass()
class ActorMultiKeyframeData(BaseProperty):
    num_animations: int = dataclasses.field(default=0)
    actor_multi_keyframe_struct_0xe2db9114: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x085d4c76: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xe70ffa97: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x0621f0f3: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xe9734612: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x03f59b70: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xeca72d91: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x1ad889f9: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xf58a3f18: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xda6ba7ad: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x3539114c: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xdfbfcc2e: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x30ed7acf: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xd1c370ab: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x3e91c64a: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xd4171b28: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x3b45adc9: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0xcd3a09a1: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x2268bf40: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)
    actor_multi_keyframe_struct_0x793d2104: ActorMultiKeyframeStruct = dataclasses.field(default_factory=ActorMultiKeyframeStruct)

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'\x8d\xaa\x84"')  # 0x8daa8422
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_animations))

        data.write(b'\xe2\xdb\x91\x14')  # 0xe2db9114
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xe2db9114.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08]Lv')  # 0x85d4c76
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x085d4c76.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\x0f\xfa\x97')  # 0xe70ffa97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xe70ffa97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06!\xf0\xf3')  # 0x621f0f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x0621f0f3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9sF\x12')  # 0xe9734612
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xe9734612.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03\xf5\x9bp')  # 0x3f59b70
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x03f59b70.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec\xa7-\x91')  # 0xeca72d91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xeca72d91.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a\xd8\x89\xf9')  # 0x1ad889f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x1ad889f9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\x8a?\x18')  # 0xf58a3f18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xf58a3f18.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdak\xa7\xad')  # 0xda6ba7ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xda6ba7ad.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'59\x11L')  # 0x3539114c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x3539114c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\xbf\xcc.')  # 0xdfbfcc2e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xdfbfcc2e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\xedz\xcf')  # 0x30ed7acf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x30ed7acf.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1\xc3p\xab')  # 0xd1c370ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xd1c370ab.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\x91\xc6J')  # 0x3e91c64a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x3e91c64a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd4\x17\x1b(')  # 0xd4171b28
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xd4171b28.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';E\xad\xc9')  # 0x3b45adc9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x3b45adc9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd:\t\xa1')  # 0xcd3a09a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0xcd3a09a1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'"h\xbf@')  # 0x2268bf40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x2268bf40.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y=!\x04')  # 0x793d2104
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_multi_keyframe_struct_0x793d2104.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            num_animations=data['num_animations'],
            actor_multi_keyframe_struct_0xe2db9114=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xe2db9114']),
            actor_multi_keyframe_struct_0x085d4c76=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x085d4c76']),
            actor_multi_keyframe_struct_0xe70ffa97=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xe70ffa97']),
            actor_multi_keyframe_struct_0x0621f0f3=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x0621f0f3']),
            actor_multi_keyframe_struct_0xe9734612=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xe9734612']),
            actor_multi_keyframe_struct_0x03f59b70=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x03f59b70']),
            actor_multi_keyframe_struct_0xeca72d91=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xeca72d91']),
            actor_multi_keyframe_struct_0x1ad889f9=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x1ad889f9']),
            actor_multi_keyframe_struct_0xf58a3f18=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xf58a3f18']),
            actor_multi_keyframe_struct_0xda6ba7ad=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xda6ba7ad']),
            actor_multi_keyframe_struct_0x3539114c=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x3539114c']),
            actor_multi_keyframe_struct_0xdfbfcc2e=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xdfbfcc2e']),
            actor_multi_keyframe_struct_0x30ed7acf=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x30ed7acf']),
            actor_multi_keyframe_struct_0xd1c370ab=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xd1c370ab']),
            actor_multi_keyframe_struct_0x3e91c64a=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x3e91c64a']),
            actor_multi_keyframe_struct_0xd4171b28=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xd4171b28']),
            actor_multi_keyframe_struct_0x3b45adc9=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x3b45adc9']),
            actor_multi_keyframe_struct_0xcd3a09a1=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0xcd3a09a1']),
            actor_multi_keyframe_struct_0x2268bf40=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x2268bf40']),
            actor_multi_keyframe_struct_0x793d2104=ActorMultiKeyframeStruct.from_json(data['actor_multi_keyframe_struct_0x793d2104']),
        )

    def to_json(self) -> dict:
        return {
            'num_animations': self.num_animations,
            'actor_multi_keyframe_struct_0xe2db9114': self.actor_multi_keyframe_struct_0xe2db9114.to_json(),
            'actor_multi_keyframe_struct_0x085d4c76': self.actor_multi_keyframe_struct_0x085d4c76.to_json(),
            'actor_multi_keyframe_struct_0xe70ffa97': self.actor_multi_keyframe_struct_0xe70ffa97.to_json(),
            'actor_multi_keyframe_struct_0x0621f0f3': self.actor_multi_keyframe_struct_0x0621f0f3.to_json(),
            'actor_multi_keyframe_struct_0xe9734612': self.actor_multi_keyframe_struct_0xe9734612.to_json(),
            'actor_multi_keyframe_struct_0x03f59b70': self.actor_multi_keyframe_struct_0x03f59b70.to_json(),
            'actor_multi_keyframe_struct_0xeca72d91': self.actor_multi_keyframe_struct_0xeca72d91.to_json(),
            'actor_multi_keyframe_struct_0x1ad889f9': self.actor_multi_keyframe_struct_0x1ad889f9.to_json(),
            'actor_multi_keyframe_struct_0xf58a3f18': self.actor_multi_keyframe_struct_0xf58a3f18.to_json(),
            'actor_multi_keyframe_struct_0xda6ba7ad': self.actor_multi_keyframe_struct_0xda6ba7ad.to_json(),
            'actor_multi_keyframe_struct_0x3539114c': self.actor_multi_keyframe_struct_0x3539114c.to_json(),
            'actor_multi_keyframe_struct_0xdfbfcc2e': self.actor_multi_keyframe_struct_0xdfbfcc2e.to_json(),
            'actor_multi_keyframe_struct_0x30ed7acf': self.actor_multi_keyframe_struct_0x30ed7acf.to_json(),
            'actor_multi_keyframe_struct_0xd1c370ab': self.actor_multi_keyframe_struct_0xd1c370ab.to_json(),
            'actor_multi_keyframe_struct_0x3e91c64a': self.actor_multi_keyframe_struct_0x3e91c64a.to_json(),
            'actor_multi_keyframe_struct_0xd4171b28': self.actor_multi_keyframe_struct_0xd4171b28.to_json(),
            'actor_multi_keyframe_struct_0x3b45adc9': self.actor_multi_keyframe_struct_0x3b45adc9.to_json(),
            'actor_multi_keyframe_struct_0xcd3a09a1': self.actor_multi_keyframe_struct_0xcd3a09a1.to_json(),
            'actor_multi_keyframe_struct_0x2268bf40': self.actor_multi_keyframe_struct_0x2268bf40.to_json(),
            'actor_multi_keyframe_struct_0x793d2104': self.actor_multi_keyframe_struct_0x793d2104.to_json(),
        }


def _decode_num_animations(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_actor_multi_keyframe_struct_0xe2db9114(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x085d4c76(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xe70ffa97(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x0621f0f3(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xe9734612(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x03f59b70(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xeca72d91(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x1ad889f9(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xf58a3f18(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xda6ba7ad(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x3539114c(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xdfbfcc2e(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x30ed7acf(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xd1c370ab(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x3e91c64a(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xd4171b28(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x3b45adc9(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0xcd3a09a1(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x2268bf40(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


def _decode_actor_multi_keyframe_struct_0x793d2104(data: typing.BinaryIO, property_size: int):
    return ActorMultiKeyframeStruct.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8daa8422: ('num_animations', _decode_num_animations),
    0xe2db9114: ('actor_multi_keyframe_struct_0xe2db9114', _decode_actor_multi_keyframe_struct_0xe2db9114),
    0x85d4c76: ('actor_multi_keyframe_struct_0x085d4c76', _decode_actor_multi_keyframe_struct_0x085d4c76),
    0xe70ffa97: ('actor_multi_keyframe_struct_0xe70ffa97', _decode_actor_multi_keyframe_struct_0xe70ffa97),
    0x621f0f3: ('actor_multi_keyframe_struct_0x0621f0f3', _decode_actor_multi_keyframe_struct_0x0621f0f3),
    0xe9734612: ('actor_multi_keyframe_struct_0xe9734612', _decode_actor_multi_keyframe_struct_0xe9734612),
    0x3f59b70: ('actor_multi_keyframe_struct_0x03f59b70', _decode_actor_multi_keyframe_struct_0x03f59b70),
    0xeca72d91: ('actor_multi_keyframe_struct_0xeca72d91', _decode_actor_multi_keyframe_struct_0xeca72d91),
    0x1ad889f9: ('actor_multi_keyframe_struct_0x1ad889f9', _decode_actor_multi_keyframe_struct_0x1ad889f9),
    0xf58a3f18: ('actor_multi_keyframe_struct_0xf58a3f18', _decode_actor_multi_keyframe_struct_0xf58a3f18),
    0xda6ba7ad: ('actor_multi_keyframe_struct_0xda6ba7ad', _decode_actor_multi_keyframe_struct_0xda6ba7ad),
    0x3539114c: ('actor_multi_keyframe_struct_0x3539114c', _decode_actor_multi_keyframe_struct_0x3539114c),
    0xdfbfcc2e: ('actor_multi_keyframe_struct_0xdfbfcc2e', _decode_actor_multi_keyframe_struct_0xdfbfcc2e),
    0x30ed7acf: ('actor_multi_keyframe_struct_0x30ed7acf', _decode_actor_multi_keyframe_struct_0x30ed7acf),
    0xd1c370ab: ('actor_multi_keyframe_struct_0xd1c370ab', _decode_actor_multi_keyframe_struct_0xd1c370ab),
    0x3e91c64a: ('actor_multi_keyframe_struct_0x3e91c64a', _decode_actor_multi_keyframe_struct_0x3e91c64a),
    0xd4171b28: ('actor_multi_keyframe_struct_0xd4171b28', _decode_actor_multi_keyframe_struct_0xd4171b28),
    0x3b45adc9: ('actor_multi_keyframe_struct_0x3b45adc9', _decode_actor_multi_keyframe_struct_0x3b45adc9),
    0xcd3a09a1: ('actor_multi_keyframe_struct_0xcd3a09a1', _decode_actor_multi_keyframe_struct_0xcd3a09a1),
    0x2268bf40: ('actor_multi_keyframe_struct_0x2268bf40', _decode_actor_multi_keyframe_struct_0x2268bf40),
    0x793d2104: ('actor_multi_keyframe_struct_0x793d2104', _decode_actor_multi_keyframe_struct_0x793d2104),
}
