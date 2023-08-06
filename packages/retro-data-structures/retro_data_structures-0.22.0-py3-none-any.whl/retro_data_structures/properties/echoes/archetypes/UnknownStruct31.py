# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.IngSpiderballGuardianStruct import IngSpiderballGuardianStruct


@dataclasses.dataclass()
class UnknownStruct31(BaseProperty):
    ing_spiderball_guardian_struct_0x152db484: IngSpiderballGuardianStruct = dataclasses.field(default_factory=IngSpiderballGuardianStruct)
    ing_spiderball_guardian_struct_0x2d163ff7: IngSpiderballGuardianStruct = dataclasses.field(default_factory=IngSpiderballGuardianStruct)
    ing_spiderball_guardian_struct_0x8c2fbb19: IngSpiderballGuardianStruct = dataclasses.field(default_factory=IngSpiderballGuardianStruct)
    ing_spiderball_guardian_struct_0x5d612911: IngSpiderballGuardianStruct = dataclasses.field(default_factory=IngSpiderballGuardianStruct)
    ing_spiderball_guardian_struct_0xfc58adff: IngSpiderballGuardianStruct = dataclasses.field(default_factory=IngSpiderballGuardianStruct)
    ing_spiderball_guardian_struct_0xc463268c: IngSpiderballGuardianStruct = dataclasses.field(default_factory=IngSpiderballGuardianStruct)
    damage_radius: float = dataclasses.field(default=2.0)
    proximity_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown: float = dataclasses.field(default=20.0)
    audio_playback_parms_0xaed23abc: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_spiderball_rolling: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0xcee38f10: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x796fa303: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_enter_stunned: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms_0x44c1f241: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x15-\xb4\x84')  # 0x152db484
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spiderball_guardian_struct_0x152db484.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\x16?\xf7')  # 0x2d163ff7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spiderball_guardian_struct_0x2d163ff7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c/\xbb\x19')  # 0x8c2fbb19
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spiderball_guardian_struct_0x8c2fbb19.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']a)\x11')  # 0x5d612911
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spiderball_guardian_struct_0x5d612911.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfcX\xad\xff')  # 0xfc58adff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spiderball_guardian_struct_0xfc58adff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4c&\x8c')  # 0xc463268c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spiderball_guardian_struct_0xc463268c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0fY\x879')  # 0xf598739
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_radius))

        data.write(b'\xbax\xd2\x81')  # 0xba78d281
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.proximity_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 40.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\x13;9')  # 0x32133b39
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xae\xd2:\xbc')  # 0xaed23abc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0xaed23abc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':^/R')  # 0x3a5e2f52
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_spiderball_rolling.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xce\xe3\x8f\x10')  # 0xcee38f10
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0xcee38f10.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'yo\xa3\x03')  # 0x796fa303
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x796fa303.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd5\xf3\xe9\xc4')  # 0xd5f3e9c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_enter_stunned.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D\xc1\xf2A')  # 0x44c1f241
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x44c1f241.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ing_spiderball_guardian_struct_0x152db484=IngSpiderballGuardianStruct.from_json(data['ing_spiderball_guardian_struct_0x152db484']),
            ing_spiderball_guardian_struct_0x2d163ff7=IngSpiderballGuardianStruct.from_json(data['ing_spiderball_guardian_struct_0x2d163ff7']),
            ing_spiderball_guardian_struct_0x8c2fbb19=IngSpiderballGuardianStruct.from_json(data['ing_spiderball_guardian_struct_0x8c2fbb19']),
            ing_spiderball_guardian_struct_0x5d612911=IngSpiderballGuardianStruct.from_json(data['ing_spiderball_guardian_struct_0x5d612911']),
            ing_spiderball_guardian_struct_0xfc58adff=IngSpiderballGuardianStruct.from_json(data['ing_spiderball_guardian_struct_0xfc58adff']),
            ing_spiderball_guardian_struct_0xc463268c=IngSpiderballGuardianStruct.from_json(data['ing_spiderball_guardian_struct_0xc463268c']),
            damage_radius=data['damage_radius'],
            proximity_damage=DamageInfo.from_json(data['proximity_damage']),
            unknown=data['unknown'],
            audio_playback_parms_0xaed23abc=AudioPlaybackParms.from_json(data['audio_playback_parms_0xaed23abc']),
            sound_spiderball_rolling=AudioPlaybackParms.from_json(data['sound_spiderball_rolling']),
            audio_playback_parms_0xcee38f10=AudioPlaybackParms.from_json(data['audio_playback_parms_0xcee38f10']),
            audio_playback_parms_0x796fa303=AudioPlaybackParms.from_json(data['audio_playback_parms_0x796fa303']),
            sound_enter_stunned=AudioPlaybackParms.from_json(data['sound_enter_stunned']),
            audio_playback_parms_0x44c1f241=AudioPlaybackParms.from_json(data['audio_playback_parms_0x44c1f241']),
        )

    def to_json(self) -> dict:
        return {
            'ing_spiderball_guardian_struct_0x152db484': self.ing_spiderball_guardian_struct_0x152db484.to_json(),
            'ing_spiderball_guardian_struct_0x2d163ff7': self.ing_spiderball_guardian_struct_0x2d163ff7.to_json(),
            'ing_spiderball_guardian_struct_0x8c2fbb19': self.ing_spiderball_guardian_struct_0x8c2fbb19.to_json(),
            'ing_spiderball_guardian_struct_0x5d612911': self.ing_spiderball_guardian_struct_0x5d612911.to_json(),
            'ing_spiderball_guardian_struct_0xfc58adff': self.ing_spiderball_guardian_struct_0xfc58adff.to_json(),
            'ing_spiderball_guardian_struct_0xc463268c': self.ing_spiderball_guardian_struct_0xc463268c.to_json(),
            'damage_radius': self.damage_radius,
            'proximity_damage': self.proximity_damage.to_json(),
            'unknown': self.unknown,
            'audio_playback_parms_0xaed23abc': self.audio_playback_parms_0xaed23abc.to_json(),
            'sound_spiderball_rolling': self.sound_spiderball_rolling.to_json(),
            'audio_playback_parms_0xcee38f10': self.audio_playback_parms_0xcee38f10.to_json(),
            'audio_playback_parms_0x796fa303': self.audio_playback_parms_0x796fa303.to_json(),
            'sound_enter_stunned': self.sound_enter_stunned.to_json(),
            'audio_playback_parms_0x44c1f241': self.audio_playback_parms_0x44c1f241.to_json(),
        }

    def _dependencies_for_ing_spiderball_guardian_struct_0x152db484(self, asset_manager):
        yield from self.ing_spiderball_guardian_struct_0x152db484.dependencies_for(asset_manager)

    def _dependencies_for_ing_spiderball_guardian_struct_0x2d163ff7(self, asset_manager):
        yield from self.ing_spiderball_guardian_struct_0x2d163ff7.dependencies_for(asset_manager)

    def _dependencies_for_ing_spiderball_guardian_struct_0x8c2fbb19(self, asset_manager):
        yield from self.ing_spiderball_guardian_struct_0x8c2fbb19.dependencies_for(asset_manager)

    def _dependencies_for_ing_spiderball_guardian_struct_0x5d612911(self, asset_manager):
        yield from self.ing_spiderball_guardian_struct_0x5d612911.dependencies_for(asset_manager)

    def _dependencies_for_ing_spiderball_guardian_struct_0xfc58adff(self, asset_manager):
        yield from self.ing_spiderball_guardian_struct_0xfc58adff.dependencies_for(asset_manager)

    def _dependencies_for_ing_spiderball_guardian_struct_0xc463268c(self, asset_manager):
        yield from self.ing_spiderball_guardian_struct_0xc463268c.dependencies_for(asset_manager)

    def _dependencies_for_proximity_damage(self, asset_manager):
        yield from self.proximity_damage.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0xaed23abc(self, asset_manager):
        yield from self.audio_playback_parms_0xaed23abc.dependencies_for(asset_manager)

    def _dependencies_for_sound_spiderball_rolling(self, asset_manager):
        yield from self.sound_spiderball_rolling.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0xcee38f10(self, asset_manager):
        yield from self.audio_playback_parms_0xcee38f10.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x796fa303(self, asset_manager):
        yield from self.audio_playback_parms_0x796fa303.dependencies_for(asset_manager)

    def _dependencies_for_sound_enter_stunned(self, asset_manager):
        yield from self.sound_enter_stunned.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0x44c1f241(self, asset_manager):
        yield from self.audio_playback_parms_0x44c1f241.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_ing_spiderball_guardian_struct_0x152db484, "ing_spiderball_guardian_struct_0x152db484", "IngSpiderballGuardianStruct"),
            (self._dependencies_for_ing_spiderball_guardian_struct_0x2d163ff7, "ing_spiderball_guardian_struct_0x2d163ff7", "IngSpiderballGuardianStruct"),
            (self._dependencies_for_ing_spiderball_guardian_struct_0x8c2fbb19, "ing_spiderball_guardian_struct_0x8c2fbb19", "IngSpiderballGuardianStruct"),
            (self._dependencies_for_ing_spiderball_guardian_struct_0x5d612911, "ing_spiderball_guardian_struct_0x5d612911", "IngSpiderballGuardianStruct"),
            (self._dependencies_for_ing_spiderball_guardian_struct_0xfc58adff, "ing_spiderball_guardian_struct_0xfc58adff", "IngSpiderballGuardianStruct"),
            (self._dependencies_for_ing_spiderball_guardian_struct_0xc463268c, "ing_spiderball_guardian_struct_0xc463268c", "IngSpiderballGuardianStruct"),
            (self._dependencies_for_proximity_damage, "proximity_damage", "DamageInfo"),
            (self._dependencies_for_audio_playback_parms_0xaed23abc, "audio_playback_parms_0xaed23abc", "AudioPlaybackParms"),
            (self._dependencies_for_sound_spiderball_rolling, "sound_spiderball_rolling", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0xcee38f10, "audio_playback_parms_0xcee38f10", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x796fa303, "audio_playback_parms_0x796fa303", "AudioPlaybackParms"),
            (self._dependencies_for_sound_enter_stunned, "sound_enter_stunned", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms_0x44c1f241, "audio_playback_parms_0x44c1f241", "AudioPlaybackParms"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct31.{field_name} ({field_type}): {e}"
                )


