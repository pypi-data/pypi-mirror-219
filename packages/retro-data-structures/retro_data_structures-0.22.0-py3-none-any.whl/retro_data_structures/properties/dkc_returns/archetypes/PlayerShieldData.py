# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerShieldSplineData import PlayerShieldSplineData


@dataclasses.dataclass()
class PlayerShieldData(BaseProperty):
    num_splines: int = dataclasses.field(default=1)
    spline1: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline2: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline3: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline4: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline5: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline6: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline7: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline8: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline9: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)
    spline10: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData)

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

        data.write(b"Z\x15\xd1'")  # 0x5a15d127
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_splines))

        data.write(b'\xcdB\r#')  # 0xcd420d23
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xa74\x1e')  # 0xbba7341e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \xd4\xde\xca')  # 0x20d4deca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'VmFd')  # 0x566d4664
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\x1e\xac\xb0')  # 0xcd1eacb0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xfb\x95\x8d')  # 0xbbfb958d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \x88\x7fY')  # 0x20887f59
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x88\xa4\xd1')  # 0x5688a4d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\xfbN\x05')  # 0xcdfb4e05
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec{|M')  # 0xec7b7c4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline10.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            num_splines=data['num_splines'],
            spline1=PlayerShieldSplineData.from_json(data['spline1']),
            spline2=PlayerShieldSplineData.from_json(data['spline2']),
            spline3=PlayerShieldSplineData.from_json(data['spline3']),
            spline4=PlayerShieldSplineData.from_json(data['spline4']),
            spline5=PlayerShieldSplineData.from_json(data['spline5']),
            spline6=PlayerShieldSplineData.from_json(data['spline6']),
            spline7=PlayerShieldSplineData.from_json(data['spline7']),
            spline8=PlayerShieldSplineData.from_json(data['spline8']),
            spline9=PlayerShieldSplineData.from_json(data['spline9']),
            spline10=PlayerShieldSplineData.from_json(data['spline10']),
        )

    def to_json(self) -> dict:
        return {
            'num_splines': self.num_splines,
            'spline1': self.spline1.to_json(),
            'spline2': self.spline2.to_json(),
            'spline3': self.spline3.to_json(),
            'spline4': self.spline4.to_json(),
            'spline5': self.spline5.to_json(),
            'spline6': self.spline6.to_json(),
            'spline7': self.spline7.to_json(),
            'spline8': self.spline8.to_json(),
            'spline9': self.spline9.to_json(),
            'spline10': self.spline10.to_json(),
        }


def _decode_num_splines(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spline1(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline2(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline3(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline4(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline5(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline6(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline7(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline8(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline9(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


def _decode_spline10(data: typing.BinaryIO, property_size: int):
    return PlayerShieldSplineData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5a15d127: ('num_splines', _decode_num_splines),
    0xcd420d23: ('spline1', _decode_spline1),
    0xbba7341e: ('spline2', _decode_spline2),
    0x20d4deca: ('spline3', _decode_spline3),
    0x566d4664: ('spline4', _decode_spline4),
    0xcd1eacb0: ('spline5', _decode_spline5),
    0xbbfb958d: ('spline6', _decode_spline6),
    0x20887f59: ('spline7', _decode_spline7),
    0x5688a4d1: ('spline8', _decode_spline8),
    0xcdfb4e05: ('spline9', _decode_spline9),
    0xec7b7c4d: ('spline10', _decode_spline10),
}
