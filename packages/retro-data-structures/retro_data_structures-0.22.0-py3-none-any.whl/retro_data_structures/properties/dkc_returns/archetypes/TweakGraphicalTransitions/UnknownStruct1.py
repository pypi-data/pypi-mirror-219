# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.TweakGraphicalTransitions.UnknownStruct2 import UnknownStruct2
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    background: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    tiki_face: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    time_attack_stop_watch: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    black_screen: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    swirl: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    start_mask: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    end_mask: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    balloon_board: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    text_font_name: str = dataclasses.field(default='')
    text_gradient_start_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    text_gradient_end_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    text_decrement_time: float = dataclasses.field(default=1.0)
    text_pos_x: float = dataclasses.field(default=0.0)
    text_pos_y: float = dataclasses.field(default=0.0)
    model_camera_pos: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model_look_at_pos: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    balloon_start_pos: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    super_guide_dk_start_pos: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    super_guide_anim_delay: float = dataclasses.field(default=0.0)
    balloon_velocity: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    quit_button_position: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    game_over_text_pos: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    button_text_locator: str = dataclasses.field(default='')

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
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'x\xa6\x16G')  # 0x78a61647
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.background.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\xeaLd')  # 0x8dea4c64
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tiki_face.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9\xda\xfd\xc8')  # 0xb9dafdc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.time_attack_stop_watch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd\xc6\xc0<')  # 0x64c6c03c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.black_screen.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'4yz ')  # 0x34797a20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swirl.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6\x81\xd6U')  # 0xa681d655
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.start_mask.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\x0c\x91\x1d')  # 0x930c911d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.end_mask.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[vb\xce')  # 0x5b7662ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balloon_board.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9k\xa9J')  # 0xc96ba94a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.text_font_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xe0\xd0\xfb')  # 0xf9e0d0fb
        data.write(b'\x00\x10')  # size
        self.text_gradient_start_color.to_stream(data)

        data.write(b'\xe0A~\x89')  # 0xe0417e89
        data.write(b'\x00\x10')  # size
        self.text_gradient_end_color.to_stream(data)

        data.write(b'\xf2\xe15\x06')  # 0xf2e13506
        data.write(b'\x00\x10')  # size
        self.text_outline_color.to_stream(data)

        data.write(b'\x9c\xd3]i')  # 0x9cd35d69
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_decrement_time))

        data.write(b'{Is\x13')  # 0x7b497313
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_pos_x))

        data.write(b'\xb0\x15\xa0\xb6')  # 0xb015a0b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_pos_y))

        data.write(b'\x0e\xd3\xbb\xa6')  # 0xed3bba6
        data.write(b'\x00\x0c')  # size
        self.model_camera_pos.to_stream(data)

        data.write(b'h\xa2,_')  # 0x68a22c5f
        data.write(b'\x00\x0c')  # size
        self.model_look_at_pos.to_stream(data)

        data.write(b'\xf9n\x96\xa8')  # 0xf96e96a8
        data.write(b'\x00\x0c')  # size
        self.balloon_start_pos.to_stream(data)

        data.write(b'\xb65\xe8\xb7')  # 0xb635e8b7
        data.write(b'\x00\x0c')  # size
        self.super_guide_dk_start_pos.to_stream(data)

        data.write(b'ji\xaa\x8c')  # 0x6a69aa8c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.super_guide_anim_delay))

        data.write(b'-\xd0\x91\x93')  # 0x2dd09193
        data.write(b'\x00\x0c')  # size
        self.balloon_velocity.to_stream(data)

        data.write(b'\xbd]#\x95')  # 0xbd5d2395
        data.write(b'\x00\x0c')  # size
        self.quit_button_position.to_stream(data)

        data.write(b'\x92\x1b\x9c\xdc')  # 0x921b9cdc
        data.write(b'\x00\x0c')  # size
        self.game_over_text_pos.to_stream(data)

        data.write(b'\x92\xbe\x12\xe9')  # 0x92be12e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.button_text_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            background=UnknownStruct2.from_json(data['background']),
            tiki_face=UnknownStruct2.from_json(data['tiki_face']),
            time_attack_stop_watch=UnknownStruct2.from_json(data['time_attack_stop_watch']),
            black_screen=UnknownStruct2.from_json(data['black_screen']),
            swirl=UnknownStruct2.from_json(data['swirl']),
            start_mask=UnknownStruct2.from_json(data['start_mask']),
            end_mask=UnknownStruct2.from_json(data['end_mask']),
            balloon_board=UnknownStruct2.from_json(data['balloon_board']),
            text_font_name=data['text_font_name'],
            text_gradient_start_color=Color.from_json(data['text_gradient_start_color']),
            text_gradient_end_color=Color.from_json(data['text_gradient_end_color']),
            text_outline_color=Color.from_json(data['text_outline_color']),
            text_decrement_time=data['text_decrement_time'],
            text_pos_x=data['text_pos_x'],
            text_pos_y=data['text_pos_y'],
            model_camera_pos=Vector.from_json(data['model_camera_pos']),
            model_look_at_pos=Vector.from_json(data['model_look_at_pos']),
            balloon_start_pos=Vector.from_json(data['balloon_start_pos']),
            super_guide_dk_start_pos=Vector.from_json(data['super_guide_dk_start_pos']),
            super_guide_anim_delay=data['super_guide_anim_delay'],
            balloon_velocity=Vector.from_json(data['balloon_velocity']),
            quit_button_position=Vector.from_json(data['quit_button_position']),
            game_over_text_pos=Vector.from_json(data['game_over_text_pos']),
            button_text_locator=data['button_text_locator'],
        )

    def to_json(self) -> dict:
        return {
            'background': self.background.to_json(),
            'tiki_face': self.tiki_face.to_json(),
            'time_attack_stop_watch': self.time_attack_stop_watch.to_json(),
            'black_screen': self.black_screen.to_json(),
            'swirl': self.swirl.to_json(),
            'start_mask': self.start_mask.to_json(),
            'end_mask': self.end_mask.to_json(),
            'balloon_board': self.balloon_board.to_json(),
            'text_font_name': self.text_font_name,
            'text_gradient_start_color': self.text_gradient_start_color.to_json(),
            'text_gradient_end_color': self.text_gradient_end_color.to_json(),
            'text_outline_color': self.text_outline_color.to_json(),
            'text_decrement_time': self.text_decrement_time,
            'text_pos_x': self.text_pos_x,
            'text_pos_y': self.text_pos_y,
            'model_camera_pos': self.model_camera_pos.to_json(),
            'model_look_at_pos': self.model_look_at_pos.to_json(),
            'balloon_start_pos': self.balloon_start_pos.to_json(),
            'super_guide_dk_start_pos': self.super_guide_dk_start_pos.to_json(),
            'super_guide_anim_delay': self.super_guide_anim_delay,
            'balloon_velocity': self.balloon_velocity.to_json(),
            'quit_button_position': self.quit_button_position.to_json(),
            'game_over_text_pos': self.game_over_text_pos.to_json(),
            'button_text_locator': self.button_text_locator,
        }


