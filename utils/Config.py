from dotenv import dotenv_values
import argparse
import os

from utils.Singleton import Singleton


class Config(metaclass=Singleton):
    def getCLIParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-env", "--Environment", help="[optional]Provide environment (local/prod)"
        )
        parser.add_argument(
            "-mode",
            "--Mode",
            help="[optional]Provide service mode (single/multiple). single [to restrict which chat can add your bot] , multiple [to allow any chat to add the bot]",
        )
        return parser

    def __init__(self) -> None:
        self.args = self.getCLIParser().parse_args()

        if self.args.Environment == "prod":
            self.config = {
                **dotenv_values(".env.common"),
                **dotenv_values(".env"),
                **os.environ,
            }
            self.config["env"] = "prod"
        else:
            self.config = {
                **dotenv_values(".env.common"),
                **dotenv_values(".env.local"),
                **os.environ,
            }
            self.config["env"] = "local"

        self.config["source"] = "tgcalls"

        self.config["server"] = "tgserver"

        self.config["ALLOWED_CHAT_TYPES"] = [
            "channel",
            "groups",
            "group",
            "supergroup",
            "supergroups",
            "megagroup",
        ]
        self.config["ACTIVE_CLIENTS"] = []
        # user ids of users who can perform global admin actions
        self.config["GLOBAL_ADMINS"] = []
        # numebr which dentores how many simulataneous playbacks can run
        self.config["SIMULTANEOUS_CALLS"] = 5
        # text to add at footer of each play message (if any)
        self.config["PLAYBACK_FOOTER"] = ""
        # number of songs that can be added to queue
        self.config["PLAYLIST_SIZE"] = 10
        # chat where restriction of number of simulataneous playbacks is not applicable
        # if service runs in single mode this needs to be entered
        self.config["SUDO_CHAT"] = []

        # by default any chat can add the bot (multiple mode)
        if "MODE" not in self.config or self.config["MODE"].lower() not in [
            "single",
            "multiple",
        ]:
            print(f"ENV Mode provided is invalid, using multiple by default")
            self.config["MODE"] = "multiple"
        else:
            self.config["MODE"] = self.config["MODE"].lower()
        if self.args.Mode is not None:
            if self.args.Mode.lower() not in ["single", "multiple"]:
                print(
                    f"Mode must be either single [to restrict which chat can add your bot] or multiple [to allow any chat to add the bot]"
                )
                exit()
            self.config["MODE"] = self.args.Mode.lower()
        print(f"Starting in {self.config['MODE']} Mode.")

        if (
            "MONGO_URL" not in self.config
            or self.config["MONGO_URL"] is None
            or len(self.config["MONGO_URL"]) == 0
        ) and self.config["MODE"] == "single":
            print("Switchign to multiple mode as MONGO_URL is empty.")
            self.config["MODE"] = "multiple"

        if self.config["ALLOWED_SONG_DURATION_IN_MIN"] is None:
            self.config["ALLOWED_SONG_DURATION_IN_MIN"] = 15

    def get(self, key):
        return self.config.get(key)

    def getAll(self):
        return self.config

    def setAllowedChatTypes(self, value):
        self.config["ALLOWED_CHAT_TYPES"] = value

    def setActiveClients(self, value):
        self.config["ACTIVE_CLIENTS"] = value

    def setExtraData(self, key, value):
        self.config[key] = value

    def saveGlobalAdmins(self, value):
        self.config["GLOBAL_ADMINS"] = value

    def save_simultaneous_calls(self, value):
        self.config["SIMULTANEOUS_CALLS"] = value

    def save_playback_footer(self, value):
        self.config["PLAYBACK_FOOTER"] = value

    def save_playlist_size(self, value):
        self.config["PLAYLIST_SIZE"] = value

    def setBotId(self, value):
        self.config["BOT_ID"] = value

    def setHelperActId(self, value):
        self.config["HELPER_ACT_ID"] = value

    def setHeleprActUserName(self, value):
        self.config["HELPER_ACT"] = value

    def fetchClient(self, chat_id):
        data = list(
            filter(lambda a: a["chat_id"] == chat_id, self.config["ACTIVE_CLIENTS"])
        )

        return None if len(data) == 0 else data[0]

    def getAdminForChat(self, chat_id):
        chat_admins = self.fetchClient(chat_id)
        return (
            self.config["GLOBAL_ADMINS"] + chat_admins.get("admins", [])
            if chat_admins not in [[], None]
            else []
        )

    def updateChat(self, chat, updateMissing=False):
        found = False
        for c in self.config["ACTIVE_CLIENTS"]:
            if c["chat_id"] == chat["chat_id"]:
                c.update(chat)
                found = True
        if found is False and updateMissing is True:
            self.config["ACTIVE_CLIENTS"].append(chat)
