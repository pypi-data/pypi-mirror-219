# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.TweakGui.Completion import Completion
from retro_data_structures.properties.echoes.archetypes.TweakGui.Credits import Credits
from retro_data_structures.properties.echoes.archetypes.TweakGui.DarkVisor import DarkVisor
from retro_data_structures.properties.echoes.archetypes.TweakGui.EchoVisor import EchoVisor
from retro_data_structures.properties.echoes.archetypes.TweakGui.LogBook import LogBook
from retro_data_structures.properties.echoes.archetypes.TweakGui.Misc import Misc
from retro_data_structures.properties.echoes.archetypes.TweakGui.MovieVolumes import MovieVolumes
from retro_data_structures.properties.echoes.archetypes.TweakGui.ScanVisor import ScanVisor
from retro_data_structures.properties.echoes.archetypes.TweakGui.ScannableObjectDownloadTimes import ScannableObjectDownloadTimes


@dataclasses.dataclass()
class TweakGui(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    misc: Misc = dataclasses.field(default_factory=Misc)
    scannable_object_download_times: ScannableObjectDownloadTimes = dataclasses.field(default_factory=ScannableObjectDownloadTimes)
    unknown: DarkVisor = dataclasses.field(default_factory=DarkVisor)
    echo_visor: EchoVisor = dataclasses.field(default_factory=EchoVisor)
    scan_visor: ScanVisor = dataclasses.field(default_factory=ScanVisor)
    log_book: LogBook = dataclasses.field(default_factory=LogBook)
    credits: Credits = dataclasses.field(default_factory=Credits)
    completion: Completion = dataclasses.field(default_factory=Completion)
    movie_volumes: MovieVolumes = dataclasses.field(default_factory=MovieVolumes)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWGU'

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd4_vc')  # 0xd45f7663
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xb1>`')  # 0x80b13e60
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scannable_object_download_times.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10*\xa3\x8d')  # 0x102aa38d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+i\x8eE')  # 0x2b698e45
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.echo_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@\xff\xb3\xc4')  # 0x40ffb3c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scan_visor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\xb8\xa7j')  # 0x97b8a76a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.log_book.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w94\x16')  # 0x77393416
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.credits.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\x14\x98\x92')  # 0x2149892
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.completion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf6\x1e\x92')  # 0xa4f61e92
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.movie_volumes.to_stream(data)
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
            misc=Misc.from_json(data['misc']),
            scannable_object_download_times=ScannableObjectDownloadTimes.from_json(data['scannable_object_download_times']),
            unknown=DarkVisor.from_json(data['unknown']),
            echo_visor=EchoVisor.from_json(data['echo_visor']),
            scan_visor=ScanVisor.from_json(data['scan_visor']),
            log_book=LogBook.from_json(data['log_book']),
            credits=Credits.from_json(data['credits']),
            completion=Completion.from_json(data['completion']),
            movie_volumes=MovieVolumes.from_json(data['movie_volumes']),
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'misc': self.misc.to_json(),
            'scannable_object_download_times': self.scannable_object_download_times.to_json(),
            'unknown': self.unknown.to_json(),
            'echo_visor': self.echo_visor.to_json(),
            'scan_visor': self.scan_visor.to_json(),
            'log_book': self.log_book.to_json(),
            'credits': self.credits.to_json(),
            'completion': self.completion.to_json(),
            'movie_volumes': self.movie_volumes.to_json(),
        }

    def _dependencies_for_misc(self, asset_manager):
        yield from self.misc.dependencies_for(asset_manager)

    def _dependencies_for_scannable_object_download_times(self, asset_manager):
        yield from self.scannable_object_download_times.dependencies_for(asset_manager)

    def _dependencies_for_unknown(self, asset_manager):
        yield from self.unknown.dependencies_for(asset_manager)

    def _dependencies_for_echo_visor(self, asset_manager):
        yield from self.echo_visor.dependencies_for(asset_manager)

    def _dependencies_for_scan_visor(self, asset_manager):
        yield from self.scan_visor.dependencies_for(asset_manager)

    def _dependencies_for_log_book(self, asset_manager):
        yield from self.log_book.dependencies_for(asset_manager)

    def _dependencies_for_credits(self, asset_manager):
        yield from self.credits.dependencies_for(asset_manager)

    def _dependencies_for_completion(self, asset_manager):
        yield from self.completion.dependencies_for(asset_manager)

    def _dependencies_for_movie_volumes(self, asset_manager):
        yield from self.movie_volumes.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_misc, "misc", "Misc"),
            (self._dependencies_for_scannable_object_download_times, "scannable_object_download_times", "ScannableObjectDownloadTimes"),
            (self._dependencies_for_unknown, "unknown", "DarkVisor"),
            (self._dependencies_for_echo_visor, "echo_visor", "EchoVisor"),
            (self._dependencies_for_scan_visor, "scan_visor", "ScanVisor"),
            (self._dependencies_for_log_book, "log_book", "LogBook"),
            (self._dependencies_for_credits, "credits", "Credits"),
            (self._dependencies_for_completion, "completion", "Completion"),
            (self._dependencies_for_movie_volumes, "movie_volumes", "MovieVolumes"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TweakGui.{field_name} ({field_type}): {e}"
                )


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_misc(data: typing.BinaryIO, property_size: int):
    return Misc.from_stream(data, property_size)


def _decode_scannable_object_download_times(data: typing.BinaryIO, property_size: int):
    return ScannableObjectDownloadTimes.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return DarkVisor.from_stream(data, property_size)


def _decode_echo_visor(data: typing.BinaryIO, property_size: int):
    return EchoVisor.from_stream(data, property_size)


def _decode_scan_visor(data: typing.BinaryIO, property_size: int):
    return ScanVisor.from_stream(data, property_size)


def _decode_log_book(data: typing.BinaryIO, property_size: int):
    return LogBook.from_stream(data, property_size)


def _decode_credits(data: typing.BinaryIO, property_size: int):
    return Credits.from_stream(data, property_size)


def _decode_completion(data: typing.BinaryIO, property_size: int):
    return Completion.from_stream(data, property_size)


def _decode_movie_volumes(data: typing.BinaryIO, property_size: int):
    return MovieVolumes.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0xd45f7663: ('misc', _decode_misc),
    0x80b13e60: ('scannable_object_download_times', _decode_scannable_object_download_times),
    0x102aa38d: ('unknown', _decode_unknown),
    0x2b698e45: ('echo_visor', _decode_echo_visor),
    0x40ffb3c4: ('scan_visor', _decode_scan_visor),
    0x97b8a76a: ('log_book', _decode_log_book),
    0x77393416: ('credits', _decode_credits),
    0x2149892: ('completion', _decode_completion),
    0xa4f61e92: ('movie_volumes', _decode_movie_volumes),
}
