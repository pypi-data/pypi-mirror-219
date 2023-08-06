# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class PlasmaBeamInfo(BaseProperty):
    unknown: int = dataclasses.field(default=0)
    weapon_system: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    contact_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    pulse_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    beam_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    glow_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    length: float = dataclasses.field(default=10.0)
    radius: float = dataclasses.field(default=0.10000000149011612)
    expansion_speed: float = dataclasses.field(default=1.0)
    life_time: float = dataclasses.field(default=10.0)
    pulse_speed: float = dataclasses.field(default=10.0)
    shutdown_time: float = dataclasses.field(default=1.0)
    contact_effect_scale: float = dataclasses.field(default=1.0)
    pulse_effect_scale: float = dataclasses.field(default=1.0)
    travel_speed: float = dataclasses.field(default=150.0)
    inner_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    outer_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    beam_streaks: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\xffq:\xad')  # 0xff713aad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'E\x9a\xe4\xa8')  # 0x459ae4a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.weapon_system))

        data.write(b'O8|I')  # 0x4f387c49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.contact_effect))

        data.write(b'\xdd\xd5.:')  # 0xddd52e3a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.pulse_effect))

        data.write(b'\xc6\xf2)\xc6')  # 0xc6f229c6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.beam_texture))

        data.write(b'\x8f\x1av\xc3')  # 0x8f1a76c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.glow_texture))

        data.write(b'\xc2l)\x1c')  # 0xc26c291c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.length))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\xecw=\x1d')  # 0xec773d1d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.expansion_speed))

        data.write(b'\xb0-\xe5U')  # 0xb02de555
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.life_time))

        data.write(b'Q\x80\x18\x1e')  # 0x5180181e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pulse_speed))

        data.write(b'r\xa9bR')  # 0x72a96252
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shutdown_time))

        data.write(b'\x85^\xd9\xb9')  # 0x855ed9b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.contact_effect_scale))

        data.write(b'\xb8e/\xe4')  # 0xb8652fe4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pulse_effect_scale))

        data.write(b'?\xed^R')  # 0x3fed5e52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.travel_speed))

        data.write(b'\x1a\xfb+s')  # 0x1afb2b73
        data.write(b'\x00\x10')  # size
        self.inner_color.to_stream(data)

        data.write(b'\x9f\xd38\xfc')  # 0x9fd338fc
        data.write(b'\x00\x10')  # size
        self.outer_color.to_stream(data)

        data.write(b'\xae\xb3\x1a\xf3')  # 0xaeb31af3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.beam_streaks))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            weapon_system=data['weapon_system'],
            contact_effect=data['contact_effect'],
            pulse_effect=data['pulse_effect'],
            beam_texture=data['beam_texture'],
            glow_texture=data['glow_texture'],
            length=data['length'],
            radius=data['radius'],
            expansion_speed=data['expansion_speed'],
            life_time=data['life_time'],
            pulse_speed=data['pulse_speed'],
            shutdown_time=data['shutdown_time'],
            contact_effect_scale=data['contact_effect_scale'],
            pulse_effect_scale=data['pulse_effect_scale'],
            travel_speed=data['travel_speed'],
            inner_color=Color.from_json(data['inner_color']),
            outer_color=Color.from_json(data['outer_color']),
            beam_streaks=data['beam_streaks'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'weapon_system': self.weapon_system,
            'contact_effect': self.contact_effect,
            'pulse_effect': self.pulse_effect,
            'beam_texture': self.beam_texture,
            'glow_texture': self.glow_texture,
            'length': self.length,
            'radius': self.radius,
            'expansion_speed': self.expansion_speed,
            'life_time': self.life_time,
            'pulse_speed': self.pulse_speed,
            'shutdown_time': self.shutdown_time,
            'contact_effect_scale': self.contact_effect_scale,
            'pulse_effect_scale': self.pulse_effect_scale,
            'travel_speed': self.travel_speed,
            'inner_color': self.inner_color.to_json(),
            'outer_color': self.outer_color.to_json(),
            'beam_streaks': self.beam_streaks,
        }

    def _dependencies_for_weapon_system(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.weapon_system)

    def _dependencies_for_contact_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.contact_effect)

    def _dependencies_for_pulse_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.pulse_effect)

    def _dependencies_for_beam_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.beam_texture)

    def _dependencies_for_glow_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.glow_texture)

    def _dependencies_for_beam_streaks(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.beam_streaks)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_weapon_system, "weapon_system", "AssetId"),
            (self._dependencies_for_contact_effect, "contact_effect", "AssetId"),
            (self._dependencies_for_pulse_effect, "pulse_effect", "AssetId"),
            (self._dependencies_for_beam_texture, "beam_texture", "AssetId"),
            (self._dependencies_for_glow_texture, "glow_texture", "AssetId"),
            (self._dependencies_for_beam_streaks, "beam_streaks", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PlasmaBeamInfo.{field_name} ({field_type}): {e}"
                )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_weapon_system(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_contact_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_pulse_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_beam_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_glow_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_expansion_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pulse_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shutdown_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_effect_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pulse_effect_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_travel_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_inner_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_outer_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_beam_streaks(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xff713aad: ('unknown', _decode_unknown),
    0x459ae4a8: ('weapon_system', _decode_weapon_system),
    0x4f387c49: ('contact_effect', _decode_contact_effect),
    0xddd52e3a: ('pulse_effect', _decode_pulse_effect),
    0xc6f229c6: ('beam_texture', _decode_beam_texture),
    0x8f1a76c3: ('glow_texture', _decode_glow_texture),
    0xc26c291c: ('length', _decode_length),
    0x78c507eb: ('radius', _decode_radius),
    0xec773d1d: ('expansion_speed', _decode_expansion_speed),
    0xb02de555: ('life_time', _decode_life_time),
    0x5180181e: ('pulse_speed', _decode_pulse_speed),
    0x72a96252: ('shutdown_time', _decode_shutdown_time),
    0x855ed9b9: ('contact_effect_scale', _decode_contact_effect_scale),
    0xb8652fe4: ('pulse_effect_scale', _decode_pulse_effect_scale),
    0x3fed5e52: ('travel_speed', _decode_travel_speed),
    0x1afb2b73: ('inner_color', _decode_inner_color),
    0x9fd338fc: ('outer_color', _decode_outer_color),
    0xaeb31af3: ('beam_streaks', _decode_beam_streaks),
}
