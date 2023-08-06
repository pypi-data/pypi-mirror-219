# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ElectricBeamInfo(BaseProperty):
    beam_weapon: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    beam_projectile: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    beam_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    beam_visor_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    visor_effect_delay: float = dataclasses.field(default=1.0)
    beam_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    length: float = dataclasses.field(default=10.0)
    radius: float = dataclasses.field(default=0.10000000149011612)
    travel_speed: float = dataclasses.field(default=150.0)
    contact_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    fade_time: float = dataclasses.field(default=1.0)
    damage_delay: float = dataclasses.field(default=0.0)

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
        num_properties_offset = data.tell()
        data.write(b'\x00\x06')  # 6 properties
        num_properties_written = 6

        data.write(b'-9E\x0e')  # 0x2d39450e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_weapon))

        if self.beam_projectile != default_override.get('beam_projectile', default_asset_id):
            num_properties_written += 1
            data.write(b'\x1cV\x87\xcc')  # 0x1c5687cc
            data.write(b'\x00\x08')  # size
            data.write(struct.pack(">Q", self.beam_projectile))

        data.write(b'\xc9Ty\xd4')  # 0xc95479d4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_visor_effect))

        data.write(b'\x17DU\xba')  # 0x174455ba
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_visor_sound))

        data.write(b'\x10B\x84\xe6')  # 0x104284e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visor_effect_delay))

        data.write(b'\x98\x82\x19\x96')  # 0x98821996
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if self.length != default_override.get('length', 10.0):
            num_properties_written += 1
            data.write(b'\xc2l)\x1c')  # 0xc26c291c
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.length))

        if self.radius != default_override.get('radius', 0.10000000149011612):
            num_properties_written += 1
            data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.radius))

        if self.travel_speed != default_override.get('travel_speed', 150.0):
            num_properties_written += 1
            data.write(b'?\xed^R')  # 0x3fed5e52
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.travel_speed))

        if self.contact_effect != default_override.get('contact_effect', default_asset_id):
            num_properties_written += 1
            data.write(b'O8|I')  # 0x4f387c49
            data.write(b'\x00\x08')  # size
            data.write(struct.pack(">Q", self.contact_effect))

        if self.fade_time != default_override.get('fade_time', 1.0):
            num_properties_written += 1
            data.write(b'\xd4\x12LL')  # 0xd4124c4c
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>f', self.fade_time))

        data.write(b'\x8fO\xb7\x9d')  # 0x8f4fb79d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_delay))

        if num_properties_written != 6:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack(">H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            beam_weapon=data['beam_weapon'],
            beam_projectile=data['beam_projectile'],
            beam_visor_effect=data['beam_visor_effect'],
            beam_visor_sound=data['beam_visor_sound'],
            visor_effect_delay=data['visor_effect_delay'],
            beam_damage_info=DamageInfo.from_json(data['beam_damage_info']),
            length=data['length'],
            radius=data['radius'],
            travel_speed=data['travel_speed'],
            contact_effect=data['contact_effect'],
            fade_time=data['fade_time'],
            damage_delay=data['damage_delay'],
        )

    def to_json(self) -> dict:
        return {
            'beam_weapon': self.beam_weapon,
            'beam_projectile': self.beam_projectile,
            'beam_visor_effect': self.beam_visor_effect,
            'beam_visor_sound': self.beam_visor_sound,
            'visor_effect_delay': self.visor_effect_delay,
            'beam_damage_info': self.beam_damage_info.to_json(),
            'length': self.length,
            'radius': self.radius,
            'travel_speed': self.travel_speed,
            'contact_effect': self.contact_effect,
            'fade_time': self.fade_time,
            'damage_delay': self.damage_delay,
        }


def _decode_beam_weapon(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_visor_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_visor_effect_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_travel_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2d39450e: ('beam_weapon', _decode_beam_weapon),
    0x1c5687cc: ('beam_projectile', _decode_beam_projectile),
    0xc95479d4: ('beam_visor_effect', _decode_beam_visor_effect),
    0x174455ba: ('beam_visor_sound', _decode_beam_visor_sound),
    0x104284e6: ('visor_effect_delay', _decode_visor_effect_delay),
    0x98821996: ('beam_damage_info', _decode_beam_damage_info),
    0xc26c291c: ('length', _decode_length),
    0x78c507eb: ('radius', _decode_radius),
    0x3fed5e52: ('travel_speed', _decode_travel_speed),
    0x4f387c49: ('contact_effect', _decode_contact_effect),
    0xd4124c4c: ('fade_time', _decode_fade_time),
    0x8f4fb79d: ('damage_delay', _decode_damage_delay),
}
