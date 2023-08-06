# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.LayerToggle import LayerToggle


@dataclasses.dataclass()
class UnknownStruct24(BaseProperty):
    num_layers: int = dataclasses.field(default=0)
    layer_switch_0x5a8b108c: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0xc12e5ce3: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0xb6b08e13: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0x2d15c27c: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0x598d2bf3: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0xc228679c: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0xb5b6b56c: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0x2e13f903: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0x5c876672: LayerToggle = dataclasses.field(default_factory=LayerToggle)
    layer_switch_0xc7222a1d: LayerToggle = dataclasses.field(default_factory=LayerToggle)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xe2\xb2\xc8V')  # 0xe2b2c856
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_layers))

        data.write(b'Z\x8b\x10\x8c')  # 0x5a8b108c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x5a8b108c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1.\\\xe3')  # 0xc12e5ce3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xc12e5ce3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\xb0\x8e\x13')  # 0xb6b08e13
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xb6b08e13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\x15\xc2|')  # 0x2d15c27c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x2d15c27c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x8d+\xf3')  # 0x598d2bf3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x598d2bf3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2(g\x9c')  # 0xc228679c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xc228679c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb5\xb6\xb5l')  # 0xb5b6b56c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xb5b6b56c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.\x13\xf9\x03')  # 0x2e13f903
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x2e13f903.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\x87fr')  # 0x5c876672
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x5c876672.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7"*\x1d')  # 0xc7222a1d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xc7222a1d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            num_layers=data['num_layers'],
            layer_switch_0x5a8b108c=LayerToggle.from_json(data['layer_switch_0x5a8b108c']),
            layer_switch_0xc12e5ce3=LayerToggle.from_json(data['layer_switch_0xc12e5ce3']),
            layer_switch_0xb6b08e13=LayerToggle.from_json(data['layer_switch_0xb6b08e13']),
            layer_switch_0x2d15c27c=LayerToggle.from_json(data['layer_switch_0x2d15c27c']),
            layer_switch_0x598d2bf3=LayerToggle.from_json(data['layer_switch_0x598d2bf3']),
            layer_switch_0xc228679c=LayerToggle.from_json(data['layer_switch_0xc228679c']),
            layer_switch_0xb5b6b56c=LayerToggle.from_json(data['layer_switch_0xb5b6b56c']),
            layer_switch_0x2e13f903=LayerToggle.from_json(data['layer_switch_0x2e13f903']),
            layer_switch_0x5c876672=LayerToggle.from_json(data['layer_switch_0x5c876672']),
            layer_switch_0xc7222a1d=LayerToggle.from_json(data['layer_switch_0xc7222a1d']),
        )

    def to_json(self) -> dict:
        return {
            'num_layers': self.num_layers,
            'layer_switch_0x5a8b108c': self.layer_switch_0x5a8b108c.to_json(),
            'layer_switch_0xc12e5ce3': self.layer_switch_0xc12e5ce3.to_json(),
            'layer_switch_0xb6b08e13': self.layer_switch_0xb6b08e13.to_json(),
            'layer_switch_0x2d15c27c': self.layer_switch_0x2d15c27c.to_json(),
            'layer_switch_0x598d2bf3': self.layer_switch_0x598d2bf3.to_json(),
            'layer_switch_0xc228679c': self.layer_switch_0xc228679c.to_json(),
            'layer_switch_0xb5b6b56c': self.layer_switch_0xb5b6b56c.to_json(),
            'layer_switch_0x2e13f903': self.layer_switch_0x2e13f903.to_json(),
            'layer_switch_0x5c876672': self.layer_switch_0x5c876672.to_json(),
            'layer_switch_0xc7222a1d': self.layer_switch_0xc7222a1d.to_json(),
        }


def _decode_num_layers(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_layer_switch_0x5a8b108c(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0xc12e5ce3(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0xb6b08e13(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0x2d15c27c(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0x598d2bf3(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0xc228679c(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0xb5b6b56c(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0x2e13f903(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0x5c876672(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


def _decode_layer_switch_0xc7222a1d(data: typing.BinaryIO, property_size: int):
    return LayerToggle.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe2b2c856: ('num_layers', _decode_num_layers),
    0x5a8b108c: ('layer_switch_0x5a8b108c', _decode_layer_switch_0x5a8b108c),
    0xc12e5ce3: ('layer_switch_0xc12e5ce3', _decode_layer_switch_0xc12e5ce3),
    0xb6b08e13: ('layer_switch_0xb6b08e13', _decode_layer_switch_0xb6b08e13),
    0x2d15c27c: ('layer_switch_0x2d15c27c', _decode_layer_switch_0x2d15c27c),
    0x598d2bf3: ('layer_switch_0x598d2bf3', _decode_layer_switch_0x598d2bf3),
    0xc228679c: ('layer_switch_0xc228679c', _decode_layer_switch_0xc228679c),
    0xb5b6b56c: ('layer_switch_0xb5b6b56c', _decode_layer_switch_0xb5b6b56c),
    0x2e13f903: ('layer_switch_0x2e13f903', _decode_layer_switch_0x2e13f903),
    0x5c876672: ('layer_switch_0x5c876672', _decode_layer_switch_0x5c876672),
    0xc7222a1d: ('layer_switch_0xc7222a1d', _decode_layer_switch_0xc7222a1d),
}
