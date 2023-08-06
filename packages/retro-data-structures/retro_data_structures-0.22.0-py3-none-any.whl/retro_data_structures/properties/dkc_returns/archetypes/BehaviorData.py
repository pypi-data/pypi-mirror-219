# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.AdditiveTouchAttackBehaviorData import AdditiveTouchAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.AreaAttackBehaviorData import AreaAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.BopJumpBehaviorData import BopJumpBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.DamagedBehaviorData import DamagedBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.DrivenIntoGroundBehaviorData import DrivenIntoGroundBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FleeBehaviorData import FleeBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FollowPathControlBehaviorData import FollowPathControlBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FollowSurfaceBehaviorData import FollowSurfaceBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FollowWaypointsBehaviorData import FollowWaypointsBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.GrabPlayerBehaviorData import GrabPlayerBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.GrabbedBehaviorData import GrabbedBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.IdleBehaviorData import IdleBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.OneShotBehaviorData import OneShotBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileAttackBehaviorData import ProjectileAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileBehaviorData import ProjectileBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SeekerBehaviorData import SeekerBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SeparateAndReformBehaviorData import SeparateAndReformBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SlideBehaviorData import SlideBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SpawnBehaviorData import SpawnBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.StackableBlockBehaviorData import StackableBlockBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.StunnedByBopBehaviorData import StunnedByBopBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.StunnedByContactRuleData import StunnedByContactRuleData
from retro_data_structures.properties.dkc_returns.archetypes.StunnedByGroundPoundBehaviorData import StunnedByGroundPoundBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SwingLineBehaviorData import SwingLineBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SwoopBehaviorData import SwoopBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.TargetPlayerBehaviorData import TargetPlayerBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.TouchAttackBehaviorData import TouchAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct109 import UnknownStruct109
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct115 import UnknownStruct115
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct116 import UnknownStruct116
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct118 import UnknownStruct118
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct119 import UnknownStruct119
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct122 import UnknownStruct122
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct128 import UnknownStruct128
from retro_data_structures.properties.dkc_returns.archetypes.VerticalFlightBehaviorData import VerticalFlightBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.WanderBehaviorData import WanderBehaviorData


