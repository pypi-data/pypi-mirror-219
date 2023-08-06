# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct65(BaseProperty):
    unknown: Spline = dataclasses.field(default_factory=Spline)
    effect_mode: enums.EffectMode = dataclasses.field(default=enums.EffectMode.Unknown1)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xdc\xbf\xa4\xe6')  # 0xdcbfa4e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\x10\xeb\x13')  # 0x1610eb13
        data.write(b'\x00\x04')  # size
        self.effect_mode.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=Spline.from_json(data['unknown']),
            effect_mode=enums.EffectMode.from_json(data['effect_mode']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown.to_json(),
            'effect_mode': self.effect_mode.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_effect_mode(data: typing.BinaryIO, property_size: int):
    return enums.EffectMode.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdcbfa4e6: ('unknown', _decode_unknown),
    0x1610eb13: ('effect_mode', _decode_effect_mode),
}
