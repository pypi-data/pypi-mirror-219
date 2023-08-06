# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class GuiCharacter(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    widget_name: str = dataclasses.field(default='')
    unknown_0x8b891f5a: str = dataclasses.field(default='')
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x181e33cc: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    idle_animation: int = dataclasses.field(default=0)
    unknown_0xc23bd607: int = dataclasses.field(default=0)
    unknown_0x4a6a84c1: int = dataclasses.field(default=0)
    unknown_0x601fce68: int = dataclasses.field(default=0)
    unknown_0x63e53fd8: int = dataclasses.field(default=0)
    unknown_0x247db024: int = dataclasses.field(default=0)
    unknown_0xfdccb479: int = dataclasses.field(default=0)
    unknown_0x10706107: int = dataclasses.field(default=0)
    unknown_0x98e160f8: int = dataclasses.field(default=0)
    unknown_0x3bb7e651: int = dataclasses.field(default=0)
    unknown_0xec556609: int = dataclasses.field(default=0)
    unknown_0xa66bed42: int = dataclasses.field(default=0)
    unknown_0x71896d1a: int = dataclasses.field(default=0)
    unknown_0xd2dfebb3: int = dataclasses.field(default=0)
    unknown_0x053d6beb: int = dataclasses.field(default=0)
    unknown_0x46a2fd25: int = dataclasses.field(default=0)
    unknown_0x91407d7d: int = dataclasses.field(default=0)
    unknown_0x579ed88f: int = dataclasses.field(default=0)
    unknown_0x807c58d7: int = dataclasses.field(default=0)
    unknown_0x232ade7e: int = dataclasses.field(default=0)
    unknown_0xf4c85e26: int = dataclasses.field(default=0)
    unknown_0xbef6d56d: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'GUCH'

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
        data.write(b'\x00\x1c')  # 28 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|$W\xbc')  # 0x7c2457bc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.widget_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\x89\x1fZ')  # 0x8b891f5a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x8b891f5a.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18\x1e3\xcc')  # 0x181e33cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x181e33cc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\xa5\xb3\x8f')  # 0xa2a5b38f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.idle_animation))

        data.write(b'\xc2;\xd6\x07')  # 0xc23bd607
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc23bd607))

        data.write(b'Jj\x84\xc1')  # 0x4a6a84c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x4a6a84c1))

        data.write(b'`\x1f\xceh')  # 0x601fce68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x601fce68))

        data.write(b'c\xe5?\xd8')  # 0x63e53fd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x63e53fd8))

        data.write(b'$}\xb0$')  # 0x247db024
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x247db024))

        data.write(b'\xfd\xcc\xb4y')  # 0xfdccb479
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xfdccb479))

        data.write(b'\x10pa\x07')  # 0x10706107
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x10706107))

        data.write(b'\x98\xe1`\xf8')  # 0x98e160f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x98e160f8))

        data.write(b';\xb7\xe6Q')  # 0x3bb7e651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x3bb7e651))

        data.write(b'\xecUf\t')  # 0xec556609
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xec556609))

        data.write(b'\xa6k\xedB')  # 0xa66bed42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa66bed42))

        data.write(b'q\x89m\x1a')  # 0x71896d1a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x71896d1a))

        data.write(b'\xd2\xdf\xeb\xb3')  # 0xd2dfebb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd2dfebb3))

        data.write(b'\x05=k\xeb')  # 0x53d6beb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x053d6beb))

        data.write(b'F\xa2\xfd%')  # 0x46a2fd25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x46a2fd25))

        data.write(b'\x91@}}')  # 0x91407d7d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x91407d7d))

        data.write(b'W\x9e\xd8\x8f')  # 0x579ed88f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x579ed88f))

        data.write(b'\x80|X\xd7')  # 0x807c58d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x807c58d7))

        data.write(b'#*\xde~')  # 0x232ade7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x232ade7e))

        data.write(b'\xf4\xc8^&')  # 0xf4c85e26
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf4c85e26))

        data.write(b'\xbe\xf6\xd5m')  # 0xbef6d56d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbef6d56d))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            widget_name=data['widget_name'],
            unknown_0x8b891f5a=data['unknown_0x8b891f5a'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            unknown_0x181e33cc=AnimationParameters.from_json(data['unknown_0x181e33cc']),
            idle_animation=data['idle_animation'],
            unknown_0xc23bd607=data['unknown_0xc23bd607'],
            unknown_0x4a6a84c1=data['unknown_0x4a6a84c1'],
            unknown_0x601fce68=data['unknown_0x601fce68'],
            unknown_0x63e53fd8=data['unknown_0x63e53fd8'],
            unknown_0x247db024=data['unknown_0x247db024'],
            unknown_0xfdccb479=data['unknown_0xfdccb479'],
            unknown_0x10706107=data['unknown_0x10706107'],
            unknown_0x98e160f8=data['unknown_0x98e160f8'],
            unknown_0x3bb7e651=data['unknown_0x3bb7e651'],
            unknown_0xec556609=data['unknown_0xec556609'],
            unknown_0xa66bed42=data['unknown_0xa66bed42'],
            unknown_0x71896d1a=data['unknown_0x71896d1a'],
            unknown_0xd2dfebb3=data['unknown_0xd2dfebb3'],
            unknown_0x053d6beb=data['unknown_0x053d6beb'],
            unknown_0x46a2fd25=data['unknown_0x46a2fd25'],
            unknown_0x91407d7d=data['unknown_0x91407d7d'],
            unknown_0x579ed88f=data['unknown_0x579ed88f'],
            unknown_0x807c58d7=data['unknown_0x807c58d7'],
            unknown_0x232ade7e=data['unknown_0x232ade7e'],
            unknown_0xf4c85e26=data['unknown_0xf4c85e26'],
            unknown_0xbef6d56d=data['unknown_0xbef6d56d'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'widget_name': self.widget_name,
            'unknown_0x8b891f5a': self.unknown_0x8b891f5a,
            'actor_information': self.actor_information.to_json(),
            'character_animation_information': self.character_animation_information.to_json(),
            'unknown_0x181e33cc': self.unknown_0x181e33cc.to_json(),
            'idle_animation': self.idle_animation,
            'unknown_0xc23bd607': self.unknown_0xc23bd607,
            'unknown_0x4a6a84c1': self.unknown_0x4a6a84c1,
            'unknown_0x601fce68': self.unknown_0x601fce68,
            'unknown_0x63e53fd8': self.unknown_0x63e53fd8,
            'unknown_0x247db024': self.unknown_0x247db024,
            'unknown_0xfdccb479': self.unknown_0xfdccb479,
            'unknown_0x10706107': self.unknown_0x10706107,
            'unknown_0x98e160f8': self.unknown_0x98e160f8,
            'unknown_0x3bb7e651': self.unknown_0x3bb7e651,
            'unknown_0xec556609': self.unknown_0xec556609,
            'unknown_0xa66bed42': self.unknown_0xa66bed42,
            'unknown_0x71896d1a': self.unknown_0x71896d1a,
            'unknown_0xd2dfebb3': self.unknown_0xd2dfebb3,
            'unknown_0x053d6beb': self.unknown_0x053d6beb,
            'unknown_0x46a2fd25': self.unknown_0x46a2fd25,
            'unknown_0x91407d7d': self.unknown_0x91407d7d,
            'unknown_0x579ed88f': self.unknown_0x579ed88f,
            'unknown_0x807c58d7': self.unknown_0x807c58d7,
            'unknown_0x232ade7e': self.unknown_0x232ade7e,
            'unknown_0xf4c85e26': self.unknown_0xf4c85e26,
            'unknown_0xbef6d56d': self.unknown_0xbef6d56d,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_widget_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x8b891f5a(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x181e33cc(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_idle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc23bd607(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4a6a84c1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x601fce68(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x63e53fd8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x247db024(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xfdccb479(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x10706107(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x98e160f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3bb7e651(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xec556609(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xa66bed42(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x71896d1a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd2dfebb3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x053d6beb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x46a2fd25(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x91407d7d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x579ed88f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x807c58d7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x232ade7e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xf4c85e26(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xbef6d56d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7c2457bc: ('widget_name', _decode_widget_name),
    0x8b891f5a: ('unknown_0x8b891f5a', _decode_unknown_0x8b891f5a),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x181e33cc: ('unknown_0x181e33cc', _decode_unknown_0x181e33cc),
    0xa2a5b38f: ('idle_animation', _decode_idle_animation),
    0xc23bd607: ('unknown_0xc23bd607', _decode_unknown_0xc23bd607),
    0x4a6a84c1: ('unknown_0x4a6a84c1', _decode_unknown_0x4a6a84c1),
    0x601fce68: ('unknown_0x601fce68', _decode_unknown_0x601fce68),
    0x63e53fd8: ('unknown_0x63e53fd8', _decode_unknown_0x63e53fd8),
    0x247db024: ('unknown_0x247db024', _decode_unknown_0x247db024),
    0xfdccb479: ('unknown_0xfdccb479', _decode_unknown_0xfdccb479),
    0x10706107: ('unknown_0x10706107', _decode_unknown_0x10706107),
    0x98e160f8: ('unknown_0x98e160f8', _decode_unknown_0x98e160f8),
    0x3bb7e651: ('unknown_0x3bb7e651', _decode_unknown_0x3bb7e651),
    0xec556609: ('unknown_0xec556609', _decode_unknown_0xec556609),
    0xa66bed42: ('unknown_0xa66bed42', _decode_unknown_0xa66bed42),
    0x71896d1a: ('unknown_0x71896d1a', _decode_unknown_0x71896d1a),
    0xd2dfebb3: ('unknown_0xd2dfebb3', _decode_unknown_0xd2dfebb3),
    0x53d6beb: ('unknown_0x053d6beb', _decode_unknown_0x053d6beb),
    0x46a2fd25: ('unknown_0x46a2fd25', _decode_unknown_0x46a2fd25),
    0x91407d7d: ('unknown_0x91407d7d', _decode_unknown_0x91407d7d),
    0x579ed88f: ('unknown_0x579ed88f', _decode_unknown_0x579ed88f),
    0x807c58d7: ('unknown_0x807c58d7', _decode_unknown_0x807c58d7),
    0x232ade7e: ('unknown_0x232ade7e', _decode_unknown_0x232ade7e),
    0xf4c85e26: ('unknown_0xf4c85e26', _decode_unknown_0xf4c85e26),
    0xbef6d56d: ('unknown_0xbef6d56d', _decode_unknown_0xbef6d56d),
}