@dataclasses.dataclass()
class BehaviorData(BaseProperty):
    behavior_type: enums.BehaviorType = dataclasses.field(default=enums.BehaviorType.Unknown1)
    damaged: DamagedBehaviorData = dataclasses.field(default_factory=DamagedBehaviorData)
    stunned_by_ground_pound: StunnedByGroundPoundBehaviorData = dataclasses.field(default_factory=StunnedByGroundPoundBehaviorData)
    stunned_by_bop: StunnedByBopBehaviorData = dataclasses.field(default_factory=StunnedByBopBehaviorData)
    touch_attack: TouchAttackBehaviorData = dataclasses.field(default_factory=TouchAttackBehaviorData)
    projectile_attack: ProjectileAttackBehaviorData = dataclasses.field(default_factory=ProjectileAttackBehaviorData)
    follow_waypoints: FollowWaypointsBehaviorData = dataclasses.field(default_factory=FollowWaypointsBehaviorData)
    grabbed: GrabbedBehaviorData = dataclasses.field(default_factory=GrabbedBehaviorData)
    flee: FleeBehaviorData = dataclasses.field(default_factory=FleeBehaviorData)
    wander: WanderBehaviorData = dataclasses.field(default_factory=WanderBehaviorData)
    follow_surface: FollowSurfaceBehaviorData = dataclasses.field(default_factory=FollowSurfaceBehaviorData)
    bop_jump: BopJumpBehaviorData = dataclasses.field(default_factory=BopJumpBehaviorData)
    idle: IdleBehaviorData = dataclasses.field(default_factory=IdleBehaviorData)
    unknown_struct109: UnknownStruct109 = dataclasses.field(default_factory=UnknownStruct109)
    projectile: ProjectileBehaviorData = dataclasses.field(default_factory=ProjectileBehaviorData)
    vertical_flight: VerticalFlightBehaviorData = dataclasses.field(default_factory=VerticalFlightBehaviorData)
    stackable_block: StackableBlockBehaviorData = dataclasses.field(default_factory=StackableBlockBehaviorData)
    spawn: SpawnBehaviorData = dataclasses.field(default_factory=SpawnBehaviorData)
    swoop: SwoopBehaviorData = dataclasses.field(default_factory=SwoopBehaviorData)
    unknown_struct115: UnknownStruct115 = dataclasses.field(default_factory=UnknownStruct115)
    unknown_struct116: UnknownStruct116 = dataclasses.field(default_factory=UnknownStruct116)
    slide: SlideBehaviorData = dataclasses.field(default_factory=SlideBehaviorData)
    unknown_struct118: UnknownStruct118 = dataclasses.field(default_factory=UnknownStruct118)
    unknown_struct119: UnknownStruct119 = dataclasses.field(default_factory=UnknownStruct119)
    swing_line: SwingLineBehaviorData = dataclasses.field(default_factory=SwingLineBehaviorData)
    grab_player: GrabPlayerBehaviorData = dataclasses.field(default_factory=GrabPlayerBehaviorData)
    additive_touch_attack: AdditiveTouchAttackBehaviorData = dataclasses.field(default_factory=AdditiveTouchAttackBehaviorData)
    unknown_struct122: UnknownStruct122 = dataclasses.field(default_factory=UnknownStruct122)
    stunned_by_contact_rule: StunnedByContactRuleData = dataclasses.field(default_factory=StunnedByContactRuleData)
    driven_into_ground: DrivenIntoGroundBehaviorData = dataclasses.field(default_factory=DrivenIntoGroundBehaviorData)
    one_shot: OneShotBehaviorData = dataclasses.field(default_factory=OneShotBehaviorData)
    target_player: TargetPlayerBehaviorData = dataclasses.field(default_factory=TargetPlayerBehaviorData)
    unknown: DrivenIntoGroundBehaviorData = dataclasses.field(default_factory=DrivenIntoGroundBehaviorData)
    area_attack: AreaAttackBehaviorData = dataclasses.field(default_factory=AreaAttackBehaviorData)
    unknown_struct128: UnknownStruct128 = dataclasses.field(default_factory=UnknownStruct128)
    separate_and_reform: SeparateAndReformBehaviorData = dataclasses.field(default_factory=SeparateAndReformBehaviorData)
    additive_projectile_attack: ProjectileAttackBehaviorData = dataclasses.field(default_factory=ProjectileAttackBehaviorData)
    seeker: SeekerBehaviorData = dataclasses.field(default_factory=SeekerBehaviorData)
    follow_path_control: FollowPathControlBehaviorData = dataclasses.field(default_factory=FollowPathControlBehaviorData)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b"\x00'")  # 39 properties

        data.write(b'd\x03\xda\xed')  # 0x6403daed
        data.write(b'\x00\x04')  # size
        self.behavior_type.to_stream(data)

        data.write(b'\xd5\x11\x00P')  # 0xd5110050
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damaged.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x92r]')  # 0xa792725d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned_by_ground_pound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\xeaT\xaf')  # 0x33ea54af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned_by_bop.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\xf0\xd5H')  # 0x50f0d548
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.touch_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\xf1\x11\xb9')  # 0x3ff111b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm,\x07?')  # 0x6d2c073f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.follow_waypoints.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xffur')  # 0x24ff7572
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grabbed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x9f\xe4\xf9')  # 0x799fe4f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flee.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8cII\xcf')  # 0x8c4949cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.wander.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93D\xed\x81')  # 0x9344ed81
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.follow_surface.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7d\xa9\xd2')  # 0xf764a9d2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bop_jump.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\x97\xc5M')  # 0x1b97c54d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.idle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'JT\xcb\x95')  # 0x4a54cb95
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct109.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\xd0\xd0\x8a')  # 0x9bd0d08a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xech\x9eV')  # 0xec689e56
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vertical_flight.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab\xf0\xe7\xc3')  # 0xabf0e7c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stackable_block.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xe1P\xa1')  # 0xb3e150a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spawn.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x13\x9d\xb0')  # 0xe5139db0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swoop.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':Y%\xd6')  # 0x3a5925d6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct115.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdeD\rS')  # 0xde440d53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct116.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\x80\xd0:')  # 0x6c80d03a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe23\x13Z')  # 0xe233135a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct118.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\x99\xb8 ')  # 0x4699b820
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct119.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea,\x12\xf9')  # 0xea2c12f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swing_line.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\xdaj\xa8')  # 0x32da6aa8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grab_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9b\xcb\x9c')  # 0xc962cb9c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.additive_touch_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\x0fnS'")  # 0xf6e5327
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct122.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\xc2\xf5\xef')  # 0xe2c2f5ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned_by_contact_rule.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x92\xcc\xec')  # 0x5192ccec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.driven_into_ground.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf\xca\xde`')  # 0xafcade60
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.one_shot.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\x9ah\xa1')  # 0x749a68a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\xccoR')  # 0x2cc6f52
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x7f5a')  # 0xe37f3561
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1\xf0\x91\xb2')  # 0xa1f091b2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct128.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x068\xfc+')  # 0x638fc2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.separate_and_reform.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\x17Y\xa0')  # 0x311759a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.additive_projectile_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\xcej\x84')  # 0x5fce6a84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seeker.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\xd6nm')  # 0xeed66e6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.follow_path_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            behavior_type=enums.BehaviorType.from_json(data['behavior_type']),
            damaged=DamagedBehaviorData.from_json(data['damaged']),
            stunned_by_ground_pound=StunnedByGroundPoundBehaviorData.from_json(data['stunned_by_ground_pound']),
            stunned_by_bop=StunnedByBopBehaviorData.from_json(data['stunned_by_bop']),
            touch_attack=TouchAttackBehaviorData.from_json(data['touch_attack']),
            projectile_attack=ProjectileAttackBehaviorData.from_json(data['projectile_attack']),
            follow_waypoints=FollowWaypointsBehaviorData.from_json(data['follow_waypoints']),
            grabbed=GrabbedBehaviorData.from_json(data['grabbed']),
            flee=FleeBehaviorData.from_json(data['flee']),
            wander=WanderBehaviorData.from_json(data['wander']),
            follow_surface=FollowSurfaceBehaviorData.from_json(data['follow_surface']),
            bop_jump=BopJumpBehaviorData.from_json(data['bop_jump']),
            idle=IdleBehaviorData.from_json(data['idle']),
            unknown_struct109=UnknownStruct109.from_json(data['unknown_struct109']),
            projectile=ProjectileBehaviorData.from_json(data['projectile']),
            vertical_flight=VerticalFlightBehaviorData.from_json(data['vertical_flight']),
            stackable_block=StackableBlockBehaviorData.from_json(data['stackable_block']),
            spawn=SpawnBehaviorData.from_json(data['spawn']),
            swoop=SwoopBehaviorData.from_json(data['swoop']),
            unknown_struct115=UnknownStruct115.from_json(data['unknown_struct115']),
            unknown_struct116=UnknownStruct116.from_json(data['unknown_struct116']),
            slide=SlideBehaviorData.from_json(data['slide']),
            unknown_struct118=UnknownStruct118.from_json(data['unknown_struct118']),
            unknown_struct119=UnknownStruct119.from_json(data['unknown_struct119']),
            swing_line=SwingLineBehaviorData.from_json(data['swing_line']),
            grab_player=GrabPlayerBehaviorData.from_json(data['grab_player']),
            additive_touch_attack=AdditiveTouchAttackBehaviorData.from_json(data['additive_touch_attack']),
            unknown_struct122=UnknownStruct122.from_json(data['unknown_struct122']),
            stunned_by_contact_rule=StunnedByContactRuleData.from_json(data['stunned_by_contact_rule']),
            driven_into_ground=DrivenIntoGroundBehaviorData.from_json(data['driven_into_ground']),
            one_shot=OneShotBehaviorData.from_json(data['one_shot']),
            target_player=TargetPlayerBehaviorData.from_json(data['target_player']),
            unknown=DrivenIntoGroundBehaviorData.from_json(data['unknown']),
            area_attack=AreaAttackBehaviorData.from_json(data['area_attack']),
            unknown_struct128=UnknownStruct128.from_json(data['unknown_struct128']),
            separate_and_reform=SeparateAndReformBehaviorData.from_json(data['separate_and_reform']),
            additive_projectile_attack=ProjectileAttackBehaviorData.from_json(data['additive_projectile_attack']),
            seeker=SeekerBehaviorData.from_json(data['seeker']),
            follow_path_control=FollowPathControlBehaviorData.from_json(data['follow_path_control']),
        )

    def to_json(self) -> dict:
        return {
            'behavior_type': self.behavior_type.to_json(),
            'damaged': self.damaged.to_json(),
            'stunned_by_ground_pound': self.stunned_by_ground_pound.to_json(),
            'stunned_by_bop': self.stunned_by_bop.to_json(),
            'touch_attack': self.touch_attack.to_json(),
            'projectile_attack': self.projectile_attack.to_json(),
            'follow_waypoints': self.follow_waypoints.to_json(),
            'grabbed': self.grabbed.to_json(),
            'flee': self.flee.to_json(),
            'wander': self.wander.to_json(),
            'follow_surface': self.follow_surface.to_json(),
            'bop_jump': self.bop_jump.to_json(),
            'idle': self.idle.to_json(),
            'unknown_struct109': self.unknown_struct109.to_json(),
            'projectile': self.projectile.to_json(),
            'vertical_flight': self.vertical_flight.to_json(),
            'stackable_block': self.stackable_block.to_json(),
            'spawn': self.spawn.to_json(),
            'swoop': self.swoop.to_json(),
            'unknown_struct115': self.unknown_struct115.to_json(),
            'unknown_struct116': self.unknown_struct116.to_json(),
            'slide': self.slide.to_json(),
            'unknown_struct118': self.unknown_struct118.to_json(),
            'unknown_struct119': self.unknown_struct119.to_json(),
            'swing_line': self.swing_line.to_json(),
            'grab_player': self.grab_player.to_json(),
            'additive_touch_attack': self.additive_touch_attack.to_json(),
            'unknown_struct122': self.unknown_struct122.to_json(),
            'stunned_by_contact_rule': self.stunned_by_contact_rule.to_json(),
            'driven_into_ground': self.driven_into_ground.to_json(),
            'one_shot': self.one_shot.to_json(),
            'target_player': self.target_player.to_json(),
            'unknown': self.unknown.to_json(),
            'area_attack': self.area_attack.to_json(),
            'unknown_struct128': self.unknown_struct128.to_json(),
            'separate_and_reform': self.separate_and_reform.to_json(),
            'additive_projectile_attack': self.additive_projectile_attack.to_json(),
            'seeker': self.seeker.to_json(),
            'follow_path_control': self.follow_path_control.to_json(),
        }


