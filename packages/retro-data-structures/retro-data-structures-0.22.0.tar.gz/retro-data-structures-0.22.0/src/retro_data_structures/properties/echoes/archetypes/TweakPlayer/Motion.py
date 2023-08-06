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
    unknown: float = dataclasses.field(default=0.0)
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
        return Game.ECHOES

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
        data.write(b'\x00L')  # 76 properties

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
        data.write(struct.pack('>f', self.unknown))

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
            unknown=data['unknown'],
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
            'unknown': self.unknown,
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

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x18d0b2da, 0x84f61ac5, 0xedb06c1d, 0x56f9f2af, 0xd05b643f, 0x122ce118, 0xf848dabe, 0x68ac6028, 0xcd4ee9fc, 0x3c461db2, 0x55006b6a, 0x8421e909, 0x2e41a61d, 0xdcf5b580, 0x2dd68198, 0x1a946073, 0xd4a25028, 0x2b5cb136, 0x421ac7ee, 0x586137d, 0xaece038b, 0x3637e815, 0x343a384c, 0xcaf4624, 0x34b2c148, 0xb917ae8a, 0xd051d852, 0x48d462b4, 0x6bb67d81, 0xf4725cad, 0xd42aa92c, 0x319526db, 0x4b6eb6ca, 0xc107f3db, 0xa8418503, 0x4b1d5ccf, 0xddcc44cd, 0xe8662d92, 0xabf6deae, 0x3c3f9884, 0xffd4a030, 0x59dfbcb9, 0x3099ca61, 0x16c1fddb, 0x6c648931, 0x4b42f5a9, 0x1f4cc854, 0xb3408173, 0x14b78aaf, 0x2c7620d3, 0xc2c91f7, 0x938c77d4, 0x13c95dfd, 0x8e41fed2, 0xb261fa30, 0x6ae560e9, 0x3149633, 0xd7b3f3ea, 0xaf1450a2, 0x980d701a, 0xa805feae, 0x233e3199, 0x97f30b95, 0x4c4c5872, 0x9bb73a0b, 0x4c8d664c, 0x1fc20169, 0xe7a5d759, 0x7044b295, 0xd82380a6, 0x2a2e4100, 0x905545e6, 0x229460be, 0xe238fd3, 0xdc92a0ac, 0xe1fefd3c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Motion]:
    if property_count != 76:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(757))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72], dec[75], dec[78], dec[81], dec[84], dec[87], dec[90], dec[93], dec[96], dec[99], dec[102], dec[105], dec[108], dec[111], dec[114], dec[117], dec[120], dec[123], dec[126], dec[129], dec[132], dec[135], dec[138], dec[141], dec[144], dec[147], dec[150], dec[153], dec[156], dec[159], dec[162], dec[165], dec[168], dec[171], dec[174], dec[177], dec[180], dec[183], dec[186], dec[189], dec[192], dec[195], dec[198], dec[201], dec[204], dec[207], dec[210], dec[213], dec[216], dec[219], dec[222], dec[225]) != _FAST_IDS:
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


def _decode_unknown(data: typing.BinaryIO, property_size: int):
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
    0x9bb73a0b: ('unknown', _decode_unknown),
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
