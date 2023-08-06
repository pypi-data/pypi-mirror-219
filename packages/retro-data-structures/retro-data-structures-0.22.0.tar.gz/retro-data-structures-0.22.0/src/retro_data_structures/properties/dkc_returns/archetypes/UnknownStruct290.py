# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct289 import UnknownStruct289
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructB import VolcanoBossBodyPartStructB


@dataclasses.dataclass()
class UnknownStruct290(BaseProperty):
    unknown_struct289: UnknownStruct289 = dataclasses.field(default_factory=UnknownStruct289)
    volcano_boss_body_part_struct_b_0xc3e3ef00: VolcanoBossBodyPartStructB = dataclasses.field(default_factory=VolcanoBossBodyPartStructB)
    volcano_boss_body_part_struct_b_0xfa9b4240: VolcanoBossBodyPartStructB = dataclasses.field(default_factory=VolcanoBossBodyPartStructB)
    volcano_boss_body_part_struct_b_0xedb32680: VolcanoBossBodyPartStructB = dataclasses.field(default_factory=VolcanoBossBodyPartStructB)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b' \x8ci\xa5')  # 0x208c69a5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct289.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3\xe3\xef\x00')  # 0xc3e3ef00
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_b_0xc3e3ef00.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x9bB@')  # 0xfa9b4240
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_b_0xfa9b4240.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xb3&\x80')  # 0xedb32680
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_b_0xedb32680.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct289=UnknownStruct289.from_json(data['unknown_struct289']),
            volcano_boss_body_part_struct_b_0xc3e3ef00=VolcanoBossBodyPartStructB.from_json(data['volcano_boss_body_part_struct_b_0xc3e3ef00']),
            volcano_boss_body_part_struct_b_0xfa9b4240=VolcanoBossBodyPartStructB.from_json(data['volcano_boss_body_part_struct_b_0xfa9b4240']),
            volcano_boss_body_part_struct_b_0xedb32680=VolcanoBossBodyPartStructB.from_json(data['volcano_boss_body_part_struct_b_0xedb32680']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct289': self.unknown_struct289.to_json(),
            'volcano_boss_body_part_struct_b_0xc3e3ef00': self.volcano_boss_body_part_struct_b_0xc3e3ef00.to_json(),
            'volcano_boss_body_part_struct_b_0xfa9b4240': self.volcano_boss_body_part_struct_b_0xfa9b4240.to_json(),
            'volcano_boss_body_part_struct_b_0xedb32680': self.volcano_boss_body_part_struct_b_0xedb32680.to_json(),
        }


def _decode_unknown_struct289(data: typing.BinaryIO, property_size: int):
    return UnknownStruct289.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_b_0xc3e3ef00(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructB.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_b_0xfa9b4240(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructB.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_b_0xedb32680(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x208c69a5: ('unknown_struct289', _decode_unknown_struct289),
    0xc3e3ef00: ('volcano_boss_body_part_struct_b_0xc3e3ef00', _decode_volcano_boss_body_part_struct_b_0xc3e3ef00),
    0xfa9b4240: ('volcano_boss_body_part_struct_b_0xfa9b4240', _decode_volcano_boss_body_part_struct_b_0xfa9b4240),
    0xedb32680: ('volcano_boss_body_part_struct_b_0xedb32680', _decode_volcano_boss_body_part_struct_b_0xedb32680),
}