def _decode_behavior_type(data: typing.BinaryIO, property_size: int):
    return enums.BehaviorType.from_stream(data)


def _decode_damaged(data: typing.BinaryIO, property_size: int):
    return DamagedBehaviorData.from_stream(data, property_size)


def _decode_stunned_by_ground_pound(data: typing.BinaryIO, property_size: int):
    return StunnedByGroundPoundBehaviorData.from_stream(data, property_size)


def _decode_stunned_by_bop(data: typing.BinaryIO, property_size: int):
    return StunnedByBopBehaviorData.from_stream(data, property_size)


def _decode_touch_attack(data: typing.BinaryIO, property_size: int):
    return TouchAttackBehaviorData.from_stream(data, property_size)


def _decode_projectile_attack(data: typing.BinaryIO, property_size: int):
    return ProjectileAttackBehaviorData.from_stream(data, property_size)


def _decode_follow_waypoints(data: typing.BinaryIO, property_size: int):
    return FollowWaypointsBehaviorData.from_stream(data, property_size)


def _decode_grabbed(data: typing.BinaryIO, property_size: int):
    return GrabbedBehaviorData.from_stream(data, property_size)


def _decode_flee(data: typing.BinaryIO, property_size: int):
    return FleeBehaviorData.from_stream(data, property_size)


