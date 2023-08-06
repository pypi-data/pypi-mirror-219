# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class PlayerWeaponControls(BaseProperty):
    fire_beam: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    auto_fire_beam: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    charge_beam: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    fire_missile: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    fire_seeker: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    hyper_mode: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    switch_weapons: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    aim_up_control: Spline = dataclasses.field(default_factory=Spline)
    aim_down_control: Spline = dataclasses.field(default_factory=Spline)
    aim_left_control: Spline = dataclasses.field(default_factory=Spline)
    aim_right_control: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x03b0a66b: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x1a86616e: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x05f281c4: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x42c64d90: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x82\x16\x88`')  # 0x82168860
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fire_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd5\\$\xc4')  # 0xd55c24c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.auto_fire_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'o\xe9=p')  # 0x6fe93d70
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb\xb8\x8c\xb7')  # 0xcbb88cb7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fire_missile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'q\x18\x04\xa6')  # 0x711804a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fire_seeker.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xd94\x0e')  # 0xfad9340e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\xa6\x9aS')  # 0x78a69a53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.switch_weapons.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00/\x1e\x9d')  # 0x2f1e9d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aim_up_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xd9E\xbe')  # 0xfad945be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aim_down_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1f\x12\\')  # 0xa166125c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aim_left_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\x87\xaaN')  # 0xdf87aa4e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aim_right_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03\xb0\xa6k')  # 0x3b0a66b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x03b0a66b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a\x86an')  # 0x1a86616e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1a86616e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05\xf2\x81\xc4')  # 0x5f281c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x05f281c4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\xc6M\x90')  # 0x42c64d90
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x42c64d90))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            fire_beam=RevolutionControl.from_json(data['fire_beam']),
            auto_fire_beam=RevolutionControl.from_json(data['auto_fire_beam']),
            charge_beam=RevolutionControl.from_json(data['charge_beam']),
            fire_missile=RevolutionControl.from_json(data['fire_missile']),
            fire_seeker=RevolutionControl.from_json(data['fire_seeker']),
            hyper_mode=RevolutionControl.from_json(data['hyper_mode']),
            switch_weapons=RevolutionControl.from_json(data['switch_weapons']),
            aim_up_control=Spline.from_json(data['aim_up_control']),
            aim_down_control=Spline.from_json(data['aim_down_control']),
            aim_left_control=Spline.from_json(data['aim_left_control']),
            aim_right_control=Spline.from_json(data['aim_right_control']),
            unknown_0x03b0a66b=Spline.from_json(data['unknown_0x03b0a66b']),
            unknown_0x1a86616e=Spline.from_json(data['unknown_0x1a86616e']),
            unknown_0x05f281c4=Spline.from_json(data['unknown_0x05f281c4']),
            unknown_0x42c64d90=data['unknown_0x42c64d90'],
        )

    def to_json(self) -> dict:
        return {
            'fire_beam': self.fire_beam.to_json(),
            'auto_fire_beam': self.auto_fire_beam.to_json(),
            'charge_beam': self.charge_beam.to_json(),
            'fire_missile': self.fire_missile.to_json(),
            'fire_seeker': self.fire_seeker.to_json(),
            'hyper_mode': self.hyper_mode.to_json(),
            'switch_weapons': self.switch_weapons.to_json(),
            'aim_up_control': self.aim_up_control.to_json(),
            'aim_down_control': self.aim_down_control.to_json(),
            'aim_left_control': self.aim_left_control.to_json(),
            'aim_right_control': self.aim_right_control.to_json(),
            'unknown_0x03b0a66b': self.unknown_0x03b0a66b.to_json(),
            'unknown_0x1a86616e': self.unknown_0x1a86616e.to_json(),
            'unknown_0x05f281c4': self.unknown_0x05f281c4.to_json(),
            'unknown_0x42c64d90': self.unknown_0x42c64d90,
        }


def _decode_fire_beam(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_auto_fire_beam(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_charge_beam(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_fire_missile(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_fire_seeker(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_hyper_mode(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_switch_weapons(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_aim_up_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_aim_down_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_aim_left_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_aim_right_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x03b0a66b(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x1a86616e(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x05f281c4(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x42c64d90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x82168860: ('fire_beam', _decode_fire_beam),
    0xd55c24c4: ('auto_fire_beam', _decode_auto_fire_beam),
    0x6fe93d70: ('charge_beam', _decode_charge_beam),
    0xcbb88cb7: ('fire_missile', _decode_fire_missile),
    0x711804a6: ('fire_seeker', _decode_fire_seeker),
    0xfad9340e: ('hyper_mode', _decode_hyper_mode),
    0x78a69a53: ('switch_weapons', _decode_switch_weapons),
    0x2f1e9d: ('aim_up_control', _decode_aim_up_control),
    0xfad945be: ('aim_down_control', _decode_aim_down_control),
    0xa166125c: ('aim_left_control', _decode_aim_left_control),
    0xdf87aa4e: ('aim_right_control', _decode_aim_right_control),
    0x3b0a66b: ('unknown_0x03b0a66b', _decode_unknown_0x03b0a66b),
    0x1a86616e: ('unknown_0x1a86616e', _decode_unknown_0x1a86616e),
    0x5f281c4: ('unknown_0x05f281c4', _decode_unknown_0x05f281c4),
    0x42c64d90: ('unknown_0x42c64d90', _decode_unknown_0x42c64d90),
}
