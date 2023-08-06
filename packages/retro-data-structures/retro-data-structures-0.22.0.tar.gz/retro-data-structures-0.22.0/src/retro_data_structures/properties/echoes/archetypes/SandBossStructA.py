# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SandBossStructA(BaseProperty):
    head_armor: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_piece2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_piece3: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_piece4: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_piece5: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_piece6: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_piece7: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    tail_armor: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    sound_armor_impact: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        data.write(b'\x07\xd8\xccO')  # 0x7d8cc4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.head_armor))

        data.write(b'\xae0\xae\x06')  # 0xae30ae06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.armor_piece2))

        data.write(b'el}\xa3')  # 0x656c7da3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.armor_piece3))

        data.write(b'xiM\x1b')  # 0x78694d1b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.armor_piece4))

        data.write(b'\xb35\x9e\xbe')  # 0xb3359ebe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.armor_piece5))

        data.write(b'5\xa1\xec\x10')  # 0x35a1ec10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.armor_piece6))

        data.write(b'\xfe\xfd?\xb5')  # 0xfefd3fb5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.armor_piece7))

        data.write(b'7\xe9\x9c#')  # 0x37e99c23
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.tail_armor))

        data.write(b'\xdc\xc2\xbf\x11')  # 0xdcc2bf11
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound_armor_impact))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            head_armor=data['head_armor'],
            armor_piece2=data['armor_piece2'],
            armor_piece3=data['armor_piece3'],
            armor_piece4=data['armor_piece4'],
            armor_piece5=data['armor_piece5'],
            armor_piece6=data['armor_piece6'],
            armor_piece7=data['armor_piece7'],
            tail_armor=data['tail_armor'],
            sound_armor_impact=data['sound_armor_impact'],
        )

    def to_json(self) -> dict:
        return {
            'head_armor': self.head_armor,
            'armor_piece2': self.armor_piece2,
            'armor_piece3': self.armor_piece3,
            'armor_piece4': self.armor_piece4,
            'armor_piece5': self.armor_piece5,
            'armor_piece6': self.armor_piece6,
            'armor_piece7': self.armor_piece7,
            'tail_armor': self.tail_armor,
            'sound_armor_impact': self.sound_armor_impact,
        }

    def _dependencies_for_head_armor(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.head_armor)

    def _dependencies_for_armor_piece2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.armor_piece2)

    def _dependencies_for_armor_piece3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.armor_piece3)

    def _dependencies_for_armor_piece4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.armor_piece4)

    def _dependencies_for_armor_piece5(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.armor_piece5)

    def _dependencies_for_armor_piece6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.armor_piece6)

    def _dependencies_for_armor_piece7(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.armor_piece7)

    def _dependencies_for_tail_armor(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.tail_armor)

    def _dependencies_for_sound_armor_impact(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.sound_armor_impact)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_head_armor, "head_armor", "AssetId"),
            (self._dependencies_for_armor_piece2, "armor_piece2", "AssetId"),
            (self._dependencies_for_armor_piece3, "armor_piece3", "AssetId"),
            (self._dependencies_for_armor_piece4, "armor_piece4", "AssetId"),
            (self._dependencies_for_armor_piece5, "armor_piece5", "AssetId"),
            (self._dependencies_for_armor_piece6, "armor_piece6", "AssetId"),
            (self._dependencies_for_armor_piece7, "armor_piece7", "AssetId"),
            (self._dependencies_for_tail_armor, "tail_armor", "AssetId"),
            (self._dependencies_for_sound_armor_impact, "sound_armor_impact", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SandBossStructA.{field_name} ({field_type}): {e}"
                )


_FAST_FORMAT = None
_FAST_IDS = (0x7d8cc4f, 0xae30ae06, 0x656c7da3, 0x78694d1b, 0xb3359ebe, 0x35a1ec10, 0xfefd3fb5, 0x37e99c23, 0xdcc2bf11)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SandBossStructA]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHLLHLLHLLHLLHLLHLLHLLHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(90))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return SandBossStructA(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_head_armor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_armor_piece2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_armor_piece3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_armor_piece4(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_armor_piece5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_armor_piece6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_armor_piece7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_tail_armor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_armor_impact(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7d8cc4f: ('head_armor', _decode_head_armor),
    0xae30ae06: ('armor_piece2', _decode_armor_piece2),
    0x656c7da3: ('armor_piece3', _decode_armor_piece3),
    0x78694d1b: ('armor_piece4', _decode_armor_piece4),
    0xb3359ebe: ('armor_piece5', _decode_armor_piece5),
    0x35a1ec10: ('armor_piece6', _decode_armor_piece6),
    0xfefd3fb5: ('armor_piece7', _decode_armor_piece7),
    0x37e99c23: ('tail_armor', _decode_tail_armor),
    0xdcc2bf11: ('sound_armor_impact', _decode_sound_armor_impact),
}
