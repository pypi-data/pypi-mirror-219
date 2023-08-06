# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.TriggerInfo import TriggerInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Steam(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    trigger: TriggerInfo = dataclasses.field(default_factory=TriggerInfo)
    steam: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    strength: float = dataclasses.field(default=0.3499999940395355)
    fade_in_rate: float = dataclasses.field(default=1.0)
    fade_out_rate: float = dataclasses.field(default=2.0)
    radius: float = dataclasses.field(default=0.0)
    unknown_0xa366c949: bool = dataclasses.field(default=False)
    unknown_0x606539fa: bool = dataclasses.field(default=False)
    filter_shape: enums.FilterShape = dataclasses.field(default=enums.FilterShape.Unknown1)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'STEM'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\n')  # 10 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\xa2t\x11')  # 0x77a27411
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.trigger.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&4`P')  # 0x26346050
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.steam))

        data.write(b'O\x8f_\\')  # 0x4f8f5f5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.strength))

        data.write(b'\xc2\x13\x8f=')  # 0xc2138f3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_rate))

        data.write(b'.\x9f%\x9e')  # 0x2e9f259e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_rate))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\xa3f\xc9I')  # 0xa366c949
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa366c949))

        data.write(b'`e9\xfa')  # 0x606539fa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x606539fa))

        data.write(b'\x92\x86\x90R')  # 0x92869052
        data.write(b'\x00\x04')  # size
        self.filter_shape.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            trigger=TriggerInfo.from_json(data['trigger']),
            steam=data['steam'],
            strength=data['strength'],
            fade_in_rate=data['fade_in_rate'],
            fade_out_rate=data['fade_out_rate'],
            radius=data['radius'],
            unknown_0xa366c949=data['unknown_0xa366c949'],
            unknown_0x606539fa=data['unknown_0x606539fa'],
            filter_shape=enums.FilterShape.from_json(data['filter_shape']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'trigger': self.trigger.to_json(),
            'steam': self.steam,
            'strength': self.strength,
            'fade_in_rate': self.fade_in_rate,
            'fade_out_rate': self.fade_out_rate,
            'radius': self.radius,
            'unknown_0xa366c949': self.unknown_0xa366c949,
            'unknown_0x606539fa': self.unknown_0x606539fa,
            'filter_shape': self.filter_shape.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_trigger(data: typing.BinaryIO, property_size: int):
    return TriggerInfo.from_stream(data, property_size)


def _decode_steam(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strength(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa366c949(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x606539fa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_filter_shape(data: typing.BinaryIO, property_size: int):
    return enums.FilterShape.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x77a27411: ('trigger', _decode_trigger),
    0x26346050: ('steam', _decode_steam),
    0x4f8f5f5c: ('strength', _decode_strength),
    0xc2138f3d: ('fade_in_rate', _decode_fade_in_rate),
    0x2e9f259e: ('fade_out_rate', _decode_fade_out_rate),
    0x78c507eb: ('radius', _decode_radius),
    0xa366c949: ('unknown_0xa366c949', _decode_unknown_0xa366c949),
    0x606539fa: ('unknown_0x606539fa', _decode_unknown_0x606539fa),
    0x92869052: ('filter_shape', _decode_filter_shape),
}
