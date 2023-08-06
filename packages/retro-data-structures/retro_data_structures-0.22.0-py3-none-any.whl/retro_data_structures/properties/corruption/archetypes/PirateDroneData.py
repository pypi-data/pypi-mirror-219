# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.FlyerMovementMode import FlyerMovementMode
from retro_data_structures.properties.corruption.archetypes.HyperModeData import HyperModeData
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.ScanBeamInfo import ScanBeamInfo


@dataclasses.dataclass()
class PirateDroneData(BaseProperty):
    unknown_0xdfd70ccc: bool = dataclasses.field(default=False)
    unknown_0x7e922362: bool = dataclasses.field(default=False)
    new_hyper_mode: HyperModeData = dataclasses.field(default_factory=HyperModeData)
    hyper_mode_data_0x37b432d6: HyperModeData = dataclasses.field(default_factory=HyperModeData)
    hyper_mode_data_0xae27b368: HyperModeData = dataclasses.field(default_factory=HyperModeData)
    flyer_movement_mode_0x4b1bc354: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    normal_shot_prediction: float = dataclasses.field(default=0.699999988079071)
    unknown_0x46353d93: bool = dataclasses.field(default=True)
    unknown_0x0b955d7d: float = dataclasses.field(default=5.0)
    unknown_0xedf5f29c: float = dataclasses.field(default=0.0)
    unknown_0xa75a9e68: float = dataclasses.field(default=5.0)
    unknown_0x413a3189: float = dataclasses.field(default=0.0)
    normal_projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    use_old_hyper_mode: bool = dataclasses.field(default=True)
    hyper_shot_prediction: float = dataclasses.field(default=0.5)
    hyper_projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    paint_target_projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    warning_projectile: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    unknown_0xc3680c31: bool = dataclasses.field(default=False)
    patrol: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    attack: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    cloak: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    hyper: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    cover: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x89a18334: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    avoidance_range: float = dataclasses.field(default=3.0)
    height_random_max: float = dataclasses.field(default=2.0)
    height_random_min: float = dataclasses.field(default=0.0)
    floor_buffer: float = dataclasses.field(default=1.0)
    ceiling_buffer: float = dataclasses.field(default=1.0)
    max_lerp: float = dataclasses.field(default=1080.0)
    patrol_speed: float = dataclasses.field(default=8.0)
    patrol_acceleration: float = dataclasses.field(default=1.0)
    attack_speed: float = dataclasses.field(default=10.0)
    attack_acceleration: float = dataclasses.field(default=2.0)
    cloak_speed: float = dataclasses.field(default=10.0)
    cloak_acceleration: float = dataclasses.field(default=1.0)
    hyper_speed: float = dataclasses.field(default=12.0)
    hyper_acceleration: float = dataclasses.field(default=3.0)
    cover_speed: float = dataclasses.field(default=10.0)
    cover_acceleration: float = dataclasses.field(default=15.0)
    side_scroller_speed: float = dataclasses.field(default=10.0)
    side_scroller_acceleration: float = dataclasses.field(default=15.0)
    can_strafe: bool = dataclasses.field(default=False)
    unknown_0x50e84e20: int = dataclasses.field(default=5)
    unknown_0x15ea0da2: int = dataclasses.field(default=3)
    add_damage_vulnerability: float = dataclasses.field(default=5.0)
    unknown_0x6bb44c6b: float = dataclasses.field(default=4.0)
    unknown_0x0fa5da72: float = dataclasses.field(default=0.30000001192092896)
    unknown_0xe9c57593: float = dataclasses.field(default=0.5)
    recheck_path_time: float = dataclasses.field(default=1.0)
    recheck_path_distance: float = dataclasses.field(default=5.0)
    path_finding_range: float = dataclasses.field(default=10.0)
    unknown_0x8cd7444d: bool = dataclasses.field(default=True)
    scan_delay: float = dataclasses.field(default=0.5)
    unknown_0x854e412d: bool = dataclasses.field(default=True)
    cloak_enabled: bool = dataclasses.field(default=True)
    cloak_time: float = dataclasses.field(default=0.5)
    unknown_0xda888721: float = dataclasses.field(default=0.10000000149011612)
    advanced_hyper_mode: bool = dataclasses.field(default=False)
    unknown_0x0b1b1def: float = dataclasses.field(default=90.0)
    unknown_0xed7bb20e: float = dataclasses.field(default=30.0)
    unknown_0xd2d94276: float = dataclasses.field(default=1.0)
    unknown_0x927ed6d8: int = dataclasses.field(default=0)
    unknown_0x96e4e7f2: int = dataclasses.field(default=1)
    unknown_0xa74ef708: int = dataclasses.field(default=0)
    unknown_0xe659c88e: int = dataclasses.field(default=2)
    unknown_0x10bbdfd1: float = dataclasses.field(default=3.0)
    unknown_0xe201a83d: float = dataclasses.field(default=10.0)
    scan_beam_info: ScanBeamInfo = dataclasses.field(default_factory=ScanBeamInfo)

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
        data.write(b'\x00F')  # 70 properties

        data.write(b'\xdf\xd7\x0c\xcc')  # 0xdfd70ccc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdfd70ccc))

        data.write(b'~\x92#b')  # 0x7e922362
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7e922362))

        data.write(b'M\x7f\x98R')  # 0x4d7f9852
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.new_hyper_mode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\xb42\xd6')  # 0x37b432d6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode_data_0x37b432d6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xae'\xb3h")  # 0xae27b368
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode_data_0xae27b368.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'K\x1b\xc3T')  # 0x4b1bc354
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x4b1bc354.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7@XM')  # 0xb740584d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_shot_prediction))

        data.write(b'F5=\x93')  # 0x46353d93
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x46353d93))

        data.write(b'\x0b\x95]}')  # 0xb955d7d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0b955d7d))

        data.write(b'\xed\xf5\xf2\x9c')  # 0xedf5f29c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xedf5f29c))

        data.write(b'\xa7Z\x9eh')  # 0xa75a9e68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa75a9e68))

        data.write(b'A:1\x89')  # 0x413a3189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x413a3189))

        data.write(b'\r\x1d\xc1(')  # 0xd1dc128
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3|\xdb\xad')  # 0xe37cdbad
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_old_hyper_mode))

        data.write(b'\x08\xdb4d')  # 0x8db3464
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_shot_prediction))

        data.write(b'|\x01\x8cl')  # 0x7c018c6c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6@\xcf#')  # 0xd640cf23
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.paint_target_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d,t\xa8')  # 0x1d2c74a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.warning_projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3h\x0c1')  # 0xc3680c31
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc3680c31))

        data.write(b'\xcc\xdd:\xca')  # 0xccdd3aca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patrol.to_stream(data)
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

        data.write(b'\xf9\xf1\xc1\xb1')  # 0xf9f1c1b1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cloak.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\x9cM+')  # 0x1c9c4d2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5]L\x94')  # 0xa55d4c94
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cover.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x89\xa1\x834')  # 0x89a18334
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x89a18334.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\xa9\xbd\r')  # 0x50a9bd0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.avoidance_range))

        data.write(b'I\xc3\x8a\xaf')  # 0x49c38aaf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height_random_max))

        data.write(b'\xaf\xa3%N')  # 0xafa3254e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height_random_min))

        data.write(b'e\x815\x8c')  # 0x6581358c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_buffer))

        data.write(b'\x11[\xb3\x8c')  # 0x115bb38c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ceiling_buffer))

        data.write(b'\x81\xdd8\x9d')  # 0x81dd389d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_lerp))

        data.write(b'v\\7\x15')  # 0x765c3715
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.patrol_speed))

        data.write(b'?\xec\x08[')  # 0x3fec085b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.patrol_acceleration))

        data.write(b'l\n+\xc8')  # 0x6c0a2bc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_speed))

        data.write(b'\t\x1b%\xae')  # 0x91b25ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_acceleration))

        data.write(b'\xc3\xe4\x1a\xaf')  # 0xc3e41aaf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_speed))

        data.write(b'\n\xc0\xf3 ')  # 0xac0f320
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_acceleration))

        data.write(b'\xba\xcb\\\x8e')  # 0xbacb5c8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_speed))

        data.write(b'\xef\xad\x7f\xba')  # 0xefad7fba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_acceleration))

        data.write(b'Z\xaaRw')  # 0x5aaa5277
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cover_speed))

        data.write(b'Vl~\x05')  # 0x566c7e05
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cover_acceleration))

        data.write(b'\xabg\xd3\x02')  # 0xab67d302
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.side_scroller_speed))

        data.write(b'\x12\x8f\x1b\\')  # 0x128f1b5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.side_scroller_acceleration))

        data.write(b'\x86\xfbZ\x9b')  # 0x86fb5a9b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_strafe))

        data.write(b'P\xe8N ')  # 0x50e84e20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x50e84e20))

        data.write(b'\x15\xea\r\xa2')  # 0x15ea0da2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x15ea0da2))

        data.write(b'\x8d\xd4\xe3\x8a')  # 0x8dd4e38a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.add_damage_vulnerability))

        data.write(b'k\xb4Lk')  # 0x6bb44c6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6bb44c6b))

        data.write(b'\x0f\xa5\xdar')  # 0xfa5da72
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0fa5da72))

        data.write(b'\xe9\xc5u\x93')  # 0xe9c57593
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe9c57593))

        data.write(b'\x9a\xa9\x0bk')  # 0x9aa90b6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_time))

        data.write(b'v&\xec\x89')  # 0x7626ec89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_distance))

        data.write(b'\x15\x08\xb0\xb1')  # 0x1508b0b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.path_finding_range))

        data.write(b'\x8c\xd7DM')  # 0x8cd7444d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8cd7444d))

        data.write(b"\x7f\xc8'\xa2")  # 0x7fc827a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_delay))

        data.write(b'\x85NA-')  # 0x854e412d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x854e412d))

        data.write(b'\xfej\xd9\x93')  # 0xfe6ad993
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.cloak_enabled))

        data.write(b'8\x8b\xc3\x1f')  # 0x388bc31f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_time))

        data.write(b'\xda\x88\x87!')  # 0xda888721
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xda888721))

        data.write(b'\xaf\xe2n\x84')  # 0xafe26e84
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.advanced_hyper_mode))

        data.write(b'\x0b\x1b\x1d\xef')  # 0xb1b1def
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0b1b1def))

        data.write(b'\xed{\xb2\x0e')  # 0xed7bb20e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed7bb20e))

        data.write(b'\xd2\xd9Bv')  # 0xd2d94276
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd2d94276))

        data.write(b'\x92~\xd6\xd8')  # 0x927ed6d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x927ed6d8))

        data.write(b'\x96\xe4\xe7\xf2')  # 0x96e4e7f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x96e4e7f2))

        data.write(b'\xa7N\xf7\x08')  # 0xa74ef708
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa74ef708))

        data.write(b'\xe6Y\xc8\x8e')  # 0xe659c88e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe659c88e))

        data.write(b'\x10\xbb\xdf\xd1')  # 0x10bbdfd1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x10bbdfd1))

        data.write(b'\xe2\x01\xa8=')  # 0xe201a83d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe201a83d))

        data.write(b'y\xf0dY')  # 0x79f06459
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_beam_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xdfd70ccc=data['unknown_0xdfd70ccc'],
            unknown_0x7e922362=data['unknown_0x7e922362'],
            new_hyper_mode=HyperModeData.from_json(data['new_hyper_mode']),
            hyper_mode_data_0x37b432d6=HyperModeData.from_json(data['hyper_mode_data_0x37b432d6']),
            hyper_mode_data_0xae27b368=HyperModeData.from_json(data['hyper_mode_data_0xae27b368']),
            flyer_movement_mode_0x4b1bc354=FlyerMovementMode.from_json(data['flyer_movement_mode_0x4b1bc354']),
            normal_shot_prediction=data['normal_shot_prediction'],
            unknown_0x46353d93=data['unknown_0x46353d93'],
            unknown_0x0b955d7d=data['unknown_0x0b955d7d'],
            unknown_0xedf5f29c=data['unknown_0xedf5f29c'],
            unknown_0xa75a9e68=data['unknown_0xa75a9e68'],
            unknown_0x413a3189=data['unknown_0x413a3189'],
            normal_projectile=LaunchProjectileData.from_json(data['normal_projectile']),
            use_old_hyper_mode=data['use_old_hyper_mode'],
            hyper_shot_prediction=data['hyper_shot_prediction'],
            hyper_projectile=LaunchProjectileData.from_json(data['hyper_projectile']),
            paint_target_projectile=LaunchProjectileData.from_json(data['paint_target_projectile']),
            warning_projectile=LaunchProjectileData.from_json(data['warning_projectile']),
            unknown_0xc3680c31=data['unknown_0xc3680c31'],
            patrol=FlyerMovementMode.from_json(data['patrol']),
            attack=FlyerMovementMode.from_json(data['attack']),
            cloak=FlyerMovementMode.from_json(data['cloak']),
            hyper=FlyerMovementMode.from_json(data['hyper']),
            cover=FlyerMovementMode.from_json(data['cover']),
            flyer_movement_mode_0x89a18334=FlyerMovementMode.from_json(data['flyer_movement_mode_0x89a18334']),
            avoidance_range=data['avoidance_range'],
            height_random_max=data['height_random_max'],
            height_random_min=data['height_random_min'],
            floor_buffer=data['floor_buffer'],
            ceiling_buffer=data['ceiling_buffer'],
            max_lerp=data['max_lerp'],
            patrol_speed=data['patrol_speed'],
            patrol_acceleration=data['patrol_acceleration'],
            attack_speed=data['attack_speed'],
            attack_acceleration=data['attack_acceleration'],
            cloak_speed=data['cloak_speed'],
            cloak_acceleration=data['cloak_acceleration'],
            hyper_speed=data['hyper_speed'],
            hyper_acceleration=data['hyper_acceleration'],
            cover_speed=data['cover_speed'],
            cover_acceleration=data['cover_acceleration'],
            side_scroller_speed=data['side_scroller_speed'],
            side_scroller_acceleration=data['side_scroller_acceleration'],
            can_strafe=data['can_strafe'],
            unknown_0x50e84e20=data['unknown_0x50e84e20'],
            unknown_0x15ea0da2=data['unknown_0x15ea0da2'],
            add_damage_vulnerability=data['add_damage_vulnerability'],
            unknown_0x6bb44c6b=data['unknown_0x6bb44c6b'],
            unknown_0x0fa5da72=data['unknown_0x0fa5da72'],
            unknown_0xe9c57593=data['unknown_0xe9c57593'],
            recheck_path_time=data['recheck_path_time'],
            recheck_path_distance=data['recheck_path_distance'],
            path_finding_range=data['path_finding_range'],
            unknown_0x8cd7444d=data['unknown_0x8cd7444d'],
            scan_delay=data['scan_delay'],
            unknown_0x854e412d=data['unknown_0x854e412d'],
            cloak_enabled=data['cloak_enabled'],
            cloak_time=data['cloak_time'],
            unknown_0xda888721=data['unknown_0xda888721'],
            advanced_hyper_mode=data['advanced_hyper_mode'],
            unknown_0x0b1b1def=data['unknown_0x0b1b1def'],
            unknown_0xed7bb20e=data['unknown_0xed7bb20e'],
            unknown_0xd2d94276=data['unknown_0xd2d94276'],
            unknown_0x927ed6d8=data['unknown_0x927ed6d8'],
            unknown_0x96e4e7f2=data['unknown_0x96e4e7f2'],
            unknown_0xa74ef708=data['unknown_0xa74ef708'],
            unknown_0xe659c88e=data['unknown_0xe659c88e'],
            unknown_0x10bbdfd1=data['unknown_0x10bbdfd1'],
            unknown_0xe201a83d=data['unknown_0xe201a83d'],
            scan_beam_info=ScanBeamInfo.from_json(data['scan_beam_info']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xdfd70ccc': self.unknown_0xdfd70ccc,
            'unknown_0x7e922362': self.unknown_0x7e922362,
            'new_hyper_mode': self.new_hyper_mode.to_json(),
            'hyper_mode_data_0x37b432d6': self.hyper_mode_data_0x37b432d6.to_json(),
            'hyper_mode_data_0xae27b368': self.hyper_mode_data_0xae27b368.to_json(),
            'flyer_movement_mode_0x4b1bc354': self.flyer_movement_mode_0x4b1bc354.to_json(),
            'normal_shot_prediction': self.normal_shot_prediction,
            'unknown_0x46353d93': self.unknown_0x46353d93,
            'unknown_0x0b955d7d': self.unknown_0x0b955d7d,
            'unknown_0xedf5f29c': self.unknown_0xedf5f29c,
            'unknown_0xa75a9e68': self.unknown_0xa75a9e68,
            'unknown_0x413a3189': self.unknown_0x413a3189,
            'normal_projectile': self.normal_projectile.to_json(),
            'use_old_hyper_mode': self.use_old_hyper_mode,
            'hyper_shot_prediction': self.hyper_shot_prediction,
            'hyper_projectile': self.hyper_projectile.to_json(),
            'paint_target_projectile': self.paint_target_projectile.to_json(),
            'warning_projectile': self.warning_projectile.to_json(),
            'unknown_0xc3680c31': self.unknown_0xc3680c31,
            'patrol': self.patrol.to_json(),
            'attack': self.attack.to_json(),
            'cloak': self.cloak.to_json(),
            'hyper': self.hyper.to_json(),
            'cover': self.cover.to_json(),
            'flyer_movement_mode_0x89a18334': self.flyer_movement_mode_0x89a18334.to_json(),
            'avoidance_range': self.avoidance_range,
            'height_random_max': self.height_random_max,
            'height_random_min': self.height_random_min,
            'floor_buffer': self.floor_buffer,
            'ceiling_buffer': self.ceiling_buffer,
            'max_lerp': self.max_lerp,
            'patrol_speed': self.patrol_speed,
            'patrol_acceleration': self.patrol_acceleration,
            'attack_speed': self.attack_speed,
            'attack_acceleration': self.attack_acceleration,
            'cloak_speed': self.cloak_speed,
            'cloak_acceleration': self.cloak_acceleration,
            'hyper_speed': self.hyper_speed,
            'hyper_acceleration': self.hyper_acceleration,
            'cover_speed': self.cover_speed,
            'cover_acceleration': self.cover_acceleration,
            'side_scroller_speed': self.side_scroller_speed,
            'side_scroller_acceleration': self.side_scroller_acceleration,
            'can_strafe': self.can_strafe,
            'unknown_0x50e84e20': self.unknown_0x50e84e20,
            'unknown_0x15ea0da2': self.unknown_0x15ea0da2,
            'add_damage_vulnerability': self.add_damage_vulnerability,
            'unknown_0x6bb44c6b': self.unknown_0x6bb44c6b,
            'unknown_0x0fa5da72': self.unknown_0x0fa5da72,
            'unknown_0xe9c57593': self.unknown_0xe9c57593,
            'recheck_path_time': self.recheck_path_time,
            'recheck_path_distance': self.recheck_path_distance,
            'path_finding_range': self.path_finding_range,
            'unknown_0x8cd7444d': self.unknown_0x8cd7444d,
            'scan_delay': self.scan_delay,
            'unknown_0x854e412d': self.unknown_0x854e412d,
            'cloak_enabled': self.cloak_enabled,
            'cloak_time': self.cloak_time,
            'unknown_0xda888721': self.unknown_0xda888721,
            'advanced_hyper_mode': self.advanced_hyper_mode,
            'unknown_0x0b1b1def': self.unknown_0x0b1b1def,
            'unknown_0xed7bb20e': self.unknown_0xed7bb20e,
            'unknown_0xd2d94276': self.unknown_0xd2d94276,
            'unknown_0x927ed6d8': self.unknown_0x927ed6d8,
            'unknown_0x96e4e7f2': self.unknown_0x96e4e7f2,
            'unknown_0xa74ef708': self.unknown_0xa74ef708,
            'unknown_0xe659c88e': self.unknown_0xe659c88e,
            'unknown_0x10bbdfd1': self.unknown_0x10bbdfd1,
            'unknown_0xe201a83d': self.unknown_0xe201a83d,
            'scan_beam_info': self.scan_beam_info.to_json(),
        }


