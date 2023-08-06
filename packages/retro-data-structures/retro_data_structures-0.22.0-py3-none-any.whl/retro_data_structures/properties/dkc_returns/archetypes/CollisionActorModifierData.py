# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.GenericCreatureStructC import GenericCreatureStructC


@dataclasses.dataclass()
class CollisionActorModifierData(BaseProperty):
    number_of_collision_actor_sets: int = dataclasses.field(default=0)
    actor_rule1: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC)
    actor_rule2: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC)
    actor_rule3: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC)
    actor_rule4: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC)
    actor_rule5: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'iP\xb5\xda')  # 0x6950b5da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_collision_actor_sets))

        data.write(b'\xd5Mo\xad')  # 0xd54d6fad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaeS\xedN')  # 0xae53ed4e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\x89n\xd0')  # 0x31896ed0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Xn\xe8\x88')  # 0x586ee888
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7\xb4k\x16')  # 0xc7b46b16
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_collision_actor_sets=data['number_of_collision_actor_sets'],
            actor_rule1=GenericCreatureStructC.from_json(data['actor_rule1']),
            actor_rule2=GenericCreatureStructC.from_json(data['actor_rule2']),
            actor_rule3=GenericCreatureStructC.from_json(data['actor_rule3']),
            actor_rule4=GenericCreatureStructC.from_json(data['actor_rule4']),
            actor_rule5=GenericCreatureStructC.from_json(data['actor_rule5']),
        )

    def to_json(self) -> dict:
        return {
            'number_of_collision_actor_sets': self.number_of_collision_actor_sets,
            'actor_rule1': self.actor_rule1.to_json(),
            'actor_rule2': self.actor_rule2.to_json(),
            'actor_rule3': self.actor_rule3.to_json(),
            'actor_rule4': self.actor_rule4.to_json(),
            'actor_rule5': self.actor_rule5.to_json(),
        }


def _decode_number_of_collision_actor_sets(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_actor_rule1(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructC.from_stream(data, property_size)


def _decode_actor_rule2(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructC.from_stream(data, property_size)


def _decode_actor_rule3(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructC.from_stream(data, property_size)


def _decode_actor_rule4(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructC.from_stream(data, property_size)


def _decode_actor_rule5(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructC.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6950b5da: ('number_of_collision_actor_sets', _decode_number_of_collision_actor_sets),
    0xd54d6fad: ('actor_rule1', _decode_actor_rule1),
    0xae53ed4e: ('actor_rule2', _decode_actor_rule2),
    0x31896ed0: ('actor_rule3', _decode_actor_rule3),
    0x586ee888: ('actor_rule4', _decode_actor_rule4),
    0xc7b46b16: ('actor_rule5', _decode_actor_rule5),
}
