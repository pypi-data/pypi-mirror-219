# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime_remastered as enums
from retro_data_structures.properties.prime_remastered.archetypes.ActorInformationMP1 import ActorInformationMP1
from retro_data_structures.properties.prime_remastered.archetypes.AnimSetMP1 import AnimSetMP1
from retro_data_structures.properties.prime_remastered.archetypes.MapInfoMP1 import MapInfoMP1
from retro_data_structures.properties.prime_remastered.archetypes.VectorMP1 import VectorMP1
from retro_data_structures.properties.prime_remastered.core.AssetId import AssetId, default_asset_id
import uuid


@dataclasses.dataclass()
class PickupMP1(BaseProperty):
    collision_scale: VectorMP1 = dataclasses.field(default_factory=VectorMP1)
    scan_collision_offset: VectorMP1 = dataclasses.field(default_factory=VectorMP1)
    item: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    capacity: int = dataclasses.field(default=1)
    amount: int = dataclasses.field(default=1)
    drop_rate: float = dataclasses.field(default=100.0)
    life_time: float = dataclasses.field(default=0.0)
    fade_length: float = dataclasses.field(default=0.0)
    guid_1: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    animation_parameters: AnimSetMP1 = dataclasses.field(default_factory=AnimSetMP1)
    spawn_delay: float = dataclasses.field(default=0.0)
    guid_2: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unk_vec_3: VectorMP1 = dataclasses.field(default_factory=VectorMP1)
    map_info: MapInfoMP1 = dataclasses.field(default_factory=MapInfoMP1)
    actor_info: ActorInformationMP1 = dataclasses.field(default_factory=ActorInformationMP1)
    unk_bool_1: bool = dataclasses.field(default=False)
    unk_bool_2: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack("<LH", data.read(6))
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
        data.write(b'\x08\x00')  # 8 properties
        num_properties_written = 8

        data.write(b'\xc6\x9e\xe3p')  # 0x70e39ec6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.collision_scale.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        data.write(b'DHd-')  # 0x2d644844
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_collision_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\x94\x97\xc7')  # 0xc79794ee
        data.write(b'\x04\x00')  # size
        self.item.to_stream(data)

        if self.capacity != default_override.get('capacity', 1):
            num_properties_written += 1
            data.write(b'\xd5\x91\xbev')  # 0x76be91d5
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<l', self.capacity))

        if self.amount != default_override.get('amount', 1):
            num_properties_written += 1
            data.write(b'\xf6\xd2\xdb\x9f')  # 0x9fdbd2f6
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<l', self.amount))

        if self.drop_rate != default_override.get('drop_rate', 100.0):
            num_properties_written += 1
            data.write(b'\xd2I\xf3\xfc')  # 0xfcf349d2
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.drop_rate))

        if self.life_time != default_override.get('life_time', 0.0):
            num_properties_written += 1
            data.write(b'}\xaf*\x7f')  # 0x7f2aaf7d
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.life_time))

        if self.fade_length != default_override.get('fade_length', 0.0):
            num_properties_written += 1
            data.write(b'+\x0f\x93\xef')  # 0xef930f2b
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.fade_length))

        if self.guid_1 != default_override.get('guid_1', default_asset_id):
            num_properties_written += 1
            data.write(b'\xb3\x9c\xe2\xbc')  # 0xbce29cb3
            data.write(b'\x10\x00')  # size
            data.write(self.guid_1.bytes_le)

        data.write(b'\xb1\x11\xd9\x19')  # 0x19d911b1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        if self.spawn_delay != default_override.get('spawn_delay', 0.0):
            num_properties_written += 1
            data.write(b'\xff^\x9f>')  # 0x3e9f5eff
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<f', self.spawn_delay))

        data.write(b'\x8e}\xa0\xe2')  # 0xe2a07d8e
        data.write(b'\x10\x00')  # size
        data.write(self.guid_2.bytes_le)

        data.write(b'\x8aC?\x85')  # 0x853f438a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unk_vec_3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b\xa88\xba')  # 0xba38a80b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.map_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\xd4\xf9h')  # 0x68f9d4b6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack("<H", after - before - 2))
        data.seek(after)

        if self.unk_bool_1 != default_override.get('unk_bool_1', False):
            num_properties_written += 1
            data.write(b'\xf2\xe2q\xbd')  # 0xbd71e2f2
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unk_bool_1))

        if self.unk_bool_2 != default_override.get('unk_bool_2', False):
            num_properties_written += 1
            data.write(b'n\\\x16\xf2')  # 0xf2165c6e
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unk_bool_2))

        if num_properties_written != 8:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            collision_scale=VectorMP1.from_json(data['collision_scale']),
            scan_collision_offset=VectorMP1.from_json(data['scan_collision_offset']),
            item=enums.PlayerItem.from_json(data['item']),
            capacity=data['capacity'],
            amount=data['amount'],
            drop_rate=data['drop_rate'],
            life_time=data['life_time'],
            fade_length=data['fade_length'],
            guid_1=uuid.UUID(data['guid_1']),
            animation_parameters=AnimSetMP1.from_json(data['animation_parameters']),
            spawn_delay=data['spawn_delay'],
            guid_2=uuid.UUID(data['guid_2']),
            unk_vec_3=VectorMP1.from_json(data['unk_vec_3']),
            map_info=MapInfoMP1.from_json(data['map_info']),
            actor_info=ActorInformationMP1.from_json(data['actor_info']),
            unk_bool_1=data['unk_bool_1'],
            unk_bool_2=data['unk_bool_2'],
        )

    def to_json(self) -> dict:
        return {
            'collision_scale': self.collision_scale.to_json(),
            'scan_collision_offset': self.scan_collision_offset.to_json(),
            'item': self.item.to_json(),
            'capacity': self.capacity,
            'amount': self.amount,
            'drop_rate': self.drop_rate,
            'life_time': self.life_time,
            'fade_length': self.fade_length,
            'guid_1': str(self.guid_1),
            'animation_parameters': self.animation_parameters.to_json(),
            'spawn_delay': self.spawn_delay,
            'guid_2': str(self.guid_2),
            'unk_vec_3': self.unk_vec_3.to_json(),
            'map_info': self.map_info.to_json(),
            'actor_info': self.actor_info.to_json(),
            'unk_bool_1': self.unk_bool_1,
            'unk_bool_2': self.unk_bool_2,
        }


