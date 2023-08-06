# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.ElectricBeamInfo import ElectricBeamInfo
from retro_data_structures.properties.corruption.archetypes.FlyerMovementMode import FlyerMovementMode
from retro_data_structures.properties.corruption.archetypes.MetroidPhazeoidStruct import MetroidPhazeoidStruct
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class MetroidPhazeoidData(BaseProperty):
    disable_player_grab: bool = dataclasses.field(default=False)
    disable_pirate_grab: bool = dataclasses.field(default=False)
    disable_hungry_mode: bool = dataclasses.field(default=False)
    post_hatch_scale: float = dataclasses.field(default=0.6600000262260437)
    unknown_0xef6d8c96: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x763e71ae: float = dataclasses.field(default=0.10000000149011612)
    recheck_path_time: float = dataclasses.field(default=1.0)
    recheck_path_distance: float = dataclasses.field(default=5.0)
    scan_delay: float = dataclasses.field(default=0.5)
    patrol: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    attack: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    hungry: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x7b6c604a: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x292754af: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    ball_lift: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    initial_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    hungry_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    ball_lift_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    phase_out_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    phase_out_radius_missile: float = dataclasses.field(default=5.0)
    metroid_phazeoid_struct_0x7c187bd0: MetroidPhazeoidStruct = dataclasses.field(default_factory=MetroidPhazeoidStruct)
    metroid_phazeoid_struct_0x0c7b243d: MetroidPhazeoidStruct = dataclasses.field(default_factory=MetroidPhazeoidStruct)
    metroid_phazeoid_struct_0x33b1809f: MetroidPhazeoidStruct = dataclasses.field(default_factory=MetroidPhazeoidStruct)
    metroid_phazeoid_struct_0x0ec6856a: MetroidPhazeoidStruct = dataclasses.field(default_factory=MetroidPhazeoidStruct)
    metroid_phazeoid_struct_0x61fab47a: MetroidPhazeoidStruct = dataclasses.field(default_factory=MetroidPhazeoidStruct)
    metroid_phazeoid_struct_0x26aac761: MetroidPhazeoidStruct = dataclasses.field(default_factory=MetroidPhazeoidStruct)
    brain_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    x_ray_brain_radius: float = dataclasses.field(default=1.0)
    normal_brain_radius: float = dataclasses.field(default=0.10000000149011612)
    phase_out_time_min: float = dataclasses.field(default=0.10000000149011612)
    phase_out_time_max: float = dataclasses.field(default=0.20000000298023224)
    phase_in_time_min: float = dataclasses.field(default=0.5)
    phase_in_time_max: float = dataclasses.field(default=1.0)
    phase_temple_disable_time_max: float = dataclasses.field(default=0.4000000059604645)
    phase_temple_disable_time_min: float = dataclasses.field(default=0.6000000238418579)
    unknown_0xa77f2fe5: float = dataclasses.field(default=0.5)
    unknown_0x411f8004: float = dataclasses.field(default=1.0)
    unknown_0xd14fc373: float = dataclasses.field(default=50.0)
    unknown_0x372f6c92: float = dataclasses.field(default=-50.0)
    ball_lift_slope_padding: float = dataclasses.field(default=25.0)
    unknown_0x900a62f6: float = dataclasses.field(default=5.0)
    arc_range_min: float = dataclasses.field(default=0.0)
    arc_range_max: float = dataclasses.field(default=15.0)
    unknown_0x9aab0b9a: float = dataclasses.field(default=5.0)
    unknown_0x7ccba47b: float = dataclasses.field(default=10.0)
    arc_attack: ElectricBeamInfo = dataclasses.field(default_factory=ElectricBeamInfo)
    unknown_0x0a8b169f: float = dataclasses.field(default=0.0)
    unknown_0xecebb97e: float = dataclasses.field(default=25.0)
    unknown_0x2b53dc0d: float = dataclasses.field(default=1.0)
    energy_drain: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x3af75fcc: float = dataclasses.field(default=15.0)
    max_static_intensity: float = dataclasses.field(default=0.5)
    ball_lift_delay_min: float = dataclasses.field(default=0.5)
    ball_lift_delay_max: float = dataclasses.field(default=1.0)
    unknown_0x283f2238: float = dataclasses.field(default=0.0)
    unknown_0xce5f8dd9: float = dataclasses.field(default=15.0)
    unknown_0x638d46ce: float = dataclasses.field(default=1.0)
    unknown_0x85ede92f: float = dataclasses.field(default=2.0)
    hungry_damage_threshold: float = dataclasses.field(default=0.0)
    unknown_0x677e48ea: bool = dataclasses.field(default=False)
    unknown_0x7edf931d: bool = dataclasses.field(default=False)
    unknown_0x15283674: bool = dataclasses.field(default=False)
    unknown_0x1ae10f78: float = dataclasses.field(default=3.0)
    unknown_0x93f9240c: float = dataclasses.field(default=10.0)
    phase_out_says_actions: float = dataclasses.field(default=5.0)
    max_says_actions: float = dataclasses.field(default=1.0)
    arc_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    arc_explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_arc_explosion: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    arc_number: int = dataclasses.field(default=5)
    arc_length: float = dataclasses.field(default=4.0)
    arc_move_time_max: float = dataclasses.field(default=0.10000000149011612)
    arc_move_time_min: float = dataclasses.field(default=0.020999999716877937)
    arc_on_time_max: float = dataclasses.field(default=0.10000000149011612)
    arc_on_time_min: float = dataclasses.field(default=0.020999999716877937)
    unknown_0x6dc77716: float = dataclasses.field(default=3.0)
    unknown_0x6fc4508c: float = dataclasses.field(default=-3.0)
    unknown_0x7de8da8d: float = dataclasses.field(default=1.0)
    unknown_0xf67dbaab: float = dataclasses.field(default=3.0)
    blur_radius: float = dataclasses.field(default=10.0)
    blur_duration: float = dataclasses.field(default=0.5)

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
        data.write(b'\x00Q')  # 81 properties

        data.write(b't(\x8e\xf3')  # 0x74288ef3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_player_grab))

        data.write(b'\x06y\xe2\x0c')  # 0x679e20c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_pirate_grab))

        data.write(b'\xaeF\xd8\x0e')  # 0xae46d80e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_hungry_mode))

        data.write(b'\xbdb\xd0.')  # 0xbd62d02e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.post_hatch_scale))

        data.write(b'\xefm\x8c\x96')  # 0xef6d8c96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xef6d8c96))

        data.write(b'v>q\xae')  # 0x763e71ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x763e71ae))

        data.write(b'\x9a\xa9\x0bk')  # 0x9aa90b6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_time))

        data.write(b'v&\xec\x89')  # 0x7626ec89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_distance))

        data.write(b"\x7f\xc8'\xa2")  # 0x7fc827a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_delay))

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

        data.write(b'\x97\xee\xd1\xf6')  # 0x97eed1f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hungry.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{l`J')  # 0x7b6c604a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x7b6c604a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b")'T\xaf")  # 0x292754af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x292754af.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18\xb5\x14:')  # 0x18b5143a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_lift.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xd0\xd4\r')  # 0xedd0d40d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.initial_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d~\x81\xd6')  # 0x8d7e81d6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hungry_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\x8e\xad\xc9')  # 0xf68eadc9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_lift_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdc\x02\r\xa7')  # 0xdc020da7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.phase_out_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa48\xa3\xcd')  # 0xa438a3cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_out_radius_missile))

        data.write(b'|\x18{\xd0')  # 0x7c187bd0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_phazeoid_struct_0x7c187bd0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c{$=')  # 0xc7b243d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_phazeoid_struct_0x0c7b243d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\xb1\x80\x9f')  # 0x33b1809f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_phazeoid_struct_0x33b1809f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0e\xc6\x85j')  # 0xec6856a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_phazeoid_struct_0x0ec6856a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\xfa\xb4z')  # 0x61fab47a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_phazeoid_struct_0x61fab47a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&\xaa\xc7a')  # 0x26aac761
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_phazeoid_struct_0x26aac761.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$:\xb1\r')  # 0x243ab10d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.brain_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\xc4\xac\x9c')  # 0x2dc4ac9c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.x_ray_brain_radius))

        data.write(b'|\xb7`\xa5')  # 0x7cb760a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_brain_radius))

        data.write(b'\x06\xa2\xbb\xb8')  # 0x6a2bbb8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_out_time_min))

        data.write(b'\xe0\xc2\x14Y')  # 0xe0c21459
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_out_time_max))

        data.write(b'TO\xa22')  # 0x544fa232
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_in_time_min))

        data.write(b'\xb2/\r\xd3')  # 0xb22f0dd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_in_time_max))

        data.write(b'\xac\xda\xcc\x80')  # 0xacdacc80
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_temple_disable_time_max))

        data.write(b'J\xbaca')  # 0x4aba6361
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_temple_disable_time_min))

        data.write(b'\xa7\x7f/\xe5')  # 0xa77f2fe5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa77f2fe5))

        data.write(b'A\x1f\x80\x04')  # 0x411f8004
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x411f8004))

        data.write(b'\xd1O\xc3s')  # 0xd14fc373
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd14fc373))

        data.write(b'7/l\x92')  # 0x372f6c92
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x372f6c92))

        data.write(b'\xf6}\x89\xb1')  # 0xf67d89b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_lift_slope_padding))

        data.write(b'\x90\nb\xf6')  # 0x900a62f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x900a62f6))

        data.write(b"\xa1\xb7\xcf'")  # 0xa1b7cf27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_range_min))

        data.write(b'G\xd7`\xc6')  # 0x47d760c6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_range_max))

        data.write(b'\x9a\xab\x0b\x9a')  # 0x9aab0b9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9aab0b9a))

        data.write(b'|\xcb\xa4{')  # 0x7ccba47b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7ccba47b))

        data.write(b'mA\x7fL')  # 0x6d417f4c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.arc_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\n\x8b\x16\x9f')  # 0xa8b169f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a8b169f))

        data.write(b'\xec\xeb\xb9~')  # 0xecebb97e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xecebb97e))

        data.write(b'+S\xdc\r')  # 0x2b53dc0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2b53dc0d))

        data.write(b'y\xcc\xc5\xb8')  # 0x79ccc5b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_drain.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':\xf7_\xcc')  # 0x3af75fcc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3af75fcc))

        data.write(b'\xe7\xb4\x92*')  # 0xe7b4922a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_static_intensity))

        data.write(b'OHB\xa3')  # 0x4f4842a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_lift_delay_min))

        data.write(b'\xa9(\xedB')  # 0xa928ed42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_lift_delay_max))

        data.write(b'(?"8')  # 0x283f2238
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x283f2238))

        data.write(b'\xce_\x8d\xd9')  # 0xce5f8dd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xce5f8dd9))

        data.write(b'c\x8dF\xce')  # 0x638d46ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x638d46ce))

        data.write(b'\x85\xed\xe9/')  # 0x85ede92f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x85ede92f))

        data.write(b'b\xfbG\xa5')  # 0x62fb47a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hungry_damage_threshold))

        data.write(b'g~H\xea')  # 0x677e48ea
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x677e48ea))

        data.write(b'~\xdf\x93\x1d')  # 0x7edf931d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7edf931d))

        data.write(b'\x15(6t')  # 0x15283674
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x15283674))

        data.write(b'\x1a\xe1\x0fx')  # 0x1ae10f78
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1ae10f78))

        data.write(b'\x93\xf9$\x0c')  # 0x93f9240c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x93f9240c))

        data.write(b'P\xb0y\xed')  # 0x50b079ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phase_out_says_actions))

        data.write(b'\xb1[A\xfa')  # 0xb15b41fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_says_actions))

        data.write(b'Ub\xc4\r')  # 0x5562c40d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.arc_effect))

        data.write(b'\x11\xf7Nq')  # 0x11f74e71
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.arc_explosion))

        data.write(b'5\t\xcd\xd9')  # 0x3509cdd9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_arc_explosion))

        data.write(b'\x95;\xc1\xd2')  # 0x953bc1d2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.arc_number))

        data.write(b'!\x82\x80\x87')  # 0x21828087
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_length))

        data.write(b'2\x8b>n')  # 0x328b3e6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_move_time_max))

        data.write(b'\xd4\xeb\x91\x8f')  # 0xd4eb918f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_move_time_min))

        data.write(b'U\xeb\xb8P')  # 0x55ebb850
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_on_time_max))

        data.write(b'\xb3\x8b\x17\xb1')  # 0xb38b17b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_on_time_min))

        data.write(b'm\xc7w\x16')  # 0x6dc77716
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6dc77716))

        data.write(b'o\xc4P\x8c')  # 0x6fc4508c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6fc4508c))

        data.write(b'}\xe8\xda\x8d')  # 0x7de8da8d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7de8da8d))

        data.write(b'\xf6}\xba\xab')  # 0xf67dbaab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf67dbaab))

        data.write(b'on\xb1\xf4')  # 0x6f6eb1f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.blur_radius))

        data.write(b'd\t\xed\xb3')  # 0x6409edb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.blur_duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            disable_player_grab=data['disable_player_grab'],
            disable_pirate_grab=data['disable_pirate_grab'],
            disable_hungry_mode=data['disable_hungry_mode'],
            post_hatch_scale=data['post_hatch_scale'],
            unknown_0xef6d8c96=data['unknown_0xef6d8c96'],
            unknown_0x763e71ae=data['unknown_0x763e71ae'],
            recheck_path_time=data['recheck_path_time'],
            recheck_path_distance=data['recheck_path_distance'],
            scan_delay=data['scan_delay'],
            patrol=FlyerMovementMode.from_json(data['patrol']),
            attack=FlyerMovementMode.from_json(data['attack']),
            hungry=FlyerMovementMode.from_json(data['hungry']),
            flyer_movement_mode_0x7b6c604a=FlyerMovementMode.from_json(data['flyer_movement_mode_0x7b6c604a']),
            flyer_movement_mode_0x292754af=FlyerMovementMode.from_json(data['flyer_movement_mode_0x292754af']),
            ball_lift=FlyerMovementMode.from_json(data['ball_lift']),
            initial_vulnerability=DamageVulnerability.from_json(data['initial_vulnerability']),
            hungry_vulnerability=DamageVulnerability.from_json(data['hungry_vulnerability']),
            ball_lift_vulnerability=DamageVulnerability.from_json(data['ball_lift_vulnerability']),
            phase_out_vulnerability=DamageVulnerability.from_json(data['phase_out_vulnerability']),
            phase_out_radius_missile=data['phase_out_radius_missile'],
            metroid_phazeoid_struct_0x7c187bd0=MetroidPhazeoidStruct.from_json(data['metroid_phazeoid_struct_0x7c187bd0']),
            metroid_phazeoid_struct_0x0c7b243d=MetroidPhazeoidStruct.from_json(data['metroid_phazeoid_struct_0x0c7b243d']),
            metroid_phazeoid_struct_0x33b1809f=MetroidPhazeoidStruct.from_json(data['metroid_phazeoid_struct_0x33b1809f']),
            metroid_phazeoid_struct_0x0ec6856a=MetroidPhazeoidStruct.from_json(data['metroid_phazeoid_struct_0x0ec6856a']),
            metroid_phazeoid_struct_0x61fab47a=MetroidPhazeoidStruct.from_json(data['metroid_phazeoid_struct_0x61fab47a']),
            metroid_phazeoid_struct_0x26aac761=MetroidPhazeoidStruct.from_json(data['metroid_phazeoid_struct_0x26aac761']),
            brain_vulnerability=DamageVulnerability.from_json(data['brain_vulnerability']),
            x_ray_brain_radius=data['x_ray_brain_radius'],
            normal_brain_radius=data['normal_brain_radius'],
            phase_out_time_min=data['phase_out_time_min'],
            phase_out_time_max=data['phase_out_time_max'],
            phase_in_time_min=data['phase_in_time_min'],
            phase_in_time_max=data['phase_in_time_max'],
            phase_temple_disable_time_max=data['phase_temple_disable_time_max'],
            phase_temple_disable_time_min=data['phase_temple_disable_time_min'],
            unknown_0xa77f2fe5=data['unknown_0xa77f2fe5'],
            unknown_0x411f8004=data['unknown_0x411f8004'],
            unknown_0xd14fc373=data['unknown_0xd14fc373'],
            unknown_0x372f6c92=data['unknown_0x372f6c92'],
            ball_lift_slope_padding=data['ball_lift_slope_padding'],
            unknown_0x900a62f6=data['unknown_0x900a62f6'],
            arc_range_min=data['arc_range_min'],
            arc_range_max=data['arc_range_max'],
            unknown_0x9aab0b9a=data['unknown_0x9aab0b9a'],
            unknown_0x7ccba47b=data['unknown_0x7ccba47b'],
            arc_attack=ElectricBeamInfo.from_json(data['arc_attack']),
            unknown_0x0a8b169f=data['unknown_0x0a8b169f'],
            unknown_0xecebb97e=data['unknown_0xecebb97e'],
            unknown_0x2b53dc0d=data['unknown_0x2b53dc0d'],
            energy_drain=Spline.from_json(data['energy_drain']),
            unknown_0x3af75fcc=data['unknown_0x3af75fcc'],
            max_static_intensity=data['max_static_intensity'],
            ball_lift_delay_min=data['ball_lift_delay_min'],
            ball_lift_delay_max=data['ball_lift_delay_max'],
            unknown_0x283f2238=data['unknown_0x283f2238'],
            unknown_0xce5f8dd9=data['unknown_0xce5f8dd9'],
            unknown_0x638d46ce=data['unknown_0x638d46ce'],
            unknown_0x85ede92f=data['unknown_0x85ede92f'],
            hungry_damage_threshold=data['hungry_damage_threshold'],
            unknown_0x677e48ea=data['unknown_0x677e48ea'],
            unknown_0x7edf931d=data['unknown_0x7edf931d'],
            unknown_0x15283674=data['unknown_0x15283674'],
            unknown_0x1ae10f78=data['unknown_0x1ae10f78'],
            unknown_0x93f9240c=data['unknown_0x93f9240c'],
            phase_out_says_actions=data['phase_out_says_actions'],
            max_says_actions=data['max_says_actions'],
            arc_effect=data['arc_effect'],
            arc_explosion=data['arc_explosion'],
            sound_arc_explosion=data['sound_arc_explosion'],
            arc_number=data['arc_number'],
            arc_length=data['arc_length'],
            arc_move_time_max=data['arc_move_time_max'],
            arc_move_time_min=data['arc_move_time_min'],
            arc_on_time_max=data['arc_on_time_max'],
            arc_on_time_min=data['arc_on_time_min'],
            unknown_0x6dc77716=data['unknown_0x6dc77716'],
            unknown_0x6fc4508c=data['unknown_0x6fc4508c'],
            unknown_0x7de8da8d=data['unknown_0x7de8da8d'],
            unknown_0xf67dbaab=data['unknown_0xf67dbaab'],
            blur_radius=data['blur_radius'],
            blur_duration=data['blur_duration'],
        )

    def to_json(self) -> dict:
        return {
            'disable_player_grab': self.disable_player_grab,
            'disable_pirate_grab': self.disable_pirate_grab,
            'disable_hungry_mode': self.disable_hungry_mode,
            'post_hatch_scale': self.post_hatch_scale,
            'unknown_0xef6d8c96': self.unknown_0xef6d8c96,
            'unknown_0x763e71ae': self.unknown_0x763e71ae,
            'recheck_path_time': self.recheck_path_time,
            'recheck_path_distance': self.recheck_path_distance,
            'scan_delay': self.scan_delay,
            'patrol': self.patrol.to_json(),
            'attack': self.attack.to_json(),
            'hungry': self.hungry.to_json(),
            'flyer_movement_mode_0x7b6c604a': self.flyer_movement_mode_0x7b6c604a.to_json(),
            'flyer_movement_mode_0x292754af': self.flyer_movement_mode_0x292754af.to_json(),
            'ball_lift': self.ball_lift.to_json(),
            'initial_vulnerability': self.initial_vulnerability.to_json(),
            'hungry_vulnerability': self.hungry_vulnerability.to_json(),
            'ball_lift_vulnerability': self.ball_lift_vulnerability.to_json(),
            'phase_out_vulnerability': self.phase_out_vulnerability.to_json(),
            'phase_out_radius_missile': self.phase_out_radius_missile,
            'metroid_phazeoid_struct_0x7c187bd0': self.metroid_phazeoid_struct_0x7c187bd0.to_json(),
            'metroid_phazeoid_struct_0x0c7b243d': self.metroid_phazeoid_struct_0x0c7b243d.to_json(),
            'metroid_phazeoid_struct_0x33b1809f': self.metroid_phazeoid_struct_0x33b1809f.to_json(),
            'metroid_phazeoid_struct_0x0ec6856a': self.metroid_phazeoid_struct_0x0ec6856a.to_json(),
            'metroid_phazeoid_struct_0x61fab47a': self.metroid_phazeoid_struct_0x61fab47a.to_json(),
            'metroid_phazeoid_struct_0x26aac761': self.metroid_phazeoid_struct_0x26aac761.to_json(),
            'brain_vulnerability': self.brain_vulnerability.to_json(),
            'x_ray_brain_radius': self.x_ray_brain_radius,
            'normal_brain_radius': self.normal_brain_radius,
            'phase_out_time_min': self.phase_out_time_min,
            'phase_out_time_max': self.phase_out_time_max,
            'phase_in_time_min': self.phase_in_time_min,
            'phase_in_time_max': self.phase_in_time_max,
            'phase_temple_disable_time_max': self.phase_temple_disable_time_max,
            'phase_temple_disable_time_min': self.phase_temple_disable_time_min,
            'unknown_0xa77f2fe5': self.unknown_0xa77f2fe5,
            'unknown_0x411f8004': self.unknown_0x411f8004,
            'unknown_0xd14fc373': self.unknown_0xd14fc373,
            'unknown_0x372f6c92': self.unknown_0x372f6c92,
            'ball_lift_slope_padding': self.ball_lift_slope_padding,
            'unknown_0x900a62f6': self.unknown_0x900a62f6,
            'arc_range_min': self.arc_range_min,
            'arc_range_max': self.arc_range_max,
            'unknown_0x9aab0b9a': self.unknown_0x9aab0b9a,
            'unknown_0x7ccba47b': self.unknown_0x7ccba47b,
            'arc_attack': self.arc_attack.to_json(),
            'unknown_0x0a8b169f': self.unknown_0x0a8b169f,
            'unknown_0xecebb97e': self.unknown_0xecebb97e,
            'unknown_0x2b53dc0d': self.unknown_0x2b53dc0d,
            'energy_drain': self.energy_drain.to_json(),
            'unknown_0x3af75fcc': self.unknown_0x3af75fcc,
            'max_static_intensity': self.max_static_intensity,
            'ball_lift_delay_min': self.ball_lift_delay_min,
            'ball_lift_delay_max': self.ball_lift_delay_max,
            'unknown_0x283f2238': self.unknown_0x283f2238,
            'unknown_0xce5f8dd9': self.unknown_0xce5f8dd9,
            'unknown_0x638d46ce': self.unknown_0x638d46ce,
            'unknown_0x85ede92f': self.unknown_0x85ede92f,
            'hungry_damage_threshold': self.hungry_damage_threshold,
            'unknown_0x677e48ea': self.unknown_0x677e48ea,
            'unknown_0x7edf931d': self.unknown_0x7edf931d,
            'unknown_0x15283674': self.unknown_0x15283674,
            'unknown_0x1ae10f78': self.unknown_0x1ae10f78,
            'unknown_0x93f9240c': self.unknown_0x93f9240c,
            'phase_out_says_actions': self.phase_out_says_actions,
            'max_says_actions': self.max_says_actions,
            'arc_effect': self.arc_effect,
            'arc_explosion': self.arc_explosion,
            'sound_arc_explosion': self.sound_arc_explosion,
            'arc_number': self.arc_number,
            'arc_length': self.arc_length,
            'arc_move_time_max': self.arc_move_time_max,
            'arc_move_time_min': self.arc_move_time_min,
            'arc_on_time_max': self.arc_on_time_max,
            'arc_on_time_min': self.arc_on_time_min,
            'unknown_0x6dc77716': self.unknown_0x6dc77716,
            'unknown_0x6fc4508c': self.unknown_0x6fc4508c,
            'unknown_0x7de8da8d': self.unknown_0x7de8da8d,
            'unknown_0xf67dbaab': self.unknown_0xf67dbaab,
            'blur_radius': self.blur_radius,
            'blur_duration': self.blur_duration,
        }


