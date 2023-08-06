import os


def is_copilot():
    """Are we running in copilot/ECS?"""
    return "ECS_CONTAINER_METADATA_URI_V4" in os.environ
