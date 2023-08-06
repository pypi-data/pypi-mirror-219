# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class PlayerAlternateSkin(BaseProperty):
    texture_set: int = dataclasses.field(default=0)
    alternate: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    tar: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    super_guide: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    super_guide_alternate: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    invulnerable: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    invulnerable_alternate: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'/\xae\x04z')  # 0x2fae047a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.alternate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\xcf\x02:')  # 0x21cf023a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\xebZh')  # 0x47eb5a68
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_guide.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\t)\xf0')  # 0xfc0929f0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_guide_alternate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5\x9b\x85\x13')  # 0x359b8513
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.invulnerable.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb@l\xa9')  # 0xfb406ca9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.invulnerable_alternate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            texture_set=data['texture_set'],
            alternate=AnimationParameters.from_json(data['alternate']),
            tar=AnimationParameters.from_json(data['tar']),
            super_guide=AnimationParameters.from_json(data['super_guide']),
            super_guide_alternate=AnimationParameters.from_json(data['super_guide_alternate']),
            invulnerable=AnimationParameters.from_json(data['invulnerable']),
            invulnerable_alternate=AnimationParameters.from_json(data['invulnerable_alternate']),
        )

    def to_json(self) -> dict:
        return {
            'texture_set': self.texture_set,
            'alternate': self.alternate.to_json(),
            'tar': self.tar.to_json(),
            'super_guide': self.super_guide.to_json(),
            'super_guide_alternate': self.super_guide_alternate.to_json(),
            'invulnerable': self.invulnerable.to_json(),
            'invulnerable_alternate': self.invulnerable_alternate.to_json(),
        }


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_alternate(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_tar(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_super_guide(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_super_guide_alternate(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_invulnerable(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_invulnerable_alternate(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6b40acef: ('texture_set', _decode_texture_set),
    0x2fae047a: ('alternate', _decode_alternate),
    0x21cf023a: ('tar', _decode_tar),
    0x47eb5a68: ('super_guide', _decode_super_guide),
    0xfc0929f0: ('super_guide_alternate', _decode_super_guide_alternate),
    0x359b8513: ('invulnerable', _decode_invulnerable),
    0xfb406ca9: ('invulnerable_alternate', _decode_invulnerable_alternate),
}
