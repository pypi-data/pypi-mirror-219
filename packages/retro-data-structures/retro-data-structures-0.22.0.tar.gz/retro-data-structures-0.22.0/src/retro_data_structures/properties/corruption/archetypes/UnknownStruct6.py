# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct6(BaseProperty):
    gravity_buster_chance: float = dataclasses.field(default=35.0)
    combat_hatches_chance: float = dataclasses.field(default=25.0)
    dark_samus_echoes_chance: float = dataclasses.field(default=15.0)
    turret_chance: float = dataclasses.field(default=25.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xa1D3\xc3')  # 0xa14433c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_buster_chance))

        data.write(b'\xaf\xe4\x82\x13')  # 0xafe48213
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.combat_hatches_chance))

        data.write(b'\x05\xa5\xd4\xd0')  # 0x5a5d4d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dark_samus_echoes_chance))

        data.write(b'\xd5x\t\x05')  # 0xd5780905
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turret_chance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gravity_buster_chance=data['gravity_buster_chance'],
            combat_hatches_chance=data['combat_hatches_chance'],
            dark_samus_echoes_chance=data['dark_samus_echoes_chance'],
            turret_chance=data['turret_chance'],
        )

    def to_json(self) -> dict:
        return {
            'gravity_buster_chance': self.gravity_buster_chance,
            'combat_hatches_chance': self.combat_hatches_chance,
            'dark_samus_echoes_chance': self.dark_samus_echoes_chance,
            'turret_chance': self.turret_chance,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xa14433c3, 0xafe48213, 0x5a5d4d0, 0xd5780905)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct6]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct6(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_gravity_buster_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_combat_hatches_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dark_samus_echoes_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turret_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa14433c3: ('gravity_buster_chance', _decode_gravity_buster_chance),
    0xafe48213: ('combat_hatches_chance', _decode_combat_hatches_chance),
    0x5a5d4d0: ('dark_samus_echoes_chance', _decode_dark_samus_echoes_chance),
    0xd5780905: ('turret_chance', _decode_turret_chance),
}
