# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.echoes as enums
from retro_data_structures.properties.echoes.archetypes.ScanInfoSecondaryModel import ScanInfoSecondaryModel
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScannableObjectInfo(BaseObjectType):
    string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    scan_speed: enums.ScanSpeed = dataclasses.field(default=enums.ScanSpeed.Normal)
    critical: bool = dataclasses.field(default=False)
    unknown_0x1733b1ec: bool = dataclasses.field(default=False)
    unknown_0x53336141: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    model_initial_pitch: float = dataclasses.field(default=0.0)
    model_initial_yaw: float = dataclasses.field(default=0.0)
    model_scale: float = dataclasses.field(default=1.0)
    static_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animated_model: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x58f9fe99: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    secondary_model0: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model1: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model2: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model3: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model4: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model5: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model6: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model7: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)
    secondary_model8: ScanInfoSecondaryModel = dataclasses.field(default_factory=ScanInfoSecondaryModel)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'SNFO'

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
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'/[d#')  # 0x2f5b6423
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.string))

        data.write(b'\xc3\x08\xa3"')  # 0xc308a322
        data.write(b'\x00\x04')  # size
        self.scan_speed.to_stream(data)

        data.write(b'{qH\x14')  # 0x7b714814
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.critical))

        data.write(b'\x173\xb1\xec')  # 0x1733b1ec
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1733b1ec))

        data.write(b'S3aA')  # 0x53336141
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x53336141))

        data.write(b'=\xe0\xbad')  # 0x3de0ba64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.model_initial_pitch))

        data.write(b'*\xddf(')  # 0x2add6628
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.model_initial_yaw))

        data.write(b'\xd0\xc1Pf')  # 0xd0c15066
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.model_scale))

        data.write(b'\xb7\xad\xc4\x18')  # 0xb7adc418
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.static_model))

        data.write(b'\x15iN\xe1')  # 0x15694ee1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animated_model.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\xf9\xfe\x99')  # 0x58f9fe99
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x58f9fe99.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c[J:')  # 0x1c5b4a3a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x87(\xa0\xee')  # 0x8728a0ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1\xcd\x99\xd3')  # 0xf1cd99d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j\xbes\x07')  # 0x6abe7307
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\x07\xeb\xa9')  # 0x1c07eba9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x87t\x01}')  # 0x8774017d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1\x918@')  # 0xf1913840
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j\xe2\xd2\x94')  # 0x6ae2d294
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\xe2\t\x1c')  # 0x1ce2091c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.secondary_model8.to_stream(data)
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
            string=data['string'],
            scan_speed=enums.ScanSpeed.from_json(data['scan_speed']),
            critical=data['critical'],
            unknown_0x1733b1ec=data['unknown_0x1733b1ec'],
            unknown_0x53336141=data['unknown_0x53336141'],
            model_initial_pitch=data['model_initial_pitch'],
            model_initial_yaw=data['model_initial_yaw'],
            model_scale=data['model_scale'],
            static_model=data['static_model'],
            animated_model=AnimationParameters.from_json(data['animated_model']),
            unknown_0x58f9fe99=AnimationParameters.from_json(data['unknown_0x58f9fe99']),
            secondary_model0=ScanInfoSecondaryModel.from_json(data['secondary_model0']),
            secondary_model1=ScanInfoSecondaryModel.from_json(data['secondary_model1']),
            secondary_model2=ScanInfoSecondaryModel.from_json(data['secondary_model2']),
            secondary_model3=ScanInfoSecondaryModel.from_json(data['secondary_model3']),
            secondary_model4=ScanInfoSecondaryModel.from_json(data['secondary_model4']),
            secondary_model5=ScanInfoSecondaryModel.from_json(data['secondary_model5']),
            secondary_model6=ScanInfoSecondaryModel.from_json(data['secondary_model6']),
            secondary_model7=ScanInfoSecondaryModel.from_json(data['secondary_model7']),
            secondary_model8=ScanInfoSecondaryModel.from_json(data['secondary_model8']),
        )

    def to_json(self) -> dict:
        return {
            'string': self.string,
            'scan_speed': self.scan_speed.to_json(),
            'critical': self.critical,
            'unknown_0x1733b1ec': self.unknown_0x1733b1ec,
            'unknown_0x53336141': self.unknown_0x53336141,
            'model_initial_pitch': self.model_initial_pitch,
            'model_initial_yaw': self.model_initial_yaw,
            'model_scale': self.model_scale,
            'static_model': self.static_model,
            'animated_model': self.animated_model.to_json(),
            'unknown_0x58f9fe99': self.unknown_0x58f9fe99.to_json(),
            'secondary_model0': self.secondary_model0.to_json(),
            'secondary_model1': self.secondary_model1.to_json(),
            'secondary_model2': self.secondary_model2.to_json(),
            'secondary_model3': self.secondary_model3.to_json(),
            'secondary_model4': self.secondary_model4.to_json(),
            'secondary_model5': self.secondary_model5.to_json(),
            'secondary_model6': self.secondary_model6.to_json(),
            'secondary_model7': self.secondary_model7.to_json(),
            'secondary_model8': self.secondary_model8.to_json(),
        }

    def _dependencies_for_string(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.string)

    def _dependencies_for_unknown_0x53336141(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.unknown_0x53336141)

    def _dependencies_for_static_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.static_model)

    def _dependencies_for_animated_model(self, asset_manager):
        yield from self.animated_model.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x58f9fe99(self, asset_manager):
        yield from self.unknown_0x58f9fe99.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model0(self, asset_manager):
        yield from self.secondary_model0.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model1(self, asset_manager):
        yield from self.secondary_model1.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model2(self, asset_manager):
        yield from self.secondary_model2.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model3(self, asset_manager):
        yield from self.secondary_model3.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model4(self, asset_manager):
        yield from self.secondary_model4.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model5(self, asset_manager):
        yield from self.secondary_model5.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model6(self, asset_manager):
        yield from self.secondary_model6.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model7(self, asset_manager):
        yield from self.secondary_model7.dependencies_for(asset_manager)

    def _dependencies_for_secondary_model8(self, asset_manager):
        yield from self.secondary_model8.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_string, "string", "AssetId"),
            (self._dependencies_for_unknown_0x53336141, "unknown_0x53336141", "AssetId"),
            (self._dependencies_for_static_model, "static_model", "AssetId"),
            (self._dependencies_for_animated_model, "animated_model", "AnimationParameters"),
            (self._dependencies_for_unknown_0x58f9fe99, "unknown_0x58f9fe99", "AnimationParameters"),
            (self._dependencies_for_secondary_model0, "secondary_model0", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model1, "secondary_model1", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model2, "secondary_model2", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model3, "secondary_model3", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model4, "secondary_model4", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model5, "secondary_model5", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model6, "secondary_model6", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model7, "secondary_model7", "ScanInfoSecondaryModel"),
            (self._dependencies_for_secondary_model8, "secondary_model8", "ScanInfoSecondaryModel"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScannableObjectInfo.{field_name} ({field_type}): {e}"
                )


