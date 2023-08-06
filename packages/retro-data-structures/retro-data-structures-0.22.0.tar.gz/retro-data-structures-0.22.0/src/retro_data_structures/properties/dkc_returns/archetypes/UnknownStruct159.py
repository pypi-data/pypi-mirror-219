# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct158 import UnknownStruct158
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct159(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_struct26_0xf0f0840b: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x3397f5e0: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x95833e87: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    strg_0x518dd3da: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0xd374144c: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x6a89715b: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct158: UnknownStruct158 = dataclasses.field(default_factory=UnknownStruct158)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xf0\xf0\x84\x0b')  # 0xf0f0840b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xf0f0840b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\x97\xf5\xe0')  # 0x3397f5e0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x3397f5e0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\x83>\x87')  # 0x95833e87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x95833e87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x8d\xd3\xda')  # 0x518dd3da
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x518dd3da))

        data.write(b'\xd3t\x14L')  # 0xd374144c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xd374144c))

        data.write(b'j\x89q[')  # 0x6a89715b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x6a89715b))

        data.write(b'R6?\xb6')  # 0x52363fb6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct158.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_frame=data['gui_frame'],
            unknown_struct26_0xf0f0840b=UnknownStruct26.from_json(data['unknown_struct26_0xf0f0840b']),
            unknown_struct26_0x3397f5e0=UnknownStruct26.from_json(data['unknown_struct26_0x3397f5e0']),
            unknown_struct26_0x95833e87=UnknownStruct26.from_json(data['unknown_struct26_0x95833e87']),
            strg_0x518dd3da=data['strg_0x518dd3da'],
            strg_0xd374144c=data['strg_0xd374144c'],
            strg_0x6a89715b=data['strg_0x6a89715b'],
            unknown_struct158=UnknownStruct158.from_json(data['unknown_struct158']),
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct26_0xf0f0840b': self.unknown_struct26_0xf0f0840b.to_json(),
            'unknown_struct26_0x3397f5e0': self.unknown_struct26_0x3397f5e0.to_json(),
            'unknown_struct26_0x95833e87': self.unknown_struct26_0x95833e87.to_json(),
            'strg_0x518dd3da': self.strg_0x518dd3da,
            'strg_0xd374144c': self.strg_0xd374144c,
            'strg_0x6a89715b': self.strg_0x6a89715b,
            'unknown_struct158': self.unknown_struct158.to_json(),
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct26_0xf0f0840b(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x3397f5e0(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x95833e87(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_strg_0x518dd3da(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xd374144c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x6a89715b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct158(data: typing.BinaryIO, property_size: int):
    return UnknownStruct158.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xf0f0840b: ('unknown_struct26_0xf0f0840b', _decode_unknown_struct26_0xf0f0840b),
    0x3397f5e0: ('unknown_struct26_0x3397f5e0', _decode_unknown_struct26_0x3397f5e0),
    0x95833e87: ('unknown_struct26_0x95833e87', _decode_unknown_struct26_0x95833e87),
    0x518dd3da: ('strg_0x518dd3da', _decode_strg_0x518dd3da),
    0xd374144c: ('strg_0xd374144c', _decode_strg_0xd374144c),
    0x6a89715b: ('strg_0x6a89715b', _decode_strg_0x6a89715b),
    0x52363fb6: ('unknown_struct158', _decode_unknown_struct158),
}
