# pylint: disable=duplicate-code
from enum import Enum

class Emote(Enum):
    NORMAL: int = 0
    PAIN: int = 1
    HAPPY: int = 2
    SURPRISE: int = 3
    ANGRY: int = 4
    BLINK: int = 5

class Powerup(Enum):
    HEALTH: int = 0
    ARMOR: int = 1
    WEAPON: int = 2
    NINJA: int = 3

class Emoticon(Enum):
    OOP: int = 0
    EXCLAMATION: int = 1
    HEARTS: int = 2
    DROP: int = 3
    DOTDOT: int = 4
    MUSIC: int = 5
    SORRY: int = 6
    GHOST: int = 7
    SUSHI: int = 8
    SPLATTEE: int = 9
    DEVILTEE: int = 10
    ZOMG: int = 11
    ZZZ: int = 12
    WTF: int = 13
    EYES: int = 14
    QUESTION: int = 15

class Weapon(Enum):
    HAMMER: int = 0
    PISTOL: int = 1
    SHOTGUN: int = 2
    GRENADE: int = 3
    RIFLE: int = 4
    NINJA: int = 5

class Team(Enum):
    SPECTATORS: int = -1
    RED: int = 0
    BLUE: int = 1

class Sound(Enum):
    GUN_FIRE: int = 0
    SHOTGUN_FIRE: int = 1
    GRENADE_FIRE: int = 2
    HAMMER_FIRE: int = 3
    HAMMER_HIT: int = 4
    NINJA_FIRE: int = 5
    GRENADE_EXPLODE: int = 6
    NINJA_HIT: int = 7
    RIFLE_FIRE: int = 8
    RIFLE_BOUNCE: int = 9
    WEAPON_SWITCH: int = 10
    PLAYER_PAIN_SHORT: int = 11
    PLAYER_PAIN_LONG: int = 12
    BODY_LAND: int = 13
    PLAYER_AIRJUMP: int = 14
    PLAYER_JUMP: int = 15
    PLAYER_DIE: int = 16
    PLAYER_SPAWN: int = 17
    PLAYER_SKID: int = 18
    TEE_CRY: int = 19
    HOOK_LOOP: int = 20
    HOOK_ATTACH_GROUND: int = 21
    HOOK_ATTACH_PLAYER: int = 22
    HOOK_NOATTACH: int = 23
    PICKUP_HEALTH: int = 24
    PICKUP_ARMOR: int = 25
    PICKUP_GRENADE: int = 26
    PICKUP_SHOTGUN: int = 27
    PICKUP_NINJA: int = 28
    WEAPON_SPAWN: int = 29
    WEAPON_NOAMMO: int = 30
    HIT: int = 31
    CHAT_SERVER: int = 32
    CHAT_CLIENT: int = 33
    CHAT_HIGHLIGHT: int = 34
    CTF_DROP: int = 35
    CTF_RETURN: int = 36
    CTF_GRAB_PL: int = 37
    CTF_GRAB_EN: int = 38
    CTF_CAPTURE: int = 39
    MENU: int = 40
