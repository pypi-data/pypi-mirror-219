# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.PlayerInventoryItem import PlayerInventoryItem


@dataclasses.dataclass()
class Weapons(BaseProperty):
    power_beam: bool = dataclasses.field(default=True)
    plasma_beam: bool = dataclasses.field(default=False)
    nova_beam: bool = dataclasses.field(default=False)
    charge_upgrade: bool = dataclasses.field(default=False)
    missile: PlayerInventoryItem = dataclasses.field(default_factory=PlayerInventoryItem)
    ice_missile: bool = dataclasses.field(default=False)
    seeker_missile: bool = dataclasses.field(default=False)
    grapple_beam_pull: bool = dataclasses.field(default=False)
    grapple_beam_swing: bool = dataclasses.field(default=False)
    grapple_beam_voltage: bool = dataclasses.field(default=False)
    bomb: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xf9\xbc>=')  # 0xf9bc3e3d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.power_beam))

        data.write(b'B\xc9\x00\xed')  # 0x42c900ed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.plasma_beam))

        data.write(b'J\xe2\x7f\xe7')  # 0x4ae27fe7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.nova_beam))

        data.write(b'\xf3O\x99\xd7')  # 0xf34f99d7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.charge_upgrade))

        data.write(b'\xa3\x87\x19\x1d')  # 0xa387191d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\xb3\xe6\x94')  # 0x5db3e694
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ice_missile))

        data.write(b'\x9a\xa4\x05\xc1')  # 0x9aa405c1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.seeker_missile))

        data.write(b'\xa4e\x86\x88')  # 0xa4658688
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_beam_pull))

        data.write(b'\xd2<\xf2\x9d')  # 0xd23cf29d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_beam_swing))

        data.write(b'Z~0\x1e')  # 0x5a7e301e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_beam_voltage))

        data.write(b'\xaf\xc6\x08-')  # 0xafc6082d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.bomb))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            power_beam=data['power_beam'],
            plasma_beam=data['plasma_beam'],
            nova_beam=data['nova_beam'],
            charge_upgrade=data['charge_upgrade'],
            missile=PlayerInventoryItem.from_json(data['missile']),
            ice_missile=data['ice_missile'],
            seeker_missile=data['seeker_missile'],
            grapple_beam_pull=data['grapple_beam_pull'],
            grapple_beam_swing=data['grapple_beam_swing'],
            grapple_beam_voltage=data['grapple_beam_voltage'],
            bomb=data['bomb'],
        )

    def to_json(self) -> dict:
        return {
            'power_beam': self.power_beam,
            'plasma_beam': self.plasma_beam,
            'nova_beam': self.nova_beam,
            'charge_upgrade': self.charge_upgrade,
            'missile': self.missile.to_json(),
            'ice_missile': self.ice_missile,
            'seeker_missile': self.seeker_missile,
            'grapple_beam_pull': self.grapple_beam_pull,
            'grapple_beam_swing': self.grapple_beam_swing,
            'grapple_beam_voltage': self.grapple_beam_voltage,
            'bomb': self.bomb,
        }


def _decode_power_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_plasma_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_nova_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_charge_upgrade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_missile(data: typing.BinaryIO, property_size: int):
    return PlayerInventoryItem.from_stream(data, property_size)


def _decode_ice_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seeker_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_beam_pull(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_beam_swing(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_beam_voltage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bomb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf9bc3e3d: ('power_beam', _decode_power_beam),
    0x42c900ed: ('plasma_beam', _decode_plasma_beam),
    0x4ae27fe7: ('nova_beam', _decode_nova_beam),
    0xf34f99d7: ('charge_upgrade', _decode_charge_upgrade),
    0xa387191d: ('missile', _decode_missile),
    0x5db3e694: ('ice_missile', _decode_ice_missile),
    0x9aa405c1: ('seeker_missile', _decode_seeker_missile),
    0xa4658688: ('grapple_beam_pull', _decode_grapple_beam_pull),
    0xd23cf29d: ('grapple_beam_swing', _decode_grapple_beam_swing),
    0x5a7e301e: ('grapple_beam_voltage', _decode_grapple_beam_voltage),
    0xafc6082d: ('bomb', _decode_bomb),
}
