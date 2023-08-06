# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct14(BaseProperty):
    unknown_0xa0d037ee: float = dataclasses.field(default=25.0)
    unknown_0x4f522994: float = dataclasses.field(default=40.0)
    shadow_dash_speed: float = dataclasses.field(default=25.0)
    unknown_0x5d02f384: float = dataclasses.field(default=20.0)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    audio_playback_parms: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_cloak: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_de_cloak: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    shadow_decoy_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    shadow_dash_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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

        data.write(b'\xa0\xd07\xee')  # 0xa0d037ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa0d037ee))

        data.write(b'OR)\x94')  # 0x4f522994
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f522994))

        data.write(b'\x87F\x1c\xc6')  # 0x87461cc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shadow_dash_speed))

        data.write(b']\x02\xf3\x84')  # 0x5d02f384
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d02f384))

        data.write(b'-\xc8\x0bK')  # 0x2dc80b4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part))

        data.write(b'\x039"\x83')  # 0x3392283
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\xed\xcf\xf1')  # 0x9dedcff1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_cloak.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7@\xe0\x1d')  # 0xf740e01d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_de_cloak.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\xf6K\xb4')  # 0xb2f64bb4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shadow_decoy_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\x06tG')  # 0xed067447
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shadow_dash_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xa0d037ee=data['unknown_0xa0d037ee'],
            unknown_0x4f522994=data['unknown_0x4f522994'],
            shadow_dash_speed=data['shadow_dash_speed'],
            unknown_0x5d02f384=data['unknown_0x5d02f384'],
            part=data['part'],
            audio_playback_parms=AudioPlaybackParms.from_json(data['audio_playback_parms']),
            sound_cloak=AudioPlaybackParms.from_json(data['sound_cloak']),
            sound_de_cloak=AudioPlaybackParms.from_json(data['sound_de_cloak']),
            shadow_decoy_vulnerability=DamageVulnerability.from_json(data['shadow_decoy_vulnerability']),
            shadow_dash_vulnerability=DamageVulnerability.from_json(data['shadow_dash_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xa0d037ee': self.unknown_0xa0d037ee,
            'unknown_0x4f522994': self.unknown_0x4f522994,
            'shadow_dash_speed': self.shadow_dash_speed,
            'unknown_0x5d02f384': self.unknown_0x5d02f384,
            'part': self.part,
            'audio_playback_parms': self.audio_playback_parms.to_json(),
            'sound_cloak': self.sound_cloak.to_json(),
            'sound_de_cloak': self.sound_de_cloak.to_json(),
            'shadow_decoy_vulnerability': self.shadow_decoy_vulnerability.to_json(),
            'shadow_dash_vulnerability': self.shadow_dash_vulnerability.to_json(),
        }

    def _dependencies_for_part(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part)

    def _dependencies_for_audio_playback_parms(self, asset_manager):
        yield from self.audio_playback_parms.dependencies_for(asset_manager)

    def _dependencies_for_sound_cloak(self, asset_manager):
        yield from self.sound_cloak.dependencies_for(asset_manager)

    def _dependencies_for_sound_de_cloak(self, asset_manager):
        yield from self.sound_de_cloak.dependencies_for(asset_manager)

    def _dependencies_for_shadow_decoy_vulnerability(self, asset_manager):
        yield from self.shadow_decoy_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_shadow_dash_vulnerability(self, asset_manager):
        yield from self.shadow_dash_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_part, "part", "AssetId"),
            (self._dependencies_for_audio_playback_parms, "audio_playback_parms", "AudioPlaybackParms"),
            (self._dependencies_for_sound_cloak, "sound_cloak", "AudioPlaybackParms"),
            (self._dependencies_for_sound_de_cloak, "sound_de_cloak", "AudioPlaybackParms"),
            (self._dependencies_for_shadow_decoy_vulnerability, "shadow_decoy_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_shadow_dash_vulnerability, "shadow_dash_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct14.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0xa0d037ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4f522994(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shadow_dash_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5d02f384(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_audio_playback_parms(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_cloak(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_de_cloak(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_shadow_decoy_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_shadow_dash_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa0d037ee: ('unknown_0xa0d037ee', _decode_unknown_0xa0d037ee),
    0x4f522994: ('unknown_0x4f522994', _decode_unknown_0x4f522994),
    0x87461cc6: ('shadow_dash_speed', _decode_shadow_dash_speed),
    0x5d02f384: ('unknown_0x5d02f384', _decode_unknown_0x5d02f384),
    0x2dc80b4b: ('part', _decode_part),
    0x3392283: ('audio_playback_parms', _decode_audio_playback_parms),
    0x9dedcff1: ('sound_cloak', _decode_sound_cloak),
    0xf740e01d: ('sound_de_cloak', _decode_sound_de_cloak),
    0xb2f64bb4: ('shadow_decoy_vulnerability', _decode_shadow_decoy_vulnerability),
    0xed067447: ('shadow_dash_vulnerability', _decode_shadow_dash_vulnerability),
}
