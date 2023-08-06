# Generated File
import functools
import typing

from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.objects.ActorAnimGridModifier import ActorAnimGridModifier
from retro_data_structures.properties.dkc_returns.objects.ActorKeyframe import ActorKeyframe
from retro_data_structures.properties.dkc_returns.objects.Acoustics import Acoustics
from retro_data_structures.properties.dkc_returns.objects.Actor import Actor
from retro_data_structures.properties.dkc_returns.objects.AreaDamage import AreaDamage
from retro_data_structures.properties.dkc_returns.objects.AIHint import AIHint
from retro_data_structures.properties.dkc_returns.objects.AIKeyframe import AIKeyframe
from retro_data_structures.properties.dkc_returns.objects.AIWaypoint import AIWaypoint
from retro_data_structures.properties.dkc_returns.objects.ActorMultiKeyFrame import ActorMultiKeyFrame
from retro_data_structures.properties.dkc_returns.objects.AudioOccluder import AudioOccluder
from retro_data_structures.properties.dkc_returns.objects.AreaNode import AreaNode
from retro_data_structures.properties.dkc_returns.objects.AreaPath import AreaPath
from retro_data_structures.properties.dkc_returns.objects.AreaStreamedAudioState import AreaStreamedAudioState
from retro_data_structures.properties.dkc_returns.objects.ActorTransform import ActorTransform
from retro_data_structures.properties.dkc_returns.objects.AVIS import AVIS
from retro_data_structures.properties.dkc_returns.objects.BarrelBalloon import BarrelBalloon
from retro_data_structures.properties.dkc_returns.objects.BarrelCannon import BarrelCannon
from retro_data_structures.properties.dkc_returns.objects.BirdBoss import BirdBoss
from retro_data_structures.properties.dkc_returns.objects.BloomEffect import BloomEffect
from retro_data_structures.properties.dkc_returns.objects.BloomVolume import BloomVolume
from retro_data_structures.properties.dkc_returns.objects.CameraBlurKeyframe import CameraBlurKeyframe
from retro_data_structures.properties.dkc_returns.objects.BonusRoom import BonusRoom
from retro_data_structures.properties.dkc_returns.objects.BouncyTire import BouncyTire
from retro_data_structures.properties.dkc_returns.objects.BeatUpHandler import BeatUpHandler
from retro_data_structures.properties.dkc_returns.objects.Cable import Cable
from retro_data_structures.properties.dkc_returns.objects.CameraHint import CameraHint
from retro_data_structures.properties.dkc_returns.objects.CameraShaker import CameraShaker
from retro_data_structures.properties.dkc_returns.objects.MineCart import MineCart
from retro_data_structures.properties.dkc_returns.objects.CinematicCamera import CinematicCamera
from retro_data_structures.properties.dkc_returns.objects.Checkpoint import Checkpoint
from retro_data_structures.properties.dkc_returns.objects.ClingPathControl import ClingPathControl
from retro_data_structures.properties.dkc_returns.objects.ColorModulate import ColorModulate
from retro_data_structures.properties.dkc_returns.objects.CameraManager import CameraManager
from retro_data_structures.properties.dkc_returns.objects.PirateCrabManager import PirateCrabManager
from retro_data_structures.properties.dkc_returns.objects.CameraModifier import CameraModifier
from retro_data_structures.properties.dkc_returns.objects.ControllerAction import ControllerAction
from retro_data_structures.properties.dkc_returns.objects.Counter import Counter
from retro_data_structures.properties.dkc_returns.objects.PirateCrab import PirateCrab
from retro_data_structures.properties.dkc_returns.objects.CreditsScreen import CreditsScreen
from retro_data_structures.properties.dkc_returns.objects.ConditionalRelay import ConditionalRelay
from retro_data_structures.properties.dkc_returns.objects.GameOverDisplay import GameOverDisplay
from retro_data_structures.properties.dkc_returns.objects.CustomInterpolation import CustomInterpolation
from retro_data_structures.properties.dkc_returns.objects.Debris import Debris
from retro_data_structures.properties.dkc_returns.objects.DistanceFog import DistanceFog
from retro_data_structures.properties.dkc_returns.objects.DynamicLight import DynamicLight
from retro_data_structures.properties.dkc_returns.objects.DamageArea import DamageArea
from retro_data_structures.properties.dkc_returns.objects.DamageEffect import DamageEffect
from retro_data_structures.properties.dkc_returns.objects.DepthOfFieldTuner import DepthOfFieldTuner
from retro_data_structures.properties.dkc_returns.objects.DamageableTrigger import DamageableTrigger
from retro_data_structures.properties.dkc_returns.objects.DamageableTriggerOrientated import DamageableTriggerOrientated
from retro_data_structures.properties.dkc_returns.objects.Effect import Effect
from retro_data_structures.properties.dkc_returns.objects.EOLDisplay import EOLDisplay
from retro_data_structures.properties.dkc_returns.objects.CameraFilterKeyframe import CameraFilterKeyframe
from retro_data_structures.properties.dkc_returns.objects.FalsePerspective import FalsePerspective
from retro_data_structures.properties.dkc_returns.objects.ForestBoss import ForestBoss
from retro_data_structures.properties.dkc_returns.objects.FogOverlay import FogOverlay
from retro_data_structures.properties.dkc_returns.objects.FogVolume import FogVolume
from retro_data_structures.properties.dkc_returns.objects.FactorySwitch import FactorySwitch
from retro_data_structures.properties.dkc_returns.objects.EnvFxDensityController import EnvFxDensityController
from retro_data_structures.properties.dkc_returns.objects.GenericCreatureGroup import GenericCreatureGroup
from retro_data_structures.properties.dkc_returns.objects.GenericCreature import GenericCreature
from retro_data_structures.properties.dkc_returns.objects.Generator import Generator
from retro_data_structures.properties.dkc_returns.objects.GameManager import GameManager
from retro_data_structures.properties.dkc_returns.objects.GuiMenu import GuiMenu
from retro_data_structures.properties.dkc_returns.objects.GeneratedObjectDeleter import GeneratedObjectDeleter
from retro_data_structures.properties.dkc_returns.objects.GroundPoundDetector import GroundPoundDetector
from retro_data_structures.properties.dkc_returns.objects.GPTR import GPTR
from retro_data_structures.properties.dkc_returns.objects.GuiSlider import GuiSlider
from retro_data_structures.properties.dkc_returns.objects.GuiCharacter import GuiCharacter
from retro_data_structures.properties.dkc_returns.objects.GuiWidget import GuiWidget
from retro_data_structures.properties.dkc_returns.objects.PlayerActionHint import PlayerActionHint
from retro_data_structures.properties.dkc_returns.objects.HUD import HUD
from retro_data_structures.properties.dkc_returns.objects.HUDProxy import HUDProxy
from retro_data_structures.properties.dkc_returns.objects.IslandHUD import IslandHUD
from retro_data_structures.properties.dkc_returns.objects.IslandArea import IslandArea
from retro_data_structures.properties.dkc_returns.objects.JungleBoss1 import JungleBoss1
from retro_data_structures.properties.dkc_returns.objects.KongProxy import KongProxy
from retro_data_structures.properties.dkc_returns.objects.Kong import Kong
from retro_data_structures.properties.dkc_returns.objects.LODController import LODController
from retro_data_structures.properties.dkc_returns.objects.LevelDarkener import LevelDarkener
from retro_data_structures.properties.dkc_returns.objects.LightVolume import LightVolume
from retro_data_structures.properties.dkc_returns.objects.MEAT import MEAT
from retro_data_structures.properties.dkc_returns.objects.MultiModelActor import MultiModelActor
from retro_data_structures.properties.dkc_returns.objects.MotionPlatform import MotionPlatform
from retro_data_structures.properties.dkc_returns.objects.MoleCart import MoleCart
from retro_data_structures.properties.dkc_returns.objects.Mole import Mole
from retro_data_structures.properties.dkc_returns.objects.MoleTrainManager import MoleTrainManager
from retro_data_structures.properties.dkc_returns.objects.StreamedMovie import StreamedMovie
from retro_data_structures.properties.dkc_returns.objects.MultiplayerSyncRelay import MultiplayerSyncRelay
from retro_data_structures.properties.dkc_returns.objects.MemoryRelay import MemoryRelay
from retro_data_structures.properties.dkc_returns.objects.MusicMaster import MusicMaster
from retro_data_structures.properties.dkc_returns.objects.MusicTrack import MusicTrack
from retro_data_structures.properties.dkc_returns.objects.OceanBridge import OceanBridge
from retro_data_structures.properties.dkc_returns.objects.OptionalAreaAsset import OptionalAreaAsset
from retro_data_structures.properties.dkc_returns.objects.PilotChicken import PilotChicken
from retro_data_structures.properties.dkc_returns.objects.Pickup import Pickup
from retro_data_structures.properties.dkc_returns.objects.PathControl import PathControl
from retro_data_structures.properties.dkc_returns.objects.PlayerActor import PlayerActor
from retro_data_structures.properties.dkc_returns.objects.Platform import Platform
from retro_data_structures.properties.dkc_returns.objects.Peanut import Peanut
from retro_data_structures.properties.dkc_returns.objects.PoiObject import PoiObject
from retro_data_structures.properties.dkc_returns.objects.ProbabilityRelay import ProbabilityRelay
from retro_data_structures.properties.dkc_returns.objects.Projectile import Projectile
from retro_data_structures.properties.dkc_returns.objects.PlayerRespawn import PlayerRespawn
from retro_data_structures.properties.dkc_returns.objects.PlayerToken import PlayerToken
from retro_data_structures.properties.dkc_returns.objects.RambiCrate import RambiCrate
from retro_data_structures.properties.dkc_returns.objects.RadialDamage import RadialDamage
from retro_data_structures.properties.dkc_returns.objects.RocketBarrel import RocketBarrel
from retro_data_structures.properties.dkc_returns.objects.RobotChicken import RobotChicken
from retro_data_structures.properties.dkc_returns.objects.RobotChickenFlyer import RobotChickenFlyer
from retro_data_structures.properties.dkc_returns.objects.ReviewControl import ReviewControl
from retro_data_structures.properties.dkc_returns.objects.AreaAttributes import AreaAttributes
from retro_data_structures.properties.dkc_returns.objects.ReactiveActor import ReactiveActor
from retro_data_structures.properties.dkc_returns.objects.Rambi import Rambi
from retro_data_structures.properties.dkc_returns.objects.SwingRope import SwingRope
from retro_data_structures.properties.dkc_returns.objects.RelayRandom import RelayRandom
from retro_data_structures.properties.dkc_returns.objects.RespawnBalloon import RespawnBalloon
from retro_data_structures.properties.dkc_returns.objects.ReactiveScale import ReactiveScale
from retro_data_structures.properties.dkc_returns.objects.Retronome import Retronome
from retro_data_structures.properties.dkc_returns.objects.RumbleEffect import RumbleEffect
from retro_data_structures.properties.dkc_returns.objects.MusicModifier import MusicModifier
from retro_data_structures.properties.dkc_returns.objects.SkyboxModInca import SkyboxModInca
from retro_data_structures.properties.dkc_returns.objects.SurfaceControl import SurfaceControl
from retro_data_structures.properties.dkc_returns.objects.ShadowProjector import ShadowProjector
from retro_data_structures.properties.dkc_returns.objects.ScriptLayerController import ScriptLayerController
from retro_data_structures.properties.dkc_returns.objects.SoundModifier import SoundModifier
from retro_data_structures.properties.dkc_returns.objects.SoundModifierData import SoundModifierData
from retro_data_structures.properties.dkc_returns.objects.Sound import Sound
from retro_data_structures.properties.dkc_returns.objects.SpecialFunction import SpecialFunction
from retro_data_structures.properties.dkc_returns.objects.Spinner import Spinner
from retro_data_structures.properties.dkc_returns.objects.SplinePathNetwork import SplinePathNetwork
from retro_data_structures.properties.dkc_returns.objects.SplinePath import SplinePath
from retro_data_structures.properties.dkc_returns.objects.PositionRelay import PositionRelay
from retro_data_structures.properties.dkc_returns.objects.SpawnPoint import SpawnPoint
from retro_data_structures.properties.dkc_returns.objects.SequenceTimer import SequenceTimer
from retro_data_structures.properties.dkc_returns.objects.Relay import Relay
from retro_data_structures.properties.dkc_returns.objects.StreamedAudio import StreamedAudio
from retro_data_structures.properties.dkc_returns.objects.Subtitles import Subtitles
from retro_data_structures.properties.dkc_returns.objects.SuspensionBridge import SuspensionBridge
from retro_data_structures.properties.dkc_returns.objects.SplineModifierVolume import SplineModifierVolume
from retro_data_structures.properties.dkc_returns.objects.SquawkProxy import SquawkProxy
from retro_data_structures.properties.dkc_returns.objects.Switch import Switch
from retro_data_structures.properties.dkc_returns.objects.TarPit import TarPit
from retro_data_structures.properties.dkc_returns.objects.TimeAttackEOLDisplay import TimeAttackEOLDisplay
from retro_data_structures.properties.dkc_returns.objects.TidalWave import TidalWave
from retro_data_structures.properties.dkc_returns.objects.Timer import Timer
from retro_data_structures.properties.dkc_returns.objects.TippyPlatform import TippyPlatform
from retro_data_structures.properties.dkc_returns.objects.TimeKeyframe import TimeKeyframe
from retro_data_structures.properties.dkc_returns.objects.TrainTrackManager import TrainTrackManager
from retro_data_structures.properties.dkc_returns.objects.TPND import TPND
from retro_data_structures.properties.dkc_returns.objects.Trigger import Trigger
from retro_data_structures.properties.dkc_returns.objects.TransitionScreen import TransitionScreen
from retro_data_structures.properties.dkc_returns.objects.TrainSequence import TrainSequence
from retro_data_structures.properties.dkc_returns.objects.Tutorial import Tutorial
from retro_data_structures.properties.dkc_returns.objects.TextPane import TextPane
from retro_data_structures.properties.dkc_returns.objects.VolcanoBossBodyPart import VolcanoBossBodyPart
from retro_data_structures.properties.dkc_returns.objects.VolumeGroup import VolumeGroup
from retro_data_structures.properties.dkc_returns.objects.VerticalRocketBarrel import VerticalRocketBarrel
from retro_data_structures.properties.dkc_returns.objects.OceanWave import OceanWave
from retro_data_structures.properties.dkc_returns.objects.Waypoint import Waypoint
from retro_data_structures.properties.dkc_returns.objects.WorldAttributes import WorldAttributes
from retro_data_structures.properties.dkc_returns.objects.WorldLightFader import WorldLightFader

