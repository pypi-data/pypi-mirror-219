# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class EffectRepulsor(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    item: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    zap_time: float = dataclasses.field(default=0.10000000149011612)
    retrigger_time: float = dataclasses.field(default=0.10000000149011612)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'EFTR'

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1i\xd4$')  # 0xa169d424
        data.write(b'\x00\x04')  # size
        self.item.to_stream(data)

        data.write(b'\xb6\x8cm\x96')  # 0xb68c6d96
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.effect))

        data.write(b'h\xb0\xf63')  # 0x68b0f633
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.zap_time))

        data.write(b'\xa8\xe3\xaf\xf1')  # 0xa8e3aff1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.retrigger_time))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data, default_override={'di_knock_back_power': 1.0})
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
            item=enums.PlayerItem.from_json(data['item']),
            effect=data['effect'],
            zap_time=data['zap_time'],
            retrigger_time=data['retrigger_time'],
            damage=DamageInfo.from_json(data['damage']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'item': self.item.to_json(),
            'effect': self.effect,
            'zap_time': self.zap_time,
            'retrigger_time': self.retrigger_time,
            'damage': self.damage.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_item(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_zap_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_retrigger_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_knock_back_power': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa169d424: ('item', _decode_item),
    0xb68c6d96: ('effect', _decode_effect),
    0x68b0f633: ('zap_time', _decode_zap_time),
    0xa8e3aff1: ('retrigger_time', _decode_retrigger_time),
    0x337f9524: ('damage', _decode_damage),
}
