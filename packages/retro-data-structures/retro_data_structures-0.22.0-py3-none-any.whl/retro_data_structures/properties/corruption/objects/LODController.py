# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class LODController(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0x00b17e5f: int = dataclasses.field(default=1)
    model01: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance01: float = dataclasses.field(default=0.0)
    model02: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance02: float = dataclasses.field(default=0.0)
    model03: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance03: float = dataclasses.field(default=0.0)
    model04: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance04: float = dataclasses.field(default=0.0)
    model05: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance05: float = dataclasses.field(default=0.0)
    model06: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance06: float = dataclasses.field(default=0.0)
    model07: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance07: float = dataclasses.field(default=0.0)
    model08: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance08: float = dataclasses.field(default=0.0)
    model09: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance09: float = dataclasses.field(default=0.0)
    model10: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    distance10: float = dataclasses.field(default=0.0)
    unknown_0xb67e3bf9: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'LODC'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptLODController.rso']

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xb1~_')  # 0xb17e5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x00b17e5f))

        data.write(b'\x03\xbe\xe4~')  # 0x3bee47e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model01))

        data.write(b'\xa1\x01\x8e\xf9')  # 0xa1018ef9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance01))

        data.write(b'\x85*\x96\xd0')  # 0x852a96d0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model02))

        data.write(b"'\x95\xfcW")  # 0x2795fc57
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance02))

        data.write(b'NvEu')  # 0x4e764575
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model03))

        data.write(b'\xec\xc9/\xf2')  # 0xecc92ff2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance03))

        data.write(b'Ssu\xcd')  # 0x537375cd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model04))

        data.write(b'\xf1\xcc\x1fJ')  # 0xf1cc1f4a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance04))

        data.write(b'\x98/\xa6h')  # 0x982fa668
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model05))

        data.write(b':\x90\xcc\xef')  # 0x3a90ccef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance05))

        data.write(b'\x1e\xbb\xd4\xc6')  # 0x1ebbd4c6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model06))

        data.write(b'\xbc\x04\xbeA')  # 0xbc04be41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance06))

        data.write(b'\xd5\xe7\x07c')  # 0xd5e70763
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model07))

        data.write(b'wXm\xe4')  # 0x77586de4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance07))

        data.write(b'$\xb1\xb5\xb6')  # 0x24b1b5b6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model08))

        data.write(b'\x86\x0e\xdf1')  # 0x860edf31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance08))

        data.write(b'\xef\xedf\x13')  # 0xefed6613
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model09))

        data.write(b'MR\x0c\x94')  # 0x4d520c94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance09))

        data.write(b'n\x95<o')  # 0x6e953c6f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model10))

        data.write(b'\xcc*V\xe8')  # 0xcc2a56e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance10))

        data.write(b'\xb6~;\xf9')  # 0xb67e3bf9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb67e3bf9))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_0x00b17e5f=data['unknown_0x00b17e5f'],
            model01=data['model01'],
            distance01=data['distance01'],
            model02=data['model02'],
            distance02=data['distance02'],
            model03=data['model03'],
            distance03=data['distance03'],
            model04=data['model04'],
            distance04=data['distance04'],
            model05=data['model05'],
            distance05=data['distance05'],
            model06=data['model06'],
            distance06=data['distance06'],
            model07=data['model07'],
            distance07=data['distance07'],
            model08=data['model08'],
            distance08=data['distance08'],
            model09=data['model09'],
            distance09=data['distance09'],
            model10=data['model10'],
            distance10=data['distance10'],
            unknown_0xb67e3bf9=data['unknown_0xb67e3bf9'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0x00b17e5f': self.unknown_0x00b17e5f,
            'model01': self.model01,
            'distance01': self.distance01,
            'model02': self.model02,
            'distance02': self.distance02,
            'model03': self.model03,
            'distance03': self.distance03,
            'model04': self.model04,
            'distance04': self.distance04,
            'model05': self.model05,
            'distance05': self.distance05,
            'model06': self.model06,
            'distance06': self.distance06,
            'model07': self.model07,
            'distance07': self.distance07,
            'model08': self.model08,
            'distance08': self.distance08,
            'model09': self.model09,
            'distance09': self.distance09,
            'model10': self.model10,
            'distance10': self.distance10,
            'unknown_0xb67e3bf9': self.unknown_0xb67e3bf9,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0x00b17e5f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_model01(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance01(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model02(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance02(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model03(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance03(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model04(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance04(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model05(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance05(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model06(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance06(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model07(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance07(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model08(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance08(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model09(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance09(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model10(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_distance10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb67e3bf9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb17e5f: ('unknown_0x00b17e5f', _decode_unknown_0x00b17e5f),
    0x3bee47e: ('model01', _decode_model01),
    0xa1018ef9: ('distance01', _decode_distance01),
    0x852a96d0: ('model02', _decode_model02),
    0x2795fc57: ('distance02', _decode_distance02),
    0x4e764575: ('model03', _decode_model03),
    0xecc92ff2: ('distance03', _decode_distance03),
    0x537375cd: ('model04', _decode_model04),
    0xf1cc1f4a: ('distance04', _decode_distance04),
    0x982fa668: ('model05', _decode_model05),
    0x3a90ccef: ('distance05', _decode_distance05),
    0x1ebbd4c6: ('model06', _decode_model06),
    0xbc04be41: ('distance06', _decode_distance06),
    0xd5e70763: ('model07', _decode_model07),
    0x77586de4: ('distance07', _decode_distance07),
    0x24b1b5b6: ('model08', _decode_model08),
    0x860edf31: ('distance08', _decode_distance08),
    0xefed6613: ('model09', _decode_model09),
    0x4d520c94: ('distance09', _decode_distance09),
    0x6e953c6f: ('model10', _decode_model10),
    0xcc2a56e8: ('distance10', _decode_distance10),
    0xb67e3bf9: ('unknown_0xb67e3bf9', _decode_unknown_0xb67e3bf9),
}
