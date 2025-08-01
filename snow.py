import discord
import random
import os
import json
import aiohttp
import google.generativeai as genai
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GIMINI = os.getenv("GEMINI_API")

genai.configure(api_key=GIMINI)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

ID_CHANNEL_LB = 1393593535365775472
ID_CHANNEL_WELLCOME = 1392346223381450802
ID_CHANNEL_EXIT = 1392714811913011250
ID_CHANNEL_AI = 1392848960112300153 and 1393822485702508555
riwayat_chat = {}

bot = commands.Bot(command_prefix = "!", intents=intents)
user_data = {}

def di_channel_bot(channel_id):
    async def predikat(ctx):
        if ctx.channel.id == channel_id:
            return True

        else:
            channel_obj = bot.get_channel(channel_id)
            await ctx.send(f"Command ini cuman bisa di pake di {channel_obj.mention}")
            return False
    return commands.check(predikat)

def buka_data():
    if os.path.exists("python/bot/lvl.json"):
        with open("python/bot/lvl.json", "r") as f:
            user = json.load(f)
        return user
    else:
        return{}

def simpan_data(data_to_save):
    with open("python/bot/lvl.json", "w") as f:
        json.dump(data_to_save, f, indent=4)

@tasks.loop(minutes=5)
async def auto_save_data():
    """Menyimpan data otomatis"""
    simpan_data(user_data)
    print("LOG: Berhasil menyimpan data.")