def _decode_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scan_speed(data: typing.BinaryIO, property_size: int):
    return enums.ScanSpeed.from_stream(data)


def _decode_critical(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x1733b1ec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x53336141(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_model_initial_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model_initial_yaw(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_static_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_animated_model(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x58f9fe99(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_secondary_model0(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model1(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model2(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model3(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model4(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model5(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model6(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model7(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


def _decode_secondary_model8(data: typing.BinaryIO, property_size: int):
    return ScanInfoSecondaryModel.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2f5b6423: ('string', _decode_string),
    0xc308a322: ('scan_speed', _decode_scan_speed),
    0x7b714814: ('critical', _decode_critical),
    0x1733b1ec: ('unknown_0x1733b1ec', _decode_unknown_0x1733b1ec),
    0x53336141: ('unknown_0x53336141', _decode_unknown_0x53336141),
    0x3de0ba64: ('model_initial_pitch', _decode_model_initial_pitch),
    0x2add6628: ('model_initial_yaw', _decode_model_initial_yaw),
    0xd0c15066: ('model_scale', _decode_model_scale),
    0xb7adc418: ('static_model', _decode_static_model),
    0x15694ee1: ('animated_model', _decode_animated_model),
    0x58f9fe99: ('unknown_0x58f9fe99', _decode_unknown_0x58f9fe99),
    0x1c5b4a3a: ('secondary_model0', _decode_secondary_model0),
    0x8728a0ee: ('secondary_model1', _decode_secondary_model1),
    0xf1cd99d3: ('secondary_model2', _decode_secondary_model2),
    0x6abe7307: ('secondary_model3', _decode_secondary_model3),
    0x1c07eba9: ('secondary_model4', _decode_secondary_model4),
    0x8774017d: ('secondary_model5', _decode_secondary_model5),
    0xf1913840: ('secondary_model6', _decode_secondary_model6),
    0x6ae2d294: ('secondary_model7', _decode_secondary_model7),
    0x1ce2091c: ('secondary_model8', _decode_secondary_model8),
}
