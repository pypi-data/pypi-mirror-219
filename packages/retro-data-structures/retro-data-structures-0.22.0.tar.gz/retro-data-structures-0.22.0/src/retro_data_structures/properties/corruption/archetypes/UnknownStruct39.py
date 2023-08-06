# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.GhorStructC import GhorStructC
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct39(BaseProperty):
    ghor_struct_c: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    reset_time: float = dataclasses.field(default=10.0)
    reset_damage: float = dataclasses.field(default=50.0)
    activate_spline: Spline = dataclasses.field(default_factory=Spline)
    deactivate_spline: Spline = dataclasses.field(default_factory=Spline)
    active_effect: str = dataclasses.field(default='')
    hit_effect: str = dataclasses.field(default='')
    inactive_effect: str = dataclasses.field(default='')
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    shield_off_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xfd\xea]\x06')  # 0xfdea5d06
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+\xcd\x1dw')  # 0x2bcd1d77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reset_time))

        data.write(b'\x7f\xecab')  # 0x7fec6162
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reset_damage))

        data.write(b'9\xd6N@')  # 0x39d64e40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.activate_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc3k\xed')  # 0xfc336bed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.deactivate_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'`\xbd\xaa8')  # 0x60bdaa38
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.active_effect.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x0bA\xb4')  # 0xc60b41b4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.hit_effect.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\x80\x87\x80')  # 0x67808780
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.inactive_effect.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'bw\x1ff')  # 0x62771f66
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xb7[\x84B')  # 0xb75b8442
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shield_off_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ghor_struct_c=GhorStructC.from_json(data['ghor_struct_c']),
            reset_time=data['reset_time'],
            reset_damage=data['reset_damage'],
            activate_spline=Spline.from_json(data['activate_spline']),
            deactivate_spline=Spline.from_json(data['deactivate_spline']),
            active_effect=data['active_effect'],
            hit_effect=data['hit_effect'],
            inactive_effect=data['inactive_effect'],
            caud=data['caud'],
            shield_off_sound=data['shield_off_sound'],
        )

    def to_json(self) -> dict:
        return {
            'ghor_struct_c': self.ghor_struct_c.to_json(),
            'reset_time': self.reset_time,
            'reset_damage': self.reset_damage,
            'activate_spline': self.activate_spline.to_json(),
            'deactivate_spline': self.deactivate_spline.to_json(),
            'active_effect': self.active_effect,
            'hit_effect': self.hit_effect,
            'inactive_effect': self.inactive_effect,
            'caud': self.caud,
            'shield_off_sound': self.shield_off_sound,
        }


def _decode_ghor_struct_c(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_reset_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reset_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activate_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_deactivate_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_active_effect(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_hit_effect(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_inactive_effect(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shield_off_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfdea5d06: ('ghor_struct_c', _decode_ghor_struct_c),
    0x2bcd1d77: ('reset_time', _decode_reset_time),
    0x7fec6162: ('reset_damage', _decode_reset_damage),
    0x39d64e40: ('activate_spline', _decode_activate_spline),
    0xfc336bed: ('deactivate_spline', _decode_deactivate_spline),
    0x60bdaa38: ('active_effect', _decode_active_effect),
    0xc60b41b4: ('hit_effect', _decode_hit_effect),
    0x67808780: ('inactive_effect', _decode_inactive_effect),
    0x62771f66: ('caud', _decode_caud),
    0xb75b8442: ('shield_off_sound', _decode_shield_off_sound),
}
