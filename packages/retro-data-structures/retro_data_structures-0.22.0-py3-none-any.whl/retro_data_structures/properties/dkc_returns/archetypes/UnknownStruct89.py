# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.AnimGridModifierData import AnimGridModifierData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct85 import UnknownStruct85
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct86 import UnknownStruct86
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct87 import UnknownStruct87
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct88 import UnknownStruct88


@dataclasses.dataclass()
class UnknownStruct89(BaseProperty):
    gravity: float = dataclasses.field(default=55.0)
    snap_to_spline: bool = dataclasses.field(default=True)
    unknown_0xdaccc7de: bool = dataclasses.field(default=True)
    unknown_0xcff6090d: float = dataclasses.field(default=5.0)
    disable_attack_time: float = dataclasses.field(default=0.6600000262260437)
    minimum_toss_distance: float = dataclasses.field(default=10.0)
    unknown_0xedf6ba25: float = dataclasses.field(default=3.0)
    unknown_0x268ea25f: int = dataclasses.field(default=5)
    anger_duration: float = dataclasses.field(default=3.5)
    anim_grid: AnimGridModifierData = dataclasses.field(default_factory=AnimGridModifierData)
    unknown_struct85: UnknownStruct85 = dataclasses.field(default_factory=UnknownStruct85)
    unknown_struct86: UnknownStruct86 = dataclasses.field(default_factory=UnknownStruct86)
    unknown_struct87: UnknownStruct87 = dataclasses.field(default_factory=UnknownStruct87)
    unknown_struct88: UnknownStruct88 = dataclasses.field(default_factory=UnknownStruct88)

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'\xda\xcc\xc7\xde')  # 0xdaccc7de
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdaccc7de))

        data.write(b'\xcf\xf6\t\r')  # 0xcff6090d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcff6090d))

        data.write(b'wJ\xc8<')  # 0x774ac83c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_attack_time))

        data.write(b'{\x95\xabG')  # 0x7b95ab47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_toss_distance))

        data.write(b'\xed\xf6\xba%')  # 0xedf6ba25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xedf6ba25))

        data.write(b'&\x8e\xa2_')  # 0x268ea25f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x268ea25f))

        data.write(b': \xfb\x9b')  # 0x3a20fb9b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anger_duration))

        data.write(b'h\xfdI\xae')  # 0x68fd49ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.anim_grid.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xa8\x1fD')  # 0xa81f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct85.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xac\xee\xf4+')  # 0xaceef42b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct86.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1ed\xb8\xdf')  # 0x1e64b8df
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x04\xde\xdf\x14')  # 0x4dedf14
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct88.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gravity=data['gravity'],
            snap_to_spline=data['snap_to_spline'],
            unknown_0xdaccc7de=data['unknown_0xdaccc7de'],
            unknown_0xcff6090d=data['unknown_0xcff6090d'],
            disable_attack_time=data['disable_attack_time'],
            minimum_toss_distance=data['minimum_toss_distance'],
            unknown_0xedf6ba25=data['unknown_0xedf6ba25'],
            unknown_0x268ea25f=data['unknown_0x268ea25f'],
            anger_duration=data['anger_duration'],
            anim_grid=AnimGridModifierData.from_json(data['anim_grid']),
            unknown_struct85=UnknownStruct85.from_json(data['unknown_struct85']),
            unknown_struct86=UnknownStruct86.from_json(data['unknown_struct86']),
            unknown_struct87=UnknownStruct87.from_json(data['unknown_struct87']),
            unknown_struct88=UnknownStruct88.from_json(data['unknown_struct88']),
        )

    def to_json(self) -> dict:
        return {
            'gravity': self.gravity,
            'snap_to_spline': self.snap_to_spline,
            'unknown_0xdaccc7de': self.unknown_0xdaccc7de,
            'unknown_0xcff6090d': self.unknown_0xcff6090d,
            'disable_attack_time': self.disable_attack_time,
            'minimum_toss_distance': self.minimum_toss_distance,
            'unknown_0xedf6ba25': self.unknown_0xedf6ba25,
            'unknown_0x268ea25f': self.unknown_0x268ea25f,
            'anger_duration': self.anger_duration,
            'anim_grid': self.anim_grid.to_json(),
            'unknown_struct85': self.unknown_struct85.to_json(),
            'unknown_struct86': self.unknown_struct86.to_json(),
            'unknown_struct87': self.unknown_struct87.to_json(),
            'unknown_struct88': self.unknown_struct88.to_json(),
        }


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xdaccc7de(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xcff6090d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_toss_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xedf6ba25(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x268ea25f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_anger_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_anim_grid(data: typing.BinaryIO, property_size: int):
    return AnimGridModifierData.from_stream(data, property_size)


def _decode_unknown_struct85(data: typing.BinaryIO, property_size: int):
    return UnknownStruct85.from_stream(data, property_size)


def _decode_unknown_struct86(data: typing.BinaryIO, property_size: int):
    return UnknownStruct86.from_stream(data, property_size)


def _decode_unknown_struct87(data: typing.BinaryIO, property_size: int):
    return UnknownStruct87.from_stream(data, property_size)


def _decode_unknown_struct88(data: typing.BinaryIO, property_size: int):
    return UnknownStruct88.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0xdaccc7de: ('unknown_0xdaccc7de', _decode_unknown_0xdaccc7de),
    0xcff6090d: ('unknown_0xcff6090d', _decode_unknown_0xcff6090d),
    0x774ac83c: ('disable_attack_time', _decode_disable_attack_time),
    0x7b95ab47: ('minimum_toss_distance', _decode_minimum_toss_distance),
    0xedf6ba25: ('unknown_0xedf6ba25', _decode_unknown_0xedf6ba25),
    0x268ea25f: ('unknown_0x268ea25f', _decode_unknown_0x268ea25f),
    0x3a20fb9b: ('anger_duration', _decode_anger_duration),
    0x68fd49ae: ('anim_grid', _decode_anim_grid),
    0xa81f44: ('unknown_struct85', _decode_unknown_struct85),
    0xaceef42b: ('unknown_struct86', _decode_unknown_struct86),
    0x1e64b8df: ('unknown_struct87', _decode_unknown_struct87),
    0x4dedf14: ('unknown_struct88', _decode_unknown_struct88),
}
