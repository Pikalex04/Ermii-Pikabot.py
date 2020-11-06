from json import load, dump
from discord import Embed, Status, Intents
from discord.ext import commands
from discord.utils import get
from time import monotonic
from datetime import datetime, timezone
from math import floor
from sys import exc_info
from random import choice
from asyncio import sleep
from difflib import get_close_matches
import socket

bot = commands.Bot(command_prefix='e.', owner_id=552615180450660360, case_insensitive=True,
                   intents=Intents.default().all())
bot.remove_command('help')


def json_dump(n, d):
    with open(n, 'w+') as f:
        dump(d, f)
        f.close()


def json_load(n):
    with open(n, 'r') as f:
        a = load(f)
        f.close()
        return a


def closematch(w, o):
    p = []
    for v in o:
        p.append(v.name)
        if v.nick:
            p.append(v.nick)
    r = get_close_matches(w, p, 1, 0.1).pop()
    if not get(o, name=r):
        return get(o, nick=r)
    return get(o, name=r)


def get_role(g, r):
    return get(g, id=r)


def embed_color():
    return choice([0x0d0d0d, 0x1d1d1d, 0x2f2f2f, 0x1a1a1a, 0x988001, 0xfad301, 0xfff6c5, 0xeb234b, 0x9f0121])


def update_data(a):
    d = 'bjson/db.json'
    db = json_load(d)
    if a not in db['sp']:
        db['sp'][a] = 0
        json_dump(d, db)


def update_uptime():
    d = json_load('bjson/db.json')
    d['u'] = datetime.now().isoformat(' ')
    json_dump('bjson/db.json', d)


@bot.group()
async def help(c):
    if c.invoked_subcommand is None:
        e = Embed(title='Use `e.help <command name>` to receive helpful information about that specific command!',
                  description='It\'s highly recommended to run `e.help` before using a command.', color=embed_color())
        e.set_author(name='These are the available commands')
        e.add_field(name='1. Utilities',
                    value='`info` `mod` `ping`\n'
                          '`uptime`')
        e.add_field(name='2. Minecraft',
                    value='~~`mcsize` `mcstatus`~~')
        e.add_field(name='3. Fun',
                    value='~~`pizza`~~ `water`')
        e.set_footer(text='Canceled commands aren\'t currently working.\n'
                          'Underlined commands aren\'t working properly.\n'
                          'For administrative commands, run e.mod.')
        await c.send(embed=e)


@help.command()
async def info(c):
    e = Embed(title='e.info', description='Provides information about the bot.', color=embed_color())
    e.set_author(name='Info')
    e.add_field(name='Usages', value='`e.info`: Provides information.', inline=False)
    e.add_field(name='Examples', value='`e.info`')
    e.add_field(name='Alias', value='`i`')
    await c.send(embed=e)


@help.command()
async def mod(c):
    if c.author.id in json_load('bjson/db.json')['a']:
        e = Embed(title='Use `e.help <command name>` to receive helpful information about that specific command!',
                  description='It\'s highly recommended to run `e.help` before using a command.', color=embed_color())
        e.set_author(name='These are the available commands')
        e.add_field(name='1. Utilities',
                    value='`givepoints` `points`\n'
                          '`removepoints`')
        e.add_field(name='2. Minecraft', value='None!')
        e.add_field(name='3. Fun', value='None :P')
        e.set_footer(text='Canceled commands aren\'t currently working.\n'
                          'Underlined commands aren\'t working properly.\n'
                          'For normal commands, run e.help.')
        await c.send(embed=e)


@help.command()
async def ping(c):
    e = Embed(title='e.ping', description='Calculates the latency of the connection between the bot and Discord API.',
              color=embed_color())
    e.set_author(name='Ping')
    e.add_field(name='Usages', value='`e.ping`: Calculates the latency.', inline=False)
    e.add_field(name='Examples', value='`e.ping`')
    await c.send(embed=e)


@help.command()
async def uptime(c):
    e = Embed(title='e.uptime',
              description='Tells you when the bot last restarted and the amount of online members right now.',
              color=embed_color())
    e.set_author(name='Uptime')
    e.add_field(name='Usages',
                value='`e.uptime`: Tells you when the bot last restarted and the amount of online members.',
                inline=False)
    e.add_field(name='Examples', value='`e.uptime`')
    await c.send(embed=e)


