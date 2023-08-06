# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.KongGrabData import KongGrabData
from retro_data_structures.properties.dkc_returns.archetypes.KongGroundPoundData import KongGroundPoundData
from retro_data_structures.properties.dkc_returns.archetypes.KongRunningSlapData import KongRunningSlapData
from retro_data_structures.properties.dkc_returns.archetypes.KongSlideData import KongSlideData
from retro_data_structures.properties.dkc_returns.archetypes.KongStalledDescentData import KongStalledDescentData
from retro_data_structures.properties.dkc_returns.archetypes.KongSwingData import KongSwingData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAttachmentsData import PlayerAttachmentsData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerBarrelCannonData import PlayerBarrelCannonData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerBasicMovementData import PlayerBasicMovementData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerBopAnimThresholds import PlayerBopAnimThresholds
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCling2Data import PlayerCling2Data
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCommonData import PlayerCommonData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCrouchData import PlayerCrouchData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCrushData import PlayerCrushData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerFireReactionData import PlayerFireReactionData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerHeadTrackingData import PlayerHeadTrackingData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerJumpAnimWeights import PlayerJumpAnimWeights
from retro_data_structures.properties.dkc_returns.archetypes.PlayerJumpData import PlayerJumpData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMeleeData import PlayerMeleeData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountData import PlayerMountData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountRiderList import PlayerMountRiderList
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardData import PlayerMultiKillRewardData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerOffscreenIndicator import PlayerOffscreenIndicator
from retro_data_structures.properties.dkc_returns.archetypes.PlayerPeanutGunData import PlayerPeanutGunData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerPeriodicAdditiveAnimationData import PlayerPeriodicAdditiveAnimationData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerRiseFromTheGraveData import PlayerRiseFromTheGraveData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerShieldData import PlayerShieldData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerSlaveData import PlayerSlaveData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerSplineAdvancementData import PlayerSplineAdvancementData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTarInteractionData import PlayerTarInteractionData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTeleportData import PlayerTeleportData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTerrainAlignmentData import PlayerTerrainAlignmentData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTireInteractionData import PlayerTireInteractionData
from retro_data_structures.properties.dkc_returns.archetypes.RambiControllerData import RambiControllerData


