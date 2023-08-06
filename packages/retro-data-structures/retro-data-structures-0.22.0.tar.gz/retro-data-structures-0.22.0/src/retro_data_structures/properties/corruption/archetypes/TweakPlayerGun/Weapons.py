# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.TBeamInfo import TBeamInfo
from retro_data_structures.properties.corruption.archetypes.TDamageInfo import TDamageInfo
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class Weapons(BaseProperty):
    bomb: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    unknown_0xe8907530: float = dataclasses.field(default=2.0)
    unknown_0x0a9186cb: float = dataclasses.field(default=0.6000000238418579)
    unknown_0x519c83e7: float = dataclasses.field(default=1.0)
    unknown_0xea7f3336: float = dataclasses.field(default=2.5)
    unknown_0xba3ef7ea: float = dataclasses.field(default=2.5)
    unknown_0xebdf0b9b: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xf9125d7e: Spline = dataclasses.field(default_factory=Spline)
    missile: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    unknown_0xe58d6c84: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    unknown_0xd26376fd: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    missile_reload_time: float = dataclasses.field(default=1.2999999523162842)
    power_beam: TBeamInfo = dataclasses.field(default_factory=TBeamInfo)
    unknown_0x86a941fc: TBeamInfo = dataclasses.field(default_factory=TBeamInfo)
    unknown_0x25906c03: TBeamInfo = dataclasses.field(default_factory=TBeamInfo)
    phazon_beam: TBeamInfo = dataclasses.field(default_factory=TBeamInfo)

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'as\xad\x96')  # 0x6173ad96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bomb.to_stream(data, default_override={'weapon_type': 7, 'radius_damage_amount': 10.0, 'damage_radius': 3.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe8\x90u0')  # 0xe8907530
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe8907530))

        data.write(b'\n\x91\x86\xcb')  # 0xa9186cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a9186cb))

        data.write(b'Q\x9c\x83\xe7')  # 0x519c83e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x519c83e7))

        data.write(b'\xea\x7f36')  # 0xea7f3336
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xea7f3336))

        data.write(b'\xba>\xf7\xea')  # 0xba3ef7ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xba3ef7ea))

        data.write(b'\xeb\xdf\x0b\x9b')  # 0xebdf0b9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xebdf0b9b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\x12]~')  # 0xf9125d7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xf9125d7e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\xf0\x0b\n')  # 0x58f00b0a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile.to_stream(data, default_override={'weapon_type': 4, 'damage_amount': 30.0, 'radius_damage_amount': 15.0, 'damage_radius': 4.5, 'knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x8dl\x84')  # 0xe58d6c84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xe58d6c84.to_stream(data, default_override={'weapon_type': 5, 'damage_amount': 30.0, 'radius_damage_amount': 15.0, 'damage_radius': 4.5, 'knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2cv\xfd')  # 0xd26376fd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd26376fd.to_stream(data, default_override={'weapon_type': 5, 'damage_amount': 30.0, 'radius_damage_amount': 15.0, 'damage_radius': 4.5, 'knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xf0\xa8\xa0')  # 0x43f0a8a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.missile_reload_time))

        data.write(b'\x1fl\x1ak')  # 0x1f6c1a6b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_beam.to_stream(data, default_override={'cooldown': 0.11100000143051147})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\xa9A\xfc')  # 0x86a941fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x86a941fc.to_stream(data, default_override={'cooldown': 0.5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%\x90l\x03')  # 0x25906c03
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x25906c03.to_stream(data, default_override={'cooldown': 0.33000001311302185})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd_.=')  # 0xdd5f2e3d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.phazon_beam.to_stream(data, default_override={'cooldown': 0.10000000149011612})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            bomb=TDamageInfo.from_json(data['bomb']),
            unknown_0xe8907530=data['unknown_0xe8907530'],
            unknown_0x0a9186cb=data['unknown_0x0a9186cb'],
            unknown_0x519c83e7=data['unknown_0x519c83e7'],
            unknown_0xea7f3336=data['unknown_0xea7f3336'],
            unknown_0xba3ef7ea=data['unknown_0xba3ef7ea'],
            unknown_0xebdf0b9b=Spline.from_json(data['unknown_0xebdf0b9b']),
            unknown_0xf9125d7e=Spline.from_json(data['unknown_0xf9125d7e']),
            missile=TDamageInfo.from_json(data['missile']),
            unknown_0xe58d6c84=TDamageInfo.from_json(data['unknown_0xe58d6c84']),
            unknown_0xd26376fd=TDamageInfo.from_json(data['unknown_0xd26376fd']),
            missile_reload_time=data['missile_reload_time'],
            power_beam=TBeamInfo.from_json(data['power_beam']),
            unknown_0x86a941fc=TBeamInfo.from_json(data['unknown_0x86a941fc']),
            unknown_0x25906c03=TBeamInfo.from_json(data['unknown_0x25906c03']),
            phazon_beam=TBeamInfo.from_json(data['phazon_beam']),
        )

    def to_json(self) -> dict:
        return {
            'bomb': self.bomb.to_json(),
            'unknown_0xe8907530': self.unknown_0xe8907530,
            'unknown_0x0a9186cb': self.unknown_0x0a9186cb,
            'unknown_0x519c83e7': self.unknown_0x519c83e7,
            'unknown_0xea7f3336': self.unknown_0xea7f3336,
            'unknown_0xba3ef7ea': self.unknown_0xba3ef7ea,
            'unknown_0xebdf0b9b': self.unknown_0xebdf0b9b.to_json(),
            'unknown_0xf9125d7e': self.unknown_0xf9125d7e.to_json(),
            'missile': self.missile.to_json(),
            'unknown_0xe58d6c84': self.unknown_0xe58d6c84.to_json(),
            'unknown_0xd26376fd': self.unknown_0xd26376fd.to_json(),
            'missile_reload_time': self.missile_reload_time,
            'power_beam': self.power_beam.to_json(),
            'unknown_0x86a941fc': self.unknown_0x86a941fc.to_json(),
            'unknown_0x25906c03': self.unknown_0x25906c03.to_json(),
            'phazon_beam': self.phazon_beam.to_json(),
        }


