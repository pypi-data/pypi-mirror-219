# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.BallMiscControls import BallMiscControls
from retro_data_structures.properties.corruption.archetypes.BallMovementControls import BallMovementControls
from retro_data_structures.properties.corruption.archetypes.CameraControls import CameraControls
from retro_data_structures.properties.corruption.archetypes.DebugControls import DebugControls
from retro_data_structures.properties.corruption.archetypes.MiscControls import MiscControls
from retro_data_structures.properties.corruption.archetypes.PlayerMiscControls import PlayerMiscControls
from retro_data_structures.properties.corruption.archetypes.PlayerMovementControls import PlayerMovementControls
from retro_data_structures.properties.corruption.archetypes.PlayerWeaponControls import PlayerWeaponControls


@dataclasses.dataclass()
class PlayerControls(BaseProperty):
    unknown_0x4cf2b66e: PlayerMovementControls = dataclasses.field(default_factory=PlayerMovementControls)
    unknown_0x478b6c20: PlayerWeaponControls = dataclasses.field(default_factory=PlayerWeaponControls)
    unknown_0x49bd3f51: PlayerMiscControls = dataclasses.field(default_factory=PlayerMiscControls)
    unknown_0x61fe67a1: int = dataclasses.field(default=61)
    ball_movement: BallMovementControls = dataclasses.field(default_factory=BallMovementControls)
    ball_misc: BallMiscControls = dataclasses.field(default_factory=BallMiscControls)
    unknown_0xd1777bf7: int = dataclasses.field(default=0)
    camera: CameraControls = dataclasses.field(default_factory=CameraControls)
    misc: MiscControls = dataclasses.field(default_factory=MiscControls)
    debug: DebugControls = dataclasses.field(default_factory=DebugControls)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'L\xf2\xb6n')  # 0x4cf2b66e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x4cf2b66e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\x8bl ')  # 0x478b6c20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x478b6c20.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'I\xbd?Q')  # 0x49bd3f51
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x49bd3f51.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\xfeg\xa1')  # 0x61fe67a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x61fe67a1))

        data.write(b'\x16\x81\xd3\xe9')  # 0x1681d3e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_movement.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02e\xe5i')  # 0x265e569
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1w{\xf7')  # 0xd1777bf7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd1777bf7))

        data.write(b'@\xe3P\xad')  # 0x40e350ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbew\xde\xd2')  # 0xbe77ded2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\x06\x99\x11')  # 0x47069911
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.debug.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x4cf2b66e=PlayerMovementControls.from_json(data['unknown_0x4cf2b66e']),
            unknown_0x478b6c20=PlayerWeaponControls.from_json(data['unknown_0x478b6c20']),
            unknown_0x49bd3f51=PlayerMiscControls.from_json(data['unknown_0x49bd3f51']),
            unknown_0x61fe67a1=data['unknown_0x61fe67a1'],
            ball_movement=BallMovementControls.from_json(data['ball_movement']),
            ball_misc=BallMiscControls.from_json(data['ball_misc']),
            unknown_0xd1777bf7=data['unknown_0xd1777bf7'],
            camera=CameraControls.from_json(data['camera']),
            misc=MiscControls.from_json(data['misc']),
            debug=DebugControls.from_json(data['debug']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x4cf2b66e': self.unknown_0x4cf2b66e.to_json(),
            'unknown_0x478b6c20': self.unknown_0x478b6c20.to_json(),
            'unknown_0x49bd3f51': self.unknown_0x49bd3f51.to_json(),
            'unknown_0x61fe67a1': self.unknown_0x61fe67a1,
            'ball_movement': self.ball_movement.to_json(),
            'ball_misc': self.ball_misc.to_json(),
            'unknown_0xd1777bf7': self.unknown_0xd1777bf7,
            'camera': self.camera.to_json(),
            'misc': self.misc.to_json(),
            'debug': self.debug.to_json(),
        }


def _decode_unknown_0x4cf2b66e(data: typing.BinaryIO, property_size: int):
    return PlayerMovementControls.from_stream(data, property_size)


def _decode_unknown_0x478b6c20(data: typing.BinaryIO, property_size: int):
    return PlayerWeaponControls.from_stream(data, property_size)


def _decode_unknown_0x49bd3f51(data: typing.BinaryIO, property_size: int):
    return PlayerMiscControls.from_stream(data, property_size)


def _decode_unknown_0x61fe67a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ball_movement(data: typing.BinaryIO, property_size: int):
    return BallMovementControls.from_stream(data, property_size)


def _decode_ball_misc(data: typing.BinaryIO, property_size: int):
    return BallMiscControls.from_stream(data, property_size)


def _decode_unknown_0xd1777bf7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_camera(data: typing.BinaryIO, property_size: int):
    return CameraControls.from_stream(data, property_size)


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return MiscControls.from_stream(data, property_size)


def _decode_debug(data: typing.BinaryIO, property_size: int):
    return DebugControls.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4cf2b66e: ('unknown_0x4cf2b66e', _decode_unknown_0x4cf2b66e),
    0x478b6c20: ('unknown_0x478b6c20', _decode_unknown_0x478b6c20),
    0x49bd3f51: ('unknown_0x49bd3f51', _decode_unknown_0x49bd3f51),
    0x61fe67a1: ('unknown_0x61fe67a1', _decode_unknown_0x61fe67a1),
    0x1681d3e9: ('ball_movement', _decode_ball_movement),
    0x265e569: ('ball_misc', _decode_ball_misc),
    0xd1777bf7: ('unknown_0xd1777bf7', _decode_unknown_0xd1777bf7),
    0x40e350ad: ('camera', _decode_camera),
    0xbe77ded2: ('misc', _decode_misc),
    0x47069911: ('debug', _decode_debug),
}
