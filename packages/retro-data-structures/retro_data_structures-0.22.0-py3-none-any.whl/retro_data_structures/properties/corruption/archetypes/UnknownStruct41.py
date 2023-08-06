# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct41(BaseProperty):
    unknown_0xea4b88c8: float = dataclasses.field(default=12.0)
    unknown_0xaa04f0be: float = dataclasses.field(default=40.0)
    unknown_0x59f8b6d0: float = dataclasses.field(default=3.0)
    unknown_0x460020aa: float = dataclasses.field(default=5.0)
    unknown_0x353abf40: float = dataclasses.field(default=8.0)
    caud_0x2822a8fa: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x95d26130: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xbfb8336b: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xf79adca8: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x68454cb4: float = dataclasses.field(default=20.0)
    beam_sweep: Spline = dataclasses.field(default_factory=Spline)
    beam_sweep2: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xb2671c2a: int = dataclasses.field(default=3)
    beam_track_speed: float = dataclasses.field(default=20.0)
    beam_cancel_range: float = dataclasses.field(default=10.0)
    beam_cancel_time: float = dataclasses.field(default=3.0)
    jump_min_range: float = dataclasses.field(default=5.0)
    jump_max_range: float = dataclasses.field(default=25.0)
    unknown_0xb619c33a: float = dataclasses.field(default=1.0)
    missile_min_range: float = dataclasses.field(default=10.0)
    unknown_0x041abba6: float = dataclasses.field(default=20.0)
    melee_attack_min_range: float = dataclasses.field(default=10.0)
    unknown_0x625f214b: float = dataclasses.field(default=25.0)
    melee_attack_range: float = dataclasses.field(default=40.0)
    unknown_0x3e618127: float = dataclasses.field(default=12.0)
    melee_collide_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    collision_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    hypermode_effect: str = dataclasses.field(default='')
    hypermode_cycle_time: float = dataclasses.field(default=40.0)
    unknown_0xe64bd01e: float = dataclasses.field(default=10.0)
    unknown_0xd8255983: float = dataclasses.field(default=8.0)

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'\xeaK\x88\xc8')  # 0xea4b88c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xea4b88c8))

        data.write(b'\xaa\x04\xf0\xbe')  # 0xaa04f0be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaa04f0be))

        data.write(b'Y\xf8\xb6\xd0')  # 0x59f8b6d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x59f8b6d0))

        data.write(b'F\x00 \xaa')  # 0x460020aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x460020aa))

        data.write(b'5:\xbf@')  # 0x353abf40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x353abf40))

        data.write(b'("\xa8\xfa')  # 0x2822a8fa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x2822a8fa))

        data.write(b'\x95\xd2a0')  # 0x95d26130
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x95d26130))

        data.write(b'\xbf\xb83k')  # 0xbfb8336b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbfb8336b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\x9a\xdc\xa8')  # 0xf79adca8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xf79adca8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'hEL\xb4')  # 0x68454cb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x68454cb4))

        data.write(b'4\xdd\xd2\x1c')  # 0x34ddd21c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_sweep.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9p]\xd6')  # 0x39705dd6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_sweep2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2g\x1c*')  # 0xb2671c2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb2671c2a))

        data.write(b'Tm\xabL')  # 0x546dab4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_track_speed))

        data.write(b'\xfb\xdc\xb4\x0f')  # 0xfbdcb40f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_cancel_range))

        data.write(b'\r"^\n')  # 0xd225e0a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_cancel_time))

        data.write(b'\xcf\xd5p)')  # 0xcfd57029
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_min_range))

        data.write(b'\x8f\x9a\x08_')  # 0x8f9a085f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_max_range))

        data.write(b'\xb6\x19\xc3:')  # 0xb619c33a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb619c33a))

        data.write(b'^\xcc\xb9\x8c')  # 0x5eccb98c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.missile_min_range))

        data.write(b'\x04\x1a\xbb\xa6')  # 0x41abba6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x041abba6))

        data.write(b'\xbe\xad\xf2\xe0')  # 0xbeadf2e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack_min_range))

        data.write(b'b_!K')  # 0x625f214b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x625f214b))

        data.write(b'\xc3\xe4=\x0e')  # 0xc3e43d0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack_range))

        data.write(b">a\x81'")  # 0x3e618127
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3e618127))

        data.write(b'\tP\x80\xd9')  # 0x95080d9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.melee_collide_sound))

        data.write(b'\x0c\xfd19')  # 0xcfd3139
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.collision_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80b\xd2\xf8')  # 0x8062d2f8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.hypermode_effect.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf&\xfc\xfb')  # 0xbf26fcfb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hypermode_cycle_time))

        data.write(b'\xe6K\xd0\x1e')  # 0xe64bd01e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe64bd01e))

        data.write(b'\xd8%Y\x83')  # 0xd8255983
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd8255983))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xea4b88c8=data['unknown_0xea4b88c8'],
            unknown_0xaa04f0be=data['unknown_0xaa04f0be'],
            unknown_0x59f8b6d0=data['unknown_0x59f8b6d0'],
            unknown_0x460020aa=data['unknown_0x460020aa'],
            unknown_0x353abf40=data['unknown_0x353abf40'],
            caud_0x2822a8fa=data['caud_0x2822a8fa'],
            caud_0x95d26130=data['caud_0x95d26130'],
            unknown_0xbfb8336b=Spline.from_json(data['unknown_0xbfb8336b']),
            unknown_0xf79adca8=Spline.from_json(data['unknown_0xf79adca8']),
            unknown_0x68454cb4=data['unknown_0x68454cb4'],
            beam_sweep=Spline.from_json(data['beam_sweep']),
            beam_sweep2=Spline.from_json(data['beam_sweep2']),
            unknown_0xb2671c2a=data['unknown_0xb2671c2a'],
            beam_track_speed=data['beam_track_speed'],
            beam_cancel_range=data['beam_cancel_range'],
            beam_cancel_time=data['beam_cancel_time'],
            jump_min_range=data['jump_min_range'],
            jump_max_range=data['jump_max_range'],
            unknown_0xb619c33a=data['unknown_0xb619c33a'],
            missile_min_range=data['missile_min_range'],
            unknown_0x041abba6=data['unknown_0x041abba6'],
            melee_attack_min_range=data['melee_attack_min_range'],
            unknown_0x625f214b=data['unknown_0x625f214b'],
            melee_attack_range=data['melee_attack_range'],
            unknown_0x3e618127=data['unknown_0x3e618127'],
            melee_collide_sound=data['melee_collide_sound'],
            collision_damage=DamageInfo.from_json(data['collision_damage']),
            hypermode_effect=data['hypermode_effect'],
            hypermode_cycle_time=data['hypermode_cycle_time'],
            unknown_0xe64bd01e=data['unknown_0xe64bd01e'],
            unknown_0xd8255983=data['unknown_0xd8255983'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xea4b88c8': self.unknown_0xea4b88c8,
            'unknown_0xaa04f0be': self.unknown_0xaa04f0be,
            'unknown_0x59f8b6d0': self.unknown_0x59f8b6d0,
            'unknown_0x460020aa': self.unknown_0x460020aa,
            'unknown_0x353abf40': self.unknown_0x353abf40,
            'caud_0x2822a8fa': self.caud_0x2822a8fa,
            'caud_0x95d26130': self.caud_0x95d26130,
            'unknown_0xbfb8336b': self.unknown_0xbfb8336b.to_json(),
            'unknown_0xf79adca8': self.unknown_0xf79adca8.to_json(),
            'unknown_0x68454cb4': self.unknown_0x68454cb4,
            'beam_sweep': self.beam_sweep.to_json(),
            'beam_sweep2': self.beam_sweep2.to_json(),
            'unknown_0xb2671c2a': self.unknown_0xb2671c2a,
            'beam_track_speed': self.beam_track_speed,
            'beam_cancel_range': self.beam_cancel_range,
            'beam_cancel_time': self.beam_cancel_time,
            'jump_min_range': self.jump_min_range,
            'jump_max_range': self.jump_max_range,
            'unknown_0xb619c33a': self.unknown_0xb619c33a,
            'missile_min_range': self.missile_min_range,
            'unknown_0x041abba6': self.unknown_0x041abba6,
            'melee_attack_min_range': self.melee_attack_min_range,
            'unknown_0x625f214b': self.unknown_0x625f214b,
            'melee_attack_range': self.melee_attack_range,
            'unknown_0x3e618127': self.unknown_0x3e618127,
            'melee_collide_sound': self.melee_collide_sound,
            'collision_damage': self.collision_damage.to_json(),
            'hypermode_effect': self.hypermode_effect,
            'hypermode_cycle_time': self.hypermode_cycle_time,
            'unknown_0xe64bd01e': self.unknown_0xe64bd01e,
            'unknown_0xd8255983': self.unknown_0xd8255983,
        }


