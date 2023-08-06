# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct24(BaseProperty):
    welding_tip: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    welding_torch: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    welding_beam: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xea2c7744: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x5a3ed5a0: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    start_weld: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    inside_collision: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    outside_collision: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x5b468021: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    cmdl: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    weld_shatter: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0xbface762: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3761c8e8: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    weld_torch_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    weld_beam_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    inside_weld_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    outside_weld_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x1961d4a5: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    start_weld_sound: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    weld_succeeded_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    weld_failed_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x902d66f9: float = dataclasses.field(default=0.25)
    unknown_0xedf4020e: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x9cf48efc: float = dataclasses.field(default=100.0)
    welding_time: float = dataclasses.field(default=10.0)

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
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'j\xde\x8b\x91')  # 0x6ade8b91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.welding_tip.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb\xf9V\x9b')  # 0xfbf9569b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.welding_torch))

        data.write(b'\x8e\x14V{')  # 0x8e14567b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.welding_beam))

        data.write(b'\xea,wD')  # 0xea2c7744
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xea2c7744))

        data.write(b'Z>\xd5\xa0')  # 0x5a3ed5a0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x5a3ed5a0))

        data.write(b"p\xbe\xd4'")  # 0x70bed427
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.start_weld))

        data.write(b'\xac\xd3i\xc1')  # 0xacd369c1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inside_collision))

        data.write(b'\x1d\xad\x13\xa3')  # 0x1dad13a3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.outside_collision))

        data.write(b'[F\x80!')  # 0x5b468021
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x5b468021))

        data.write(b'\xce\xca\xd2\xc3')  # 0xcecad2c3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl))

        data.write(b'~T.\xaa')  # 0x7e542eaa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weld_shatter))

        data.write(b'\xbf\xac\xe7b')  # 0xbface762
        data.write(b'\x00\x10')  # size
        self.unknown_0xbface762.to_stream(data)

        data.write(b'7a\xc8\xe8')  # 0x3761c8e8
        data.write(b'\x00\x10')  # size
        self.unknown_0x3761c8e8.to_stream(data)

        data.write(b'1\xc8\xbc\xaa')  # 0x31c8bcaa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weld_torch_sound))

        data.write(b'\x1e\x1aI\xd5')  # 0x1e1a49d5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weld_beam_sound))

        data.write(b'J\x8c\xf2\xf7')  # 0x4a8cf2f7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inside_weld_sound))

        data.write(b'\xfb\xf2\x88\x95')  # 0xfbf28895
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.outside_weld_sound))

        data.write(b'\x19a\xd4\xa5')  # 0x1961d4a5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x1961d4a5))

        data.write(b'\x1f\xe9f\xf1')  # 0x1fe966f1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.start_weld_sound))

        data.write(b'}\xec\x1a\xef')  # 0x7dec1aef
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weld_succeeded_sound))

        data.write(b'\xb3\xb5\xc8\xcb')  # 0xb3b5c8cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weld_failed_sound))

        data.write(b'\x90-f\xf9')  # 0x902d66f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x902d66f9))

        data.write(b'\xed\xf4\x02\x0e')  # 0xedf4020e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xedf4020e))

        data.write(b'\x9c\xf4\x8e\xfc')  # 0x9cf48efc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9cf48efc))

        data.write(b'\xe6\x98\x94\x1f')  # 0xe698941f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.welding_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            welding_tip=AnimationParameters.from_json(data['welding_tip']),
            welding_torch=data['welding_torch'],
            welding_beam=data['welding_beam'],
            part_0xea2c7744=data['part_0xea2c7744'],
            part_0x5a3ed5a0=data['part_0x5a3ed5a0'],
            start_weld=data['start_weld'],
            inside_collision=data['inside_collision'],
            outside_collision=data['outside_collision'],
            part_0x5b468021=data['part_0x5b468021'],
            cmdl=data['cmdl'],
            weld_shatter=data['weld_shatter'],
            unknown_0xbface762=Color.from_json(data['unknown_0xbface762']),
            unknown_0x3761c8e8=Color.from_json(data['unknown_0x3761c8e8']),
            weld_torch_sound=data['weld_torch_sound'],
            weld_beam_sound=data['weld_beam_sound'],
            inside_weld_sound=data['inside_weld_sound'],
            outside_weld_sound=data['outside_weld_sound'],
            unknown_0x1961d4a5=data['unknown_0x1961d4a5'],
            start_weld_sound=data['start_weld_sound'],
            weld_succeeded_sound=data['weld_succeeded_sound'],
            weld_failed_sound=data['weld_failed_sound'],
            unknown_0x902d66f9=data['unknown_0x902d66f9'],
            unknown_0xedf4020e=data['unknown_0xedf4020e'],
            unknown_0x9cf48efc=data['unknown_0x9cf48efc'],
            welding_time=data['welding_time'],
        )

    def to_json(self) -> dict:
        return {
            'welding_tip': self.welding_tip.to_json(),
            'welding_torch': self.welding_torch,
            'welding_beam': self.welding_beam,
            'part_0xea2c7744': self.part_0xea2c7744,
            'part_0x5a3ed5a0': self.part_0x5a3ed5a0,
            'start_weld': self.start_weld,
            'inside_collision': self.inside_collision,
            'outside_collision': self.outside_collision,
            'part_0x5b468021': self.part_0x5b468021,
            'cmdl': self.cmdl,
            'weld_shatter': self.weld_shatter,
            'unknown_0xbface762': self.unknown_0xbface762.to_json(),
            'unknown_0x3761c8e8': self.unknown_0x3761c8e8.to_json(),
            'weld_torch_sound': self.weld_torch_sound,
            'weld_beam_sound': self.weld_beam_sound,
            'inside_weld_sound': self.inside_weld_sound,
            'outside_weld_sound': self.outside_weld_sound,
            'unknown_0x1961d4a5': self.unknown_0x1961d4a5,
            'start_weld_sound': self.start_weld_sound,
            'weld_succeeded_sound': self.weld_succeeded_sound,
            'weld_failed_sound': self.weld_failed_sound,
            'unknown_0x902d66f9': self.unknown_0x902d66f9,
            'unknown_0xedf4020e': self.unknown_0xedf4020e,
            'unknown_0x9cf48efc': self.unknown_0x9cf48efc,
            'welding_time': self.welding_time,
        }


