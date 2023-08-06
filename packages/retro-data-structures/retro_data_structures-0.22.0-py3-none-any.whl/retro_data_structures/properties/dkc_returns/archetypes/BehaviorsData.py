# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.BehaviorData import BehaviorData


@dataclasses.dataclass()
class BehaviorsData(BaseProperty):
    behavior0: BehaviorData = dataclasses.field(default_factory=BehaviorData)
    behavior1: BehaviorData = dataclasses.field(default_factory=BehaviorData)
    behavior2: BehaviorData = dataclasses.field(default_factory=BehaviorData)
    behavior3: BehaviorData = dataclasses.field(default_factory=BehaviorData)
    behavior4: BehaviorData = dataclasses.field(default_factory=BehaviorData)
    behavior5: BehaviorData = dataclasses.field(default_factory=BehaviorData)
    behavior6: BehaviorData = dataclasses.field(default_factory=BehaviorData)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xabG\x97_')  # 0xab47975f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior0.to_stream(data, default_override={'behavior_type': enums.BehaviorType.Unknown2})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xd1N\xda')  # 0x76d14eda
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior1.to_stream(data, default_override={'behavior_type': enums.BehaviorType.Unknown7})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb\x1b"\x14')  # 0xcb1b2214
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior2.to_stream(data, default_override={'behavior_type': enums.BehaviorType.Unknown3})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\x8d\xfb\x91')  # 0x168dfb91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior3.to_stream(data, default_override={'behavior_type': enums.BehaviorType.Unknown4})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'k\xfe\xfd\xc9')  # 0x6bfefdc9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior4.to_stream(data, default_override={'behavior_type': enums.BehaviorType.Unknown5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6h$L')  # 0xb668244c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b\xa2H\x82')  # 0xba24882
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            behavior0=BehaviorData.from_json(data['behavior0']),
            behavior1=BehaviorData.from_json(data['behavior1']),
            behavior2=BehaviorData.from_json(data['behavior2']),
            behavior3=BehaviorData.from_json(data['behavior3']),
            behavior4=BehaviorData.from_json(data['behavior4']),
            behavior5=BehaviorData.from_json(data['behavior5']),
            behavior6=BehaviorData.from_json(data['behavior6']),
        )

    def to_json(self) -> dict:
        return {
            'behavior0': self.behavior0.to_json(),
            'behavior1': self.behavior1.to_json(),
            'behavior2': self.behavior2.to_json(),
            'behavior3': self.behavior3.to_json(),
            'behavior4': self.behavior4.to_json(),
            'behavior5': self.behavior5.to_json(),
            'behavior6': self.behavior6.to_json(),
        }


def _decode_behavior0(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size, default_override={'behavior_type': enums.BehaviorType.Unknown2})


def _decode_behavior1(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size, default_override={'behavior_type': enums.BehaviorType.Unknown7})


def _decode_behavior2(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size, default_override={'behavior_type': enums.BehaviorType.Unknown3})


def _decode_behavior3(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size, default_override={'behavior_type': enums.BehaviorType.Unknown4})


def _decode_behavior4(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size, default_override={'behavior_type': enums.BehaviorType.Unknown5})


def _decode_behavior5(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size)


def _decode_behavior6(data: typing.BinaryIO, property_size: int):
    return BehaviorData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xab47975f: ('behavior0', _decode_behavior0),
    0x76d14eda: ('behavior1', _decode_behavior1),
    0xcb1b2214: ('behavior2', _decode_behavior2),
    0x168dfb91: ('behavior3', _decode_behavior3),
    0x6bfefdc9: ('behavior4', _decode_behavior4),
    0xb668244c: ('behavior5', _decode_behavior5),
    0xba24882: ('behavior6', _decode_behavior6),
}
