# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.TDamageInfo import TDamageInfo


@dataclasses.dataclass()
class DeathBall(BaseProperty):
    death_ball_damage_delay: float = dataclasses.field(default=0.5)
    death_ball_damage: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xc9\x15ho')  # 0xc915686f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.death_ball_damage_delay))

        data.write(b'\xcc\xcc\xef$')  # 0xccccef24
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.death_ball_damage.to_stream(data, default_override={'weapon_type': 5, 'damage_amount': 50.0, 'radius_damage_amount': 50.0, 'damage_radius': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            death_ball_damage_delay=data['death_ball_damage_delay'],
            death_ball_damage=TDamageInfo.from_json(data['death_ball_damage']),
        )

    def to_json(self) -> dict:
        return {
            'death_ball_damage_delay': self.death_ball_damage_delay,
            'death_ball_damage': self.death_ball_damage.to_json(),
        }


def _decode_death_ball_damage_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_ball_damage(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 5, 'damage_amount': 50.0, 'radius_damage_amount': 50.0, 'damage_radius': 2.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc915686f: ('death_ball_damage_delay', _decode_death_ball_damage_delay),
    0xccccef24: ('death_ball_damage', _decode_death_ball_damage),
}
