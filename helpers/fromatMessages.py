from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from utils.Logger import *
from utils.Config import Config

Config = Config()


def getMessage(message, action):
    try:
        extra_options = {
            "-video": "Stream the video file in video chat.",
            "-audio": "Stream just the audio.",
            "-repeat": "Play the song/video in repeat mode.",
            "-res720": "Stream the audio/video in the provided quality/resolution.",
            "-silent": "Silently play the requested file/url.",
            "-lipsync": "Use this if audio is not in sync with video",
        }
        if action == "private-chat":
            send_message = f"**Hi šµ {message.chat.first_name if hasattr(message.chat, 'first_name') else 'User'}**"
            send_message = (
                send_message
                + f"\n\n**[Voice Chat Music Player]({config.get('BOT_URL')})** is a [SkTechHub Product]({config.get('PARENT_URL')})."
            )
            send_message = (
                send_message
                + f"\n__It is designed to play, as simple as possible, music in your groups through the **new voice chats** introduced by Telegram.__"
            )
            send_message = (
                send_message
                + f"\n\n**So why wait š add the bot to a group and get started š§**\n\n**Source Code :** [Repository]({config.get('GITHUB_REPO')})"
            )
            return send_message, getReplyKeyBoard(message, action)

        elif action == "help-msg":
            helpMessage = f"**VoiceChat Music Player**\n**Source Code :** [Repository]({config.get('GITHUB_REPO')})"
            helpMessage = (
                helpMessage
                + f"\n\nā¢ **/play song name/song url : ** __Start a song / add to queue.__"
            )
            for k, v in extra_options.items():
                helpMessage = helpMessage + f"\n\t\t\t\t- **{k} : ** __{v}__"
            helpMessage = helpMessage + f"\nā¢ **/stop : ** __Stop the playback.__"
            helpMessage = (
                helpMessage + f"\nā¢ **/refreshadmins : ** __Refreshes the admin list.__"
            )
            helpMessage = (
                helpMessage
                + f"\nā¢ **/auth : ** __Adds the user in reply to the message as admin.__"
            )
            helpMessage = (
                helpMessage
                + f"\nā¢ **/unauth : ** __Removes the user in reply to the message as admin.__"
            )
            helpMessage = (
                helpMessage
                + f"\nā¢ **/listadmins : ** __Lists the users assigned as admins for the bot.__"
            )
            helpMessage = (
                helpMessage
                + f"\nā¢ **/adminmode on|off : ** __Turning this on makes the bot actions available only to bot admins.__"
            )
            helpMessage = (
                helpMessage + f"\n\n**__For any issues contact @voicechatsupport__**"
            )
            return helpMessage, getReplyKeyBoard(message, action)

        elif action == "chat-not-allowed":
            send_message = f"**š Sorry but this chat is not yet allowed to access the service. You can always check the demo in [Support Group]({config.get('SUPPORT_GROUP')}).**"
            send_message = (
                send_message
                + f"\n\n**Why ā**\n- __Due to high usage we have restricted the usage of the bot in just our [Support Group]({config.get('SUPPORT_GROUP')}) __"
            )
            send_message = (
                send_message
                + f"\n- __Join the [Support Group]({config.get('SUPPORT_GROUP')}) to access the bot or deploy your own bot __ **Source Code :** [Github]({config.get('GITHUB_REPO')})"
            )

            return send_message, getReplyKeyBoard(message, action)

        elif action == "start-voice-chat":
            send_message = (
                f"**Please start a voice chat and then send the command again**"
            )
            send_message = (
                send_message
                + f"\n**1.** __To start a group chat, you can head over to your groupās description page.__"
            )
            send_message = (
                send_message
                + f"\n**2.** __Then tap the three-dot button next to Mute and Search start a Voice Chat.__"
            )
            return send_message, getReplyKeyBoard(message, action)

    except Exception as ex:
        logException(f"**__Error : {ex}__**", True)


def getReplyKeyBoard(message, action):
    try:
        if action == "private-chat":
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ā Add the bot to Group ā",
                            url=f"{config.get('BOT_URL')}?startgroup=bot",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "š„ Support Group", url=f"{config.get('SUPPORT_GROUP')}"
                        ),
                        InlineKeyboardButton(
                            "š Source Code", url=f"{config.get('GITHUB_REPO')}"
                        ),
                    ],
                ]
            )
            return keyboard
        elif action == "chat-not-allowed":
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "š Use In Demo Group", url=f"{config.get('SUPPORT_GROUP')}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "š Source Code", url=f"{config.get('GITHUB_REPO')}"
                        ),
                    ],
                ]
            )
            return keyboard
        return None
    except Exception as ex:
        logException(f"**__Error : {ex}__**", True)
