import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

SECRETS = pathlib.Path(PATH.parent, "secrets")

DISCORD_TOKEN: str
with open(pathlib.Path(SECRETS, "discord_token.txt"), encoding="UTF-8") as secret:
    DISCORD_TOKEN = secret.readline().rstrip("\n")
