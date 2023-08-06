# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class DestructibleBarrier(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0xcd4f7e71: int = dataclasses.field(default=2)
    unknown_0xa7f551f7: int = dataclasses.field(default=5)
    unknown_0x609c6240: int = dataclasses.field(default=1)
    chunk_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.5, y=0.20000000298023224, z=1.0))
    left_model: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    center_model: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    right_model: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x396660b4: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x48e25884: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    base_model: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x1eb90d06: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x9d852dfe: int = dataclasses.field(default=4)
    unknown_0x982d7fa8: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x2e11003d: int = dataclasses.field(default=4)
    unknown_0x5371ac0d: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x409d1b7c: int = dataclasses.field(default=1)
    unknown_0x4e749cb5: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unknown_0x92485dfa: int = dataclasses.field(default=1)
    unknown_0x6e4a9d27: int = dataclasses.field(default=0)
    unknown_0xbc2381a6: int = dataclasses.field(default=0)
    unknown_0x6575a3d5: int = dataclasses.field(default=0)
    unknown_0xc91b0946: int = dataclasses.field(default=0)
    unknown_0x4b2d5a37: int = dataclasses.field(default=0)
    unknown_0x605847b9: float = dataclasses.field(default=50.0)
    unknown_0xcd9c67fe: float = dataclasses.field(default=10.0)
    unknown_0x0af428b4: float = dataclasses.field(default=10.0)
    unknown_0x4d3109e3: bool = dataclasses.field(default=False)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DBAR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['DestructibleBarrier.rel']

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcdO~q')  # 0xcd4f7e71
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xcd4f7e71))

        data.write(b'\xa7\xf5Q\xf7')  # 0xa7f551f7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa7f551f7))

        data.write(b'`\x9cb@')  # 0x609c6240
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x609c6240))

        data.write(b'\xb2\x9e\x15\x9e')  # 0xb29e159e
        data.write(b'\x00\x0c')  # size
        self.chunk_size.to_stream(data)

        data.write(b'\x01J\x0c6')  # 0x14a0c36
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.left_model))

        data.write(b'\x90\xf5\\]')  # 0x90f55c5d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.center_model))

        data.write(b'\xe1\x97SU')  # 0xe1975355
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.right_model))

        data.write(b'9f`\xb4')  # 0x396660b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x396660b4))

        data.write(b'H\xe2X\x84')  # 0x48e25884
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x48e25884))

        data.write(b'\xf1\xab\xb2\xc7')  # 0xf1abb2c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.base_model))

        data.write(b'\x1e\xb9\r\x06')  # 0x1eb90d06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x1eb90d06))

        data.write(b'\x9d\x85-\xfe')  # 0x9d852dfe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9d852dfe))

        data.write(b'\x98-\x7f\xa8')  # 0x982d7fa8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x982d7fa8))

        data.write(b'.\x11\x00=')  # 0x2e11003d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x2e11003d))

        data.write(b'Sq\xac\r')  # 0x5371ac0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x5371ac0d))

        data.write(b'@\x9d\x1b|')  # 0x409d1b7c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x409d1b7c))

        data.write(b'Nt\x9c\xb5')  # 0x4e749cb5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x4e749cb5))

        data.write(b'\x92H]\xfa')  # 0x92485dfa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x92485dfa))

        data.write(b"nJ\x9d'")  # 0x6e4a9d27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6e4a9d27))

        data.write(b'\xbc#\x81\xa6')  # 0xbc2381a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbc2381a6))

        data.write(b'eu\xa3\xd5')  # 0x6575a3d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6575a3d5))

        data.write(b'\xc9\x1b\tF')  # 0xc91b0946
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc91b0946))

        data.write(b'K-Z7')  # 0x4b2d5a37
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x4b2d5a37))

        data.write(b'`XG\xb9')  # 0x605847b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x605847b9))

        data.write(b'\xcd\x9cg\xfe')  # 0xcd9c67fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd9c67fe))

        data.write(b'\n\xf4(\xb4')  # 0xaf428b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0af428b4))

        data.write(b'M1\t\xe3')  # 0x4d3109e3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4d3109e3))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
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

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_0xcd4f7e71=data['unknown_0xcd4f7e71'],
            unknown_0xa7f551f7=data['unknown_0xa7f551f7'],
            unknown_0x609c6240=data['unknown_0x609c6240'],
            chunk_size=Vector.from_json(data['chunk_size']),
            left_model=data['left_model'],
            center_model=data['center_model'],
            right_model=data['right_model'],
            unknown_0x396660b4=data['unknown_0x396660b4'],
            unknown_0x48e25884=data['unknown_0x48e25884'],
            base_model=data['base_model'],
            unknown_0x1eb90d06=data['unknown_0x1eb90d06'],
            unknown_0x9d852dfe=data['unknown_0x9d852dfe'],
            unknown_0x982d7fa8=data['unknown_0x982d7fa8'],
            unknown_0x2e11003d=data['unknown_0x2e11003d'],
            unknown_0x5371ac0d=data['unknown_0x5371ac0d'],
            unknown_0x409d1b7c=data['unknown_0x409d1b7c'],
            unknown_0x4e749cb5=data['unknown_0x4e749cb5'],
            unknown_0x92485dfa=data['unknown_0x92485dfa'],
            unknown_0x6e4a9d27=data['unknown_0x6e4a9d27'],
            unknown_0xbc2381a6=data['unknown_0xbc2381a6'],
            unknown_0x6575a3d5=data['unknown_0x6575a3d5'],
            unknown_0xc91b0946=data['unknown_0xc91b0946'],
            unknown_0x4b2d5a37=data['unknown_0x4b2d5a37'],
            unknown_0x605847b9=data['unknown_0x605847b9'],
            unknown_0xcd9c67fe=data['unknown_0xcd9c67fe'],
            unknown_0x0af428b4=data['unknown_0x0af428b4'],
            unknown_0x4d3109e3=data['unknown_0x4d3109e3'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0xcd4f7e71': self.unknown_0xcd4f7e71,
            'unknown_0xa7f551f7': self.unknown_0xa7f551f7,
            'unknown_0x609c6240': self.unknown_0x609c6240,
            'chunk_size': self.chunk_size.to_json(),
            'left_model': self.left_model,
            'center_model': self.center_model,
            'right_model': self.right_model,
            'unknown_0x396660b4': self.unknown_0x396660b4,
            'unknown_0x48e25884': self.unknown_0x48e25884,
            'base_model': self.base_model,
            'unknown_0x1eb90d06': self.unknown_0x1eb90d06,
            'unknown_0x9d852dfe': self.unknown_0x9d852dfe,
            'unknown_0x982d7fa8': self.unknown_0x982d7fa8,
            'unknown_0x2e11003d': self.unknown_0x2e11003d,
            'unknown_0x5371ac0d': self.unknown_0x5371ac0d,
            'unknown_0x409d1b7c': self.unknown_0x409d1b7c,
            'unknown_0x4e749cb5': self.unknown_0x4e749cb5,
            'unknown_0x92485dfa': self.unknown_0x92485dfa,
            'unknown_0x6e4a9d27': self.unknown_0x6e4a9d27,
            'unknown_0xbc2381a6': self.unknown_0xbc2381a6,
            'unknown_0x6575a3d5': self.unknown_0x6575a3d5,
            'unknown_0xc91b0946': self.unknown_0xc91b0946,
            'unknown_0x4b2d5a37': self.unknown_0x4b2d5a37,
            'unknown_0x605847b9': self.unknown_0x605847b9,
            'unknown_0xcd9c67fe': self.unknown_0xcd9c67fe,
            'unknown_0x0af428b4': self.unknown_0x0af428b4,
            'unknown_0x4d3109e3': self.unknown_0x4d3109e3,
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'actor_information': self.actor_information.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_left_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.left_model)

    def _dependencies_for_center_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.center_model)

    def _dependencies_for_right_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.right_model)

    def _dependencies_for_unknown_0x396660b4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x396660b4)

    def _dependencies_for_unknown_0x48e25884(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x48e25884)

    def _dependencies_for_base_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.base_model)

    def _dependencies_for_unknown_0x1eb90d06(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x1eb90d06)

    def _dependencies_for_unknown_0x982d7fa8(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x982d7fa8)

    def _dependencies_for_unknown_0x5371ac0d(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x5371ac0d)

    def _dependencies_for_unknown_0x4e749cb5(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x4e749cb5)

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_vulnerability(self, asset_manager):
        yield from self.vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_left_model, "left_model", "AssetId"),
            (self._dependencies_for_center_model, "center_model", "AssetId"),
            (self._dependencies_for_right_model, "right_model", "AssetId"),
            (self._dependencies_for_unknown_0x396660b4, "unknown_0x396660b4", "AssetId"),
            (self._dependencies_for_unknown_0x48e25884, "unknown_0x48e25884", "AssetId"),
            (self._dependencies_for_base_model, "base_model", "AssetId"),
            (self._dependencies_for_unknown_0x1eb90d06, "unknown_0x1eb90d06", "AssetId"),
            (self._dependencies_for_unknown_0x982d7fa8, "unknown_0x982d7fa8", "AssetId"),
            (self._dependencies_for_unknown_0x5371ac0d, "unknown_0x5371ac0d", "AssetId"),
            (self._dependencies_for_unknown_0x4e749cb5, "unknown_0x4e749cb5", "AssetId"),
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_vulnerability, "vulnerability", "DamageVulnerability"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DestructibleBarrier.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0xcd4f7e71(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xa7f551f7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x609c6240(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_chunk_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_left_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_center_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_right_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x396660b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x48e25884(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_base_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x1eb90d06(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x9d852dfe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x982d7fa8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x2e11003d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x5371ac0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x409d1b7c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4e749cb5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x92485dfa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6e4a9d27(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xbc2381a6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6575a3d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc91b0946(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4b2d5a37(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x605847b9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd9c67fe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0af428b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4d3109e3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xcd4f7e71: ('unknown_0xcd4f7e71', _decode_unknown_0xcd4f7e71),
    0xa7f551f7: ('unknown_0xa7f551f7', _decode_unknown_0xa7f551f7),
    0x609c6240: ('unknown_0x609c6240', _decode_unknown_0x609c6240),
    0xb29e159e: ('chunk_size', _decode_chunk_size),
    0x14a0c36: ('left_model', _decode_left_model),
    0x90f55c5d: ('center_model', _decode_center_model),
    0xe1975355: ('right_model', _decode_right_model),
    0x396660b4: ('unknown_0x396660b4', _decode_unknown_0x396660b4),
    0x48e25884: ('unknown_0x48e25884', _decode_unknown_0x48e25884),
    0xf1abb2c7: ('base_model', _decode_base_model),
    0x1eb90d06: ('unknown_0x1eb90d06', _decode_unknown_0x1eb90d06),
    0x9d852dfe: ('unknown_0x9d852dfe', _decode_unknown_0x9d852dfe),
    0x982d7fa8: ('unknown_0x982d7fa8', _decode_unknown_0x982d7fa8),
    0x2e11003d: ('unknown_0x2e11003d', _decode_unknown_0x2e11003d),
    0x5371ac0d: ('unknown_0x5371ac0d', _decode_unknown_0x5371ac0d),
    0x409d1b7c: ('unknown_0x409d1b7c', _decode_unknown_0x409d1b7c),
    0x4e749cb5: ('unknown_0x4e749cb5', _decode_unknown_0x4e749cb5),
    0x92485dfa: ('unknown_0x92485dfa', _decode_unknown_0x92485dfa),
    0x6e4a9d27: ('unknown_0x6e4a9d27', _decode_unknown_0x6e4a9d27),
    0xbc2381a6: ('unknown_0xbc2381a6', _decode_unknown_0xbc2381a6),
    0x6575a3d5: ('unknown_0x6575a3d5', _decode_unknown_0x6575a3d5),
    0xc91b0946: ('unknown_0xc91b0946', _decode_unknown_0xc91b0946),
    0x4b2d5a37: ('unknown_0x4b2d5a37', _decode_unknown_0x4b2d5a37),
    0x605847b9: ('unknown_0x605847b9', _decode_unknown_0x605847b9),
    0xcd9c67fe: ('unknown_0xcd9c67fe', _decode_unknown_0xcd9c67fe),
    0xaf428b4: ('unknown_0x0af428b4', _decode_unknown_0x0af428b4),
    0x4d3109e3: ('unknown_0x4d3109e3', _decode_unknown_0x4d3109e3),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
