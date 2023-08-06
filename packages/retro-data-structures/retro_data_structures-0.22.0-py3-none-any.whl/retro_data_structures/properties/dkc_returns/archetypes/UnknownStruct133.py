# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.AreaDamageData import AreaDamageData


@dataclasses.dataclass()
class UnknownStruct133(BaseProperty):
    number_of_area_damages: int = dataclasses.field(default=0)
    area_damage1: AreaDamageData = dataclasses.field(default_factory=AreaDamageData)
    area_damage2: AreaDamageData = dataclasses.field(default_factory=AreaDamageData)
    area_damage3: AreaDamageData = dataclasses.field(default_factory=AreaDamageData)
    area_damage4: AreaDamageData = dataclasses.field(default_factory=AreaDamageData)
    area_damage5: AreaDamageData = dataclasses.field(default_factory=AreaDamageData)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'M*\xf7\xb7')  # 0x4d2af7b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_area_damages))

        data.write(b'\xd768/')  # 0xd736382f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6KRV')  # 0xc64b5256
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xb0\x89\xbe')  # 0x7fb089be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4\xb1\x86\xa4')  # 0xe4b186a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']J]L')  # 0x5d4a5d4c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_area_damages=data['number_of_area_damages'],
            area_damage1=AreaDamageData.from_json(data['area_damage1']),
            area_damage2=AreaDamageData.from_json(data['area_damage2']),
            area_damage3=AreaDamageData.from_json(data['area_damage3']),
            area_damage4=AreaDamageData.from_json(data['area_damage4']),
            area_damage5=AreaDamageData.from_json(data['area_damage5']),
        )

    def to_json(self) -> dict:
        return {
            'number_of_area_damages': self.number_of_area_damages,
            'area_damage1': self.area_damage1.to_json(),
            'area_damage2': self.area_damage2.to_json(),
            'area_damage3': self.area_damage3.to_json(),
            'area_damage4': self.area_damage4.to_json(),
            'area_damage5': self.area_damage5.to_json(),
        }


def _decode_number_of_area_damages(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_area_damage1(data: typing.BinaryIO, property_size: int):
    return AreaDamageData.from_stream(data, property_size)


def _decode_area_damage2(data: typing.BinaryIO, property_size: int):
    return AreaDamageData.from_stream(data, property_size)


def _decode_area_damage3(data: typing.BinaryIO, property_size: int):
    return AreaDamageData.from_stream(data, property_size)


def _decode_area_damage4(data: typing.BinaryIO, property_size: int):
    return AreaDamageData.from_stream(data, property_size)


def _decode_area_damage5(data: typing.BinaryIO, property_size: int):
    return AreaDamageData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4d2af7b7: ('number_of_area_damages', _decode_number_of_area_damages),
    0xd736382f: ('area_damage1', _decode_area_damage1),
    0xc64b5256: ('area_damage2', _decode_area_damage2),
    0x7fb089be: ('area_damage3', _decode_area_damage3),
    0xe4b186a4: ('area_damage4', _decode_area_damage4),
    0x5d4a5d4c: ('area_damage5', _decode_area_damage5),
}
