# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct38(BaseProperty):
    range: float = dataclasses.field(default=20.0)
    turn_rate: float = dataclasses.field(default=180.0)
    sound_effect: int = dataclasses.field(default=0, metadata={'sound': True})
    warp_scale: float = dataclasses.field(default=5.0)
    repel_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=1.0, z=5.0))

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'6B\xa3\x98')  # 0x3642a398
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.range))

        data.write(b'\xe3M\xc7\x03')  # 0xe34dc703
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_rate))

        data.write(b'\x8d;\xa8\xae')  # 0x8d3ba8ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_effect))

        data.write(b'\xb9\x90\x98\xd9')  # 0xb99098d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warp_scale))

        data.write(b'\xb3%#$')  # 0xb3252324
        data.write(b'\x00\x0c')  # size
        self.repel_offset.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            range=data['range'],
            turn_rate=data['turn_rate'],
            sound_effect=data['sound_effect'],
            warp_scale=data['warp_scale'],
            repel_offset=Vector.from_json(data['repel_offset']),
        )

    def to_json(self) -> dict:
        return {
            'range': self.range,
            'turn_rate': self.turn_rate,
            'sound_effect': self.sound_effect,
            'warp_scale': self.warp_scale,
            'repel_offset': self.repel_offset.to_json(),
        }

    def _dependencies_for_sound_effect(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_effect)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_sound_effect, "sound_effect", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct38.{field_name} ({field_type}): {e}"
                )


def _decode_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_warp_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_repel_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3642a398: ('range', _decode_range),
    0xe34dc703: ('turn_rate', _decode_turn_rate),
    0x8d3ba8ae: ('sound_effect', _decode_sound_effect),
    0xb99098d9: ('warp_scale', _decode_warp_scale),
    0xb3252324: ('repel_offset', _decode_repel_offset),
}
