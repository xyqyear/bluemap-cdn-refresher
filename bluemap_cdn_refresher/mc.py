from mcstatus import JavaServer
from .config import config


def get_online_player_number():
    server = JavaServer(
        config["minecraft_server"]["host"], config["minecraft_server"]["port"]
    )
    try:
        status = server.status()
        return status.players.online
    except:
        return 0
