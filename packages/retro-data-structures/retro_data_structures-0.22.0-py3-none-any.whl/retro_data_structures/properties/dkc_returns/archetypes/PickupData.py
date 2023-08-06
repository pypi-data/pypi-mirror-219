# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class PickupData(BaseProperty):
    item_to_give: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana)
    capacity_increase: int = dataclasses.field(default=1)
    item_percentage_increase: int = dataclasses.field(default=0)
    amount: int = dataclasses.field(default=1)
    unknown_0x39262bce: int = dataclasses.field(default=1)
    respawn_time: float = dataclasses.field(default=0.0)
    lifetime: float = dataclasses.field(default=0.0)
    fadetime: float = dataclasses.field(default=0.0)
    fade_out_time: float = dataclasses.field(default=2.0)
    activation_delay: float = dataclasses.field(default=0.0)
    unknown_0x059fefc5: float = dataclasses.field(default=0.25)
    flying_pickup_speed: float = dataclasses.field(default=3.0)
    flying_pickup_target_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    flying_pickup_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    flying_pickup_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    pickup_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    touched_sound_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xdb5b110d: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x5dcf63a3: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x9693b006: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    ghost_touched_sound_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x2cf86398: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x93d41865: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x15406acb: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xde1cb96e: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    texture_set: int = dataclasses.field(default=0)
    auto_spin: bool = dataclasses.field(default=False)
    blink_out: bool = dataclasses.field(default=False)
    unknown_0x69539dfc: bool = dataclasses.field(default=True)
    can_render_sort: bool = dataclasses.field(default=True)
    unknown_0x4ddc1327: bool = dataclasses.field(default=False)
    render_in_foreground: bool = dataclasses.field(default=False)
    pickup_delay: float = dataclasses.field(default=0.0)
    unknown_0xe722238d: bool = dataclasses.field(default=True)
    unknown_0xfc7cfe9b: bool = dataclasses.field(default=True)
    unknown_0xea3675c5: bool = dataclasses.field(default=False)

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
        data.write(b'\x00%')  # 37 properties

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

        data.write(b'9&+\xce')  # 0x39262bce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x39262bce))

        data.write(b'\xf7\xfb\xaa\xa5')  # 0xf7fbaaa5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_time))

        data.write(b'2\xdcg\xf6')  # 0x32dc67f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lifetime))

        data.write(b'V\xe3\xce\xef')  # 0x56e3ceef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fadetime))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xe5\x85\xf1f')  # 0xe585f166
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_delay))

        data.write(b'\x05\x9f\xef\xc5')  # 0x59fefc5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x059fefc5))

        data.write(b'L\xd44:')  # 0x4cd4343a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flying_pickup_speed))

        data.write(b'/TV\xa7')  # 0x2f5456a7
        data.write(b'\x00\x0c')  # size
        self.flying_pickup_target_scale.to_stream(data)

        data.write(b'\xed9\x8e\xfb')  # 0xed398efb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flying_pickup_model))

        data.write(b'\xe1\xcb\x9e\xc7')  # 0xe1cb9ec7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flying_pickup_effect))

        data.write(b'\xa9\xfe\x87*')  # 0xa9fe872a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pickup_effect))

        data.write(b'7\x1c\xd74')  # 0x371cd734
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.touched_sound_effect))

        data.write(b'\xaa\x12_\x90')  # 0xaa125f90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xdb[\x11\r')  # 0xdb5b110d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xdb5b110d))

        data.write(b']\xcfc\xa3')  # 0x5dcf63a3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x5dcf63a3))

        data.write(b'\x96\x93\xb0\x06')  # 0x9693b006
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x9693b006))

        data.write(b'\x1e\t;\x02')  # 0x1e093b02
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ghost_touched_sound_effect))

        data.write(b',\xf8c\x98')  # 0x2cf86398
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x2cf86398))

        data.write(b'\x93\xd4\x18e')  # 0x93d41865
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x93d41865))

        data.write(b'\x15@j\xcb')  # 0x15406acb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x15406acb))

        data.write(b'\xde\x1c\xb9n')  # 0xde1cb96e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xde1cb96e))

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'\x96\x1c\r\x17')  # 0x961c0d17
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_spin))

        data.write(b'\xa7U\xeb\x02')  # 0xa755eb02
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.blink_out))

        data.write(b'iS\x9d\xfc')  # 0x69539dfc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x69539dfc))

        data.write(b'\x85\xce\xa2f')  # 0x85cea266
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_render_sort))

        data.write(b"M\xdc\x13'")  # 0x4ddc1327
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4ddc1327))

        data.write(b'\xa6\xaa\x06\xd5')  # 0xa6aa06d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_in_foreground))

        data.write(b'\xbc\x96!O')  # 0xbc96214f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pickup_delay))

        data.write(b'\xe7"#\x8d')  # 0xe722238d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe722238d))

        data.write(b'\xfc|\xfe\x9b')  # 0xfc7cfe9b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xfc7cfe9b))

        data.write(b'\xea6u\xc5')  # 0xea3675c5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xea3675c5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            item_to_give=enums.PlayerItem.from_json(data['item_to_give']),
            capacity_increase=data['capacity_increase'],
            item_percentage_increase=data['item_percentage_increase'],
            amount=data['amount'],
            unknown_0x39262bce=data['unknown_0x39262bce'],
            respawn_time=data['respawn_time'],
            lifetime=data['lifetime'],
            fadetime=data['fadetime'],
            fade_out_time=data['fade_out_time'],
            activation_delay=data['activation_delay'],
            unknown_0x059fefc5=data['unknown_0x059fefc5'],
            flying_pickup_speed=data['flying_pickup_speed'],
            flying_pickup_target_scale=Vector.from_json(data['flying_pickup_target_scale']),
            flying_pickup_model=data['flying_pickup_model'],
            flying_pickup_effect=data['flying_pickup_effect'],
            pickup_effect=data['pickup_effect'],
            touched_sound_effect=data['touched_sound_effect'],
            caud=data['caud'],
            unknown_0xdb5b110d=data['unknown_0xdb5b110d'],
            unknown_0x5dcf63a3=data['unknown_0x5dcf63a3'],
            unknown_0x9693b006=data['unknown_0x9693b006'],
            ghost_touched_sound_effect=data['ghost_touched_sound_effect'],
            unknown_0x2cf86398=data['unknown_0x2cf86398'],
            unknown_0x93d41865=data['unknown_0x93d41865'],
            unknown_0x15406acb=data['unknown_0x15406acb'],
            unknown_0xde1cb96e=data['unknown_0xde1cb96e'],
            texture_set=data['texture_set'],
            auto_spin=data['auto_spin'],
            blink_out=data['blink_out'],
            unknown_0x69539dfc=data['unknown_0x69539dfc'],
            can_render_sort=data['can_render_sort'],
            unknown_0x4ddc1327=data['unknown_0x4ddc1327'],
            render_in_foreground=data['render_in_foreground'],
            pickup_delay=data['pickup_delay'],
            unknown_0xe722238d=data['unknown_0xe722238d'],
            unknown_0xfc7cfe9b=data['unknown_0xfc7cfe9b'],
            unknown_0xea3675c5=data['unknown_0xea3675c5'],
        )

    def to_json(self) -> dict:
        return {
            'item_to_give': self.item_to_give.to_json(),
            'capacity_increase': self.capacity_increase,
            'item_percentage_increase': self.item_percentage_increase,
            'amount': self.amount,
            'unknown_0x39262bce': self.unknown_0x39262bce,
            'respawn_time': self.respawn_time,
            'lifetime': self.lifetime,
            'fadetime': self.fadetime,
            'fade_out_time': self.fade_out_time,
            'activation_delay': self.activation_delay,
            'unknown_0x059fefc5': self.unknown_0x059fefc5,
            'flying_pickup_speed': self.flying_pickup_speed,
            'flying_pickup_target_scale': self.flying_pickup_target_scale.to_json(),
            'flying_pickup_model': self.flying_pickup_model,
            'flying_pickup_effect': self.flying_pickup_effect,
            'pickup_effect': self.pickup_effect,
            'touched_sound_effect': self.touched_sound_effect,
            'caud': self.caud,
            'unknown_0xdb5b110d': self.unknown_0xdb5b110d,
            'unknown_0x5dcf63a3': self.unknown_0x5dcf63a3,
            'unknown_0x9693b006': self.unknown_0x9693b006,
            'ghost_touched_sound_effect': self.ghost_touched_sound_effect,
            'unknown_0x2cf86398': self.unknown_0x2cf86398,
            'unknown_0x93d41865': self.unknown_0x93d41865,
            'unknown_0x15406acb': self.unknown_0x15406acb,
            'unknown_0xde1cb96e': self.unknown_0xde1cb96e,
            'texture_set': self.texture_set,
            'auto_spin': self.auto_spin,
            'blink_out': self.blink_out,
            'unknown_0x69539dfc': self.unknown_0x69539dfc,
            'can_render_sort': self.can_render_sort,
            'unknown_0x4ddc1327': self.unknown_0x4ddc1327,
            'render_in_foreground': self.render_in_foreground,
            'pickup_delay': self.pickup_delay,
            'unknown_0xe722238d': self.unknown_0xe722238d,
            'unknown_0xfc7cfe9b': self.unknown_0xfc7cfe9b,
            'unknown_0xea3675c5': self.unknown_0xea3675c5,
        }


