# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class LUAScript(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    abandoned_world: AssetId = dataclasses.field(metadata={'asset_types': ['MLVL']}, default=default_asset_id)
    phaaze_world: AssetId = dataclasses.field(metadata={'asset_types': ['MLVL']}, default=default_asset_id)
    unknown_0xed4a2787: str = dataclasses.field(default='')
    unknown_0x9facea01: str = dataclasses.field(default='')
    unknown_0xea46b664: str = dataclasses.field(default='')
    unknown_0xa1ecc54b: str = dataclasses.field(default='')

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'LUAX'

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
        data.write(b'\x00\x05')  # 5 properties
        num_properties_written = 5

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if self.abandoned_world != default_override.get('abandoned_world', default_asset_id):
            num_properties_written += 1
            data.write(b'+\xf9\xaet')  # 0x2bf9ae74
            data.write(b'\x00\x08')  # size
            data.write(struct.pack(">Q", self.abandoned_world))

        if self.phaaze_world != default_override.get('phaaze_world', default_asset_id):
            num_properties_written += 1
            data.write(b'VzH\xf4')  # 0x567a48f4
            data.write(b'\x00\x08')  # size
            data.write(struct.pack(">Q", self.phaaze_world))

        data.write(b"\xedJ'\x87")  # 0xed4a2787
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xed4a2787.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9f\xac\xea\x01')  # 0x9facea01
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x9facea01.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeaF\xb6d')  # 0xea46b664
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xea46b664.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1\xec\xc5K')  # 0xa1ecc54b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xa1ecc54b.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.write(struct.pack(">H", num_properties_written))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            abandoned_world=data['abandoned_world'],
            phaaze_world=data['phaaze_world'],
            unknown_0xed4a2787=data['unknown_0xed4a2787'],
            unknown_0x9facea01=data['unknown_0x9facea01'],
            unknown_0xea46b664=data['unknown_0xea46b664'],
            unknown_0xa1ecc54b=data['unknown_0xa1ecc54b'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'abandoned_world': self.abandoned_world,
            'phaaze_world': self.phaaze_world,
            'unknown_0xed4a2787': self.unknown_0xed4a2787,
            'unknown_0x9facea01': self.unknown_0x9facea01,
            'unknown_0xea46b664': self.unknown_0xea46b664,
            'unknown_0xa1ecc54b': self.unknown_0xa1ecc54b,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_abandoned_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_phaaze_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xed4a2787(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x9facea01(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0xea46b664(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0xa1ecc54b(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x2bf9ae74: ('abandoned_world', _decode_abandoned_world),
    0x567a48f4: ('phaaze_world', _decode_phaaze_world),
    0xed4a2787: ('unknown_0xed4a2787', _decode_unknown_0xed4a2787),
    0x9facea01: ('unknown_0x9facea01', _decode_unknown_0x9facea01),
    0xea46b664: ('unknown_0xea46b664', _decode_unknown_0xea46b664),
    0xa1ecc54b: ('unknown_0xa1ecc54b', _decode_unknown_0xa1ecc54b),
}
