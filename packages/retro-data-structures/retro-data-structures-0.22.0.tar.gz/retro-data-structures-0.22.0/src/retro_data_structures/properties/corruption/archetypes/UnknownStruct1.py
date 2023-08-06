# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    light_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=0.0, a=0.0))
    light_intensity: float = dataclasses.field(default=500.0)
    light_attenuation: float = dataclasses.field(default=0.019999999552965164)
    hover_height: float = dataclasses.field(default=2.0)
    min_rattle_time: float = dataclasses.field(default=0.0)
    max_rattle_time: float = dataclasses.field(default=3.0)
    unknown: float = dataclasses.field(default=10.0)
    max_flight_speed: float = dataclasses.field(default=30.0)
    in_flight_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    landed_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd>\xfe}')  # 0xbd3efe7d
        data.write(b'\x00\x10')  # size
        self.light_color.to_stream(data)

        data.write(b'\xed\xe7\xb3t')  # 0xede7b374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.light_intensity))

        data.write(b'\xd2K\x88\x8f')  # 0xd24b888f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.light_attenuation))

        data.write(b'\xc7Y\x98\xaa')  # 0xc75998aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_height))

        data.write(b'\x80[\xca\xc6')  # 0x805bcac6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_rattle_time))

        data.write(b'\xd3\xfd\xd2"')  # 0xd3fdd222
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_rattle_time))

        data.write(b'\xfa\x08\xf04')  # 0xfa08f034
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xe1\x84\x86\xed')  # 0xe18486ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_flight_speed))

        data.write(b'\x1a\t()')  # 0x1a092829
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.in_flight_sound))

        data.write(b'\x01\x05\xa0/')  # 0x105a02f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.landed_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            light_color=Color.from_json(data['light_color']),
            light_intensity=data['light_intensity'],
            light_attenuation=data['light_attenuation'],
            hover_height=data['hover_height'],
            min_rattle_time=data['min_rattle_time'],
            max_rattle_time=data['max_rattle_time'],
            unknown=data['unknown'],
            max_flight_speed=data['max_flight_speed'],
            in_flight_sound=data['in_flight_sound'],
            landed_sound=data['landed_sound'],
        )

    def to_json(self) -> dict:
        return {
            'character_animation_information': self.character_animation_information.to_json(),
            'light_color': self.light_color.to_json(),
            'light_intensity': self.light_intensity,
            'light_attenuation': self.light_attenuation,
            'hover_height': self.hover_height,
            'min_rattle_time': self.min_rattle_time,
            'max_rattle_time': self.max_rattle_time,
            'unknown': self.unknown,
            'max_flight_speed': self.max_flight_speed,
            'in_flight_sound': self.in_flight_sound,
            'landed_sound': self.landed_sound,
        }


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_light_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_light_intensity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_light_attenuation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_rattle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_rattle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_flight_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_in_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_landed_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xbd3efe7d: ('light_color', _decode_light_color),
    0xede7b374: ('light_intensity', _decode_light_intensity),
    0xd24b888f: ('light_attenuation', _decode_light_attenuation),
    0xc75998aa: ('hover_height', _decode_hover_height),
    0x805bcac6: ('min_rattle_time', _decode_min_rattle_time),
    0xd3fdd222: ('max_rattle_time', _decode_max_rattle_time),
    0xfa08f034: ('unknown', _decode_unknown),
    0xe18486ed: ('max_flight_speed', _decode_max_flight_speed),
    0x1a092829: ('in_flight_sound', _decode_in_flight_sound),
    0x105a02f: ('landed_sound', _decode_landed_sound),
}
