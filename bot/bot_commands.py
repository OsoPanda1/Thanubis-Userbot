import asyncio
from telethon import TelegramClient, events
from telethon.errors import *
from telethon.tl.functions.channels import EditBannedRequest, DeleteChannelRequest
from telethon.tl.functions.messages import DeleteChatUserRequest
from telethon.tl.types import ChatBannedRights
from config.security_config import SecurityConfig
from database.secure_database import SecureDatabase
from detection.threat_detector import ThreatDetector

class BotCommands:
    def __init__(self, client: TelegramClient, db: SecureDatabase, threat_detector: ThreatDetector):
        self.client = client
        self.db = db
        self.threat_detector = threat_detector
        self._register_handlers()

    def _register_handlers(self):
        @self.client.on(events.NewMessage(pattern='^.ban(?: |$)(.*)'))
        async def command_ban(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .ban <user_id> [reason]")
                return
            user_id = int(args[0])
            reason = ' '.join(args[1:]) if len(args) > 1 else "No reason provided"
            await self._ban_user(event.chat_id, user_id, reason)
            await event.respond(f"El usuario {user_id} ha sido baneado por: {reason}")

        @self.client.on(events.NewMessage(pattern='^.unban(?: |$)(.*)'))
        async def command_unban(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .unban <user_id>")
                return
            user_id = int(args[0])
            await self._unban_user(event.chat_id, user_id)
            await event.respond(f"El usuario {user_id} ha sido desbaneado.")

        @self.client.on(events.NewMessage(pattern='^.mute(?: |$)(.*)'))
        async def command_mute(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .mute <user_id> [duration] [reason]")
                return
            user_id = int(args[0])
            duration = args[1] if len(args) > 1 else "forever"
            reason = ' '.join(args[2:]) if len(args) > 2 else "No reason provided"
            await self._mute_user(event.chat_id, user_id, duration, reason)
            await event.respond(f"El usuario {user_id} ha sido silenciado por {duration} debido a: {reason}")

        @self.client.on(events.NewMessage(pattern='^.unmute(?: |$)(.*)'))
        async def command_unmute(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .unmute <user_id>")
                return
            user_id = int(args[0])
            await self._unmute_user(event.chat_id, user_id)
            await event.respond(f"El usuario {user_id} ha sido des-silenciado.")

        @self.client.on(events.NewMessage(pattern='^.kick(?: |$)(.*)'))
        async def command_kick(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .kick <user_id> [reason]")
                return
            user_id = int(args[0])
            reason = ' '.join(args[1:]) if len(args) > 1 else "No reason provided"
            await self._kick_user(event.chat_id, user_id, reason)
            await event.respond(f"El usuario {user_id} ha sido expulsado por: {reason}")

        @self.client.on(events.NewMessage(pattern='^.warn(?: |$)(.*)'))
        async def command_warn(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .warn <user_id> [reason]")
                return
            user_id = int(args[0])
            reason = ' '.join(args[1:]) if len(args) > 1 else "No reason provided"
            await self._warn_user(event.chat_id, user_id, reason)
            await event.respond(f"El usuario {user_id} ha sido advertido por: {reason}")

        @self.client.on(events.NewMessage(pattern='^.unwarn(?: |$)(.*)'))
        async def command_unwarn(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .unwarn <user_id>")
                return
            user_id = int(args[0])
            await self._unwarn_user(event.chat_id, user_id)
            await event.respond(f"Las advertencias del usuario {user_id} han sido eliminadas.")

        @self.client.on(events.NewMessage(pattern='^.warnings(?: |$)(.*)'))
        async def command_warnings(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .warnings <user_id>")
                return
            user_id = int(args[0])
            warnings = await self._get_warnings(event.chat_id, user_id)
            await event.respond(f"El usuario {user_id} tiene {warnings} advertencias.")

        @self.client.on(events.NewMessage(pattern='^.deletegroup$'))
        async def command_delete_group(event):
            chat_id = event.chat_id
            await self._delete_group(chat_id)
            await event.respond("El grupo ha sido eliminado por violar las políticas.")

        @self.client.on(events.NewMessage(pattern='^.deleteuser(?: |$)(.*)'))
        async def command_delete_user(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .deleteuser <user_id>")
                return
            user_id = int(args[0])
            chat_id = event.chat_id
            await self._delete_user(chat_id, user_id)
            await event.respond(f"El usuario {user_id} ha sido eliminado por violar las políticas.")

        @self.client.on(events.NewMessage(pattern='^.gban(?: |$)(.*)'))
        async def command_gban(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .gban <user_id>")
                return
            user_id = int(args[0])
            username = await self._get_username(user_id)
            await event.respond(f"Nacion Ironblood Anubis inicia procedimiento de Baneo Global en contra de {username}....")
            await asyncio.sleep(2)
            await event.respond("AnubisSpamWatch Elite gbanning....")
            await asyncio.sleep(2)
            await self._ban_user_global(user_id)
            await event.respond(f"GBAN APPROVED. El usuario {username} ha sido baneado globalmente.")

        @self.client.on(events.NewMessage(pattern='^.ungban(?: |$)(.*)'))
        async def command_ungban(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .ungban <user_id>")
                return
            user_id = int(args[0])
            username = await self._get_username(user_id)
            await self._unban_user_global(user_id)
            await event.respond(f"El usuario {username} ha sido desbaneado globalmente.")

        @self.client.on(events.NewMessage(pattern='^.gmute(?: |$)(.*)'))
        async def command_gmute(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .gmute <user_id>")
                return
            user_id = int(args[0])
            username = await self._get_username(user_id)
            await event.respond(f"Nacion Ironblood Anubis inicia procedimiento de Silencio Global en contra de {username}....")
            await asyncio.sleep(2)
            await event.respond("AnubisSpamWatch Elite gmuting....")
            await asyncio.sleep(2)
            await self._mute_user_global(user_id)
            await event.respond(f"GMUTE APPROVED. El usuario {username} ha sido silenciado globalmente.")

        @self.client.on(events.NewMessage(pattern='^.ungmute(?: |$)(.*)'))
        async def command_ungmute(event):
            args = event.pattern_match.group(1).split()
            if len(args) < 1:
                await event.respond("Uso: .ungmute <user_id>")
                return
            user_id = int(args[0])
            username = await self._get_username(user_id)
            await self._unmute_user_global(user_id)
            await event.respond(f"El usuario {username} ha sido des-silenciado globalmente.")

    async def _ban_user(self, chat_id: int, user_id: int, reason: str):
        try:
            rights = ChatBannedRights(
                until_date=None,
                view_messages=True,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True
            )
            await self.client(EditBannedRequest(chat_id, user_id, rights))
            await self.db.log_action(
                user_id,
                "user_banned",
                {"chat_id": chat_id, "reason": reason, "admin_id": self.client.user_id}
            )
        except Exception as e:
            logger.error(f"Failed to ban user {user_id}: {str(e)}")

    async def _unban_user(self, chat_id: int, user_id: int):
        try:
            rights = ChatBannedRights(
                until_date=None,
                view_messages=False,
                send_messages=False,
                send_media=False,
                send_stickers=False,
                send_gifs=False,
                send_games=False,
                send_inline=False,
                embed_links=False
            )
            await self.client(EditBannedRequest(chat_id, user_id, rights))
            await self.db.log_action(
                user_id,
                "user_unbanned",
                {"chat_id": chat_id, "admin_id": self.client.user_id}
            )
        except Exception as e:
            logger.error(f"Failed to unban user {user_id}: {str(e)}")

    async def _mute_user(self, chat_id: int, user_id: int, duration: str, reason: str):
        try:
            until_date = None
            if duration != "forever":
                duration_seconds = self._parse_duration(duration)
                until_date = datetime.utcnow() + timedelta(seconds=duration_seconds)
            rights = ChatBannedRights(
                until_date=until_date,
                send_messages=True
            )
            await self.client(EditBannedRequest(chat_id, user_id, rights))
            await self.db.log_action(
                user_id,
                "user_muted",
                {"chat_id": chat_id, "duration": duration, "reason": reason, "admin_id": self.client.user_id}
            )
        except Exception as e:
            logger.error(f"Failed to mute user {user_id}: {str(e)}")

    async def _unmute_user(self, chat_id: int, user_id: int):
        try:
            rights = ChatBannedRights(
                until_date=None,
                send_messages=False
            )
            await self.client(EditBannedRequest(chat_id, user_id, rights))
            await self.db.log_action(
                user_id,
                "user_unmuted",
                {"chat_id": chat_id, "admin_id": self.client.user_id}
            )
        except Exception as e:
            logger.error(f"Failed to unmute user {user_id}: {str(e)}")

    async def _kick_user(self, chat_id: int, user_id: int, reason: str):
        try:
            await self.client(DeleteChatUserRequest(chat_id, user_id))
            await self.db.log_action(
                user_id,
                "user_kicked",
                {"chat_id": chat_id, "reason": reason, "admin_id": self.client.user_id}
            )
        except Exception as e:
            logger.error(f"Failed to kick user {user_id}: {str(e)}")

    async def _warn_user(self, chat_id: int, user_id: int, reason: str):
        # Add logic to warn user and log the action
        pass

    async def _unwarn_user(self, chat_id: int, user_id: int):
        # Add logic to unwarn user and log the action
        pass

    async def _get_warnings(self, chat_id: int, user_id: int) -> int:
        # Add logic to get warnings for a user
        return 0

    async def _delete_group(self, chat_id: int):
        try:
            await self.client(DeleteChannelRequest(chat_id))
            await self.db.log_action(
                self.client.user_id,
                "group_deleted",
                {"chat_id": chat_id, "reason": "Violación de políticas"}
            )
        except Exception as e:
            logger.error(f"Failed to delete group {chat_id}: {str(e)}")

    async def _delete_user(self, chat_id: int, user_id: int):
        try:
            await self.client(DeleteChatUserRequest(chat_id, user_id))
            await self.db.log_action(
                self.client.user_id,
                "user_deleted",
                {"chat_id": chat_id, "user_id": user_id, "reason": "Violación de políticas"}
            )
        except Exception as e:
            logger.error(f"Failed to delete user {user_id} from chat {chat_id}: {str(e)}")

    async def _ban_user_global(self, user_id: int):
        try:
            group_ids = await self._get_all_groups()
            for group_id in group_ids:
                await self._ban_user(group_id, user_id, "Global ban")
            await self.db.log_action(
                user_id,
                "user_globally_banned",
                {"reason": "Global ban"}
            )
        except Exception as e:
            logger.error(f"Failed to globally ban user {user_id}: {str(e)}")

    async def _unban_user_global(self, user_id: int):
        try:
            group_ids = await self._get_all_groups()
            for group_id in group_ids:
                await self._unban_user(group_id, user_id)
            await self.db.log_action(
                user_id,
                "user_globally_unbanned",
                {"reason": "Global unban"}
            )
        except Exception as e:
            logger.error(f"Failed to globally unban user {user_id}: {str(e)}")

    async def _mute_user_global(self, user_id: int):
        try:
            group_ids = await self._get_all_groups()
            for group_id in group_ids:
                await self._mute_user(group_id, user_id, "forever", "Global mute")
            await self.db.log_action(
                user_id,
                "user_globally_muted",
                {"reason": "Global mute"}
            )
        except Exception as e:
            logger.error(f"Failed to globally mute user {user_id}: {str(e)}")

    async def _unmute_user_global(self, user_id: int):
        try:
            group_ids = await self._get_all_groups()
            for group_id in group_ids:
                await self._unmute_user(group_id, user_id)
            await self.db.log_action(
                user_id,
                "user_globally_unmuted",
                {"reason": "Global unmute"}
            )
        except Exception as e:
            logger.error(f"Failed to globally unmute user {user_id}: {str(e)}")

    async def _get_all_groups(self) -> List[int]:
        # Fetch all group IDs where the bot is an admin
        # This is a placeholder implementation
        return []

    def _parse_duration(self, duration: str) -> int:
        # Placeholder for parsing duration strings into seconds
        return 0

    async def _get_username(self, user_id: int) -> str:
        # Placeholder for fetching a username given a user ID
        return "username_placeholder"