def _decode_wander(data: typing.BinaryIO, property_size: int):
    return WanderBehaviorData.from_stream(data, property_size)


def _decode_follow_surface(data: typing.BinaryIO, property_size: int):
    return FollowSurfaceBehaviorData.from_stream(data, property_size)


def _decode_bop_jump(data: typing.BinaryIO, property_size: int):
    return BopJumpBehaviorData.from_stream(data, property_size)


def _decode_idle(data: typing.BinaryIO, property_size: int):
    return IdleBehaviorData.from_stream(data, property_size)


def _decode_unknown_struct109(data: typing.BinaryIO, property_size: int):
    return UnknownStruct109.from_stream(data, property_size)


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return ProjectileBehaviorData.from_stream(data, property_size)


def _decode_vertical_flight(data: typing.BinaryIO, property_size: int):
    return VerticalFlightBehaviorData.from_stream(data, property_size)


def _decode_stackable_block(data: typing.BinaryIO, property_size: int):
    return StackableBlockBehaviorData.from_stream(data, property_size)


def _decode_spawn(data: typing.BinaryIO, property_size: int):
    return SpawnBehaviorData.from_stream(data, property_size)


def _decode_swoop(data: typing.BinaryIO, property_size: int):
    return SwoopBehaviorData.from_stream(data, property_size)


