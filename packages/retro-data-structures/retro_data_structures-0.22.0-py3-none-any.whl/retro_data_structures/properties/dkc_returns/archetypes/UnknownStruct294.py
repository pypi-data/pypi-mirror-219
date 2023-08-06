# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructC import VolcanoBossBodyPartStructC


@dataclasses.dataclass()
class UnknownStruct294(BaseProperty):
    volcano_boss_body_part_struct_c_0x92807f97: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC)
    volcano_boss_body_part_struct_c_0x7663abf3: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC)
    volcano_boss_body_part_struct_c_0x8a4c3f96: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC)
    volcano_boss_body_part_struct_c_0x70d8cac0: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC)

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

        data.write(b'\x92\x80\x7f\x97')  # 0x92807f97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x92807f97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'vc\xab\xf3')  # 0x7663abf3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x7663abf3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8aL?\x96')  # 0x8a4c3f96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x8a4c3f96.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'p\xd8\xca\xc0')  # 0x70d8cac0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x70d8cac0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            volcano_boss_body_part_struct_c_0x92807f97=VolcanoBossBodyPartStructC.from_json(data['volcano_boss_body_part_struct_c_0x92807f97']),
            volcano_boss_body_part_struct_c_0x7663abf3=VolcanoBossBodyPartStructC.from_json(data['volcano_boss_body_part_struct_c_0x7663abf3']),
            volcano_boss_body_part_struct_c_0x8a4c3f96=VolcanoBossBodyPartStructC.from_json(data['volcano_boss_body_part_struct_c_0x8a4c3f96']),
            volcano_boss_body_part_struct_c_0x70d8cac0=VolcanoBossBodyPartStructC.from_json(data['volcano_boss_body_part_struct_c_0x70d8cac0']),
        )

    def to_json(self) -> dict:
        return {
            'volcano_boss_body_part_struct_c_0x92807f97': self.volcano_boss_body_part_struct_c_0x92807f97.to_json(),
            'volcano_boss_body_part_struct_c_0x7663abf3': self.volcano_boss_body_part_struct_c_0x7663abf3.to_json(),
            'volcano_boss_body_part_struct_c_0x8a4c3f96': self.volcano_boss_body_part_struct_c_0x8a4c3f96.to_json(),
            'volcano_boss_body_part_struct_c_0x70d8cac0': self.volcano_boss_body_part_struct_c_0x70d8cac0.to_json(),
        }


def _decode_volcano_boss_body_part_struct_c_0x92807f97(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructC.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_c_0x7663abf3(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructC.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_c_0x8a4c3f96(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructC.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_c_0x70d8cac0(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructC.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x92807f97: ('volcano_boss_body_part_struct_c_0x92807f97', _decode_volcano_boss_body_part_struct_c_0x92807f97),
    0x7663abf3: ('volcano_boss_body_part_struct_c_0x7663abf3', _decode_volcano_boss_body_part_struct_c_0x7663abf3),
    0x8a4c3f96: ('volcano_boss_body_part_struct_c_0x8a4c3f96', _decode_volcano_boss_body_part_struct_c_0x8a4c3f96),
    0x70d8cac0: ('volcano_boss_body_part_struct_c_0x70d8cac0', _decode_volcano_boss_body_part_struct_c_0x70d8cac0),
}
