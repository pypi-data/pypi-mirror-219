# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class LockFire(BaseProperty):
    lock_fire_reticle_scale: float = dataclasses.field(default=1.0)
    lock_fire_anim_time: float = dataclasses.field(default=0.30000001192092896)
    lock_fire_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xd4\xe5\x9eY')  # 0xd4e59e59
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_fire_reticle_scale))

        data.write(b'\xb7\x9d\xe7\xe8')  # 0xb79de7e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_fire_anim_time))

        data.write(b'\xf5\xe9\x89\x9f')  # 0xf5e9899f
        data.write(b'\x00\x10')  # size
        self.lock_fire_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            lock_fire_reticle_scale=data['lock_fire_reticle_scale'],
            lock_fire_anim_time=data['lock_fire_anim_time'],
            lock_fire_color=Color.from_json(data['lock_fire_color']),
        )

    def to_json(self) -> dict:
        return {
            'lock_fire_reticle_scale': self.lock_fire_reticle_scale,
            'lock_fire_anim_time': self.lock_fire_anim_time,
            'lock_fire_color': self.lock_fire_color.to_json(),
        }


def _decode_lock_fire_reticle_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_fire_anim_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_fire_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd4e59e59: ('lock_fire_reticle_scale', _decode_lock_fire_reticle_scale),
    0xb79de7e8: ('lock_fire_anim_time', _decode_lock_fire_anim_time),
    0xf5e9899f: ('lock_fire_color', _decode_lock_fire_color),
}
