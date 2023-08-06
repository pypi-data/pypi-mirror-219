# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.CameraHintStructA import CameraHintStructA
from retro_data_structures.properties.echoes.archetypes.CameraHintStructB import CameraHintStructB
from retro_data_structures.properties.echoes.archetypes.CameraHintStructC import CameraHintStructC
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.UnknownStruct4 import UnknownStruct4
from retro_data_structures.properties.echoes.archetypes.UnknownStruct5 import UnknownStruct5
from retro_data_structures.properties.echoes.archetypes.UnknownStruct6 import UnknownStruct6
from retro_data_structures.properties.echoes.archetypes.UnknownStruct7 import UnknownStruct7
from retro_data_structures.properties.echoes.archetypes.UnknownStruct8 import UnknownStruct8
from retro_data_structures.properties.echoes.archetypes.UnknownStruct9 import UnknownStruct9
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class CameraHint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    priority: int = dataclasses.field(default=50)
    timer: float = dataclasses.field(default=0.0)
    unknown_struct4: UnknownStruct4 = dataclasses.field(default_factory=UnknownStruct4)
    flags_camera_hint: int = dataclasses.field(default=286)
    camera_hint_struct_a_0x456d05c6: CameraHintStructB = dataclasses.field(default_factory=CameraHintStructB)
    camera_hint_struct_a_0xf5521ffa: CameraHintStructB = dataclasses.field(default_factory=CameraHintStructB)
    camera_hint_struct_a_0x89658a06: CameraHintStructB = dataclasses.field(default_factory=CameraHintStructB)
    unknown_struct5: UnknownStruct5 = dataclasses.field(default_factory=UnknownStruct5)
    world_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    unknown_struct6: UnknownStruct6 = dataclasses.field(default_factory=UnknownStruct6)
    camera_hint_struct_b_0x664c450a: CameraHintStructC = dataclasses.field(default_factory=CameraHintStructC)
    camera_hint_struct_b_0xc82395fa: CameraHintStructC = dataclasses.field(default_factory=CameraHintStructC)
    unknown_struct7: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)
    unknown_struct8: UnknownStruct8 = dataclasses.field(default_factory=UnknownStruct8)
    unknown_0x2ae08be1: float = dataclasses.field(default=2.0)
    unknown_0x4361d075: float = dataclasses.field(default=1.0)
    unknown_0xc91ef813: float = dataclasses.field(default=1.0)
    camera_hint_struct_a1: CameraHintStructA = dataclasses.field(default_factory=CameraHintStructA)
    unknown_struct9: UnknownStruct9 = dataclasses.field(default_factory=UnknownStruct9)
    camera_hint_struct_a_0x138729a7: CameraHintStructA = dataclasses.field(default_factory=CameraHintStructA)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CAMH'

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

        data.write(b'\x87GU.')  # 0x8747552e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.timer))

        data.write(b'8\x05\x85\xec')  # 0x380585ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\xd7 \xa9')  # 0x21d720a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_camera_hint))

        data.write(b'Em\x05\xc6')  # 0x456d05c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_a_0x456d05c6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5R\x1f\xfa')  # 0xf5521ffa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_a_0xf5521ffa.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x89e\x8a\x06')  # 0x89658a06
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_a_0x89658a06.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\n\x91\x13')  # 0x8d0a9113
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xef\xeb\xe88')  # 0xefebe838
        data.write(b'\x00\x0c')  # size
        self.world_offset.to_stream(data)

        data.write(b'\xf7\x1c6\xf2')  # 0xf71c36f2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'fLE\n')  # 0x664c450a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_b_0x664c450a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8#\x95\xfa')  # 0xc82395fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_b_0xc82395fa.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd^\xb0\t')  # 0x645eb009
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xcf\xbbT')  # 0x80cfbb54
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*\xe0\x8b\xe1')  # 0x2ae08be1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2ae08be1))

        data.write(b'Ca\xd0u')  # 0x4361d075
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4361d075))

        data.write(b'\xc9\x1e\xf8\x13')  # 0xc91ef813
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc91ef813))

        data.write(b'\x93N9,')  # 0x934e392c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_a1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\x861\xf1')  # 0x9e8631f1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\x87)\xa7')  # 0x138729a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_hint_struct_a_0x138729a7.to_stream(data)
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
            priority=data['priority'],
            timer=data['timer'],
            unknown_struct4=UnknownStruct4.from_json(data['unknown_struct4']),
            flags_camera_hint=data['flags_camera_hint'],
            camera_hint_struct_a_0x456d05c6=CameraHintStructB.from_json(data['camera_hint_struct_a_0x456d05c6']),
            camera_hint_struct_a_0xf5521ffa=CameraHintStructB.from_json(data['camera_hint_struct_a_0xf5521ffa']),
            camera_hint_struct_a_0x89658a06=CameraHintStructB.from_json(data['camera_hint_struct_a_0x89658a06']),
            unknown_struct5=UnknownStruct5.from_json(data['unknown_struct5']),
            world_offset=Vector.from_json(data['world_offset']),
            unknown_struct6=UnknownStruct6.from_json(data['unknown_struct6']),
            camera_hint_struct_b_0x664c450a=CameraHintStructC.from_json(data['camera_hint_struct_b_0x664c450a']),
            camera_hint_struct_b_0xc82395fa=CameraHintStructC.from_json(data['camera_hint_struct_b_0xc82395fa']),
            unknown_struct7=UnknownStruct7.from_json(data['unknown_struct7']),
            unknown_struct8=UnknownStruct8.from_json(data['unknown_struct8']),
            unknown_0x2ae08be1=data['unknown_0x2ae08be1'],
            unknown_0x4361d075=data['unknown_0x4361d075'],
            unknown_0xc91ef813=data['unknown_0xc91ef813'],
            camera_hint_struct_a1=CameraHintStructA.from_json(data['camera_hint_struct_a1']),
            unknown_struct9=UnknownStruct9.from_json(data['unknown_struct9']),
            camera_hint_struct_a_0x138729a7=CameraHintStructA.from_json(data['camera_hint_struct_a_0x138729a7']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'priority': self.priority,
            'timer': self.timer,
            'unknown_struct4': self.unknown_struct4.to_json(),
            'flags_camera_hint': self.flags_camera_hint,
            'camera_hint_struct_a_0x456d05c6': self.camera_hint_struct_a_0x456d05c6.to_json(),
            'camera_hint_struct_a_0xf5521ffa': self.camera_hint_struct_a_0xf5521ffa.to_json(),
            'camera_hint_struct_a_0x89658a06': self.camera_hint_struct_a_0x89658a06.to_json(),
            'unknown_struct5': self.unknown_struct5.to_json(),
            'world_offset': self.world_offset.to_json(),
            'unknown_struct6': self.unknown_struct6.to_json(),
            'camera_hint_struct_b_0x664c450a': self.camera_hint_struct_b_0x664c450a.to_json(),
            'camera_hint_struct_b_0xc82395fa': self.camera_hint_struct_b_0xc82395fa.to_json(),
            'unknown_struct7': self.unknown_struct7.to_json(),
            'unknown_struct8': self.unknown_struct8.to_json(),
            'unknown_0x2ae08be1': self.unknown_0x2ae08be1,
            'unknown_0x4361d075': self.unknown_0x4361d075,
            'unknown_0xc91ef813': self.unknown_0xc91ef813,
            'camera_hint_struct_a1': self.camera_hint_struct_a1.to_json(),
            'unknown_struct9': self.unknown_struct9.to_json(),
            'camera_hint_struct_a_0x138729a7': self.camera_hint_struct_a_0x138729a7.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct4(self, asset_manager):
        yield from self.unknown_struct4.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_a_0x456d05c6(self, asset_manager):
        yield from self.camera_hint_struct_a_0x456d05c6.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_a_0xf5521ffa(self, asset_manager):
        yield from self.camera_hint_struct_a_0xf5521ffa.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_a_0x89658a06(self, asset_manager):
        yield from self.camera_hint_struct_a_0x89658a06.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct5(self, asset_manager):
        yield from self.unknown_struct5.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct6(self, asset_manager):
        yield from self.unknown_struct6.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_b_0x664c450a(self, asset_manager):
        yield from self.camera_hint_struct_b_0x664c450a.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_b_0xc82395fa(self, asset_manager):
        yield from self.camera_hint_struct_b_0xc82395fa.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct7(self, asset_manager):
        yield from self.unknown_struct7.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct8(self, asset_manager):
        yield from self.unknown_struct8.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_a1(self, asset_manager):
        yield from self.camera_hint_struct_a1.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct9(self, asset_manager):
        yield from self.unknown_struct9.dependencies_for(asset_manager)

    def _dependencies_for_camera_hint_struct_a_0x138729a7(self, asset_manager):
        yield from self.camera_hint_struct_a_0x138729a7.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_unknown_struct4, "unknown_struct4", "UnknownStruct4"),
            (self._dependencies_for_camera_hint_struct_a_0x456d05c6, "camera_hint_struct_a_0x456d05c6", "CameraHintStructB"),
            (self._dependencies_for_camera_hint_struct_a_0xf5521ffa, "camera_hint_struct_a_0xf5521ffa", "CameraHintStructB"),
            (self._dependencies_for_camera_hint_struct_a_0x89658a06, "camera_hint_struct_a_0x89658a06", "CameraHintStructB"),
            (self._dependencies_for_unknown_struct5, "unknown_struct5", "UnknownStruct5"),
            (self._dependencies_for_unknown_struct6, "unknown_struct6", "UnknownStruct6"),
            (self._dependencies_for_camera_hint_struct_b_0x664c450a, "camera_hint_struct_b_0x664c450a", "CameraHintStructC"),
            (self._dependencies_for_camera_hint_struct_b_0xc82395fa, "camera_hint_struct_b_0xc82395fa", "CameraHintStructC"),
            (self._dependencies_for_unknown_struct7, "unknown_struct7", "UnknownStruct7"),
            (self._dependencies_for_unknown_struct8, "unknown_struct8", "UnknownStruct8"),
            (self._dependencies_for_camera_hint_struct_a1, "camera_hint_struct_a1", "CameraHintStructA"),
            (self._dependencies_for_unknown_struct9, "unknown_struct9", "UnknownStruct9"),
            (self._dependencies_for_camera_hint_struct_a_0x138729a7, "camera_hint_struct_a_0x138729a7", "CameraHintStructA"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for CameraHint.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct4(data: typing.BinaryIO, property_size: int):
    return UnknownStruct4.from_stream(data, property_size)


def _decode_flags_camera_hint(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_camera_hint_struct_a_0x456d05c6(data: typing.BinaryIO, property_size: int):
    return CameraHintStructB.from_stream(data, property_size)


def _decode_camera_hint_struct_a_0xf5521ffa(data: typing.BinaryIO, property_size: int):
    return CameraHintStructB.from_stream(data, property_size)


def _decode_camera_hint_struct_a_0x89658a06(data: typing.BinaryIO, property_size: int):
    return CameraHintStructB.from_stream(data, property_size)


def _decode_unknown_struct5(data: typing.BinaryIO, property_size: int):
    return UnknownStruct5.from_stream(data, property_size)


def _decode_world_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_struct6(data: typing.BinaryIO, property_size: int):
    return UnknownStruct6.from_stream(data, property_size)


def _decode_camera_hint_struct_b_0x664c450a(data: typing.BinaryIO, property_size: int):
    return CameraHintStructC.from_stream(data, property_size)


def _decode_camera_hint_struct_b_0xc82395fa(data: typing.BinaryIO, property_size: int):
    return CameraHintStructC.from_stream(data, property_size)


def _decode_unknown_struct7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


def _decode_unknown_struct8(data: typing.BinaryIO, property_size: int):
    return UnknownStruct8.from_stream(data, property_size)


def _decode_unknown_0x2ae08be1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4361d075(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc91ef813(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_hint_struct_a1(data: typing.BinaryIO, property_size: int):
    return CameraHintStructA.from_stream(data, property_size)


def _decode_unknown_struct9(data: typing.BinaryIO, property_size: int):
    return UnknownStruct9.from_stream(data, property_size)


def _decode_camera_hint_struct_a_0x138729a7(data: typing.BinaryIO, property_size: int):
    return CameraHintStructA.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x42087650: ('priority', _decode_priority),
    0x8747552e: ('timer', _decode_timer),
    0x380585ec: ('unknown_struct4', _decode_unknown_struct4),
    0x21d720a9: ('flags_camera_hint', _decode_flags_camera_hint),
    0x456d05c6: ('camera_hint_struct_a_0x456d05c6', _decode_camera_hint_struct_a_0x456d05c6),
    0xf5521ffa: ('camera_hint_struct_a_0xf5521ffa', _decode_camera_hint_struct_a_0xf5521ffa),
    0x89658a06: ('camera_hint_struct_a_0x89658a06', _decode_camera_hint_struct_a_0x89658a06),
    0x8d0a9113: ('unknown_struct5', _decode_unknown_struct5),
    0xefebe838: ('world_offset', _decode_world_offset),
    0xf71c36f2: ('unknown_struct6', _decode_unknown_struct6),
    0x664c450a: ('camera_hint_struct_b_0x664c450a', _decode_camera_hint_struct_b_0x664c450a),
    0xc82395fa: ('camera_hint_struct_b_0xc82395fa', _decode_camera_hint_struct_b_0xc82395fa),
    0x645eb009: ('unknown_struct7', _decode_unknown_struct7),
    0x80cfbb54: ('unknown_struct8', _decode_unknown_struct8),
    0x2ae08be1: ('unknown_0x2ae08be1', _decode_unknown_0x2ae08be1),
    0x4361d075: ('unknown_0x4361d075', _decode_unknown_0x4361d075),
    0xc91ef813: ('unknown_0xc91ef813', _decode_unknown_0xc91ef813),
    0x934e392c: ('camera_hint_struct_a1', _decode_camera_hint_struct_a1),
    0x9e8631f1: ('unknown_struct9', _decode_unknown_struct9),
    0x138729a7: ('camera_hint_struct_a_0x138729a7', _decode_camera_hint_struct_a_0x138729a7),
}
