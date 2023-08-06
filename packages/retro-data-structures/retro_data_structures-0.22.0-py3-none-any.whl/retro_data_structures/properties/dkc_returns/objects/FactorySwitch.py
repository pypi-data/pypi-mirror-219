# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.RotationSplines import RotationSplines
from retro_data_structures.properties.dkc_returns.archetypes.TranslationSplines import TranslationSplines
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class FactorySwitch(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    case_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    indicator_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    switch_state: bool = dataclasses.field(default=False)
    switch_delay: float = dataclasses.field(default=0.6000000238418579)
    rotation_controls: RotationSplines = dataclasses.field(default_factory=RotationSplines)
    translation_control: TranslationSplines = dataclasses.field(default_factory=TranslationSplines)
    toggle_sound: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    reset_sound: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x25c9c68f: bool = dataclasses.field(default=False)
    unknown_0x10e79562: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x7357fbac: bool = dataclasses.field(default=False)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FSWC'

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\xa4S\xb1')  # 0x6ca453b1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.case_model))

        data.write(b'\xb6\xd3L\xbe')  # 0xb6d34cbe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.indicator_model))

        data.write(b'f\xe6N\xba')  # 0x66e64eba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.switch_state))

        data.write(b'\x8a\x1f\xd6a')  # 0x8a1fd661
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.switch_delay))

        data.write(b'\xef\xe4\xeaW')  # 0xefe4ea57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotation_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i"g\xea')  # 0x692267ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.translation_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xf9oT')  # 0x36f96f54
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.toggle_sound))

        data.write(b'FQY\xa3')  # 0x465159a3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reset_sound))

        data.write(b'%\xc9\xc6\x8f')  # 0x25c9c68f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x25c9c68f))

        data.write(b'\x10\xe7\x95b')  # 0x10e79562
        data.write(b'\x00\x0c')  # size
        self.unknown_0x10e79562.to_stream(data)

        data.write(b'sW\xfb\xac')  # 0x7357fbac
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7357fbac))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            case_model=data['case_model'],
            indicator_model=data['indicator_model'],
            switch_state=data['switch_state'],
            switch_delay=data['switch_delay'],
            rotation_controls=RotationSplines.from_json(data['rotation_controls']),
            translation_control=TranslationSplines.from_json(data['translation_control']),
            toggle_sound=data['toggle_sound'],
            reset_sound=data['reset_sound'],
            unknown_0x25c9c68f=data['unknown_0x25c9c68f'],
            unknown_0x10e79562=Vector.from_json(data['unknown_0x10e79562']),
            unknown_0x7357fbac=data['unknown_0x7357fbac'],
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'case_model': self.case_model,
            'indicator_model': self.indicator_model,
            'switch_state': self.switch_state,
            'switch_delay': self.switch_delay,
            'rotation_controls': self.rotation_controls.to_json(),
            'translation_control': self.translation_control.to_json(),
            'toggle_sound': self.toggle_sound,
            'reset_sound': self.reset_sound,
            'unknown_0x25c9c68f': self.unknown_0x25c9c68f,
            'unknown_0x10e79562': self.unknown_0x10e79562.to_json(),
            'unknown_0x7357fbac': self.unknown_0x7357fbac,
            'actor_information': self.actor_information.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_case_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_indicator_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_switch_state(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_switch_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_controls(data: typing.BinaryIO, property_size: int):
    return RotationSplines.from_stream(data, property_size)


def _decode_translation_control(data: typing.BinaryIO, property_size: int):
    return TranslationSplines.from_stream(data, property_size)


def _decode_toggle_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reset_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x25c9c68f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x10e79562(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x7357fbac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x6ca453b1: ('case_model', _decode_case_model),
    0xb6d34cbe: ('indicator_model', _decode_indicator_model),
    0x66e64eba: ('switch_state', _decode_switch_state),
    0x8a1fd661: ('switch_delay', _decode_switch_delay),
    0xefe4ea57: ('rotation_controls', _decode_rotation_controls),
    0x692267ea: ('translation_control', _decode_translation_control),
    0x36f96f54: ('toggle_sound', _decode_toggle_sound),
    0x465159a3: ('reset_sound', _decode_reset_sound),
    0x25c9c68f: ('unknown_0x25c9c68f', _decode_unknown_0x25c9c68f),
    0x10e79562: ('unknown_0x10e79562', _decode_unknown_0x10e79562),
    0x7357fbac: ('unknown_0x7357fbac', _decode_unknown_0x7357fbac),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