def _decode_unknown_0xea4b88c8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xaa04f0be(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x59f8b6d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x460020aa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x353abf40(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_caud_0x2822a8fa(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x95d26130(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xbfb8336b(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xf79adca8(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x68454cb4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_sweep(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_beam_sweep2(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xb2671c2a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_beam_track_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_cancel_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_cancel_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_max_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb619c33a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x041abba6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_attack_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x625f214b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3e618127(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_collide_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_hypermode_effect(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_hypermode_cycle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe64bd01e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd8255983(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xea4b88c8: ('unknown_0xea4b88c8', _decode_unknown_0xea4b88c8),
    0xaa04f0be: ('unknown_0xaa04f0be', _decode_unknown_0xaa04f0be),
    0x59f8b6d0: ('unknown_0x59f8b6d0', _decode_unknown_0x59f8b6d0),
    0x460020aa: ('unknown_0x460020aa', _decode_unknown_0x460020aa),
    0x353abf40: ('unknown_0x353abf40', _decode_unknown_0x353abf40),
    0x2822a8fa: ('caud_0x2822a8fa', _decode_caud_0x2822a8fa),
    0x95d26130: ('caud_0x95d26130', _decode_caud_0x95d26130),
    0xbfb8336b: ('unknown_0xbfb8336b', _decode_unknown_0xbfb8336b),
    0xf79adca8: ('unknown_0xf79adca8', _decode_unknown_0xf79adca8),
    0x68454cb4: ('unknown_0x68454cb4', _decode_unknown_0x68454cb4),
    0x34ddd21c: ('beam_sweep', _decode_beam_sweep),
    0x39705dd6: ('beam_sweep2', _decode_beam_sweep2),
    0xb2671c2a: ('unknown_0xb2671c2a', _decode_unknown_0xb2671c2a),
    0x546dab4c: ('beam_track_speed', _decode_beam_track_speed),
    0xfbdcb40f: ('beam_cancel_range', _decode_beam_cancel_range),
    0xd225e0a: ('beam_cancel_time', _decode_beam_cancel_time),
    0xcfd57029: ('jump_min_range', _decode_jump_min_range),
    0x8f9a085f: ('jump_max_range', _decode_jump_max_range),
    0xb619c33a: ('unknown_0xb619c33a', _decode_unknown_0xb619c33a),
    0x5eccb98c: ('missile_min_range', _decode_missile_min_range),
    0x41abba6: ('unknown_0x041abba6', _decode_unknown_0x041abba6),
    0xbeadf2e0: ('melee_attack_min_range', _decode_melee_attack_min_range),
    0x625f214b: ('unknown_0x625f214b', _decode_unknown_0x625f214b),
    0xc3e43d0e: ('melee_attack_range', _decode_melee_attack_range),
    0x3e618127: ('unknown_0x3e618127', _decode_unknown_0x3e618127),
    0x95080d9: ('melee_collide_sound', _decode_melee_collide_sound),
    0xcfd3139: ('collision_damage', _decode_collision_damage),
    0x8062d2f8: ('hypermode_effect', _decode_hypermode_effect),
    0xbf26fcfb: ('hypermode_cycle_time', _decode_hypermode_cycle_time),
    0xe64bd01e: ('unknown_0xe64bd01e', _decode_unknown_0xe64bd01e),
    0xd8255983: ('unknown_0xd8255983', _decode_unknown_0xd8255983),
}
