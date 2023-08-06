# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.TrainTrackManagerStructB import TrainTrackManagerStructB


@dataclasses.dataclass()
class UnknownStruct275(BaseProperty):
    unknown: int = dataclasses.field(default=0)
    train_track_manager_struct_b_0xfc8fbdb7: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x2f14a14c: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x619daae5: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x53539efb: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x1dda9552: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xce4189a9: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x80c88200: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xabdde195: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xe554ea3c: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x61e5d2a4: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x2f6cd90d: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xfcf7c5f6: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xb27ece5f: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x80b0fa41: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xce39f1e8: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x1da2ed13: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x532be6ba: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x783e852f: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x36b78e86: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x4b59622c: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x05d06985: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xd64b757e: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x98c27ed7: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xaa0c4ac9: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xe4854160: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x371e5d9b: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x79975632: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x528235a7: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x1c0b3e0e: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xe41df06b: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0xaa94fbc2: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)
    train_track_manager_struct_b_0x790fe739: TrainTrackManagerStructB = dataclasses.field(default_factory=TrainTrackManagerStructB)

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
        data.write(b'\x00!')  # 33 properties

        data.write(b'\x979^\xea')  # 0x97395eea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xfc\x8f\xbd\xb7')  # 0xfc8fbdb7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xfc8fbdb7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/\x14\xa1L')  # 0x2f14a14c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x2f14a14c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\x9d\xaa\xe5')  # 0x619daae5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x619daae5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'SS\x9e\xfb')  # 0x53539efb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x53539efb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\xda\x95R')  # 0x1dda9552
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x1dda9552.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xceA\x89\xa9')  # 0xce4189a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xce4189a9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xc8\x82\x00')  # 0x80c88200
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x80c88200.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab\xdd\xe1\x95')  # 0xabdde195
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xabdde195.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5T\xea<')  # 0xe554ea3c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xe554ea3c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\xe5\xd2\xa4')  # 0x61e5d2a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x61e5d2a4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/l\xd9\r')  # 0x2f6cd90d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x2f6cd90d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\xf7\xc5\xf6')  # 0xfcf7c5f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xfcf7c5f6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2~\xce_')  # 0xb27ece5f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xb27ece5f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xb0\xfaA')  # 0x80b0fa41
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x80b0fa41.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xce9\xf1\xe8')  # 0xce39f1e8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xce39f1e8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\xa2\xed\x13')  # 0x1da2ed13
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x1da2ed13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S+\xe6\xba')  # 0x532be6ba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x532be6ba.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x>\x85/')  # 0x783e852f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x783e852f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xb7\x8e\x86')  # 0x36b78e86
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x36b78e86.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'KYb,')  # 0x4b59622c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x4b59622c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05\xd0i\x85')  # 0x5d06985
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x05d06985.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6Ku~')  # 0xd64b757e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xd64b757e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xc2~\xd7')  # 0x98c27ed7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x98c27ed7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\x0cJ\xc9')  # 0xaa0c4ac9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xaa0c4ac9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4\x85A`')  # 0xe4854160
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xe4854160.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\x1e]\x9b')  # 0x371e5d9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x371e5d9b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x97V2')  # 0x79975632
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x79975632.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'R\x825\xa7')  # 0x528235a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x528235a7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\x0b>\x0e')  # 0x1c0b3e0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x1c0b3e0e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4\x1d\xf0k')  # 0xe41df06b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xe41df06b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\x94\xfb\xc2')  # 0xaa94fbc2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0xaa94fbc2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x0f\xe79')  # 0x790fe739
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_b_0x790fe739.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            train_track_manager_struct_b_0xfc8fbdb7=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xfc8fbdb7']),
            train_track_manager_struct_b_0x2f14a14c=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x2f14a14c']),
            train_track_manager_struct_b_0x619daae5=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x619daae5']),
            train_track_manager_struct_b_0x53539efb=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x53539efb']),
            train_track_manager_struct_b_0x1dda9552=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x1dda9552']),
            train_track_manager_struct_b_0xce4189a9=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xce4189a9']),
            train_track_manager_struct_b_0x80c88200=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x80c88200']),
            train_track_manager_struct_b_0xabdde195=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xabdde195']),
            train_track_manager_struct_b_0xe554ea3c=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xe554ea3c']),
            train_track_manager_struct_b_0x61e5d2a4=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x61e5d2a4']),
            train_track_manager_struct_b_0x2f6cd90d=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x2f6cd90d']),
            train_track_manager_struct_b_0xfcf7c5f6=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xfcf7c5f6']),
            train_track_manager_struct_b_0xb27ece5f=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xb27ece5f']),
            train_track_manager_struct_b_0x80b0fa41=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x80b0fa41']),
            train_track_manager_struct_b_0xce39f1e8=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xce39f1e8']),
            train_track_manager_struct_b_0x1da2ed13=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x1da2ed13']),
            train_track_manager_struct_b_0x532be6ba=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x532be6ba']),
            train_track_manager_struct_b_0x783e852f=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x783e852f']),
            train_track_manager_struct_b_0x36b78e86=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x36b78e86']),
            train_track_manager_struct_b_0x4b59622c=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x4b59622c']),
            train_track_manager_struct_b_0x05d06985=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x05d06985']),
            train_track_manager_struct_b_0xd64b757e=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xd64b757e']),
            train_track_manager_struct_b_0x98c27ed7=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x98c27ed7']),
            train_track_manager_struct_b_0xaa0c4ac9=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xaa0c4ac9']),
            train_track_manager_struct_b_0xe4854160=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xe4854160']),
            train_track_manager_struct_b_0x371e5d9b=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x371e5d9b']),
            train_track_manager_struct_b_0x79975632=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x79975632']),
            train_track_manager_struct_b_0x528235a7=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x528235a7']),
            train_track_manager_struct_b_0x1c0b3e0e=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x1c0b3e0e']),
            train_track_manager_struct_b_0xe41df06b=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xe41df06b']),
            train_track_manager_struct_b_0xaa94fbc2=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0xaa94fbc2']),
            train_track_manager_struct_b_0x790fe739=TrainTrackManagerStructB.from_json(data['train_track_manager_struct_b_0x790fe739']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'train_track_manager_struct_b_0xfc8fbdb7': self.train_track_manager_struct_b_0xfc8fbdb7.to_json(),
            'train_track_manager_struct_b_0x2f14a14c': self.train_track_manager_struct_b_0x2f14a14c.to_json(),
            'train_track_manager_struct_b_0x619daae5': self.train_track_manager_struct_b_0x619daae5.to_json(),
            'train_track_manager_struct_b_0x53539efb': self.train_track_manager_struct_b_0x53539efb.to_json(),
            'train_track_manager_struct_b_0x1dda9552': self.train_track_manager_struct_b_0x1dda9552.to_json(),
            'train_track_manager_struct_b_0xce4189a9': self.train_track_manager_struct_b_0xce4189a9.to_json(),
            'train_track_manager_struct_b_0x80c88200': self.train_track_manager_struct_b_0x80c88200.to_json(),
            'train_track_manager_struct_b_0xabdde195': self.train_track_manager_struct_b_0xabdde195.to_json(),
            'train_track_manager_struct_b_0xe554ea3c': self.train_track_manager_struct_b_0xe554ea3c.to_json(),
            'train_track_manager_struct_b_0x61e5d2a4': self.train_track_manager_struct_b_0x61e5d2a4.to_json(),
            'train_track_manager_struct_b_0x2f6cd90d': self.train_track_manager_struct_b_0x2f6cd90d.to_json(),
            'train_track_manager_struct_b_0xfcf7c5f6': self.train_track_manager_struct_b_0xfcf7c5f6.to_json(),
            'train_track_manager_struct_b_0xb27ece5f': self.train_track_manager_struct_b_0xb27ece5f.to_json(),
            'train_track_manager_struct_b_0x80b0fa41': self.train_track_manager_struct_b_0x80b0fa41.to_json(),
            'train_track_manager_struct_b_0xce39f1e8': self.train_track_manager_struct_b_0xce39f1e8.to_json(),
            'train_track_manager_struct_b_0x1da2ed13': self.train_track_manager_struct_b_0x1da2ed13.to_json(),
            'train_track_manager_struct_b_0x532be6ba': self.train_track_manager_struct_b_0x532be6ba.to_json(),
            'train_track_manager_struct_b_0x783e852f': self.train_track_manager_struct_b_0x783e852f.to_json(),
            'train_track_manager_struct_b_0x36b78e86': self.train_track_manager_struct_b_0x36b78e86.to_json(),
            'train_track_manager_struct_b_0x4b59622c': self.train_track_manager_struct_b_0x4b59622c.to_json(),
            'train_track_manager_struct_b_0x05d06985': self.train_track_manager_struct_b_0x05d06985.to_json(),
            'train_track_manager_struct_b_0xd64b757e': self.train_track_manager_struct_b_0xd64b757e.to_json(),
            'train_track_manager_struct_b_0x98c27ed7': self.train_track_manager_struct_b_0x98c27ed7.to_json(),
            'train_track_manager_struct_b_0xaa0c4ac9': self.train_track_manager_struct_b_0xaa0c4ac9.to_json(),
            'train_track_manager_struct_b_0xe4854160': self.train_track_manager_struct_b_0xe4854160.to_json(),
            'train_track_manager_struct_b_0x371e5d9b': self.train_track_manager_struct_b_0x371e5d9b.to_json(),
            'train_track_manager_struct_b_0x79975632': self.train_track_manager_struct_b_0x79975632.to_json(),
            'train_track_manager_struct_b_0x528235a7': self.train_track_manager_struct_b_0x528235a7.to_json(),
            'train_track_manager_struct_b_0x1c0b3e0e': self.train_track_manager_struct_b_0x1c0b3e0e.to_json(),
            'train_track_manager_struct_b_0xe41df06b': self.train_track_manager_struct_b_0xe41df06b.to_json(),
            'train_track_manager_struct_b_0xaa94fbc2': self.train_track_manager_struct_b_0xaa94fbc2.to_json(),
            'train_track_manager_struct_b_0x790fe739': self.train_track_manager_struct_b_0x790fe739.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_train_track_manager_struct_b_0xfc8fbdb7(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x2f14a14c(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x619daae5(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x53539efb(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x1dda9552(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xce4189a9(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x80c88200(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xabdde195(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xe554ea3c(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x61e5d2a4(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x2f6cd90d(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xfcf7c5f6(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xb27ece5f(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x80b0fa41(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xce39f1e8(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x1da2ed13(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x532be6ba(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x783e852f(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x36b78e86(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x4b59622c(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x05d06985(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xd64b757e(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x98c27ed7(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xaa0c4ac9(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xe4854160(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x371e5d9b(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x79975632(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x528235a7(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x1c0b3e0e(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xe41df06b(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0xaa94fbc2(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


def _decode_train_track_manager_struct_b_0x790fe739(data: typing.BinaryIO, property_size: int):
    return TrainTrackManagerStructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97395eea: ('unknown', _decode_unknown),
    0xfc8fbdb7: ('train_track_manager_struct_b_0xfc8fbdb7', _decode_train_track_manager_struct_b_0xfc8fbdb7),
    0x2f14a14c: ('train_track_manager_struct_b_0x2f14a14c', _decode_train_track_manager_struct_b_0x2f14a14c),
    0x619daae5: ('train_track_manager_struct_b_0x619daae5', _decode_train_track_manager_struct_b_0x619daae5),
    0x53539efb: ('train_track_manager_struct_b_0x53539efb', _decode_train_track_manager_struct_b_0x53539efb),
    0x1dda9552: ('train_track_manager_struct_b_0x1dda9552', _decode_train_track_manager_struct_b_0x1dda9552),
    0xce4189a9: ('train_track_manager_struct_b_0xce4189a9', _decode_train_track_manager_struct_b_0xce4189a9),
    0x80c88200: ('train_track_manager_struct_b_0x80c88200', _decode_train_track_manager_struct_b_0x80c88200),
    0xabdde195: ('train_track_manager_struct_b_0xabdde195', _decode_train_track_manager_struct_b_0xabdde195),
    0xe554ea3c: ('train_track_manager_struct_b_0xe554ea3c', _decode_train_track_manager_struct_b_0xe554ea3c),
    0x61e5d2a4: ('train_track_manager_struct_b_0x61e5d2a4', _decode_train_track_manager_struct_b_0x61e5d2a4),
    0x2f6cd90d: ('train_track_manager_struct_b_0x2f6cd90d', _decode_train_track_manager_struct_b_0x2f6cd90d),
    0xfcf7c5f6: ('train_track_manager_struct_b_0xfcf7c5f6', _decode_train_track_manager_struct_b_0xfcf7c5f6),
    0xb27ece5f: ('train_track_manager_struct_b_0xb27ece5f', _decode_train_track_manager_struct_b_0xb27ece5f),
    0x80b0fa41: ('train_track_manager_struct_b_0x80b0fa41', _decode_train_track_manager_struct_b_0x80b0fa41),
    0xce39f1e8: ('train_track_manager_struct_b_0xce39f1e8', _decode_train_track_manager_struct_b_0xce39f1e8),
    0x1da2ed13: ('train_track_manager_struct_b_0x1da2ed13', _decode_train_track_manager_struct_b_0x1da2ed13),
    0x532be6ba: ('train_track_manager_struct_b_0x532be6ba', _decode_train_track_manager_struct_b_0x532be6ba),
    0x783e852f: ('train_track_manager_struct_b_0x783e852f', _decode_train_track_manager_struct_b_0x783e852f),
    0x36b78e86: ('train_track_manager_struct_b_0x36b78e86', _decode_train_track_manager_struct_b_0x36b78e86),
    0x4b59622c: ('train_track_manager_struct_b_0x4b59622c', _decode_train_track_manager_struct_b_0x4b59622c),
    0x5d06985: ('train_track_manager_struct_b_0x05d06985', _decode_train_track_manager_struct_b_0x05d06985),
    0xd64b757e: ('train_track_manager_struct_b_0xd64b757e', _decode_train_track_manager_struct_b_0xd64b757e),
    0x98c27ed7: ('train_track_manager_struct_b_0x98c27ed7', _decode_train_track_manager_struct_b_0x98c27ed7),
    0xaa0c4ac9: ('train_track_manager_struct_b_0xaa0c4ac9', _decode_train_track_manager_struct_b_0xaa0c4ac9),
    0xe4854160: ('train_track_manager_struct_b_0xe4854160', _decode_train_track_manager_struct_b_0xe4854160),
    0x371e5d9b: ('train_track_manager_struct_b_0x371e5d9b', _decode_train_track_manager_struct_b_0x371e5d9b),
    0x79975632: ('train_track_manager_struct_b_0x79975632', _decode_train_track_manager_struct_b_0x79975632),
    0x528235a7: ('train_track_manager_struct_b_0x528235a7', _decode_train_track_manager_struct_b_0x528235a7),
    0x1c0b3e0e: ('train_track_manager_struct_b_0x1c0b3e0e', _decode_train_track_manager_struct_b_0x1c0b3e0e),
    0xe41df06b: ('train_track_manager_struct_b_0xe41df06b', _decode_train_track_manager_struct_b_0xe41df06b),
    0xaa94fbc2: ('train_track_manager_struct_b_0xaa94fbc2', _decode_train_track_manager_struct_b_0xaa94fbc2),
    0x790fe739: ('train_track_manager_struct_b_0x790fe739', _decode_train_track_manager_struct_b_0x790fe739),
}
