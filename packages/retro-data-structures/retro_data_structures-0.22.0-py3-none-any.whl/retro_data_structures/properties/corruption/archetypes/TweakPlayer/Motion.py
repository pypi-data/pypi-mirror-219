# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Motion(BaseProperty):
    forward_accel_normal: float = dataclasses.field(default=35000.0)
    forward_accel_air: float = dataclasses.field(default=8000.0)
    forward_accel_ice: float = dataclasses.field(default=35000.0)
    forward_accel_organic: float = dataclasses.field(default=35000.0)
    forward_accel_water: float = dataclasses.field(default=20000.0)
    forward_accel_lava: float = dataclasses.field(default=20000.0)
    forward_accel_phazon: float = dataclasses.field(default=20000.0)
    forward_accel_shrubbery: float = dataclasses.field(default=20000.0)
    rotational_accel_normal: float = dataclasses.field(default=14000.0)
    rotational_accel_air: float = dataclasses.field(default=14000.0)
    rotational_accel_ice: float = dataclasses.field(default=14000.0)
    rotational_accel_organic: float = dataclasses.field(default=14000.0)
    rotational_accel_water: float = dataclasses.field(default=14000.0)
    rotational_accel_lava: float = dataclasses.field(default=14000.0)
    rotational_accel_phazon: float = dataclasses.field(default=14000.0)
    rotational_accel_shrubbery: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_normal: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_air: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_ice: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_organic: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_water: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_lava: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_phazon: float = dataclasses.field(default=14000.0)
    advanced_rotational_accel_shrubbery: float = dataclasses.field(default=14000.0)
    unknown_0x600e90ff: float = dataclasses.field(default=14000.0)
    unknown_0x81f724a0: float = dataclasses.field(default=14000.0)
    unknown_0xe8b15278: float = dataclasses.field(default=14000.0)
    unknown_0x1d85f8ca: float = dataclasses.field(default=14000.0)
    unknown_0x09b0e377: float = dataclasses.field(default=14000.0)
    unknown_0x2ff175f1: float = dataclasses.field(default=14000.0)
    unknown_0x8096f89b: float = dataclasses.field(default=14000.0)
    unknown_0x90f35da8: float = dataclasses.field(default=14000.0)
    movement_friction_normal: float = dataclasses.field(default=1.0)
    movement_friction_air: float = dataclasses.field(default=0.75)
    movement_friction_ice: float = dataclasses.field(default=1.0)
    movement_friction_organic: float = dataclasses.field(default=1.0)
    movement_friction_water: float = dataclasses.field(default=1.0)
    movement_friction_lava: float = dataclasses.field(default=1.0)
    movement_friction_phazon: float = dataclasses.field(default=1.0)
    movement_friction_shrubbery: float = dataclasses.field(default=1.0)
    rotation_friction_normal: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_air: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_ice: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_organic: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_water: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_lava: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_phazon: float = dataclasses.field(default=0.44999998807907104)
    rotation_friction_shrubbery: float = dataclasses.field(default=0.44999998807907104)
    rotation_max_speed_normal: float = dataclasses.field(default=2.5)
    rotation_max_speed_air: float = dataclasses.field(default=2.5)
    rotation_max_speed_ice: float = dataclasses.field(default=2.5)
    rotation_max_speed_organic: float = dataclasses.field(default=2.5)
    rotation_max_speed_water: float = dataclasses.field(default=2.5)
    rotation_max_speed_lava: float = dataclasses.field(default=2.5)
    rotation_max_speed_phazon: float = dataclasses.field(default=2.5)
    rotation_max_speed_shrubbery: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_normal: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_air: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_ice: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_organic: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_water: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_lava: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_phazon: float = dataclasses.field(default=2.5)
    advanced_rotation_max_speed_shrubbery: float = dataclasses.field(default=2.5)
    unknown_0xd2caa709: float = dataclasses.field(default=2.5)
    unknown_0x320333aa: float = dataclasses.field(default=2.5)
    unknown_0x5b454572: float = dataclasses.field(default=2.5)
    unknown_0x49e96bd4: float = dataclasses.field(default=2.5)
    unknown_0x708c3dce: float = dataclasses.field(default=2.5)
    unknown_0xcf9768f8: float = dataclasses.field(default=2.5)
    unknown_0x3252cf6d: float = dataclasses.field(default=2.5)
    unknown_0x2db4f4e5: float = dataclasses.field(default=2.5)
    forward_max_speed_normal: float = dataclasses.field(default=16.5)
    forward_max_speed_air: float = dataclasses.field(default=16.5)
    forward_max_speed_ice: float = dataclasses.field(default=16.5)
    forward_max_speed_organic: float = dataclasses.field(default=16.5)
    forward_max_speed_water: float = dataclasses.field(default=12.5)
    forward_max_speed_lava: float = dataclasses.field(default=12.5)
    forward_max_speed_phazon: float = dataclasses.field(default=12.5)
    forward_max_speed_shrubbery: float = dataclasses.field(default=12.5)
    gravitational_accel: float = dataclasses.field(default=-35.0)
    fluid_gravitational_accel: float = dataclasses.field(default=-10.0)
    vertical_jump_accel: float = dataclasses.field(default=50.0)
    horizontal_jump_accel: float = dataclasses.field(default=50.0)
    vertical_double_jump_accel: float = dataclasses.field(default=60.0)
    horizontal_double_jump_accel: float = dataclasses.field(default=60.0)
    water_jump_factor: float = dataclasses.field(default=0.3700000047683716)
    water_ball_jump_factor: float = dataclasses.field(default=0.3700000047683716)
    lava_jump_factor: float = dataclasses.field(default=0.3700000047683716)
    lava_ball_jump_factor: float = dataclasses.field(default=0.3700000047683716)
    phazon_jump_factor: float = dataclasses.field(default=0.3700000047683716)
    phazon_ball_jump_factor: float = dataclasses.field(default=0.3700000047683716)
    allowed_jump_time: float = dataclasses.field(default=0.24950000643730164)
    allowed_double_jump_time: float = dataclasses.field(default=0.10000000149011612)
    min_double_jump_window: float = dataclasses.field(default=0.0)
    max_double_jump_window: float = dataclasses.field(default=2.0)
    unknown_0x9bb73a0b: float = dataclasses.field(default=0.0)
    min_jump_time: float = dataclasses.field(default=0.23499999940395355)
    min_double_jump_time: float = dataclasses.field(default=0.10000000149011612)
    ledge_fall_time: float = dataclasses.field(default=0.05000000074505806)
    double_jump_impulse: float = dataclasses.field(default=8.0)
    backwards_force_multiplier: float = dataclasses.field(default=1.0)
    bomb_jump_height: float = dataclasses.field(default=7.900000095367432)
    bomb_jump_radius: float = dataclasses.field(default=1.5)
    gravity_boost_time: float = dataclasses.field(default=1.5)
    gravity_boost_force: float = dataclasses.field(default=9000.0)
    gravity_boost_cancel_dampening: float = dataclasses.field(default=0.30000001192092896)
    gravity_boost_multiple_allowed: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00l')  # 108 properties

        data.write(b'\x18\xd0\xb2\xda')  # 0x18d0b2da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_normal))

        data.write(b'\x84\xf6\x1a\xc5')  # 0x84f61ac5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_air))

        data.write(b'\xed\xb0l\x1d')  # 0xedb06c1d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_ice))

        data.write(b'V\xf9\xf2\xaf')  # 0x56f9f2af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_organic))

        data.write(b'\xd0[d?')  # 0xd05b643f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_water))

        data.write(b'\x12,\xe1\x18')  # 0x122ce118
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_lava))

        data.write(b'\xf8H\xda\xbe')  # 0xf848dabe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_phazon))

        data.write(b'h\xac`(')  # 0x68ac6028
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_accel_shrubbery))

        data.write(b'\xcdN\xe9\xfc')  # 0xcd4ee9fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_normal))

        data.write(b'<F\x1d\xb2')  # 0x3c461db2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_air))

        data.write(b'U\x00kj')  # 0x55006b6a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_ice))

        data.write(b'\x84!\xe9\t')  # 0x8421e909
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_organic))

        data.write(b'.A\xa6\x1d')  # 0x2e41a61d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_water))

        data.write(b'\xdc\xf5\xb5\x80')  # 0xdcf5b580
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_lava))

        data.write(b'-\xd6\x81\x98')  # 0x2dd68198
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_phazon))

        data.write(b'\x1a\x94`s')  # 0x1a946073
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_accel_shrubbery))

        data.write(b'\x80\x05w\xd0')  # 0x800577d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_normal))

        data.write(b'\xfe\xf7\xf8\x1d')  # 0xfef7f81d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_air))

        data.write(b'\x97\xb1\x8e\xc5')  # 0x97b18ec5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_ice))

        data.write(b'\xb6\xb4\xcet')  # 0xb6b4ce74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_organic))

        data.write(b'\xd7\xbe\xd2}')  # 0xd7bed27d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_water))

        data.write(b'\x9a^\xba\x1c')  # 0x9a5eba1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_lava))

        data.write(b'`\x9d\x1f\xb4')  # 0x609d1fb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_phazon))

        data.write(b'%\x0f\xe06')  # 0x250fe036
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotational_accel_shrubbery))

        data.write(b'`\x0e\x90\xff')  # 0x600e90ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x600e90ff))

        data.write(b'\x81\xf7$\xa0')  # 0x81f724a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x81f724a0))

        data.write(b'\xe8\xb1Rx')  # 0xe8b15278
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe8b15278))

        data.write(b'\x1d\x85\xf8\xca')  # 0x1d85f8ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1d85f8ca))

        data.write(b'\t\xb0\xe3w')  # 0x9b0e377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x09b0e377))

        data.write(b'/\xf1u\xf1')  # 0x2ff175f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2ff175f1))

        data.write(b'\x80\x96\xf8\x9b')  # 0x8096f89b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8096f89b))

        data.write(b'\x90\xf3]\xa8')  # 0x90f35da8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x90f35da8))

        data.write(b'\xd4\xa2P(')  # 0xd4a25028
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_normal))

        data.write(b'+\\\xb16')  # 0x2b5cb136
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_air))

        data.write(b'B\x1a\xc7\xee')  # 0x421ac7ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_ice))

        data.write(b'\x05\x86\x13}')  # 0x586137d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_organic))

        data.write(b'\xae\xce\x03\x8b')  # 0xaece038b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_water))

        data.write(b'67\xe8\x15')  # 0x3637e815
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_lava))

        data.write(b'4:8L')  # 0x343a384c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_phazon))

        data.write(b'\x0c\xafF$')  # 0xcaf4624
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_friction_shrubbery))

        data.write(b'4\xb2\xc1H')  # 0x34b2c148
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_normal))

        data.write(b'\xb9\x17\xae\x8a')  # 0xb917ae8a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_air))

        data.write(b'\xd0Q\xd8R')  # 0xd051d852
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_ice))

        data.write(b'H\xd4b\xb4')  # 0x48d462b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_organic))

        data.write(b'k\xb6}\x81')  # 0x6bb67d81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_water))

        data.write(b'\xf4r\\\xad')  # 0xf4725cad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_lava))

        data.write(b'\xd4*\xa9,')  # 0xd42aa92c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_phazon))

        data.write(b'1\x95&\xdb')  # 0x319526db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_friction_shrubbery))

        data.write(b'Kn\xb6\xca')  # 0x4b6eb6ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_normal))

        data.write(b'\xc1\x07\xf3\xdb')  # 0xc107f3db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_air))

        data.write(b'\xa8A\x85\x03')  # 0xa8418503
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_ice))

        data.write(b'K\x1d\\\xcf')  # 0x4b1d5ccf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_organic))

        data.write(b'\xdd\xccD\xcd')  # 0xddcc44cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_water))

        data.write(b'\xe8f-\x92')  # 0xe8662d92
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_lava))

        data.write(b'\xab\xf6\xde\xae')  # 0xabf6deae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_phazon))

        data.write(b'<?\x98\x84')  # 0x3c3f9884
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_max_speed_shrubbery))

        data.write(b'y\xfb\x91\xb7')  # 0x79fb91b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_normal))

        data.write(b'\x87\xac\xfcG')  # 0x87acfc47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_air))

        data.write(b'\xee\xea\x8a\x9f')  # 0xeeea8a9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_ice))

        data.write(b'e\x9b\xc4i')  # 0x659bc469
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_organic))

        data.write(b'\x90\x87\xda\xe1')  # 0x9087dae1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_water))

        data.write(b'\x11\x99Y\xf2')  # 0x119959f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_lava))

        data.write(b'\x99c\xf9\xd3')  # 0x9963f9d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_phazon))

        data.write(b':\xb6\xb6\x1b')  # 0x3ab6b61b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.advanced_rotation_max_speed_shrubbery))

        data.write(b'\xd2\xca\xa7\t')  # 0xd2caa709
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd2caa709))

        data.write(b'2\x033\xaa')  # 0x320333aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x320333aa))

        data.write(b'[EEr')  # 0x5b454572
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5b454572))

        data.write(b'I\xe9k\xd4')  # 0x49e96bd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x49e96bd4))

        data.write(b'p\x8c=\xce')  # 0x708c3dce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x708c3dce))

        data.write(b'\xcf\x97h\xf8')  # 0xcf9768f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcf9768f8))

        data.write(b'2R\xcfm')  # 0x3252cf6d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3252cf6d))

        data.write(b'-\xb4\xf4\xe5')  # 0x2db4f4e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2db4f4e5))

        data.write(b'\xff\xd4\xa00')  # 0xffd4a030
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_normal))

        data.write(b'Y\xdf\xbc\xb9')  # 0x59dfbcb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_air))

        data.write(b'0\x99\xcaa')  # 0x3099ca61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_ice))

        data.write(b'\x16\xc1\xfd\xdb')  # 0x16c1fddb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_organic))

        data.write(b'ld\x891')  # 0x6c648931
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_water))

        data.write(b'KB\xf5\xa9')  # 0x4b42f5a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_lava))

        data.write(b'\x1fL\xc8T')  # 0x1f4cc854
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_phazon))

        data.write(b'\xb3@\x81s')  # 0xb3408173
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_max_speed_shrubbery))

        data.write(b'\x14\xb7\x8a\xaf')  # 0x14b78aaf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravitational_accel))

        data.write(b',v \xd3')  # 0x2c7620d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fluid_gravitational_accel))

        data.write(b'\x0c,\x91\xf7')  # 0xc2c91f7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_jump_accel))

        data.write(b'\x93\x8cw\xd4')  # 0x938c77d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_jump_accel))

        data.write(b'\x13\xc9]\xfd')  # 0x13c95dfd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_double_jump_accel))

        data.write(b'\x8eA\xfe\xd2')  # 0x8e41fed2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_double_jump_accel))

        data.write(b'\xb2a\xfa0')  # 0xb261fa30
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.water_jump_factor))

        data.write(b'j\xe5`\xe9')  # 0x6ae560e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.water_ball_jump_factor))

        data.write(b'\x03\x14\x963')  # 0x3149633
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lava_jump_factor))

        data.write(b'\xd7\xb3\xf3\xea')  # 0xd7b3f3ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lava_ball_jump_factor))

        data.write(b'\xaf\x14P\xa2')  # 0xaf1450a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_jump_factor))

        data.write(b'\x98\rp\x1a')  # 0x980d701a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_ball_jump_factor))

        data.write(b'\xa8\x05\xfe\xae')  # 0xa805feae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.allowed_jump_time))

        data.write(b'#>1\x99')  # 0x233e3199
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.allowed_double_jump_time))

        data.write(b'\x97\xf3\x0b\x95')  # 0x97f30b95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_double_jump_window))

        data.write(b'LLXr')  # 0x4c4c5872
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_double_jump_window))

        data.write(b'\x9b\xb7:\x0b')  # 0x9bb73a0b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9bb73a0b))

        data.write(b'L\x8dfL')  # 0x4c8d664c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_jump_time))

        data.write(b'\x1f\xc2\x01i')  # 0x1fc20169
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_double_jump_time))

        data.write(b'\xe7\xa5\xd7Y')  # 0xe7a5d759
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ledge_fall_time))

        data.write(b'pD\xb2\x95')  # 0x7044b295
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.double_jump_impulse))

        data.write(b'\xd8#\x80\xa6')  # 0xd82380a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.backwards_force_multiplier))

        data.write(b'*.A\x00')  # 0x2a2e4100
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_jump_height))

        data.write(b'\x90UE\xe6')  # 0x905545e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_jump_radius))

        data.write(b'"\x94`\xbe')  # 0x229460be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_boost_time))

        data.write(b'\x0e#\x8f\xd3')  # 0xe238fd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_boost_force))

        data.write(b'\xdc\x92\xa0\xac')  # 0xdc92a0ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_boost_cancel_dampening))

        data.write(b'\xe1\xfe\xfd<')  # 0xe1fefd3c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.gravity_boost_multiple_allowed))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            forward_accel_normal=data['forward_accel_normal'],
            forward_accel_air=data['forward_accel_air'],
            forward_accel_ice=data['forward_accel_ice'],
            forward_accel_organic=data['forward_accel_organic'],
            forward_accel_water=data['forward_accel_water'],
            forward_accel_lava=data['forward_accel_lava'],
            forward_accel_phazon=data['forward_accel_phazon'],
            forward_accel_shrubbery=data['forward_accel_shrubbery'],
            rotational_accel_normal=data['rotational_accel_normal'],
            rotational_accel_air=data['rotational_accel_air'],
            rotational_accel_ice=data['rotational_accel_ice'],
            rotational_accel_organic=data['rotational_accel_organic'],
            rotational_accel_water=data['rotational_accel_water'],
            rotational_accel_lava=data['rotational_accel_lava'],
            rotational_accel_phazon=data['rotational_accel_phazon'],
            rotational_accel_shrubbery=data['rotational_accel_shrubbery'],
            advanced_rotational_accel_normal=data['advanced_rotational_accel_normal'],
            advanced_rotational_accel_air=data['advanced_rotational_accel_air'],
            advanced_rotational_accel_ice=data['advanced_rotational_accel_ice'],
            advanced_rotational_accel_organic=data['advanced_rotational_accel_organic'],
            advanced_rotational_accel_water=data['advanced_rotational_accel_water'],
            advanced_rotational_accel_lava=data['advanced_rotational_accel_lava'],
            advanced_rotational_accel_phazon=data['advanced_rotational_accel_phazon'],
            advanced_rotational_accel_shrubbery=data['advanced_rotational_accel_shrubbery'],
            unknown_0x600e90ff=data['unknown_0x600e90ff'],
            unknown_0x81f724a0=data['unknown_0x81f724a0'],
            unknown_0xe8b15278=data['unknown_0xe8b15278'],
            unknown_0x1d85f8ca=data['unknown_0x1d85f8ca'],
            unknown_0x09b0e377=data['unknown_0x09b0e377'],
            unknown_0x2ff175f1=data['unknown_0x2ff175f1'],
            unknown_0x8096f89b=data['unknown_0x8096f89b'],
            unknown_0x90f35da8=data['unknown_0x90f35da8'],
            movement_friction_normal=data['movement_friction_normal'],
            movement_friction_air=data['movement_friction_air'],
            movement_friction_ice=data['movement_friction_ice'],
            movement_friction_organic=data['movement_friction_organic'],
            movement_friction_water=data['movement_friction_water'],
            movement_friction_lava=data['movement_friction_lava'],
            movement_friction_phazon=data['movement_friction_phazon'],
            movement_friction_shrubbery=data['movement_friction_shrubbery'],
            rotation_friction_normal=data['rotation_friction_normal'],
            rotation_friction_air=data['rotation_friction_air'],
            rotation_friction_ice=data['rotation_friction_ice'],
            rotation_friction_organic=data['rotation_friction_organic'],
            rotation_friction_water=data['rotation_friction_water'],
            rotation_friction_lava=data['rotation_friction_lava'],
            rotation_friction_phazon=data['rotation_friction_phazon'],
            rotation_friction_shrubbery=data['rotation_friction_shrubbery'],
            rotation_max_speed_normal=data['rotation_max_speed_normal'],
            rotation_max_speed_air=data['rotation_max_speed_air'],
            rotation_max_speed_ice=data['rotation_max_speed_ice'],
            rotation_max_speed_organic=data['rotation_max_speed_organic'],
            rotation_max_speed_water=data['rotation_max_speed_water'],
            rotation_max_speed_lava=data['rotation_max_speed_lava'],
            rotation_max_speed_phazon=data['rotation_max_speed_phazon'],
            rotation_max_speed_shrubbery=data['rotation_max_speed_shrubbery'],
            advanced_rotation_max_speed_normal=data['advanced_rotation_max_speed_normal'],
            advanced_rotation_max_speed_air=data['advanced_rotation_max_speed_air'],
            advanced_rotation_max_speed_ice=data['advanced_rotation_max_speed_ice'],
            advanced_rotation_max_speed_organic=data['advanced_rotation_max_speed_organic'],
            advanced_rotation_max_speed_water=data['advanced_rotation_max_speed_water'],
            advanced_rotation_max_speed_lava=data['advanced_rotation_max_speed_lava'],
            advanced_rotation_max_speed_phazon=data['advanced_rotation_max_speed_phazon'],
            advanced_rotation_max_speed_shrubbery=data['advanced_rotation_max_speed_shrubbery'],
            unknown_0xd2caa709=data['unknown_0xd2caa709'],
            unknown_0x320333aa=data['unknown_0x320333aa'],
            unknown_0x5b454572=data['unknown_0x5b454572'],
            unknown_0x49e96bd4=data['unknown_0x49e96bd4'],
            unknown_0x708c3dce=data['unknown_0x708c3dce'],
            unknown_0xcf9768f8=data['unknown_0xcf9768f8'],
            unknown_0x3252cf6d=data['unknown_0x3252cf6d'],
            unknown_0x2db4f4e5=data['unknown_0x2db4f4e5'],
            forward_max_speed_normal=data['forward_max_speed_normal'],
            forward_max_speed_air=data['forward_max_speed_air'],
            forward_max_speed_ice=data['forward_max_speed_ice'],
            forward_max_speed_organic=data['forward_max_speed_organic'],
            forward_max_speed_water=data['forward_max_speed_water'],
            forward_max_speed_lava=data['forward_max_speed_lava'],
            forward_max_speed_phazon=data['forward_max_speed_phazon'],
            forward_max_speed_shrubbery=data['forward_max_speed_shrubbery'],
            gravitational_accel=data['gravitational_accel'],
            fluid_gravitational_accel=data['fluid_gravitational_accel'],
            vertical_jump_accel=data['vertical_jump_accel'],
            horizontal_jump_accel=data['horizontal_jump_accel'],
            vertical_double_jump_accel=data['vertical_double_jump_accel'],
            horizontal_double_jump_accel=data['horizontal_double_jump_accel'],
            water_jump_factor=data['water_jump_factor'],
            water_ball_jump_factor=data['water_ball_jump_factor'],
            lava_jump_factor=data['lava_jump_factor'],
            lava_ball_jump_factor=data['lava_ball_jump_factor'],
            phazon_jump_factor=data['phazon_jump_factor'],
            phazon_ball_jump_factor=data['phazon_ball_jump_factor'],
            allowed_jump_time=data['allowed_jump_time'],
            allowed_double_jump_time=data['allowed_double_jump_time'],
            min_double_jump_window=data['min_double_jump_window'],
            max_double_jump_window=data['max_double_jump_window'],
            unknown_0x9bb73a0b=data['unknown_0x9bb73a0b'],
            min_jump_time=data['min_jump_time'],
            min_double_jump_time=data['min_double_jump_time'],
            ledge_fall_time=data['ledge_fall_time'],
            double_jump_impulse=data['double_jump_impulse'],
            backwards_force_multiplier=data['backwards_force_multiplier'],
            bomb_jump_height=data['bomb_jump_height'],
            bomb_jump_radius=data['bomb_jump_radius'],
            gravity_boost_time=data['gravity_boost_time'],
            gravity_boost_force=data['gravity_boost_force'],
            gravity_boost_cancel_dampening=data['gravity_boost_cancel_dampening'],
            gravity_boost_multiple_allowed=data['gravity_boost_multiple_allowed'],
        )

    def to_json(self) -> dict:
        return {
            'forward_accel_normal': self.forward_accel_normal,
            'forward_accel_air': self.forward_accel_air,
            'forward_accel_ice': self.forward_accel_ice,
            'forward_accel_organic': self.forward_accel_organic,
            'forward_accel_water': self.forward_accel_water,
            'forward_accel_lava': self.forward_accel_lava,
            'forward_accel_phazon': self.forward_accel_phazon,
            'forward_accel_shrubbery': self.forward_accel_shrubbery,
            'rotational_accel_normal': self.rotational_accel_normal,
            'rotational_accel_air': self.rotational_accel_air,
            'rotational_accel_ice': self.rotational_accel_ice,
            'rotational_accel_organic': self.rotational_accel_organic,
            'rotational_accel_water': self.rotational_accel_water,
            'rotational_accel_lava': self.rotational_accel_lava,
            'rotational_accel_phazon': self.rotational_accel_phazon,
            'rotational_accel_shrubbery': self.rotational_accel_shrubbery,
            'advanced_rotational_accel_normal': self.advanced_rotational_accel_normal,
            'advanced_rotational_accel_air': self.advanced_rotational_accel_air,
            'advanced_rotational_accel_ice': self.advanced_rotational_accel_ice,
            'advanced_rotational_accel_organic': self.advanced_rotational_accel_organic,
            'advanced_rotational_accel_water': self.advanced_rotational_accel_water,
            'advanced_rotational_accel_lava': self.advanced_rotational_accel_lava,
            'advanced_rotational_accel_phazon': self.advanced_rotational_accel_phazon,
            'advanced_rotational_accel_shrubbery': self.advanced_rotational_accel_shrubbery,
            'unknown_0x600e90ff': self.unknown_0x600e90ff,
            'unknown_0x81f724a0': self.unknown_0x81f724a0,
            'unknown_0xe8b15278': self.unknown_0xe8b15278,
            'unknown_0x1d85f8ca': self.unknown_0x1d85f8ca,
            'unknown_0x09b0e377': self.unknown_0x09b0e377,
            'unknown_0x2ff175f1': self.unknown_0x2ff175f1,
            'unknown_0x8096f89b': self.unknown_0x8096f89b,
            'unknown_0x90f35da8': self.unknown_0x90f35da8,
            'movement_friction_normal': self.movement_friction_normal,
            'movement_friction_air': self.movement_friction_air,
            'movement_friction_ice': self.movement_friction_ice,
            'movement_friction_organic': self.movement_friction_organic,
            'movement_friction_water': self.movement_friction_water,
            'movement_friction_lava': self.movement_friction_lava,
            'movement_friction_phazon': self.movement_friction_phazon,
            'movement_friction_shrubbery': self.movement_friction_shrubbery,
            'rotation_friction_normal': self.rotation_friction_normal,
            'rotation_friction_air': self.rotation_friction_air,
            'rotation_friction_ice': self.rotation_friction_ice,
            'rotation_friction_organic': self.rotation_friction_organic,
            'rotation_friction_water': self.rotation_friction_water,
            'rotation_friction_lava': self.rotation_friction_lava,
            'rotation_friction_phazon': self.rotation_friction_phazon,
            'rotation_friction_shrubbery': self.rotation_friction_shrubbery,
            'rotation_max_speed_normal': self.rotation_max_speed_normal,
            'rotation_max_speed_air': self.rotation_max_speed_air,
            'rotation_max_speed_ice': self.rotation_max_speed_ice,
            'rotation_max_speed_organic': self.rotation_max_speed_organic,
            'rotation_max_speed_water': self.rotation_max_speed_water,
            'rotation_max_speed_lava': self.rotation_max_speed_lava,
            'rotation_max_speed_phazon': self.rotation_max_speed_phazon,
            'rotation_max_speed_shrubbery': self.rotation_max_speed_shrubbery,
            'advanced_rotation_max_speed_normal': self.advanced_rotation_max_speed_normal,
            'advanced_rotation_max_speed_air': self.advanced_rotation_max_speed_air,
            'advanced_rotation_max_speed_ice': self.advanced_rotation_max_speed_ice,
            'advanced_rotation_max_speed_organic': self.advanced_rotation_max_speed_organic,
            'advanced_rotation_max_speed_water': self.advanced_rotation_max_speed_water,
            'advanced_rotation_max_speed_lava': self.advanced_rotation_max_speed_lava,
            'advanced_rotation_max_speed_phazon': self.advanced_rotation_max_speed_phazon,
            'advanced_rotation_max_speed_shrubbery': self.advanced_rotation_max_speed_shrubbery,
            'unknown_0xd2caa709': self.unknown_0xd2caa709,
            'unknown_0x320333aa': self.unknown_0x320333aa,
            'unknown_0x5b454572': self.unknown_0x5b454572,
            'unknown_0x49e96bd4': self.unknown_0x49e96bd4,
            'unknown_0x708c3dce': self.unknown_0x708c3dce,
            'unknown_0xcf9768f8': self.unknown_0xcf9768f8,
            'unknown_0x3252cf6d': self.unknown_0x3252cf6d,
            'unknown_0x2db4f4e5': self.unknown_0x2db4f4e5,
            'forward_max_speed_normal': self.forward_max_speed_normal,
            'forward_max_speed_air': self.forward_max_speed_air,
            'forward_max_speed_ice': self.forward_max_speed_ice,
            'forward_max_speed_organic': self.forward_max_speed_organic,
            'forward_max_speed_water': self.forward_max_speed_water,
            'forward_max_speed_lava': self.forward_max_speed_lava,
            'forward_max_speed_phazon': self.forward_max_speed_phazon,
            'forward_max_speed_shrubbery': self.forward_max_speed_shrubbery,
            'gravitational_accel': self.gravitational_accel,
            'fluid_gravitational_accel': self.fluid_gravitational_accel,
            'vertical_jump_accel': self.vertical_jump_accel,
            'horizontal_jump_accel': self.horizontal_jump_accel,
            'vertical_double_jump_accel': self.vertical_double_jump_accel,
            'horizontal_double_jump_accel': self.horizontal_double_jump_accel,
            'water_jump_factor': self.water_jump_factor,
            'water_ball_jump_factor': self.water_ball_jump_factor,
            'lava_jump_factor': self.lava_jump_factor,
            'lava_ball_jump_factor': self.lava_ball_jump_factor,
            'phazon_jump_factor': self.phazon_jump_factor,
            'phazon_ball_jump_factor': self.phazon_ball_jump_factor,
            'allowed_jump_time': self.allowed_jump_time,
            'allowed_double_jump_time': self.allowed_double_jump_time,
            'min_double_jump_window': self.min_double_jump_window,
            'max_double_jump_window': self.max_double_jump_window,
            'unknown_0x9bb73a0b': self.unknown_0x9bb73a0b,
            'min_jump_time': self.min_jump_time,
            'min_double_jump_time': self.min_double_jump_time,
            'ledge_fall_time': self.ledge_fall_time,
            'double_jump_impulse': self.double_jump_impulse,
            'backwards_force_multiplier': self.backwards_force_multiplier,
            'bomb_jump_height': self.bomb_jump_height,
            'bomb_jump_radius': self.bomb_jump_radius,
            'gravity_boost_time': self.gravity_boost_time,
            'gravity_boost_force': self.gravity_boost_force,
            'gravity_boost_cancel_dampening': self.gravity_boost_cancel_dampening,
            'gravity_boost_multiple_allowed': self.gravity_boost_multiple_allowed,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x18d0b2da, 0x84f61ac5, 0xedb06c1d, 0x56f9f2af, 0xd05b643f, 0x122ce118, 0xf848dabe, 0x68ac6028, 0xcd4ee9fc, 0x3c461db2, 0x55006b6a, 0x8421e909, 0x2e41a61d, 0xdcf5b580, 0x2dd68198, 0x1a946073, 0x800577d0, 0xfef7f81d, 0x97b18ec5, 0xb6b4ce74, 0xd7bed27d, 0x9a5eba1c, 0x609d1fb4, 0x250fe036, 0x600e90ff, 0x81f724a0, 0xe8b15278, 0x1d85f8ca, 0x9b0e377, 0x2ff175f1, 0x8096f89b, 0x90f35da8, 0xd4a25028, 0x2b5cb136, 0x421ac7ee, 0x586137d, 0xaece038b, 0x3637e815, 0x343a384c, 0xcaf4624, 0x34b2c148, 0xb917ae8a, 0xd051d852, 0x48d462b4, 0x6bb67d81, 0xf4725cad, 0xd42aa92c, 0x319526db, 0x4b6eb6ca, 0xc107f3db, 0xa8418503, 0x4b1d5ccf, 0xddcc44cd, 0xe8662d92, 0xabf6deae, 0x3c3f9884, 0x79fb91b7, 0x87acfc47, 0xeeea8a9f, 0x659bc469, 0x9087dae1, 0x119959f2, 0x9963f9d3, 0x3ab6b61b, 0xd2caa709, 0x320333aa, 0x5b454572, 0x49e96bd4, 0x708c3dce, 0xcf9768f8, 0x3252cf6d, 0x2db4f4e5, 0xffd4a030, 0x59dfbcb9, 0x3099ca61, 0x16c1fddb, 0x6c648931, 0x4b42f5a9, 0x1f4cc854, 0xb3408173, 0x14b78aaf, 0x2c7620d3, 0xc2c91f7, 0x938c77d4, 0x13c95dfd, 0x8e41fed2, 0xb261fa30, 0x6ae560e9, 0x3149633, 0xd7b3f3ea, 0xaf1450a2, 0x980d701a, 0xa805feae, 0x233e3199, 0x97f30b95, 0x4c4c5872, 0x9bb73a0b, 0x4c8d664c, 0x1fc20169, 0xe7a5d759, 0x7044b295, 0xd82380a6, 0x2a2e4100, 0x905545e6, 0x229460be, 0xe238fd3, 0xdc92a0ac, 0xe1fefd3c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Motion]:
    if property_count != 108:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(1077))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72], dec[75], dec[78], dec[81], dec[84], dec[87], dec[90], dec[93], dec[96], dec[99], dec[102], dec[105], dec[108], dec[111], dec[114], dec[117], dec[120], dec[123], dec[126], dec[129], dec[132], dec[135], dec[138], dec[141], dec[144], dec[147], dec[150], dec[153], dec[156], dec[159], dec[162], dec[165], dec[168], dec[171], dec[174], dec[177], dec[180], dec[183], dec[186], dec[189], dec[192], dec[195], dec[198], dec[201], dec[204], dec[207], dec[210], dec[213], dec[216], dec[219], dec[222], dec[225], dec[228], dec[231], dec[234], dec[237], dec[240], dec[243], dec[246], dec[249], dec[252], dec[255], dec[258], dec[261], dec[264], dec[267], dec[270], dec[273], dec[276], dec[279], dec[282], dec[285], dec[288], dec[291], dec[294], dec[297], dec[300], dec[303], dec[306], dec[309], dec[312], dec[315], dec[318], dec[321]) != _FAST_IDS:
        data.seek(before)
        return None

    return Motion(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
        dec[44],
        dec[47],
        dec[50],
        dec[53],
        dec[56],
        dec[59],
        dec[62],
        dec[65],
        dec[68],
        dec[71],
        dec[74],
        dec[77],
        dec[80],
        dec[83],
        dec[86],
        dec[89],
        dec[92],
        dec[95],
        dec[98],
        dec[101],
        dec[104],
        dec[107],
        dec[110],
        dec[113],
        dec[116],
        dec[119],
        dec[122],
        dec[125],
        dec[128],
        dec[131],
        dec[134],
        dec[137],
        dec[140],
        dec[143],
        dec[146],
        dec[149],
        dec[152],
        dec[155],
        dec[158],
        dec[161],
        dec[164],
        dec[167],
        dec[170],
        dec[173],
        dec[176],
        dec[179],
        dec[182],
        dec[185],
        dec[188],
        dec[191],
        dec[194],
        dec[197],
        dec[200],
        dec[203],
        dec[206],
        dec[209],
        dec[212],
        dec[215],
        dec[218],
        dec[221],
        dec[224],
        dec[227],
        dec[230],
        dec[233],
        dec[236],
        dec[239],
        dec[242],
        dec[245],
        dec[248],
        dec[251],
        dec[254],
        dec[257],
        dec[260],
        dec[263],
        dec[266],
        dec[269],
        dec[272],
        dec[275],
        dec[278],
        dec[281],
        dec[284],
        dec[287],
        dec[290],
        dec[293],
        dec[296],
        dec[299],
        dec[302],
        dec[305],
        dec[308],
        dec[311],
        dec[314],
        dec[317],
        dec[320],
        dec[323],
    )


