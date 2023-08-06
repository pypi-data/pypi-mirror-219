# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TBallTransitionResources import TBallTransitionResources
from retro_data_structures.properties.echoes.archetypes.TGunResources import TGunResources
from retro_data_structures.properties.echoes.archetypes.TweakPlayerRes.AutoMapperIcons import AutoMapperIcons
from retro_data_structures.properties.echoes.archetypes.TweakPlayerRes.MapScreenIcons import MapScreenIcons


@dataclasses.dataclass()
class TweakPlayerRes(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    auto_mapper_icons: AutoMapperIcons = dataclasses.field(default_factory=AutoMapperIcons)
    map_screen_icons: MapScreenIcons = dataclasses.field(default_factory=MapScreenIcons)
    ball_transition_resources: TBallTransitionResources = dataclasses.field(default_factory=TBallTransitionResources)
    cinematic_resources: TGunResources = dataclasses.field(default_factory=TGunResources)
    unknown: float = dataclasses.field(default=-0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWPR'

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

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5wA\xe0')  # 0x357741e0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.auto_mapper_icons.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\r^\x02\xa0')  # 0xd5e02a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.map_screen_icons.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'\x98R\xba")  # 0x279852ba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_transition_resources.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^c\x06\x08')  # 0x5e630608
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cinematic_resources.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xad\x9d\x19')  # 0x36ad9d19
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            instance_name=data['instance_name'],
            auto_mapper_icons=AutoMapperIcons.from_json(data['auto_mapper_icons']),
            map_screen_icons=MapScreenIcons.from_json(data['map_screen_icons']),
            ball_transition_resources=TBallTransitionResources.from_json(data['ball_transition_resources']),
            cinematic_resources=TGunResources.from_json(data['cinematic_resources']),
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'auto_mapper_icons': self.auto_mapper_icons.to_json(),
            'map_screen_icons': self.map_screen_icons.to_json(),
            'ball_transition_resources': self.ball_transition_resources.to_json(),
            'cinematic_resources': self.cinematic_resources.to_json(),
            'unknown': self.unknown,
        }

    def _dependencies_for_auto_mapper_icons(self, asset_manager):
        yield from self.auto_mapper_icons.dependencies_for(asset_manager)

    def _dependencies_for_map_screen_icons(self, asset_manager):
        yield from self.map_screen_icons.dependencies_for(asset_manager)

    def _dependencies_for_ball_transition_resources(self, asset_manager):
        yield from self.ball_transition_resources.dependencies_for(asset_manager)

    def _dependencies_for_cinematic_resources(self, asset_manager):
        yield from self.cinematic_resources.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_auto_mapper_icons, "auto_mapper_icons", "AutoMapperIcons"),
            (self._dependencies_for_map_screen_icons, "map_screen_icons", "MapScreenIcons"),
            (self._dependencies_for_ball_transition_resources, "ball_transition_resources", "TBallTransitionResources"),
            (self._dependencies_for_cinematic_resources, "cinematic_resources", "TGunResources"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakPlayerRes.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_auto_mapper_icons(data: typing.BinaryIO, property_size: int):
    return AutoMapperIcons.from_stream(data, property_size)


def _decode_map_screen_icons(data: typing.BinaryIO, property_size: int):
    return MapScreenIcons.from_stream(data, property_size)


def _decode_ball_transition_resources(data: typing.BinaryIO, property_size: int):
    return TBallTransitionResources.from_stream(data, property_size)


def _decode_cinematic_resources(data: typing.BinaryIO, property_size: int):
    return TGunResources.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0x357741e0: ('auto_mapper_icons', _decode_auto_mapper_icons),
    0xd5e02a0: ('map_screen_icons', _decode_map_screen_icons),
    0x279852ba: ('ball_transition_resources', _decode_ball_transition_resources),
    0x5e630608: ('cinematic_resources', _decode_cinematic_resources),
    0x36ad9d19: ('unknown', _decode_unknown),
}
