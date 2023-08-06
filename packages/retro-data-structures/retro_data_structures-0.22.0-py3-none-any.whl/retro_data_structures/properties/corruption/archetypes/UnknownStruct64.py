# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.FlyerMovementMode import FlyerMovementMode
from retro_data_structures.properties.corruption.archetypes.SpriteStruct import SpriteStruct


@dataclasses.dataclass()
class UnknownStruct64(BaseProperty):
    patrol: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    sprite_struct_0x2cbb438b: SpriteStruct = dataclasses.field(default_factory=SpriteStruct)
    sprite_struct_0xa80227e6: SpriteStruct = dataclasses.field(default_factory=SpriteStruct)
    sprite_struct_0x34799811: SpriteStruct = dataclasses.field(default_factory=SpriteStruct)
    flash_range: float = dataclasses.field(default=0.0)
    flash_range_max: float = dataclasses.field(default=0.0)
    flash_intensity: float = dataclasses.field(default=0.0)
    flash_duration: float = dataclasses.field(default=0.0)
    unknown: float = dataclasses.field(default=0.0)
    flash_delay: float = dataclasses.field(default=0.0)
    scan_delay: float = dataclasses.field(default=0.0)

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

        data.write(b'\xcc\xdd:\xca')  # 0xccdd3aca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patrol.to_stream(data, default_override={'speed': 1.0, 'acceleration': 0.5, 'facing_turn_rate': 10.0, 'turn_threshold': 180.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',\xbbC\x8b')  # 0x2cbb438b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sprite_struct_0x2cbb438b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xa8\x02'\xe6")  # 0xa80227e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sprite_struct_0xa80227e6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'4y\x98\x11')  # 0x34799811
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sprite_struct_0x34799811.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&\x94^ ')  # 0x26945e20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_range))

        data.write(b'\x7f\x87\x8c\x1c')  # 0x7f878c1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_range_max))

        data.write(b'nW]g')  # 0x6e575d67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_intensity))

        data.write(b'\x8e\xbe\xa5\x96')  # 0x8ebea596
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_duration))

        data.write(b'B\x9cf\xd3')  # 0x429c66d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\x04)\x0e$')  # 0x4290e24
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flash_delay))

        data.write(b"\x7f\xc8'\xa2")  # 0x7fc827a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_delay))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            patrol=FlyerMovementMode.from_json(data['patrol']),
            sprite_struct_0x2cbb438b=SpriteStruct.from_json(data['sprite_struct_0x2cbb438b']),
            sprite_struct_0xa80227e6=SpriteStruct.from_json(data['sprite_struct_0xa80227e6']),
            sprite_struct_0x34799811=SpriteStruct.from_json(data['sprite_struct_0x34799811']),
            flash_range=data['flash_range'],
            flash_range_max=data['flash_range_max'],
            flash_intensity=data['flash_intensity'],
            flash_duration=data['flash_duration'],
            unknown=data['unknown'],
            flash_delay=data['flash_delay'],
            scan_delay=data['scan_delay'],
        )

    def to_json(self) -> dict:
        return {
            'patrol': self.patrol.to_json(),
            'sprite_struct_0x2cbb438b': self.sprite_struct_0x2cbb438b.to_json(),
            'sprite_struct_0xa80227e6': self.sprite_struct_0xa80227e6.to_json(),
            'sprite_struct_0x34799811': self.sprite_struct_0x34799811.to_json(),
            'flash_range': self.flash_range,
            'flash_range_max': self.flash_range_max,
            'flash_intensity': self.flash_intensity,
            'flash_duration': self.flash_duration,
            'unknown': self.unknown,
            'flash_delay': self.flash_delay,
            'scan_delay': self.scan_delay,
        }


def _decode_patrol(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 1.0, 'acceleration': 0.5, 'facing_turn_rate': 10.0, 'turn_threshold': 180.0})


def _decode_sprite_struct_0x2cbb438b(data: typing.BinaryIO, property_size: int):
    return SpriteStruct.from_stream(data, property_size)


def _decode_sprite_struct_0xa80227e6(data: typing.BinaryIO, property_size: int):
    return SpriteStruct.from_stream(data, property_size)


def _decode_sprite_struct_0x34799811(data: typing.BinaryIO, property_size: int):
    return SpriteStruct.from_stream(data, property_size)


def _decode_flash_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_range_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_intensity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xccdd3aca: ('patrol', _decode_patrol),
    0x2cbb438b: ('sprite_struct_0x2cbb438b', _decode_sprite_struct_0x2cbb438b),
    0xa80227e6: ('sprite_struct_0xa80227e6', _decode_sprite_struct_0xa80227e6),
    0x34799811: ('sprite_struct_0x34799811', _decode_sprite_struct_0x34799811),
    0x26945e20: ('flash_range', _decode_flash_range),
    0x7f878c1c: ('flash_range_max', _decode_flash_range_max),
    0x6e575d67: ('flash_intensity', _decode_flash_intensity),
    0x8ebea596: ('flash_duration', _decode_flash_duration),
    0x429c66d3: ('unknown', _decode_unknown),
    0x4290e24: ('flash_delay', _decode_flash_delay),
    0x7fc827a2: ('scan_delay', _decode_scan_delay),
}
