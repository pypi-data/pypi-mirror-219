# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct40(BaseProperty):
    main: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    left: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    joint: str = dataclasses.field(default='')
    extend: Spline = dataclasses.field(default_factory=Spline)
    retract: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x2eb71b6b: float = dataclasses.field(default=4.0)
    unknown_0x25bd39c0: float = dataclasses.field(default=3.0)
    open_time: float = dataclasses.field(default=5.0)
    open_damage: float = dataclasses.field(default=100.0)
    look_around_time: float = dataclasses.field(default=1.5)
    unknown_0x193c048f: float = dataclasses.field(default=0.5)
    stunned_time: float = dataclasses.field(default=4.0)
    target_deploy_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    target_retract_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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

        data.write(b'\xc27ey')  # 0xc2376579
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.main))

        data.write(b'\x05\x03.\xd4')  # 0x5032ed4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left))

        data.write(b'g\x1d\xbf\xb5')  # 0x671dbfb5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right))

        data.write(b'\x82\x892\xc1')  # 0x828932c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.joint.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\xf1\x85\xfa')  # 0xbff185fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.extend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\x84fF')  # 0x1c846646
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.retract.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.\xb7\x1bk')  # 0x2eb71b6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2eb71b6b))

        data.write(b'%\xbd9\xc0')  # 0x25bd39c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x25bd39c0))

        data.write(b'\xfdT\xc3\x00')  # 0xfd54c300
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.open_time))

        data.write(b'~\xf9\xa7\x19')  # 0x7ef9a719
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.open_damage))

        data.write(b'%\x7f\xe2n')  # 0x257fe26e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_around_time))

        data.write(b'\x19<\x04\x8f')  # 0x193c048f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x193c048f))

        data.write(b'\x81\x05\xec\xfd')  # 0x8105ecfd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stunned_time))

        data.write(b'7_\x16c')  # 0x375f1663
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.target_deploy_sound))

        data.write(b'h\xa5\x1a\xbb')  # 0x68a51abb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.target_retract_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            main=data['main'],
            left=data['left'],
            right=data['right'],
            joint=data['joint'],
            extend=Spline.from_json(data['extend']),
            retract=Spline.from_json(data['retract']),
            unknown_0x2eb71b6b=data['unknown_0x2eb71b6b'],
            unknown_0x25bd39c0=data['unknown_0x25bd39c0'],
            open_time=data['open_time'],
            open_damage=data['open_damage'],
            look_around_time=data['look_around_time'],
            unknown_0x193c048f=data['unknown_0x193c048f'],
            stunned_time=data['stunned_time'],
            target_deploy_sound=data['target_deploy_sound'],
            target_retract_sound=data['target_retract_sound'],
        )

    def to_json(self) -> dict:
        return {
            'main': self.main,
            'left': self.left,
            'right': self.right,
            'joint': self.joint,
            'extend': self.extend.to_json(),
            'retract': self.retract.to_json(),
            'unknown_0x2eb71b6b': self.unknown_0x2eb71b6b,
            'unknown_0x25bd39c0': self.unknown_0x25bd39c0,
            'open_time': self.open_time,
            'open_damage': self.open_damage,
            'look_around_time': self.look_around_time,
            'unknown_0x193c048f': self.unknown_0x193c048f,
            'stunned_time': self.stunned_time,
            'target_deploy_sound': self.target_deploy_sound,
            'target_retract_sound': self.target_retract_sound,
        }


def _decode_main(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_joint(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_extend(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_retract(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x2eb71b6b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x25bd39c0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_open_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_open_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_around_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x193c048f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stunned_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_deploy_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_target_retract_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc2376579: ('main', _decode_main),
    0x5032ed4: ('left', _decode_left),
    0x671dbfb5: ('right', _decode_right),
    0x828932c1: ('joint', _decode_joint),
    0xbff185fa: ('extend', _decode_extend),
    0x1c846646: ('retract', _decode_retract),
    0x2eb71b6b: ('unknown_0x2eb71b6b', _decode_unknown_0x2eb71b6b),
    0x25bd39c0: ('unknown_0x25bd39c0', _decode_unknown_0x25bd39c0),
    0xfd54c300: ('open_time', _decode_open_time),
    0x7ef9a719: ('open_damage', _decode_open_damage),
    0x257fe26e: ('look_around_time', _decode_look_around_time),
    0x193c048f: ('unknown_0x193c048f', _decode_unknown_0x193c048f),
    0x8105ecfd: ('stunned_time', _decode_stunned_time),
    0x375f1663: ('target_deploy_sound', _decode_target_deploy_sound),
    0x68a51abb: ('target_retract_sound', _decode_target_retract_sound),
}