def _decode_disable_player_grab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_pirate_grab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_hungry_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_post_hatch_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xef6d8c96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x763e71ae(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_attack(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_hungry(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_flyer_movement_mode_0x7b6c604a(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_flyer_movement_mode_0x292754af(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_ball_lift(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size)


def _decode_initial_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_hungry_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_ball_lift_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_phase_out_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_phase_out_radius_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_metroid_phazeoid_struct_0x7c187bd0(data: typing.BinaryIO, property_size: int):
    return MetroidPhazeoidStruct.from_stream(data, property_size)


def _decode_metroid_phazeoid_struct_0x0c7b243d(data: typing.BinaryIO, property_size: int):
    return MetroidPhazeoidStruct.from_stream(data, property_size)


def _decode_metroid_phazeoid_struct_0x33b1809f(data: typing.BinaryIO, property_size: int):
    return MetroidPhazeoidStruct.from_stream(data, property_size)


def _decode_metroid_phazeoid_struct_0x0ec6856a(data: typing.BinaryIO, property_size: int):
    return MetroidPhazeoidStruct.from_stream(data, property_size)


def _decode_metroid_phazeoid_struct_0x61fab47a(data: typing.BinaryIO, property_size: int):
    return MetroidPhazeoidStruct.from_stream(data, property_size)


def _decode_metroid_phazeoid_struct_0x26aac761(data: typing.BinaryIO, property_size: int):
    return MetroidPhazeoidStruct.from_stream(data, property_size)


def _decode_brain_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_x_ray_brain_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_brain_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_out_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_out_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_in_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_in_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_temple_disable_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_temple_disable_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa77f2fe5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x411f8004(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd14fc373(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x372f6c92(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_lift_slope_padding(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x900a62f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_range_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_range_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9aab0b9a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7ccba47b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_attack(data: typing.BinaryIO, property_size: int):
    return ElectricBeamInfo.from_stream(data, property_size)


def _decode_unknown_0x0a8b169f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xecebb97e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2b53dc0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_drain(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x3af75fcc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_static_intensity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_lift_delay_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_lift_delay_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x283f2238(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xce5f8dd9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x638d46ce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x85ede92f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hungry_damage_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x677e48ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7edf931d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x15283674(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x1ae10f78(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x93f9240c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_out_says_actions(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_says_actions(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_arc_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_arc_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_arc_number(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_arc_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_move_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_move_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_on_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_on_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6dc77716(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6fc4508c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7de8da8d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf67dbaab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blur_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blur_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x74288ef3: ('disable_player_grab', _decode_disable_player_grab),
    0x679e20c: ('disable_pirate_grab', _decode_disable_pirate_grab),
    0xae46d80e: ('disable_hungry_mode', _decode_disable_hungry_mode),
    0xbd62d02e: ('post_hatch_scale', _decode_post_hatch_scale),
    0xef6d8c96: ('unknown_0xef6d8c96', _decode_unknown_0xef6d8c96),
    0x763e71ae: ('unknown_0x763e71ae', _decode_unknown_0x763e71ae),
    0x9aa90b6b: ('recheck_path_time', _decode_recheck_path_time),
    0x7626ec89: ('recheck_path_distance', _decode_recheck_path_distance),
    0x7fc827a2: ('scan_delay', _decode_scan_delay),
    0xccdd3aca: ('patrol', _decode_patrol),
    0xfa2a173f: ('attack', _decode_attack),
    0x97eed1f6: ('hungry', _decode_hungry),
    0x7b6c604a: ('flyer_movement_mode_0x7b6c604a', _decode_flyer_movement_mode_0x7b6c604a),
    0x292754af: ('flyer_movement_mode_0x292754af', _decode_flyer_movement_mode_0x292754af),
    0x18b5143a: ('ball_lift', _decode_ball_lift),
    0xedd0d40d: ('initial_vulnerability', _decode_initial_vulnerability),
    0x8d7e81d6: ('hungry_vulnerability', _decode_hungry_vulnerability),
    0xf68eadc9: ('ball_lift_vulnerability', _decode_ball_lift_vulnerability),
    0xdc020da7: ('phase_out_vulnerability', _decode_phase_out_vulnerability),
    0xa438a3cd: ('phase_out_radius_missile', _decode_phase_out_radius_missile),
    0x7c187bd0: ('metroid_phazeoid_struct_0x7c187bd0', _decode_metroid_phazeoid_struct_0x7c187bd0),
    0xc7b243d: ('metroid_phazeoid_struct_0x0c7b243d', _decode_metroid_phazeoid_struct_0x0c7b243d),
    0x33b1809f: ('metroid_phazeoid_struct_0x33b1809f', _decode_metroid_phazeoid_struct_0x33b1809f),
    0xec6856a: ('metroid_phazeoid_struct_0x0ec6856a', _decode_metroid_phazeoid_struct_0x0ec6856a),
    0x61fab47a: ('metroid_phazeoid_struct_0x61fab47a', _decode_metroid_phazeoid_struct_0x61fab47a),
    0x26aac761: ('metroid_phazeoid_struct_0x26aac761', _decode_metroid_phazeoid_struct_0x26aac761),
    0x243ab10d: ('brain_vulnerability', _decode_brain_vulnerability),
    0x2dc4ac9c: ('x_ray_brain_radius', _decode_x_ray_brain_radius),
    0x7cb760a5: ('normal_brain_radius', _decode_normal_brain_radius),
    0x6a2bbb8: ('phase_out_time_min', _decode_phase_out_time_min),
    0xe0c21459: ('phase_out_time_max', _decode_phase_out_time_max),
    0x544fa232: ('phase_in_time_min', _decode_phase_in_time_min),
    0xb22f0dd3: ('phase_in_time_max', _decode_phase_in_time_max),
    0xacdacc80: ('phase_temple_disable_time_max', _decode_phase_temple_disable_time_max),
    0x4aba6361: ('phase_temple_disable_time_min', _decode_phase_temple_disable_time_min),
    0xa77f2fe5: ('unknown_0xa77f2fe5', _decode_unknown_0xa77f2fe5),
    0x411f8004: ('unknown_0x411f8004', _decode_unknown_0x411f8004),
    0xd14fc373: ('unknown_0xd14fc373', _decode_unknown_0xd14fc373),
    0x372f6c92: ('unknown_0x372f6c92', _decode_unknown_0x372f6c92),
    0xf67d89b1: ('ball_lift_slope_padding', _decode_ball_lift_slope_padding),
    0x900a62f6: ('unknown_0x900a62f6', _decode_unknown_0x900a62f6),
    0xa1b7cf27: ('arc_range_min', _decode_arc_range_min),
    0x47d760c6: ('arc_range_max', _decode_arc_range_max),
    0x9aab0b9a: ('unknown_0x9aab0b9a', _decode_unknown_0x9aab0b9a),
    0x7ccba47b: ('unknown_0x7ccba47b', _decode_unknown_0x7ccba47b),
    0x6d417f4c: ('arc_attack', _decode_arc_attack),
    0xa8b169f: ('unknown_0x0a8b169f', _decode_unknown_0x0a8b169f),
    0xecebb97e: ('unknown_0xecebb97e', _decode_unknown_0xecebb97e),
    0x2b53dc0d: ('unknown_0x2b53dc0d', _decode_unknown_0x2b53dc0d),
    0x79ccc5b8: ('energy_drain', _decode_energy_drain),
    0x3af75fcc: ('unknown_0x3af75fcc', _decode_unknown_0x3af75fcc),
    0xe7b4922a: ('max_static_intensity', _decode_max_static_intensity),
    0x4f4842a3: ('ball_lift_delay_min', _decode_ball_lift_delay_min),
    0xa928ed42: ('ball_lift_delay_max', _decode_ball_lift_delay_max),
    0x283f2238: ('unknown_0x283f2238', _decode_unknown_0x283f2238),
    0xce5f8dd9: ('unknown_0xce5f8dd9', _decode_unknown_0xce5f8dd9),
    0x638d46ce: ('unknown_0x638d46ce', _decode_unknown_0x638d46ce),
    0x85ede92f: ('unknown_0x85ede92f', _decode_unknown_0x85ede92f),
    0x62fb47a5: ('hungry_damage_threshold', _decode_hungry_damage_threshold),
    0x677e48ea: ('unknown_0x677e48ea', _decode_unknown_0x677e48ea),
    0x7edf931d: ('unknown_0x7edf931d', _decode_unknown_0x7edf931d),
    0x15283674: ('unknown_0x15283674', _decode_unknown_0x15283674),
    0x1ae10f78: ('unknown_0x1ae10f78', _decode_unknown_0x1ae10f78),
    0x93f9240c: ('unknown_0x93f9240c', _decode_unknown_0x93f9240c),
    0x50b079ed: ('phase_out_says_actions', _decode_phase_out_says_actions),
    0xb15b41fa: ('max_says_actions', _decode_max_says_actions),
    0x5562c40d: ('arc_effect', _decode_arc_effect),
    0x11f74e71: ('arc_explosion', _decode_arc_explosion),
    0x3509cdd9: ('sound_arc_explosion', _decode_sound_arc_explosion),
    0x953bc1d2: ('arc_number', _decode_arc_number),
    0x21828087: ('arc_length', _decode_arc_length),
    0x328b3e6e: ('arc_move_time_max', _decode_arc_move_time_max),
    0xd4eb918f: ('arc_move_time_min', _decode_arc_move_time_min),
    0x55ebb850: ('arc_on_time_max', _decode_arc_on_time_max),
    0xb38b17b1: ('arc_on_time_min', _decode_arc_on_time_min),
    0x6dc77716: ('unknown_0x6dc77716', _decode_unknown_0x6dc77716),
    0x6fc4508c: ('unknown_0x6fc4508c', _decode_unknown_0x6fc4508c),
    0x7de8da8d: ('unknown_0x7de8da8d', _decode_unknown_0x7de8da8d),
    0xf67dbaab: ('unknown_0xf67dbaab', _decode_unknown_0xf67dbaab),
    0x6f6eb1f4: ('blur_radius', _decode_blur_radius),
    0x6409edb3: ('blur_duration', _decode_blur_duration),
}
