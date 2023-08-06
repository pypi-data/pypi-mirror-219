# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.GrappleData import GrappleData
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData


@dataclasses.dataclass()
class ShellBugData(BaseProperty):
    launch_projectile_data: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    unknown_0xa023555c: float = dataclasses.field(default=0.0)
    unknown_0x4643fabd: float = dataclasses.field(default=0.0)
    ball_range: float = dataclasses.field(default=0.0)
    ball_radius: float = dataclasses.field(default=0.0)
    look_ahead_time: float = dataclasses.field(default=0.0)
    unknown_0x34bbc7a5: bool = dataclasses.field(default=False)
    unknown_0xe5839374: float = dataclasses.field(default=0.0)
    unknown_0x03e33c95: float = dataclasses.field(default=0.0)
    weak_spot_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0x84e71870: bool = dataclasses.field(default=True)
    unknown_0x76264db1: bool = dataclasses.field(default=False)
    grapple_data: GrappleData = dataclasses.field(default_factory=GrappleData)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xab\xa9\xa5m')  # 0xaba9a56d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0#U\\')  # 0xa023555c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa023555c))

        data.write(b'FC\xfa\xbd')  # 0x4643fabd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4643fabd))

        data.write(b'\x00W\xa7\xd8')  # 0x57a7d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_range))

        data.write(b'\x0e/S\x7f')  # 0xe2f537f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_radius))

        data.write(b'\x8c\xb2\x0cS')  # 0x8cb20c53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_ahead_time))

        data.write(b'4\xbb\xc7\xa5')  # 0x34bbc7a5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x34bbc7a5))

        data.write(b'\xe5\x83\x93t')  # 0xe5839374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe5839374))

        data.write(b'\x03\xe3<\x95')  # 0x3e33c95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x03e33c95))

        data.write(b'\x95\x03\x18\xf0')  # 0x950318f0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weak_spot_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84\xe7\x18p')  # 0x84e71870
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x84e71870))

        data.write(b'v&M\xb1')  # 0x76264db1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x76264db1))

        data.write(b'\xf6\t\xc67')  # 0xf609c637
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            launch_projectile_data=LaunchProjectileData.from_json(data['launch_projectile_data']),
            unknown_0xa023555c=data['unknown_0xa023555c'],
            unknown_0x4643fabd=data['unknown_0x4643fabd'],
            ball_range=data['ball_range'],
            ball_radius=data['ball_radius'],
            look_ahead_time=data['look_ahead_time'],
            unknown_0x34bbc7a5=data['unknown_0x34bbc7a5'],
            unknown_0xe5839374=data['unknown_0xe5839374'],
            unknown_0x03e33c95=data['unknown_0x03e33c95'],
            weak_spot_vulnerability=DamageVulnerability.from_json(data['weak_spot_vulnerability']),
            unknown_0x84e71870=data['unknown_0x84e71870'],
            unknown_0x76264db1=data['unknown_0x76264db1'],
            grapple_data=GrappleData.from_json(data['grapple_data']),
        )

    def to_json(self) -> dict:
        return {
            'launch_projectile_data': self.launch_projectile_data.to_json(),
            'unknown_0xa023555c': self.unknown_0xa023555c,
            'unknown_0x4643fabd': self.unknown_0x4643fabd,
            'ball_range': self.ball_range,
            'ball_radius': self.ball_radius,
            'look_ahead_time': self.look_ahead_time,
            'unknown_0x34bbc7a5': self.unknown_0x34bbc7a5,
            'unknown_0xe5839374': self.unknown_0xe5839374,
            'unknown_0x03e33c95': self.unknown_0x03e33c95,
            'weak_spot_vulnerability': self.weak_spot_vulnerability.to_json(),
            'unknown_0x84e71870': self.unknown_0x84e71870,
            'unknown_0x76264db1': self.unknown_0x76264db1,
            'grapple_data': self.grapple_data.to_json(),
        }


def _decode_launch_projectile_data(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_unknown_0xa023555c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4643fabd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_ahead_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x34bbc7a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe5839374(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x03e33c95(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_weak_spot_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0x84e71870(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x76264db1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_data(data: typing.BinaryIO, property_size: int):
    return GrappleData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaba9a56d: ('launch_projectile_data', _decode_launch_projectile_data),
    0xa023555c: ('unknown_0xa023555c', _decode_unknown_0xa023555c),
    0x4643fabd: ('unknown_0x4643fabd', _decode_unknown_0x4643fabd),
    0x57a7d8: ('ball_range', _decode_ball_range),
    0xe2f537f: ('ball_radius', _decode_ball_radius),
    0x8cb20c53: ('look_ahead_time', _decode_look_ahead_time),
    0x34bbc7a5: ('unknown_0x34bbc7a5', _decode_unknown_0x34bbc7a5),
    0xe5839374: ('unknown_0xe5839374', _decode_unknown_0xe5839374),
    0x3e33c95: ('unknown_0x03e33c95', _decode_unknown_0x03e33c95),
    0x950318f0: ('weak_spot_vulnerability', _decode_weak_spot_vulnerability),
    0x84e71870: ('unknown_0x84e71870', _decode_unknown_0x84e71870),
    0x76264db1: ('unknown_0x76264db1', _decode_unknown_0x76264db1),
    0xf609c637: ('grapple_data', _decode_grapple_data),
}
