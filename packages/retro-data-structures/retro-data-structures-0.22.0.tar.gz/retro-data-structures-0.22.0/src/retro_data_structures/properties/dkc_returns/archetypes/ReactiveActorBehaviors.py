# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.ReactiveActorBehavior import ReactiveActorBehavior


@dataclasses.dataclass()
class ReactiveActorBehaviors(BaseProperty):
    num_behaviors: int = dataclasses.field(default=0)
    behavior1: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior)
    behavior2: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior)
    behavior3: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior)
    behavior4: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior)
    behavior5: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior)
    behavior6: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior)

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

        data.write(b'\xc0\x7f\xa9\xbe')  # 0xc07fa9be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_behaviors))

        data.write(b'\x8e\xa6|O')  # 0x8ea67c4f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\xde\xd1\x0f')  # 0xb7ded10f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0\xf6\xb5\xcf')  # 0xa0f6b5cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5/\x8b\x8f')  # 0xc52f8b8f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x07\xefO')  # 0xd207ef4f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\x7fB\x0f')  # 0xeb7f420f
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
            num_behaviors=data['num_behaviors'],
            behavior1=ReactiveActorBehavior.from_json(data['behavior1']),
            behavior2=ReactiveActorBehavior.from_json(data['behavior2']),
            behavior3=ReactiveActorBehavior.from_json(data['behavior3']),
            behavior4=ReactiveActorBehavior.from_json(data['behavior4']),
            behavior5=ReactiveActorBehavior.from_json(data['behavior5']),
            behavior6=ReactiveActorBehavior.from_json(data['behavior6']),
        )

    def to_json(self) -> dict:
        return {
            'num_behaviors': self.num_behaviors,
            'behavior1': self.behavior1.to_json(),
            'behavior2': self.behavior2.to_json(),
            'behavior3': self.behavior3.to_json(),
            'behavior4': self.behavior4.to_json(),
            'behavior5': self.behavior5.to_json(),
            'behavior6': self.behavior6.to_json(),
        }


def _decode_num_behaviors(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_behavior1(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehavior.from_stream(data, property_size)


def _decode_behavior2(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehavior.from_stream(data, property_size)


def _decode_behavior3(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehavior.from_stream(data, property_size)


def _decode_behavior4(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehavior.from_stream(data, property_size)


def _decode_behavior5(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehavior.from_stream(data, property_size)


def _decode_behavior6(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehavior.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc07fa9be: ('num_behaviors', _decode_num_behaviors),
    0x8ea67c4f: ('behavior1', _decode_behavior1),
    0xb7ded10f: ('behavior2', _decode_behavior2),
    0xa0f6b5cf: ('behavior3', _decode_behavior3),
    0xc52f8b8f: ('behavior4', _decode_behavior4),
    0xd207ef4f: ('behavior5', _decode_behavior5),
    0xeb7f420f: ('behavior6', _decode_behavior6),
}
