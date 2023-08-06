# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.AimStuff import AimStuff
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Collision import Collision
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.DarkWorld import DarkWorld
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.FirstPersonCamera import FirstPersonCamera
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Frozen import Frozen
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Grapple import Grapple
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.GrappleBeam import GrappleBeam
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Misc import Misc
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Motion import Motion
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Orbit import Orbit
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.ScanVisor import ScanVisor
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.Shield import Shield
from retro_data_structures.properties.echoes.archetypes.TweakPlayer.SuitDamageReduction import SuitDamageReduction


@dataclasses.dataclass()
class TweakPlayer(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    dark_world: DarkWorld = dataclasses.field(default_factory=DarkWorld)
    grapple_beam: GrappleBeam = dataclasses.field(default_factory=GrappleBeam)
    motion: Motion = dataclasses.field(default_factory=Motion)
    misc: Misc = dataclasses.field(default_factory=Misc)
    aim_stuff: AimStuff = dataclasses.field(default_factory=AimStuff)
    orbit: Orbit = dataclasses.field(default_factory=Orbit)
    scan_visor: ScanVisor = dataclasses.field(default_factory=ScanVisor)
    grapple: Grapple = dataclasses.field(default_factory=Grapple)
    collision: Collision = dataclasses.field(default_factory=Collision)
    first_person_camera: FirstPersonCamera = dataclasses.field(default_factory=FirstPersonCamera)
    shield: Shield = dataclasses.field(default_factory=Shield)
    frozen: Frozen = dataclasses.field(default_factory=Frozen)
    suit_damage_reduction: SuitDamageReduction = dataclasses.field(default_factory=SuitDamageReduction)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWPL'

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\xd0\x8e\xba')  # 0xdfd08eba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_world.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'E\x17\x1a\x96')  # 0x45171a96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x82\xcfL\xf1')  # 0x82cf4cf1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\xa7 \xc8')  # 0x56a720c8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\xa1t8')  # 0x42a17438
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aim_stuff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$:\xe08')  # 0x243ae038
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orbit.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \x12L=')  # 0x20124c3d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0A$@')  # 0x30412440
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\xd3*\xe5')  # 0xc4d32ae5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.collision.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6\x15]K')  # 0xd6155d4b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.first_person_camera.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\xcav~')  # 0xbcca767e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'M; \xb7')  # 0x4d3b20b7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.frozen.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xae\xaf\xf2\x10')  # 0xaeaff210
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.suit_damage_reduction.to_stream(data)
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
            dark_world=DarkWorld.from_json(data['dark_world']),
            grapple_beam=GrappleBeam.from_json(data['grapple_beam']),
            motion=Motion.from_json(data['motion']),
            misc=Misc.from_json(data['misc']),
            aim_stuff=AimStuff.from_json(data['aim_stuff']),
            orbit=Orbit.from_json(data['orbit']),
            scan_visor=ScanVisor.from_json(data['scan_visor']),
            grapple=Grapple.from_json(data['grapple']),
            collision=Collision.from_json(data['collision']),
            first_person_camera=FirstPersonCamera.from_json(data['first_person_camera']),
            shield=Shield.from_json(data['shield']),
            frozen=Frozen.from_json(data['frozen']),
            suit_damage_reduction=SuitDamageReduction.from_json(data['suit_damage_reduction']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'dark_world': self.dark_world.to_json(),
            'grapple_beam': self.grapple_beam.to_json(),
            'motion': self.motion.to_json(),
            'misc': self.misc.to_json(),
            'aim_stuff': self.aim_stuff.to_json(),
            'orbit': self.orbit.to_json(),
            'scan_visor': self.scan_visor.to_json(),
            'grapple': self.grapple.to_json(),
            'collision': self.collision.to_json(),
            'first_person_camera': self.first_person_camera.to_json(),
            'shield': self.shield.to_json(),
            'frozen': self.frozen.to_json(),
            'suit_damage_reduction': self.suit_damage_reduction.to_json(),
        }

    def _dependencies_for_dark_world(self, asset_manager):
        yield from self.dark_world.dependencies_for(asset_manager)

    def _dependencies_for_grapple_beam(self, asset_manager):
        yield from self.grapple_beam.dependencies_for(asset_manager)

    def _dependencies_for_motion(self, asset_manager):
        yield from self.motion.dependencies_for(asset_manager)

    def _dependencies_for_misc(self, asset_manager):
        yield from self.misc.dependencies_for(asset_manager)

    def _dependencies_for_aim_stuff(self, asset_manager):
        yield from self.aim_stuff.dependencies_for(asset_manager)

    def _dependencies_for_orbit(self, asset_manager):
        yield from self.orbit.dependencies_for(asset_manager)

    def _dependencies_for_scan_visor(self, asset_manager):
        yield from self.scan_visor.dependencies_for(asset_manager)

    def _dependencies_for_grapple(self, asset_manager):
        yield from self.grapple.dependencies_for(asset_manager)

    def _dependencies_for_collision(self, asset_manager):
        yield from self.collision.dependencies_for(asset_manager)

    def _dependencies_for_first_person_camera(self, asset_manager):
        yield from self.first_person_camera.dependencies_for(asset_manager)

    def _dependencies_for_shield(self, asset_manager):
        yield from self.shield.dependencies_for(asset_manager)

    def _dependencies_for_frozen(self, asset_manager):
        yield from self.frozen.dependencies_for(asset_manager)

    def _dependencies_for_suit_damage_reduction(self, asset_manager):
        yield from self.suit_damage_reduction.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_dark_world, "dark_world", "DarkWorld"),
            (self._dependencies_for_grapple_beam, "grapple_beam", "GrappleBeam"),
            (self._dependencies_for_motion, "motion", "Motion"),
            (self._dependencies_for_misc, "misc", "Misc"),
            (self._dependencies_for_aim_stuff, "aim_stuff", "AimStuff"),
            (self._dependencies_for_orbit, "orbit", "Orbit"),
            (self._dependencies_for_scan_visor, "scan_visor", "ScanVisor"),
            (self._dependencies_for_grapple, "grapple", "Grapple"),
            (self._dependencies_for_collision, "collision", "Collision"),
            (self._dependencies_for_first_person_camera, "first_person_camera", "FirstPersonCamera"),
            (self._dependencies_for_shield, "shield", "Shield"),
            (self._dependencies_for_frozen, "frozen", "Frozen"),
            (self._dependencies_for_suit_damage_reduction, "suit_damage_reduction", "SuitDamageReduction"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakPlayer.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_dark_world(data: typing.BinaryIO, property_size: int):
    return DarkWorld.from_stream(data, property_size)


def _decode_grapple_beam(data: typing.BinaryIO, property_size: int):
    return GrappleBeam.from_stream(data, property_size)


def _decode_motion(data: typing.BinaryIO, property_size: int):
    return Motion.from_stream(data, property_size)


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_aim_stuff(data: typing.BinaryIO, property_size: int):
    return AimStuff.from_stream(data, property_size)


def _decode_orbit(data: typing.BinaryIO, property_size: int):
    return Orbit.from_stream(data, property_size)


def _decode_scan_visor(data: typing.BinaryIO, property_size: int):
    return ScanVisor.from_stream(data, property_size)


def _decode_grapple(data: typing.BinaryIO, property_size: int):
    return Grapple.from_stream(data, property_size)


def _decode_collision(data: typing.BinaryIO, property_size: int):
    return Collision.from_stream(data, property_size)


def _decode_first_person_camera(data: typing.BinaryIO, property_size: int):
    return FirstPersonCamera.from_stream(data, property_size)


def _decode_shield(data: typing.BinaryIO, property_size: int):
    return Shield.from_stream(data, property_size)


def _decode_frozen(data: typing.BinaryIO, property_size: int):
    return Frozen.from_stream(data, property_size)


def _decode_suit_damage_reduction(data: typing.BinaryIO, property_size: int):
    return SuitDamageReduction.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0xdfd08eba: ('dark_world', _decode_dark_world),
    0x45171a96: ('grapple_beam', _decode_grapple_beam),
    0x82cf4cf1: ('motion', _decode_motion),
    0x56a720c8: ('misc', _decode_misc),
    0x42a17438: ('aim_stuff', _decode_aim_stuff),
    0x243ae038: ('orbit', _decode_orbit),
    0x20124c3d: ('scan_visor', _decode_scan_visor),
    0x30412440: ('grapple', _decode_grapple),
    0xc4d32ae5: ('collision', _decode_collision),
    0xd6155d4b: ('first_person_camera', _decode_first_person_camera),
    0xbcca767e: ('shield', _decode_shield),
    0x4d3b20b7: ('frozen', _decode_frozen),
    0xaeaff210: ('suit_damage_reduction', _decode_suit_damage_reduction),
}
