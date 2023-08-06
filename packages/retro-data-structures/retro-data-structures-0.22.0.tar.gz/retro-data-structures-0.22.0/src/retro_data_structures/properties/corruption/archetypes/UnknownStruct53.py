# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct53(BaseProperty):
    part_0xccf0cc68: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x9cf6186b: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xafa0d295: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    wpsc_0xb93e46e5: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    below_beam: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    txtr: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_0xab46a8c3: float = dataclasses.field(default=100.0)
    part_0xc89c34fd: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xb10f94c5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    above_missile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    wpsc_0x67dd641e: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    above_fireball: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    part_0xca7f8a50: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    tunnel_steam_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    tunnel_steam_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    sound_steam: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xe13ab25f: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x79169d11: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_mouth_beam: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xbd8e8710: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x7802cbf0: float = dataclasses.field(default=15.0)
    unknown_0x491096be: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xdbf376a9: float = dataclasses.field(default=25.0)
    unknown_0x6d56bc5b: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    sound_beam_telegraph: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_initial_warning: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xf1bf1c16: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x0436327d: float = dataclasses.field(default=500.0)
    unknown_0x772b6eb8: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x154b5804: float = dataclasses.field(default=250.0)
    unknown_0xbc77bd1d: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xacb083ec: float = dataclasses.field(default=100.0)
    unknown_0x0cd1f3cf: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x5804032e: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0xa48bdf63: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x1a058c4f: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)

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
        data.write(b'\x00$')  # 36 properties

        data.write(b'\xcc\xf0\xcch')  # 0xccf0cc68
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xccf0cc68))

        data.write(b'\x9c\xf6\x18k')  # 0x9cf6186b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0x9cf6186b))

        data.write(b'\xaf\xa0\xd2\x95')  # 0xafa0d295
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xafa0d295))

        data.write(b'\xb9>F\xe5')  # 0xb93e46e5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wpsc_0xb93e46e5))

        data.write(b'\x1a\xae=\xb5')  # 0x1aae3db5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.below_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbfO\x8d\x8c')  # 0xbf4f8d8c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.txtr))

        data.write(b'\xabF\xa8\xc3')  # 0xab46a8c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xab46a8c3))

        data.write(b'\xc8\x9c4\xfd')  # 0xc89c34fd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xc89c34fd))

        data.write(b'\xb1\x0f\x94\xc5')  # 0xb10f94c5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xb10f94c5))

        data.write(b'\x0b\xd5nP')  # 0xbd56e50
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.above_missile))

        data.write(b'g\xddd\x1e')  # 0x67dd641e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wpsc_0x67dd641e))

        data.write(b'Q\xfbEB')  # 0x51fb4542
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.above_fireball))

        data.write(b'\xca\x7f\x8aP')  # 0xca7f8a50
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part_0xca7f8a50))

        data.write(b'\xc3B\x87\xe4')  # 0xc34287e4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tunnel_steam_effect))

        data.write(b'o\x88\x86\x88')  # 0x6f888688
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tunnel_steam_texture))

        data.write(b'\x84\xe9\xcc\xc8')  # 0x84e9ccc8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_steam))

        data.write(b'\xe1:\xb2_')  # 0xe13ab25f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xe13ab25f))

        data.write(b'y\x16\x9d\x11')  # 0x79169d11
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x79169d11))

        data.write(b'P7\xfa\xfb')  # 0x5037fafb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_mouth_beam))

        data.write(b'\xbd\x8e\x87\x10')  # 0xbd8e8710
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xbd8e8710))

        data.write(b'x\x02\xcb\xf0')  # 0x7802cbf0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7802cbf0))

        data.write(b'I\x10\x96\xbe')  # 0x491096be
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x491096be))

        data.write(b'\xdb\xf3v\xa9')  # 0xdbf376a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdbf376a9))

        data.write(b'mV\xbc[')  # 0x6d56bc5b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x6d56bc5b))

        data.write(b'M\x0b\xfci')  # 0x4d0bfc69
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_beam_telegraph))

        data.write(b'\x88\x13\xc5a')  # 0x8813c561
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_initial_warning))

        data.write(b'\xf1\xbf\x1c\x16')  # 0xf1bf1c16
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xf1bf1c16))

        data.write(b'\x0462}')  # 0x436327d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0436327d))

        data.write(b'w+n\xb8')  # 0x772b6eb8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x772b6eb8))

        data.write(b'\x15KX\x04')  # 0x154b5804
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x154b5804))

        data.write(b'\xbcw\xbd\x1d')  # 0xbc77bd1d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xbc77bd1d))

        data.write(b'\xac\xb0\x83\xec')  # 0xacb083ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xacb083ec))

        data.write(b'\x0c\xd1\xf3\xcf')  # 0xcd1f3cf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x0cd1f3cf))

        data.write(b'X\x04\x03.')  # 0x5804032e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x5804032e))

        data.write(b'\xa4\x8b\xdfc')  # 0xa48bdf63
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xa48bdf63))

        data.write(b'\x1a\x05\x8cO')  # 0x1a058c4f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x1a058c4f))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            part_0xccf0cc68=data['part_0xccf0cc68'],
            part_0x9cf6186b=data['part_0x9cf6186b'],
            part_0xafa0d295=data['part_0xafa0d295'],
            wpsc_0xb93e46e5=data['wpsc_0xb93e46e5'],
            below_beam=PlasmaBeamInfo.from_json(data['below_beam']),
            txtr=data['txtr'],
            unknown_0xab46a8c3=data['unknown_0xab46a8c3'],
            part_0xc89c34fd=data['part_0xc89c34fd'],
            part_0xb10f94c5=data['part_0xb10f94c5'],
            above_missile=data['above_missile'],
            wpsc_0x67dd641e=data['wpsc_0x67dd641e'],
            above_fireball=data['above_fireball'],
            part_0xca7f8a50=data['part_0xca7f8a50'],
            tunnel_steam_effect=data['tunnel_steam_effect'],
            tunnel_steam_texture=data['tunnel_steam_texture'],
            sound_steam=data['sound_steam'],
            caud_0xe13ab25f=data['caud_0xe13ab25f'],
            caud_0x79169d11=data['caud_0x79169d11'],
            sound_mouth_beam=data['sound_mouth_beam'],
            caud_0xbd8e8710=data['caud_0xbd8e8710'],
            unknown_0x7802cbf0=data['unknown_0x7802cbf0'],
            unknown_0x491096be=data['unknown_0x491096be'],
            unknown_0xdbf376a9=data['unknown_0xdbf376a9'],
            unknown_0x6d56bc5b=data['unknown_0x6d56bc5b'],
            sound_beam_telegraph=data['sound_beam_telegraph'],
            sound_initial_warning=data['sound_initial_warning'],
            unknown_0xf1bf1c16=data['unknown_0xf1bf1c16'],
            unknown_0x0436327d=data['unknown_0x0436327d'],
            unknown_0x772b6eb8=data['unknown_0x772b6eb8'],
            unknown_0x154b5804=data['unknown_0x154b5804'],
            unknown_0xbc77bd1d=data['unknown_0xbc77bd1d'],
            unknown_0xacb083ec=data['unknown_0xacb083ec'],
            unknown_0x0cd1f3cf=data['unknown_0x0cd1f3cf'],
            unknown_0x5804032e=data['unknown_0x5804032e'],
            unknown_0xa48bdf63=data['unknown_0xa48bdf63'],
            unknown_0x1a058c4f=data['unknown_0x1a058c4f'],
        )

    def to_json(self) -> dict:
        return {
            'part_0xccf0cc68': self.part_0xccf0cc68,
            'part_0x9cf6186b': self.part_0x9cf6186b,
            'part_0xafa0d295': self.part_0xafa0d295,
            'wpsc_0xb93e46e5': self.wpsc_0xb93e46e5,
            'below_beam': self.below_beam.to_json(),
            'txtr': self.txtr,
            'unknown_0xab46a8c3': self.unknown_0xab46a8c3,
            'part_0xc89c34fd': self.part_0xc89c34fd,
            'part_0xb10f94c5': self.part_0xb10f94c5,
            'above_missile': self.above_missile,
            'wpsc_0x67dd641e': self.wpsc_0x67dd641e,
            'above_fireball': self.above_fireball,
            'part_0xca7f8a50': self.part_0xca7f8a50,
            'tunnel_steam_effect': self.tunnel_steam_effect,
            'tunnel_steam_texture': self.tunnel_steam_texture,
            'sound_steam': self.sound_steam,
            'caud_0xe13ab25f': self.caud_0xe13ab25f,
            'caud_0x79169d11': self.caud_0x79169d11,
            'sound_mouth_beam': self.sound_mouth_beam,
            'caud_0xbd8e8710': self.caud_0xbd8e8710,
            'unknown_0x7802cbf0': self.unknown_0x7802cbf0,
            'unknown_0x491096be': self.unknown_0x491096be,
            'unknown_0xdbf376a9': self.unknown_0xdbf376a9,
            'unknown_0x6d56bc5b': self.unknown_0x6d56bc5b,
            'sound_beam_telegraph': self.sound_beam_telegraph,
            'sound_initial_warning': self.sound_initial_warning,
            'unknown_0xf1bf1c16': self.unknown_0xf1bf1c16,
            'unknown_0x0436327d': self.unknown_0x0436327d,
            'unknown_0x772b6eb8': self.unknown_0x772b6eb8,
            'unknown_0x154b5804': self.unknown_0x154b5804,
            'unknown_0xbc77bd1d': self.unknown_0xbc77bd1d,
            'unknown_0xacb083ec': self.unknown_0xacb083ec,
            'unknown_0x0cd1f3cf': self.unknown_0x0cd1f3cf,
            'unknown_0x5804032e': self.unknown_0x5804032e,
            'unknown_0xa48bdf63': self.unknown_0xa48bdf63,
            'unknown_0x1a058c4f': self.unknown_0x1a058c4f,
        }