def _decode_ing_spiderball_guardian_struct_0x152db484(data: typing.BinaryIO, property_size: int):
    return IngSpiderballGuardianStruct.from_stream(data, property_size)


def _decode_ing_spiderball_guardian_struct_0x2d163ff7(data: typing.BinaryIO, property_size: int):
    return IngSpiderballGuardianStruct.from_stream(data, property_size)


def _decode_ing_spiderball_guardian_struct_0x8c2fbb19(data: typing.BinaryIO, property_size: int):
    return IngSpiderballGuardianStruct.from_stream(data, property_size)


def _decode_ing_spiderball_guardian_struct_0x5d612911(data: typing.BinaryIO, property_size: int):
    return IngSpiderballGuardianStruct.from_stream(data, property_size)


def _decode_ing_spiderball_guardian_struct_0xfc58adff(data: typing.BinaryIO, property_size: int):
    return IngSpiderballGuardianStruct.from_stream(data, property_size)


def _decode_ing_spiderball_guardian_struct_0xc463268c(data: typing.BinaryIO, property_size: int):
    return IngSpiderballGuardianStruct.from_stream(data, property_size)


def _decode_damage_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_proximity_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 40.0, 'di_knock_back_power': 10.0})


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_playback_parms_0xaed23abc(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_spiderball_rolling(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0xcee38f10(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x796fa303(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_enter_stunned(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms_0x44c1f241(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x152db484: ('ing_spiderball_guardian_struct_0x152db484', _decode_ing_spiderball_guardian_struct_0x152db484),
    0x2d163ff7: ('ing_spiderball_guardian_struct_0x2d163ff7', _decode_ing_spiderball_guardian_struct_0x2d163ff7),
    0x8c2fbb19: ('ing_spiderball_guardian_struct_0x8c2fbb19', _decode_ing_spiderball_guardian_struct_0x8c2fbb19),
    0x5d612911: ('ing_spiderball_guardian_struct_0x5d612911', _decode_ing_spiderball_guardian_struct_0x5d612911),
    0xfc58adff: ('ing_spiderball_guardian_struct_0xfc58adff', _decode_ing_spiderball_guardian_struct_0xfc58adff),
    0xc463268c: ('ing_spiderball_guardian_struct_0xc463268c', _decode_ing_spiderball_guardian_struct_0xc463268c),
    0xf598739: ('damage_radius', _decode_damage_radius),
    0xba78d281: ('proximity_damage', _decode_proximity_damage),
    0x32133b39: ('unknown', _decode_unknown),
    0xaed23abc: ('audio_playback_parms_0xaed23abc', _decode_audio_playback_parms_0xaed23abc),
    0x3a5e2f52: ('sound_spiderball_rolling', _decode_sound_spiderball_rolling),
    0xcee38f10: ('audio_playback_parms_0xcee38f10', _decode_audio_playback_parms_0xcee38f10),
    0x796fa303: ('audio_playback_parms_0x796fa303', _decode_audio_playback_parms_0x796fa303),
    0xd5f3e9c4: ('sound_enter_stunned', _decode_sound_enter_stunned),
    0x44c1f241: ('audio_playback_parms_0x44c1f241', _decode_audio_playback_parms_0x44c1f241),
}
