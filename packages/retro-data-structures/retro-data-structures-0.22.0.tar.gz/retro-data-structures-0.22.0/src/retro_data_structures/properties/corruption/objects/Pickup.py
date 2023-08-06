# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.SavedStateID import SavedStateID
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class Pickup(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    object_id: SavedStateID = dataclasses.field(default_factory=SavedStateID)
    collision_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    item_to_give: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    capacity_increase: int = dataclasses.field(default=1)
    item_percentage_increase: int = dataclasses.field(default=0)
    amount: int = dataclasses.field(default=1)
    respawn_time: float = dataclasses.field(default=0.0)
    pickup_effect_lifetime: float = dataclasses.field(default=0.0)
    lifetime: float = dataclasses.field(default=0.0)
    fadetime: float = dataclasses.field(default=0.0)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    activation_delay: float = dataclasses.field(default=0.0)
    pickup_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    absolute_value: bool = dataclasses.field(default=False)
    calculate_visibility: bool = dataclasses.field(default=True)
    unknown_0x2de4a294: bool = dataclasses.field(default=False)
    auto_home_range: float = dataclasses.field(default=0.0)
    delay_until_home: float = dataclasses.field(default=0.0)
    homing_speed: float = dataclasses.field(default=20.0)
    auto_spin: bool = dataclasses.field(default=False)
    blink_out: bool = dataclasses.field(default=False)
    orbit_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0xa09d4a1f: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PCKP'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\xd9\xa7]')  # 0x16d9a75d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.object_id.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':>\x03\xba')  # 0x3a3e03ba
        data.write(b'\x00\x0c')  # size
        self.collision_size.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xa0.\xf0\xc4')  # 0xa02ef0c4
        data.write(b'\x00\x04')  # size
        self.item_to_give.to_stream(data)

        data.write(b'(\xc7\x1bT')  # 0x28c71b54
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.capacity_increase))

        data.write(b'\x16Z\xb0i')  # 0x165ab069
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.item_percentage_increase))

        data.write(b'\x94\xaf\x14E')  # 0x94af1445
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.amount))

        data.write(b'\xf7\xfb\xaa\xa5')  # 0xf7fbaaa5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_time))

        data.write(b"\xc8\x0f\xc8'")  # 0xc80fc827
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pickup_effect_lifetime))

        data.write(b'2\xdcg\xf6')  # 0x32dc67f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lifetime))

        data.write(b'V\xe3\xce\xef')  # 0x56e3ceef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fadetime))

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x85\xf1f')  # 0xe585f166
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_delay))

        data.write(b'\xa9\xfe\x87*')  # 0xa9fe872a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pickup_effect))

        data.write(b'\xe1\x0b\xcb\x96')  # 0xe10bcb96
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.absolute_value))

        data.write(b'\xce3#\x9f')  # 0xce33239f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.calculate_visibility))

        data.write(b'-\xe4\xa2\x94')  # 0x2de4a294
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2de4a294))

        data.write(b'\xa6\xea(\r')  # 0xa6ea280d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_home_range))

        data.write(b'\xc2\xb1\x1c\xfd')  # 0xc2b11cfd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_until_home))

        data.write(b'-\xb5\x9f\xcf')  # 0x2db59fcf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.homing_speed))

        data.write(b'\x96\x1c\r\x17')  # 0x961c0d17
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_spin))

        data.write(b'\xa7U\xeb\x02')  # 0xa755eb02
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.blink_out))

        data.write(b'\x85\x01\x15\xe4')  # 0x850115e4
        data.write(b'\x00\x0c')  # size
        self.orbit_offset.to_stream(data)

        data.write(b'\xa0\x9dJ\x1f')  # 0xa09d4a1f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa09d4a1f))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            object_id=SavedStateID.from_json(data['object_id']),
            collision_size=Vector.from_json(data['collision_size']),
            collision_offset=Vector.from_json(data['collision_offset']),
            item_to_give=enums.PlayerItem.from_json(data['item_to_give']),
            capacity_increase=data['capacity_increase'],
            item_percentage_increase=data['item_percentage_increase'],
            amount=data['amount'],
            respawn_time=data['respawn_time'],
            pickup_effect_lifetime=data['pickup_effect_lifetime'],
            lifetime=data['lifetime'],
            fadetime=data['fadetime'],
            model=data['model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            activation_delay=data['activation_delay'],
            pickup_effect=data['pickup_effect'],
            absolute_value=data['absolute_value'],
            calculate_visibility=data['calculate_visibility'],
            unknown_0x2de4a294=data['unknown_0x2de4a294'],
            auto_home_range=data['auto_home_range'],
            delay_until_home=data['delay_until_home'],
            homing_speed=data['homing_speed'],
            auto_spin=data['auto_spin'],
            blink_out=data['blink_out'],
            orbit_offset=Vector.from_json(data['orbit_offset']),
            unknown_0xa09d4a1f=data['unknown_0xa09d4a1f'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'object_id': self.object_id.to_json(),
            'collision_size': self.collision_size.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'item_to_give': self.item_to_give.to_json(),
            'capacity_increase': self.capacity_increase,
            'item_percentage_increase': self.item_percentage_increase,
            'amount': self.amount,
            'respawn_time': self.respawn_time,
            'pickup_effect_lifetime': self.pickup_effect_lifetime,
            'lifetime': self.lifetime,
            'fadetime': self.fadetime,
            'model': self.model,
            'character_animation_information': self.character_animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'activation_delay': self.activation_delay,
            'pickup_effect': self.pickup_effect,
            'absolute_value': self.absolute_value,
            'calculate_visibility': self.calculate_visibility,
            'unknown_0x2de4a294': self.unknown_0x2de4a294,
            'auto_home_range': self.auto_home_range,
            'delay_until_home': self.delay_until_home,
            'homing_speed': self.homing_speed,
            'auto_spin': self.auto_spin,
            'blink_out': self.blink_out,
            'orbit_offset': self.orbit_offset.to_json(),
            'unknown_0xa09d4a1f': self.unknown_0xa09d4a1f,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_object_id(data: typing.BinaryIO, property_size: int):
    return SavedStateID.from_stream(data, property_size)


def _decode_collision_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_item_to_give(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_capacity_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_item_percentage_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_respawn_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pickup_effect_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fadetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_activation_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pickup_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_absolute_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_calculate_visibility(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2de4a294(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_home_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_until_home(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_homing_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_spin(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_blink_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_orbit_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0xa09d4a1f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x16d9a75d: ('object_id', _decode_object_id),
    0x3a3e03ba: ('collision_size', _decode_collision_size),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xa02ef0c4: ('item_to_give', _decode_item_to_give),
    0x28c71b54: ('capacity_increase', _decode_capacity_increase),
    0x165ab069: ('item_percentage_increase', _decode_item_percentage_increase),
    0x94af1445: ('amount', _decode_amount),
    0xf7fbaaa5: ('respawn_time', _decode_respawn_time),
    0xc80fc827: ('pickup_effect_lifetime', _decode_pickup_effect_lifetime),
    0x32dc67f6: ('lifetime', _decode_lifetime),
    0x56e3ceef: ('fadetime', _decode_fadetime),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xe585f166: ('activation_delay', _decode_activation_delay),
    0xa9fe872a: ('pickup_effect', _decode_pickup_effect),
    0xe10bcb96: ('absolute_value', _decode_absolute_value),
    0xce33239f: ('calculate_visibility', _decode_calculate_visibility),
    0x2de4a294: ('unknown_0x2de4a294', _decode_unknown_0x2de4a294),
    0xa6ea280d: ('auto_home_range', _decode_auto_home_range),
    0xc2b11cfd: ('delay_until_home', _decode_delay_until_home),
    0x2db59fcf: ('homing_speed', _decode_homing_speed),
    0x961c0d17: ('auto_spin', _decode_auto_spin),
    0xa755eb02: ('blink_out', _decode_blink_out),
    0x850115e4: ('orbit_offset', _decode_orbit_offset),
    0xa09d4a1f: ('unknown_0xa09d4a1f', _decode_unknown_0xa09d4a1f),
}
