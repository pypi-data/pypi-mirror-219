# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class DigitalGuardianHeadStruct(BaseProperty):
    first_shot_type: int = dataclasses.field(default=4)
    projectile_telegraph_time: float = dataclasses.field(default=1.25)
    projectile_attack_time: float = dataclasses.field(default=2.0)
    unknown_0xfdfca535: float = dataclasses.field(default=25.0)
    unknown_0xcd03632c: float = dataclasses.field(default=25.0)
    unknown_0xf1548397: float = dataclasses.field(default=25.0)
    unknown_0xf967e246: float = dataclasses.field(default=25.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xd2\x02\x88\xa4')  # 0xd20288a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.first_shot_type))

        data.write(b'u\xdc\x92\xbc')  # 0x75dc92bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_telegraph_time))

        data.write(b'\x9e\x1c?l')  # 0x9e1c3f6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_attack_time))

        data.write(b'\xfd\xfc\xa55')  # 0xfdfca535
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfdfca535))

        data.write(b'\xcd\x03c,')  # 0xcd03632c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd03632c))

        data.write(b'\xf1T\x83\x97')  # 0xf1548397
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf1548397))

        data.write(b'\xf9g\xe2F')  # 0xf967e246
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf967e246))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            first_shot_type=data['first_shot_type'],
            projectile_telegraph_time=data['projectile_telegraph_time'],
            projectile_attack_time=data['projectile_attack_time'],
            unknown_0xfdfca535=data['unknown_0xfdfca535'],
            unknown_0xcd03632c=data['unknown_0xcd03632c'],
            unknown_0xf1548397=data['unknown_0xf1548397'],
            unknown_0xf967e246=data['unknown_0xf967e246'],
        )

    def to_json(self) -> dict:
        return {
            'first_shot_type': self.first_shot_type,
            'projectile_telegraph_time': self.projectile_telegraph_time,
            'projectile_attack_time': self.projectile_attack_time,
            'unknown_0xfdfca535': self.unknown_0xfdfca535,
            'unknown_0xcd03632c': self.unknown_0xcd03632c,
            'unknown_0xf1548397': self.unknown_0xf1548397,
            'unknown_0xf967e246': self.unknown_0xf967e246,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xd20288a4, 0x75dc92bc, 0x9e1c3f6c, 0xfdfca535, 0xcd03632c, 0xf1548397, 0xf967e246)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DigitalGuardianHeadStruct]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(70))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return DigitalGuardianHeadStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_first_shot_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_projectile_telegraph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfdfca535(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd03632c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf1548397(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf967e246(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd20288a4: ('first_shot_type', _decode_first_shot_type),
    0x75dc92bc: ('projectile_telegraph_time', _decode_projectile_telegraph_time),
    0x9e1c3f6c: ('projectile_attack_time', _decode_projectile_attack_time),
    0xfdfca535: ('unknown_0xfdfca535', _decode_unknown_0xfdfca535),
    0xcd03632c: ('unknown_0xcd03632c', _decode_unknown_0xcd03632c),
    0xf1548397: ('unknown_0xf1548397', _decode_unknown_0xf1548397),
    0xf967e246: ('unknown_0xf967e246', _decode_unknown_0xf967e246),
}