def _decode_forward_accel_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_accel_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotational_accel_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotational_accel_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x600e90ff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81f724a0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe8b15278(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1d85f8ca(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x09b0e377(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2ff175f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8096f89b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x90f35da8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_friction_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_friction_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_max_speed_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_rotation_max_speed_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd2caa709(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x320333aa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5b454572(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x49e96bd4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x708c3dce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcf9768f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3252cf6d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2db4f4e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_normal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_ice(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_organic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_water(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_lava(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_phazon(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_max_speed_shrubbery(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravitational_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fluid_gravitational_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_jump_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_jump_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_double_jump_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_double_jump_accel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_water_jump_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_water_ball_jump_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lava_jump_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lava_ball_jump_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_jump_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_ball_jump_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allowed_jump_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allowed_double_jump_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_double_jump_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_double_jump_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9bb73a0b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_jump_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_double_jump_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ledge_fall_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_double_jump_impulse(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_backwards_force_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_jump_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_boost_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_boost_force(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_boost_cancel_dampening(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_boost_multiple_allowed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x18d0b2da: ('forward_accel_normal', _decode_forward_accel_normal),
    0x84f61ac5: ('forward_accel_air', _decode_forward_accel_air),
    0xedb06c1d: ('forward_accel_ice', _decode_forward_accel_ice),
    0x56f9f2af: ('forward_accel_organic', _decode_forward_accel_organic),
    0xd05b643f: ('forward_accel_water', _decode_forward_accel_water),
    0x122ce118: ('forward_accel_lava', _decode_forward_accel_lava),
    0xf848dabe: ('forward_accel_phazon', _decode_forward_accel_phazon),
    0x68ac6028: ('forward_accel_shrubbery', _decode_forward_accel_shrubbery),
    0xcd4ee9fc: ('rotational_accel_normal', _decode_rotational_accel_normal),
    0x3c461db2: ('rotational_accel_air', _decode_rotational_accel_air),
    0x55006b6a: ('rotational_accel_ice', _decode_rotational_accel_ice),
    0x8421e909: ('rotational_accel_organic', _decode_rotational_accel_organic),
    0x2e41a61d: ('rotational_accel_water', _decode_rotational_accel_water),
    0xdcf5b580: ('rotational_accel_lava', _decode_rotational_accel_lava),
    0x2dd68198: ('rotational_accel_phazon', _decode_rotational_accel_phazon),
    0x1a946073: ('rotational_accel_shrubbery', _decode_rotational_accel_shrubbery),
    0x800577d0: ('advanced_rotational_accel_normal', _decode_advanced_rotational_accel_normal),
    0xfef7f81d: ('advanced_rotational_accel_air', _decode_advanced_rotational_accel_air),
    0x97b18ec5: ('advanced_rotational_accel_ice', _decode_advanced_rotational_accel_ice),
    0xb6b4ce74: ('advanced_rotational_accel_organic', _decode_advanced_rotational_accel_organic),
    0xd7bed27d: ('advanced_rotational_accel_water', _decode_advanced_rotational_accel_water),
    0x9a5eba1c: ('advanced_rotational_accel_lava', _decode_advanced_rotational_accel_lava),
    0x609d1fb4: ('advanced_rotational_accel_phazon', _decode_advanced_rotational_accel_phazon),
    0x250fe036: ('advanced_rotational_accel_shrubbery', _decode_advanced_rotational_accel_shrubbery),
    0x600e90ff: ('unknown_0x600e90ff', _decode_unknown_0x600e90ff),
    0x81f724a0: ('unknown_0x81f724a0', _decode_unknown_0x81f724a0),
    0xe8b15278: ('unknown_0xe8b15278', _decode_unknown_0xe8b15278),
    0x1d85f8ca: ('unknown_0x1d85f8ca', _decode_unknown_0x1d85f8ca),
    0x9b0e377: ('unknown_0x09b0e377', _decode_unknown_0x09b0e377),
    0x2ff175f1: ('unknown_0x2ff175f1', _decode_unknown_0x2ff175f1),
    0x8096f89b: ('unknown_0x8096f89b', _decode_unknown_0x8096f89b),
    0x90f35da8: ('unknown_0x90f35da8', _decode_unknown_0x90f35da8),
    0xd4a25028: ('movement_friction_normal', _decode_movement_friction_normal),
    0x2b5cb136: ('movement_friction_air', _decode_movement_friction_air),
    0x421ac7ee: ('movement_friction_ice', _decode_movement_friction_ice),
    0x586137d: ('movement_friction_organic', _decode_movement_friction_organic),
    0xaece038b: ('movement_friction_water', _decode_movement_friction_water),
    0x3637e815: ('movement_friction_lava', _decode_movement_friction_lava),
    0x343a384c: ('movement_friction_phazon', _decode_movement_friction_phazon),
    0xcaf4624: ('movement_friction_shrubbery', _decode_movement_friction_shrubbery),
    0x34b2c148: ('rotation_friction_normal', _decode_rotation_friction_normal),
    0xb917ae8a: ('rotation_friction_air', _decode_rotation_friction_air),
    0xd051d852: ('rotation_friction_ice', _decode_rotation_friction_ice),
    0x48d462b4: ('rotation_friction_organic', _decode_rotation_friction_organic),
    0x6bb67d81: ('rotation_friction_water', _decode_rotation_friction_water),
    0xf4725cad: ('rotation_friction_lava', _decode_rotation_friction_lava),
    0xd42aa92c: ('rotation_friction_phazon', _decode_rotation_friction_phazon),
    0x319526db: ('rotation_friction_shrubbery', _decode_rotation_friction_shrubbery),
    0x4b6eb6ca: ('rotation_max_speed_normal', _decode_rotation_max_speed_normal),
    0xc107f3db: ('rotation_max_speed_air', _decode_rotation_max_speed_air),
    0xa8418503: ('rotation_max_speed_ice', _decode_rotation_max_speed_ice),
    0x4b1d5ccf: ('rotation_max_speed_organic', _decode_rotation_max_speed_organic),
    0xddcc44cd: ('rotation_max_speed_water', _decode_rotation_max_speed_water),
    0xe8662d92: ('rotation_max_speed_lava', _decode_rotation_max_speed_lava),
    0xabf6deae: ('rotation_max_speed_phazon', _decode_rotation_max_speed_phazon),
    0x3c3f9884: ('rotation_max_speed_shrubbery', _decode_rotation_max_speed_shrubbery),
    0x79fb91b7: ('advanced_rotation_max_speed_normal', _decode_advanced_rotation_max_speed_normal),
    0x87acfc47: ('advanced_rotation_max_speed_air', _decode_advanced_rotation_max_speed_air),
    0xeeea8a9f: ('advanced_rotation_max_speed_ice', _decode_advanced_rotation_max_speed_ice),
    0x659bc469: ('advanced_rotation_max_speed_organic', _decode_advanced_rotation_max_speed_organic),
    0x9087dae1: ('advanced_rotation_max_speed_water', _decode_advanced_rotation_max_speed_water),
    0x119959f2: ('advanced_rotation_max_speed_lava', _decode_advanced_rotation_max_speed_lava),
    0x9963f9d3: ('advanced_rotation_max_speed_phazon', _decode_advanced_rotation_max_speed_phazon),
    0x3ab6b61b: ('advanced_rotation_max_speed_shrubbery', _decode_advanced_rotation_max_speed_shrubbery),
    0xd2caa709: ('unknown_0xd2caa709', _decode_unknown_0xd2caa709),
    0x320333aa: ('unknown_0x320333aa', _decode_unknown_0x320333aa),
    0x5b454572: ('unknown_0x5b454572', _decode_unknown_0x5b454572),
    0x49e96bd4: ('unknown_0x49e96bd4', _decode_unknown_0x49e96bd4),
    0x708c3dce: ('unknown_0x708c3dce', _decode_unknown_0x708c3dce),
    0xcf9768f8: ('unknown_0xcf9768f8', _decode_unknown_0xcf9768f8),
    0x3252cf6d: ('unknown_0x3252cf6d', _decode_unknown_0x3252cf6d),
    0x2db4f4e5: ('unknown_0x2db4f4e5', _decode_unknown_0x2db4f4e5),
    0xffd4a030: ('forward_max_speed_normal', _decode_forward_max_speed_normal),
    0x59dfbcb9: ('forward_max_speed_air', _decode_forward_max_speed_air),
    0x3099ca61: ('forward_max_speed_ice', _decode_forward_max_speed_ice),
    0x16c1fddb: ('forward_max_speed_organic', _decode_forward_max_speed_organic),
    0x6c648931: ('forward_max_speed_water', _decode_forward_max_speed_water),
    0x4b42f5a9: ('forward_max_speed_lava', _decode_forward_max_speed_lava),
    0x1f4cc854: ('forward_max_speed_phazon', _decode_forward_max_speed_phazon),
    0xb3408173: ('forward_max_speed_shrubbery', _decode_forward_max_speed_shrubbery),
    0x14b78aaf: ('gravitational_accel', _decode_gravitational_accel),
    0x2c7620d3: ('fluid_gravitational_accel', _decode_fluid_gravitational_accel),
    0xc2c91f7: ('vertical_jump_accel', _decode_vertical_jump_accel),
    0x938c77d4: ('horizontal_jump_accel', _decode_horizontal_jump_accel),
    0x13c95dfd: ('vertical_double_jump_accel', _decode_vertical_double_jump_accel),
    0x8e41fed2: ('horizontal_double_jump_accel', _decode_horizontal_double_jump_accel),
    0xb261fa30: ('water_jump_factor', _decode_water_jump_factor),
    0x6ae560e9: ('water_ball_jump_factor', _decode_water_ball_jump_factor),
    0x3149633: ('lava_jump_factor', _decode_lava_jump_factor),
    0xd7b3f3ea: ('lava_ball_jump_factor', _decode_lava_ball_jump_factor),
    0xaf1450a2: ('phazon_jump_factor', _decode_phazon_jump_factor),
    0x980d701a: ('phazon_ball_jump_factor', _decode_phazon_ball_jump_factor),
    0xa805feae: ('allowed_jump_time', _decode_allowed_jump_time),
    0x233e3199: ('allowed_double_jump_time', _decode_allowed_double_jump_time),
    0x97f30b95: ('min_double_jump_window', _decode_min_double_jump_window),
    0x4c4c5872: ('max_double_jump_window', _decode_max_double_jump_window),
    0x9bb73a0b: ('unknown_0x9bb73a0b', _decode_unknown_0x9bb73a0b),
    0x4c8d664c: ('min_jump_time', _decode_min_jump_time),
    0x1fc20169: ('min_double_jump_time', _decode_min_double_jump_time),
    0xe7a5d759: ('ledge_fall_time', _decode_ledge_fall_time),
    0x7044b295: ('double_jump_impulse', _decode_double_jump_impulse),
    0xd82380a6: ('backwards_force_multiplier', _decode_backwards_force_multiplier),
    0x2a2e4100: ('bomb_jump_height', _decode_bomb_jump_height),
    0x905545e6: ('bomb_jump_radius', _decode_bomb_jump_radius),
    0x229460be: ('gravity_boost_time', _decode_gravity_boost_time),
    0xe238fd3: ('gravity_boost_force', _decode_gravity_boost_force),
    0xdc92a0ac: ('gravity_boost_cancel_dampening', _decode_gravity_boost_cancel_dampening),
    0xe1fefd3c: ('gravity_boost_multiple_allowed', _decode_gravity_boost_multiple_allowed),
}
