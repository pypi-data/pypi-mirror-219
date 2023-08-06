# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class ReactiveActorBehavior(BaseProperty):
    triggering_behavior: enums.TriggeringBehavior = dataclasses.field(default=enums.TriggeringBehavior.Unknown1)
    player: bool = dataclasses.field(default=False)
    rambi: bool = dataclasses.field(default=False)
    generic_creature: bool = dataclasses.field(default=False)
    actor: bool = dataclasses.field(default=False)
    unknown_0xbb0ee668: int = dataclasses.field(default=0)
    repeat_delay: float = dataclasses.field(default=0.0)
    detection_radius: float = dataclasses.field(default=1.0)
    unknown_0x8ffefc1e: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xde\x87Tj')  # 0xde87546a
        data.write(b'\x00\x04')  # size
        self.triggering_behavior.to_stream(data)

        data.write(b'\xd5i\x92d')  # 0xd5699264
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player))

        data.write(b'\x16\xa9]B')  # 0x16a95d42
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rambi))

        data.write(b'\x07\x93\xa3\xf7')  # 0x793a3f7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.generic_creature))

        data.write(b'\x98)H\xdb')  # 0x982948db
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.actor))

        data.write(b'\xbb\x0e\xe6h')  # 0xbb0ee668
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbb0ee668))

        data.write(b'!1\x1d\xce')  # 0x21311dce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.repeat_delay))

        data.write(b'!\xcd\xcf!')  # 0x21cdcf21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_radius))

        data.write(b'\x8f\xfe\xfc\x1e')  # 0x8ffefc1e
        data.write(b'\x00\x0c')  # size
        self.unknown_0x8ffefc1e.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            triggering_behavior=enums.TriggeringBehavior.from_json(data['triggering_behavior']),
            player=data['player'],
            rambi=data['rambi'],
            generic_creature=data['generic_creature'],
            actor=data['actor'],
            unknown_0xbb0ee668=data['unknown_0xbb0ee668'],
            repeat_delay=data['repeat_delay'],
            detection_radius=data['detection_radius'],
            unknown_0x8ffefc1e=Vector.from_json(data['unknown_0x8ffefc1e']),
        )

    def to_json(self) -> dict:
        return {
            'triggering_behavior': self.triggering_behavior.to_json(),
            'player': self.player,
            'rambi': self.rambi,
            'generic_creature': self.generic_creature,
            'actor': self.actor,
            'unknown_0xbb0ee668': self.unknown_0xbb0ee668,
            'repeat_delay': self.repeat_delay,
            'detection_radius': self.detection_radius,
            'unknown_0x8ffefc1e': self.unknown_0x8ffefc1e.to_json(),
        }


def _decode_triggering_behavior(data: typing.BinaryIO, property_size: int):
    return enums.TriggeringBehavior.from_stream(data)


def _decode_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_generic_creature(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_actor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbb0ee668(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_repeat_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8ffefc1e(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde87546a: ('triggering_behavior', _decode_triggering_behavior),
    0xd5699264: ('player', _decode_player),
    0x16a95d42: ('rambi', _decode_rambi),
    0x793a3f7: ('generic_creature', _decode_generic_creature),
    0x982948db: ('actor', _decode_actor),
    0xbb0ee668: ('unknown_0xbb0ee668', _decode_unknown_0xbb0ee668),
    0x21311dce: ('repeat_delay', _decode_repeat_delay),
    0x21cdcf21: ('detection_radius', _decode_detection_radius),
    0x8ffefc1e: ('unknown_0x8ffefc1e', _decode_unknown_0x8ffefc1e),
}