@help.command()
async def water(c):
    e = Embed(title='Tells you when is the real water hours.',
              description='Quick and simple.', color=embed_color())
    e.set_author(name='Water')
    e.add_field(name='Usages', value='`e.water`: Tells you when is the real water hours.', inline=False)
    e.add_field(name='Examples', value='`e.water`')
    await c.send(embed=e)


@help.command(aliases=['gp'])
async def givepoints(c):
    if c.author.id in json_load('bjson/db.json')['a']:
        e = Embed(title='e.givepoints', description='Gives Infraction Points to a user.', color=embed_color())
        e.set_author(name='Givepoints')
        e.add_field(name='Usages', value='`e.givepoints @someone`: Gives Infraction Points to someone.', inline=False)
        e.add_field(name='Examples', value='`e.givepoints @Pikalex#8877`')
        e.add_field(name='Alias', value='`gp`')
        await c.send(embed=e)


@help.command(aliases=['p'])
async def points(c):
    if c.author.id in json_load('bjson/db.json')['a']:
        e = Embed(title='e.points', description='Shows a user\'s Infraction Points.', color=embed_color())
        e.set_author(name='Points')
        e.add_field(name='Usages', value='`e.points @someone`: Shows someone\'s Infraction Points.', inline=False)
        e.add_field(name='Examples', value='`e.points @Pikalex#8877`')
        e.add_field(name='Alias', value='`p`')
        await c.send(embed=e)


@help.command(aliases=['rp'])
async def removepoints(c):
    if c.author.id in json_load('bjson/db.json')['a']:
        e = Embed(title='e.removepoints', description='Removes Infraction Points from a user.', color=embed_color())
        e.set_author(name='Removepoints')
        e.add_field(name='Usages', value='`e.removepoints @someone`: Removes Infraction Points from someone.',
                    inline=False)
        e.add_field(name='Examples', value='`e.removepoints @Pikalex#8877`')
        e.add_field(name='Alias', value='`rp`')
        await c.send(embed=e)


@bot.command(aliases=['i'])
async def info(c):
    e = Embed(title='General information about Mario Kart Bot can be read here.',
              description='This bot is the new Ermii Bot.', color=embed_color())
    e.set_author(name='Ermii Pikabot Info',
                 icon_url='https://cdn.discordapp.com/avatars/607320011366989826/101bac55cf15807c5c74d7e0d95bb510.png')
    e.add_field(name='Latest Version', value=json_load('bjson/db.json')['v'])
    e.add_field(name='First Version', value='1.0 (2020-09-28)')
    e.add_field(name='Source Code', value='https://github.com/Pikalex04/Ermii-Pikabot.py', inline=False)
    e.add_field(name='Developers', value='Pikalex04 and Ermelber')
    e.add_field(name='Discord API Libraries', value='discord.py')
    e.add_field(name='Languages', value='Python, JSON and Markdown')
    e.set_footer(text='This bot was made by Pikalex. Still Hosted on Pika\'s Ubuntu Server.\n'
                      'This bot was ispired by Ermelber\'s bot. Not Anymore Hosted on Szymmy\'s Pi.')
    await c.send(embed=e)


@bot.command(aliases=['mc'])
async def mcsize(c):
    if c.author.id == bot.owner_id:
        host = "garhoogin.com"
        port = 25566
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print(s)
    else:
        return


@bot.command()
async def ping(c):
    b = monotonic()
    m = await c.send(embed=Embed(description='*Calculating...*', color=embed_color()))
    await m.edit(embed=Embed(description=f'I suffer of `{int((monotonic() - b) * 1000)}ms` of latency, by the way.',
                             color=embed_color()))


@bot.command()
async def uptime(c):
    m = 0
    for member in c.guild.members:
        if member.status != Status.offline:
            m += 1
    await c.send(embed=Embed(description=f'Current time: **{datetime.now().isoformat(" ")}**\n'
                                         f'Bot last started at: **{json_load("bjson/db.json")["u"]}**\n'
                                         f'Online members: **{m}**', color=embed_color()))


