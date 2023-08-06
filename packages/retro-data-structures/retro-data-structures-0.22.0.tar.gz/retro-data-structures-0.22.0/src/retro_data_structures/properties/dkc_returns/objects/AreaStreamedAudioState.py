# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class AreaStreamedAudioState(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    area_state: enums.MusicEnumB = dataclasses.field(default=enums.MusicEnumB.Unknown1)
    auto_set: bool = dataclasses.field(default=False)
    global_: bool = dataclasses.field(default=False)
    unknown_0xeb9f334c: bool = dataclasses.field(default=False)
    increment_delay: float = dataclasses.field(default=0.0)
    decrement_delay: float = dataclasses.field(default=0.0)
    unknown_0xcab4886b: bool = dataclasses.field(default=False)
    custom_increment_fade_in: float = dataclasses.field(default=0.0)
    custom_increment_fade_out: float = dataclasses.field(default=0.0)
    unknown_0x8c95539a: bool = dataclasses.field(default=False)
    custom_decrement_fade_in: float = dataclasses.field(default=0.0)
    custom_decrement_fade_out: float = dataclasses.field(default=0.0)
    unknown_0x250142a2: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ASAS'

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xd8\xd8#')  # 0xe7d8d823
        data.write(b'\x00\x04')  # size
        self.area_state.to_stream(data)

        data.write(b'\x05\xc9$l')  # 0x5c9246c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_set))

        data.write(b'$\t\xb9\x06')  # 0x2409b906
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.global_))

        data.write(b'\xeb\x9f3L')  # 0xeb9f334c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xeb9f334c))

        data.write(b'\xee\xb3\x90i')  # 0xeeb39069
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.increment_delay))

        data.write(b'$Os8')  # 0x244f7338
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.decrement_delay))

        data.write(b'\xca\xb4\x88k')  # 0xcab4886b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcab4886b))

        data.write(b'\x1b\xb8\x197')  # 0x1bb81937
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_increment_fade_in))

        data.write(b'gH\xb6A')  # 0x6748b641
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_increment_fade_out))

        data.write(b'\x8c\x95S\x9a')  # 0x8c95539a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8c95539a))

        data.write(b'\x07\x1e\x84\xb6')  # 0x71e84b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_decrement_fade_in))

        data.write(b'\xfd\xeb\xa3j')  # 0xfdeba36a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_decrement_fade_out))

        data.write(b'%\x01B\xa2')  # 0x250142a2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x250142a2))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            area_state=enums.MusicEnumB.from_json(data['area_state']),
            auto_set=data['auto_set'],
            global_=data['global_'],
            unknown_0xeb9f334c=data['unknown_0xeb9f334c'],
            increment_delay=data['increment_delay'],
            decrement_delay=data['decrement_delay'],
            unknown_0xcab4886b=data['unknown_0xcab4886b'],
            custom_increment_fade_in=data['custom_increment_fade_in'],
            custom_increment_fade_out=data['custom_increment_fade_out'],
            unknown_0x8c95539a=data['unknown_0x8c95539a'],
            custom_decrement_fade_in=data['custom_decrement_fade_in'],
            custom_decrement_fade_out=data['custom_decrement_fade_out'],
            unknown_0x250142a2=data['unknown_0x250142a2'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'area_state': self.area_state.to_json(),
            'auto_set': self.auto_set,
            'global_': self.global_,
            'unknown_0xeb9f334c': self.unknown_0xeb9f334c,
            'increment_delay': self.increment_delay,
            'decrement_delay': self.decrement_delay,
            'unknown_0xcab4886b': self.unknown_0xcab4886b,
            'custom_increment_fade_in': self.custom_increment_fade_in,
            'custom_increment_fade_out': self.custom_increment_fade_out,
            'unknown_0x8c95539a': self.unknown_0x8c95539a,
            'custom_decrement_fade_in': self.custom_decrement_fade_in,
            'custom_decrement_fade_out': self.custom_decrement_fade_out,
            'unknown_0x250142a2': self.unknown_0x250142a2,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_area_state(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumB.from_stream(data)


def _decode_auto_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_global_(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xeb9f334c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_increment_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_decrement_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcab4886b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_custom_increment_fade_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_custom_increment_fade_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8c95539a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_custom_decrement_fade_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_custom_decrement_fade_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x250142a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe7d8d823: ('area_state', _decode_area_state),
    0x5c9246c: ('auto_set', _decode_auto_set),
    0x2409b906: ('global_', _decode_global_),
    0xeb9f334c: ('unknown_0xeb9f334c', _decode_unknown_0xeb9f334c),
    0xeeb39069: ('increment_delay', _decode_increment_delay),
    0x244f7338: ('decrement_delay', _decode_decrement_delay),
    0xcab4886b: ('unknown_0xcab4886b', _decode_unknown_0xcab4886b),
    0x1bb81937: ('custom_increment_fade_in', _decode_custom_increment_fade_in),
    0x6748b641: ('custom_increment_fade_out', _decode_custom_increment_fade_out),
    0x8c95539a: ('unknown_0x8c95539a', _decode_unknown_0x8c95539a),
    0x71e84b6: ('custom_decrement_fade_in', _decode_custom_decrement_fade_in),
    0xfdeba36a: ('custom_decrement_fade_out', _decode_custom_decrement_fade_out),
    0x250142a2: ('unknown_0x250142a2', _decode_unknown_0x250142a2),
}