def _decode_part_0xccf0cc68(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0x9cf6186b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xafa0d295(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wpsc_0xb93e46e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_below_beam(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_txtr(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xab46a8c3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part_0xc89c34fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xb10f94c5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_above_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wpsc_0x67dd641e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_above_fireball(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part_0xca7f8a50(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tunnel_steam_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tunnel_steam_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_steam(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xe13ab25f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x79169d11(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_mouth_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xbd8e8710(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x7802cbf0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x491096be(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xdbf376a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d56bc5b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_beam_telegraph(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_initial_warning(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf1bf1c16(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x0436327d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x772b6eb8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x154b5804(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbc77bd1d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xacb083ec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0cd1f3cf(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x5804032e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xa48bdf63(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x1a058c4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xccf0cc68: ('part_0xccf0cc68', _decode_part_0xccf0cc68),
    0x9cf6186b: ('part_0x9cf6186b', _decode_part_0x9cf6186b),
    0xafa0d295: ('part_0xafa0d295', _decode_part_0xafa0d295),
    0xb93e46e5: ('wpsc_0xb93e46e5', _decode_wpsc_0xb93e46e5),
    0x1aae3db5: ('below_beam', _decode_below_beam),
    0xbf4f8d8c: ('txtr', _decode_txtr),
    0xab46a8c3: ('unknown_0xab46a8c3', _decode_unknown_0xab46a8c3),
    0xc89c34fd: ('part_0xc89c34fd', _decode_part_0xc89c34fd),
    0xb10f94c5: ('part_0xb10f94c5', _decode_part_0xb10f94c5),
    0xbd56e50: ('above_missile', _decode_above_missile),
    0x67dd641e: ('wpsc_0x67dd641e', _decode_wpsc_0x67dd641e),
    0x51fb4542: ('above_fireball', _decode_above_fireball),
    0xca7f8a50: ('part_0xca7f8a50', _decode_part_0xca7f8a50),
    0xc34287e4: ('tunnel_steam_effect', _decode_tunnel_steam_effect),
    0x6f888688: ('tunnel_steam_texture', _decode_tunnel_steam_texture),
    0x84e9ccc8: ('sound_steam', _decode_sound_steam),
    0xe13ab25f: ('caud_0xe13ab25f', _decode_caud_0xe13ab25f),
    0x79169d11: ('caud_0x79169d11', _decode_caud_0x79169d11),
    0x5037fafb: ('sound_mouth_beam', _decode_sound_mouth_beam),
    0xbd8e8710: ('caud_0xbd8e8710', _decode_caud_0xbd8e8710),
    0x7802cbf0: ('unknown_0x7802cbf0', _decode_unknown_0x7802cbf0),
    0x491096be: ('unknown_0x491096be', _decode_unknown_0x491096be),
    0xdbf376a9: ('unknown_0xdbf376a9', _decode_unknown_0xdbf376a9),
    0x6d56bc5b: ('unknown_0x6d56bc5b', _decode_unknown_0x6d56bc5b),
    0x4d0bfc69: ('sound_beam_telegraph', _decode_sound_beam_telegraph),
    0x8813c561: ('sound_initial_warning', _decode_sound_initial_warning),
    0xf1bf1c16: ('unknown_0xf1bf1c16', _decode_unknown_0xf1bf1c16),
    0x436327d: ('unknown_0x0436327d', _decode_unknown_0x0436327d),
    0x772b6eb8: ('unknown_0x772b6eb8', _decode_unknown_0x772b6eb8),
    0x154b5804: ('unknown_0x154b5804', _decode_unknown_0x154b5804),
    0xbc77bd1d: ('unknown_0xbc77bd1d', _decode_unknown_0xbc77bd1d),
    0xacb083ec: ('unknown_0xacb083ec', _decode_unknown_0xacb083ec),
    0xcd1f3cf: ('unknown_0x0cd1f3cf', _decode_unknown_0x0cd1f3cf),
    0x5804032e: ('unknown_0x5804032e', _decode_unknown_0x5804032e),
    0xa48bdf63: ('unknown_0xa48bdf63', _decode_unknown_0xa48bdf63),
    0x1a058c4f: ('unknown_0x1a058c4f', _decode_unknown_0x1a058c4f),
}