def _decode_unknown_0xdfd70ccc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7e922362(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_new_hyper_mode(data: typing.BinaryIO, property_size: int):
    return HyperModeData.from_stream(data, property_size)


def _decode_hyper_mode_data_0x37b432d6(data: typing.BinaryIO, property_size: int):
    return HyperModeData.from_stream(data, property_size)


def _decode_hyper_mode_data_0xae27b368(data: typing.BinaryIO, property_size: int):
    return HyperModeData.from_stream(data, property_size)


def _decode_flyer_movement_mode_0x4b1bc354(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_normal_shot_prediction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x46353d93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0b955d7d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xedf5f29c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa75a9e68(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x413a3189(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_use_old_hyper_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_hyper_shot_prediction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_paint_target_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_warning_projectile(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_unknown_0xc3680c31(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_patrol(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_attack(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_cloak(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_hyper(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_cover(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_flyer_movement_mode_0x89a18334(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_avoidance_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height_random_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height_random_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ceiling_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_lerp(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cloak_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cloak_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cover_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cover_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_side_scroller_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_side_scroller_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_strafe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x50e84e20(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x15ea0da2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_add_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6bb44c6b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0fa5da72(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe9c57593(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_path_finding_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8cd7444d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scan_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x854e412d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_cloak_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_cloak_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xda888721(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_advanced_hyper_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0b1b1def(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed7bb20e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd2d94276(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x927ed6d8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x96e4e7f2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xa74ef708(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xe659c88e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x10bbdfd1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe201a83d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_beam_info(data: typing.BinaryIO, property_size: int):
    return ScanBeamInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdfd70ccc: ('unknown_0xdfd70ccc', _decode_unknown_0xdfd70ccc),
    0x7e922362: ('unknown_0x7e922362', _decode_unknown_0x7e922362),
    0x4d7f9852: ('new_hyper_mode', _decode_new_hyper_mode),
    0x37b432d6: ('hyper_mode_data_0x37b432d6', _decode_hyper_mode_data_0x37b432d6),
    0xae27b368: ('hyper_mode_data_0xae27b368', _decode_hyper_mode_data_0xae27b368),
    0x4b1bc354: ('flyer_movement_mode_0x4b1bc354', _decode_flyer_movement_mode_0x4b1bc354),
    0xb740584d: ('normal_shot_prediction', _decode_normal_shot_prediction),
    0x46353d93: ('unknown_0x46353d93', _decode_unknown_0x46353d93),
    0xb955d7d: ('unknown_0x0b955d7d', _decode_unknown_0x0b955d7d),
    0xedf5f29c: ('unknown_0xedf5f29c', _decode_unknown_0xedf5f29c),
    0xa75a9e68: ('unknown_0xa75a9e68', _decode_unknown_0xa75a9e68),
    0x413a3189: ('unknown_0x413a3189', _decode_unknown_0x413a3189),
    0xd1dc128: ('normal_projectile', _decode_normal_projectile),
    0xe37cdbad: ('use_old_hyper_mode', _decode_use_old_hyper_mode),
    0x8db3464: ('hyper_shot_prediction', _decode_hyper_shot_prediction),
    0x7c018c6c: ('hyper_projectile', _decode_hyper_projectile),
    0xd640cf23: ('paint_target_projectile', _decode_paint_target_projectile),
    0x1d2c74a8: ('warning_projectile', _decode_warning_projectile),
    0xc3680c31: ('unknown_0xc3680c31', _decode_unknown_0xc3680c31),
    0xccdd3aca: ('patrol', _decode_patrol),
    0xfa2a173f: ('attack', _decode_attack),
    0xf9f1c1b1: ('cloak', _decode_cloak),
    0x1c9c4d2b: ('hyper', _decode_hyper),
    0xa55d4c94: ('cover', _decode_cover),
    0x89a18334: ('flyer_movement_mode_0x89a18334', _decode_flyer_movement_mode_0x89a18334),
    0x50a9bd0d: ('avoidance_range', _decode_avoidance_range),
    0x49c38aaf: ('height_random_max', _decode_height_random_max),
    0xafa3254e: ('height_random_min', _decode_height_random_min),
    0x6581358c: ('floor_buffer', _decode_floor_buffer),
    0x115bb38c: ('ceiling_buffer', _decode_ceiling_buffer),
    0x81dd389d: ('max_lerp', _decode_max_lerp),
    0x765c3715: ('patrol_speed', _decode_patrol_speed),
    0x3fec085b: ('patrol_acceleration', _decode_patrol_acceleration),
    0x6c0a2bc8: ('attack_speed', _decode_attack_speed),
    0x91b25ae: ('attack_acceleration', _decode_attack_acceleration),
    0xc3e41aaf: ('cloak_speed', _decode_cloak_speed),
    0xac0f320: ('cloak_acceleration', _decode_cloak_acceleration),
    0xbacb5c8e: ('hyper_speed', _decode_hyper_speed),
    0xefad7fba: ('hyper_acceleration', _decode_hyper_acceleration),
    0x5aaa5277: ('cover_speed', _decode_cover_speed),
    0x566c7e05: ('cover_acceleration', _decode_cover_acceleration),
    0xab67d302: ('side_scroller_speed', _decode_side_scroller_speed),
    0x128f1b5c: ('side_scroller_acceleration', _decode_side_scroller_acceleration),
    0x86fb5a9b: ('can_strafe', _decode_can_strafe),
    0x50e84e20: ('unknown_0x50e84e20', _decode_unknown_0x50e84e20),
    0x15ea0da2: ('unknown_0x15ea0da2', _decode_unknown_0x15ea0da2),
    0x8dd4e38a: ('add_damage_vulnerability', _decode_add_damage_vulnerability),
    0x6bb44c6b: ('unknown_0x6bb44c6b', _decode_unknown_0x6bb44c6b),
    0xfa5da72: ('unknown_0x0fa5da72', _decode_unknown_0x0fa5da72),
    0xe9c57593: ('unknown_0xe9c57593', _decode_unknown_0xe9c57593),
    0x9aa90b6b: ('recheck_path_time', _decode_recheck_path_time),
    0x7626ec89: ('recheck_path_distance', _decode_recheck_path_distance),
    0x1508b0b1: ('path_finding_range', _decode_path_finding_range),
    0x8cd7444d: ('unknown_0x8cd7444d', _decode_unknown_0x8cd7444d),
    0x7fc827a2: ('scan_delay', _decode_scan_delay),
    0x854e412d: ('unknown_0x854e412d', _decode_unknown_0x854e412d),
    0xfe6ad993: ('cloak_enabled', _decode_cloak_enabled),
    0x388bc31f: ('cloak_time', _decode_cloak_time),
    0xda888721: ('unknown_0xda888721', _decode_unknown_0xda888721),
    0xafe26e84: ('advanced_hyper_mode', _decode_advanced_hyper_mode),
    0xb1b1def: ('unknown_0x0b1b1def', _decode_unknown_0x0b1b1def),
    0xed7bb20e: ('unknown_0xed7bb20e', _decode_unknown_0xed7bb20e),
    0xd2d94276: ('unknown_0xd2d94276', _decode_unknown_0xd2d94276),
    0x927ed6d8: ('unknown_0x927ed6d8', _decode_unknown_0x927ed6d8),
    0x96e4e7f2: ('unknown_0x96e4e7f2', _decode_unknown_0x96e4e7f2),
    0xa74ef708: ('unknown_0xa74ef708', _decode_unknown_0xa74ef708),
    0xe659c88e: ('unknown_0xe659c88e', _decode_unknown_0xe659c88e),
    0x10bbdfd1: ('unknown_0x10bbdfd1', _decode_unknown_0x10bbdfd1),
    0xe201a83d: ('unknown_0xe201a83d', _decode_unknown_0xe201a83d),
    0x79f06459: ('scan_beam_info', _decode_scan_beam_info),
}
