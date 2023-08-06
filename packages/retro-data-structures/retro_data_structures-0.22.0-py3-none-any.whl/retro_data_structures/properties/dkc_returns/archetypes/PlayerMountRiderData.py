# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType


@dataclasses.dataclass()
class PlayerMountRiderData(BaseProperty):
    character_type: PlayerType = dataclasses.field(default_factory=PlayerType)
    mount_locator: str = dataclasses.field(default='')
    alternate_mount_locator: str = dataclasses.field(default='')
    allow_butt_slap_interaction: bool = dataclasses.field(default=False)
    allow_grab_detach: bool = dataclasses.field(default=False)
    allow_crouch: bool = dataclasses.field(default=False)
    generate_arc_motion: bool = dataclasses.field(default=True)
    struggle_turn_priority: int = dataclasses.field(default=1)
    optional_lerp_duration: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x01>5\xfb')  # 0x13e35fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xf9R\xbd')  # 0xe7f952bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.mount_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xf7\x959')  # 0xb0f79539
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.alternate_mount_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j\x1b\xa6o')  # 0x6a1ba66f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_butt_slap_interaction))

        data.write(b'\x1a.cr')  # 0x1a2e6372
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_grab_detach))

        data.write(b"\xab6'\xb8")  # 0xab3627b8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_crouch))

        data.write(b'l\xdf\x86\x83')  # 0x6cdf8683
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.generate_arc_motion))

        data.write(b'E\xe4KN')  # 0x45e44b4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.struggle_turn_priority))

        data.write(b'\xe8)\x96\x9a')  # 0xe829969a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.optional_lerp_duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            character_type=PlayerType.from_json(data['character_type']),
            mount_locator=data['mount_locator'],
            alternate_mount_locator=data['alternate_mount_locator'],
            allow_butt_slap_interaction=data['allow_butt_slap_interaction'],
            allow_grab_detach=data['allow_grab_detach'],
            allow_crouch=data['allow_crouch'],
            generate_arc_motion=data['generate_arc_motion'],
            struggle_turn_priority=data['struggle_turn_priority'],
            optional_lerp_duration=data['optional_lerp_duration'],
        )

    def to_json(self) -> dict:
        return {
            'character_type': self.character_type.to_json(),
            'mount_locator': self.mount_locator,
            'alternate_mount_locator': self.alternate_mount_locator,
            'allow_butt_slap_interaction': self.allow_butt_slap_interaction,
            'allow_grab_detach': self.allow_grab_detach,
            'allow_crouch': self.allow_crouch,
            'generate_arc_motion': self.generate_arc_motion,
            'struggle_turn_priority': self.struggle_turn_priority,
            'optional_lerp_duration': self.optional_lerp_duration,
        }


def _decode_character_type(data: typing.BinaryIO, property_size: int):
    return PlayerType.from_stream(data, property_size)


def _decode_mount_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_alternate_mount_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_allow_butt_slap_interaction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_grab_detach(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_crouch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_generate_arc_motion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_struggle_turn_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_optional_lerp_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13e35fb: ('character_type', _decode_character_type),
    0xe7f952bd: ('mount_locator', _decode_mount_locator),
    0xb0f79539: ('alternate_mount_locator', _decode_alternate_mount_locator),
    0x6a1ba66f: ('allow_butt_slap_interaction', _decode_allow_butt_slap_interaction),
    0x1a2e6372: ('allow_grab_detach', _decode_allow_grab_detach),
    0xab3627b8: ('allow_crouch', _decode_allow_crouch),
    0x6cdf8683: ('generate_arc_motion', _decode_generate_arc_motion),
    0x45e44b4e: ('struggle_turn_priority', _decode_struggle_turn_priority),
    0xe829969a: ('optional_lerp_duration', _decode_optional_lerp_duration),
}
