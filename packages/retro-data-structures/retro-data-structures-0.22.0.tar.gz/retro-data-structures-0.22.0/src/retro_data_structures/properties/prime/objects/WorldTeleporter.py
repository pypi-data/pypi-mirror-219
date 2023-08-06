# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class WorldTeleporter(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    world: AssetId = dataclasses.field(metadata={'asset_types': ['MLVL']}, default=default_asset_id)
    area: AssetId = dataclasses.field(metadata={'asset_types': ['MREA']}, default=default_asset_id)
    player_model: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    player_scale: Vector = dataclasses.field(default_factory=Vector)
    elevator_platform_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    elevator_platform_scale: Vector = dataclasses.field(default_factory=Vector)
    elevator_background_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    elevator_background_scale: Vector = dataclasses.field(default_factory=Vector)
    upward_elevator: bool = dataclasses.field(default=False)
    elevator_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_volume: int = dataclasses.field(default=0)
    unknown_sound_related: int = dataclasses.field(default=0)
    show_text_instead_of_cutscene: bool = dataclasses.field(default=False)
    font: AssetId = dataclasses.field(metadata={'asset_types': ['FONT']}, default=default_asset_id)
    string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    fade_in_from_out_to_white: bool = dataclasses.field(default=False)
    character_fade_in_time: float = dataclasses.field(default=0.0)
    characters_per_second: float = dataclasses.field(default=0.0)
    delay_before_showing_text: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x62

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        world = struct.unpack(">L", data.read(4))[0]
        area = struct.unpack(">L", data.read(4))[0]
        player_model = AnimationParameters.from_stream(data, property_size)
        player_scale = Vector.from_stream(data)
        elevator_platform_model = struct.unpack(">L", data.read(4))[0]
        elevator_platform_scale = Vector.from_stream(data)
        elevator_background_model = struct.unpack(">L", data.read(4))[0]
        elevator_background_scale = Vector.from_stream(data)
        upward_elevator = struct.unpack('>?', data.read(1))[0]
        elevator_sound = struct.unpack('>l', data.read(4))[0]
        sound_volume = struct.unpack('>l', data.read(4))[0]
        unknown_sound_related = struct.unpack('>l', data.read(4))[0]
        show_text_instead_of_cutscene = struct.unpack('>?', data.read(1))[0]
        font = struct.unpack(">L", data.read(4))[0]
        string = struct.unpack(">L", data.read(4))[0]
        fade_in_from_out_to_white = struct.unpack('>?', data.read(1))[0]
        character_fade_in_time = struct.unpack('>f', data.read(4))[0]
        characters_per_second = struct.unpack('>f', data.read(4))[0]
        delay_before_showing_text = struct.unpack('>f', data.read(4))[0]
        return cls(name, active, world, area, player_model, player_scale, elevator_platform_model, elevator_platform_scale, elevator_background_model, elevator_background_scale, upward_elevator, elevator_sound, sound_volume, unknown_sound_related, show_text_instead_of_cutscene, font, string, fade_in_from_out_to_white, character_fade_in_time, characters_per_second, delay_before_showing_text)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x15')  # 21 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack(">L", self.world))
        data.write(struct.pack(">L", self.area))
        self.player_model.to_stream(data)
        self.player_scale.to_stream(data)
        data.write(struct.pack(">L", self.elevator_platform_model))
        self.elevator_platform_scale.to_stream(data)
        data.write(struct.pack(">L", self.elevator_background_model))
        self.elevator_background_scale.to_stream(data)
        data.write(struct.pack('>?', self.upward_elevator))
        data.write(struct.pack('>l', self.elevator_sound))
        data.write(struct.pack('>l', self.sound_volume))
        data.write(struct.pack('>l', self.unknown_sound_related))
        data.write(struct.pack('>?', self.show_text_instead_of_cutscene))
        data.write(struct.pack(">L", self.font))
        data.write(struct.pack(">L", self.string))
        data.write(struct.pack('>?', self.fade_in_from_out_to_white))
        data.write(struct.pack('>f', self.character_fade_in_time))
        data.write(struct.pack('>f', self.characters_per_second))
        data.write(struct.pack('>f', self.delay_before_showing_text))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            world=data['world'],
            area=data['area'],
            player_model=AnimationParameters.from_json(data['player_model']),
            player_scale=Vector.from_json(data['player_scale']),
            elevator_platform_model=data['elevator_platform_model'],
            elevator_platform_scale=Vector.from_json(data['elevator_platform_scale']),
            elevator_background_model=data['elevator_background_model'],
            elevator_background_scale=Vector.from_json(data['elevator_background_scale']),
            upward_elevator=data['upward_elevator'],
            elevator_sound=data['elevator_sound'],
            sound_volume=data['sound_volume'],
            unknown_sound_related=data['unknown_sound_related'],
            show_text_instead_of_cutscene=data['show_text_instead_of_cutscene'],
            font=data['font'],
            string=data['string'],
            fade_in_from_out_to_white=data['fade_in_from_out_to_white'],
            character_fade_in_time=data['character_fade_in_time'],
            characters_per_second=data['characters_per_second'],
            delay_before_showing_text=data['delay_before_showing_text'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'world': self.world,
            'area': self.area,
            'player_model': self.player_model.to_json(),
            'player_scale': self.player_scale.to_json(),
            'elevator_platform_model': self.elevator_platform_model,
            'elevator_platform_scale': self.elevator_platform_scale.to_json(),
            'elevator_background_model': self.elevator_background_model,
            'elevator_background_scale': self.elevator_background_scale.to_json(),
            'upward_elevator': self.upward_elevator,
            'elevator_sound': self.elevator_sound,
            'sound_volume': self.sound_volume,
            'unknown_sound_related': self.unknown_sound_related,
            'show_text_instead_of_cutscene': self.show_text_instead_of_cutscene,
            'font': self.font,
            'string': self.string,
            'fade_in_from_out_to_white': self.fade_in_from_out_to_white,
            'character_fade_in_time': self.character_fade_in_time,
            'characters_per_second': self.characters_per_second,
            'delay_before_showing_text': self.delay_before_showing_text,
        }

    def _dependencies_for_player_model(self, asset_manager):
        yield from self.player_model.dependencies_for(asset_manager)

    def _dependencies_for_elevator_platform_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elevator_platform_model)

    def _dependencies_for_elevator_background_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elevator_background_model)

    def _dependencies_for_elevator_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.elevator_sound)

    def _dependencies_for_font(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.font)

    def _dependencies_for_string(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.string)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_player_model, "player_model", "AnimationParameters"),
            (self._dependencies_for_elevator_platform_model, "elevator_platform_model", "AssetId"),
            (self._dependencies_for_elevator_background_model, "elevator_background_model", "AssetId"),
            (self._dependencies_for_elevator_sound, "elevator_sound", "int"),
            (self._dependencies_for_font, "font", "AssetId"),
            (self._dependencies_for_string, "string", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for WorldTeleporter.{field_name} ({field_type}): {e}"
                )
