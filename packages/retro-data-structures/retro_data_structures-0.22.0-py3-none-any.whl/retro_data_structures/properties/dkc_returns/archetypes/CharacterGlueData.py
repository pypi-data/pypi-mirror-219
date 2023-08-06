# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.DKBarrelGlueData import DKBarrelGlueData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct138 import UnknownStruct138


@dataclasses.dataclass()
class CharacterGlueData(BaseProperty):
    glue_type: enums.GlueType = dataclasses.field(default=enums.GlueType.Unknown1)
    unknown_struct138: UnknownStruct138 = dataclasses.field(default_factory=UnknownStruct138)
    dk_barrel_glue_data: DKBarrelGlueData = dataclasses.field(default_factory=DKBarrelGlueData)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'A\x1d\x05R')  # 0x411d0552
        data.write(b'\x00\x04')  # size
        self.glue_type.to_stream(data)

        data.write(b'\xa4osA')  # 0xa46f7341
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct138.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6S\x80e')  # 0x36538065
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dk_barrel_glue_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            glue_type=enums.GlueType.from_json(data['glue_type']),
            unknown_struct138=UnknownStruct138.from_json(data['unknown_struct138']),
            dk_barrel_glue_data=DKBarrelGlueData.from_json(data['dk_barrel_glue_data']),
        )

    def to_json(self) -> dict:
        return {
            'glue_type': self.glue_type.to_json(),
            'unknown_struct138': self.unknown_struct138.to_json(),
            'dk_barrel_glue_data': self.dk_barrel_glue_data.to_json(),
        }


def _decode_glue_type(data: typing.BinaryIO, property_size: int):
    return enums.GlueType.from_stream(data)


def _decode_unknown_struct138(data: typing.BinaryIO, property_size: int):
    return UnknownStruct138.from_stream(data, property_size)


def _decode_dk_barrel_glue_data(data: typing.BinaryIO, property_size: int):
    return DKBarrelGlueData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x411d0552: ('glue_type', _decode_glue_type),
    0xa46f7341: ('unknown_struct138', _decode_unknown_struct138),
    0x36538065: ('dk_barrel_glue_data', _decode_dk_barrel_glue_data),
}
