# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.echoes as enums
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class LightParameters(BaseProperty):
    cast_shadow: bool = dataclasses.field(default=True)
    shadow_scale: float = dataclasses.field(default=1.0)
    unknown_0xecda4163: int = dataclasses.field(default=0)
    shadow_alpha: float = dataclasses.field(default=1.0)
    max_shadow_height: float = dataclasses.field(default=20.0)
    ambient_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    unknown_0xa71810e9: bool = dataclasses.field(default=True)
    world_lighting_options: enums.WorldLightingOptions = dataclasses.field(default=enums.WorldLightingOptions.NormalWorldLighting)
    light_recalculation: int = dataclasses.field(default=1)  # Choice
    lighting_position_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    num_dynamic_lights: int = dataclasses.field(default=4)
    num_area_lights: int = dataclasses.field(default=4)
    use_old_lighting: bool = dataclasses.field(default=False)
    ignore_ambient_lighting: bool = dataclasses.field(default=False)
    use_light_set: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\xcdc\x9bF')  # 0xcd639b46
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.cast_shadow))

        data.write(b'\x1d\x01\x1a9')  # 0x1d011a39
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_scale))

        data.write(b'\xec\xdaAc')  # 0xecda4163
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xecda4163))

        data.write(b'>,\xd3\x8d')  # 0x3e2cd38d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_alpha))

        data.write(b'\x03(\xe3\x1b')  # 0x328e31b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_shadow_height))

        data.write(b'\xa3>[\x0e')  # 0xa33e5b0e
        data.write(b'\x00\x10')  # size
        self.ambient_color.to_stream(data)

        data.write(b'\xa7\x18\x10\xe9')  # 0xa71810e9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa71810e9))

        data.write(b'k^u\t')  # 0x6b5e7509
        data.write(b'\x00\x04')  # size
        self.world_lighting_options.to_stream(data)

        data.write(b'b\x8ej\xc3')  # 0x628e6ac3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.light_recalculation))

        data.write(b'\xd1\x9d\xe7u')  # 0xd19de775
        data.write(b'\x00\x0c')  # size
        self.lighting_position_offset.to_stream(data)

        data.write(b'\xca\xc1\xe7x')  # 0xcac1e778
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_dynamic_lights))

        data.write(b'g\xf4\xd3\xde')  # 0x67f4d3de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_area_lights))

        data.write(b'\xfbzz\xbb')  # 0xfb7a7abb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_old_lighting))

        data.write(b'a\xa9@\xd6')  # 0x61a940d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_ambient_lighting))

        data.write(b'\x1fq_\xd3')  # 0x1f715fd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.use_light_set))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cast_shadow=data['cast_shadow'],
            shadow_scale=data['shadow_scale'],
            unknown_0xecda4163=data['unknown_0xecda4163'],
            shadow_alpha=data['shadow_alpha'],
            max_shadow_height=data['max_shadow_height'],
            ambient_color=Color.from_json(data['ambient_color']),
            unknown_0xa71810e9=data['unknown_0xa71810e9'],
            world_lighting_options=enums.WorldLightingOptions.from_json(data['world_lighting_options']),
            light_recalculation=data['light_recalculation'],
            lighting_position_offset=Vector.from_json(data['lighting_position_offset']),
            num_dynamic_lights=data['num_dynamic_lights'],
            num_area_lights=data['num_area_lights'],
            use_old_lighting=data['use_old_lighting'],
            ignore_ambient_lighting=data['ignore_ambient_lighting'],
            use_light_set=data['use_light_set'],
        )

    def to_json(self) -> dict:
        return {
            'cast_shadow': self.cast_shadow,
            'shadow_scale': self.shadow_scale,
            'unknown_0xecda4163': self.unknown_0xecda4163,
            'shadow_alpha': self.shadow_alpha,
            'max_shadow_height': self.max_shadow_height,
            'ambient_color': self.ambient_color.to_json(),
            'unknown_0xa71810e9': self.unknown_0xa71810e9,
            'world_lighting_options': self.world_lighting_options.to_json(),
            'light_recalculation': self.light_recalculation,
            'lighting_position_offset': self.lighting_position_offset.to_json(),
            'num_dynamic_lights': self.num_dynamic_lights,
            'num_area_lights': self.num_area_lights,
            'use_old_lighting': self.use_old_lighting,
            'ignore_ambient_lighting': self.ignore_ambient_lighting,
            'use_light_set': self.use_light_set,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_cast_shadow(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shadow_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xecda4163(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_shadow_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_shadow_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ambient_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa71810e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_world_lighting_options(data: typing.BinaryIO, property_size: int):
    return enums.WorldLightingOptions.from_stream(data)


def _decode_light_recalculation(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_lighting_position_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_num_dynamic_lights(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_num_area_lights(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_use_old_lighting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_ambient_lighting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_light_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcd639b46: ('cast_shadow', _decode_cast_shadow),
    0x1d011a39: ('shadow_scale', _decode_shadow_scale),
    0xecda4163: ('unknown_0xecda4163', _decode_unknown_0xecda4163),
    0x3e2cd38d: ('shadow_alpha', _decode_shadow_alpha),
    0x328e31b: ('max_shadow_height', _decode_max_shadow_height),
    0xa33e5b0e: ('ambient_color', _decode_ambient_color),
    0xa71810e9: ('unknown_0xa71810e9', _decode_unknown_0xa71810e9),
    0x6b5e7509: ('world_lighting_options', _decode_world_lighting_options),
    0x628e6ac3: ('light_recalculation', _decode_light_recalculation),
    0xd19de775: ('lighting_position_offset', _decode_lighting_position_offset),
    0xcac1e778: ('num_dynamic_lights', _decode_num_dynamic_lights),
    0x67f4d3de: ('num_area_lights', _decode_num_area_lights),
    0xfb7a7abb: ('use_old_lighting', _decode_use_old_lighting),
    0x61a940d6: ('ignore_ambient_lighting', _decode_ignore_ambient_lighting),
    0x1f715fd3: ('use_light_set', _decode_use_light_set),
}
