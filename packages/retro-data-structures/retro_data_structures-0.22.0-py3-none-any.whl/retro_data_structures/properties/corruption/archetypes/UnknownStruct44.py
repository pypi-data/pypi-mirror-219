# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.GrappleData import GrappleData
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct44(BaseProperty):
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    carapace1: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    carapace2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    stomach_plate: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    tongue_piece: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    tongue_tip: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    max_grapple_distance: float = dataclasses.field(default=25.0)
    grapple_data: GrappleData = dataclasses.field(default_factory=GrappleData)
    sound_stomach_hit: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_phazon_lance: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_tongue_attack_loop: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_tongue_latch: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    sound_tongue_release: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\x86\x1c\xd2\xa0')  # 0x861cd2a0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wpsc))

        data.write(b'\xa8\xc2\xacv')  # 0xa8c2ac76
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.carapace1))

        data.write(b'.V\xde\xd8')  # 0x2e56ded8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.carapace2))

        data.write(b'\xf4tv\xce')  # 0xf47476ce
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stomach_plate))

        data.write(b'G\x03\x06\xbe')  # 0x470306be
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tongue_piece))

        data.write(b'\x87\x95/\xc5')  # 0x87952fc5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tongue_tip))

        data.write(b'\x01\xd8.\xeb')  # 0x1d82eeb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'\x1c\xc99\x84')  # 0x1cc93984
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_grapple_distance))

        data.write(b'\xf6\t\xc67')  # 0xf609c637
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\x87y+')  # 0xd887792b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_stomach_hit))

        data.write(b'\xf9\x82ds')  # 0xf9826473
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_phazon_lance))

        data.write(b'\x9dn\x1aG')  # 0x9d6e1a47
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_tongue_attack_loop))

        data.write(b'\x87\xe6\xe9X')  # 0x87e6e958
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_tongue_latch))

        data.write(b'\xa6Yx9')  # 0xa6597839
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_tongue_release))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            wpsc=data['wpsc'],
            carapace1=data['carapace1'],
            carapace2=data['carapace2'],
            stomach_plate=data['stomach_plate'],
            tongue_piece=data['tongue_piece'],
            tongue_tip=data['tongue_tip'],
            part=data['part'],
            max_grapple_distance=data['max_grapple_distance'],
            grapple_data=GrappleData.from_json(data['grapple_data']),
            sound_stomach_hit=data['sound_stomach_hit'],
            sound_phazon_lance=data['sound_phazon_lance'],
            sound_tongue_attack_loop=data['sound_tongue_attack_loop'],
            sound_tongue_latch=data['sound_tongue_latch'],
            sound_tongue_release=data['sound_tongue_release'],
        )

    def to_json(self) -> dict:
        return {
            'wpsc': self.wpsc,
            'carapace1': self.carapace1,
            'carapace2': self.carapace2,
            'stomach_plate': self.stomach_plate,
            'tongue_piece': self.tongue_piece,
            'tongue_tip': self.tongue_tip,
            'part': self.part,
            'max_grapple_distance': self.max_grapple_distance,
            'grapple_data': self.grapple_data.to_json(),
            'sound_stomach_hit': self.sound_stomach_hit,
            'sound_phazon_lance': self.sound_phazon_lance,
            'sound_tongue_attack_loop': self.sound_tongue_attack_loop,
            'sound_tongue_latch': self.sound_tongue_latch,
            'sound_tongue_release': self.sound_tongue_release,
        }


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_carapace1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_carapace2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stomach_plate(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tongue_piece(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tongue_tip(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_max_grapple_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_data(data: typing.BinaryIO, property_size: int):
    return GrappleData.from_stream(data, property_size)


def _decode_sound_stomach_hit(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_phazon_lance(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_tongue_attack_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_tongue_latch(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_tongue_release(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x861cd2a0: ('wpsc', _decode_wpsc),
    0xa8c2ac76: ('carapace1', _decode_carapace1),
    0x2e56ded8: ('carapace2', _decode_carapace2),
    0xf47476ce: ('stomach_plate', _decode_stomach_plate),
    0x470306be: ('tongue_piece', _decode_tongue_piece),
    0x87952fc5: ('tongue_tip', _decode_tongue_tip),
    0x1d82eeb: ('part', _decode_part),
    0x1cc93984: ('max_grapple_distance', _decode_max_grapple_distance),
    0xf609c637: ('grapple_data', _decode_grapple_data),
    0xd887792b: ('sound_stomach_hit', _decode_sound_stomach_hit),
    0xf9826473: ('sound_phazon_lance', _decode_sound_phazon_lance),
    0x9d6e1a47: ('sound_tongue_attack_loop', _decode_sound_tongue_attack_loop),
    0x87e6e958: ('sound_tongue_latch', _decode_sound_tongue_latch),
    0xa6597839: ('sound_tongue_release', _decode_sound_tongue_release),
}