@bot.event
async def on_ready():
    global user_data
    user_data = buka_data()
    auto_save_data.start()
    print(f'{bot.user} siap bertugas')
    print('Auto-save aktif')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(ID_CHANNEL_WELLCOME)
    daftar_pesan = [
            f"Selamat datang di server {member.mention}.",
            f"Halo {member.mention}, semoga betah.",
            f"Selamat datang di server {member.mention}, selamat bergabung dengan kami.",
            f"Lihat siapa yang datang {member.mention}, apa kamu bawa makanan?",
            f"Liat ada anak baru nih {member.mention}."
        ]
    embed = discord.Embed(
        title = "**SELAMAT DATANG**",
        description = random.choice(daftar_pesan),
        color = discord.Color.red()
    )

    embed.set_thumbnail(url = member.display_avatar.url)

    await channel.send(embed = embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(ID_CHANNEL_EXIT)

    embed = discord.Embed(
        title = "**GOODBYE**",
        description= f"selamat tinggal {member.name}",
        color = discord.Color.red()
    )

    embed.set_thumbnail(url = member.display_avatar.url)

    await channel.send(embed = embed)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    if message.channel.id == ID_CHANNEL_AI:
        await message.channel.typing()
        user_id = message.author.id
        prompt = message.content
        model = genai.GenerativeModel('gemini-1.5-flash')

        if user_id not in riwayat_chat:
            riwayat_chat[user_id] = model.start_chat(history=[])

        try:
            respon = riwayat_chat[user_id].send_message(prompt)
            teks_bersih = respon.text.strip("` ")
            await message.reply(teks_bersih)
        except Exception as e:
            await message.reply("Aduhh, bentar, otak AI-ku ngehang nih.")
            print(f"Error dari Gemini: {e}")
        
        return

    user_id = str(message.author.id)
    if user_id not in user_data:
        user_data[user_id] = {'rank': 'None', 'level': 0, 'xp': 0}
    
    level_data = user_data[user_id].get('level', 0)

    if isinstance(level_data, int):
        xp_didapat = random.randint(1, 5)
        user_data[user_id]["xp"] += xp_didapat
        level_sekarang = user_data[user_id]["level"]
        xp_sekarang = user_data[user_id]["xp"]
        xp_dibutuhkan = 5 * (level_sekarang ** 2) + (50 * level_sekarang) + 100
        
        if xp_sekarang >= xp_dibutuhkan:
            user_data[user_id]["level"] += 1
            level_berikutnya = user_data[user_id]["level"]
            user_data[user_id]["xp"] = 0
            await message.channel.send(f"Selamat, {message.author.mention}, kamu telah naik ke level {level_berikutnya}!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention} sorry command nya gk ada nih cek `!menu` ya.", delete_after = 5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"{ctx.author.mention} inputnya salah paling coba kasih angka.", delete_after = 5)
    elif isinstance(error, commands.NotOwner):
        await ctx.send(f"{ctx.author.mention} command ini khusus owner aja yaa 🤗.", delete_after = 5)
    else:
        print(f"Pak boss, ada error nih: {error}")
        await ctx.send(f"{ctx.author.mention} Aduh ad error aneh nih, ak bilang pak bos dulu ya.", delete_after = 5)

@bot.command()
@commands.is_owner()
async def clear(ctx, jumlah: int):
    """Menghapus chat menggunakan command"""
    await ctx.channel.purge(limit = jumlah + 1)
    await ctx.send(f"berhasil menghapus pesan sejumlah {jumlah + 1}", delete_after = 5 )

@bot.command()
@commands.is_owner()
async def setrank(ctx, member: discord.Member, *, value: str):
    """Mengubah rank menggunakan command"""
    user_id = str(member.id)

    if user_id not in user_data:
        user_data[user_id] = {'rank': 'None', 'level': 0, 'xp': 0}

    user_data[user_id]['rank'] = value
    simpan_data(user_data)

    await ctx.send(f"Rank dari {member.display_name} berhasil di ubah menjadi {value}", delete_after = 5)

@bot.command()
@commands.is_owner()
async def setlevel(ctx, member: discord.Member, *, value: str):
    """Menambah level menggunakan command"""
    user_id = str(member.id)

    if user_id not in user_data:
        user_data[user_id] = {'rank': 'None', 'level': 0, 'xp': 0}

    try:
        level_angka = int(value)
        user_data[user_id]['level'] = level_angka
        notif = f"level berhasil di ubah menjadi {level_angka}"
    
    except ValueError:
        level_teks = value
        user_data[user_id]['level'] = level_teks
        notif = f"Level berhasil di ubah menjadi {level_teks}"
    user_data[user_id]['xp'] = 0

    simpan_data(user_data)
    await ctx.send(notif, delete_after = 1)

@bot.command()
@commands.is_owner()
async def kick(ctx, member: discord.Member, *, reason = "Takbisa berkata-kata"):
    """Kick menggunakan command"""
    if member == ctx.guild.me:
        return await ctx.send("anda tidak bisa mengeluarkan saya.")
    if member == ctx.author:
        return await ctx.send("anda tidak bisa mengeluarkan diri anda sendiri.")

    await member.kick(reason = f"Di kick oleh {ctx.author.name}. Alasan: {reason}")

    embed = discord.Embed(
        title = "**Kick member**",
        description = f"{member} telah di kick dari server.",
        color = discord.Color.red()
    )

    embed.add_field(name = "oleh moderator", value = ctx.author.mention, inline = False)
    embed.add_field(name = "alasan", value = reason, inline = False)

    await ctx.send(embed = embed, delete_after = 10)


@bot.command()
async def menu(ctx):
    embed = discord.Embed(
        title = "📜 Daftar command bot",
        color = discord.Color.red()
    )
    
    if bot.user.display_avatar:
        embed.set_thumbnail(url = bot.user.display_avatar.url)
    embed.add_field(name = "**GENERAL**", value = "", inline = False)

    embed.add_field(name = "!halo", value = "buat nyapa bot.", inline = False)
    embed.add_field(name = "!leaderboard / !lb", value = "buat liat top 10 level terttinggi", inline = False)
    embed.add_field(name = "!meme", value = "pake ini biar bot bisa ngirim meme", inline = False)
    embed.add_field(name = "!rank", value = "buat liat rank, mention orang lain biar kmu bisa liat rank orang", inline = False)
    embed.add_field(name = "!serverinfo", value= "buat liat info dari server.", inline = False)
    embed.add_field(name = "!userinfo", value = "buat liat informasi dari user, mention orang yng mau kmu liat.", inline = False)

    embed.add_field(name = "**GAME**", value = "", inline = False)

    embed.add_field(name = "!coinflip", value = "coin atau gambar?, tambah kan `coin` atau `gambar` setelah !coinflip", inline = False)

    await ctx.send(embed = embed)


@bot.command()
async def rank(ctx, member: discord.Member = None):
    target = member or ctx.author

    user_id = str(target.id)

    if user_id in user_data:
        rank_sekarang = user_data[user_id]["rank"]
        level_sekarang = user_data[user_id]["level"]
        xp_sekarang = user_data[user_id]["xp"]

        embed = discord.Embed(
            title = f"level {target.display_name}",
            color = discord.Color.red()
        )

        if target.display_avatar:
            embed.set_thumbnail(url= target.display_avatar.url)
        
        if isinstance(level_sekarang, str):
            embed.add_field(name = "Rank", value = rank_sekarang, inline = False)
            embed.add_field(name = "Level", value = level_sekarang, inline = False)
            embed.add_field(name = "xp", value = xp_sekarang, inline = False)

        elif isinstance(level_sekarang, int):
            xp_dibutuhkan = 5 * (level_sekarang ** 2) + (50 * level_sekarang) + 100
            embed.add_field(name = "Rank", value = rank_sekarang, inline = False)
            embed.add_field(name = "Level", value = level_sekarang, inline = False)
            embed.add_field(name = "xp", value = f"{xp_sekarang} / {xp_dibutuhkan}", inline = False)


        await ctx.send(embed = embed)
    else:
        await ctx.send(f"{target.mention} belum ada di database, minta pengguna menulis pesan dahulu.", delete_after = 2)

@bot.command()
async def halo(ctx):
    jawab = [
            'Halo juga',
            'Hai',
            'Ada yang bisa dibantu',
            'Yo, apa kabar',
            'YO',
            'Heyoo',
            'Ada apa nih'
            ]

    await ctx.send(f"{random.choice(jawab)} {ctx.author.mention}")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    target = member or ctx.author

    embed = discord.Embed(
        title = f"🔍 Informasi pengguna {target.display_name}",
        color = target.top_role.color if target.top_role.color != discord.Color.default() else discord.Color.green()
    )

    if target.display_avatar:
        embed.set_thumbnail(url=target.display_avatar.url)

    embed.add_field(name='Nama', value=f'{str(target)}', inline=True)
    embed.add_field(name="ID Pengguna", value=f'{target.id}', inline=True)
    embed.add_field(name='Status', value=f'{str(target.status).capitalize()}', inline=True)
    embed.add_field(name="Akun Dibuat", value=f'<t:{int(target.created_at.timestamp())}:D>', inline=True)
    embed.add_field(name="Bergabung Server", value=f'<t:{int(target.joined_at.timestamp())}:D>', inline=True)

    await ctx.send(embed = embed)

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild

    embed = discord.Embed(
        title = f"🔍 Informasi server {server.name}",
        color = discord.Color.blue()
    )

    if server.icon:
        embed.set_thumbnail(url = server.icon.url)

    embed.add_field(name = "nama server", value=f"{str(server.name)}", inline = True)
    embed.add_field(name = "ID server", value = f"{server.id}", inline = True)
    embed.add_field(name = "Ownner", value = f"{server.owner}", inline = True)
    embed.add_field(name = "Jumlah anggota", value = f"{server.member_count}", inline = True)
    embed.add_field(name = "Tanggal dibuat", value = f"<t:{int(server.created_at.timestamp())}:D>", inline = True)


    await ctx.send(embed = embed)

@bot.command()
async def meme(ctx):
    meme_api = "https://meme-api.com/gimme"
    await ctx.typing()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(meme_api) as response:
                if response.status == 200:
                    data = await response.json()
                    meme_title = data['title']
                    meme_url = data['url']

                    embed = discord.Embed(
                        title = meme_title,
                        color = discord.Color.red()
                    )
                    embed.set_image(url = meme_url)

                    await ctx.send(embed = embed)
                else:
                    await ctx.send("waduh API meme nya lg eror nih sorry yaa.")
    except Exception as e:
        print(f"error saat mengambil meme: {e}")
        await ctx.send("Aduh, ada error nih pas nyoba ngambil meme. Maaf ya.")

@bot.command(name="leaderboard", aliases=["lb"])
@di_channel_bot(ID_CHANNEL_LB)
async def leaderboard(ctx):
    if not user_data:
        await ctx.send("Belum ad data untuk di tampilkan.")
        return
    
    sorted_user = sorted(user_data.items(), key=lambda item: (item[1].get('level', 0), item[1].get('xp', 0)), reverse=True)

    embed = discord.Embed(
        title = "🏆 Leaderboard",
        description = "Berikut adalah 10 pengguna dengan level tertinggi!",
        color = discord.Color.gold()
    )

    for i, (user_id, data) in enumerate(sorted_user[:10]):
        try:
            member = await bot.fetch_user(int(user_id))
            username = member.display_name
        except discord.NotFound:
            username = "Unknown"
        
        level = data.get('level', 0)
        xp = data.get('xp', 0)

        embed.add_field(
            name = f"#{i + 1} - {username}",
            value = f"Level: {level} | xp: {xp}",
            inline = False
            )

    await ctx.send(embed = embed)

@bot.command()
async def coinflip(ctx, tebakan_user: str):
    pilihan_valid = ["gambar", "coin"]
    tebakan_user = tebakan_user.lower()

    if tebakan_user not in pilihan_valid:
        await ctx.send(f"pilihan {tebakan_user} ini tidak valid, pilih antara `Gambar` atau `Coin`.")
        return

    pilihan_bot = random.choice(pilihan_valid)
    hasil = f"Kamu memilih {tebakan_user}\nbot melempar coin  dan hasil nya adalah **{pilihan_bot}**\n\n"

    if tebakan_user == pilihan_bot:
        hasil += "Tebakan mu **BENAR**🎉"
    else:
        hasil += "Tebakan mu **SALAH**❌"

    await ctx.send(hasil)


bot.run(TOKEN)