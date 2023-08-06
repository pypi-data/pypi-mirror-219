# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct193 import UnknownStruct193
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class ProjectileData(BaseProperty):
    max_lifetime: float = dataclasses.field(default=30.0)
    unknown_0x9cbc24b1: bool = dataclasses.field(default=False)
    unknown_0x7e2ea16c: bool = dataclasses.field(default=False)
    explosion_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xebefb1a9: bool = dataclasses.field(default=False)
    use_alternate_damage_effect: bool = dataclasses.field(default=False)
    launch_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    crash_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    flight_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x05c67d0b: bool = dataclasses.field(default=False)
    launch_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    crash_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    flight_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    orientation: enums.Orientation = dataclasses.field(default=enums.Orientation.Unknown1)
    unknown_0xa17c618d: bool = dataclasses.field(default=False)
    unknown_0x469f8fb8: bool = dataclasses.field(default=False)
    constant_rotation: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_struct193: UnknownStruct193 = dataclasses.field(default_factory=UnknownStruct193)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\xd4\xd4\xed\xfa')  # 0xd4d4edfa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_lifetime))

        data.write(b'\x9c\xbc$\xb1')  # 0x9cbc24b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9cbc24b1))

        data.write(b'~.\xa1l')  # 0x7e2ea16c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7e2ea16c))

        data.write(b'\xde\xfft\xea')  # 0xdeff74ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.explosion_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xef\xb1\xa9')  # 0xebefb1a9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xebefb1a9))

        data.write(b'\xf0\x99;\xfe')  # 0xf0993bfe
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_alternate_damage_effect))

        data.write(b'\xa4i.\x9c')  # 0xa4692e9c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.launch_effect))

        data.write(b'\xa0n\xda\xf9')  # 0xa06edaf9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.crash_effect))

        data.write(b'\xde\x15e\xa9')  # 0xde1565a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flight_effect))

        data.write(b'\x05\xc6}\x0b')  # 0x5c67d0b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x05c67d0b))

        data.write(b'\xf7\xf7\xf6\xaf')  # 0xf7f7f6af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.launch_sound))

        data.write(b'+%\x86)')  # 0x2b258629
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.crash_sound))

        data.write(b'\xe1\xe6k$')  # 0xe1e66b24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flight_sound))

        data.write(b'\xf4\xbff7')  # 0xf4bf6637
        data.write(b'\x00\x04')  # size
        self.orientation.to_stream(data)

        data.write(b'\xa1|a\x8d')  # 0xa17c618d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa17c618d))

        data.write(b'F\x9f\x8f\xb8')  # 0x469f8fb8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x469f8fb8))

        data.write(b'\xec\x08(\xce')  # 0xec0828ce
        data.write(b'\x00\x0c')  # size
        self.constant_rotation.to_stream(data)

        data.write(b'\x01\x83\xdcq')  # 0x183dc71
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct193.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            max_lifetime=data['max_lifetime'],
            unknown_0x9cbc24b1=data['unknown_0x9cbc24b1'],
            unknown_0x7e2ea16c=data['unknown_0x7e2ea16c'],
            explosion_damage=DamageInfo.from_json(data['explosion_damage']),
            unknown_0xebefb1a9=data['unknown_0xebefb1a9'],
            use_alternate_damage_effect=data['use_alternate_damage_effect'],
            launch_effect=data['launch_effect'],
            crash_effect=data['crash_effect'],
            flight_effect=data['flight_effect'],
            unknown_0x05c67d0b=data['unknown_0x05c67d0b'],
            launch_sound=data['launch_sound'],
            crash_sound=data['crash_sound'],
            flight_sound=data['flight_sound'],
            orientation=enums.Orientation.from_json(data['orientation']),
            unknown_0xa17c618d=data['unknown_0xa17c618d'],
            unknown_0x469f8fb8=data['unknown_0x469f8fb8'],
            constant_rotation=Vector.from_json(data['constant_rotation']),
            unknown_struct193=UnknownStruct193.from_json(data['unknown_struct193']),
        )

    def to_json(self) -> dict:
        return {
            'max_lifetime': self.max_lifetime,
            'unknown_0x9cbc24b1': self.unknown_0x9cbc24b1,
            'unknown_0x7e2ea16c': self.unknown_0x7e2ea16c,
            'explosion_damage': self.explosion_damage.to_json(),
            'unknown_0xebefb1a9': self.unknown_0xebefb1a9,
            'use_alternate_damage_effect': self.use_alternate_damage_effect,
            'launch_effect': self.launch_effect,
            'crash_effect': self.crash_effect,
            'flight_effect': self.flight_effect,
            'unknown_0x05c67d0b': self.unknown_0x05c67d0b,
            'launch_sound': self.launch_sound,
            'crash_sound': self.crash_sound,
            'flight_sound': self.flight_sound,
            'orientation': self.orientation.to_json(),
            'unknown_0xa17c618d': self.unknown_0xa17c618d,
            'unknown_0x469f8fb8': self.unknown_0x469f8fb8,
            'constant_rotation': self.constant_rotation.to_json(),
            'unknown_struct193': self.unknown_struct193.to_json(),
        }


def _decode_max_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9cbc24b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7e2ea16c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explosion_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xebefb1a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_alternate_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_launch_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_crash_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flight_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x05c67d0b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_launch_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_crash_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_orientation(data: typing.BinaryIO, property_size: int):
    return enums.Orientation.from_stream(data)


def _decode_unknown_0xa17c618d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x469f8fb8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_constant_rotation(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_struct193(data: typing.BinaryIO, property_size: int):
    return UnknownStruct193.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd4d4edfa: ('max_lifetime', _decode_max_lifetime),
    0x9cbc24b1: ('unknown_0x9cbc24b1', _decode_unknown_0x9cbc24b1),
    0x7e2ea16c: ('unknown_0x7e2ea16c', _decode_unknown_0x7e2ea16c),
    0xdeff74ea: ('explosion_damage', _decode_explosion_damage),
    0xebefb1a9: ('unknown_0xebefb1a9', _decode_unknown_0xebefb1a9),
    0xf0993bfe: ('use_alternate_damage_effect', _decode_use_alternate_damage_effect),
    0xa4692e9c: ('launch_effect', _decode_launch_effect),
    0xa06edaf9: ('crash_effect', _decode_crash_effect),
    0xde1565a9: ('flight_effect', _decode_flight_effect),
    0x5c67d0b: ('unknown_0x05c67d0b', _decode_unknown_0x05c67d0b),
    0xf7f7f6af: ('launch_sound', _decode_launch_sound),
    0x2b258629: ('crash_sound', _decode_crash_sound),
    0xe1e66b24: ('flight_sound', _decode_flight_sound),
    0xf4bf6637: ('orientation', _decode_orientation),
    0xa17c618d: ('unknown_0xa17c618d', _decode_unknown_0xa17c618d),
    0x469f8fb8: ('unknown_0x469f8fb8', _decode_unknown_0x469f8fb8),
    0xec0828ce: ('constant_rotation', _decode_constant_rotation),
    0x183dc71: ('unknown_struct193', _decode_unknown_struct193),
}
