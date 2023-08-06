# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.CameraShakerData import CameraShakerData
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.Arm.Position import Position
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.Beam.Misc import Misc
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.Holstering import Holstering
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.Misc import Misc
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.Position import Position
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.RicochetDamage.Factor import Factor
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.UnknownStruct1 import UnknownStruct1
from retro_data_structures.properties.echoes.archetypes.TweakPlayerGun.Weapons import Weapons


@dataclasses.dataclass()
class TweakPlayerGun(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    misc: Misc = dataclasses.field(default_factory=Misc)
    holstering: Holstering = dataclasses.field(default_factory=Holstering)
    position: Position = dataclasses.field(default_factory=Position)
    arm_position: Position = dataclasses.field(default_factory=Position)
    weapons: Weapons = dataclasses.field(default_factory=Weapons)
    combos: UnknownStruct1 = dataclasses.field(default_factory=UnknownStruct1)
    beam_misc: Misc = dataclasses.field(default_factory=Misc)
    ricochet_damage_factor: Factor = dataclasses.field(default_factory=Factor)
    recoil: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)
    combo_recoil: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)
    projectile_recoil: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)
    flame_thrower: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)
    wave_buster: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)
    projectile_impact: CameraShakerData = dataclasses.field(default_factory=CameraShakerData)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWPM'

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8.\xd4$')  # 0xb82ed424
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'kk\xdcG')  # 0x6b6bdc47
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.holstering.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x87\x88,\xb0')  # 0x87882cb0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.position.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%P\x07\xad')  # 0x255007ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.arm_position.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83\xd7X\xab')  # 0x83d758ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapons.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\x8c\x87u')  # 0x888c8775
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.combos.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\xeb\xb7>')  # 0xaaebb73e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\xa0X\xfe')  # 0x8da058fe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ricochet_damage_factor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xff\xdbK\xb7')  # 0xffdb4bb7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.recoil.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93z5\xbd')  # 0x937a35bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.combo_recoil.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&\x19g8')  # 0x26196738
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_recoil.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\x08\x08\xc9')  # 0xf40808c9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flame_thrower.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9amz1')  # 0x9a6d7a31
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.wave_buster.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\xf1LZ')  # 0x12f14c5a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_impact.to_stream(data, default_override={'flags_camera_shaker': 19})
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
            misc=Misc.from_json(data['misc']),
            holstering=Holstering.from_json(data['holstering']),
            position=Position.from_json(data['position']),
            arm_position=Position.from_json(data['arm_position']),
            weapons=Weapons.from_json(data['weapons']),
            combos=UnknownStruct1.from_json(data['combos']),
            beam_misc=Misc.from_json(data['beam_misc']),
            ricochet_damage_factor=Factor.from_json(data['ricochet_damage_factor']),
            recoil=CameraShakerData.from_json(data['recoil']),
            combo_recoil=CameraShakerData.from_json(data['combo_recoil']),
            projectile_recoil=CameraShakerData.from_json(data['projectile_recoil']),
            flame_thrower=CameraShakerData.from_json(data['flame_thrower']),
            wave_buster=CameraShakerData.from_json(data['wave_buster']),
            projectile_impact=CameraShakerData.from_json(data['projectile_impact']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'misc': self.misc.to_json(),
            'holstering': self.holstering.to_json(),
            'position': self.position.to_json(),
            'arm_position': self.arm_position.to_json(),
            'weapons': self.weapons.to_json(),
            'combos': self.combos.to_json(),
            'beam_misc': self.beam_misc.to_json(),
            'ricochet_damage_factor': self.ricochet_damage_factor.to_json(),
            'recoil': self.recoil.to_json(),
            'combo_recoil': self.combo_recoil.to_json(),
            'projectile_recoil': self.projectile_recoil.to_json(),
            'flame_thrower': self.flame_thrower.to_json(),
            'wave_buster': self.wave_buster.to_json(),
            'projectile_impact': self.projectile_impact.to_json(),
        }

    def _dependencies_for_misc(self, asset_manager):
        yield from self.misc.dependencies_for(asset_manager)

    def _dependencies_for_holstering(self, asset_manager):
        yield from self.holstering.dependencies_for(asset_manager)

    def _dependencies_for_position(self, asset_manager):
        yield from self.position.dependencies_for(asset_manager)

    def _dependencies_for_arm_position(self, asset_manager):
        yield from self.arm_position.dependencies_for(asset_manager)

    def _dependencies_for_weapons(self, asset_manager):
        yield from self.weapons.dependencies_for(asset_manager)

    def _dependencies_for_combos(self, asset_manager):
        yield from self.combos.dependencies_for(asset_manager)

    def _dependencies_for_beam_misc(self, asset_manager):
        yield from self.beam_misc.dependencies_for(asset_manager)

    def _dependencies_for_ricochet_damage_factor(self, asset_manager):
        yield from self.ricochet_damage_factor.dependencies_for(asset_manager)

    def _dependencies_for_recoil(self, asset_manager):
        yield from self.recoil.dependencies_for(asset_manager)

    def _dependencies_for_combo_recoil(self, asset_manager):
        yield from self.combo_recoil.dependencies_for(asset_manager)

    def _dependencies_for_projectile_recoil(self, asset_manager):
        yield from self.projectile_recoil.dependencies_for(asset_manager)

    def _dependencies_for_flame_thrower(self, asset_manager):
        yield from self.flame_thrower.dependencies_for(asset_manager)

    def _dependencies_for_wave_buster(self, asset_manager):
        yield from self.wave_buster.dependencies_for(asset_manager)

    def _dependencies_for_projectile_impact(self, asset_manager):
        yield from self.projectile_impact.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_misc, "misc", "Misc"),
            (self._dependencies_for_holstering, "holstering", "Holstering"),
            (self._dependencies_for_position, "position", "Position"),
            (self._dependencies_for_arm_position, "arm_position", "Position"),
            (self._dependencies_for_weapons, "weapons", "Weapons"),
            (self._dependencies_for_combos, "combos", "UnknownStruct1"),
            (self._dependencies_for_beam_misc, "beam_misc", "Misc"),
            (self._dependencies_for_ricochet_damage_factor, "ricochet_damage_factor", "Factor"),
            (self._dependencies_for_recoil, "recoil", "CameraShakerData"),
            (self._dependencies_for_combo_recoil, "combo_recoil", "CameraShakerData"),
            (self._dependencies_for_projectile_recoil, "projectile_recoil", "CameraShakerData"),
            (self._dependencies_for_flame_thrower, "flame_thrower", "CameraShakerData"),
            (self._dependencies_for_wave_buster, "wave_buster", "CameraShakerData"),
            (self._dependencies_for_projectile_impact, "projectile_impact", "CameraShakerData"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakPlayerGun.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_holstering(data: typing.BinaryIO, property_size: int):
    return Holstering.from_stream(data, property_size)


def _decode_position(data: typing.BinaryIO, property_size: int):
    return Position.from_stream(data, property_size)


def _decode_arm_position(data: typing.BinaryIO, property_size: int):
    return Position.from_stream(data, property_size)


def _decode_weapons(data: typing.BinaryIO, property_size: int):
    return Weapons.from_stream(data, property_size)


def _decode_combos(data: typing.BinaryIO, property_size: int):
    return UnknownStruct1.from_stream(data, property_size)


def _decode_beam_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_ricochet_damage_factor(data: typing.BinaryIO, property_size: int):
    return Factor.from_stream(data, property_size)


def _decode_recoil(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


def _decode_combo_recoil(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


def _decode_projectile_recoil(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


def _decode_flame_thrower(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


def _decode_wave_buster(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size)


def _decode_projectile_impact(data: typing.BinaryIO, property_size: int):
    return CameraShakerData.from_stream(data, property_size, default_override={'flags_camera_shaker': 19})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0xb82ed424: ('misc', _decode_misc),
    0x6b6bdc47: ('holstering', _decode_holstering),
    0x87882cb0: ('position', _decode_position),
    0x255007ad: ('arm_position', _decode_arm_position),
    0x83d758ab: ('weapons', _decode_weapons),
    0x888c8775: ('combos', _decode_combos),
    0xaaebb73e: ('beam_misc', _decode_beam_misc),
    0x8da058fe: ('ricochet_damage_factor', _decode_ricochet_damage_factor),
    0xffdb4bb7: ('recoil', _decode_recoil),
    0x937a35bd: ('combo_recoil', _decode_combo_recoil),
    0x26196738: ('projectile_recoil', _decode_projectile_recoil),
    0xf40808c9: ('flame_thrower', _decode_flame_thrower),
    0x9a6d7a31: ('wave_buster', _decode_wave_buster),
    0x12f14c5a: ('projectile_impact', _decode_projectile_impact),
}
