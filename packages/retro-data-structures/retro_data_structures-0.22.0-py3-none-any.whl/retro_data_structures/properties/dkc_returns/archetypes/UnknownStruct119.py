# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct119(BaseProperty):
    unknown_0x835677a5: float = dataclasses.field(default=0.0)
    return_speed: float = dataclasses.field(default=5.0)
    unknown_0x9b6c3ae4: float = dataclasses.field(default=4.0)
    unknown_0x6893e2ce: float = dataclasses.field(default=4.0)
    max_layer_activation: float = dataclasses.field(default=4.0)
    stun_time: float = dataclasses.field(default=4.0)
    unknown_0x34d15039: float = dataclasses.field(default=1.0)
    unknown_0xa407c02a: float = dataclasses.field(default=2.0)
    unknown_0x60e63efc: float = dataclasses.field(default=4.0)
    unknown_0x9963bf82: float = dataclasses.field(default=2.0)
    hold_locator: str = dataclasses.field(default='')
    unknown_0x3311ba2b: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x83Vw\xa5')  # 0x835677a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x835677a5))

        data.write(b'\xcc($\x9e')  # 0xcc28249e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.return_speed))

        data.write(b'\x9bl:\xe4')  # 0x9b6c3ae4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9b6c3ae4))

        data.write(b'h\x93\xe2\xce')  # 0x6893e2ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6893e2ce))

        data.write(b'\xb9W%\xac')  # 0xb95725ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_layer_activation))

        data.write(b'~\x19#\x95')  # 0x7e192395
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_time))

        data.write(b'4\xd1P9')  # 0x34d15039
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x34d15039))

        data.write(b'\xa4\x07\xc0*')  # 0xa407c02a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa407c02a))

        data.write(b'`\xe6>\xfc')  # 0x60e63efc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x60e63efc))

        data.write(b'\x99c\xbf\x82')  # 0x9963bf82
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9963bf82))

        data.write(b'\xd2\xba\x948')  # 0xd2ba9438
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.hold_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\x11\xba+')  # 0x3311ba2b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x3311ba2b))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x835677a5=data['unknown_0x835677a5'],
            return_speed=data['return_speed'],
            unknown_0x9b6c3ae4=data['unknown_0x9b6c3ae4'],
            unknown_0x6893e2ce=data['unknown_0x6893e2ce'],
            max_layer_activation=data['max_layer_activation'],
            stun_time=data['stun_time'],
            unknown_0x34d15039=data['unknown_0x34d15039'],
            unknown_0xa407c02a=data['unknown_0xa407c02a'],
            unknown_0x60e63efc=data['unknown_0x60e63efc'],
            unknown_0x9963bf82=data['unknown_0x9963bf82'],
            hold_locator=data['hold_locator'],
            unknown_0x3311ba2b=data['unknown_0x3311ba2b'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x835677a5': self.unknown_0x835677a5,
            'return_speed': self.return_speed,
            'unknown_0x9b6c3ae4': self.unknown_0x9b6c3ae4,
            'unknown_0x6893e2ce': self.unknown_0x6893e2ce,
            'max_layer_activation': self.max_layer_activation,
            'stun_time': self.stun_time,
            'unknown_0x34d15039': self.unknown_0x34d15039,
            'unknown_0xa407c02a': self.unknown_0xa407c02a,
            'unknown_0x60e63efc': self.unknown_0x60e63efc,
            'unknown_0x9963bf82': self.unknown_0x9963bf82,
            'hold_locator': self.hold_locator,
            'unknown_0x3311ba2b': self.unknown_0x3311ba2b,
        }


def _decode_unknown_0x835677a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_return_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9b6c3ae4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6893e2ce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_layer_activation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x34d15039(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa407c02a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x60e63efc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9963bf82(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hold_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x3311ba2b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x835677a5: ('unknown_0x835677a5', _decode_unknown_0x835677a5),
    0xcc28249e: ('return_speed', _decode_return_speed),
    0x9b6c3ae4: ('unknown_0x9b6c3ae4', _decode_unknown_0x9b6c3ae4),
    0x6893e2ce: ('unknown_0x6893e2ce', _decode_unknown_0x6893e2ce),
    0xb95725ac: ('max_layer_activation', _decode_max_layer_activation),
    0x7e192395: ('stun_time', _decode_stun_time),
    0x34d15039: ('unknown_0x34d15039', _decode_unknown_0x34d15039),
    0xa407c02a: ('unknown_0xa407c02a', _decode_unknown_0xa407c02a),
    0x60e63efc: ('unknown_0x60e63efc', _decode_unknown_0x60e63efc),
    0x9963bf82: ('unknown_0x9963bf82', _decode_unknown_0x9963bf82),
    0xd2ba9438: ('hold_locator', _decode_hold_locator),
    0x3311ba2b: ('unknown_0x3311ba2b', _decode_unknown_0x3311ba2b),
}
