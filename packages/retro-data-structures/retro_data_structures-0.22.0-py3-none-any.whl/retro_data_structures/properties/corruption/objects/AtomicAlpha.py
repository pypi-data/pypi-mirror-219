# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class AtomicAlpha(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    bomb_weapon: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    bomb_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    bomb_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    bomb_drop_delay: float = dataclasses.field(default=3.0)
    bomb_reappear_delay: float = dataclasses.field(default=2.0)
    bomb_reappear_time: float = dataclasses.field(default=1.5)
    invisible: bool = dataclasses.field(default=False)
    home_while_charging: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ATMA'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_AtomicAlpha.rso']

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
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

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17 \xb9\x1f')  # 0x1720b91f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bomb_weapon))

        data.write(b'\xc7_\x95\x16')  # 0xc75f9516
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bomb_model))

        data.write(b'\xb4\x8d_\xe6')  # 0xb48d5fe6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bomb_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f\xba\x00\x9c')  # 0x66ba009c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_drop_delay))

        data.write(b'y\xddf\xa9')  # 0x79dd66a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_reappear_delay))

        data.write(b'\xbbB\x84\xea')  # 0xbb4284ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_reappear_time))

        data.write(b'p\x17\xed\xfc')  # 0x7017edfc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.invisible))

        data.write(b'&9\xf0\xb9')  # 0x2639f0b9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.home_while_charging))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            bomb_weapon=data['bomb_weapon'],
            bomb_model=data['bomb_model'],
            bomb_damage=DamageInfo.from_json(data['bomb_damage']),
            bomb_drop_delay=data['bomb_drop_delay'],
            bomb_reappear_delay=data['bomb_reappear_delay'],
            bomb_reappear_time=data['bomb_reappear_time'],
            invisible=data['invisible'],
            home_while_charging=data['home_while_charging'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'patterned': self.patterned.to_json(),
            'bomb_weapon': self.bomb_weapon,
            'bomb_model': self.bomb_model,
            'bomb_damage': self.bomb_damage.to_json(),
            'bomb_drop_delay': self.bomb_drop_delay,
            'bomb_reappear_delay': self.bomb_reappear_delay,
            'bomb_reappear_time': self.bomb_reappear_time,
            'invisible': self.invisible,
            'home_while_charging': self.home_while_charging,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_bomb_weapon(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bomb_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bomb_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_bomb_drop_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_reappear_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_reappear_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_invisible(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_home_while_charging(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xb3774750: ('patterned', _decode_patterned),
    0x1720b91f: ('bomb_weapon', _decode_bomb_weapon),
    0xc75f9516: ('bomb_model', _decode_bomb_model),
    0xb48d5fe6: ('bomb_damage', _decode_bomb_damage),
    0x66ba009c: ('bomb_drop_delay', _decode_bomb_drop_delay),
    0x79dd66a9: ('bomb_reappear_delay', _decode_bomb_reappear_delay),
    0xbb4284ea: ('bomb_reappear_time', _decode_bomb_reappear_time),
    0x7017edfc: ('invisible', _decode_invisible),
    0x2639f0b9: ('home_while_charging', _decode_home_while_charging),
}
