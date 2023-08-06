# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.UnknownStruct16 import UnknownStruct16


@dataclasses.dataclass()
class UnknownStruct17(BaseProperty):
    unknown_0xb5af7831: float = dataclasses.field(default=-1.0)
    unknown_0xac65eb7a: float = dataclasses.field(default=2.5)
    unknown_0x4f3855a0: float = dataclasses.field(default=4.0)
    unknown_0x08c0b02c: float = dataclasses.field(default=2.5)
    unknown_0x695f68c7: float = dataclasses.field(default=4.0)
    unknown_0xd061ff99: float = dataclasses.field(default=20.0)
    pause_duration_min: float = dataclasses.field(default=1.5)
    pause_duration_max: float = dataclasses.field(default=3.0)
    chance_to_double_dash: float = dataclasses.field(default=0.0)
    unknown_struct16: UnknownStruct16 = dataclasses.field(default_factory=UnknownStruct16)
    unknown_0x3ff87a8c: bool = dataclasses.field(default=False)
    unknown_0x49b9936d: bool = dataclasses.field(default=False)
    unknown_0xc96b8223: bool = dataclasses.field(default=False)
    unknown_0x53fdcb5b: bool = dataclasses.field(default=False)
    unknown_0x0d7ef013: bool = dataclasses.field(default=False)
    unknown_0xaa85c885: bool = dataclasses.field(default=False)
    pause: float = dataclasses.field(default=0.0)
    taunt: float = dataclasses.field(default=0.0)
    look_around: bool = dataclasses.field(default=True)
    melee_attack: float = dataclasses.field(default=0.0)
    melee_dash: float = dataclasses.field(default=0.0)
    scatter_shot: float = dataclasses.field(default=0.0)
    unknown_0x94f48974: float = dataclasses.field(default=0.0)
    dive_attack: float = dataclasses.field(default=0.0)
    unknown_0xb2c1e4fa: bool = dataclasses.field(default=False)
    unknown_0xf5cf3c0f: bool = dataclasses.field(default=True)
    normal_missile: float = dataclasses.field(default=0.0)
    missile_jump: float = dataclasses.field(default=0.0)
    super_missile: float = dataclasses.field(default=0.0)
    unknown_0xe63286eb: float = dataclasses.field(default=0.0)
    unknown_0x4aae6186: float = dataclasses.field(default=0.0)
    sweep_beam: float = dataclasses.field(default=0.0)
    boost_ball: float = dataclasses.field(default=0.0)
    unknown_0x2d7551e6: bool = dataclasses.field(default=False)
    phazon_attack: float = dataclasses.field(default=0.0)
    phazon_enrage: float = dataclasses.field(default=0.0)
    unknown_0x911a2476: bool = dataclasses.field(default=False)

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
        data.write(b'\x00%')  # 37 properties

        data.write(b'\xb5\xafx1')  # 0xb5af7831
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb5af7831))

        data.write(b'\xace\xebz')  # 0xac65eb7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xac65eb7a))

        data.write(b'O8U\xa0')  # 0x4f3855a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f3855a0))

        data.write(b'\x08\xc0\xb0,')  # 0x8c0b02c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x08c0b02c))

        data.write(b'i_h\xc7')  # 0x695f68c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x695f68c7))

        data.write(b'\xd0a\xff\x99')  # 0xd061ff99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd061ff99))

        data.write(b'\x97\xdb\xd4*')  # 0x97dbd42a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause_duration_min))

        data.write(b'q\xbb{\xcb')  # 0x71bb7bcb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause_duration_max))

        data.write(b'\xb7Qw\x8b')  # 0xb751778b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chance_to_double_dash))

        data.write(b'\xd6t\x03H')  # 0xd6740348
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct16.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\xf8z\x8c')  # 0x3ff87a8c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3ff87a8c))

        data.write(b'I\xb9\x93m')  # 0x49b9936d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x49b9936d))

        data.write(b'\xc9k\x82#')  # 0xc96b8223
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc96b8223))

        data.write(b'S\xfd\xcb[')  # 0x53fdcb5b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x53fdcb5b))

        data.write(b'\r~\xf0\x13')  # 0xd7ef013
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0d7ef013))

        data.write(b'\xaa\x85\xc8\x85')  # 0xaa85c885
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xaa85c885))

        data.write(b'\x80\xf7\xe6\x05')  # 0x80f7e605
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause))

        data.write(b'G\x9fjO')  # 0x479f6a4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt))

        data.write(b'w\x87\x91\xf5')  # 0x778791f5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.look_around))

        data.write(b'\xceLFh')  # 0xce4c4668
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack))

        data.write(b'YQ\xa0?')  # 0x5951a03f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_dash))

        data.write(b'\x94aVQ')  # 0x94615651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scatter_shot))

        data.write(b'\x94\xf4\x89t')  # 0x94f48974
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x94f48974))

        data.write(b'n@\xfbv')  # 0x6e40fb76
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dive_attack))

        data.write(b'\xb2\xc1\xe4\xfa')  # 0xb2c1e4fa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb2c1e4fa))

        data.write(b'\xf5\xcf<\x0f')  # 0xf5cf3c0f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf5cf3c0f))

        data.write(b'hG\xef\xa7')  # 0x6847efa7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_missile))

        data.write(b'\x08?\xd6\x02')  # 0x83fd602
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.missile_jump))

        data.write(b'\xdb!@/')  # 0xdb21402f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.super_missile))

        data.write(b'\xe62\x86\xeb')  # 0xe63286eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe63286eb))

        data.write(b'J\xaea\x86')  # 0x4aae6186
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4aae6186))

        data.write(b'+\xd1\xc1[')  # 0x2bd1c15b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sweep_beam))

        data.write(b'\xb56\x93\xfa')  # 0xb53693fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_ball))

        data.write(b'-uQ\xe6')  # 0x2d7551e6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2d7551e6))

        data.write(b'\x93\xa8v\xf3')  # 0x93a876f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_attack))

        data.write(b'\xae\xa2(\xb9')  # 0xaea228b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_enrage))

        data.write(b'\x91\x1a$v')  # 0x911a2476
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x911a2476))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xb5af7831=data['unknown_0xb5af7831'],
            unknown_0xac65eb7a=data['unknown_0xac65eb7a'],
            unknown_0x4f3855a0=data['unknown_0x4f3855a0'],
            unknown_0x08c0b02c=data['unknown_0x08c0b02c'],
            unknown_0x695f68c7=data['unknown_0x695f68c7'],
            unknown_0xd061ff99=data['unknown_0xd061ff99'],
            pause_duration_min=data['pause_duration_min'],
            pause_duration_max=data['pause_duration_max'],
            chance_to_double_dash=data['chance_to_double_dash'],
            unknown_struct16=UnknownStruct16.from_json(data['unknown_struct16']),
            unknown_0x3ff87a8c=data['unknown_0x3ff87a8c'],
            unknown_0x49b9936d=data['unknown_0x49b9936d'],
            unknown_0xc96b8223=data['unknown_0xc96b8223'],
            unknown_0x53fdcb5b=data['unknown_0x53fdcb5b'],
            unknown_0x0d7ef013=data['unknown_0x0d7ef013'],
            unknown_0xaa85c885=data['unknown_0xaa85c885'],
            pause=data['pause'],
            taunt=data['taunt'],
            look_around=data['look_around'],
            melee_attack=data['melee_attack'],
            melee_dash=data['melee_dash'],
            scatter_shot=data['scatter_shot'],
            unknown_0x94f48974=data['unknown_0x94f48974'],
            dive_attack=data['dive_attack'],
            unknown_0xb2c1e4fa=data['unknown_0xb2c1e4fa'],
            unknown_0xf5cf3c0f=data['unknown_0xf5cf3c0f'],
            normal_missile=data['normal_missile'],
            missile_jump=data['missile_jump'],
            super_missile=data['super_missile'],
            unknown_0xe63286eb=data['unknown_0xe63286eb'],
            unknown_0x4aae6186=data['unknown_0x4aae6186'],
            sweep_beam=data['sweep_beam'],
            boost_ball=data['boost_ball'],
            unknown_0x2d7551e6=data['unknown_0x2d7551e6'],
            phazon_attack=data['phazon_attack'],
            phazon_enrage=data['phazon_enrage'],
            unknown_0x911a2476=data['unknown_0x911a2476'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xb5af7831': self.unknown_0xb5af7831,
            'unknown_0xac65eb7a': self.unknown_0xac65eb7a,
            'unknown_0x4f3855a0': self.unknown_0x4f3855a0,
            'unknown_0x08c0b02c': self.unknown_0x08c0b02c,
            'unknown_0x695f68c7': self.unknown_0x695f68c7,
            'unknown_0xd061ff99': self.unknown_0xd061ff99,
            'pause_duration_min': self.pause_duration_min,
            'pause_duration_max': self.pause_duration_max,
            'chance_to_double_dash': self.chance_to_double_dash,
            'unknown_struct16': self.unknown_struct16.to_json(),
            'unknown_0x3ff87a8c': self.unknown_0x3ff87a8c,
            'unknown_0x49b9936d': self.unknown_0x49b9936d,
            'unknown_0xc96b8223': self.unknown_0xc96b8223,
            'unknown_0x53fdcb5b': self.unknown_0x53fdcb5b,
            'unknown_0x0d7ef013': self.unknown_0x0d7ef013,
            'unknown_0xaa85c885': self.unknown_0xaa85c885,
            'pause': self.pause,
            'taunt': self.taunt,
            'look_around': self.look_around,
            'melee_attack': self.melee_attack,
            'melee_dash': self.melee_dash,
            'scatter_shot': self.scatter_shot,
            'unknown_0x94f48974': self.unknown_0x94f48974,
            'dive_attack': self.dive_attack,
            'unknown_0xb2c1e4fa': self.unknown_0xb2c1e4fa,
            'unknown_0xf5cf3c0f': self.unknown_0xf5cf3c0f,
            'normal_missile': self.normal_missile,
            'missile_jump': self.missile_jump,
            'super_missile': self.super_missile,
            'unknown_0xe63286eb': self.unknown_0xe63286eb,
            'unknown_0x4aae6186': self.unknown_0x4aae6186,
            'sweep_beam': self.sweep_beam,
            'boost_ball': self.boost_ball,
            'unknown_0x2d7551e6': self.unknown_0x2d7551e6,
            'phazon_attack': self.phazon_attack,
            'phazon_enrage': self.phazon_enrage,
            'unknown_0x911a2476': self.unknown_0x911a2476,
        }

    def _dependencies_for_unknown_struct16(self, asset_manager):
        yield from self.unknown_struct16.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unknown_struct16, "unknown_struct16", "UnknownStruct16"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct17.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0xb5af7831(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xac65eb7a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4f3855a0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x08c0b02c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x695f68c7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd061ff99(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pause_duration_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pause_duration_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chance_to_double_dash(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct16(data: typing.BinaryIO, property_size: int):
    return UnknownStruct16.from_stream(data, property_size)


def _decode_unknown_0x3ff87a8c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x49b9936d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xc96b8223(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x53fdcb5b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0d7ef013(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xaa85c885(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pause(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_taunt(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_around(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_melee_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_dash(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scatter_shot(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x94f48974(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dive_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb2c1e4fa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf5cf3c0f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_normal_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_super_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe63286eb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4aae6186(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sweep_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d7551e6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_phazon_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_enrage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x911a2476(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb5af7831: ('unknown_0xb5af7831', _decode_unknown_0xb5af7831),
    0xac65eb7a: ('unknown_0xac65eb7a', _decode_unknown_0xac65eb7a),
    0x4f3855a0: ('unknown_0x4f3855a0', _decode_unknown_0x4f3855a0),
    0x8c0b02c: ('unknown_0x08c0b02c', _decode_unknown_0x08c0b02c),
    0x695f68c7: ('unknown_0x695f68c7', _decode_unknown_0x695f68c7),
    0xd061ff99: ('unknown_0xd061ff99', _decode_unknown_0xd061ff99),
    0x97dbd42a: ('pause_duration_min', _decode_pause_duration_min),
    0x71bb7bcb: ('pause_duration_max', _decode_pause_duration_max),
    0xb751778b: ('chance_to_double_dash', _decode_chance_to_double_dash),
    0xd6740348: ('unknown_struct16', _decode_unknown_struct16),
    0x3ff87a8c: ('unknown_0x3ff87a8c', _decode_unknown_0x3ff87a8c),
    0x49b9936d: ('unknown_0x49b9936d', _decode_unknown_0x49b9936d),
    0xc96b8223: ('unknown_0xc96b8223', _decode_unknown_0xc96b8223),
    0x53fdcb5b: ('unknown_0x53fdcb5b', _decode_unknown_0x53fdcb5b),
    0xd7ef013: ('unknown_0x0d7ef013', _decode_unknown_0x0d7ef013),
    0xaa85c885: ('unknown_0xaa85c885', _decode_unknown_0xaa85c885),
    0x80f7e605: ('pause', _decode_pause),
    0x479f6a4f: ('taunt', _decode_taunt),
    0x778791f5: ('look_around', _decode_look_around),
    0xce4c4668: ('melee_attack', _decode_melee_attack),
    0x5951a03f: ('melee_dash', _decode_melee_dash),
    0x94615651: ('scatter_shot', _decode_scatter_shot),
    0x94f48974: ('unknown_0x94f48974', _decode_unknown_0x94f48974),
    0x6e40fb76: ('dive_attack', _decode_dive_attack),
    0xb2c1e4fa: ('unknown_0xb2c1e4fa', _decode_unknown_0xb2c1e4fa),
    0xf5cf3c0f: ('unknown_0xf5cf3c0f', _decode_unknown_0xf5cf3c0f),
    0x6847efa7: ('normal_missile', _decode_normal_missile),
    0x83fd602: ('missile_jump', _decode_missile_jump),
    0xdb21402f: ('super_missile', _decode_super_missile),
    0xe63286eb: ('unknown_0xe63286eb', _decode_unknown_0xe63286eb),
    0x4aae6186: ('unknown_0x4aae6186', _decode_unknown_0x4aae6186),
    0x2bd1c15b: ('sweep_beam', _decode_sweep_beam),
    0xb53693fa: ('boost_ball', _decode_boost_ball),
    0x2d7551e6: ('unknown_0x2d7551e6', _decode_unknown_0x2d7551e6),
    0x93a876f3: ('phazon_attack', _decode_phazon_attack),
    0xaea228b9: ('phazon_enrage', _decode_phazon_enrage),
    0x911a2476: ('unknown_0x911a2476', _decode_unknown_0x911a2476),
}
