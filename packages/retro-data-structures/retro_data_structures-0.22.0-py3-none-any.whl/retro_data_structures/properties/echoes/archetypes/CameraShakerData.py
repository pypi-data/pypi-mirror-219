# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class CameraShakerData(BaseProperty):
    flags_camera_shaker: int = dataclasses.field(default=16)  # Flagset
    attenuation_distance: float = dataclasses.field(default=5.0)
    horizontal_motion: Spline = dataclasses.field(default_factory=Spline)
    vertical_motion: Spline = dataclasses.field(default_factory=Spline)
    forward_motion: Spline = dataclasses.field(default_factory=Spline)
    duration: float = dataclasses.field(default=1.0)
    audio_effect: int = dataclasses.field(default=0, metadata={'sound': True})

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xc3\xe7\\_')  # 0xc3e75c5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_camera_shaker))

        data.write(b'M(:\xc5')  # 0x4d283ac5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attenuation_distance))

        data.write(b'\xf1"\xcd\x97')  # 0xf122cd97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.horizontal_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b")'\xe5D")  # 0x2927e544
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vertical_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xfaFx')  # 0x7cfa4678
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forward_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'8\x8d.F')  # 0x388d2e46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.audio_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_camera_shaker=data['flags_camera_shaker'],
            attenuation_distance=data['attenuation_distance'],
            horizontal_motion=Spline.from_json(data['horizontal_motion']),
            vertical_motion=Spline.from_json(data['vertical_motion']),
            forward_motion=Spline.from_json(data['forward_motion']),
            duration=data['duration'],
            audio_effect=data['audio_effect'],
        )

    def to_json(self) -> dict:
        return {
            'flags_camera_shaker': self.flags_camera_shaker,
            'attenuation_distance': self.attenuation_distance,
            'horizontal_motion': self.horizontal_motion.to_json(),
            'vertical_motion': self.vertical_motion.to_json(),
            'forward_motion': self.forward_motion.to_json(),
            'duration': self.duration,
            'audio_effect': self.audio_effect,
        }

    def _dependencies_for_audio_effect(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.audio_effect)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_audio_effect, "audio_effect", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for CameraShakerData.{field_name} ({field_type}): {e}"
                )


def _decode_flags_camera_shaker(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attenuation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_vertical_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_forward_motion(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc3e75c5f: ('flags_camera_shaker', _decode_flags_camera_shaker),
    0x4d283ac5: ('attenuation_distance', _decode_attenuation_distance),
    0xf122cd97: ('horizontal_motion', _decode_horizontal_motion),
    0x2927e544: ('vertical_motion', _decode_vertical_motion),
    0x7cfa4678: ('forward_motion', _decode_forward_motion),
    0x8b51e23f: ('duration', _decode_duration),
    0x388d2e46: ('audio_effect', _decode_audio_effect),
}
