# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.ElectricBeamInfo import ElectricBeamInfo
from retro_data_structures.properties.corruption.archetypes.FlyerMovementMode import FlyerMovementMode
from retro_data_structures.properties.corruption.archetypes.GrappleData import GrappleData
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.ModIncaData import ModIncaData
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class GragnolFlyerData(BaseProperty):
    shooter: bool = dataclasses.field(default=False)
    projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    missile_deflection_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    missile_deflection_radius: float = dataclasses.field(default=20.0)
    missile_deflection_rate: float = dataclasses.field(default=120.0)
    beam_weapon_info: ElectricBeamInfo = dataclasses.field(default_factory=ElectricBeamInfo)
    deflection_particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    beam_deflection_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xf10ee8e2: float = dataclasses.field(default=-1.0)
    unknown_0x7171bfc2: float = dataclasses.field(default=5.0)
    electric_beam_info: ElectricBeamInfo = dataclasses.field(default_factory=ElectricBeamInfo)
    patrol: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    attack_path: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    attack: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    grapple_pull_distance: float = dataclasses.field(default=5.0)
    min_idle_delay: float = dataclasses.field(default=2.0)
    max_idle_delay: float = dataclasses.field(default=10.0)
    recheck_path_time: float = dataclasses.field(default=1.0)
    recheck_path_distance: float = dataclasses.field(default=5.0)
    unknown_0xdff6c19b: bool = dataclasses.field(default=False)
    unknown_0xf7381a24: bool = dataclasses.field(default=True)
    unknown_0xb2c2928e: float = dataclasses.field(default=5.0)
    grapple_data: GrappleData = dataclasses.field(default_factory=GrappleData)
    mod_inca_data: ModIncaData = dataclasses.field(default_factory=ModIncaData)

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
        num_properties_offset = data.tell()
        data.write(b'\x00\x10')  # 16 properties
        num_properties_written = 16

        data.write(b'\x8a\xcc} ')  # 0x8acc7d20
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.shooter))

        if self.projectile != default_override.get('projectile', LaunchProjectileData()):
            num_properties_written += 1
            data.write(b',\x83\xc0\x12')  # 0x2c83c012
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.projectile.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        data.write(b'z\xb4\xab\x98')  # 0x7ab4ab98
        data.write(b'\x00\x0c')  # size
        self.missile_deflection_offset.to_stream(data)

        if self.missile_deflection_radius != default_override.get('missile_deflection_radius', 20.0):
            num_properties_written += 1
            data.write(b'\x88\xfa*\xcf')  # 0x88fa2acf
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.missile_deflection_radius))

        if self.missile_deflection_rate != default_override.get('missile_deflection_rate', 120.0):
            num_properties_written += 1
            data.write(b'\x1d\x15\x982')  # 0x1d159832
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.missile_deflection_rate))

        if self.beam_weapon_info != default_override.get('beam_weapon_info', ElectricBeamInfo()):
            num_properties_written += 1
            data.write(b'\x05\x01Wu')  # 0x5015775
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.beam_weapon_info.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.deflection_particle != default_override.get('deflection_particle', default_asset_id):
            num_properties_written += 1
            data.write(b'\x8f\x1d\xed\x1b')  # 0x8f1ded1b
            data.write(b'\x00\x08')  # size
            data.write(struct.pack(">Q", self.deflection_particle))

        if self.beam_deflection_sound != default_override.get('beam_deflection_sound', default_asset_id):
            num_properties_written += 1
            data.write(b'\x0b3\x9f\xac')  # 0xb339fac
            data.write(b'\x00\x08')  # size
            data.write(struct.pack(">Q", self.beam_deflection_sound))

        data.write(b'\xf1\x0e\xe8\xe2')  # 0xf10ee8e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf10ee8e2))

        data.write(b'qq\xbf\xc2')  # 0x7171bfc2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7171bfc2))

        if self.electric_beam_info != default_override.get('electric_beam_info', ElectricBeamInfo()):
            num_properties_written += 1
            data.write(b'$&X9')  # 0x24265839
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.electric_beam_info.to_stream(data, default_override={'length': 50.0})
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        data.write(b'\xcc\xdd:\xca')  # 0xccdd3aca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patrol.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8E\xd3\xc0')  # 0xc845d3c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_path.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa*\x17?')  # 0xfa2a173f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7L\xf5\x83')  # 0xe74cf583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_distance))

        data.write(b'\x17k\xd1\xf4')  # 0x176bd1f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_idle_delay))

        data.write(b'\x02\xe0\x05\x06')  # 0x2e00506
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_idle_delay))

        data.write(b'\x9a\xa9\x0bk')  # 0x9aa90b6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_time))

        data.write(b'v&\xec\x89')  # 0x7626ec89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_distance))

        data.write(b'\xdf\xf6\xc1\x9b')  # 0xdff6c19b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdff6c19b))

        data.write(b'\xf78\x1a$')  # 0xf7381a24
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf7381a24))

        data.write(b'\xb2\xc2\x92\x8e')  # 0xb2c2928e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb2c2928e))

        if self.grapple_data != default_override.get('grapple_data', GrappleData()):
            num_properties_written += 1
            data.write(b'\xf6\t\xc67')  # 0xf609c637
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.grapple_data.to_stream(data, default_override={'grapple_type': 1})
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        data.write(b'\xb4\xc0(T')  # 0xb4c02854
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mod_inca_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if num_properties_written != 16:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack(">H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            shooter=data['shooter'],
            projectile=LaunchProjectileData.from_json(data['projectile']),
            missile_deflection_offset=Vector.from_json(data['missile_deflection_offset']),
            missile_deflection_radius=data['missile_deflection_radius'],
            missile_deflection_rate=data['missile_deflection_rate'],
            beam_weapon_info=ElectricBeamInfo.from_json(data['beam_weapon_info']),
            deflection_particle=data['deflection_particle'],
            beam_deflection_sound=data['beam_deflection_sound'],
            unknown_0xf10ee8e2=data['unknown_0xf10ee8e2'],
            unknown_0x7171bfc2=data['unknown_0x7171bfc2'],
            electric_beam_info=ElectricBeamInfo.from_json(data['electric_beam_info']),
            patrol=FlyerMovementMode.from_json(data['patrol']),
            attack_path=FlyerMovementMode.from_json(data['attack_path']),
            attack=FlyerMovementMode.from_json(data['attack']),
            grapple_pull_distance=data['grapple_pull_distance'],
            min_idle_delay=data['min_idle_delay'],
            max_idle_delay=data['max_idle_delay'],
            recheck_path_time=data['recheck_path_time'],
            recheck_path_distance=data['recheck_path_distance'],
            unknown_0xdff6c19b=data['unknown_0xdff6c19b'],
            unknown_0xf7381a24=data['unknown_0xf7381a24'],
            unknown_0xb2c2928e=data['unknown_0xb2c2928e'],
            grapple_data=GrappleData.from_json(data['grapple_data']),
            mod_inca_data=ModIncaData.from_json(data['mod_inca_data']),
        )

    def to_json(self) -> dict:
        return {
            'shooter': self.shooter,
            'projectile': self.projectile.to_json(),
            'missile_deflection_offset': self.missile_deflection_offset.to_json(),
            'missile_deflection_radius': self.missile_deflection_radius,
            'missile_deflection_rate': self.missile_deflection_rate,
            'beam_weapon_info': self.beam_weapon_info.to_json(),
            'deflection_particle': self.deflection_particle,
            'beam_deflection_sound': self.beam_deflection_sound,
            'unknown_0xf10ee8e2': self.unknown_0xf10ee8e2,
            'unknown_0x7171bfc2': self.unknown_0x7171bfc2,
            'electric_beam_info': self.electric_beam_info.to_json(),
            'patrol': self.patrol.to_json(),
            'attack_path': self.attack_path.to_json(),
            'attack': self.attack.to_json(),
            'grapple_pull_distance': self.grapple_pull_distance,
            'min_idle_delay': self.min_idle_delay,
            'max_idle_delay': self.max_idle_delay,
            'recheck_path_time': self.recheck_path_time,
            'recheck_path_distance': self.recheck_path_distance,
            'unknown_0xdff6c19b': self.unknown_0xdff6c19b,
            'unknown_0xf7381a24': self.unknown_0xf7381a24,
            'unknown_0xb2c2928e': self.unknown_0xb2c2928e,
            'grapple_data': self.grapple_data.to_json(),
            'mod_inca_data': self.mod_inca_data.to_json(),
        }