def _decode_bomb(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 7, 'radius_damage_amount': 10.0, 'damage_radius': 3.0})


def _decode_unknown_0xe8907530(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0a9186cb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x519c83e7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xea7f3336(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xba3ef7ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xebdf0b9b(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xf9125d7e(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_missile(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 4, 'damage_amount': 30.0, 'radius_damage_amount': 15.0, 'damage_radius': 4.5, 'knock_back_power': 4.0})


def _decode_unknown_0xe58d6c84(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 5, 'damage_amount': 30.0, 'radius_damage_amount': 15.0, 'damage_radius': 4.5, 'knock_back_power': 4.0})


def _decode_unknown_0xd26376fd(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 5, 'damage_amount': 30.0, 'radius_damage_amount': 15.0, 'damage_radius': 4.5, 'knock_back_power': 4.0})


def _decode_missile_reload_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_power_beam(data: typing.BinaryIO, property_size: int):
    return TBeamInfo.from_stream(data, property_size, default_override={'cooldown': 0.11100000143051147})


def _decode_unknown_0x86a941fc(data: typing.BinaryIO, property_size: int):
    return TBeamInfo.from_stream(data, property_size, default_override={'cooldown': 0.5})


def _decode_unknown_0x25906c03(data: typing.BinaryIO, property_size: int):
    return TBeamInfo.from_stream(data, property_size, default_override={'cooldown': 0.33000001311302185})


def _decode_phazon_beam(data: typing.BinaryIO, property_size: int):
    return TBeamInfo.from_stream(data, property_size, default_override={'cooldown': 0.10000000149011612})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6173ad96: ('bomb', _decode_bomb),
    0xe8907530: ('unknown_0xe8907530', _decode_unknown_0xe8907530),
    0xa9186cb: ('unknown_0x0a9186cb', _decode_unknown_0x0a9186cb),
    0x519c83e7: ('unknown_0x519c83e7', _decode_unknown_0x519c83e7),
    0xea7f3336: ('unknown_0xea7f3336', _decode_unknown_0xea7f3336),
    0xba3ef7ea: ('unknown_0xba3ef7ea', _decode_unknown_0xba3ef7ea),
    0xebdf0b9b: ('unknown_0xebdf0b9b', _decode_unknown_0xebdf0b9b),
    0xf9125d7e: ('unknown_0xf9125d7e', _decode_unknown_0xf9125d7e),
    0x58f00b0a: ('missile', _decode_missile),
    0xe58d6c84: ('unknown_0xe58d6c84', _decode_unknown_0xe58d6c84),
    0xd26376fd: ('unknown_0xd26376fd', _decode_unknown_0xd26376fd),
    0x43f0a8a0: ('missile_reload_time', _decode_missile_reload_time),
    0x1f6c1a6b: ('power_beam', _decode_power_beam),
    0x86a941fc: ('unknown_0x86a941fc', _decode_unknown_0x86a941fc),
    0x25906c03: ('unknown_0x25906c03', _decode_unknown_0x25906c03),
    0xdd5f2e3d: ('phazon_beam', _decode_phazon_beam),
}
