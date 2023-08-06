# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class Misc(BaseProperty):
    unknown_0x8ed04c36: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x166c22e0: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xcec78e81: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x91338f72: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0d24ae6b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xddc561eb: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9be28150: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_memo_text_foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_memo_text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc8ddc662: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_glow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5c336f85: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdefca700: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    selected_visor_beam_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unselected_visor_beam_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_low_filled_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_low_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_low_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_damage_modulate_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    damage_indicator_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_title_foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_title_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe7070332: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x779c7b9c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x13bd3b64: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x1531edd3: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x27d0c234: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xbaa6d6a1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x59e416aa: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x92b8c50f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x142cb7a1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdf706404: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x81269ee0: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4a7a4d45: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xccee3feb: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x07b2ec4e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_warning_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_warning_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_warning_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x83040135: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x1adea12b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_bar_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_bar_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3c1ae0ff: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_bar_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_bar_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_group_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa6609cc5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xbe3c29a1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf4379cf4: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_group_inactive_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_group_inactive_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_group_combo_charge_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4c5aff4f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0b17b693: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xfad063d5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x2eafedf7: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_name_avoidance_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x8b0a4c90: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_warning_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_warning_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_warning_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x78522461: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    flash_pass_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x79ea6f12: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdc901206: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc54fa7bc: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x18717fa7: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x8b7d7378: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x867b01a2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x08be8347: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe6ec3c8d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x591cd695: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x26e1eb8c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x63e9e374: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x738d9c43: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xba6c75a2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc37d11b7: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xef1ec40e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0ca7beb2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x87d3ce8a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xeb7eb756: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    metroid_suck_pulse_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xce7c9d8d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_damage_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xafe2d45d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_holo_grid_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_seeker_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_seeker_ticks_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_seeker_ticks_outer_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_top_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_bottom_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_left_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_right_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_corner_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x51c5aad9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x60e8322b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa947a67c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x421bae2a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf0049167: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x76357179: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x439a3774: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x8ee94c81: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_download_square_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_dot_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x716e6398: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    steam_no_blur_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0f37e756: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf7283644: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x37564b7d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x66b7eda3: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf895098f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9b27be10: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x6c8550c9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5368a35f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5a807b81: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xeb63afed: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_panel_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x96f650c3: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_images_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xd3bafaf5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_group_damage_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4f1d443e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0f6451da: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc1ec3637: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xb6a61e34: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xfdcd9589: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xb0253266: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_seeker_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe8401c5a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x659147ae: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x43ed3310: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa781ed1d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x35402188: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x223058b5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe846d37f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    thermal_lock_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    log_book_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    inventory_equipped_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x02d5344f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf37f8deb: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5a6587df: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc18bdc67: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4d916bb8: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5ba76807: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa42f6495: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x448156ae: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x1a8b61b8: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf36adacb: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3aee673f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf9c88b05: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3bffe826: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x19e9738b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9329c6ff: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf9e7e0df: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x04e77411: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3c5d7111: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x42e2dfc1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc758541f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xde649e48: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5bf10430: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc01f5f88: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x7d2500d2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x14558146: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x949b0fff: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x74353dc4: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5ff96af1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x074bb42f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xaaf6e9a9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5e5b8c0a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xabe766b0: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x34f26028: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa59b3320: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xbfffe95a: int = dataclasses.field(default=5)
    unknown_0x0c3c55c9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf0c61af5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc87c1ff5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x88936aa2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xea4347bc: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\xb3')  # 179 properties

        data.write(b'\x8e\xd0L6')  # 0x8ed04c36
        data.write(b'\x00\x10')  # size
        self.unknown_0x8ed04c36.to_stream(data)

        data.write(b'\x16l"\xe0')  # 0x166c22e0
        data.write(b'\x00\x10')  # size
        self.unknown_0x166c22e0.to_stream(data)

        data.write(b'\xce\xc7\x8e\x81')  # 0xcec78e81
        data.write(b'\x00\x10')  # size
        self.unknown_0xcec78e81.to_stream(data)

        data.write(b'\x913\x8fr')  # 0x91338f72
        data.write(b'\x00\x10')  # size
        self.unknown_0x91338f72.to_stream(data)

        data.write(b'\r$\xaek')  # 0xd24ae6b
        data.write(b'\x00\x10')  # size
        self.unknown_0x0d24ae6b.to_stream(data)

        data.write(b'\xdd\xc5a\xeb')  # 0xddc561eb
        data.write(b'\x00\x10')  # size
        self.unknown_0xddc561eb.to_stream(data)

        data.write(b'\x9b\xe2\x81P')  # 0x9be28150
        data.write(b'\x00\x10')  # size
        self.unknown_0x9be28150.to_stream(data)

        data.write(b'-\xf1\xeb\x03')  # 0x2df1eb03
        data.write(b'\x00\x10')  # size
        self.hud_memo_text_foreground_color.to_stream(data)

        data.write(b'\xb5\xda0\xf4')  # 0xb5da30f4
        data.write(b'\x00\x10')  # size
        self.hud_memo_text_outline_color.to_stream(data)

        data.write(b'\xc8\xdd\xc6b')  # 0xc8ddc662
        data.write(b'\x00\x10')  # size
        self.unknown_0xc8ddc662.to_stream(data)

        data.write(b'i\x91\xe2\xcd')  # 0x6991e2cd
        data.write(b'\x00\x10')  # size
        self.hud_glow_color.to_stream(data)

        data.write(b'\\3o\x85')  # 0x5c336f85
        data.write(b'\x00\x10')  # size
        self.unknown_0x5c336f85.to_stream(data)

        data.write(b'\xde\xfc\xa7\x00')  # 0xdefca700
        data.write(b'\x00\x10')  # size
        self.unknown_0xdefca700.to_stream(data)

        data.write(b'\xcb}\xda\xf4')  # 0xcb7ddaf4
        data.write(b'\x00\x10')  # size
        self.selected_visor_beam_color.to_stream(data)

        data.write(b'\xf1y\x11\xaa')  # 0xf17911aa
        data.write(b'\x00\x10')  # size
        self.unselected_visor_beam_color.to_stream(data)

        data.write(b'\xa1L\x8d ')  # 0xa14c8d20
        data.write(b'\x00\x10')  # size
        self.energy_bar_low_filled_color.to_stream(data)

        data.write(b'\xb4\x13\\\xdd')  # 0xb4135cdd
        data.write(b'\x00\x10')  # size
        self.energy_bar_low_shadow_color.to_stream(data)

        data.write(b'\xe0)\x0cH')  # 0xe0290c48
        data.write(b'\x00\x10')  # size
        self.energy_bar_low_empty_color.to_stream(data)

        data.write(b'\x1e\xc7\xf8c')  # 0x1ec7f863
        data.write(b'\x00\x10')  # size
        self.hud_damage_modulate_color.to_stream(data)

        data.write(b'\xae\x13\x17\xd8')  # 0xae1317d8
        data.write(b'\x00\x10')  # size
        self.damage_indicator_color.to_stream(data)

        data.write(b'"\xb9\xb0\x1e')  # 0x22b9b01e
        data.write(b'\x00\x10')  # size
        self.hud_title_foreground_color.to_stream(data)

        data.write(b'p\xa2\xcdn')  # 0x70a2cd6e
        data.write(b'\x00\x10')  # size
        self.hud_title_outline_color.to_stream(data)

        data.write(b'\xe7\x07\x032')  # 0xe7070332
        data.write(b'\x00\x10')  # size
        self.unknown_0xe7070332.to_stream(data)

        data.write(b'w\x9c{\x9c')  # 0x779c7b9c
        data.write(b'\x00\x10')  # size
        self.unknown_0x779c7b9c.to_stream(data)

        data.write(b'\x13\xbd;d')  # 0x13bd3b64
        data.write(b'\x00\x10')  # size
        self.unknown_0x13bd3b64.to_stream(data)

        data.write(b'\x151\xed\xd3')  # 0x1531edd3
        data.write(b'\x00\x10')  # size
        self.unknown_0x1531edd3.to_stream(data)

        data.write(b"'\xd0\xc24")  # 0x27d0c234
        data.write(b'\x00\x10')  # size
        self.unknown_0x27d0c234.to_stream(data)

        data.write(b'\xba\xa6\xd6\xa1')  # 0xbaa6d6a1
        data.write(b'\x00\x10')  # size
        self.unknown_0xbaa6d6a1.to_stream(data)

        data.write(b'Y\xe4\x16\xaa')  # 0x59e416aa
        data.write(b'\x00\x10')  # size
        self.unknown_0x59e416aa.to_stream(data)

        data.write(b'\x92\xb8\xc5\x0f')  # 0x92b8c50f
        data.write(b'\x00\x10')  # size
        self.unknown_0x92b8c50f.to_stream(data)

        data.write(b'\x14,\xb7\xa1')  # 0x142cb7a1
        data.write(b'\x00\x10')  # size
        self.unknown_0x142cb7a1.to_stream(data)

        data.write(b'\xdfpd\x04')  # 0xdf706404
        data.write(b'\x00\x10')  # size
        self.unknown_0xdf706404.to_stream(data)

        data.write(b'\x81&\x9e\xe0')  # 0x81269ee0
        data.write(b'\x00\x10')  # size
        self.unknown_0x81269ee0.to_stream(data)

        data.write(b'JzME')  # 0x4a7a4d45
        data.write(b'\x00\x10')  # size
        self.unknown_0x4a7a4d45.to_stream(data)

        data.write(b'\xcc\xee?\xeb')  # 0xccee3feb
        data.write(b'\x00\x10')  # size
        self.unknown_0xccee3feb.to_stream(data)

        data.write(b'\x07\xb2\xecN')  # 0x7b2ec4e
        data.write(b'\x00\x10')  # size
        self.unknown_0x07b2ec4e.to_stream(data)

        data.write(b'on\x9dm')  # 0x6f6e9d6d
        data.write(b'\x00\x10')  # size
        self.energy_warning_color.to_stream(data)

        data.write(b'\xcah\xf6\x8f')  # 0xca68f68f
        data.write(b'\x00\x10')  # size
        self.threat_warning_color.to_stream(data)

        data.write(b'\x0c\x00\xa2\x9f')  # 0xc00a29f
        data.write(b'\x00\x10')  # size
        self.missile_warning_color.to_stream(data)

        data.write(b'\x83\x04\x015')  # 0x83040135
        data.write(b'\x00\x10')  # size
        self.unknown_0x83040135.to_stream(data)

        data.write(b'\x1a\xde\xa1+')  # 0x1adea12b
        data.write(b'\x00\x10')  # size
        self.unknown_0x1adea12b.to_stream(data)

        data.write(b'\x0f\x81p\xd6')  # 0xf8170d6
        data.write(b'\x00\x10')  # size
        self.threat_bar_shadow_color.to_stream(data)

        data.write(b'yB\x04\xfd')  # 0x794204fd
        data.write(b'\x00\x10')  # size
        self.threat_bar_empty_color.to_stream(data)

        data.write(b'<\x1a\xe0\xff')  # 0x3c1ae0ff
        data.write(b'\x00\x10')  # size
        self.unknown_0x3c1ae0ff.to_stream(data)

        data.write(b')E1\x02')  # 0x29453102
        data.write(b'\x00\x10')  # size
        self.missile_bar_shadow_color.to_stream(data)

        data.write(b'd3|\xcd')  # 0x64337ccd
        data.write(b'\x00\x10')  # size
        self.missile_bar_empty_color.to_stream(data)

        data.write(b'K\x86\xc59')  # 0x4b86c539
        data.write(b'\x00\x10')  # size
        self.threat_group_color.to_stream(data)

        data.write(b'\xa6`\x9c\xc5')  # 0xa6609cc5
        data.write(b'\x00\x10')  # size
        self.unknown_0xa6609cc5.to_stream(data)

        data.write(b'\xbe<)\xa1')  # 0xbe3c29a1
        data.write(b'\x00\x10')  # size
        self.unknown_0xbe3c29a1.to_stream(data)

        data.write(b'\xf47\x9c\xf4')  # 0xf4379cf4
        data.write(b'\x00\x10')  # size
        self.unknown_0xf4379cf4.to_stream(data)

        data.write(b't\xe5\xff\xa1')  # 0x74e5ffa1
        data.write(b'\x00\x10')  # size
        self.threat_group_inactive_color.to_stream(data)

        data.write(b'\xd1\x10\xa1/')  # 0xd110a12f
        data.write(b'\x00\x10')  # size
        self.missile_group_inactive_color.to_stream(data)

        data.write(b'\xce\xb1|\xdf')  # 0xceb17cdf
        data.write(b'\x00\x10')  # size
        self.missile_group_combo_charge_color.to_stream(data)

        data.write(b'LZ\xffO')  # 0x4c5aff4f
        data.write(b'\x00\x10')  # size
        self.unknown_0x4c5aff4f.to_stream(data)

        data.write(b'\x0b\x17\xb6\x93')  # 0xb17b693
        data.write(b'\x00\x10')  # size
        self.unknown_0x0b17b693.to_stream(data)

        data.write(b'\xfa\xd0c\xd5')  # 0xfad063d5
        data.write(b'\x00\x10')  # size
        self.unknown_0xfad063d5.to_stream(data)

        data.write(b'.\xaf\xed\xf7')  # 0x2eafedf7
        data.write(b'\x00\x10')  # size
        self.unknown_0x2eafedf7.to_stream(data)

        data.write(b'*\x01sO')  # 0x2a01734f
        data.write(b'\x00\x10')  # size
        self.energy_bar_name_avoidance_color.to_stream(data)

        data.write(b'\x8b\nL\x90')  # 0x8b0a4c90
        data.write(b'\x00\x10')  # size
        self.unknown_0x8b0a4c90.to_stream(data)

        data.write(b'\xc4\xe1|\xa8')  # 0xc4e17ca8
        data.write(b'\x00\x10')  # size
        self.energy_warning_outline_color.to_stream(data)

        data.write(b'\xc7\x18(\x98')  # 0xc7182898
        data.write(b'\x00\x10')  # size
        self.threat_warning_outline_color.to_stream(data)

        data.write(b'\xcd\xbds\xe1')  # 0xcdbd73e1
        data.write(b'\x00\x10')  # size
        self.missile_warning_outline_color.to_stream(data)

        data.write(b'xR$a')  # 0x78522461
        data.write(b'\x00\x10')  # size
        self.unknown_0x78522461.to_stream(data)

        data.write(b'j\x83\x9a\x97')  # 0x6a839a97
        data.write(b'\x00\x10')  # size
        self.flash_pass_color.to_stream(data)

        data.write(b'y\xeao\x12')  # 0x79ea6f12
        data.write(b'\x00\x10')  # size
        self.unknown_0x79ea6f12.to_stream(data)

        data.write(b'\xdc\x90\x12\x06')  # 0xdc901206
        data.write(b'\x00\x10')  # size
        self.unknown_0xdc901206.to_stream(data)

        data.write(b'\xc5O\xa7\xbc')  # 0xc54fa7bc
        data.write(b'\x00\x10')  # size
        self.unknown_0xc54fa7bc.to_stream(data)

        data.write(b'\x18q\x7f\xa7')  # 0x18717fa7
        data.write(b'\x00\x10')  # size
        self.unknown_0x18717fa7.to_stream(data)

        data.write(b'\x8b}sx')  # 0x8b7d7378
        data.write(b'\x00\x10')  # size
        self.unknown_0x8b7d7378.to_stream(data)

        data.write(b'\x86{\x01\xa2')  # 0x867b01a2
        data.write(b'\x00\x10')  # size
        self.unknown_0x867b01a2.to_stream(data)

        data.write(b'\x08\xbe\x83G')  # 0x8be8347
        data.write(b'\x00\x10')  # size
        self.unknown_0x08be8347.to_stream(data)

        data.write(b'\xe6\xec<\x8d')  # 0xe6ec3c8d
        data.write(b'\x00\x10')  # size
        self.unknown_0xe6ec3c8d.to_stream(data)

        data.write(b'Y\x1c\xd6\x95')  # 0x591cd695
        data.write(b'\x00\x10')  # size
        self.unknown_0x591cd695.to_stream(data)

        data.write(b'&\xe1\xeb\x8c')  # 0x26e1eb8c
        data.write(b'\x00\x10')  # size
        self.unknown_0x26e1eb8c.to_stream(data)

        data.write(b'c\xe9\xe3t')  # 0x63e9e374
        data.write(b'\x00\x10')  # size
        self.unknown_0x63e9e374.to_stream(data)

        data.write(b's\x8d\x9cC')  # 0x738d9c43
        data.write(b'\x00\x10')  # size
        self.unknown_0x738d9c43.to_stream(data)

        data.write(b'\xbalu\xa2')  # 0xba6c75a2
        data.write(b'\x00\x10')  # size
        self.unknown_0xba6c75a2.to_stream(data)

        data.write(b'\xc3}\x11\xb7')  # 0xc37d11b7
        data.write(b'\x00\x10')  # size
        self.unknown_0xc37d11b7.to_stream(data)

        data.write(b'\xef\x1e\xc4\x0e')  # 0xef1ec40e
        data.write(b'\x00\x10')  # size
        self.unknown_0xef1ec40e.to_stream(data)

        data.write(b'\x0c\xa7\xbe\xb2')  # 0xca7beb2
        data.write(b'\x00\x10')  # size
        self.unknown_0x0ca7beb2.to_stream(data)

        data.write(b'\x87\xd3\xce\x8a')  # 0x87d3ce8a
        data.write(b'\x00\x10')  # size
        self.unknown_0x87d3ce8a.to_stream(data)

        data.write(b'\xeb~\xb7V')  # 0xeb7eb756
        data.write(b'\x00\x10')  # size
        self.unknown_0xeb7eb756.to_stream(data)

        data.write(b'\xe4\xc1\xbb\xeb')  # 0xe4c1bbeb
        data.write(b'\x00\x10')  # size
        self.metroid_suck_pulse_color.to_stream(data)

        data.write(b'\xce|\x9d\x8d')  # 0xce7c9d8d
        data.write(b'\x00\x10')  # size
        self.unknown_0xce7c9d8d.to_stream(data)

        data.write(b'\x13I\x04 ')  # 0x13490420
        data.write(b'\x00\x10')  # size
        self.energy_bar_damage_color.to_stream(data)

        data.write(b'\xaf\xe2\xd4]')  # 0xafe2d45d
        data.write(b'\x00\x10')  # size
        self.unknown_0xafe2d45d.to_stream(data)

        data.write(b'*\xf5\xaa\x06')  # 0x2af5aa06
        data.write(b'\x00\x10')  # size
        self.x_ray_holo_grid_color.to_stream(data)

        data.write(b'\xd3\xcb\xe8F')  # 0xd3cbe846
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_color.to_stream(data)

        data.write(b'P{Q\xda')  # 0x507b51da
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_ticks_color.to_stream(data)

        data.write(b'\xc6\x1d\x97\xef')  # 0xc61d97ef
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_ticks_outer_color.to_stream(data)

        data.write(b'\xaf\x00\x01\xcf')  # 0xaf0001cf
        data.write(b'\x00\x10')  # size
        self.x_ray_top_puzzle_color.to_stream(data)

        data.write(b'\x15\n\x9b\x17')  # 0x150a9b17
        data.write(b'\x00\x10')  # size
        self.x_ray_bottom_puzzle_color.to_stream(data)

        data.write(b'\xd6mq_')  # 0xd66d715f
        data.write(b'\x00\x10')  # size
        self.x_ray_left_puzzle_color.to_stream(data)

        data.write(b'\xa8i\x8f\xe8')  # 0xa8698fe8
        data.write(b'\x00\x10')  # size
        self.x_ray_right_puzzle_color.to_stream(data)

        data.write(b'L\xb3\x8eq')  # 0x4cb38e71
        data.write(b'\x00\x10')  # size
        self.x_ray_corner_color.to_stream(data)

        data.write(b'Q\xc5\xaa\xd9')  # 0x51c5aad9
        data.write(b'\x00\x10')  # size
        self.unknown_0x51c5aad9.to_stream(data)

        data.write(b'`\xe82+')  # 0x60e8322b
        data.write(b'\x00\x10')  # size
        self.unknown_0x60e8322b.to_stream(data)

        data.write(b'\xa9G\xa6|')  # 0xa947a67c
        data.write(b'\x00\x10')  # size
        self.unknown_0xa947a67c.to_stream(data)

        data.write(b'B\x1b\xae*')  # 0x421bae2a
        data.write(b'\x00\x10')  # size
        self.unknown_0x421bae2a.to_stream(data)

        data.write(b'\xf0\x04\x91g')  # 0xf0049167
        data.write(b'\x00\x10')  # size
        self.unknown_0xf0049167.to_stream(data)

        data.write(b'v5qy')  # 0x76357179
        data.write(b'\x00\x10')  # size
        self.unknown_0x76357179.to_stream(data)

        data.write(b'C\x9a7t')  # 0x439a3774
        data.write(b'\x00\x10')  # size
        self.unknown_0x439a3774.to_stream(data)

        data.write(b'\x8e\xe9L\x81')  # 0x8ee94c81
        data.write(b'\x00\x10')  # size
        self.unknown_0x8ee94c81.to_stream(data)

        data.write(b'\xbb\x08\x97\xea')  # 0xbb0897ea
        data.write(b'\x00\x10')  # size
        self.scan_download_square_color.to_stream(data)

        data.write(b'\xc1,\xba\xb9')  # 0xc12cbab9
        data.write(b'\x00\x10')  # size
        self.scan_dot_color.to_stream(data)

        data.write(b'qnc\x98')  # 0x716e6398
        data.write(b'\x00\x10')  # size
        self.unknown_0x716e6398.to_stream(data)

        data.write(b'\xda\xcaF\xd4')  # 0xdaca46d4
        data.write(b'\x00\x10')  # size
        self.steam_no_blur_color.to_stream(data)

        data.write(b'\x0f7\xe7V')  # 0xf37e756
        data.write(b'\x00\x10')  # size
        self.unknown_0x0f37e756.to_stream(data)

        data.write(b'\xf7(6D')  # 0xf7283644
        data.write(b'\x00\x10')  # size
        self.unknown_0xf7283644.to_stream(data)

        data.write(b'7VK}')  # 0x37564b7d
        data.write(b'\x00\x10')  # size
        self.unknown_0x37564b7d.to_stream(data)

        data.write(b'f\xb7\xed\xa3')  # 0x66b7eda3
        data.write(b'\x00\x10')  # size
        self.unknown_0x66b7eda3.to_stream(data)

        data.write(b'\xf8\x95\t\x8f')  # 0xf895098f
        data.write(b'\x00\x10')  # size
        self.unknown_0xf895098f.to_stream(data)

        data.write(b"\x9b'\xbe\x10")  # 0x9b27be10
        data.write(b'\x00\x10')  # size
        self.unknown_0x9b27be10.to_stream(data)

        data.write(b'l\x85P\xc9')  # 0x6c8550c9
        data.write(b'\x00\x10')  # size
        self.unknown_0x6c8550c9.to_stream(data)

        data.write(b'Sh\xa3_')  # 0x5368a35f
        data.write(b'\x00\x10')  # size
        self.unknown_0x5368a35f.to_stream(data)

        data.write(b'Z\x80{\x81')  # 0x5a807b81
        data.write(b'\x00\x10')  # size
        self.unknown_0x5a807b81.to_stream(data)

        data.write(b'\xebc\xaf\xed')  # 0xeb63afed
        data.write(b'\x00\x10')  # size
        self.unknown_0xeb63afed.to_stream(data)

        data.write(b'\x92\xf5\x918')  # 0x92f59138
        data.write(b'\x00\x10')  # size
        self.scan_panel_color.to_stream(data)

        data.write(b'\x96\xf6P\xc3')  # 0x96f650c3
        data.write(b'\x00\x10')  # size
        self.unknown_0x96f650c3.to_stream(data)

        data.write(b'\xab\xdb\xfa[')  # 0xabdbfa5b
        data.write(b'\x00\x10')  # size
        self.scan_images_color.to_stream(data)

        data.write(b'\xd3\xba\xfa\xf5')  # 0xd3bafaf5
        data.write(b'\x00\x10')  # size
        self.unknown_0xd3bafaf5.to_stream(data)

        data.write(b'\xf8\xb9q\xfa')  # 0xf8b971fa
        data.write(b'\x00\x10')  # size
        self.threat_group_damage_color.to_stream(data)

        data.write(b'O\x1dD>')  # 0x4f1d443e
        data.write(b'\x00\x10')  # size
        self.unknown_0x4f1d443e.to_stream(data)

        data.write(b'\x0fdQ\xda')  # 0xf6451da
        data.write(b'\x00\x10')  # size
        self.unknown_0x0f6451da.to_stream(data)

        data.write(b'\xc1\xec67')  # 0xc1ec3637
        data.write(b'\x00\x10')  # size
        self.unknown_0xc1ec3637.to_stream(data)

        data.write(b'\xb6\xa6\x1e4')  # 0xb6a61e34
        data.write(b'\x00\x10')  # size
        self.unknown_0xb6a61e34.to_stream(data)

        data.write(b'\xfd\xcd\x95\x89')  # 0xfdcd9589
        data.write(b'\x00\x10')  # size
        self.unknown_0xfdcd9589.to_stream(data)

        data.write(b'\xb0%2f')  # 0xb0253266
        data.write(b'\x00\x10')  # size
        self.unknown_0xb0253266.to_stream(data)

        data.write(b'4^[N')  # 0x345e5b4e
        data.write(b'\x00\x10')  # size
        self.scan_seeker_color.to_stream(data)

        data.write(b'\xe8@\x1cZ')  # 0xe8401c5a
        data.write(b'\x00\x10')  # size
        self.unknown_0xe8401c5a.to_stream(data)

        data.write(b'e\x91G\xae')  # 0x659147ae
        data.write(b'\x00\x10')  # size
        self.unknown_0x659147ae.to_stream(data)

        data.write(b'C\xed3\x10')  # 0x43ed3310
        data.write(b'\x00\x10')  # size
        self.unknown_0x43ed3310.to_stream(data)

        data.write(b'\xa7\x81\xed\x1d')  # 0xa781ed1d
        data.write(b'\x00\x10')  # size
        self.unknown_0xa781ed1d.to_stream(data)

        data.write(b'5@!\x88')  # 0x35402188
        data.write(b'\x00\x10')  # size
        self.unknown_0x35402188.to_stream(data)

        data.write(b'"0X\xb5')  # 0x223058b5
        data.write(b'\x00\x10')  # size
        self.unknown_0x223058b5.to_stream(data)

        data.write(b'\xe8F\xd3\x7f')  # 0xe846d37f
        data.write(b'\x00\x10')  # size
        self.unknown_0xe846d37f.to_stream(data)

        data.write(b'\x8c\x9f*\x1a')  # 0x8c9f2a1a
        data.write(b'\x00\x10')  # size
        self.thermal_lock_color.to_stream(data)

        data.write(b'\x1b\x0f:\x85')  # 0x1b0f3a85
        data.write(b'\x00\x10')  # size
        self.log_book_color.to_stream(data)

        data.write(b'\x14\x93i\xfd')  # 0x149369fd
        data.write(b'\x00\x10')  # size
        self.inventory_equipped_color.to_stream(data)

        data.write(b'\x02\xd54O')  # 0x2d5344f
        data.write(b'\x00\x10')  # size
        self.unknown_0x02d5344f.to_stream(data)

        data.write(b'\xf3\x7f\x8d\xeb')  # 0xf37f8deb
        data.write(b'\x00\x10')  # size
        self.unknown_0xf37f8deb.to_stream(data)

        data.write(b'Ze\x87\xdf')  # 0x5a6587df
        data.write(b'\x00\x10')  # size
        self.unknown_0x5a6587df.to_stream(data)

        data.write(b'\xc1\x8b\xdcg')  # 0xc18bdc67
        data.write(b'\x00\x10')  # size
        self.unknown_0xc18bdc67.to_stream(data)

        data.write(b'M\x91k\xb8')  # 0x4d916bb8
        data.write(b'\x00\x10')  # size
        self.unknown_0x4d916bb8.to_stream(data)

        data.write(b'[\xa7h\x07')  # 0x5ba76807
        data.write(b'\x00\x10')  # size
        self.unknown_0x5ba76807.to_stream(data)

        data.write(b'\xa4/d\x95')  # 0xa42f6495
        data.write(b'\x00\x10')  # size
        self.unknown_0xa42f6495.to_stream(data)

        data.write(b'D\x81V\xae')  # 0x448156ae
        data.write(b'\x00\x10')  # size
        self.unknown_0x448156ae.to_stream(data)

        data.write(b'\x1a\x8ba\xb8')  # 0x1a8b61b8
        data.write(b'\x00\x10')  # size
        self.unknown_0x1a8b61b8.to_stream(data)

        data.write(b'\xf3j\xda\xcb')  # 0xf36adacb
        data.write(b'\x00\x10')  # size
        self.unknown_0xf36adacb.to_stream(data)

        data.write(b':\xeeg?')  # 0x3aee673f
        data.write(b'\x00\x10')  # size
        self.unknown_0x3aee673f.to_stream(data)

        data.write(b'\xf9\xc8\x8b\x05')  # 0xf9c88b05
        data.write(b'\x00\x10')  # size
        self.unknown_0xf9c88b05.to_stream(data)

        data.write(b';\xff\xe8&')  # 0x3bffe826
        data.write(b'\x00\x10')  # size
        self.unknown_0x3bffe826.to_stream(data)

        data.write(b'\x19\xe9s\x8b')  # 0x19e9738b
        data.write(b'\x00\x10')  # size
        self.unknown_0x19e9738b.to_stream(data)

        data.write(b'\x93)\xc6\xff')  # 0x9329c6ff
        data.write(b'\x00\x10')  # size
        self.unknown_0x9329c6ff.to_stream(data)

        data.write(b'\xf9\xe7\xe0\xdf')  # 0xf9e7e0df
        data.write(b'\x00\x10')  # size
        self.unknown_0xf9e7e0df.to_stream(data)

        data.write(b'\x04\xe7t\x11')  # 0x4e77411
        data.write(b'\x00\x10')  # size
        self.unknown_0x04e77411.to_stream(data)

        data.write(b'<]q\x11')  # 0x3c5d7111
        data.write(b'\x00\x10')  # size
        self.unknown_0x3c5d7111.to_stream(data)

        data.write(b'B\xe2\xdf\xc1')  # 0x42e2dfc1
        data.write(b'\x00\x10')  # size
        self.unknown_0x42e2dfc1.to_stream(data)

        data.write(b'\xc7XT\x1f')  # 0xc758541f
        data.write(b'\x00\x10')  # size
        self.unknown_0xc758541f.to_stream(data)

        data.write(b'\xded\x9eH')  # 0xde649e48
        data.write(b'\x00\x10')  # size
        self.unknown_0xde649e48.to_stream(data)

        data.write(b'[\xf1\x040')  # 0x5bf10430
        data.write(b'\x00\x10')  # size
        self.unknown_0x5bf10430.to_stream(data)

        data.write(b'\xc0\x1f_\x88')  # 0xc01f5f88
        data.write(b'\x00\x10')  # size
        self.unknown_0xc01f5f88.to_stream(data)

        data.write(b'}%\x00\xd2')  # 0x7d2500d2
        data.write(b'\x00\x10')  # size
        self.unknown_0x7d2500d2.to_stream(data)

        data.write(b'\x14U\x81F')  # 0x14558146
        data.write(b'\x00\x10')  # size
        self.unknown_0x14558146.to_stream(data)

        data.write(b'\x94\x9b\x0f\xff')  # 0x949b0fff
        data.write(b'\x00\x10')  # size
        self.unknown_0x949b0fff.to_stream(data)

        data.write(b't5=\xc4')  # 0x74353dc4
        data.write(b'\x00\x10')  # size
        self.unknown_0x74353dc4.to_stream(data)

        data.write(b'_\xf9j\xf1')  # 0x5ff96af1
        data.write(b'\x00\x10')  # size
        self.unknown_0x5ff96af1.to_stream(data)

        data.write(b'\x07K\xb4/')  # 0x74bb42f
        data.write(b'\x00\x10')  # size
        self.unknown_0x074bb42f.to_stream(data)

        data.write(b'\xaa\xf6\xe9\xa9')  # 0xaaf6e9a9
        data.write(b'\x00\x10')  # size
        self.unknown_0xaaf6e9a9.to_stream(data)

        data.write(b'^[\x8c\n')  # 0x5e5b8c0a
        data.write(b'\x00\x10')  # size
        self.unknown_0x5e5b8c0a.to_stream(data)

        data.write(b'\xab\xe7f\xb0')  # 0xabe766b0
        data.write(b'\x00\x10')  # size
        self.unknown_0xabe766b0.to_stream(data)

        data.write(b'4\xf2`(')  # 0x34f26028
        data.write(b'\x00\x10')  # size
        self.unknown_0x34f26028.to_stream(data)

        data.write(b'\xa5\x9b3 ')  # 0xa59b3320
        data.write(b'\x00\x10')  # size
        self.unknown_0xa59b3320.to_stream(data)

        data.write(b'\xbf\xff\xe9Z')  # 0xbfffe95a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbfffe95a))

        data.write(b'\x0c<U\xc9')  # 0xc3c55c9
        data.write(b'\x00\x10')  # size
        self.unknown_0x0c3c55c9.to_stream(data)

        data.write(b'\xf0\xc6\x1a\xf5')  # 0xf0c61af5
        data.write(b'\x00\x10')  # size
        self.unknown_0xf0c61af5.to_stream(data)

        data.write(b'\xc8|\x1f\xf5')  # 0xc87c1ff5
        data.write(b'\x00\x10')  # size
        self.unknown_0xc87c1ff5.to_stream(data)

        data.write(b'\x88\x93j\xa2')  # 0x88936aa2
        data.write(b'\x00\x10')  # size
        self.unknown_0x88936aa2.to_stream(data)

        data.write(b'\xeaCG\xbc')  # 0xea4347bc
        data.write(b'\x00\x10')  # size
        self.unknown_0xea4347bc.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x8ed04c36=Color.from_json(data['unknown_0x8ed04c36']),
            unknown_0x166c22e0=Color.from_json(data['unknown_0x166c22e0']),
            unknown_0xcec78e81=Color.from_json(data['unknown_0xcec78e81']),
            unknown_0x91338f72=Color.from_json(data['unknown_0x91338f72']),
            unknown_0x0d24ae6b=Color.from_json(data['unknown_0x0d24ae6b']),
            unknown_0xddc561eb=Color.from_json(data['unknown_0xddc561eb']),
            unknown_0x9be28150=Color.from_json(data['unknown_0x9be28150']),
            hud_memo_text_foreground_color=Color.from_json(data['hud_memo_text_foreground_color']),
            hud_memo_text_outline_color=Color.from_json(data['hud_memo_text_outline_color']),
            unknown_0xc8ddc662=Color.from_json(data['unknown_0xc8ddc662']),
            hud_glow_color=Color.from_json(data['hud_glow_color']),
            unknown_0x5c336f85=Color.from_json(data['unknown_0x5c336f85']),
            unknown_0xdefca700=Color.from_json(data['unknown_0xdefca700']),
            selected_visor_beam_color=Color.from_json(data['selected_visor_beam_color']),
            unselected_visor_beam_color=Color.from_json(data['unselected_visor_beam_color']),
            energy_bar_low_filled_color=Color.from_json(data['energy_bar_low_filled_color']),
            energy_bar_low_shadow_color=Color.from_json(data['energy_bar_low_shadow_color']),
            energy_bar_low_empty_color=Color.from_json(data['energy_bar_low_empty_color']),
            hud_damage_modulate_color=Color.from_json(data['hud_damage_modulate_color']),
            damage_indicator_color=Color.from_json(data['damage_indicator_color']),
            hud_title_foreground_color=Color.from_json(data['hud_title_foreground_color']),
            hud_title_outline_color=Color.from_json(data['hud_title_outline_color']),
            unknown_0xe7070332=Color.from_json(data['unknown_0xe7070332']),
            unknown_0x779c7b9c=Color.from_json(data['unknown_0x779c7b9c']),
            unknown_0x13bd3b64=Color.from_json(data['unknown_0x13bd3b64']),
            unknown_0x1531edd3=Color.from_json(data['unknown_0x1531edd3']),
            unknown_0x27d0c234=Color.from_json(data['unknown_0x27d0c234']),
            unknown_0xbaa6d6a1=Color.from_json(data['unknown_0xbaa6d6a1']),
            unknown_0x59e416aa=Color.from_json(data['unknown_0x59e416aa']),
            unknown_0x92b8c50f=Color.from_json(data['unknown_0x92b8c50f']),
            unknown_0x142cb7a1=Color.from_json(data['unknown_0x142cb7a1']),
            unknown_0xdf706404=Color.from_json(data['unknown_0xdf706404']),
            unknown_0x81269ee0=Color.from_json(data['unknown_0x81269ee0']),
            unknown_0x4a7a4d45=Color.from_json(data['unknown_0x4a7a4d45']),
            unknown_0xccee3feb=Color.from_json(data['unknown_0xccee3feb']),
            unknown_0x07b2ec4e=Color.from_json(data['unknown_0x07b2ec4e']),
            energy_warning_color=Color.from_json(data['energy_warning_color']),
            threat_warning_color=Color.from_json(data['threat_warning_color']),
            missile_warning_color=Color.from_json(data['missile_warning_color']),
            unknown_0x83040135=Color.from_json(data['unknown_0x83040135']),
            unknown_0x1adea12b=Color.from_json(data['unknown_0x1adea12b']),
            threat_bar_shadow_color=Color.from_json(data['threat_bar_shadow_color']),
            threat_bar_empty_color=Color.from_json(data['threat_bar_empty_color']),
            unknown_0x3c1ae0ff=Color.from_json(data['unknown_0x3c1ae0ff']),
            missile_bar_shadow_color=Color.from_json(data['missile_bar_shadow_color']),
            missile_bar_empty_color=Color.from_json(data['missile_bar_empty_color']),
            threat_group_color=Color.from_json(data['threat_group_color']),
            unknown_0xa6609cc5=Color.from_json(data['unknown_0xa6609cc5']),
            unknown_0xbe3c29a1=Color.from_json(data['unknown_0xbe3c29a1']),
            unknown_0xf4379cf4=Color.from_json(data['unknown_0xf4379cf4']),
            threat_group_inactive_color=Color.from_json(data['threat_group_inactive_color']),
            missile_group_inactive_color=Color.from_json(data['missile_group_inactive_color']),
            missile_group_combo_charge_color=Color.from_json(data['missile_group_combo_charge_color']),
            unknown_0x4c5aff4f=Color.from_json(data['unknown_0x4c5aff4f']),
            unknown_0x0b17b693=Color.from_json(data['unknown_0x0b17b693']),
            unknown_0xfad063d5=Color.from_json(data['unknown_0xfad063d5']),
            unknown_0x2eafedf7=Color.from_json(data['unknown_0x2eafedf7']),
            energy_bar_name_avoidance_color=Color.from_json(data['energy_bar_name_avoidance_color']),
            unknown_0x8b0a4c90=Color.from_json(data['unknown_0x8b0a4c90']),
            energy_warning_outline_color=Color.from_json(data['energy_warning_outline_color']),
            threat_warning_outline_color=Color.from_json(data['threat_warning_outline_color']),
            missile_warning_outline_color=Color.from_json(data['missile_warning_outline_color']),
            unknown_0x78522461=Color.from_json(data['unknown_0x78522461']),
            flash_pass_color=Color.from_json(data['flash_pass_color']),
            unknown_0x79ea6f12=Color.from_json(data['unknown_0x79ea6f12']),
            unknown_0xdc901206=Color.from_json(data['unknown_0xdc901206']),
            unknown_0xc54fa7bc=Color.from_json(data['unknown_0xc54fa7bc']),
            unknown_0x18717fa7=Color.from_json(data['unknown_0x18717fa7']),
            unknown_0x8b7d7378=Color.from_json(data['unknown_0x8b7d7378']),
            unknown_0x867b01a2=Color.from_json(data['unknown_0x867b01a2']),
            unknown_0x08be8347=Color.from_json(data['unknown_0x08be8347']),
            unknown_0xe6ec3c8d=Color.from_json(data['unknown_0xe6ec3c8d']),
            unknown_0x591cd695=Color.from_json(data['unknown_0x591cd695']),
            unknown_0x26e1eb8c=Color.from_json(data['unknown_0x26e1eb8c']),
            unknown_0x63e9e374=Color.from_json(data['unknown_0x63e9e374']),
            unknown_0x738d9c43=Color.from_json(data['unknown_0x738d9c43']),
            unknown_0xba6c75a2=Color.from_json(data['unknown_0xba6c75a2']),
            unknown_0xc37d11b7=Color.from_json(data['unknown_0xc37d11b7']),
            unknown_0xef1ec40e=Color.from_json(data['unknown_0xef1ec40e']),
            unknown_0x0ca7beb2=Color.from_json(data['unknown_0x0ca7beb2']),
            unknown_0x87d3ce8a=Color.from_json(data['unknown_0x87d3ce8a']),
            unknown_0xeb7eb756=Color.from_json(data['unknown_0xeb7eb756']),
            metroid_suck_pulse_color=Color.from_json(data['metroid_suck_pulse_color']),
            unknown_0xce7c9d8d=Color.from_json(data['unknown_0xce7c9d8d']),
            energy_bar_damage_color=Color.from_json(data['energy_bar_damage_color']),
            unknown_0xafe2d45d=Color.from_json(data['unknown_0xafe2d45d']),
            x_ray_holo_grid_color=Color.from_json(data['x_ray_holo_grid_color']),
            x_ray_seeker_color=Color.from_json(data['x_ray_seeker_color']),
            x_ray_seeker_ticks_color=Color.from_json(data['x_ray_seeker_ticks_color']),
            x_ray_seeker_ticks_outer_color=Color.from_json(data['x_ray_seeker_ticks_outer_color']),
            x_ray_top_puzzle_color=Color.from_json(data['x_ray_top_puzzle_color']),
            x_ray_bottom_puzzle_color=Color.from_json(data['x_ray_bottom_puzzle_color']),
            x_ray_left_puzzle_color=Color.from_json(data['x_ray_left_puzzle_color']),
            x_ray_right_puzzle_color=Color.from_json(data['x_ray_right_puzzle_color']),
            x_ray_corner_color=Color.from_json(data['x_ray_corner_color']),
            unknown_0x51c5aad9=Color.from_json(data['unknown_0x51c5aad9']),
            unknown_0x60e8322b=Color.from_json(data['unknown_0x60e8322b']),
            unknown_0xa947a67c=Color.from_json(data['unknown_0xa947a67c']),
            unknown_0x421bae2a=Color.from_json(data['unknown_0x421bae2a']),
            unknown_0xf0049167=Color.from_json(data['unknown_0xf0049167']),
            unknown_0x76357179=Color.from_json(data['unknown_0x76357179']),
            unknown_0x439a3774=Color.from_json(data['unknown_0x439a3774']),
            unknown_0x8ee94c81=Color.from_json(data['unknown_0x8ee94c81']),
            scan_download_square_color=Color.from_json(data['scan_download_square_color']),
            scan_dot_color=Color.from_json(data['scan_dot_color']),
            unknown_0x716e6398=Color.from_json(data['unknown_0x716e6398']),
            steam_no_blur_color=Color.from_json(data['steam_no_blur_color']),
            unknown_0x0f37e756=Color.from_json(data['unknown_0x0f37e756']),
            unknown_0xf7283644=Color.from_json(data['unknown_0xf7283644']),
            unknown_0x37564b7d=Color.from_json(data['unknown_0x37564b7d']),
            unknown_0x66b7eda3=Color.from_json(data['unknown_0x66b7eda3']),
            unknown_0xf895098f=Color.from_json(data['unknown_0xf895098f']),
            unknown_0x9b27be10=Color.from_json(data['unknown_0x9b27be10']),
            unknown_0x6c8550c9=Color.from_json(data['unknown_0x6c8550c9']),
            unknown_0x5368a35f=Color.from_json(data['unknown_0x5368a35f']),
            unknown_0x5a807b81=Color.from_json(data['unknown_0x5a807b81']),
            unknown_0xeb63afed=Color.from_json(data['unknown_0xeb63afed']),
            scan_panel_color=Color.from_json(data['scan_panel_color']),
            unknown_0x96f650c3=Color.from_json(data['unknown_0x96f650c3']),
            scan_images_color=Color.from_json(data['scan_images_color']),
            unknown_0xd3bafaf5=Color.from_json(data['unknown_0xd3bafaf5']),
            threat_group_damage_color=Color.from_json(data['threat_group_damage_color']),
            unknown_0x4f1d443e=Color.from_json(data['unknown_0x4f1d443e']),
            unknown_0x0f6451da=Color.from_json(data['unknown_0x0f6451da']),
            unknown_0xc1ec3637=Color.from_json(data['unknown_0xc1ec3637']),
            unknown_0xb6a61e34=Color.from_json(data['unknown_0xb6a61e34']),
            unknown_0xfdcd9589=Color.from_json(data['unknown_0xfdcd9589']),
            unknown_0xb0253266=Color.from_json(data['unknown_0xb0253266']),
            scan_seeker_color=Color.from_json(data['scan_seeker_color']),
            unknown_0xe8401c5a=Color.from_json(data['unknown_0xe8401c5a']),
            unknown_0x659147ae=Color.from_json(data['unknown_0x659147ae']),
            unknown_0x43ed3310=Color.from_json(data['unknown_0x43ed3310']),
            unknown_0xa781ed1d=Color.from_json(data['unknown_0xa781ed1d']),
            unknown_0x35402188=Color.from_json(data['unknown_0x35402188']),
            unknown_0x223058b5=Color.from_json(data['unknown_0x223058b5']),
            unknown_0xe846d37f=Color.from_json(data['unknown_0xe846d37f']),
            thermal_lock_color=Color.from_json(data['thermal_lock_color']),
            log_book_color=Color.from_json(data['log_book_color']),
            inventory_equipped_color=Color.from_json(data['inventory_equipped_color']),
            unknown_0x02d5344f=Color.from_json(data['unknown_0x02d5344f']),
            unknown_0xf37f8deb=Color.from_json(data['unknown_0xf37f8deb']),
            unknown_0x5a6587df=Color.from_json(data['unknown_0x5a6587df']),
            unknown_0xc18bdc67=Color.from_json(data['unknown_0xc18bdc67']),
            unknown_0x4d916bb8=Color.from_json(data['unknown_0x4d916bb8']),
            unknown_0x5ba76807=Color.from_json(data['unknown_0x5ba76807']),
            unknown_0xa42f6495=Color.from_json(data['unknown_0xa42f6495']),
            unknown_0x448156ae=Color.from_json(data['unknown_0x448156ae']),
            unknown_0x1a8b61b8=Color.from_json(data['unknown_0x1a8b61b8']),
            unknown_0xf36adacb=Color.from_json(data['unknown_0xf36adacb']),
            unknown_0x3aee673f=Color.from_json(data['unknown_0x3aee673f']),
            unknown_0xf9c88b05=Color.from_json(data['unknown_0xf9c88b05']),
            unknown_0x3bffe826=Color.from_json(data['unknown_0x3bffe826']),
            unknown_0x19e9738b=Color.from_json(data['unknown_0x19e9738b']),
            unknown_0x9329c6ff=Color.from_json(data['unknown_0x9329c6ff']),
            unknown_0xf9e7e0df=Color.from_json(data['unknown_0xf9e7e0df']),
            unknown_0x04e77411=Color.from_json(data['unknown_0x04e77411']),
            unknown_0x3c5d7111=Color.from_json(data['unknown_0x3c5d7111']),
            unknown_0x42e2dfc1=Color.from_json(data['unknown_0x42e2dfc1']),
            unknown_0xc758541f=Color.from_json(data['unknown_0xc758541f']),
            unknown_0xde649e48=Color.from_json(data['unknown_0xde649e48']),
            unknown_0x5bf10430=Color.from_json(data['unknown_0x5bf10430']),
            unknown_0xc01f5f88=Color.from_json(data['unknown_0xc01f5f88']),
            unknown_0x7d2500d2=Color.from_json(data['unknown_0x7d2500d2']),
            unknown_0x14558146=Color.from_json(data['unknown_0x14558146']),
            unknown_0x949b0fff=Color.from_json(data['unknown_0x949b0fff']),
            unknown_0x74353dc4=Color.from_json(data['unknown_0x74353dc4']),
            unknown_0x5ff96af1=Color.from_json(data['unknown_0x5ff96af1']),
            unknown_0x074bb42f=Color.from_json(data['unknown_0x074bb42f']),
            unknown_0xaaf6e9a9=Color.from_json(data['unknown_0xaaf6e9a9']),
            unknown_0x5e5b8c0a=Color.from_json(data['unknown_0x5e5b8c0a']),
            unknown_0xabe766b0=Color.from_json(data['unknown_0xabe766b0']),
            unknown_0x34f26028=Color.from_json(data['unknown_0x34f26028']),
            unknown_0xa59b3320=Color.from_json(data['unknown_0xa59b3320']),
            unknown_0xbfffe95a=data['unknown_0xbfffe95a'],
            unknown_0x0c3c55c9=Color.from_json(data['unknown_0x0c3c55c9']),
            unknown_0xf0c61af5=Color.from_json(data['unknown_0xf0c61af5']),
            unknown_0xc87c1ff5=Color.from_json(data['unknown_0xc87c1ff5']),
            unknown_0x88936aa2=Color.from_json(data['unknown_0x88936aa2']),
            unknown_0xea4347bc=Color.from_json(data['unknown_0xea4347bc']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x8ed04c36': self.unknown_0x8ed04c36.to_json(),
            'unknown_0x166c22e0': self.unknown_0x166c22e0.to_json(),
            'unknown_0xcec78e81': self.unknown_0xcec78e81.to_json(),
            'unknown_0x91338f72': self.unknown_0x91338f72.to_json(),
            'unknown_0x0d24ae6b': self.unknown_0x0d24ae6b.to_json(),
            'unknown_0xddc561eb': self.unknown_0xddc561eb.to_json(),
            'unknown_0x9be28150': self.unknown_0x9be28150.to_json(),
            'hud_memo_text_foreground_color': self.hud_memo_text_foreground_color.to_json(),
            'hud_memo_text_outline_color': self.hud_memo_text_outline_color.to_json(),
            'unknown_0xc8ddc662': self.unknown_0xc8ddc662.to_json(),
            'hud_glow_color': self.hud_glow_color.to_json(),
            'unknown_0x5c336f85': self.unknown_0x5c336f85.to_json(),
            'unknown_0xdefca700': self.unknown_0xdefca700.to_json(),
            'selected_visor_beam_color': self.selected_visor_beam_color.to_json(),
            'unselected_visor_beam_color': self.unselected_visor_beam_color.to_json(),
            'energy_bar_low_filled_color': self.energy_bar_low_filled_color.to_json(),
            'energy_bar_low_shadow_color': self.energy_bar_low_shadow_color.to_json(),
            'energy_bar_low_empty_color': self.energy_bar_low_empty_color.to_json(),
            'hud_damage_modulate_color': self.hud_damage_modulate_color.to_json(),
            'damage_indicator_color': self.damage_indicator_color.to_json(),
            'hud_title_foreground_color': self.hud_title_foreground_color.to_json(),
            'hud_title_outline_color': self.hud_title_outline_color.to_json(),
            'unknown_0xe7070332': self.unknown_0xe7070332.to_json(),
            'unknown_0x779c7b9c': self.unknown_0x779c7b9c.to_json(),
            'unknown_0x13bd3b64': self.unknown_0x13bd3b64.to_json(),
            'unknown_0x1531edd3': self.unknown_0x1531edd3.to_json(),
            'unknown_0x27d0c234': self.unknown_0x27d0c234.to_json(),
            'unknown_0xbaa6d6a1': self.unknown_0xbaa6d6a1.to_json(),
            'unknown_0x59e416aa': self.unknown_0x59e416aa.to_json(),
            'unknown_0x92b8c50f': self.unknown_0x92b8c50f.to_json(),
            'unknown_0x142cb7a1': self.unknown_0x142cb7a1.to_json(),
            'unknown_0xdf706404': self.unknown_0xdf706404.to_json(),
            'unknown_0x81269ee0': self.unknown_0x81269ee0.to_json(),
            'unknown_0x4a7a4d45': self.unknown_0x4a7a4d45.to_json(),
            'unknown_0xccee3feb': self.unknown_0xccee3feb.to_json(),
            'unknown_0x07b2ec4e': self.unknown_0x07b2ec4e.to_json(),
            'energy_warning_color': self.energy_warning_color.to_json(),
            'threat_warning_color': self.threat_warning_color.to_json(),
            'missile_warning_color': self.missile_warning_color.to_json(),
            'unknown_0x83040135': self.unknown_0x83040135.to_json(),
            'unknown_0x1adea12b': self.unknown_0x1adea12b.to_json(),
            'threat_bar_shadow_color': self.threat_bar_shadow_color.to_json(),
            'threat_bar_empty_color': self.threat_bar_empty_color.to_json(),
            'unknown_0x3c1ae0ff': self.unknown_0x3c1ae0ff.to_json(),
            'missile_bar_shadow_color': self.missile_bar_shadow_color.to_json(),
            'missile_bar_empty_color': self.missile_bar_empty_color.to_json(),
            'threat_group_color': self.threat_group_color.to_json(),
            'unknown_0xa6609cc5': self.unknown_0xa6609cc5.to_json(),
            'unknown_0xbe3c29a1': self.unknown_0xbe3c29a1.to_json(),
            'unknown_0xf4379cf4': self.unknown_0xf4379cf4.to_json(),
            'threat_group_inactive_color': self.threat_group_inactive_color.to_json(),
            'missile_group_inactive_color': self.missile_group_inactive_color.to_json(),
            'missile_group_combo_charge_color': self.missile_group_combo_charge_color.to_json(),
            'unknown_0x4c5aff4f': self.unknown_0x4c5aff4f.to_json(),
            'unknown_0x0b17b693': self.unknown_0x0b17b693.to_json(),
            'unknown_0xfad063d5': self.unknown_0xfad063d5.to_json(),
            'unknown_0x2eafedf7': self.unknown_0x2eafedf7.to_json(),
            'energy_bar_name_avoidance_color': self.energy_bar_name_avoidance_color.to_json(),
            'unknown_0x8b0a4c90': self.unknown_0x8b0a4c90.to_json(),
            'energy_warning_outline_color': self.energy_warning_outline_color.to_json(),
            'threat_warning_outline_color': self.threat_warning_outline_color.to_json(),
            'missile_warning_outline_color': self.missile_warning_outline_color.to_json(),
            'unknown_0x78522461': self.unknown_0x78522461.to_json(),
            'flash_pass_color': self.flash_pass_color.to_json(),
            'unknown_0x79ea6f12': self.unknown_0x79ea6f12.to_json(),
            'unknown_0xdc901206': self.unknown_0xdc901206.to_json(),
            'unknown_0xc54fa7bc': self.unknown_0xc54fa7bc.to_json(),
            'unknown_0x18717fa7': self.unknown_0x18717fa7.to_json(),
            'unknown_0x8b7d7378': self.unknown_0x8b7d7378.to_json(),
            'unknown_0x867b01a2': self.unknown_0x867b01a2.to_json(),
            'unknown_0x08be8347': self.unknown_0x08be8347.to_json(),
            'unknown_0xe6ec3c8d': self.unknown_0xe6ec3c8d.to_json(),
            'unknown_0x591cd695': self.unknown_0x591cd695.to_json(),
            'unknown_0x26e1eb8c': self.unknown_0x26e1eb8c.to_json(),
            'unknown_0x63e9e374': self.unknown_0x63e9e374.to_json(),
            'unknown_0x738d9c43': self.unknown_0x738d9c43.to_json(),
            'unknown_0xba6c75a2': self.unknown_0xba6c75a2.to_json(),
            'unknown_0xc37d11b7': self.unknown_0xc37d11b7.to_json(),
            'unknown_0xef1ec40e': self.unknown_0xef1ec40e.to_json(),
            'unknown_0x0ca7beb2': self.unknown_0x0ca7beb2.to_json(),
            'unknown_0x87d3ce8a': self.unknown_0x87d3ce8a.to_json(),
            'unknown_0xeb7eb756': self.unknown_0xeb7eb756.to_json(),
            'metroid_suck_pulse_color': self.metroid_suck_pulse_color.to_json(),
            'unknown_0xce7c9d8d': self.unknown_0xce7c9d8d.to_json(),
            'energy_bar_damage_color': self.energy_bar_damage_color.to_json(),
            'unknown_0xafe2d45d': self.unknown_0xafe2d45d.to_json(),
            'x_ray_holo_grid_color': self.x_ray_holo_grid_color.to_json(),
            'x_ray_seeker_color': self.x_ray_seeker_color.to_json(),
            'x_ray_seeker_ticks_color': self.x_ray_seeker_ticks_color.to_json(),
            'x_ray_seeker_ticks_outer_color': self.x_ray_seeker_ticks_outer_color.to_json(),
            'x_ray_top_puzzle_color': self.x_ray_top_puzzle_color.to_json(),
            'x_ray_bottom_puzzle_color': self.x_ray_bottom_puzzle_color.to_json(),
            'x_ray_left_puzzle_color': self.x_ray_left_puzzle_color.to_json(),
            'x_ray_right_puzzle_color': self.x_ray_right_puzzle_color.to_json(),
            'x_ray_corner_color': self.x_ray_corner_color.to_json(),
            'unknown_0x51c5aad9': self.unknown_0x51c5aad9.to_json(),
            'unknown_0x60e8322b': self.unknown_0x60e8322b.to_json(),
            'unknown_0xa947a67c': self.unknown_0xa947a67c.to_json(),
            'unknown_0x421bae2a': self.unknown_0x421bae2a.to_json(),
            'unknown_0xf0049167': self.unknown_0xf0049167.to_json(),
            'unknown_0x76357179': self.unknown_0x76357179.to_json(),
            'unknown_0x439a3774': self.unknown_0x439a3774.to_json(),
            'unknown_0x8ee94c81': self.unknown_0x8ee94c81.to_json(),
            'scan_download_square_color': self.scan_download_square_color.to_json(),
            'scan_dot_color': self.scan_dot_color.to_json(),
            'unknown_0x716e6398': self.unknown_0x716e6398.to_json(),
            'steam_no_blur_color': self.steam_no_blur_color.to_json(),
            'unknown_0x0f37e756': self.unknown_0x0f37e756.to_json(),
            'unknown_0xf7283644': self.unknown_0xf7283644.to_json(),
            'unknown_0x37564b7d': self.unknown_0x37564b7d.to_json(),
            'unknown_0x66b7eda3': self.unknown_0x66b7eda3.to_json(),
            'unknown_0xf895098f': self.unknown_0xf895098f.to_json(),
            'unknown_0x9b27be10': self.unknown_0x9b27be10.to_json(),
            'unknown_0x6c8550c9': self.unknown_0x6c8550c9.to_json(),
            'unknown_0x5368a35f': self.unknown_0x5368a35f.to_json(),
            'unknown_0x5a807b81': self.unknown_0x5a807b81.to_json(),
            'unknown_0xeb63afed': self.unknown_0xeb63afed.to_json(),
            'scan_panel_color': self.scan_panel_color.to_json(),
            'unknown_0x96f650c3': self.unknown_0x96f650c3.to_json(),
            'scan_images_color': self.scan_images_color.to_json(),
            'unknown_0xd3bafaf5': self.unknown_0xd3bafaf5.to_json(),
            'threat_group_damage_color': self.threat_group_damage_color.to_json(),
            'unknown_0x4f1d443e': self.unknown_0x4f1d443e.to_json(),
            'unknown_0x0f6451da': self.unknown_0x0f6451da.to_json(),
            'unknown_0xc1ec3637': self.unknown_0xc1ec3637.to_json(),
            'unknown_0xb6a61e34': self.unknown_0xb6a61e34.to_json(),
            'unknown_0xfdcd9589': self.unknown_0xfdcd9589.to_json(),
            'unknown_0xb0253266': self.unknown_0xb0253266.to_json(),
            'scan_seeker_color': self.scan_seeker_color.to_json(),
            'unknown_0xe8401c5a': self.unknown_0xe8401c5a.to_json(),
            'unknown_0x659147ae': self.unknown_0x659147ae.to_json(),
            'unknown_0x43ed3310': self.unknown_0x43ed3310.to_json(),
            'unknown_0xa781ed1d': self.unknown_0xa781ed1d.to_json(),
            'unknown_0x35402188': self.unknown_0x35402188.to_json(),
            'unknown_0x223058b5': self.unknown_0x223058b5.to_json(),
            'unknown_0xe846d37f': self.unknown_0xe846d37f.to_json(),
            'thermal_lock_color': self.thermal_lock_color.to_json(),
            'log_book_color': self.log_book_color.to_json(),
            'inventory_equipped_color': self.inventory_equipped_color.to_json(),
            'unknown_0x02d5344f': self.unknown_0x02d5344f.to_json(),
            'unknown_0xf37f8deb': self.unknown_0xf37f8deb.to_json(),
            'unknown_0x5a6587df': self.unknown_0x5a6587df.to_json(),
            'unknown_0xc18bdc67': self.unknown_0xc18bdc67.to_json(),
            'unknown_0x4d916bb8': self.unknown_0x4d916bb8.to_json(),
            'unknown_0x5ba76807': self.unknown_0x5ba76807.to_json(),
            'unknown_0xa42f6495': self.unknown_0xa42f6495.to_json(),
            'unknown_0x448156ae': self.unknown_0x448156ae.to_json(),
            'unknown_0x1a8b61b8': self.unknown_0x1a8b61b8.to_json(),
            'unknown_0xf36adacb': self.unknown_0xf36adacb.to_json(),
            'unknown_0x3aee673f': self.unknown_0x3aee673f.to_json(),
            'unknown_0xf9c88b05': self.unknown_0xf9c88b05.to_json(),
            'unknown_0x3bffe826': self.unknown_0x3bffe826.to_json(),
            'unknown_0x19e9738b': self.unknown_0x19e9738b.to_json(),
            'unknown_0x9329c6ff': self.unknown_0x9329c6ff.to_json(),
            'unknown_0xf9e7e0df': self.unknown_0xf9e7e0df.to_json(),
            'unknown_0x04e77411': self.unknown_0x04e77411.to_json(),
            'unknown_0x3c5d7111': self.unknown_0x3c5d7111.to_json(),
            'unknown_0x42e2dfc1': self.unknown_0x42e2dfc1.to_json(),
            'unknown_0xc758541f': self.unknown_0xc758541f.to_json(),
            'unknown_0xde649e48': self.unknown_0xde649e48.to_json(),
            'unknown_0x5bf10430': self.unknown_0x5bf10430.to_json(),
            'unknown_0xc01f5f88': self.unknown_0xc01f5f88.to_json(),
            'unknown_0x7d2500d2': self.unknown_0x7d2500d2.to_json(),
            'unknown_0x14558146': self.unknown_0x14558146.to_json(),
            'unknown_0x949b0fff': self.unknown_0x949b0fff.to_json(),
            'unknown_0x74353dc4': self.unknown_0x74353dc4.to_json(),
            'unknown_0x5ff96af1': self.unknown_0x5ff96af1.to_json(),
            'unknown_0x074bb42f': self.unknown_0x074bb42f.to_json(),
            'unknown_0xaaf6e9a9': self.unknown_0xaaf6e9a9.to_json(),
            'unknown_0x5e5b8c0a': self.unknown_0x5e5b8c0a.to_json(),
            'unknown_0xabe766b0': self.unknown_0xabe766b0.to_json(),
            'unknown_0x34f26028': self.unknown_0x34f26028.to_json(),
            'unknown_0xa59b3320': self.unknown_0xa59b3320.to_json(),
            'unknown_0xbfffe95a': self.unknown_0xbfffe95a,
            'unknown_0x0c3c55c9': self.unknown_0x0c3c55c9.to_json(),
            'unknown_0xf0c61af5': self.unknown_0xf0c61af5.to_json(),
            'unknown_0xc87c1ff5': self.unknown_0xc87c1ff5.to_json(),
            'unknown_0x88936aa2': self.unknown_0x88936aa2.to_json(),
            'unknown_0xea4347bc': self.unknown_0xea4347bc.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_unknown_0x8ed04c36(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x166c22e0(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xcec78e81(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x91338f72(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0d24ae6b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xddc561eb(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9be28150(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_memo_text_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_memo_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc8ddc662(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_glow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5c336f85(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdefca700(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_selected_visor_beam_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unselected_visor_beam_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_low_filled_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_low_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_low_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_damage_modulate_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_damage_indicator_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_title_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_title_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe7070332(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x779c7b9c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x13bd3b64(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x1531edd3(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x27d0c234(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xbaa6d6a1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x59e416aa(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x92b8c50f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x142cb7a1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdf706404(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x81269ee0(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4a7a4d45(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xccee3feb(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x07b2ec4e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_warning_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_warning_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_warning_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x83040135(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x1adea12b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_bar_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_bar_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3c1ae0ff(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_bar_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_bar_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_group_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa6609cc5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xbe3c29a1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf4379cf4(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_group_inactive_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_group_inactive_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_group_combo_charge_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4c5aff4f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0b17b693(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xfad063d5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x2eafedf7(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_name_avoidance_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x8b0a4c90(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_warning_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_warning_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_warning_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x78522461(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_flash_pass_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x79ea6f12(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdc901206(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc54fa7bc(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x18717fa7(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x8b7d7378(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x867b01a2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x08be8347(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe6ec3c8d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x591cd695(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x26e1eb8c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x63e9e374(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x738d9c43(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xba6c75a2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc37d11b7(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xef1ec40e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0ca7beb2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x87d3ce8a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xeb7eb756(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_metroid_suck_pulse_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xce7c9d8d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_damage_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xafe2d45d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_holo_grid_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_seeker_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_seeker_ticks_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_seeker_ticks_outer_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_top_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_bottom_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_left_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_right_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_corner_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x51c5aad9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x60e8322b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa947a67c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x421bae2a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf0049167(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x76357179(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x439a3774(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x8ee94c81(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_download_square_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_dot_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x716e6398(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_steam_no_blur_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0f37e756(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf7283644(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x37564b7d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x66b7eda3(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf895098f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9b27be10(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x6c8550c9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5368a35f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5a807b81(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xeb63afed(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_panel_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x96f650c3(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_images_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xd3bafaf5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_group_damage_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4f1d443e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0f6451da(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc1ec3637(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xb6a61e34(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xfdcd9589(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xb0253266(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_seeker_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe8401c5a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x659147ae(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x43ed3310(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa781ed1d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x35402188(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x223058b5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe846d37f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_thermal_lock_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_log_book_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_inventory_equipped_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x02d5344f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf37f8deb(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5a6587df(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc18bdc67(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4d916bb8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5ba76807(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa42f6495(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x448156ae(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x1a8b61b8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf36adacb(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3aee673f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf9c88b05(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3bffe826(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x19e9738b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9329c6ff(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf9e7e0df(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x04e77411(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3c5d7111(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x42e2dfc1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc758541f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xde649e48(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5bf10430(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc01f5f88(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x7d2500d2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x14558146(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x949b0fff(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x74353dc4(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5ff96af1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x074bb42f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xaaf6e9a9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5e5b8c0a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xabe766b0(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x34f26028(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa59b3320(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xbfffe95a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x0c3c55c9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf0c61af5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc87c1ff5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x88936aa2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xea4347bc(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8ed04c36: ('unknown_0x8ed04c36', _decode_unknown_0x8ed04c36),
    0x166c22e0: ('unknown_0x166c22e0', _decode_unknown_0x166c22e0),
    0xcec78e81: ('unknown_0xcec78e81', _decode_unknown_0xcec78e81),
    0x91338f72: ('unknown_0x91338f72', _decode_unknown_0x91338f72),
    0xd24ae6b: ('unknown_0x0d24ae6b', _decode_unknown_0x0d24ae6b),
    0xddc561eb: ('unknown_0xddc561eb', _decode_unknown_0xddc561eb),
    0x9be28150: ('unknown_0x9be28150', _decode_unknown_0x9be28150),
    0x2df1eb03: ('hud_memo_text_foreground_color', _decode_hud_memo_text_foreground_color),
    0xb5da30f4: ('hud_memo_text_outline_color', _decode_hud_memo_text_outline_color),
    0xc8ddc662: ('unknown_0xc8ddc662', _decode_unknown_0xc8ddc662),
    0x6991e2cd: ('hud_glow_color', _decode_hud_glow_color),
    0x5c336f85: ('unknown_0x5c336f85', _decode_unknown_0x5c336f85),
    0xdefca700: ('unknown_0xdefca700', _decode_unknown_0xdefca700),
    0xcb7ddaf4: ('selected_visor_beam_color', _decode_selected_visor_beam_color),
    0xf17911aa: ('unselected_visor_beam_color', _decode_unselected_visor_beam_color),
    0xa14c8d20: ('energy_bar_low_filled_color', _decode_energy_bar_low_filled_color),
    0xb4135cdd: ('energy_bar_low_shadow_color', _decode_energy_bar_low_shadow_color),
    0xe0290c48: ('energy_bar_low_empty_color', _decode_energy_bar_low_empty_color),
    0x1ec7f863: ('hud_damage_modulate_color', _decode_hud_damage_modulate_color),
    0xae1317d8: ('damage_indicator_color', _decode_damage_indicator_color),
    0x22b9b01e: ('hud_title_foreground_color', _decode_hud_title_foreground_color),
    0x70a2cd6e: ('hud_title_outline_color', _decode_hud_title_outline_color),
    0xe7070332: ('unknown_0xe7070332', _decode_unknown_0xe7070332),
    0x779c7b9c: ('unknown_0x779c7b9c', _decode_unknown_0x779c7b9c),
    0x13bd3b64: ('unknown_0x13bd3b64', _decode_unknown_0x13bd3b64),
    0x1531edd3: ('unknown_0x1531edd3', _decode_unknown_0x1531edd3),
    0x27d0c234: ('unknown_0x27d0c234', _decode_unknown_0x27d0c234),
    0xbaa6d6a1: ('unknown_0xbaa6d6a1', _decode_unknown_0xbaa6d6a1),
    0x59e416aa: ('unknown_0x59e416aa', _decode_unknown_0x59e416aa),
    0x92b8c50f: ('unknown_0x92b8c50f', _decode_unknown_0x92b8c50f),
    0x142cb7a1: ('unknown_0x142cb7a1', _decode_unknown_0x142cb7a1),
    0xdf706404: ('unknown_0xdf706404', _decode_unknown_0xdf706404),
    0x81269ee0: ('unknown_0x81269ee0', _decode_unknown_0x81269ee0),
    0x4a7a4d45: ('unknown_0x4a7a4d45', _decode_unknown_0x4a7a4d45),
    0xccee3feb: ('unknown_0xccee3feb', _decode_unknown_0xccee3feb),
    0x7b2ec4e: ('unknown_0x07b2ec4e', _decode_unknown_0x07b2ec4e),
    0x6f6e9d6d: ('energy_warning_color', _decode_energy_warning_color),
    0xca68f68f: ('threat_warning_color', _decode_threat_warning_color),
    0xc00a29f: ('missile_warning_color', _decode_missile_warning_color),
    0x83040135: ('unknown_0x83040135', _decode_unknown_0x83040135),
    0x1adea12b: ('unknown_0x1adea12b', _decode_unknown_0x1adea12b),
    0xf8170d6: ('threat_bar_shadow_color', _decode_threat_bar_shadow_color),
    0x794204fd: ('threat_bar_empty_color', _decode_threat_bar_empty_color),
    0x3c1ae0ff: ('unknown_0x3c1ae0ff', _decode_unknown_0x3c1ae0ff),
    0x29453102: ('missile_bar_shadow_color', _decode_missile_bar_shadow_color),
    0x64337ccd: ('missile_bar_empty_color', _decode_missile_bar_empty_color),
    0x4b86c539: ('threat_group_color', _decode_threat_group_color),
    0xa6609cc5: ('unknown_0xa6609cc5', _decode_unknown_0xa6609cc5),
    0xbe3c29a1: ('unknown_0xbe3c29a1', _decode_unknown_0xbe3c29a1),
    0xf4379cf4: ('unknown_0xf4379cf4', _decode_unknown_0xf4379cf4),
    0x74e5ffa1: ('threat_group_inactive_color', _decode_threat_group_inactive_color),
    0xd110a12f: ('missile_group_inactive_color', _decode_missile_group_inactive_color),
    0xceb17cdf: ('missile_group_combo_charge_color', _decode_missile_group_combo_charge_color),
    0x4c5aff4f: ('unknown_0x4c5aff4f', _decode_unknown_0x4c5aff4f),
    0xb17b693: ('unknown_0x0b17b693', _decode_unknown_0x0b17b693),
    0xfad063d5: ('unknown_0xfad063d5', _decode_unknown_0xfad063d5),
    0x2eafedf7: ('unknown_0x2eafedf7', _decode_unknown_0x2eafedf7),
    0x2a01734f: ('energy_bar_name_avoidance_color', _decode_energy_bar_name_avoidance_color),
    0x8b0a4c90: ('unknown_0x8b0a4c90', _decode_unknown_0x8b0a4c90),
    0xc4e17ca8: ('energy_warning_outline_color', _decode_energy_warning_outline_color),
    0xc7182898: ('threat_warning_outline_color', _decode_threat_warning_outline_color),
    0xcdbd73e1: ('missile_warning_outline_color', _decode_missile_warning_outline_color),
    0x78522461: ('unknown_0x78522461', _decode_unknown_0x78522461),
    0x6a839a97: ('flash_pass_color', _decode_flash_pass_color),
    0x79ea6f12: ('unknown_0x79ea6f12', _decode_unknown_0x79ea6f12),
    0xdc901206: ('unknown_0xdc901206', _decode_unknown_0xdc901206),
    0xc54fa7bc: ('unknown_0xc54fa7bc', _decode_unknown_0xc54fa7bc),
    0x18717fa7: ('unknown_0x18717fa7', _decode_unknown_0x18717fa7),
    0x8b7d7378: ('unknown_0x8b7d7378', _decode_unknown_0x8b7d7378),
    0x867b01a2: ('unknown_0x867b01a2', _decode_unknown_0x867b01a2),
    0x8be8347: ('unknown_0x08be8347', _decode_unknown_0x08be8347),
    0xe6ec3c8d: ('unknown_0xe6ec3c8d', _decode_unknown_0xe6ec3c8d),
    0x591cd695: ('unknown_0x591cd695', _decode_unknown_0x591cd695),
    0x26e1eb8c: ('unknown_0x26e1eb8c', _decode_unknown_0x26e1eb8c),
    0x63e9e374: ('unknown_0x63e9e374', _decode_unknown_0x63e9e374),
    0x738d9c43: ('unknown_0x738d9c43', _decode_unknown_0x738d9c43),
    0xba6c75a2: ('unknown_0xba6c75a2', _decode_unknown_0xba6c75a2),
    0xc37d11b7: ('unknown_0xc37d11b7', _decode_unknown_0xc37d11b7),
    0xef1ec40e: ('unknown_0xef1ec40e', _decode_unknown_0xef1ec40e),
    0xca7beb2: ('unknown_0x0ca7beb2', _decode_unknown_0x0ca7beb2),
    0x87d3ce8a: ('unknown_0x87d3ce8a', _decode_unknown_0x87d3ce8a),
    0xeb7eb756: ('unknown_0xeb7eb756', _decode_unknown_0xeb7eb756),
    0xe4c1bbeb: ('metroid_suck_pulse_color', _decode_metroid_suck_pulse_color),
    0xce7c9d8d: ('unknown_0xce7c9d8d', _decode_unknown_0xce7c9d8d),
    0x13490420: ('energy_bar_damage_color', _decode_energy_bar_damage_color),
    0xafe2d45d: ('unknown_0xafe2d45d', _decode_unknown_0xafe2d45d),
    0x2af5aa06: ('x_ray_holo_grid_color', _decode_x_ray_holo_grid_color),
    0xd3cbe846: ('x_ray_seeker_color', _decode_x_ray_seeker_color),
    0x507b51da: ('x_ray_seeker_ticks_color', _decode_x_ray_seeker_ticks_color),
    0xc61d97ef: ('x_ray_seeker_ticks_outer_color', _decode_x_ray_seeker_ticks_outer_color),
    0xaf0001cf: ('x_ray_top_puzzle_color', _decode_x_ray_top_puzzle_color),
    0x150a9b17: ('x_ray_bottom_puzzle_color', _decode_x_ray_bottom_puzzle_color),
    0xd66d715f: ('x_ray_left_puzzle_color', _decode_x_ray_left_puzzle_color),
    0xa8698fe8: ('x_ray_right_puzzle_color', _decode_x_ray_right_puzzle_color),
    0x4cb38e71: ('x_ray_corner_color', _decode_x_ray_corner_color),
    0x51c5aad9: ('unknown_0x51c5aad9', _decode_unknown_0x51c5aad9),
    0x60e8322b: ('unknown_0x60e8322b', _decode_unknown_0x60e8322b),
    0xa947a67c: ('unknown_0xa947a67c', _decode_unknown_0xa947a67c),
    0x421bae2a: ('unknown_0x421bae2a', _decode_unknown_0x421bae2a),
    0xf0049167: ('unknown_0xf0049167', _decode_unknown_0xf0049167),
    0x76357179: ('unknown_0x76357179', _decode_unknown_0x76357179),
    0x439a3774: ('unknown_0x439a3774', _decode_unknown_0x439a3774),
    0x8ee94c81: ('unknown_0x8ee94c81', _decode_unknown_0x8ee94c81),
    0xbb0897ea: ('scan_download_square_color', _decode_scan_download_square_color),
    0xc12cbab9: ('scan_dot_color', _decode_scan_dot_color),
    0x716e6398: ('unknown_0x716e6398', _decode_unknown_0x716e6398),
    0xdaca46d4: ('steam_no_blur_color', _decode_steam_no_blur_color),
    0xf37e756: ('unknown_0x0f37e756', _decode_unknown_0x0f37e756),
    0xf7283644: ('unknown_0xf7283644', _decode_unknown_0xf7283644),
    0x37564b7d: ('unknown_0x37564b7d', _decode_unknown_0x37564b7d),
    0x66b7eda3: ('unknown_0x66b7eda3', _decode_unknown_0x66b7eda3),
    0xf895098f: ('unknown_0xf895098f', _decode_unknown_0xf895098f),
    0x9b27be10: ('unknown_0x9b27be10', _decode_unknown_0x9b27be10),
    0x6c8550c9: ('unknown_0x6c8550c9', _decode_unknown_0x6c8550c9),
    0x5368a35f: ('unknown_0x5368a35f', _decode_unknown_0x5368a35f),
    0x5a807b81: ('unknown_0x5a807b81', _decode_unknown_0x5a807b81),
    0xeb63afed: ('unknown_0xeb63afed', _decode_unknown_0xeb63afed),
    0x92f59138: ('scan_panel_color', _decode_scan_panel_color),
    0x96f650c3: ('unknown_0x96f650c3', _decode_unknown_0x96f650c3),
    0xabdbfa5b: ('scan_images_color', _decode_scan_images_color),
    0xd3bafaf5: ('unknown_0xd3bafaf5', _decode_unknown_0xd3bafaf5),
    0xf8b971fa: ('threat_group_damage_color', _decode_threat_group_damage_color),
    0x4f1d443e: ('unknown_0x4f1d443e', _decode_unknown_0x4f1d443e),
    0xf6451da: ('unknown_0x0f6451da', _decode_unknown_0x0f6451da),
    0xc1ec3637: ('unknown_0xc1ec3637', _decode_unknown_0xc1ec3637),
    0xb6a61e34: ('unknown_0xb6a61e34', _decode_unknown_0xb6a61e34),
    0xfdcd9589: ('unknown_0xfdcd9589', _decode_unknown_0xfdcd9589),
    0xb0253266: ('unknown_0xb0253266', _decode_unknown_0xb0253266),
    0x345e5b4e: ('scan_seeker_color', _decode_scan_seeker_color),
    0xe8401c5a: ('unknown_0xe8401c5a', _decode_unknown_0xe8401c5a),
    0x659147ae: ('unknown_0x659147ae', _decode_unknown_0x659147ae),
    0x43ed3310: ('unknown_0x43ed3310', _decode_unknown_0x43ed3310),
    0xa781ed1d: ('unknown_0xa781ed1d', _decode_unknown_0xa781ed1d),
    0x35402188: ('unknown_0x35402188', _decode_unknown_0x35402188),
    0x223058b5: ('unknown_0x223058b5', _decode_unknown_0x223058b5),
    0xe846d37f: ('unknown_0xe846d37f', _decode_unknown_0xe846d37f),
    0x8c9f2a1a: ('thermal_lock_color', _decode_thermal_lock_color),
    0x1b0f3a85: ('log_book_color', _decode_log_book_color),
    0x149369fd: ('inventory_equipped_color', _decode_inventory_equipped_color),
    0x2d5344f: ('unknown_0x02d5344f', _decode_unknown_0x02d5344f),
    0xf37f8deb: ('unknown_0xf37f8deb', _decode_unknown_0xf37f8deb),
    0x5a6587df: ('unknown_0x5a6587df', _decode_unknown_0x5a6587df),
    0xc18bdc67: ('unknown_0xc18bdc67', _decode_unknown_0xc18bdc67),
    0x4d916bb8: ('unknown_0x4d916bb8', _decode_unknown_0x4d916bb8),
    0x5ba76807: ('unknown_0x5ba76807', _decode_unknown_0x5ba76807),
    0xa42f6495: ('unknown_0xa42f6495', _decode_unknown_0xa42f6495),
    0x448156ae: ('unknown_0x448156ae', _decode_unknown_0x448156ae),
    0x1a8b61b8: ('unknown_0x1a8b61b8', _decode_unknown_0x1a8b61b8),
    0xf36adacb: ('unknown_0xf36adacb', _decode_unknown_0xf36adacb),
    0x3aee673f: ('unknown_0x3aee673f', _decode_unknown_0x3aee673f),
    0xf9c88b05: ('unknown_0xf9c88b05', _decode_unknown_0xf9c88b05),
    0x3bffe826: ('unknown_0x3bffe826', _decode_unknown_0x3bffe826),
    0x19e9738b: ('unknown_0x19e9738b', _decode_unknown_0x19e9738b),
    0x9329c6ff: ('unknown_0x9329c6ff', _decode_unknown_0x9329c6ff),
    0xf9e7e0df: ('unknown_0xf9e7e0df', _decode_unknown_0xf9e7e0df),
    0x4e77411: ('unknown_0x04e77411', _decode_unknown_0x04e77411),
    0x3c5d7111: ('unknown_0x3c5d7111', _decode_unknown_0x3c5d7111),
    0x42e2dfc1: ('unknown_0x42e2dfc1', _decode_unknown_0x42e2dfc1),
    0xc758541f: ('unknown_0xc758541f', _decode_unknown_0xc758541f),
    0xde649e48: ('unknown_0xde649e48', _decode_unknown_0xde649e48),
    0x5bf10430: ('unknown_0x5bf10430', _decode_unknown_0x5bf10430),
    0xc01f5f88: ('unknown_0xc01f5f88', _decode_unknown_0xc01f5f88),
    0x7d2500d2: ('unknown_0x7d2500d2', _decode_unknown_0x7d2500d2),
    0x14558146: ('unknown_0x14558146', _decode_unknown_0x14558146),
    0x949b0fff: ('unknown_0x949b0fff', _decode_unknown_0x949b0fff),
    0x74353dc4: ('unknown_0x74353dc4', _decode_unknown_0x74353dc4),
    0x5ff96af1: ('unknown_0x5ff96af1', _decode_unknown_0x5ff96af1),
    0x74bb42f: ('unknown_0x074bb42f', _decode_unknown_0x074bb42f),
    0xaaf6e9a9: ('unknown_0xaaf6e9a9', _decode_unknown_0xaaf6e9a9),
    0x5e5b8c0a: ('unknown_0x5e5b8c0a', _decode_unknown_0x5e5b8c0a),
    0xabe766b0: ('unknown_0xabe766b0', _decode_unknown_0xabe766b0),
    0x34f26028: ('unknown_0x34f26028', _decode_unknown_0x34f26028),
    0xa59b3320: ('unknown_0xa59b3320', _decode_unknown_0xa59b3320),
    0xbfffe95a: ('unknown_0xbfffe95a', _decode_unknown_0xbfffe95a),
    0xc3c55c9: ('unknown_0x0c3c55c9', _decode_unknown_0x0c3c55c9),
    0xf0c61af5: ('unknown_0xf0c61af5', _decode_unknown_0xf0c61af5),
    0xc87c1ff5: ('unknown_0xc87c1ff5', _decode_unknown_0xc87c1ff5),
    0x88936aa2: ('unknown_0x88936aa2', _decode_unknown_0x88936aa2),
    0xea4347bc: ('unknown_0xea4347bc', _decode_unknown_0xea4347bc),
}