def _decode_shooter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_missile_deflection_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_missile_deflection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_deflection_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_weapon_info(data: typing.BinaryIO, property_size: int):
    return ElectricBeamInfo.from_stream(data, property_size)


def _decode_deflection_particle(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_deflection_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf10ee8e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7171bfc2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_electric_beam_info(data: typing.BinaryIO, property_size: int):
    return ElectricBeamInfo.from_stream(data, property_size, default_override={'length': 50.0})


def _decode_patrol(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_attack_path(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_attack(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_grapple_pull_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_idle_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_idle_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdff6c19b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf7381a24(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb2c2928e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_data(data: typing.BinaryIO, property_size: int):
    return GrappleData.from_stream(data, property_size, default_override={'grapple_type': 1})


def _decode_mod_inca_data(data: typing.BinaryIO, property_size: int):
    return ModIncaData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8acc7d20: ('shooter', _decode_shooter),
    0x2c83c012: ('projectile', _decode_projectile),
    0x7ab4ab98: ('missile_deflection_offset', _decode_missile_deflection_offset),
    0x88fa2acf: ('missile_deflection_radius', _decode_missile_deflection_radius),
    0x1d159832: ('missile_deflection_rate', _decode_missile_deflection_rate),
    0x5015775: ('beam_weapon_info', _decode_beam_weapon_info),
    0x8f1ded1b: ('deflection_particle', _decode_deflection_particle),
    0xb339fac: ('beam_deflection_sound', _decode_beam_deflection_sound),
    0xf10ee8e2: ('unknown_0xf10ee8e2', _decode_unknown_0xf10ee8e2),
    0x7171bfc2: ('unknown_0x7171bfc2', _decode_unknown_0x7171bfc2),
    0x24265839: ('electric_beam_info', _decode_electric_beam_info),
    0xccdd3aca: ('patrol', _decode_patrol),
    0xc845d3c0: ('attack_path', _decode_attack_path),
    0xfa2a173f: ('attack', _decode_attack),
    0xe74cf583: ('grapple_pull_distance', _decode_grapple_pull_distance),
    0x176bd1f4: ('min_idle_delay', _decode_min_idle_delay),
    0x2e00506: ('max_idle_delay', _decode_max_idle_delay),
    0x9aa90b6b: ('recheck_path_time', _decode_recheck_path_time),
    0x7626ec89: ('recheck_path_distance', _decode_recheck_path_distance),
    0xdff6c19b: ('unknown_0xdff6c19b', _decode_unknown_0xdff6c19b),
    0xf7381a24: ('unknown_0xf7381a24', _decode_unknown_0xf7381a24),
    0xb2c2928e: ('unknown_0xb2c2928e', _decode_unknown_0xb2c2928e),
    0xf609c637: ('grapple_data', _decode_grapple_data),
    0xb4c02854: ('mod_inca_data', _decode_mod_inca_data),
}
