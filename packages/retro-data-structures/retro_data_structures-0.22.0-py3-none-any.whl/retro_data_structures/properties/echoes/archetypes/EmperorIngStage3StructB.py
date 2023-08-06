# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.UnknownStruct2 import UnknownStruct2


@dataclasses.dataclass()
class EmperorIngStage3StructB(BaseProperty):
    min_health_percentage: float = dataclasses.field(default=0.0)
    unknown_0x95e7a2c2: float = dataclasses.field(default=0.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=0.0)
    unknown_struct2_0x3826ec75: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0x93bf1106: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0xc4b88b80: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0x32c6dc77: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0xc6e7b293: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0x20746b56: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0x2ab44adb: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_struct2_0xe2e78a78: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\xdf\xeaF\xb3')  # 0xdfea46b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_health_percentage))

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'8&\xecu')  # 0x3826ec75
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0x3826ec75.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\xbf\x11\x06')  # 0x93bf1106
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0x93bf1106.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\xb8\x8b\x80')  # 0xc4b88b80
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0xc4b88b80.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\xc6\xdcw')  # 0x32c6dc77
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0x32c6dc77.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xe7\xb2\x93')  # 0xc6e7b293
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0xc6e7b293.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' tkV')  # 0x20746b56
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0x20746b56.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*\xb4J\xdb')  # 0x2ab44adb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0x2ab44adb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\xe7\x8ax')  # 0xe2e78a78
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct2_0xe2e78a78.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            min_health_percentage=data['min_health_percentage'],
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_struct2_0x3826ec75=UnknownStruct2.from_json(data['unknown_struct2_0x3826ec75']),
            unknown_struct2_0x93bf1106=UnknownStruct2.from_json(data['unknown_struct2_0x93bf1106']),
            unknown_struct2_0xc4b88b80=UnknownStruct2.from_json(data['unknown_struct2_0xc4b88b80']),
            unknown_struct2_0x32c6dc77=UnknownStruct2.from_json(data['unknown_struct2_0x32c6dc77']),
            unknown_struct2_0xc6e7b293=UnknownStruct2.from_json(data['unknown_struct2_0xc6e7b293']),
            unknown_struct2_0x20746b56=UnknownStruct2.from_json(data['unknown_struct2_0x20746b56']),
            unknown_struct2_0x2ab44adb=UnknownStruct2.from_json(data['unknown_struct2_0x2ab44adb']),
            unknown_struct2_0xe2e78a78=UnknownStruct2.from_json(data['unknown_struct2_0xe2e78a78']),
        )

    def to_json(self) -> dict:
        return {
            'min_health_percentage': self.min_health_percentage,
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_struct2_0x3826ec75': self.unknown_struct2_0x3826ec75.to_json(),
            'unknown_struct2_0x93bf1106': self.unknown_struct2_0x93bf1106.to_json(),
            'unknown_struct2_0xc4b88b80': self.unknown_struct2_0xc4b88b80.to_json(),
            'unknown_struct2_0x32c6dc77': self.unknown_struct2_0x32c6dc77.to_json(),
            'unknown_struct2_0xc6e7b293': self.unknown_struct2_0xc6e7b293.to_json(),
            'unknown_struct2_0x20746b56': self.unknown_struct2_0x20746b56.to_json(),
            'unknown_struct2_0x2ab44adb': self.unknown_struct2_0x2ab44adb.to_json(),
            'unknown_struct2_0xe2e78a78': self.unknown_struct2_0xe2e78a78.to_json(),
        }

    def _dependencies_for_unknown_struct2_0x3826ec75(self, asset_manager):
        yield from self.unknown_struct2_0x3826ec75.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0x93bf1106(self, asset_manager):
        yield from self.unknown_struct2_0x93bf1106.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0xc4b88b80(self, asset_manager):
        yield from self.unknown_struct2_0xc4b88b80.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0x32c6dc77(self, asset_manager):
        yield from self.unknown_struct2_0x32c6dc77.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0xc6e7b293(self, asset_manager):
        yield from self.unknown_struct2_0xc6e7b293.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0x20746b56(self, asset_manager):
        yield from self.unknown_struct2_0x20746b56.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0x2ab44adb(self, asset_manager):
        yield from self.unknown_struct2_0x2ab44adb.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct2_0xe2e78a78(self, asset_manager):
        yield from self.unknown_struct2_0xe2e78a78.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unknown_struct2_0x3826ec75, "unknown_struct2_0x3826ec75", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0x93bf1106, "unknown_struct2_0x93bf1106", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0xc4b88b80, "unknown_struct2_0xc4b88b80", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0x32c6dc77, "unknown_struct2_0x32c6dc77", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0xc6e7b293, "unknown_struct2_0xc6e7b293", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0x20746b56, "unknown_struct2_0x20746b56", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0x2ab44adb, "unknown_struct2_0x2ab44adb", "UnknownStruct2"),
            (self._dependencies_for_unknown_struct2_0xe2e78a78, "unknown_struct2_0xe2e78a78", "UnknownStruct2"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for EmperorIngStage3StructB.{field_name} ({field_type}): {e}"
                )


def _decode_min_health_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct2_0x3826ec75(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0x93bf1106(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0xc4b88b80(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0x32c6dc77(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0xc6e7b293(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0x20746b56(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0x2ab44adb(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_struct2_0xe2e78a78(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdfea46b3: ('min_health_percentage', _decode_min_health_percentage),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0x3826ec75: ('unknown_struct2_0x3826ec75', _decode_unknown_struct2_0x3826ec75),
    0x93bf1106: ('unknown_struct2_0x93bf1106', _decode_unknown_struct2_0x93bf1106),
    0xc4b88b80: ('unknown_struct2_0xc4b88b80', _decode_unknown_struct2_0xc4b88b80),
    0x32c6dc77: ('unknown_struct2_0x32c6dc77', _decode_unknown_struct2_0x32c6dc77),
    0xc6e7b293: ('unknown_struct2_0xc6e7b293', _decode_unknown_struct2_0xc6e7b293),
    0x20746b56: ('unknown_struct2_0x20746b56', _decode_unknown_struct2_0x20746b56),
    0x2ab44adb: ('unknown_struct2_0x2ab44adb', _decode_unknown_struct2_0x2ab44adb),
    0xe2e78a78: ('unknown_struct2_0xe2e78a78', _decode_unknown_struct2_0xe2e78a78),
}
