# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class StackableBlockBehaviorData(BaseProperty):
    solid_for_roll: bool = dataclasses.field(default=False)
    push_impulse: float = dataclasses.field(default=1000.0)
    disable_physics: bool = dataclasses.field(default=False)
    replace_collision_when_deactivated: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x1d\xf1\xc4\xd1')  # 0x1df1c4d1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.solid_for_roll))

        data.write(b'[\xb5\x9a;')  # 0x5bb59a3b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.push_impulse))

        data.write(b'\xe1Z\x93\xd0')  # 0xe15a93d0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_physics))

        data.write(b'}\xba\xcfz')  # 0x7dbacf7a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.replace_collision_when_deactivated))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            solid_for_roll=data['solid_for_roll'],
            push_impulse=data['push_impulse'],
            disable_physics=data['disable_physics'],
            replace_collision_when_deactivated=data['replace_collision_when_deactivated'],
        )

    def to_json(self) -> dict:
        return {
            'solid_for_roll': self.solid_for_roll,
            'push_impulse': self.push_impulse,
            'disable_physics': self.disable_physics,
            'replace_collision_when_deactivated': self.replace_collision_when_deactivated,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x1df1c4d1, 0x5bb59a3b, 0xe15a93d0, 0x7dbacf7a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[StackableBlockBehaviorData]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(31))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return StackableBlockBehaviorData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_solid_for_roll(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_push_impulse(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_physics(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_replace_collision_when_deactivated(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1df1c4d1: ('solid_for_roll', _decode_solid_for_roll),
    0x5bb59a3b: ('push_impulse', _decode_push_impulse),
    0xe15a93d0: ('disable_physics', _decode_disable_physics),
    0x7dbacf7a: ('replace_collision_when_deactivated', _decode_replace_collision_when_deactivated),
}
