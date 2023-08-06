# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TweakGui.HudColorTypedef import HudColorTypedef
from retro_data_structures.properties.echoes.archetypes.TweakGui.VisorColorSchemeTypedef import VisorColorSchemeTypedef
from retro_data_structures.properties.echoes.archetypes.TweakGuiColors.HUDColorsTypedef import HUDColorsTypedef
from retro_data_structures.properties.echoes.archetypes.TweakGuiColors.Misc import Misc
from retro_data_structures.properties.echoes.archetypes.TweakGuiColors.Multiplayer import Multiplayer
from retro_data_structures.properties.echoes.archetypes.TweakGuiColors.TurretHudTypedef import TurretHudTypedef


@dataclasses.dataclass()
class TweakGuiColors(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    hud_colors: HUDColorsTypedef = dataclasses.field(default_factory=HUDColorsTypedef)
    misc: Misc = dataclasses.field(default_factory=Misc)
    multiplayer: Multiplayer = dataclasses.field(default_factory=Multiplayer)
    combat_hud_color_scheme: VisorColorSchemeTypedef = dataclasses.field(default_factory=VisorColorSchemeTypedef)
    echo_hud_color_scheme: VisorColorSchemeTypedef = dataclasses.field(default_factory=VisorColorSchemeTypedef)
    scan_hud_color_scheme: VisorColorSchemeTypedef = dataclasses.field(default_factory=VisorColorSchemeTypedef)
    dark_hud_color_scheme: VisorColorSchemeTypedef = dataclasses.field(default_factory=VisorColorSchemeTypedef)
    ball_hud_color_scheme: VisorColorSchemeTypedef = dataclasses.field(default_factory=VisorColorSchemeTypedef)
    combat_hud: HudColorTypedef = dataclasses.field(default_factory=HudColorTypedef)
    scan_hud: HudColorTypedef = dataclasses.field(default_factory=HudColorTypedef)
    x_ray_hud: HudColorTypedef = dataclasses.field(default_factory=HudColorTypedef)
    thermal_hud: HudColorTypedef = dataclasses.field(default_factory=HudColorTypedef)
    ball_hud: HudColorTypedef = dataclasses.field(default_factory=HudColorTypedef)
    turret_hud: TurretHudTypedef = dataclasses.field(default_factory=TurretHudTypedef)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWGC'

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

        data.write(b'\xcbsw$')  # 0xcb737724
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hud_colors.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'gV\xd4\xde')  # 0x6756d4de
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'iv\x13\xe9')  # 0x697613e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.multiplayer.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xc7\x00U')  # 0x67c70055
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.combat_hud_color_scheme.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'b\xe0\xa0\x8f')  # 0x62e0a08f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.echo_hud_color_scheme.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xbe\xcdn')  # 0x80becd6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_hud_color_scheme.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\xe4\xb2\x97')  # 0x7de4b297
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_hud_color_scheme.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\x18\x17b')  # 0xc0181762
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_hud_color_scheme.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'E\xd7\xa4\x0f')  # 0x45d7a40f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.combat_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'YKD\xcf')  # 0x594b44cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8f^\xbe\xb9')  # 0x8f5ebeb9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_ray_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1+\x1eY')  # 0xf12b1e59
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.thermal_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\xcdcs')  # 0x58cd6373
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xde\x13\x90\x81')  # 0xde139081
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.turret_hud.to_stream(data)
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
            hud_colors=HUDColorsTypedef.from_json(data['hud_colors']),
            misc=Misc.from_json(data['misc']),
            multiplayer=Multiplayer.from_json(data['multiplayer']),
            combat_hud_color_scheme=VisorColorSchemeTypedef.from_json(data['combat_hud_color_scheme']),
            echo_hud_color_scheme=VisorColorSchemeTypedef.from_json(data['echo_hud_color_scheme']),
            scan_hud_color_scheme=VisorColorSchemeTypedef.from_json(data['scan_hud_color_scheme']),
            dark_hud_color_scheme=VisorColorSchemeTypedef.from_json(data['dark_hud_color_scheme']),
            ball_hud_color_scheme=VisorColorSchemeTypedef.from_json(data['ball_hud_color_scheme']),
            combat_hud=HudColorTypedef.from_json(data['combat_hud']),
            scan_hud=HudColorTypedef.from_json(data['scan_hud']),
            x_ray_hud=HudColorTypedef.from_json(data['x_ray_hud']),
            thermal_hud=HudColorTypedef.from_json(data['thermal_hud']),
            ball_hud=HudColorTypedef.from_json(data['ball_hud']),
            turret_hud=TurretHudTypedef.from_json(data['turret_hud']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'hud_colors': self.hud_colors.to_json(),
            'misc': self.misc.to_json(),
            'multiplayer': self.multiplayer.to_json(),
            'combat_hud_color_scheme': self.combat_hud_color_scheme.to_json(),
            'echo_hud_color_scheme': self.echo_hud_color_scheme.to_json(),
            'scan_hud_color_scheme': self.scan_hud_color_scheme.to_json(),
            'dark_hud_color_scheme': self.dark_hud_color_scheme.to_json(),
            'ball_hud_color_scheme': self.ball_hud_color_scheme.to_json(),
            'combat_hud': self.combat_hud.to_json(),
            'scan_hud': self.scan_hud.to_json(),
            'x_ray_hud': self.x_ray_hud.to_json(),
            'thermal_hud': self.thermal_hud.to_json(),
            'ball_hud': self.ball_hud.to_json(),
            'turret_hud': self.turret_hud.to_json(),
        }

    def _dependencies_for_hud_colors(self, asset_manager):
        yield from self.hud_colors.dependencies_for(asset_manager)

    def _dependencies_for_misc(self, asset_manager):
        yield from self.misc.dependencies_for(asset_manager)

    def _dependencies_for_multiplayer(self, asset_manager):
        yield from self.multiplayer.dependencies_for(asset_manager)

    def _dependencies_for_combat_hud_color_scheme(self, asset_manager):
        yield from self.combat_hud_color_scheme.dependencies_for(asset_manager)

    def _dependencies_for_echo_hud_color_scheme(self, asset_manager):
        yield from self.echo_hud_color_scheme.dependencies_for(asset_manager)

    def _dependencies_for_scan_hud_color_scheme(self, asset_manager):
        yield from self.scan_hud_color_scheme.dependencies_for(asset_manager)

    def _dependencies_for_dark_hud_color_scheme(self, asset_manager):
        yield from self.dark_hud_color_scheme.dependencies_for(asset_manager)

    def _dependencies_for_ball_hud_color_scheme(self, asset_manager):
        yield from self.ball_hud_color_scheme.dependencies_for(asset_manager)

    def _dependencies_for_combat_hud(self, asset_manager):
        yield from self.combat_hud.dependencies_for(asset_manager)

    def _dependencies_for_scan_hud(self, asset_manager):
        yield from self.scan_hud.dependencies_for(asset_manager)

    def _dependencies_for_x_ray_hud(self, asset_manager):
        yield from self.x_ray_hud.dependencies_for(asset_manager)

    def _dependencies_for_thermal_hud(self, asset_manager):
        yield from self.thermal_hud.dependencies_for(asset_manager)

    def _dependencies_for_ball_hud(self, asset_manager):
        yield from self.ball_hud.dependencies_for(asset_manager)

    def _dependencies_for_turret_hud(self, asset_manager):
        yield from self.turret_hud.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_hud_colors, "hud_colors", "HUDColorsTypedef"),
            (self._dependencies_for_misc, "misc", "Misc"),
            (self._dependencies_for_multiplayer, "multiplayer", "Multiplayer"),
            (self._dependencies_for_combat_hud_color_scheme, "combat_hud_color_scheme", "VisorColorSchemeTypedef"),
            (self._dependencies_for_echo_hud_color_scheme, "echo_hud_color_scheme", "VisorColorSchemeTypedef"),
            (self._dependencies_for_scan_hud_color_scheme, "scan_hud_color_scheme", "VisorColorSchemeTypedef"),
            (self._dependencies_for_dark_hud_color_scheme, "dark_hud_color_scheme", "VisorColorSchemeTypedef"),
            (self._dependencies_for_ball_hud_color_scheme, "ball_hud_color_scheme", "VisorColorSchemeTypedef"),
            (self._dependencies_for_combat_hud, "combat_hud", "HudColorTypedef"),
            (self._dependencies_for_scan_hud, "scan_hud", "HudColorTypedef"),
            (self._dependencies_for_x_ray_hud, "x_ray_hud", "HudColorTypedef"),
            (self._dependencies_for_thermal_hud, "thermal_hud", "HudColorTypedef"),
            (self._dependencies_for_ball_hud, "ball_hud", "HudColorTypedef"),
            (self._dependencies_for_turret_hud, "turret_hud", "TurretHudTypedef"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakGuiColors.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_hud_colors(data: typing.BinaryIO, property_size: int):
    return HUDColorsTypedef.from_stream(data, property_size)


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_multiplayer(data: typing.BinaryIO, property_size: int):
    return Multiplayer.from_stream(data, property_size)


def _decode_combat_hud_color_scheme(data: typing.BinaryIO, property_size: int):
    return VisorColorSchemeTypedef.from_stream(data, property_size)


def _decode_echo_hud_color_scheme(data: typing.BinaryIO, property_size: int):
    return VisorColorSchemeTypedef.from_stream(data, property_size)


def _decode_scan_hud_color_scheme(data: typing.BinaryIO, property_size: int):
    return VisorColorSchemeTypedef.from_stream(data, property_size)


def _decode_dark_hud_color_scheme(data: typing.BinaryIO, property_size: int):
    return VisorColorSchemeTypedef.from_stream(data, property_size)


def _decode_ball_hud_color_scheme(data: typing.BinaryIO, property_size: int):
    return VisorColorSchemeTypedef.from_stream(data, property_size)


def _decode_combat_hud(data: typing.BinaryIO, property_size: int):
    return HudColorTypedef.from_stream(data, property_size)


def _decode_scan_hud(data: typing.BinaryIO, property_size: int):
    return HudColorTypedef.from_stream(data, property_size)


def _decode_x_ray_hud(data: typing.BinaryIO, property_size: int):
    return HudColorTypedef.from_stream(data, property_size)


def _decode_thermal_hud(data: typing.BinaryIO, property_size: int):
    return HudColorTypedef.from_stream(data, property_size)


def _decode_ball_hud(data: typing.BinaryIO, property_size: int):
    return HudColorTypedef.from_stream(data, property_size)


def _decode_turret_hud(data: typing.BinaryIO, property_size: int):
    return TurretHudTypedef.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0xcb737724: ('hud_colors', _decode_hud_colors),
    0x6756d4de: ('misc', _decode_misc),
    0x697613e9: ('multiplayer', _decode_multiplayer),
    0x67c70055: ('combat_hud_color_scheme', _decode_combat_hud_color_scheme),
    0x62e0a08f: ('echo_hud_color_scheme', _decode_echo_hud_color_scheme),
    0x80becd6e: ('scan_hud_color_scheme', _decode_scan_hud_color_scheme),
    0x7de4b297: ('dark_hud_color_scheme', _decode_dark_hud_color_scheme),
    0xc0181762: ('ball_hud_color_scheme', _decode_ball_hud_color_scheme),
    0x45d7a40f: ('combat_hud', _decode_combat_hud),
    0x594b44cf: ('scan_hud', _decode_scan_hud),
    0x8f5ebeb9: ('x_ray_hud', _decode_x_ray_hud),
    0xf12b1e59: ('thermal_hud', _decode_thermal_hud),
    0x58cd6373: ('ball_hud', _decode_ball_hud),
    0xde139081: ('turret_hud', _decode_turret_hud),
}