def _decode_unknown_struct115(data: typing.BinaryIO, property_size: int):
    return UnknownStruct115.from_stream(data, property_size)


def _decode_unknown_struct116(data: typing.BinaryIO, property_size: int):
    return UnknownStruct116.from_stream(data, property_size)


def _decode_slide(data: typing.BinaryIO, property_size: int):
    return SlideBehaviorData.from_stream(data, property_size)


def _decode_unknown_struct118(data: typing.BinaryIO, property_size: int):
    return UnknownStruct118.from_stream(data, property_size)


def _decode_unknown_struct119(data: typing.BinaryIO, property_size: int):
    return UnknownStruct119.from_stream(data, property_size)


def _decode_swing_line(data: typing.BinaryIO, property_size: int):
    return SwingLineBehaviorData.from_stream(data, property_size)


def _decode_grab_player(data: typing.BinaryIO, property_size: int):
    return GrabPlayerBehaviorData.from_stream(data, property_size)


def _decode_additive_touch_attack(data: typing.BinaryIO, property_size: int):
    return AdditiveTouchAttackBehaviorData.from_stream(data, property_size)


def _decode_unknown_struct122(data: typing.BinaryIO, property_size: int):
    return UnknownStruct122.from_stream(data, property_size)


def _decode_stunned_by_contact_rule(data: typing.BinaryIO, property_size: int):
    return StunnedByContactRuleData.from_stream(data, property_size)


def _decode_driven_into_ground(data: typing.BinaryIO, property_size: int):
    return DrivenIntoGroundBehaviorData.from_stream(data, property_size)


def _decode_one_shot(data: typing.BinaryIO, property_size: int):
    return OneShotBehaviorData.from_stream(data, property_size)


