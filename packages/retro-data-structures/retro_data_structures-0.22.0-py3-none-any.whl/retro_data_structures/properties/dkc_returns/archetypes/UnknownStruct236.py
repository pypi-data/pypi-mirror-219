# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct231 import UnknownStruct231
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct235 import UnknownStruct235


@dataclasses.dataclass()
class UnknownStruct236(BaseProperty):
    mole_type: enums.MoleType = dataclasses.field(default=enums.MoleType.Unknown1)
    damage_bounds_scale_z: float = dataclasses.field(default=0.5)
    unknown: str = dataclasses.field(default='')
    unknown_struct231: UnknownStruct231 = dataclasses.field(default_factory=UnknownStruct231)
    unknown_struct235: UnknownStruct235 = dataclasses.field(default_factory=UnknownStruct235)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xe9s!\x10')  # 0xe9732110
        data.write(b'\x00\x04')  # size
        self.mole_type.to_stream(data)

        data.write(b'\xc36\xa4\xef')  # 0xc336a4ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_bounds_scale_z))

        data.write(b'\x15\x87\x08E')  # 0x15870845
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Fs\xc9<')  # 0x4673c93c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct231.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6\x94\xe8\xca')  # 0xa694e8ca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct235.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mole_type=enums.MoleType.from_json(data['mole_type']),
            damage_bounds_scale_z=data['damage_bounds_scale_z'],
            unknown=data['unknown'],
            unknown_struct231=UnknownStruct231.from_json(data['unknown_struct231']),
            unknown_struct235=UnknownStruct235.from_json(data['unknown_struct235']),
        )

    def to_json(self) -> dict:
        return {
            'mole_type': self.mole_type.to_json(),
            'damage_bounds_scale_z': self.damage_bounds_scale_z,
            'unknown': self.unknown,
            'unknown_struct231': self.unknown_struct231.to_json(),
            'unknown_struct235': self.unknown_struct235.to_json(),
        }


def _decode_mole_type(data: typing.BinaryIO, property_size: int):
    return enums.MoleType.from_stream(data)


def _decode_damage_bounds_scale_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_struct231(data: typing.BinaryIO, property_size: int):
    return UnknownStruct231.from_stream(data, property_size)


def _decode_unknown_struct235(data: typing.BinaryIO, property_size: int):
    return UnknownStruct235.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe9732110: ('mole_type', _decode_mole_type),
    0xc336a4ef: ('damage_bounds_scale_z', _decode_damage_bounds_scale_z),
    0x15870845: ('unknown', _decode_unknown),
    0x4673c93c: ('unknown_struct231', _decode_unknown_struct231),
    0xa694e8ca: ('unknown_struct235', _decode_unknown_struct235),
}