def _decode_collision_scale(data: typing.BinaryIO, property_size: int):
    return VectorMP1.from_stream(data, property_size)


def _decode_scan_collision_offset(data: typing.BinaryIO, property_size: int):
    return VectorMP1.from_stream(data, property_size)


def _decode_item(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_capacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<l', data.read(4))[0]


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<l', data.read(4))[0]


def _decode_drop_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_fade_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_guid_1(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_animation_parameters(data: typing.BinaryIO, property_size: int):
    return AnimSetMP1.from_stream(data, property_size)


def _decode_spawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<f', data.read(4))[0]


def _decode_guid_2(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_unk_vec_3(data: typing.BinaryIO, property_size: int):
    return VectorMP1.from_stream(data, property_size)


def _decode_map_info(data: typing.BinaryIO, property_size: int):
    return MapInfoMP1.from_stream(data, property_size)


def _decode_actor_info(data: typing.BinaryIO, property_size: int):
    return ActorInformationMP1.from_stream(data, property_size)


def _decode_unk_bool_1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_unk_bool_2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x70e39ec6: ('collision_scale', _decode_collision_scale),
    0x2d644844: ('scan_collision_offset', _decode_scan_collision_offset),
    0xc79794ee: ('item', _decode_item),
    0x76be91d5: ('capacity', _decode_capacity),
    0x9fdbd2f6: ('amount', _decode_amount),
    0xfcf349d2: ('drop_rate', _decode_drop_rate),
    0x7f2aaf7d: ('life_time', _decode_life_time),
    0xef930f2b: ('fade_length', _decode_fade_length),
    0xbce29cb3: ('guid_1', _decode_guid_1),
    0x19d911b1: ('animation_parameters', _decode_animation_parameters),
    0x3e9f5eff: ('spawn_delay', _decode_spawn_delay),
    0xe2a07d8e: ('guid_2', _decode_guid_2),
    0x853f438a: ('unk_vec_3', _decode_unk_vec_3),
    0xba38a80b: ('map_info', _decode_map_info),
    0x68f9d4b6: ('actor_info', _decode_actor_info),
    0xbd71e2f2: ('unk_bool_1', _decode_unk_bool_1),
    0xf2165c6e: ('unk_bool_2', _decode_unk_bool_2),
}
