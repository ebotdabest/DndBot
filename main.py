import json

import yt_dlp
from PIL import Image, ImageOps, ImageFont, ImageDraw
import discord
from discord.ext import commands, bridge
from io import BytesIO

with open("config.json", "r") as config:
    config = json.load(config)

bot = commands.Bot(command_prefix='!', help_command=None, intents=discord.Intents.all())

MAPPING = {
    "danger": "red",
    "primary": "blurple",
    "secondary": "dark_grey",
    "success": "green"
}

roles_classes = (
    1317185517435097098, 1317185518055723141, 1317185519125532684, 1317185519825981501, 1317185521159635046,
    1317185522078322721, 1317185523407654922, 1317185524582187058, 1317185525081182310, 1317185526813429770,
    1317185527799349311, 1317185528931549235
)

classes = [
    ["Barbarian", discord.ButtonStyle.red, "💪"],
    ["Bard", discord.ButtonStyle.red, "🎵"],
    ["Cleric", discord.ButtonStyle.blurple, "✨"],
    ["Druid", discord.ButtonStyle.blurple, "🌿"],
    ["Fighter", discord.ButtonStyle.grey, "⚔️"],
    ["Monk", discord.ButtonStyle.grey, "🧘"],
    ["Paladin", discord.ButtonStyle.green, "🛡️"],
    ["Ranger", discord.ButtonStyle.green, "🏹"],
    ["Rogue", discord.ButtonStyle.grey, "🗡️"],
    ["Sorcerer", discord.ButtonStyle.blurple, "🔮"],
    ["Warlock", discord.ButtonStyle.blurple, "📜"],
    ["Wizard", discord.ButtonStyle.blurple, "📘"]
]

sub_role_classes = (1317189505564016753, 1317189506641952859, 1317189507568893983, 1317189508080603229,
                    1317189509263130705, 1317189510219694102, 1317189511599489045)

wizard_subclasses = [
    ["Wizard", discord.ButtonStyle.blurple, "📘"],
    ["Artificer", discord.ButtonStyle.grey, "🛠️"],
    ["Necromancer", discord.ButtonStyle.blurple, "💀"],
    ["Alchemist", discord.ButtonStyle.green, "🧪"],
    ["Illusionist", discord.ButtonStyle.red, "🎭"],
    ["Conjurer", discord.ButtonStyle.blurple, "🥴"],
    ["Elementalist", discord.ButtonStyle.red, "🔥"]
]

races = [
    ["Dwarf", discord.ButtonStyle.grey, "🪓"],
    ["Elf", discord.ButtonStyle.green, "🍃"],
    ["Halfling", discord.ButtonStyle.blurple, "🍲"],
    ["Human", discord.ButtonStyle.grey, "🏰"],
    ["Dragonborn", discord.ButtonStyle.red, "🐉"],
    ["Gnome", discord.ButtonStyle.green, "🔧"],
    ["Half-elf", discord.ButtonStyle.blurple, "🌟"],
    ["Half-orc", discord.ButtonStyle.red, "🛡️"],
    ["Tiefling", discord.ButtonStyle.red, "🔥"],
    ["Ryan Gosling", discord.ButtonStyle.red, "✨"]
]

races_roles = [1317201181268906115, 1317201182351163506, 1317201183193956474, 1317201184720949311, 1317201185681178706,
               1317201186788475082, 1317201188059353220, 1317201188906733640, 1317201190735315017, 1317201192203583498]


class RaceSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for i, cls in enumerate(races):
            btn = discord.ui.Button(label=cls[0], style=cls[1], emoji=cls[2])
            btn.callback = self.create_callback(btn, races_roles[i])
            if i + 1 == len(races):
                btn.callback = self.ryan_selected
            self.add_item(btn)

    async def ryan_selected(self, interaction: discord.Interaction):
        await interaction.respond("Literally me", ephemeral=True)

    def create_callback(self, btn, role_id):
        async def callback(interaction):
            await self.on_button_click(interaction, btn, role_id)

        return callback

    async def on_button_click(self, interaction: discord.Interaction, btn: discord.ui.Button, role_id):
        for role in interaction.user.roles:
            if role.id in races_roles:
                await interaction.user.remove_roles(role)

        role = interaction.guild.get_role(role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)

        await interaction.respond(f"Your race is now: **{btn.label}**", ephemeral=True)


class WizardSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__()

        for i, cls in enumerate(wizard_subclasses):
            btn = discord.ui.Button(label=cls[0], style=cls[1], emoji=cls[2])
            btn.callback = self.create_callback(btn, sub_role_classes[i])
            self.add_item(btn)

    def create_callback(self, btn, role_id):
        async def callback(interaction):
            await self.on_button_click(interaction, btn, role_id)

        return callback

    async def on_button_click(self, interaction: discord.Interaction, btn: discord.ui.Button, role_id):
        for role in interaction.user.roles:
            if role.id in roles_classes:
                await interaction.user.remove_roles(role)

        for role in interaction.user.roles:
            if role.id in sub_role_classes:
                await interaction.user.remove_roles(role)

        role = interaction.guild.get_role(role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)

        await interaction.respond(f"You chose: **{btn.label}**", ephemeral=True)


class ClassSelectorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for i, cls in enumerate(classes):
            btn = discord.ui.Button(label=cls[0], style=cls[1], emoji=cls[2])
            btn.callback = self.create_callback(btn, roles_classes[i])
            if i + 1 == len(classes):
                btn.callback = self.wizard_choose
            self.add_item(btn)

    def create_callback(self, btn, role_id):
        async def callback(interaction):
            await self.on_button_click(interaction, btn, role_id)

        return callback

    async def on_button_click(self, interaction: discord.Interaction, btn: discord.ui.Button, role_id):
        for role in interaction.user.roles:
            if role.id in roles_classes:
                await interaction.user.remove_roles(role)

        for role in interaction.user.roles:
            if role.id in sub_role_classes:
                await interaction.user.remove_roles(role)

        role = interaction.guild.get_role(role_id)
        await interaction.user.add_roles(role)

        await interaction.response.send_message(content=f"You chose: **{btn.label}**", ephemeral=True)

        # try:
        #     await interaction.delete_original_response()
        # except Exception:
        #     # Newly sent
        #     pass
        #
        # await interaction.respond(f"You chose: **{btn.label}**", ephemeral=True)

        # if role in interaction.user.roles:
        #     await interaction.user.remove_roles(role)
        # else:

    async def wizard_choose(self, interaction: discord.Interaction):
        await interaction.respond("You chose wizard, select the type! (Select the first when you don't know what kind "
                                  "you want to be yet)",
                                  view=WizardSelectorView(),
                                  ephemeral=True)


MSG = """Szia, Én a Higher Being ( Krisztián ) csicskása vok.
They request you to write in this manner:

Character neve: ...
Kora (év): ...
Race: ...
Class: ...
Story (tagoljad egy kicsit hogy tudjunk részeket skippelni ha kellene visszanézi rá késöbb stb.) : ...
...
...
Speciális leírás/request from us The higer beings : ..."""


@bot.event
async def on_member_join(member: discord.Member):
    ply_role = discord.utils.get(member.guild.roles, id=1316065097835221023)

    await member.add_roles(ply_role)

    ow = {
        member.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True),
        member.guild.get_role(1316064593516171284): discord.PermissionOverwrite(view_channel=True),
        member.guild.get_role(1316064823792107650): discord.PermissionOverwrite(view_channel=True)
    }
    channel = await discord.utils.get(member.guild.categories, id=1317180871207419994).create_text_channel(
        f"character-{member.display_name}", overwrites=ow)
    await channel.send(MSG)

    load_buffer = BytesIO()
    if member.avatar is None:
        with open('none.png', 'rb') as f:
            load_buffer.write(f.read())
    else:
        await member.avatar.save(load_buffer)
    load_buffer.seek(0)
    pfp = Image.open(load_buffer).convert("RGBA")

    mask = Image.open('mask.png').convert('L')
    output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output = output.resize((150, 150))

    bg = Image.open('banner.png').convert('RGBA')
    bg.paste(output, (round(bg.width / 2) - 75, round(bg.height / 2) - 80), output)

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype('Quicksand-Regular.ttf', 40)
    msg = f"Welcome, {member.display_name}!"

    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((bg.width - w) / 2, bg.height / 1.5), msg, font=font)

    buffer = BytesIO()
    bg.save(buffer, 'PNG')
    buffer.seek(0)

    file = discord.File(fp=buffer, filename="image.png")
    await discord.utils.get(member.guild.text_channels, id=1316065584101720204).send(file=file)


@commands.has_permissions(administrator=True)
@bot.command()
async def clear(ctx: commands.Context):
    await ctx.channel.purge()


@commands.has_permissions(administrator=True)
@bot.command()
async def make_creator(ctx: discord.ApplicationContext):
    await ctx.message.delete()
    await ctx.channel.send("Choose your class!", view=ClassSelectorView())


@commands.has_permissions(administrator=True)
@bot.command()
async def make_race(ctx: discord.ApplicationContext):
    await ctx.message.delete()
    await ctx.channel.send("Choose your race!", view=RaceSelection())


# @bot.command()
# async def generate_roles(ctx: commands.Context):
#     roles = []
#     for cls in races:
#         role = await ctx.guild.create_role(name=cls[0], permissions=discord.Permissions.none(),
#                                            colour=getattr(discord.Colour,
#                                                           MAPPING[cls[
#                                                               1].name])())
#         roles.append(role.id)
#
#     print(roles)


# @bot.command()
# async def remove_roles(ctx: commands.Context):
#     for r in roles:
#         await ctx.guild.get_role(r).delete()


@bot.event
async def on_ready():
    print(bot.user.name, "is online!")


async def get_yt_data(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '48000',
            '-ac', '2',
            '-b:a', '192k',
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
        'no-playlist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = ""
        for f in info['formats']:
            if f['resolution'] == "audio only" and not f['url'].startswith("https://manifest"):
                url2 = f['url']
                break

    return info, url2


async def play_music(voice_client: discord.VoiceClient, url2):
    FFmpegPCMAudio = discord.FFmpegPCMAudio(url2, **{
        'options': '-vn',
        'before_options': f'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    })
    if voice_client.is_playing():
        voice_client.stop()

    voice_client.play(FFmpegPCMAudio)


@bot.command()
async def play(ctx: bridge.Context, url):
    if ctx.author.voice is None:
        await ctx.send("Sry but you are not in a voice channel!")
        return

    d, url2 = await get_yt_data(url)
    await ctx.send(f"Now playing: {d['title']}")
    await ctx.message.delete()
    await play_music(ctx.voice_client, url2)


@bot.command()
async def stop(ctx: bridge.Context):
    if ctx.voice_client is not None and ctx.voice_client.is_playing():
        await ctx.message.delete()
        ctx.voice_client.stop()
        await ctx.send("Stopped playing!")
    else:
        await ctx.send("I'm not playing any music right now.")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id == 1317147688227180555:
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    await bot.process_commands(message)


@bot.command()
async def join(ctx: commands.Context):
    await ctx.author.voice.channel.connect()


@bot.command()
async def leave(ctx: bridge.Context):
    await bot.voice_clients[0].disconnect(force=True)


bot.run(token=config["token"])