def _decode_target_player(data: typing.BinaryIO, property_size: int):
    return TargetPlayerBehaviorData.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return DrivenIntoGroundBehaviorData.from_stream(data, property_size)


def _decode_area_attack(data: typing.BinaryIO, property_size: int):
    return AreaAttackBehaviorData.from_stream(data, property_size)


def _decode_unknown_struct128(data: typing.BinaryIO, property_size: int):
    return UnknownStruct128.from_stream(data, property_size)


def _decode_separate_and_reform(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformBehaviorData.from_stream(data, property_size)


def _decode_additive_projectile_attack(data: typing.BinaryIO, property_size: int):
    return ProjectileAttackBehaviorData.from_stream(data, property_size)


def _decode_seeker(data: typing.BinaryIO, property_size: int):
    return SeekerBehaviorData.from_stream(data, property_size)


def _decode_follow_path_control(data: typing.BinaryIO, property_size: int):
    return FollowPathControlBehaviorData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6403daed: ('behavior_type', _decode_behavior_type),
    0xd5110050: ('damaged', _decode_damaged),
    0xa792725d: ('stunned_by_ground_pound', _decode_stunned_by_ground_pound),
    0x33ea54af: ('stunned_by_bop', _decode_stunned_by_bop),
    0x50f0d548: ('touch_attack', _decode_touch_attack),
    0x3ff111b9: ('projectile_attack', _decode_projectile_attack),
    0x6d2c073f: ('follow_waypoints', _decode_follow_waypoints),
    0x24ff7572: ('grabbed', _decode_grabbed),
    0x799fe4f9: ('flee', _decode_flee),
    0x8c4949cf: ('wander', _decode_wander),
    0x9344ed81: ('follow_surface', _decode_follow_surface),
    0xf764a9d2: ('bop_jump', _decode_bop_jump),
    0x1b97c54d: ('idle', _decode_idle),
    0x4a54cb95: ('unknown_struct109', _decode_unknown_struct109),
    0x9bd0d08a: ('projectile', _decode_projectile),
    0xec689e56: ('vertical_flight', _decode_vertical_flight),
    0xabf0e7c3: ('stackable_block', _decode_stackable_block),
    0xb3e150a1: ('spawn', _decode_spawn),
    0xe5139db0: ('swoop', _decode_swoop),
    0x3a5925d6: ('unknown_struct115', _decode_unknown_struct115),
    0xde440d53: ('unknown_struct116', _decode_unknown_struct116),
    0x6c80d03a: ('slide', _decode_slide),
    0xe233135a: ('unknown_struct118', _decode_unknown_struct118),
    0x4699b820: ('unknown_struct119', _decode_unknown_struct119),
    0xea2c12f9: ('swing_line', _decode_swing_line),
    0x32da6aa8: ('grab_player', _decode_grab_player),
    0xc962cb9c: ('additive_touch_attack', _decode_additive_touch_attack),
    0xf6e5327: ('unknown_struct122', _decode_unknown_struct122),
    0xe2c2f5ef: ('stunned_by_contact_rule', _decode_stunned_by_contact_rule),
    0x5192ccec: ('driven_into_ground', _decode_driven_into_ground),
    0xafcade60: ('one_shot', _decode_one_shot),
    0x749a68a1: ('target_player', _decode_target_player),
    0x2cc6f52: ('unknown', _decode_unknown),
    0xe37f3561: ('area_attack', _decode_area_attack),
    0xa1f091b2: ('unknown_struct128', _decode_unknown_struct128),
    0x638fc2b: ('separate_and_reform', _decode_separate_and_reform),
    0x311759a0: ('additive_projectile_attack', _decode_additive_projectile_attack),
    0x5fce6a84: ('seeker', _decode_seeker),
    0xeed66e6d: ('follow_path_control', _decode_follow_path_control),
}
