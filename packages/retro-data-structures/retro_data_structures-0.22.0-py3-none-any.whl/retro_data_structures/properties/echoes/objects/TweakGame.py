# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TweakGame.CoinLimitChoices import CoinLimitChoices
from retro_data_structures.properties.echoes.archetypes.TweakGame.FragLimitChoices import FragLimitChoices
from retro_data_structures.properties.echoes.archetypes.TweakGame.TimeLimitChoices import TimeLimitChoices
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class TweakGame(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    pak_file: str = dataclasses.field(default='')
    asset: str = dataclasses.field(default='')
    fieldof_view: float = dataclasses.field(default=55.0)
    fieldof_view2_player: float = dataclasses.field(default=45.0)
    disable_debug_menu: bool = dataclasses.field(default=False)
    unknown_0x7262d27b: bool = dataclasses.field(default=True)
    development_mode: bool = dataclasses.field(default=True)
    unknown_0xa3dcf42a: float = dataclasses.field(default=25.0)
    unknown_0xb35c72be: float = dataclasses.field(default=1.0)
    unknown_0x4a02103c: float = dataclasses.field(default=30.0)
    unknown_0xe1fca71b: float = dataclasses.field(default=125.0)
    unknown_0xfbce966a: float = dataclasses.field(default=150.0)
    unknown_0x09c6ca10: float = dataclasses.field(default=300.0)
    hard_mode_damage_multiplier: float = dataclasses.field(default=1.5299999713897705)
    hard_mode_weapon_multiplier: float = dataclasses.field(default=0.5)
    unknown_0x5ab5812c: float = dataclasses.field(default=0.15000000596046448)
    unknown_0x53401390: float = dataclasses.field(default=0.15000000596046448)
    total_percentage: int = dataclasses.field(default=102)
    unknown_0x1d627808: FragLimitChoices = dataclasses.field(default_factory=FragLimitChoices)
    unknown_0xb2e8828d: TimeLimitChoices = dataclasses.field(default_factory=TimeLimitChoices)
    unknown_0x06af87bd: CoinLimitChoices = dataclasses.field(default_factory=CoinLimitChoices)
    unknown_0x1533ea4e: TimeLimitChoices = dataclasses.field(default_factory=TimeLimitChoices)
    unknown_0x40818220: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWGM'

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
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+\xd1:\xb3')  # 0x2bd13ab3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.pak_file.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xbe\x00Z')  # 0xf8be005a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.asset.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\x93\xce\xb8')  # 0xfc93ceb8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fieldof_view))

        data.write(b'\x9f\xb2\xfa\xa6')  # 0x9fb2faa6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fieldof_view2_player))

        data.write(b'\xa9\ti\x14')  # 0xa9096914
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_debug_menu))

        data.write(b'rb\xd2{')  # 0x7262d27b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7262d27b))

        data.write(b'\xe9C\xba\x12')  # 0xe943ba12
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.development_mode))

        data.write(b'\xa3\xdc\xf4*')  # 0xa3dcf42a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa3dcf42a))

        data.write(b'\xb3\\r\xbe')  # 0xb35c72be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb35c72be))

        data.write(b'J\x02\x10<')  # 0x4a02103c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4a02103c))

        data.write(b'\xe1\xfc\xa7\x1b')  # 0xe1fca71b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe1fca71b))

        data.write(b'\xfb\xce\x96j')  # 0xfbce966a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfbce966a))

        data.write(b'\t\xc6\xca\x10')  # 0x9c6ca10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x09c6ca10))

        data.write(b'M\xfc\xd42')  # 0x4dfcd432
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hard_mode_damage_multiplier))

        data.write(b'\xae\x181\xd9')  # 0xae1831d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hard_mode_weapon_multiplier))

        data.write(b'Z\xb5\x81,')  # 0x5ab5812c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5ab5812c))

        data.write(b'S@\x13\x90')  # 0x53401390
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x53401390))

        data.write(b'\xd0\x9f7;')  # 0xd09f373b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.total_percentage))

        data.write(b'\x1dbx\x08')  # 0x1d627808
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1d627808.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\xe8\x82\x8d')  # 0xb2e8828d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb2e8828d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06\xaf\x87\xbd')  # 0x6af87bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x06af87bd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x153\xeaN')  # 0x1533ea4e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1533ea4e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@\x81\x82 ')  # 0x40818220
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x40818220.to_stream(data)
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
            instance_name=data['instance_name'],
            pak_file=data['pak_file'],
            asset=data['asset'],
            fieldof_view=data['fieldof_view'],
            fieldof_view2_player=data['fieldof_view2_player'],
            disable_debug_menu=data['disable_debug_menu'],
            unknown_0x7262d27b=data['unknown_0x7262d27b'],
            development_mode=data['development_mode'],
            unknown_0xa3dcf42a=data['unknown_0xa3dcf42a'],
            unknown_0xb35c72be=data['unknown_0xb35c72be'],
            unknown_0x4a02103c=data['unknown_0x4a02103c'],
            unknown_0xe1fca71b=data['unknown_0xe1fca71b'],
            unknown_0xfbce966a=data['unknown_0xfbce966a'],
            unknown_0x09c6ca10=data['unknown_0x09c6ca10'],
            hard_mode_damage_multiplier=data['hard_mode_damage_multiplier'],
            hard_mode_weapon_multiplier=data['hard_mode_weapon_multiplier'],
            unknown_0x5ab5812c=data['unknown_0x5ab5812c'],
            unknown_0x53401390=data['unknown_0x53401390'],
            total_percentage=data['total_percentage'],
            unknown_0x1d627808=FragLimitChoices.from_json(data['unknown_0x1d627808']),
            unknown_0xb2e8828d=TimeLimitChoices.from_json(data['unknown_0xb2e8828d']),
            unknown_0x06af87bd=CoinLimitChoices.from_json(data['unknown_0x06af87bd']),
            unknown_0x1533ea4e=TimeLimitChoices.from_json(data['unknown_0x1533ea4e']),
            unknown_0x40818220=Spline.from_json(data['unknown_0x40818220']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'pak_file': self.pak_file,
            'asset': self.asset,
            'fieldof_view': self.fieldof_view,
            'fieldof_view2_player': self.fieldof_view2_player,
            'disable_debug_menu': self.disable_debug_menu,
            'unknown_0x7262d27b': self.unknown_0x7262d27b,
            'development_mode': self.development_mode,
            'unknown_0xa3dcf42a': self.unknown_0xa3dcf42a,
            'unknown_0xb35c72be': self.unknown_0xb35c72be,
            'unknown_0x4a02103c': self.unknown_0x4a02103c,
            'unknown_0xe1fca71b': self.unknown_0xe1fca71b,
            'unknown_0xfbce966a': self.unknown_0xfbce966a,
            'unknown_0x09c6ca10': self.unknown_0x09c6ca10,
            'hard_mode_damage_multiplier': self.hard_mode_damage_multiplier,
            'hard_mode_weapon_multiplier': self.hard_mode_weapon_multiplier,
            'unknown_0x5ab5812c': self.unknown_0x5ab5812c,
            'unknown_0x53401390': self.unknown_0x53401390,
            'total_percentage': self.total_percentage,
            'unknown_0x1d627808': self.unknown_0x1d627808.to_json(),
            'unknown_0xb2e8828d': self.unknown_0xb2e8828d.to_json(),
            'unknown_0x06af87bd': self.unknown_0x06af87bd.to_json(),
            'unknown_0x1533ea4e': self.unknown_0x1533ea4e.to_json(),
            'unknown_0x40818220': self.unknown_0x40818220.to_json(),
        }

    def _dependencies_for_unknown_0x1d627808(self, asset_manager):
        yield from self.unknown_0x1d627808.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0xb2e8828d(self, asset_manager):
        yield from self.unknown_0xb2e8828d.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x06af87bd(self, asset_manager):
        yield from self.unknown_0x06af87bd.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x1533ea4e(self, asset_manager):
        yield from self.unknown_0x1533ea4e.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unknown_0x1d627808, "unknown_0x1d627808", "FragLimitChoices"),
            (self._dependencies_for_unknown_0xb2e8828d, "unknown_0xb2e8828d", "TimeLimitChoices"),
            (self._dependencies_for_unknown_0x06af87bd, "unknown_0x06af87bd", "CoinLimitChoices"),
            (self._dependencies_for_unknown_0x1533ea4e, "unknown_0x1533ea4e", "TimeLimitChoices"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakGame.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_pak_file(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_asset(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_fieldof_view(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fieldof_view2_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_debug_menu(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7262d27b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_development_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa3dcf42a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb35c72be(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4a02103c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe1fca71b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfbce966a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x09c6ca10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hard_mode_damage_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hard_mode_weapon_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5ab5812c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x53401390(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_total_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1d627808(data: typing.BinaryIO, property_size: int):
    return FragLimitChoices.from_stream(data, property_size)


def _decode_unknown_0xb2e8828d(data: typing.BinaryIO, property_size: int):
    return TimeLimitChoices.from_stream(data, property_size)


def _decode_unknown_0x06af87bd(data: typing.BinaryIO, property_size: int):
    return CoinLimitChoices.from_stream(data, property_size)


def _decode_unknown_0x1533ea4e(data: typing.BinaryIO, property_size: int):
    return TimeLimitChoices.from_stream(data, property_size)


def _decode_unknown_0x40818220(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0x2bd13ab3: ('pak_file', _decode_pak_file),
    0xf8be005a: ('asset', _decode_asset),
    0xfc93ceb8: ('fieldof_view', _decode_fieldof_view),
    0x9fb2faa6: ('fieldof_view2_player', _decode_fieldof_view2_player),
    0xa9096914: ('disable_debug_menu', _decode_disable_debug_menu),
    0x7262d27b: ('unknown_0x7262d27b', _decode_unknown_0x7262d27b),
    0xe943ba12: ('development_mode', _decode_development_mode),
    0xa3dcf42a: ('unknown_0xa3dcf42a', _decode_unknown_0xa3dcf42a),
    0xb35c72be: ('unknown_0xb35c72be', _decode_unknown_0xb35c72be),
    0x4a02103c: ('unknown_0x4a02103c', _decode_unknown_0x4a02103c),
    0xe1fca71b: ('unknown_0xe1fca71b', _decode_unknown_0xe1fca71b),
    0xfbce966a: ('unknown_0xfbce966a', _decode_unknown_0xfbce966a),
    0x9c6ca10: ('unknown_0x09c6ca10', _decode_unknown_0x09c6ca10),
    0x4dfcd432: ('hard_mode_damage_multiplier', _decode_hard_mode_damage_multiplier),
    0xae1831d9: ('hard_mode_weapon_multiplier', _decode_hard_mode_weapon_multiplier),
    0x5ab5812c: ('unknown_0x5ab5812c', _decode_unknown_0x5ab5812c),
    0x53401390: ('unknown_0x53401390', _decode_unknown_0x53401390),
    0xd09f373b: ('total_percentage', _decode_total_percentage),
    0x1d627808: ('unknown_0x1d627808', _decode_unknown_0x1d627808),
    0xb2e8828d: ('unknown_0xb2e8828d', _decode_unknown_0xb2e8828d),
    0x6af87bd: ('unknown_0x06af87bd', _decode_unknown_0x06af87bd),
    0x1533ea4e: ('unknown_0x1533ea4e', _decode_unknown_0x1533ea4e),
    0x40818220: ('unknown_0x40818220', _decode_unknown_0x40818220),
}
