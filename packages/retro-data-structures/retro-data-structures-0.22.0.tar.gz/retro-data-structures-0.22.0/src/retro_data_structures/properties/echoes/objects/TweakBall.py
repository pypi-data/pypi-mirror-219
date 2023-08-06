# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TweakBall.BoostBall import BoostBall
from retro_data_structures.properties.echoes.archetypes.TweakBall.Camera import Camera
from retro_data_structures.properties.echoes.archetypes.TweakBall.CannonBall import CannonBall
from retro_data_structures.properties.echoes.archetypes.TweakBall.DeathBall import DeathBall
from retro_data_structures.properties.echoes.archetypes.TweakBall.Misc import Misc
from retro_data_structures.properties.echoes.archetypes.TweakBall.Movement import Movement
from retro_data_structures.properties.echoes.archetypes.TweakBall.ScrewAttack import ScrewAttack


@dataclasses.dataclass()
class TweakBall(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    movement: Movement = dataclasses.field(default_factory=Movement)
    camera: Camera = dataclasses.field(default_factory=Camera)
    misc: Misc = dataclasses.field(default_factory=Misc)
    boost_ball: BoostBall = dataclasses.field(default_factory=BoostBall)
    cannon_ball: CannonBall = dataclasses.field(default_factory=CannonBall)
    screw_attack: ScrewAttack = dataclasses.field(default_factory=ScrewAttack)
    death_ball: DeathBall = dataclasses.field(default_factory=DeathBall)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWBL'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\r\xef\x1f\xfb')  # 0xdef1ffb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.movement.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z\xac\t\xb9')  # 0x7aac09b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0cg\xb70')  # 0xc67b730
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcbN\xa3\xbf')  # 0xcb4ea3bf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boost_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\xb9\xe8\x08')  # 0x5fb9e808
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cannon_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'K\x1c{}')  # 0x4b1c7b7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.screw_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb_\xc8\xa4')  # 0xbb5fc8a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.death_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            instance_name=data['instance_name'],
            movement=Movement.from_json(data['movement']),
            camera=Camera.from_json(data['camera']),
            misc=Misc.from_json(data['misc']),
            boost_ball=BoostBall.from_json(data['boost_ball']),
            cannon_ball=CannonBall.from_json(data['cannon_ball']),
            screw_attack=ScrewAttack.from_json(data['screw_attack']),
            death_ball=DeathBall.from_json(data['death_ball']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'movement': self.movement.to_json(),
            'camera': self.camera.to_json(),
            'misc': self.misc.to_json(),
            'boost_ball': self.boost_ball.to_json(),
            'cannon_ball': self.cannon_ball.to_json(),
            'screw_attack': self.screw_attack.to_json(),
            'death_ball': self.death_ball.to_json(),
        }

    def _dependencies_for_movement(self, asset_manager):
        yield from self.movement.dependencies_for(asset_manager)

    def _dependencies_for_camera(self, asset_manager):
        yield from self.camera.dependencies_for(asset_manager)

    def _dependencies_for_misc(self, asset_manager):
        yield from self.misc.dependencies_for(asset_manager)

    def _dependencies_for_boost_ball(self, asset_manager):
        yield from self.boost_ball.dependencies_for(asset_manager)

    def _dependencies_for_cannon_ball(self, asset_manager):
        yield from self.cannon_ball.dependencies_for(asset_manager)

    def _dependencies_for_screw_attack(self, asset_manager):
        yield from self.screw_attack.dependencies_for(asset_manager)

    def _dependencies_for_death_ball(self, asset_manager):
        yield from self.death_ball.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_movement, "movement", "Movement"),
            (self._dependencies_for_camera, "camera", "Camera"),
            (self._dependencies_for_misc, "misc", "Misc"),
            (self._dependencies_for_boost_ball, "boost_ball", "BoostBall"),
            (self._dependencies_for_cannon_ball, "cannon_ball", "CannonBall"),
            (self._dependencies_for_screw_attack, "screw_attack", "ScrewAttack"),
            (self._dependencies_for_death_ball, "death_ball", "DeathBall"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakBall.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_movement(data: typing.BinaryIO, property_size: int):
    return Movement.from_stream(data, property_size)


def _decode_camera(data: typing.BinaryIO, property_size: int):
    return Camera.from_stream(data, property_size)


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_boost_ball(data: typing.BinaryIO, property_size: int):
    return BoostBall.from_stream(data, property_size)


def _decode_cannon_ball(data: typing.BinaryIO, property_size: int):
    return CannonBall.from_stream(data, property_size)


def _decode_screw_attack(data: typing.BinaryIO, property_size: int):
    return ScrewAttack.from_stream(data, property_size)


def _decode_death_ball(data: typing.BinaryIO, property_size: int):
    return DeathBall.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0xdef1ffb: ('movement', _decode_movement),
    0x7aac09b9: ('camera', _decode_camera),
    0xc67b730: ('misc', _decode_misc),
    0xcb4ea3bf: ('boost_ball', _decode_boost_ball),
    0x5fb9e808: ('cannon_ball', _decode_cannon_ball),
    0x4b1c7b7d: ('screw_attack', _decode_screw_attack),
    0xbb5fc8a4: ('death_ball', _decode_death_ball),
}