@dataclasses.dataclass()
class KongData(BaseProperty):
    common: PlayerCommonData = dataclasses.field(default_factory=PlayerCommonData)
    basic_movement: PlayerBasicMovementData = dataclasses.field(default_factory=PlayerBasicMovementData)
    jump_data: PlayerJumpData = dataclasses.field(default_factory=PlayerJumpData)
    jump_animation_weights: PlayerJumpAnimWeights = dataclasses.field(default_factory=PlayerJumpAnimWeights)
    jump_bop_animation_thresholds: PlayerBopAnimThresholds = dataclasses.field(default_factory=PlayerBopAnimThresholds)
    spline_advancement: PlayerSplineAdvancementData = dataclasses.field(default_factory=PlayerSplineAdvancementData)
    rambi_controller_data: RambiControllerData = dataclasses.field(default_factory=RambiControllerData)
    attachments_data: PlayerAttachmentsData = dataclasses.field(default_factory=PlayerAttachmentsData)
    barrel_cannon_data: PlayerBarrelCannonData = dataclasses.field(default_factory=PlayerBarrelCannonData)
    cling2_data: PlayerCling2Data = dataclasses.field(default_factory=PlayerCling2Data)
    kong_ground_pound_data: KongGroundPoundData = dataclasses.field(default_factory=KongGroundPoundData)
    kong_cling_slap_data: KongGroundPoundData = dataclasses.field(default_factory=KongGroundPoundData)
    kong_running_slap_data: KongRunningSlapData = dataclasses.field(default_factory=KongRunningSlapData)
    kong_swing_data: KongSwingData = dataclasses.field(default_factory=KongSwingData)
    kong_slide_data: KongSlideData = dataclasses.field(default_factory=KongSlideData)
    kong_stalled_descent_data: KongStalledDescentData = dataclasses.field(default_factory=KongStalledDescentData)
    kong_grab_data: KongGrabData = dataclasses.field(default_factory=KongGrabData)
    head_tracking_data: PlayerHeadTrackingData = dataclasses.field(default_factory=PlayerHeadTrackingData)
    melee_data: PlayerMeleeData = dataclasses.field(default_factory=PlayerMeleeData)
    mount_data: PlayerMountData = dataclasses.field(default_factory=PlayerMountData)
    rider_list_data: PlayerMountRiderList = dataclasses.field(default_factory=PlayerMountRiderList)
    periodic_additive_animation_data: PlayerPeriodicAdditiveAnimationData = dataclasses.field(default_factory=PlayerPeriodicAdditiveAnimationData)
    slave_data: PlayerSlaveData = dataclasses.field(default_factory=PlayerSlaveData)
    offscreen_data: PlayerOffscreenIndicator = dataclasses.field(default_factory=PlayerOffscreenIndicator)
    tar_interaction_data: PlayerTarInteractionData = dataclasses.field(default_factory=PlayerTarInteractionData)
    teleport_data: PlayerTeleportData = dataclasses.field(default_factory=PlayerTeleportData)
    tire_interaction_data: PlayerTireInteractionData = dataclasses.field(default_factory=PlayerTireInteractionData)
    peanut_gun_data: PlayerPeanutGunData = dataclasses.field(default_factory=PlayerPeanutGunData)
    crouch_data: PlayerCrouchData = dataclasses.field(default_factory=PlayerCrouchData)
    fire_reaction: PlayerFireReactionData = dataclasses.field(default_factory=PlayerFireReactionData)
    crush_data: PlayerCrushData = dataclasses.field(default_factory=PlayerCrushData)
    multi_kill_reward_data: PlayerMultiKillRewardData = dataclasses.field(default_factory=PlayerMultiKillRewardData)
    rise_from_the_grave_data: PlayerRiseFromTheGraveData = dataclasses.field(default_factory=PlayerRiseFromTheGraveData)
    terrain_alignment_data: PlayerTerrainAlignmentData = dataclasses.field(default_factory=PlayerTerrainAlignmentData)
    shield_data: PlayerShieldData = dataclasses.field(default_factory=PlayerShieldData)

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
        data.write(b'\x00#')  # 35 properties

        data.write(b'<8I\x8d')  # 0x3c38498d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.common.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xb7\xe8\xb1')  # 0x7fb7e8b1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.basic_movement.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0{\xecm')  # 0xf07bec6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xd8\xdc\xb1')  # 0xf3d8dcb1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_animation_weights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\x11h\xac')  # 0x5e1168ac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_bop_animation_thresholds.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\x89\x05j')  # 0x5d89056a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline_advancement.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe02\x87\xae')  # 0xe03287ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rambi_controller_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9f\x1e\xf2\xf3')  # 0x9f1ef2f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachments_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xcase')  # 0xbbca7365
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.barrel_cannon_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xb1P\xfc')  # 0xf9b150fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cling2_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85oV\xa7')  # 0x856f56a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_ground_pound_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\xe9\x08\xd1')  # 0xf5e908d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_cling_slap_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6E1\x07')  # 0x36453107
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_running_slap_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\x87\x8aZ')  # 0xf7878a5a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_swing_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'`\xc4>\xaf')  # 0x60c43eaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_slide_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x814\xfc')  # 0xe38134fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_stalled_descent_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'uXl+')  # 0x75586c2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_grab_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Ml\x99\xeb')  # 0x4d6c99eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.head_tracking_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2\xb1SD')  # 0xf2b15344
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\x8e[\xd8')  # 0x978e5bd8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mount_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7fh\x14\x11')  # 0x7f681411
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider_list_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\x9d\xc5\n')  # 0x249dc50a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.periodic_additive_animation_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')\xc89\x97')  # 0x29c83997
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slave_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\xb2\x131')  # 0x74b21331
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offscreen_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3&\x0c\xa9')  # 0xc3260ca9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar_interaction_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x11|\xdd')  # 0xa7117cdd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.teleport_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x18\x14\xdb')  # 0xe31814db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tire_interaction_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88p\xd3\xdd')  # 0x8870d3dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.peanut_gun_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-q/\xbe')  # 0x2d712fbe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.crouch_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x1fBc')  # 0xfa1f4263
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fire_reaction.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8a\xbb%\xc4')  # 0x8abb25c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.crush_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xef\xc8c')  # 0x98efc863
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.multi_kill_reward_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9\xb0\xb0W')  # 0x39b0b057
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rise_from_the_grave_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\xd6v\x9f')  # 0x1bd6769f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.terrain_alignment_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\xd0\xa4I')  # 0xb2d0a449
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            common=PlayerCommonData.from_json(data['common']),
            basic_movement=PlayerBasicMovementData.from_json(data['basic_movement']),
            jump_data=PlayerJumpData.from_json(data['jump_data']),
            jump_animation_weights=PlayerJumpAnimWeights.from_json(data['jump_animation_weights']),
            jump_bop_animation_thresholds=PlayerBopAnimThresholds.from_json(data['jump_bop_animation_thresholds']),
            spline_advancement=PlayerSplineAdvancementData.from_json(data['spline_advancement']),
            rambi_controller_data=RambiControllerData.from_json(data['rambi_controller_data']),
            attachments_data=PlayerAttachmentsData.from_json(data['attachments_data']),
            barrel_cannon_data=PlayerBarrelCannonData.from_json(data['barrel_cannon_data']),
            cling2_data=PlayerCling2Data.from_json(data['cling2_data']),
            kong_ground_pound_data=KongGroundPoundData.from_json(data['kong_ground_pound_data']),
            kong_cling_slap_data=KongGroundPoundData.from_json(data['kong_cling_slap_data']),
            kong_running_slap_data=KongRunningSlapData.from_json(data['kong_running_slap_data']),
            kong_swing_data=KongSwingData.from_json(data['kong_swing_data']),
            kong_slide_data=KongSlideData.from_json(data['kong_slide_data']),
            kong_stalled_descent_data=KongStalledDescentData.from_json(data['kong_stalled_descent_data']),
            kong_grab_data=KongGrabData.from_json(data['kong_grab_data']),
            head_tracking_data=PlayerHeadTrackingData.from_json(data['head_tracking_data']),
            melee_data=PlayerMeleeData.from_json(data['melee_data']),
            mount_data=PlayerMountData.from_json(data['mount_data']),
            rider_list_data=PlayerMountRiderList.from_json(data['rider_list_data']),
            periodic_additive_animation_data=PlayerPeriodicAdditiveAnimationData.from_json(data['periodic_additive_animation_data']),
            slave_data=PlayerSlaveData.from_json(data['slave_data']),
            offscreen_data=PlayerOffscreenIndicator.from_json(data['offscreen_data']),
            tar_interaction_data=PlayerTarInteractionData.from_json(data['tar_interaction_data']),
            teleport_data=PlayerTeleportData.from_json(data['teleport_data']),
            tire_interaction_data=PlayerTireInteractionData.from_json(data['tire_interaction_data']),
            peanut_gun_data=PlayerPeanutGunData.from_json(data['peanut_gun_data']),
            crouch_data=PlayerCrouchData.from_json(data['crouch_data']),
            fire_reaction=PlayerFireReactionData.from_json(data['fire_reaction']),
            crush_data=PlayerCrushData.from_json(data['crush_data']),
            multi_kill_reward_data=PlayerMultiKillRewardData.from_json(data['multi_kill_reward_data']),
            rise_from_the_grave_data=PlayerRiseFromTheGraveData.from_json(data['rise_from_the_grave_data']),
            terrain_alignment_data=PlayerTerrainAlignmentData.from_json(data['terrain_alignment_data']),
            shield_data=PlayerShieldData.from_json(data['shield_data']),
        )

    def to_json(self) -> dict:
        return {
            'common': self.common.to_json(),
            'basic_movement': self.basic_movement.to_json(),
            'jump_data': self.jump_data.to_json(),
            'jump_animation_weights': self.jump_animation_weights.to_json(),
            'jump_bop_animation_thresholds': self.jump_bop_animation_thresholds.to_json(),
            'spline_advancement': self.spline_advancement.to_json(),
            'rambi_controller_data': self.rambi_controller_data.to_json(),
            'attachments_data': self.attachments_data.to_json(),
            'barrel_cannon_data': self.barrel_cannon_data.to_json(),
            'cling2_data': self.cling2_data.to_json(),
            'kong_ground_pound_data': self.kong_ground_pound_data.to_json(),
            'kong_cling_slap_data': self.kong_cling_slap_data.to_json(),
            'kong_running_slap_data': self.kong_running_slap_data.to_json(),
            'kong_swing_data': self.kong_swing_data.to_json(),
            'kong_slide_data': self.kong_slide_data.to_json(),
            'kong_stalled_descent_data': self.kong_stalled_descent_data.to_json(),
            'kong_grab_data': self.kong_grab_data.to_json(),
            'head_tracking_data': self.head_tracking_data.to_json(),
            'melee_data': self.melee_data.to_json(),
            'mount_data': self.mount_data.to_json(),
            'rider_list_data': self.rider_list_data.to_json(),
            'periodic_additive_animation_data': self.periodic_additive_animation_data.to_json(),
            'slave_data': self.slave_data.to_json(),
            'offscreen_data': self.offscreen_data.to_json(),
            'tar_interaction_data': self.tar_interaction_data.to_json(),
            'teleport_data': self.teleport_data.to_json(),
            'tire_interaction_data': self.tire_interaction_data.to_json(),
            'peanut_gun_data': self.peanut_gun_data.to_json(),
            'crouch_data': self.crouch_data.to_json(),
            'fire_reaction': self.fire_reaction.to_json(),
            'crush_data': self.crush_data.to_json(),
            'multi_kill_reward_data': self.multi_kill_reward_data.to_json(),
            'rise_from_the_grave_data': self.rise_from_the_grave_data.to_json(),
            'terrain_alignment_data': self.terrain_alignment_data.to_json(),
            'shield_data': self.shield_data.to_json(),
        }


def _decode_common(data: typing.BinaryIO, property_size: int):
    return PlayerCommonData.from_stream(data, property_size)


def _decode_basic_movement(data: typing.BinaryIO, property_size: int):
    return PlayerBasicMovementData.from_stream(data, property_size)


def _decode_jump_data(data: typing.BinaryIO, property_size: int):
    return PlayerJumpData.from_stream(data, property_size)


def _decode_jump_animation_weights(data: typing.BinaryIO, property_size: int):
    return PlayerJumpAnimWeights.from_stream(data, property_size)


def _decode_jump_bop_animation_thresholds(data: typing.BinaryIO, property_size: int):
    return PlayerBopAnimThresholds.from_stream(data, property_size)


def _decode_spline_advancement(data: typing.BinaryIO, property_size: int):
    return PlayerSplineAdvancementData.from_stream(data, property_size)


def _decode_rambi_controller_data(data: typing.BinaryIO, property_size: int):
    return RambiControllerData.from_stream(data, property_size)


def _decode_attachments_data(data: typing.BinaryIO, property_size: int):
    return PlayerAttachmentsData.from_stream(data, property_size)


def _decode_barrel_cannon_data(data: typing.BinaryIO, property_size: int):
    return PlayerBarrelCannonData.from_stream(data, property_size)


def _decode_cling2_data(data: typing.BinaryIO, property_size: int):
    return PlayerCling2Data.from_stream(data, property_size)


def _decode_kong_ground_pound_data(data: typing.BinaryIO, property_size: int):
    return KongGroundPoundData.from_stream(data, property_size)


def _decode_kong_cling_slap_data(data: typing.BinaryIO, property_size: int):
    return KongGroundPoundData.from_stream(data, property_size)


def _decode_kong_running_slap_data(data: typing.BinaryIO, property_size: int):
    return KongRunningSlapData.from_stream(data, property_size)


def _decode_kong_swing_data(data: typing.BinaryIO, property_size: int):
    return KongSwingData.from_stream(data, property_size)


def _decode_kong_slide_data(data: typing.BinaryIO, property_size: int):
    return KongSlideData.from_stream(data, property_size)


def _decode_kong_stalled_descent_data(data: typing.BinaryIO, property_size: int):
    return KongStalledDescentData.from_stream(data, property_size)


def _decode_kong_grab_data(data: typing.BinaryIO, property_size: int):
    return KongGrabData.from_stream(data, property_size)


def _decode_head_tracking_data(data: typing.BinaryIO, property_size: int):
    return PlayerHeadTrackingData.from_stream(data, property_size)


def _decode_melee_data(data: typing.BinaryIO, property_size: int):
    return PlayerMeleeData.from_stream(data, property_size)


def _decode_mount_data(data: typing.BinaryIO, property_size: int):
    return PlayerMountData.from_stream(data, property_size)


def _decode_rider_list_data(data: typing.BinaryIO, property_size: int):
    return PlayerMountRiderList.from_stream(data, property_size)


def _decode_periodic_additive_animation_data(data: typing.BinaryIO, property_size: int):
    return PlayerPeriodicAdditiveAnimationData.from_stream(data, property_size)


def _decode_slave_data(data: typing.BinaryIO, property_size: int):
    return PlayerSlaveData.from_stream(data, property_size)


def _decode_offscreen_data(data: typing.BinaryIO, property_size: int):
    return PlayerOffscreenIndicator.from_stream(data, property_size)


def _decode_tar_interaction_data(data: typing.BinaryIO, property_size: int):
    return PlayerTarInteractionData.from_stream(data, property_size)


def _decode_teleport_data(data: typing.BinaryIO, property_size: int):
    return PlayerTeleportData.from_stream(data, property_size)


def _decode_tire_interaction_data(data: typing.BinaryIO, property_size: int):
    return PlayerTireInteractionData.from_stream(data, property_size)


def _decode_peanut_gun_data(data: typing.BinaryIO, property_size: int):
    return PlayerPeanutGunData.from_stream(data, property_size)


def _decode_crouch_data(data: typing.BinaryIO, property_size: int):
    return PlayerCrouchData.from_stream(data, property_size)


def _decode_fire_reaction(data: typing.BinaryIO, property_size: int):
    return PlayerFireReactionData.from_stream(data, property_size)


def _decode_crush_data(data: typing.BinaryIO, property_size: int):
    return PlayerCrushData.from_stream(data, property_size)


def _decode_multi_kill_reward_data(data: typing.BinaryIO, property_size: int):
    return PlayerMultiKillRewardData.from_stream(data, property_size)


def _decode_rise_from_the_grave_data(data: typing.BinaryIO, property_size: int):
    return PlayerRiseFromTheGraveData.from_stream(data, property_size)


def _decode_terrain_alignment_data(data: typing.BinaryIO, property_size: int):
    return PlayerTerrainAlignmentData.from_stream(data, property_size)


def _decode_shield_data(data: typing.BinaryIO, property_size: int):
    return PlayerShieldData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3c38498d: ('common', _decode_common),
    0x7fb7e8b1: ('basic_movement', _decode_basic_movement),
    0xf07bec6d: ('jump_data', _decode_jump_data),
    0xf3d8dcb1: ('jump_animation_weights', _decode_jump_animation_weights),
    0x5e1168ac: ('jump_bop_animation_thresholds', _decode_jump_bop_animation_thresholds),
    0x5d89056a: ('spline_advancement', _decode_spline_advancement),
    0xe03287ae: ('rambi_controller_data', _decode_rambi_controller_data),
    0x9f1ef2f3: ('attachments_data', _decode_attachments_data),
    0xbbca7365: ('barrel_cannon_data', _decode_barrel_cannon_data),
    0xf9b150fc: ('cling2_data', _decode_cling2_data),
    0x856f56a7: ('kong_ground_pound_data', _decode_kong_ground_pound_data),
    0xf5e908d1: ('kong_cling_slap_data', _decode_kong_cling_slap_data),
    0x36453107: ('kong_running_slap_data', _decode_kong_running_slap_data),
    0xf7878a5a: ('kong_swing_data', _decode_kong_swing_data),
    0x60c43eaf: ('kong_slide_data', _decode_kong_slide_data),
    0xe38134fc: ('kong_stalled_descent_data', _decode_kong_stalled_descent_data),
    0x75586c2b: ('kong_grab_data', _decode_kong_grab_data),
    0x4d6c99eb: ('head_tracking_data', _decode_head_tracking_data),
    0xf2b15344: ('melee_data', _decode_melee_data),
    0x978e5bd8: ('mount_data', _decode_mount_data),
    0x7f681411: ('rider_list_data', _decode_rider_list_data),
    0x249dc50a: ('periodic_additive_animation_data', _decode_periodic_additive_animation_data),
    0x29c83997: ('slave_data', _decode_slave_data),
    0x74b21331: ('offscreen_data', _decode_offscreen_data),
    0xc3260ca9: ('tar_interaction_data', _decode_tar_interaction_data),
    0xa7117cdd: ('teleport_data', _decode_teleport_data),
    0xe31814db: ('tire_interaction_data', _decode_tire_interaction_data),
    0x8870d3dd: ('peanut_gun_data', _decode_peanut_gun_data),
    0x2d712fbe: ('crouch_data', _decode_crouch_data),
    0xfa1f4263: ('fire_reaction', _decode_fire_reaction),
    0x8abb25c4: ('crush_data', _decode_crush_data),
    0x98efc863: ('multi_kill_reward_data', _decode_multi_kill_reward_data),
    0x39b0b057: ('rise_from_the_grave_data', _decode_rise_from_the_grave_data),
    0x1bd6769f: ('terrain_alignment_data', _decode_terrain_alignment_data),
    0xb2d0a449: ('shield_data', _decode_shield_data),
}
