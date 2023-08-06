# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileRenderOptions import ProjectileRenderOptions
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct194 import UnknownStruct194
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct195 import UnknownStruct195


@dataclasses.dataclass()
class ProjectileRenderData(BaseProperty):
    rendering_type: enums.RenderingType = dataclasses.field(default=enums.RenderingType.Unknown1)
    unknown_struct194: UnknownStruct194 = dataclasses.field(default_factory=UnknownStruct194)
    unknown_struct195: UnknownStruct195 = dataclasses.field(default_factory=UnknownStruct195)
    projectile_render_options: ProjectileRenderOptions = dataclasses.field(default_factory=ProjectileRenderOptions)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x0b\x91\x85y')  # 0xb918579
        data.write(b'\x00\x04')  # size
        self.rendering_type.to_stream(data)

        data.write(b'(\xe0v\xfd')  # 0x28e076fd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct194.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c\xde[\xd9')  # 0x8cde5bd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct195.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\xb2tp')  # 0x5cb27470
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_render_options.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            rendering_type=enums.RenderingType.from_json(data['rendering_type']),
            unknown_struct194=UnknownStruct194.from_json(data['unknown_struct194']),
            unknown_struct195=UnknownStruct195.from_json(data['unknown_struct195']),
            projectile_render_options=ProjectileRenderOptions.from_json(data['projectile_render_options']),
        )

    def to_json(self) -> dict:
        return {
            'rendering_type': self.rendering_type.to_json(),
            'unknown_struct194': self.unknown_struct194.to_json(),
            'unknown_struct195': self.unknown_struct195.to_json(),
            'projectile_render_options': self.projectile_render_options.to_json(),
        }


def _decode_rendering_type(data: typing.BinaryIO, property_size: int):
    return enums.RenderingType.from_stream(data)


def _decode_unknown_struct194(data: typing.BinaryIO, property_size: int):
    return UnknownStruct194.from_stream(data, property_size)


def _decode_unknown_struct195(data: typing.BinaryIO, property_size: int):
    return UnknownStruct195.from_stream(data, property_size)


def _decode_projectile_render_options(data: typing.BinaryIO, property_size: int):
    return ProjectileRenderOptions.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb918579: ('rendering_type', _decode_rendering_type),
    0x28e076fd: ('unknown_struct194', _decode_unknown_struct194),
    0x8cde5bd9: ('unknown_struct195', _decode_unknown_struct195),
    0x5cb27470: ('projectile_render_options', _decode_projectile_render_options),
}