@bot.command()
async def water(c):
    a = c.author
    r = get_role(c.guild.roles, 764196084415201321)
    if r in a.roles:
        e = Embed(title='the real water hours at 23:29 (Italian Time).',
                  description=f'You got the {r.mention} role removed. You\'ll not be mentioned anymore when it\'s the '
                              f'real water hours.', color=embed_color())
        e.set_footer(text='You can add the Real Water Hours Gang role back by running this command again.')
        await a.remove_roles(r)
        await c.send(embed=e)
    else:
        e = Embed(title='the real water hours at 23:29 (Italian Time).',
                  description=f'You now received the {r.mention} role. You\'ll be mentioned when it\'s the real water '
                              f'hours.', color=embed_color())
        e.set_footer(text='You can remove the Real Water Hours Gang role by running this command again.')
        await a.add_roles(r)
        await c.send(embed=e)


@bot.command(aliases=['gp'])
async def givepoints(c, p):
    a = c.author
    m = c.message
    s = m.content.split()
    db = json_load('bjson/db.json')
    if a.id in json_load('bjson/db.json')['a']:
        if p.isdigit() is False:
            await c.send(embed=Embed(
                description=f'<a:cross:747862910503616683> **| {a.display_name}**, you didn\'t choose a valid amount of'
                            f' points!', color=embed_color()))
            return
        if len(s) == 2:
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, you forgot to specify'
                                           ' a user!', color=embed_color()))
            return
        if m.mentions:
            u = m.mentions[0]
        else:
            if len(s) == 3 and s[2].isdigit():
                u = bot.get_user(int(s[2]))
                if u is None:
                    u = closematch(s[2], c.guild.members)
            else:
                u = closematch(m.content.replace(f'{s[0]} {s[1]}', '').strip(), c.guild.members)
        i = str(u.id)
        if i not in db:
            update_data(i)
            db = json_load('bjson/db.json')
        db['sp'][i] += int(p)
        json_dump('bjson/db.json', db)
        e = Embed(description=f'**{a.display_name}**, I gave **{p}** points to **{u.display_name}** successfully.',
                  color=embed_color())
        await c.send(embed=e)
        await bot.get_channel(764839683258712064).send(embed=e)


@givepoints.error
async def givepoints_mra(c, e):
    a = c.author
    if a.id not in json_load('bjson/db.json')['a']:
        if isinstance(e, commands.MissingRequiredArgument):
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, you forgot to specify'
                                           ' the points!', color=embed_color()))
        elif isinstance(e, Exception):
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, I didn\'t find '
                                           'anyone with that name or nickname!', color=embed_color()))


@bot.command(aliases=['rp'])
async def removepoints(c, p):
    a = c.author
    m = c.message
    s = m.content.split()
    db = json_load('bjson/db.json')
    if a.id in db['a']:
        if p.isdigit() is False:
            await c.send(embed=Embed(
                description=f'<a:cross:747862910503616683> **| {a.display_name}**, you didn\'t choose a valid amount of'
                            ' points!', color=embed_color()))
            return
        if len(s) == 2:
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, you forgot to specify'
                                           ' a user!', color=embed_color()))
            return
        if m.mentions:
            u = m.mentions[0]
        else:
            if len(s) == 3 and s[2].isdigit():
                u = bot.get_user(int(s[2]))
                if u is None:
                    u = closematch(s[2], c.guild.members)
            else:
                u = closematch(m.content.replace(f'{s[0]} {s[1]}', '').strip(), c.guild.members)
        i = str(u.id)
        if i not in db:
            update_data(i)
            db = json_load('bjson/db.json')
        db['sp'][i] -= int(p)
        json_dump('bjson/db.json', db)
        e = Embed(description=f'**{a.display_name}**, I removed **{p}** points from **{u.display_name}** successfully.',
                  color=embed_color())
        await c.send(embed=e)
        await bot.get_channel(764839683258712064).send(embed=e)


@removepoints.error
async def removepoints_mra(c, e):
    a = c.author
    if a.id not in json_load('bjson/db.json')['a']:
        if isinstance(e, commands.MissingRequiredArgument):
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, you forgot to specify'
                                           ' the points!', color=embed_color()))
        elif isinstance(e, Exception):
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, I didn\'t find '
                                           'anyone with that name or nickname!', color=embed_color()))


