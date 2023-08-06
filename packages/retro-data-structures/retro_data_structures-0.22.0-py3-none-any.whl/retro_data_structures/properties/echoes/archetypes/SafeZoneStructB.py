# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class SafeZoneStructB(BaseProperty):
    turn_on_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0xd4839a3f: float = dataclasses.field(default=0.0)
    active_loop_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    turn_off_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    player_enter_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    player_exit_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    dark_visor_spot_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    dark_visor_spot_max_size: float = dataclasses.field(default=50.0)
    shell_environment_map: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    shell1_animated_horiz_rate: float = dataclasses.field(default=-0.03999999910593033)
    shell1_animated_vert_rate: float = dataclasses.field(default=-0.029999999329447746)
    shell1_scale_horiz: float = dataclasses.field(default=2.0)
    shell1_scale_vert: float = dataclasses.field(default=1.0)
    shell1_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    shell2_animated_horiz_rate: float = dataclasses.field(default=0.0)
    shell2_animated_vert_rate: float = dataclasses.field(default=0.029999999329447746)
    shell2_scale_horiz: float = dataclasses.field(default=3.0)
    shell2_scale_vert: float = dataclasses.field(default=1.0)
    shell2_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    shell_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.09411799907684326, g=0.49803900718688965, b=0.49803900718688965, a=0.0))
    unknown_0xe68b1fa8: Color = dataclasses.field(default_factory=lambda: Color(r=0.749019980430603, g=0.749019980430603, b=0.749019980430603, a=0.0))

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'\xc6\xbf\xc2p')  # 0xc6bfc270
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.turn_on_sound))

        data.write(b'\xd4\x83\x9a?')  # 0xd4839a3f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd4839a3f))

        data.write(b'\xe0\x908%')  # 0xe0903825
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.active_loop_sound))

        data.write(b'\xe5Vy5')  # 0xe5567935
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.turn_off_sound))

        data.write(b'>\x85Hf')  # 0x3e854866
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.player_enter_sound))

        data.write(b'\xd3\xec\t\x93')  # 0xd3ec0993
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.player_exit_sound))

        data.write(b'\xd0\x9f\x83\xe7')  # 0xd09f83e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dark_visor_spot_texture))

        data.write(b'\xc4\x96\xa6\xa8')  # 0xc496a6a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dark_visor_spot_max_size))

        data.write(b't\xf8\xa7)')  # 0x74f8a729
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shell_environment_map))

        data.write(b'R\x13\x82\xc7')  # 0x521382c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell1_animated_horiz_rate))

        data.write(b'\x1b\xe4Bn')  # 0x1be4426e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell1_animated_vert_rate))

        data.write(b'4\xb2\xa1\x90')  # 0x34b2a190
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell1_scale_horiz))

        data.write(b'\xadG\x15\xa8')  # 0xad4715a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell1_scale_vert))

        data.write(b'\x1eq.\xe2')  # 0x1e712ee2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shell1_texture))

        data.write(b'$\xf6\xbb\xfa')  # 0x24f6bbfa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell2_animated_horiz_rate))

        data.write(b'"\x9c\xef.')  # 0x229cef2e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell2_animated_vert_rate))

        data.write(b'\x1dz\x15b')  # 0x1d7a1562
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell2_scale_horiz))

        data.write(b'\xbc:\x7f\xd1')  # 0xbc3a7fd1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell2_scale_vert))

        data.write(b'\xa3\xbbB,')  # 0xa3bb422c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shell2_texture))

        data.write(b'G\xb4\xe8c')  # 0x47b4e863
        data.write(b'\x00\x10')  # size
        self.shell_color.to_stream(data)

        data.write(b'\xe6\x8b\x1f\xa8')  # 0xe68b1fa8
        data.write(b'\x00\x10')  # size
        self.unknown_0xe68b1fa8.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            turn_on_sound=data['turn_on_sound'],
            unknown_0xd4839a3f=data['unknown_0xd4839a3f'],
            active_loop_sound=data['active_loop_sound'],
            turn_off_sound=data['turn_off_sound'],
            player_enter_sound=data['player_enter_sound'],
            player_exit_sound=data['player_exit_sound'],
            dark_visor_spot_texture=data['dark_visor_spot_texture'],
            dark_visor_spot_max_size=data['dark_visor_spot_max_size'],
            shell_environment_map=data['shell_environment_map'],
            shell1_animated_horiz_rate=data['shell1_animated_horiz_rate'],
            shell1_animated_vert_rate=data['shell1_animated_vert_rate'],
            shell1_scale_horiz=data['shell1_scale_horiz'],
            shell1_scale_vert=data['shell1_scale_vert'],
            shell1_texture=data['shell1_texture'],
            shell2_animated_horiz_rate=data['shell2_animated_horiz_rate'],
            shell2_animated_vert_rate=data['shell2_animated_vert_rate'],
            shell2_scale_horiz=data['shell2_scale_horiz'],
            shell2_scale_vert=data['shell2_scale_vert'],
            shell2_texture=data['shell2_texture'],
            shell_color=Color.from_json(data['shell_color']),
            unknown_0xe68b1fa8=Color.from_json(data['unknown_0xe68b1fa8']),
        )

    def to_json(self) -> dict:
        return {
            'turn_on_sound': self.turn_on_sound,
            'unknown_0xd4839a3f': self.unknown_0xd4839a3f,
            'active_loop_sound': self.active_loop_sound,
            'turn_off_sound': self.turn_off_sound,
            'player_enter_sound': self.player_enter_sound,
            'player_exit_sound': self.player_exit_sound,
            'dark_visor_spot_texture': self.dark_visor_spot_texture,
            'dark_visor_spot_max_size': self.dark_visor_spot_max_size,
            'shell_environment_map': self.shell_environment_map,
            'shell1_animated_horiz_rate': self.shell1_animated_horiz_rate,
            'shell1_animated_vert_rate': self.shell1_animated_vert_rate,
            'shell1_scale_horiz': self.shell1_scale_horiz,
            'shell1_scale_vert': self.shell1_scale_vert,
            'shell1_texture': self.shell1_texture,
            'shell2_animated_horiz_rate': self.shell2_animated_horiz_rate,
            'shell2_animated_vert_rate': self.shell2_animated_vert_rate,
            'shell2_scale_horiz': self.shell2_scale_horiz,
            'shell2_scale_vert': self.shell2_scale_vert,
            'shell2_texture': self.shell2_texture,
            'shell_color': self.shell_color.to_json(),
            'unknown_0xe68b1fa8': self.unknown_0xe68b1fa8.to_json(),
        }

    def _dependencies_for_turn_on_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.turn_on_sound)

    def _dependencies_for_active_loop_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.active_loop_sound)

    def _dependencies_for_turn_off_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.turn_off_sound)

    def _dependencies_for_player_enter_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.player_enter_sound)

    def _dependencies_for_player_exit_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.player_exit_sound)

    def _dependencies_for_dark_visor_spot_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dark_visor_spot_texture)

    def _dependencies_for_shell_environment_map(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shell_environment_map)

    def _dependencies_for_shell1_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shell1_texture)

    def _dependencies_for_shell2_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shell2_texture)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_turn_on_sound, "turn_on_sound", "int"),
            (self._dependencies_for_active_loop_sound, "active_loop_sound", "int"),
            (self._dependencies_for_turn_off_sound, "turn_off_sound", "int"),
            (self._dependencies_for_player_enter_sound, "player_enter_sound", "int"),
            (self._dependencies_for_player_exit_sound, "player_exit_sound", "int"),
            (self._dependencies_for_dark_visor_spot_texture, "dark_visor_spot_texture", "AssetId"),
            (self._dependencies_for_shell_environment_map, "shell_environment_map", "AssetId"),
            (self._dependencies_for_shell1_texture, "shell1_texture", "AssetId"),
            (self._dependencies_for_shell2_texture, "shell2_texture", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SafeZoneStructB.{field_name} ({field_type}): {e}"
                )