def _decode_item_to_give(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_capacity_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_item_percentage_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x39262bce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_respawn_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fadetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activation_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x059fefc5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flying_pickup_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flying_pickup_target_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_flying_pickup_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flying_pickup_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_pickup_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_touched_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xdb5b110d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x5dcf63a3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x9693b006(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ghost_touched_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x2cf86398(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x93d41865(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x15406acb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xde1cb96e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_auto_spin(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_blink_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x69539dfc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_render_sort(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4ddc1327(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_in_foreground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pickup_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe722238d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xfc7cfe9b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xea3675c5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa02ef0c4: ('item_to_give', _decode_item_to_give),
    0x28c71b54: ('capacity_increase', _decode_capacity_increase),
    0x165ab069: ('item_percentage_increase', _decode_item_percentage_increase),
    0x94af1445: ('amount', _decode_amount),
    0x39262bce: ('unknown_0x39262bce', _decode_unknown_0x39262bce),
    0xf7fbaaa5: ('respawn_time', _decode_respawn_time),
    0x32dc67f6: ('lifetime', _decode_lifetime),
    0x56e3ceef: ('fadetime', _decode_fadetime),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xe585f166: ('activation_delay', _decode_activation_delay),
    0x59fefc5: ('unknown_0x059fefc5', _decode_unknown_0x059fefc5),
    0x4cd4343a: ('flying_pickup_speed', _decode_flying_pickup_speed),
    0x2f5456a7: ('flying_pickup_target_scale', _decode_flying_pickup_target_scale),
    0xed398efb: ('flying_pickup_model', _decode_flying_pickup_model),
    0xe1cb9ec7: ('flying_pickup_effect', _decode_flying_pickup_effect),
    0xa9fe872a: ('pickup_effect', _decode_pickup_effect),
    0x371cd734: ('touched_sound_effect', _decode_touched_sound_effect),
    0xaa125f90: ('caud', _decode_caud),
    0xdb5b110d: ('unknown_0xdb5b110d', _decode_unknown_0xdb5b110d),
    0x5dcf63a3: ('unknown_0x5dcf63a3', _decode_unknown_0x5dcf63a3),
    0x9693b006: ('unknown_0x9693b006', _decode_unknown_0x9693b006),
    0x1e093b02: ('ghost_touched_sound_effect', _decode_ghost_touched_sound_effect),
    0x2cf86398: ('unknown_0x2cf86398', _decode_unknown_0x2cf86398),
    0x93d41865: ('unknown_0x93d41865', _decode_unknown_0x93d41865),
    0x15406acb: ('unknown_0x15406acb', _decode_unknown_0x15406acb),
    0xde1cb96e: ('unknown_0xde1cb96e', _decode_unknown_0xde1cb96e),
    0x6b40acef: ('texture_set', _decode_texture_set),
    0x961c0d17: ('auto_spin', _decode_auto_spin),
    0xa755eb02: ('blink_out', _decode_blink_out),
    0x69539dfc: ('unknown_0x69539dfc', _decode_unknown_0x69539dfc),
    0x85cea266: ('can_render_sort', _decode_can_render_sort),
    0x4ddc1327: ('unknown_0x4ddc1327', _decode_unknown_0x4ddc1327),
    0xa6aa06d5: ('render_in_foreground', _decode_render_in_foreground),
    0xbc96214f: ('pickup_delay', _decode_pickup_delay),
    0xe722238d: ('unknown_0xe722238d', _decode_unknown_0xe722238d),
    0xfc7cfe9b: ('unknown_0xfc7cfe9b', _decode_unknown_0xfc7cfe9b),
    0xea3675c5: ('unknown_0xea3675c5', _decode_unknown_0xea3675c5),
}