@bot.command(aliases=['p'])
async def points(c):
    a = c.author
    m = c.message
    db = json_load('bjson/db.json')
    if a.id in db['a']:
        if len(c.message.content.split()) == 1:
            await c.send(Embed(description=f'<a:cross:747862910503616683> **| {a.display_name}**, you forgot to specify'
                                           ' a user!', color=embed_color()))
            return
        if m.mentions:
            u = m.mentions[0]
        else:
            s = m.content.split()
            if len(s) == 3 and s[2].isdigit():
                u = bot.get_user(int(s[2]))
                if u is None:
                    u = closematch(c.message.content.replace(c.message.content.split[0], ''), c.guild.members)
            else:
                u = closematch(m.content.replace(f'{s[0]}', '').strip(), c.guild.members)
        i = str(u.id)
        if i not in db:
            update_data(i)
            db = json_load('bjson/db.json')
        await c.send(embed=Embed(description=f'**{a.display_name}**, **{u.display_name}** has **{db["sp"][i]}** '
                                             'points.', color=embed_color()))


@points.error
async def points_error(c):
    await c.send(Embed(description=f'<a:cross:747862910503616683> **| {c.author.display_name}**, I didn\'t find '
                                   'anyone with that name or nickname!', color=embed_color()))


@bot.group()
async def pika(c):
    if c.author.id == bot.owner_id:
        await c.send('Yes sir, waiting orders sir!')


@pika.command()
async def version(c, v):
    d = json_load('bjson/db.json')
    d['v'] = v
    json_dump('bjson/db.json', d)
    await c.send(f'Yes sir, changed the version to {v} sir!')


async def real_water_hour():
    while not bot.is_closed():
        if datetime.now().minute == 29 and datetime.now(tz=timezone.utc).hour == 22:
            w = json_load('water/water.json')
            t = datetime.now().weekday()
            e = d = u = ''
            for i in w:
                if t in w[i]['days']:
                    e = w[i]['title']
                    d = w[i]['description']
                    u = w[i]['image']
                    break
            e = Embed(title=e, description=d, color=embed_color())
            e.set_image(url=u)
            m = await bot.get_channel(398674318101446678).send('<@&764196084415201321>')
            await m.edit(embed=e)
            await sleep(60)
            bot.bg_task = await bot.loop.create_task(real_water_hour())
            return
        await sleep(60)


@bot.event
async def on_ready():
    bot.bg_task = await bot.loop.create_task(real_water_hour())


@bot.event
async def on_message(m):
    if m.author.id in json_load('bjson/db.json')['a']:
        d = 'bjson/db.json'
        db = json_load(d)
        t = datetime.now().day
        if t in [1, 8, 16, 22]:
            if db['rp'] == 0:
                for u in db['sp']:
                    p = floor(db['sp'][u] / 15)
                    p = 1 if p == 0 else p
                    db['sp'][u] -= p
                    await bot.get_channel(764839683258712064).send(embed=Embed(description=f'Removed {p} points from '
                                                                                           f'<@{u}>.',
                                                                               color=embed_color()))
                db['rp'] = 1
        elif t in [2, 9, 17, 23]:
            if db['rp'] == 1:
                db['rp'] = 0
        json_dump(d, db)
    await bot.process_commands(m)


@bot.event
async def on_error(v, *a, **k):
    x, u, t = exc_info()
    e = Embed(title='Error', description='This messages is sent every time an error happens.',
              color=0xFFFF00)
    e.set_author(name='Log', url=e.Empty, icon_url=e.Empty)
    e.add_field(name='Event', value=v, inline=False)
    e.add_field(name='Arguments', value=a, inline=False)
    e.add_field(name='Keyword Arguments', value=k, inline=False)
    e.add_field(name="Exception type:", value="{}".format(x), inline=False)
    e.add_field(name="Exception value:", value="{}".format(u), inline=False)
    e.add_field(name="Exception traceback object:", value="{}".format(t), inline=False)
    await bot.get_channel(764839683258712064).send(embed=e)
    await bot.get_channel(658737556023672852).send(embed=e)
    await bot.get_channel(764839683258712064).send('<@552615180450660360>, fix me.')


update_uptime()
bot.run(open('token/epb.txt', 'r').readline())
