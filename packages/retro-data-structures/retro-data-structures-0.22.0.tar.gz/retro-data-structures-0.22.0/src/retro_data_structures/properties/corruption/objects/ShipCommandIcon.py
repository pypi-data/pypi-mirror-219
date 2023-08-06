# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShipCommandIcon(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0x11234a3f: bool = dataclasses.field(default=False)
    unknown_0x4b198e71: bool = dataclasses.field(default=False)
    scannable: bool = dataclasses.field(default=True)
    function: int = dataclasses.field(default=0)
    disabled_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    category_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    specific_function_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    disabled_animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    category_animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    function_animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    necessary_upgrade: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    unknown_0x48ef8ade: int = dataclasses.field(default=4050431932)  # Choice
    unknown_0x69a7e62c: float = dataclasses.field(default=1.5)
    scan_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    executing_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    missile_empty: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SHCI'

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x11#J?')  # 0x11234a3f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x11234a3f))

        data.write(b'K\x19\x8eq')  # 0x4b198e71
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4b198e71))

        data.write(b'\x8b\x9bXL')  # 0x8b9b584c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scannable))

        data.write(b'\x95\xf8\xd6D')  # 0x95f8d644
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.function))

        data.write(b'\xc3\x9f\x896')  # 0xc39f8936
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disabled_texture))

        data.write(b'",\xf8\xec')  # 0x222cf8ec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.category_texture))

        data.write(b'\x0b\xf0\x0e\xb1')  # 0xbf00eb1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.specific_function_texture))

        data.write(b'm\x10\xc9\x87')  # 0x6d10c987
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.disabled_animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\xad\xb1\x94')  # 0x97adb194
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.category_animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x97g\x9c')  # 0xa797679c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.function_animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08\x07-\xa5')  # 0x8072da5
        data.write(b'\x00\x04')  # size
        self.necessary_upgrade.to_stream(data)

        data.write(b'H\xef\x8a\xde')  # 0x48ef8ade
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x48ef8ade))

        data.write(b'i\xa7\xe6,')  # 0x69a7e62c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x69a7e62c))

        data.write(b'\xcejx\xc8')  # 0xce6a78c8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scan_sound))

        data.write(b'QT`\xac')  # 0x515460ac
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.executing_sound))

        data.write(b'\x10(\x98\x04')  # 0x10289804
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.missile_empty))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_0x11234a3f=data['unknown_0x11234a3f'],
            unknown_0x4b198e71=data['unknown_0x4b198e71'],
            scannable=data['scannable'],
            function=data['function'],
            disabled_texture=data['disabled_texture'],
            category_texture=data['category_texture'],
            specific_function_texture=data['specific_function_texture'],
            disabled_animation=AnimationParameters.from_json(data['disabled_animation']),
            category_animation=AnimationParameters.from_json(data['category_animation']),
            function_animation=AnimationParameters.from_json(data['function_animation']),
            necessary_upgrade=enums.PlayerItem.from_json(data['necessary_upgrade']),
            unknown_0x48ef8ade=data['unknown_0x48ef8ade'],
            unknown_0x69a7e62c=data['unknown_0x69a7e62c'],
            scan_sound=data['scan_sound'],
            executing_sound=data['executing_sound'],
            missile_empty=data['missile_empty'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0x11234a3f': self.unknown_0x11234a3f,
            'unknown_0x4b198e71': self.unknown_0x4b198e71,
            'scannable': self.scannable,
            'function': self.function,
            'disabled_texture': self.disabled_texture,
            'category_texture': self.category_texture,
            'specific_function_texture': self.specific_function_texture,
            'disabled_animation': self.disabled_animation.to_json(),
            'category_animation': self.category_animation.to_json(),
            'function_animation': self.function_animation.to_json(),
            'necessary_upgrade': self.necessary_upgrade.to_json(),
            'unknown_0x48ef8ade': self.unknown_0x48ef8ade,
            'unknown_0x69a7e62c': self.unknown_0x69a7e62c,
            'scan_sound': self.scan_sound,
            'executing_sound': self.executing_sound,
            'missile_empty': self.missile_empty,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0x11234a3f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4b198e71(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scannable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_function(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_disabled_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_category_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_specific_function_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disabled_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_category_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_function_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_necessary_upgrade(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_unknown_0x48ef8ade(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x69a7e62c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_executing_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_missile_empty(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x11234a3f: ('unknown_0x11234a3f', _decode_unknown_0x11234a3f),
    0x4b198e71: ('unknown_0x4b198e71', _decode_unknown_0x4b198e71),
    0x8b9b584c: ('scannable', _decode_scannable),
    0x95f8d644: ('function', _decode_function),
    0xc39f8936: ('disabled_texture', _decode_disabled_texture),
    0x222cf8ec: ('category_texture', _decode_category_texture),
    0xbf00eb1: ('specific_function_texture', _decode_specific_function_texture),
    0x6d10c987: ('disabled_animation', _decode_disabled_animation),
    0x97adb194: ('category_animation', _decode_category_animation),
    0xa797679c: ('function_animation', _decode_function_animation),
    0x8072da5: ('necessary_upgrade', _decode_necessary_upgrade),
    0x48ef8ade: ('unknown_0x48ef8ade', _decode_unknown_0x48ef8ade),
    0x69a7e62c: ('unknown_0x69a7e62c', _decode_unknown_0x69a7e62c),
    0xce6a78c8: ('scan_sound', _decode_scan_sound),
    0x515460ac: ('executing_sound', _decode_executing_sound),
    0x10289804: ('missile_empty', _decode_missile_empty),
}
