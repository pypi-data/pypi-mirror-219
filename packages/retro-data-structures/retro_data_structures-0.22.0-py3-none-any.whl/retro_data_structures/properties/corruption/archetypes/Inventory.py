# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.Abilities import Abilities
from retro_data_structures.properties.corruption.archetypes.Ball import Ball
from retro_data_structures.properties.corruption.archetypes.HyperMode import HyperMode
from retro_data_structures.properties.corruption.archetypes.Misc import Misc
from retro_data_structures.properties.corruption.archetypes.Ship import Ship
from retro_data_structures.properties.corruption.archetypes.Visors import Visors
from retro_data_structures.properties.corruption.archetypes.Weapons import Weapons


@dataclasses.dataclass()
class Inventory(BaseProperty):
    misc: Misc = dataclasses.field(default_factory=Misc)
    weapons: Weapons = dataclasses.field(default_factory=Weapons)
    visors: Visors = dataclasses.field(default_factory=Visors)
    ball: Ball = dataclasses.field(default_factory=Ball)
    abilities: Abilities = dataclasses.field(default_factory=Abilities)
    hyper_mode: HyperMode = dataclasses.field(default_factory=HyperMode)
    ship: Ship = dataclasses.field(default_factory=Ship)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'R\xc7y\xc0')  # 0x52c779c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xefC\xb8E')  # 0xef43b845
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapons.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1}E\xbb')  # 0x317d45bb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.visors.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\x7f;J')  # 0xed7f3b4a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&\x7f\x91\xe5')  # 0x267f91e5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.abilities.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\x8e\x02\xb2')  # 0x378e02b2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9\xc4\xa7\x86')  # 0xe9c4a786
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            misc=Misc.from_json(data['misc']),
            weapons=Weapons.from_json(data['weapons']),
            visors=Visors.from_json(data['visors']),
            ball=Ball.from_json(data['ball']),
            abilities=Abilities.from_json(data['abilities']),
            hyper_mode=HyperMode.from_json(data['hyper_mode']),
            ship=Ship.from_json(data['ship']),
        )

    def to_json(self) -> dict:
        return {
            'misc': self.misc.to_json(),
            'weapons': self.weapons.to_json(),
            'visors': self.visors.to_json(),
            'ball': self.ball.to_json(),
            'abilities': self.abilities.to_json(),
            'hyper_mode': self.hyper_mode.to_json(),
            'ship': self.ship.to_json(),
        }


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_weapons(data: typing.BinaryIO, property_size: int):
    return Weapons.from_stream(data, property_size)


def _decode_visors(data: typing.BinaryIO, property_size: int):
    return Visors.from_stream(data, property_size)


def _decode_ball(data: typing.BinaryIO, property_size: int):
    return Ball.from_stream(data, property_size)


def _decode_abilities(data: typing.BinaryIO, property_size: int):
    return Abilities.from_stream(data, property_size)


def _decode_hyper_mode(data: typing.BinaryIO, property_size: int):
    return HyperMode.from_stream(data, property_size)


def _decode_ship(data: typing.BinaryIO, property_size: int):
    return Ship.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x52c779c0: ('misc', _decode_misc),
    0xef43b845: ('weapons', _decode_weapons),
    0x317d45bb: ('visors', _decode_visors),
    0xed7f3b4a: ('ball', _decode_ball),
    0x267f91e5: ('abilities', _decode_abilities),
    0x378e02b2: ('hyper_mode', _decode_hyper_mode),
    0xe9c4a786: ('ship', _decode_ship),
}