_FOUR_CC_MAPPING = {
    'AAGM': ActorAnimGridModifier,
    'ACKF': ActorKeyframe,
    'ACOU': Acoustics,
    'ACTR': Actor,
    'ADMG': AreaDamage,
    'AIHT': AIHint,
    'AIKF': AIKeyframe,
    'AIWP': AIWaypoint,
    'AMKF': ActorMultiKeyFrame,
    'AOCL': AudioOccluder,
    'ARNO': AreaNode,
    'ARPA': AreaPath,
    'ASAS': AreaStreamedAudioState,
    'ATRN': ActorTransform,
    'AVIS': AVIS,
    'BABL': BarrelBalloon,
    'BARL': BarrelCannon,
    'BIRD': BirdBoss,
    'BLME': BloomEffect,
    'BLMV': BloomVolume,
    'BLUR': CameraBlurKeyframe,
    'BONU': BonusRoom,
    'BTYR': BouncyTire,
    'BUHA': BeatUpHandler,
    'CABL': Cable,
    'CAMH': CameraHint,
    'CAMS': CameraShaker,
    'CART': MineCart,
    'CINE': CinematicCamera,
    'CKPT': Checkpoint,
    'CLPC': ClingPathControl,
    'CLRM': ColorModulate,
    'CMAN': CameraManager,
    'CMGR': PirateCrabManager,
    'CMOD': CameraModifier,
    'CNTA': ControllerAction,
    'CNTR': Counter,
    'CRAB': PirateCrab,
    'CRED': CreditsScreen,
    'CRLY': ConditionalRelay,
    'CSGO': GameOverDisplay,
    'CSTI': CustomInterpolation,
    'DEBR': Debris,
    'DFOG': DistanceFog,
    'DLHT': DynamicLight,
    'DMGA': DamageArea,
    'DMGE': DamageEffect,
    'DOFT': DepthOfFieldTuner,
    'DTRG': DamageableTrigger,
    'DTRO': DamageableTriggerOrientated,
    'EFCT': Effect,
    'EOLD': EOLDisplay,
    'FILT': CameraFilterKeyframe,
    'FLPS': FalsePerspective,
    'FOBS': ForestBoss,
    'FOGO': FogOverlay,
    'FOGV': FogVolume,
    'FSWC': FactorySwitch,
    'FXDC': EnvFxDensityController,
    'GCGP': GenericCreatureGroup,
    'GCTR': GenericCreature,
    'GENR': Generator,
    'GMGR': GameManager,
    'GMNU': GuiMenu,
    'GOBD': GeneratedObjectDeleter,
    'GPDT': GroundPoundDetector,
    'GPTR': GPTR,
    'GSLD': GuiSlider,
    'GUCH': GuiCharacter,
    'GWIG': GuiWidget,
    'HINT': PlayerActionHint,
    'HUDD': HUD,
    'HUDP': HUDProxy,
    'IHUD': IslandHUD,
    'ISAR': IslandArea,
    'JB01': JungleBoss1,
    'KNGP': KongProxy,
    'KONG': Kong,
    'LODC': LODController,
    'LVLD': LevelDarkener,
    'LVOL': LightVolume,
    'MEAT': MEAT,
    'MMDL': MultiModelActor,
    'MNPL': MotionPlatform,
    'MOLC': MoleCart,
    'MOLE': Mole,
    'MOLM': MoleTrainManager,
    'MOVI': StreamedMovie,
    'MPSR': MultiplayerSyncRelay,
    'MRLY': MemoryRelay,
    'MUMA': MusicMaster,
    'MUTR': MusicTrack,
    'OBRG': OceanBridge,
    'OPAA': OptionalAreaAsset,
    'PCHK': PilotChicken,
    'PCKP': Pickup,
    'PCTL': PathControl,
    'PLAC': PlayerActor,
    'PLAT': Platform,
    'PNUT': Peanut,
    'POIO': PoiObject,
    'PRLA': ProbabilityRelay,
    'PROJ': Projectile,
    'PRSP': PlayerRespawn,
    'PTOK': PlayerToken,
    'RACR': RambiCrate,
    'RADD': RadialDamage,
    'RBRL': RocketBarrel,
    'RCHK': RobotChicken,
    'RCKF': RobotChickenFlyer,
    'RCTL': ReviewControl,
    'REAA': AreaAttributes,
    'REAC': ReactiveActor,
    'RMBI': Rambi,
    'ROPE': SwingRope,
    'RRLY': RelayRandom,
    'RSBL': RespawnBalloon,
    'RSCL': ReactiveScale,
    'RTNM': Retronome,
    'RUMB': RumbleEffect,
    'SAMD': MusicModifier,
    'SBMI': SkyboxModInca,
    'SCTL': SurfaceControl,
    'SHDW': ShadowProjector,
    'SLCT': ScriptLayerController,
    'SNDM': SoundModifier,
    'SNMD': SoundModifierData,
    'SOND': Sound,
    'SPFN': SpecialFunction,
    'SPIN': Spinner,
    'SPNW': SplinePathNetwork,
    'SPPA': SplinePath,
    'SPRL': PositionRelay,
    'SPWN': SpawnPoint,
    'SQTR': SequenceTimer,
    'SRLY': Relay,
    'STAU': StreamedAudio,
    'SUBT': Subtitles,
    'SUSP': SuspensionBridge,
    'SVOL': SplineModifierVolume,
    'SWKP': SquawkProxy,
    'SWTC': Switch,
    'TARP': TarPit,
    'TEOL': TimeAttackEOLDisplay,
    'TIDE': TidalWave,
    'TIMR': Timer,
    'TIPI': TippyPlatform,
    'TKEY': TimeKeyframe,
    'TMGR': TrainTrackManager,
    'TPND': TPND,
    'TRGR': Trigger,
    'TRSC': TransitionScreen,
    'TSEQ': TrainSequence,
    'TUTR': Tutorial,
    'TXPN': TextPane,
    'VBPT': VolcanoBossBodyPart,
    'VOLG': VolumeGroup,
    'VRBR': VerticalRocketBarrel,
    'WAVE': OceanWave,
    'WAYP': Waypoint,
    'WLDA': WorldAttributes,
    'WLIT': WorldLightFader,
}


@functools.lru_cache(maxsize=None)
def get_object(four_cc: str) -> typing.Type[BaseObjectType]:
    return _FOUR_CC_MAPPING[four_cc]
