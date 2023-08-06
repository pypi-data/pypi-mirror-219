# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct35(BaseProperty):
    unknown_struct26_0xbdd1a035: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x8aa2bfe5: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0xca0d2611: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x731756f6: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x83fa2328: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x2f82f98c: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0xbcb5dac7: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x6126e3a3: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)

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

        data.write(b'\xbd\xd1\xa05')  # 0xbdd1a035
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xbdd1a035.to_stream(data, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=0.35686299204826355, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.7019609808921814, b=0.0, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8a\xa2\xbf\xe5')  # 0x8aa2bfe5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x8aa2bfe5.to_stream(data, default_override={'text_gradient_start_color': Color(r=1.0, g=0.9019610285758972, b=0.11764699965715408, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.5450980067253113, b=0.11764699965715408, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xca\r&\x11')  # 0xca0d2611
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xca0d2611.to_stream(data, default_override={'text_gradient_start_color': Color(r=0.6274510025978088, g=1.0, b=0.47843098640441895, a=0.0), 'text_gradient_end_color': Color(r=0.1294119954109192, g=0.549019992351532, b=0.5098040103912354, a=0.0), 'text_outline_color': Color(r=0.031373001635074615, g=0.17647099494934082, b=0.031373001635074615, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\x17V\xf6')  # 0x731756f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x731756f6.to_stream(data, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=1.0, a=0.0), 'text_gradient_end_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.0), 'text_outline_color': Color(r=0.0, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83\xfa#(')  # 0x83fa2328
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x83fa2328.to_stream(data, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=0.35686299204826355, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.7019609808921814, b=0.0, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/\x82\xf9\x8c')  # 0x2f82f98c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x2f82f98c.to_stream(data, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=0.35686299204826355, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.7019609808921814, b=0.0, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\xb5\xda\xc7')  # 0xbcb5dac7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xbcb5dac7.to_stream(data, default_override={'text_gradient_start_color': Color(r=1.0, g=0.9019610285758972, b=0.11764699965715408, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.5450980067253113, b=0.11764699965715408, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a&\xe3\xa3')  # 0x6126e3a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x6126e3a3.to_stream(data, default_override={'text_gradient_start_color': Color(r=0.0, g=0.0, b=0.0, a=0.0), 'text_gradient_end_color': Color(r=0.0, g=0.0, b=0.0, a=0.0), 'text_outline_color': Color(r=1.0, g=1.0, b=1.0, a=0.0)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct26_0xbdd1a035=UnknownStruct26.from_json(data['unknown_struct26_0xbdd1a035']),
            unknown_struct26_0x8aa2bfe5=UnknownStruct26.from_json(data['unknown_struct26_0x8aa2bfe5']),
            unknown_struct26_0xca0d2611=UnknownStruct26.from_json(data['unknown_struct26_0xca0d2611']),
            unknown_struct26_0x731756f6=UnknownStruct26.from_json(data['unknown_struct26_0x731756f6']),
            unknown_struct26_0x83fa2328=UnknownStruct26.from_json(data['unknown_struct26_0x83fa2328']),
            unknown_struct26_0x2f82f98c=UnknownStruct26.from_json(data['unknown_struct26_0x2f82f98c']),
            unknown_struct26_0xbcb5dac7=UnknownStruct26.from_json(data['unknown_struct26_0xbcb5dac7']),
            unknown_struct26_0x6126e3a3=UnknownStruct26.from_json(data['unknown_struct26_0x6126e3a3']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct26_0xbdd1a035': self.unknown_struct26_0xbdd1a035.to_json(),
            'unknown_struct26_0x8aa2bfe5': self.unknown_struct26_0x8aa2bfe5.to_json(),
            'unknown_struct26_0xca0d2611': self.unknown_struct26_0xca0d2611.to_json(),
            'unknown_struct26_0x731756f6': self.unknown_struct26_0x731756f6.to_json(),
            'unknown_struct26_0x83fa2328': self.unknown_struct26_0x83fa2328.to_json(),
            'unknown_struct26_0x2f82f98c': self.unknown_struct26_0x2f82f98c.to_json(),
            'unknown_struct26_0xbcb5dac7': self.unknown_struct26_0xbcb5dac7.to_json(),
            'unknown_struct26_0x6126e3a3': self.unknown_struct26_0x6126e3a3.to_json(),
        }


def _decode_unknown_struct26_0xbdd1a035(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=0.35686299204826355, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.7019609808921814, b=0.0, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})


def _decode_unknown_struct26_0x8aa2bfe5(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=1.0, g=0.9019610285758972, b=0.11764699965715408, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.5450980067253113, b=0.11764699965715408, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})


def _decode_unknown_struct26_0xca0d2611(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=0.6274510025978088, g=1.0, b=0.47843098640441895, a=0.0), 'text_gradient_end_color': Color(r=0.1294119954109192, g=0.549019992351532, b=0.5098040103912354, a=0.0), 'text_outline_color': Color(r=0.031373001635074615, g=0.17647099494934082, b=0.031373001635074615, a=0.0)})


def _decode_unknown_struct26_0x731756f6(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=1.0, a=0.0), 'text_gradient_end_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.0), 'text_outline_color': Color(r=0.0, g=0.0, b=0.0, a=0.0)})


def _decode_unknown_struct26_0x83fa2328(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=0.35686299204826355, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.7019609808921814, b=0.0, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})


def _decode_unknown_struct26_0x2f82f98c(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=1.0, g=1.0, b=0.35686299204826355, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.7019609808921814, b=0.0, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})


def _decode_unknown_struct26_0xbcb5dac7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=1.0, g=0.9019610285758972, b=0.11764699965715408, a=0.0), 'text_gradient_end_color': Color(r=1.0, g=0.5450980067253113, b=0.11764699965715408, a=0.0), 'text_outline_color': Color(r=0.7019609808921814, g=0.0, b=0.0, a=0.0)})


def _decode_unknown_struct26_0x6126e3a3(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size, default_override={'text_gradient_start_color': Color(r=0.0, g=0.0, b=0.0, a=0.0), 'text_gradient_end_color': Color(r=0.0, g=0.0, b=0.0, a=0.0), 'text_outline_color': Color(r=1.0, g=1.0, b=1.0, a=0.0)})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbdd1a035: ('unknown_struct26_0xbdd1a035', _decode_unknown_struct26_0xbdd1a035),
    0x8aa2bfe5: ('unknown_struct26_0x8aa2bfe5', _decode_unknown_struct26_0x8aa2bfe5),
    0xca0d2611: ('unknown_struct26_0xca0d2611', _decode_unknown_struct26_0xca0d2611),
    0x731756f6: ('unknown_struct26_0x731756f6', _decode_unknown_struct26_0x731756f6),
    0x83fa2328: ('unknown_struct26_0x83fa2328', _decode_unknown_struct26_0x83fa2328),
    0x2f82f98c: ('unknown_struct26_0x2f82f98c', _decode_unknown_struct26_0x2f82f98c),
    0xbcb5dac7: ('unknown_struct26_0xbcb5dac7', _decode_unknown_struct26_0xbcb5dac7),
    0x6126e3a3: ('unknown_struct26_0x6126e3a3', _decode_unknown_struct26_0x6126e3a3),
}