def _decode_welding_tip(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_welding_torch(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_welding_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xea2c7744(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x5a3ed5a0(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_start_weld(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inside_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_outside_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x5b468021(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_weld_shatter(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xbface762(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3761c8e8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_weld_torch_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_weld_beam_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inside_weld_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_outside_weld_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x1961d4a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_start_weld_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_weld_succeeded_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_weld_failed_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x902d66f9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xedf4020e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9cf48efc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_welding_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6ade8b91: ('welding_tip', _decode_welding_tip),
    0xfbf9569b: ('welding_torch', _decode_welding_torch),
    0x8e14567b: ('welding_beam', _decode_welding_beam),
    0xea2c7744: ('part_0xea2c7744', _decode_part_0xea2c7744),
    0x5a3ed5a0: ('part_0x5a3ed5a0', _decode_part_0x5a3ed5a0),
    0x70bed427: ('start_weld', _decode_start_weld),
    0xacd369c1: ('inside_collision', _decode_inside_collision),
    0x1dad13a3: ('outside_collision', _decode_outside_collision),
    0x5b468021: ('part_0x5b468021', _decode_part_0x5b468021),
    0xcecad2c3: ('cmdl', _decode_cmdl),
    0x7e542eaa: ('weld_shatter', _decode_weld_shatter),
    0xbface762: ('unknown_0xbface762', _decode_unknown_0xbface762),
    0x3761c8e8: ('unknown_0x3761c8e8', _decode_unknown_0x3761c8e8),
    0x31c8bcaa: ('weld_torch_sound', _decode_weld_torch_sound),
    0x1e1a49d5: ('weld_beam_sound', _decode_weld_beam_sound),
    0x4a8cf2f7: ('inside_weld_sound', _decode_inside_weld_sound),
    0xfbf28895: ('outside_weld_sound', _decode_outside_weld_sound),
    0x1961d4a5: ('unknown_0x1961d4a5', _decode_unknown_0x1961d4a5),
    0x1fe966f1: ('start_weld_sound', _decode_start_weld_sound),
    0x7dec1aef: ('weld_succeeded_sound', _decode_weld_succeeded_sound),
    0xb3b5c8cb: ('weld_failed_sound', _decode_weld_failed_sound),
    0x902d66f9: ('unknown_0x902d66f9', _decode_unknown_0x902d66f9),
    0xedf4020e: ('unknown_0xedf4020e', _decode_unknown_0xedf4020e),
    0x9cf48efc: ('unknown_0x9cf48efc', _decode_unknown_0x9cf48efc),
    0xe698941f: ('welding_time', _decode_welding_time),
}
