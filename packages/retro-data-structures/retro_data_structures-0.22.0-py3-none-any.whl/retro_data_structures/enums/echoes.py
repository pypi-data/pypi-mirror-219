"""
Generated file.
"""
import enum
import typing
import struct


class State(enum.Enum):
    NonZero = '!ZER'
    Active = 'ACTV'
    AILogicState1 = 'AIS1'
    AILogicState2 = 'AIS2'
    AILogicState3 = 'AIS3'
    Approach = 'APRC'
    Arrived = 'ARRV'
    AttachedCollisionObject = 'ATCL'
    AttachedAnimatedObject = 'ATOB'
    Attack = 'ATTK'
    BallIceXDamage = 'BIDG'
    BSCN = 'BSCN'
    BallXDamage = 'BXDG'
    Closed = 'CLOS'
    Connect = 'CONN'
    CPLR = 'CPLR'
    CameraPath = 'CPTH'
    CameraTarget = 'CTGT'
    CameraTime = 'CTIM'
    DamageAreaDark = 'DADR'
    DamageAreaLight = 'DALG'
    Damage = 'DAMG'
    DamageAnnihilator = 'DANN'
    DamageAI = 'DBAI'
    DamageBoostBall = 'DBAL'
    DamageBomb = 'DBMB'
    DamageCannonBall = 'DCAN'
    DamageCold = 'DCLD'
    DamageDark = 'DDRK'
    Dead = 'DEAD'
    DefaultState = 'DFST'
    DeGenerate = 'DGNR'
    DamageHot = 'DHOT'
    DamageLava = 'DLAV'
    DamageLight = 'DLGT'
    DamageMissile = 'DMIS'
    DamagePowerBomb = 'DPBM'
    DamagePhazon = 'DPHZ'
    DamagePower = 'DPWR'
    DamagePoisonWater = 'DPWT'
    DarkXDamage = 'DRKX'
    DamageScrewAttack = 'DSCW'
    DamageUnknownSource = 'DUNS'
    Entered = 'ENTR'
    ESCN = 'ESCN'
    Exited = 'EXIT'
    Footstep = 'FOOT'
    Freeze = 'FREZ'
    Generate = 'GRNT'
    InheritBounds = 'IBND'
    Inactive = 'ICTV'
    IceXDamage = 'IDMG'
    Inside = 'INSD'
    InternalState00 = 'IS00'
    InternalState01 = 'IS01'
    InternalState02 = 'IS02'
    InternalState03 = 'IS03'
    InternalState04 = 'IS04'
    InternalState05 = 'IS05'
    InternalState06 = 'IS06'
    InternalState07 = 'IS07'
    InternalState08 = 'IS08'
    InternalState09 = 'IS09'
    InternalState10 = 'IS10'
    InternalState11 = 'IS11'
    InternalState12 = 'IS12'
    InternalState13 = 'IS13'
    InternalState14 = 'IS14'
    InternalState15 = 'IS15'
    InternalState16 = 'IS16'
    InternalState17 = 'IS17'
    InternalState18 = 'IS18'
    InternalState19 = 'IS19'
    Left = 'LEFT'
    MaxReached = 'MAXR'
    Modify = 'MDFY'
    Open = 'OPEN'
    Play = 'PLAY'
    PressA = 'PRSA'
    PressB = 'PRSB'
    PressStart = 'PRST'
    PressX = 'PRSX'
    PressY = 'PRSY'
    PressZ = 'PRSZ'
    Patrol = 'PTRL'
    DeathRattle = 'RATL'
    SpawnResidue = 'RDUE'
    ReflectedDamage = 'REFD'
    ResistedDamage = 'RESD'
    Right = 'RGHT'
    Retreat = 'RTRT'
    ScanDone = 'SCND'
    ScanSource = 'SCNS'
    Sequence = 'SQNC'
    UnFreeze = 'UFRZ'
    Up = 'UP  '
    XDamage = 'XDMG'
    InBack = 'XINB'
    InFront = 'XINF'
    Zero = 'ZERO'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Message(enum.Enum):
    Action = 'ACTN'
    Activate = 'ACTV'
    Alert = 'ALRT'
    Arrive = 'ARRV'
    Attach = 'ATCH'
    Close = 'CLOS'
    ClearOriginator = 'CORG'
    Deactivate = 'DCTV'
    Decrement = 'DECR'
    Escape = 'ESCP'
    Follow = 'FOLW'
    InternalMessage00 = 'IM00'
    InternalMessage01 = 'IM01'
    InternalMessage02 = 'IM02'
    InternalMessage03 = 'IM03'
    InternalMessage04 = 'IM04'
    InternalMessage05 = 'IM05'
    InternalMessage06 = 'IM06'
    InternalMessage07 = 'IM07'
    InternalMessage08 = 'IM08'
    InternalMessage09 = 'IM09'
    InternalMessage10 = 'IM10'
    InternalMessage11 = 'IM11'
    InternalMessage12 = 'IM12'
    InternalMessage13 = 'IM13'
    InternalMessage14 = 'IM14'
    Increment = 'INCR'
    Kill = 'KILL'
    Left = 'LEFT'
    Load = 'LOAD'
    Lock = 'LOCK'
    Next = 'NEXT'
    Open = 'OPEN'
    Play = 'PLAY'
    Reset = 'RSET'
    ResetAndStart = 'RSTS'
    SetToMax = 'SMAX'
    SetOriginator = 'SORG'
    Stop = 'STOP'
    StopAndReset = 'STPR'
    Start = 'STRT'
    ToggleActive = 'TCTV'
    Unlock = 'ULCK'
    Unload = 'ULOD'
    XALD = 'XALD'
    XAUD = 'XAUD'
    Clear = 'XCLR'
    XCRT = 'XCRT'
    Delete = 'XDEL'
    XDamage = 'XDMG'
    XENF = 'XENF'
    XEPZ = 'XEPZ'
    XEXF = 'XEXF'
    XIPZ = 'XIPZ'
    XXPZ = 'XXPZ'
    SetToZero = 'ZERO'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class FilterShape(enum.IntEnum):
    FullScreen = 0
    FullScreenHalvesLeftRight = 1
    FullScreenHalvesTopBottom = 2
    FullScreenQuarters = 3
    CinemaBars = 4
    ScanLinesEven = 5
    ScanLinesOdd = 6
    RandomStatic = 7
    DialogBox = 8
    CinematicPlaceholderLabel = 9
    CookieCutterDepthRandomStatic = 10

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class FlagsPlayerHint(enum.IntFlag):
    Unknown1 = 1
    Unknown2 = 2
    Unknown3 = 4
    Unknown4 = 8
    Unknown5 = 16
    Unknown6 = 32
    Unknown7 = 64
    Unknown8 = 128
    Unknown9 = 256
    Unknown10 = 512
    Unknown11 = 1024
    Unknown12 = 2048
    Unknown13 = 4096
    Unknown14 = 8192
    Unknown15 = 16384
    Unknown16 = 32768
    Unknown17 = 65536
    Unknown18 = 131072
    Unknown19 = 262144
    Unknown20 = 524288
    Unknown21 = 1048576
    Unknown22 = 2097152
    Unknown23 = 4194304
    Unknown24 = 8388608

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class EnvironmentEffects(enum.IntEnum):
    _None = 0
    Snow = 1
    Rain = 2
    Bubbles = 3
    DarkWorld = 4
    Aerie = 5
    ElectricRain = 6

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class PhazonDamage(enum.IntEnum):
    _None = 0
    Blue = 1
    Orange = 2

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Function(enum.IntEnum):
    What = 0
    PlayerFollowLocator = 1
    SpinnerControllerUnused = 2
    ObjectFollowLocator = 3
    Function4Unused = 4
    InventoryActivator = 5
    MapStation = 6
    SaveStationCheckpoint = 7
    IntroBossRingControllerUnused = 8
    ViewFrustumTester = 9
    ShotSpinnerControllerUnused = 10
    EscapeSequence = 11
    BossEnergyBar = 12
    EndGame = 13
    HUDFadeInUnused = 14
    CinematicSkip = 15
    ScriptLayerControllerUnused = 16
    RainSimulatorUnused = 17
    AreaDamageUnused = 18
    ObjectFollowObject = 19
    RedundantHintSystem = 20
    DropBombUnused = 21
    Function22Unused = 22
    MissileStationUnused = 23
    BillboardUnused = 24
    PlayerInAreaRelay = 25
    HUDTargetUnused = 26
    FogFader = 27
    EnterLogbookScreenUnused = 28
    PowerBombStationUnused = 29
    Ending = 30
    FusionRelayUnused = 31
    WeaponSwitchUnused = 32
    LaunchPlayer = 33
    Function34Unused = 34
    Darkworld = 35
    Function36Unused = 36
    Function37Unused = 37
    Function38Unused = 38
    Function39Unused = 39
    SetNumPlayers___RemoveHackedEffect = 40
    EnableCannonBallDamage = 41
    ModifyInventoryAmount = 42
    IncrementDecrementPlayersJoinedCount = 43
    InventoryThing1 = 44
    InventoryThing2 = 45
    Function46Unused = 46
    AutomaticSunPlacement = 47
    Function48Unused = 48
    WipeOnOff___ = 49
    Function50Unused = 50
    InventoryLost = 51
    Function52Unused = 52
    SunGeneratorTeleporter = 53
    SkyFader = 54
    OcclusionRelay = 55
    MultiplayerCountdown = 56
    ScaleSZ = 57
    Attach___ = 58
    Function59Unused = 59
    ExtraRenderClipPlane = 60
    VisorBlowout = 61
    AreaAutoLoadController = 62
    UnlockMultiplayerMusic = 63
    EnableDarkworldAutomapperbutton = 64
    PlaySelectedMusicMultiplayer = 65
    TranslatorDoorLocation = 66
    CinematicSkipSignal = 67
    RemoveRezbitVirus = 68
    Credits = 69

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Boolean(enum.IntEnum):
    Unknown = 0
    And = 1
    Or = 2

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class AmountOrCapacity(enum.IntEnum):
    Amount = 0
    Capacity = 1

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Condition(enum.IntEnum):
    EqualTo = 0
    NotEqualTo = 1
    GreaterThan = 2
    LessThan = 3
    GreaterThanorEqualTo = 4
    LessThanorEqualTo = 5
    Unknown = 6

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class InventorySlot(enum.IntEnum):
    PowerBeam = 0
    DarkBeam = 1
    LightBeam = 2
    AnnihilatorBeam = 3
    SuperMissile = 4
    Darkburst = 5
    Sunburst = 6
    SonicBoom = 7
    CombatVisor = 8
    ScanVisor = 9
    DarkVisor = 10
    EchoVisor = 11
    VariaSuit = 12
    DarkSuit = 13
    LightSuit = 14
    MorphBall = 15
    BoostBall = 16
    SpiderBall = 17
    MorphBallBomb = 18
    ChargeBeam = 22
    GrappleBeam = 23
    SpaceJumpBoots = 24
    GravityBoost = 25
    SeekerLauncher = 26
    ScrewAttack = 27
    PowerBomb = 28
    MissileLauncher = 29
    BeamAmmoExpansion = 30
    EnergyTank = 32
    SkyTempleKey1 = 33
    SkyTempleKey2 = 34
    SkyTempleKey3 = 35
    SkyTempleKey4 = 36
    SkyTempleKey5 = 37
    SkyTempleKey6 = 38
    SkyTempleKey7 = 39
    SkyTempleKey8 = 40
    SkyTempleKey9 = 41
    DarkAgonKey1 = 42
    DarkAgonKey2 = 43
    DarkAgonKey3 = 44
    DarkTorvusKey1 = 45
    DarkTorvusKey2 = 46
    DarkTorvusKey3 = 47
    IngHiveKey1 = 48
    IngHiveKey2 = 49
    IngHiveKey3 = 50
    EnergyTransferModule = 51
    BeamCombo = 52

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class WorldLightingOptions(enum.IntEnum):
    Unknown1 = 0
    NormalWorldLighting = 1
    Unknown2 = 2
    DisableWorldLighting = 3

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class PlayerItem(enum.IntEnum):
    PowerBeam = 0
    DarkBeam = 1
    LightBeam = 2
    AnnihilatorBeam = 3
    SuperMissile = 4
    Darkburst = 5
    Sunburst = 6
    SonicBoom = 7
    CombatVisor = 8
    ScanVisor = 9
    DarkVisor = 10
    EchoVisor = 11
    VariaSuit = 12
    DarkSuit = 13
    LightSuit = 14
    MorphBall = 15
    BoostBall = 16
    SpiderBall = 17
    MorphBallBomb = 18
    LightBomb = 19
    DarkBomb = 20
    AnnihilatorBomb = 21
    ChargeBeam = 22
    GrappleBeam = 23
    SpaceJumpBoots = 24
    GravityBoost = 25
    SeekerLauncher = 26
    ScrewAttack = 27
    EnergyTransferModulePickup = 28
    SkyTempleKey1 = 29
    SkyTempleKey2 = 30
    SkyTempleKey3 = 31
    DarkAgonKey1 = 32
    DarkAgonKey2 = 33
    DarkAgonKey3 = 34
    DarkTorvusKey1 = 35
    DarkTorvusKey2 = 36
    DarkTorvusKey3 = 37
    IngHiveKey1 = 38
    IngHiveKey2 = 39
    IngHiveKey3 = 40
    HealthRefill = 41
    EnergyTank = 42
    PowerBomb = 43
    Missile = 44
    DarkAmmo = 45
    LightAmmo = 46
    ItemPercentage = 47
    NumPlayersJoined = 48
    NumPlayersInOptionsMenu = 49
    MiscCounter3 = 50
    MiscCounter4 = 51
    SwitchWeaponPower = 52
    SwitchWeaponDark = 53
    SwitchWeaponLight = 54
    SwitchWeaponAnnihilator = 55
    MultiChargeUpgrade = 56
    Invisibility = 57
    AmpDamage = 58
    Invincibility = 59
    UnknownItem60 = 60
    UnknownItem61 = 61
    UnknownItem62 = 62
    UnknownItem63 = 63
    FragCount = 64
    DiedCount = 65
    ArchenemyCount = 66
    PersistentCounter1 = 67
    PersistentCounter2 = 68
    PersistentCounter3 = 69
    PersistentCounter4 = 70
    PersistentCounter5 = 71
    PersistentCounter6 = 72
    PersistentCounter7 = 73
    PersistentCounter8 = 74
    SwitchVisorCombat = 75
    SwitchVisorScan = 76
    SwitchVisorDark = 77
    SwitchVisorEcho = 78
    CoinAmplifier = 79
    CoinCounter = 80
    UnlimitedMissiles = 81
    UnlimitedBeamAmmo = 82
    DarkShield = 83
    LightShield = 84
    AbsorbAttack = 85
    DeathBall = 86
    ScanVirus = 87
    VisorStatic = 88
    DisableBeamAmmo = 89
    DisableMissiles = 90
    DisableMorphBall = 91
    DisableBall = 92
    DisableSpaceJump = 93
    UnknownItem94 = 94
    HackedEffect = 95
    CannonBall = 96
    VioletTranslator = 97
    AmberTranslator = 98
    EmeraldTranslator = 99
    CobaltTranslator = 100
    SkyTempleKey4 = 101
    SkyTempleKey5 = 102
    SkyTempleKey6 = 103
    SkyTempleKey7 = 104
    SkyTempleKey8 = 105
    SkyTempleKey9 = 106
    EnergyTransferModuleInventory = 107
    ChargeCombo = 108

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class ScanSpeed(enum.IntEnum):
    Normal = 0
    Slow = 1

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class FlagsTrigger(enum.IntFlag):
    DetectPlayer = 1
    DetectMorphedPlayer = 2
    DetectUnmorphedPlayer = 4
    Unknown1 = 8
    Unknown2 = 16
    Unknown3 = 32
    Unknown4 = 64
    Unknown5 = 128
    Unknown6 = 256
    Unknown7 = 512
    Unknown8 = 1024
    DetectPlayer1Broken = 2048
    DetectPlayer2Broken = 4096
    DetectPlayer3Broken = 8192
    DetectPlayer4Broken = 16384
    DetectAI = 32768
    KillOnEntered = 65536
    ApplyForce = 131072
    Unknown9 = 262144
    DetectPlayerIfCompletelyInside = 524288
    BlockEnvironmentalEffects = 1048576
    DetectProjectiles = 2097152
    DetectBombs = 4194304
    Unknown10 = 8388608
    DetectBoostBall = 16777216
    SunlightMakesLumitesAppear = 33554432
    DeleteObjects = 67108864
    DetectSpiderBall = 134217728
    DetectScrewAttack = 268435456

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class VisorFlags(enum.IntFlag):
    Combat = 1
    Scan = 2
    Dark = 4
    Echo = 8

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class WeaponType(enum.IntEnum):
    Power = 0
    Dark = 1
    Light = 2
    Annihilator = 3
    Bomb = 4
    PowerBomb = 5
    Missile = 6
    BoostBall = 7
    CannonBall = 8
    ScrewAttack = 9
    Phazon = 10
    AI = 11
    PoisonWater1 = 12
    PoisonWater2 = 13
    Lava = 14
    Hot = 15
    Cold = 16
    AreaDark = 17
    AreaLight = 18
    UnknownSource = 19
    SafeZone = 20

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value


class Effect(enum.IntEnum):
    Normal = 0
    Reflect = 1
    PassThru = 2
    Immune = 3
    UnknownRumble = 4

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None):
        return cls(struct.unpack(">L", data.read(4))[0])

    def to_stream(self, data: typing.BinaryIO):
        data.write(struct.pack(">L", self.value))

    @classmethod
    def from_json(cls, data):
        return cls(data)

    def to_json(self):
        return self.value
