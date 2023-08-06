# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.SurroundPan import SurroundPan
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Sound(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    sound_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    min_audible_distance: float = dataclasses.field(default=0.0)
    max_audible_distance: float = dataclasses.field(default=0.0)
    delay_time: float = dataclasses.field(default=0.0)
    volume: float = dataclasses.field(default=1.0)
    volume_variance: float = dataclasses.field(default=0.0)
    surround_pan: SurroundPan = dataclasses.field(default_factory=SurroundPan)
    pan_variance: float = dataclasses.field(default=0.0)
    pitch: float = dataclasses.field(default=0.0)
    ambient: bool = dataclasses.field(default=False)
    auto_start: bool = dataclasses.field(default=False)
    can_occlude: bool = dataclasses.field(default=False)
    play_always: bool = dataclasses.field(default=False)
    sound_is_music: bool = dataclasses.field(default=False)
    update_velocity: bool = dataclasses.field(default=False)
    ignore_generated_behavior: bool = dataclasses.field(default=False)
    sound_is_ui_sound: bool = dataclasses.field(default=False)
    sound_is_speech: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SOND'

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
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\x1a1v')  # 0x771a3176
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_effect))

        data.write(b'%\xd4y\x8a')  # 0x25d4798a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_audible_distance))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'\x8e\x16\xe0\x12')  # 0x8e16e012
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_time))

        data.write(b'\xc7\xa7\xf1\x89')  # 0xc7a7f189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume))

        data.write(b'\xf0\xe4KV')  # 0xf0e44b56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume_variance))

        data.write(b'\x0b\xb6&9')  # 0xbb62639
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surround_pan.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95#rX')  # 0x95237258
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pan_variance))

        data.write(b',\xc5\xcb\x93')  # 0x2cc5cb93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pitch))

        data.write(b'\x89q\xb7\xa7')  # 0x8971b7a7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ambient))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'\x94r\x11c')  # 0x94721163
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_occlude))

        data.write(b'\r\x7f\x8c\x7f')  # 0xd7f8c7f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.play_always))

        data.write(b'v\xd4\x00\x91')  # 0x76d40091
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sound_is_music))

        data.write(b'\x90\x14\\\xd2')  # 0x90145cd2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.update_velocity))

        data.write(b'\xeb\xd1\x92s')  # 0xebd19273
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_generated_behavior))

        data.write(b'\x18oe\x92')  # 0x186f6592
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sound_is_ui_sound))

        data.write(b'^\to\xd2')  # 0x5e096fd2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sound_is_speech))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            sound_effect=data['sound_effect'],
            min_audible_distance=data['min_audible_distance'],
            max_audible_distance=data['max_audible_distance'],
            delay_time=data['delay_time'],
            volume=data['volume'],
            volume_variance=data['volume_variance'],
            surround_pan=SurroundPan.from_json(data['surround_pan']),
            pan_variance=data['pan_variance'],
            pitch=data['pitch'],
            ambient=data['ambient'],
            auto_start=data['auto_start'],
            can_occlude=data['can_occlude'],
            play_always=data['play_always'],
            sound_is_music=data['sound_is_music'],
            update_velocity=data['update_velocity'],
            ignore_generated_behavior=data['ignore_generated_behavior'],
            sound_is_ui_sound=data['sound_is_ui_sound'],
            sound_is_speech=data['sound_is_speech'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'sound_effect': self.sound_effect,
            'min_audible_distance': self.min_audible_distance,
            'max_audible_distance': self.max_audible_distance,
            'delay_time': self.delay_time,
            'volume': self.volume,
            'volume_variance': self.volume_variance,
            'surround_pan': self.surround_pan.to_json(),
            'pan_variance': self.pan_variance,
            'pitch': self.pitch,
            'ambient': self.ambient,
            'auto_start': self.auto_start,
            'can_occlude': self.can_occlude,
            'play_always': self.play_always,
            'sound_is_music': self.sound_is_music,
            'update_velocity': self.update_velocity,
            'ignore_generated_behavior': self.ignore_generated_behavior,
            'sound_is_ui_sound': self.sound_is_ui_sound,
            'sound_is_speech': self.sound_is_speech,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_min_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_surround_pan(data: typing.BinaryIO, property_size: int):
    return SurroundPan.from_stream(data, property_size)


def _decode_pan_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ambient(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_occlude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_play_always(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sound_is_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_update_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_generated_behavior(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sound_is_ui_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sound_is_speech(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x771a3176: ('sound_effect', _decode_sound_effect),
    0x25d4798a: ('min_audible_distance', _decode_min_audible_distance),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x8e16e012: ('delay_time', _decode_delay_time),
    0xc7a7f189: ('volume', _decode_volume),
    0xf0e44b56: ('volume_variance', _decode_volume_variance),
    0xbb62639: ('surround_pan', _decode_surround_pan),
    0x95237258: ('pan_variance', _decode_pan_variance),
    0x2cc5cb93: ('pitch', _decode_pitch),
    0x8971b7a7: ('ambient', _decode_ambient),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x94721163: ('can_occlude', _decode_can_occlude),
    0xd7f8c7f: ('play_always', _decode_play_always),
    0x76d40091: ('sound_is_music', _decode_sound_is_music),
    0x90145cd2: ('update_velocity', _decode_update_velocity),
    0xebd19273: ('ignore_generated_behavior', _decode_ignore_generated_behavior),
    0x186f6592: ('sound_is_ui_sound', _decode_sound_is_ui_sound),
    0x5e096fd2: ('sound_is_speech', _decode_sound_is_speech),
}
