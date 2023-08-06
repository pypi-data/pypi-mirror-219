# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.CameraShakerEnvelope import CameraShakerEnvelope
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class CameraShakerData(BaseProperty):
    flags_camera_shaker: int = dataclasses.field(default=528)
    attenuation_distance: float = dataclasses.field(default=5.0)
    duration: float = dataclasses.field(default=1.0)
    audio_effect: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    horizontal_motion: CameraShakerEnvelope = dataclasses.field(default_factory=CameraShakerEnvelope)
    vertical_motion: CameraShakerEnvelope = dataclasses.field(default_factory=CameraShakerEnvelope)
    forward_motion: CameraShakerEnvelope = dataclasses.field(default_factory=CameraShakerEnvelope)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xc3\xe7\\_')  # 0xc3e75c5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_camera_shaker))

        data.write(b'M(:\xc5')  # 0x4d283ac5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attenuation_distance))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\xc2\xac\xb7\x9e')  # 0xc2acb79e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.audio_effect))

        data.write(b'\xd9\xebq\xe0')  # 0xd9eb71e0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.horizontal_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\xb0\x962')  # 0xc5b09632
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vertical_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\xb7\x04\xe3')  # 0x21b704e3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forward_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_camera_shaker=data['flags_camera_shaker'],
            attenuation_distance=data['attenuation_distance'],
            duration=data['duration'],
            audio_effect=data['audio_effect'],
            horizontal_motion=CameraShakerEnvelope.from_json(data['horizontal_motion']),
            vertical_motion=CameraShakerEnvelope.from_json(data['vertical_motion']),
            forward_motion=CameraShakerEnvelope.from_json(data['forward_motion']),
        )

    def to_json(self) -> dict:
        return {
            'flags_camera_shaker': self.flags_camera_shaker,
            'attenuation_distance': self.attenuation_distance,
            'duration': self.duration,
            'audio_effect': self.audio_effect,
            'horizontal_motion': self.horizontal_motion.to_json(),
            'vertical_motion': self.vertical_motion.to_json(),
            'forward_motion': self.forward_motion.to_json(),
        }


def _decode_flags_camera_shaker(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_attenuation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_horizontal_motion(data: typing.BinaryIO, property_size: int):
    return CameraShakerEnvelope.from_stream(data, property_size)


def _decode_vertical_motion(data: typing.BinaryIO, property_size: int):
    return CameraShakerEnvelope.from_stream(data, property_size)


def _decode_forward_motion(data: typing.BinaryIO, property_size: int):
    return CameraShakerEnvelope.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc3e75c5f: ('flags_camera_shaker', _decode_flags_camera_shaker),
    0x4d283ac5: ('attenuation_distance', _decode_attenuation_distance),
    0x8b51e23f: ('duration', _decode_duration),
    0xc2acb79e: ('audio_effect', _decode_audio_effect),
    0xd9eb71e0: ('horizontal_motion', _decode_horizontal_motion),
    0xc5b09632: ('vertical_motion', _decode_vertical_motion),
    0x21b704e3: ('forward_motion', _decode_forward_motion),
}
