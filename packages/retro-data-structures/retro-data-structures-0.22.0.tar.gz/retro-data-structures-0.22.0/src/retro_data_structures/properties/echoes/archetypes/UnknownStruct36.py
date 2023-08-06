# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms


@dataclasses.dataclass()
class UnknownStruct36(BaseProperty):
    audio_playback_parms_0x4f904909: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x82e108de: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0xdf090545: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x3dd5b3cf: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0xf82231bb: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x009e3658: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x62bd75b1: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown: float = dataclasses.field(default=10.0)
    audio_playback_parms_0x32969cba: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x597d2ac9: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'O\x90I\t')  # 0x4f904909
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x4f904909.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x82\xe1\x08\xde')  # 0x82e108de
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x82e108de.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\t\x05E')  # 0xdf090545
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0xdf090545.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=\xd5\xb3\xcf')  # 0x3dd5b3cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x3dd5b3cf.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8"1\xbb')  # 0xf82231bb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0xf82231bb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\x9e6X')  # 0x9e3658
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x009e3658.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'b\xbdu\xb1')  # 0x62bd75b1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x62bd75b1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\x14\xba\xec')  # 0x7714baec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'2\x96\x9c\xba')  # 0x32969cba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x32969cba.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y}*\xc9')  # 0x597d2ac9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x597d2ac9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            audio_playback_parms_0x4f904909=AudioPlaybackParms.from_json(data['audio_playback_parms_0x4f904909']),
            audio_playback_parms_0x82e108de=AudioPlaybackParms.from_json(data['audio_playback_parms_0x82e108de']),
            audio_playback_parms_0xdf090545=AudioPlaybackParms.from_json(data['audio_playback_parms_0xdf090545']),
            audio_playback_parms_0x3dd5b3cf=AudioPlaybackParms.from_json(data['audio_playback_parms_0x3dd5b3cf']),
            audio_playback_parms_0xf82231bb=AudioPlaybackParms.from_json(data['audio_playback_parms_0xf82231bb']),
            audio_playback_parms_0x009e3658=AudioPlaybackParms.from_json(data['audio_playback_parms_0x009e3658']),
            audio_playback_parms_0x62bd75b1=AudioPlaybackParms.from_json(data['audio_playback_parms_0x62bd75b1']),
            unknown=data['unknown'],
            audio_playback_parms_0x32969cba=AudioPlaybackParms.from_json(data['audio_playback_parms_0x32969cba']),
            audio_playback_parms_0x597d2ac9=AudioPlaybackParms.from_json(data['audio_playback_parms_0x597d2ac9']),
        )

    def to_json(self) -> dict:
        return {
            'audio_playback_parms_0x4f904909': self.audio_playback_parms_0x4f904909.to_json(),
            'audio_playback_parms_0x82e108de': self.audio_playback_parms_0x82e108de.to_json(),
            'audio_playback_parms_0xdf090545': self.audio_playback_parms_0xdf090545.to_json(),
            'audio_playback_parms_0x3dd5b3cf': self.audio_playback_parms_0x3dd5b3cf.to_json(),
            'audio_playback_parms_0xf82231bb': self.audio_playback_parms_0xf82231bb.to_json(),
            'audio_playback_parms_0x009e3658': self.audio_playback_parms_0x009e3658.to_json(),
            'audio_playback_parms_0x62bd75b1': self.audio_playback_parms_0x62bd75b1.to_json(),
            'unknown': self.unknown,
            'audio_playback_parms_0x32969cba': self.audio_playback_parms_0x32969cba.to_json(),
            'audio_playback_parms_0x597d2ac9': self.audio_playback_parms_0x597d2ac9.to_json(),
        }

    def _dependencies_for_audio_playback_parms_0x4f904909(self, asset_manager):
        yield from self.audio_playback_parms_0x4f904909.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x82e108de(self, asset_manager):
        yield from self.audio_playback_parms_0x82e108de.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0xdf090545(self, asset_manager):
        yield from self.audio_playback_parms_0xdf090545.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x3dd5b3cf(self, asset_manager):
        yield from self.audio_playback_parms_0x3dd5b3cf.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0xf82231bb(self, asset_manager):
        yield from self.audio_playback_parms_0xf82231bb.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x009e3658(self, asset_manager):
        yield from self.audio_playback_parms_0x009e3658.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x62bd75b1(self, asset_manager):
        yield from self.audio_playback_parms_0x62bd75b1.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x32969cba(self, asset_manager):
        yield from self.audio_playback_parms_0x32969cba.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x597d2ac9(self, asset_manager):
        yield from self.audio_playback_parms_0x597d2ac9.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_audio_playback_parms_0x4f904909, "audio_playback_parms_0x4f904909", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x82e108de, "audio_playback_parms_0x82e108de", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0xdf090545, "audio_playback_parms_0xdf090545", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x3dd5b3cf, "audio_playback_parms_0x3dd5b3cf", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0xf82231bb, "audio_playback_parms_0xf82231bb", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x009e3658, "audio_playback_parms_0x009e3658", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x62bd75b1, "audio_playback_parms_0x62bd75b1", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x32969cba, "audio_playback_parms_0x32969cba", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x597d2ac9, "audio_playback_parms_0x597d2ac9", "AudioPlaybackParms"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct36.{field_name} ({field_type}): {e}"
                )


def _decode_audio_playback_parms_0x4f904909(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x82e108de(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0xdf090545(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x3dd5b3cf(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0xf82231bb(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x009e3658(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x62bd75b1(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_playback_parms_0x32969cba(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x597d2ac9(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4f904909: ('audio_playback_parms_0x4f904909', _decode_audio_playback_parms_0x4f904909),
    0x82e108de: ('audio_playback_parms_0x82e108de', _decode_audio_playback_parms_0x82e108de),
    0xdf090545: ('audio_playback_parms_0xdf090545', _decode_audio_playback_parms_0xdf090545),
    0x3dd5b3cf: ('audio_playback_parms_0x3dd5b3cf', _decode_audio_playback_parms_0x3dd5b3cf),
    0xf82231bb: ('audio_playback_parms_0xf82231bb', _decode_audio_playback_parms_0xf82231bb),
    0x9e3658: ('audio_playback_parms_0x009e3658', _decode_audio_playback_parms_0x009e3658),
    0x62bd75b1: ('audio_playback_parms_0x62bd75b1', _decode_audio_playback_parms_0x62bd75b1),
    0x7714baec: ('unknown', _decode_unknown),
    0x32969cba: ('audio_playback_parms_0x32969cba', _decode_audio_playback_parms_0x32969cba),
    0x597d2ac9: ('audio_playback_parms_0x597d2ac9', _decode_audio_playback_parms_0x597d2ac9),
}
