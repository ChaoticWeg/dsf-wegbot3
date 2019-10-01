import discord


_activity_type_names = {
    "watching": discord.ActivityType.watching,
    "playing": discord.ActivityType.playing
}


def is_activity_type(name: str):
    return name in _activity_type_names.keys()


def get_activity_type_by_name(name: str):
    return _activity_type_names.get(name, discord.ActivityType.playing)


def create_activity(name: str, activity_type: discord.ActivityType = discord.ActivityType.playing):
    return discord.Activity(name=name, type=activity_type)