def _decode_turn_on_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd4839a3f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_active_loop_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_turn_off_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_player_enter_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_player_exit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_visor_spot_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_dark_visor_spot_max_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell_environment_map(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shell1_animated_horiz_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell1_animated_vert_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell1_scale_horiz(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell1_scale_vert(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell1_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shell2_animated_horiz_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell2_animated_vert_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell2_scale_horiz(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell2_scale_vert(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell2_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shell_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe68b1fa8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc6bfc270: ('turn_on_sound', _decode_turn_on_sound),
    0xd4839a3f: ('unknown_0xd4839a3f', _decode_unknown_0xd4839a3f),
    0xe0903825: ('active_loop_sound', _decode_active_loop_sound),
    0xe5567935: ('turn_off_sound', _decode_turn_off_sound),
    0x3e854866: ('player_enter_sound', _decode_player_enter_sound),
    0xd3ec0993: ('player_exit_sound', _decode_player_exit_sound),
    0xd09f83e7: ('dark_visor_spot_texture', _decode_dark_visor_spot_texture),
    0xc496a6a8: ('dark_visor_spot_max_size', _decode_dark_visor_spot_max_size),
    0x74f8a729: ('shell_environment_map', _decode_shell_environment_map),
    0x521382c7: ('shell1_animated_horiz_rate', _decode_shell1_animated_horiz_rate),
    0x1be4426e: ('shell1_animated_vert_rate', _decode_shell1_animated_vert_rate),
    0x34b2a190: ('shell1_scale_horiz', _decode_shell1_scale_horiz),
    0xad4715a8: ('shell1_scale_vert', _decode_shell1_scale_vert),
    0x1e712ee2: ('shell1_texture', _decode_shell1_texture),
    0x24f6bbfa: ('shell2_animated_horiz_rate', _decode_shell2_animated_horiz_rate),
    0x229cef2e: ('shell2_animated_vert_rate', _decode_shell2_animated_vert_rate),
    0x1d7a1562: ('shell2_scale_horiz', _decode_shell2_scale_horiz),
    0xbc3a7fd1: ('shell2_scale_vert', _decode_shell2_scale_vert),
    0xa3bb422c: ('shell2_texture', _decode_shell2_texture),
    0x47b4e863: ('shell_color', _decode_shell_color),
    0xe68b1fa8: ('unknown_0xe68b1fa8', _decode_unknown_0xe68b1fa8),
}