def _decode_background(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_tiki_face(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_time_attack_stop_watch(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_black_screen(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_swirl(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_start_mask(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_end_mask(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_balloon_board(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_text_font_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_text_gradient_start_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_gradient_end_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_decrement_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_pos_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_pos_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model_camera_pos(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model_look_at_pos(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_balloon_start_pos(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_super_guide_dk_start_pos(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_super_guide_anim_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_balloon_velocity(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_quit_button_position(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_game_over_text_pos(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_button_text_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x78a61647: ('background', _decode_background),
    0x8dea4c64: ('tiki_face', _decode_tiki_face),
    0xb9dafdc8: ('time_attack_stop_watch', _decode_time_attack_stop_watch),
    0x64c6c03c: ('black_screen', _decode_black_screen),
    0x34797a20: ('swirl', _decode_swirl),
    0xa681d655: ('start_mask', _decode_start_mask),
    0x930c911d: ('end_mask', _decode_end_mask),
    0x5b7662ce: ('balloon_board', _decode_balloon_board),
    0xc96ba94a: ('text_font_name', _decode_text_font_name),
    0xf9e0d0fb: ('text_gradient_start_color', _decode_text_gradient_start_color),
    0xe0417e89: ('text_gradient_end_color', _decode_text_gradient_end_color),
    0xf2e13506: ('text_outline_color', _decode_text_outline_color),
    0x9cd35d69: ('text_decrement_time', _decode_text_decrement_time),
    0x7b497313: ('text_pos_x', _decode_text_pos_x),
    0xb015a0b6: ('text_pos_y', _decode_text_pos_y),
    0xed3bba6: ('model_camera_pos', _decode_model_camera_pos),
    0x68a22c5f: ('model_look_at_pos', _decode_model_look_at_pos),
    0xf96e96a8: ('balloon_start_pos', _decode_balloon_start_pos),
    0xb635e8b7: ('super_guide_dk_start_pos', _decode_super_guide_dk_start_pos),
    0x6a69aa8c: ('super_guide_anim_delay', _decode_super_guide_anim_delay),
    0x2dd09193: ('balloon_velocity', _decode_balloon_velocity),
    0xbd5d2395: ('quit_button_position', _decode_quit_button_position),
    0x921b9cdc: ('game_over_text_pos', _decode_game_over_text_pos),
    0x92be12e9: ('button_text_locator', _decode_button_text_locator),
}
