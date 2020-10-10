from json import load, dump
from discord import Embed
from discord.ext import commands
from discord.utils import get
from time import monotonic
from datetime import datetime, timezone
from math import floor
from sys import exc_info
from random import choice
from asyncio import sleep

bot = commands.Bot(command_prefix='e.', owner_id=552615180450660360, case_insensitive=True)
bot.remove_command('help')
authorized = [552615180450660360, 198385417341370368, 188650807120494592, 177432416959332353, 201820283697496064,
              189285659675066369, 164348894702993408, 193827690552360961, 552615180450660360, 202057451044995072,
              171336518919520256, 183210046212145152, 252137961875832833, 150974465931608064, 165668389585420288,
              94572460585779200, 188715801111560194, 203598377181642754]


def json_dump(n, d):
    with open(n, 'w+') as f:
        dump(d, f)
        f.close()


def json_load(n):
    with open(n, 'r') as f:
        a = load(f)
        f.close()
        return a


def get_channel(c):
    return bot.get_channel(c)


def get_role(g, r):
    return get(g.guild, id=r)


def embed_color():
    return choice([0x0d0d0d, 0x1d1d1d, 0x2f2f2f, 0x1a1a1a, 0x988001, 0xfad301, 0xfff6c5, 0xeb234b, 0x9f0121])


def update_data(a):
    d = 'bjson/db.json'
    db = json_load(d)
    if a not in db:
        db[a] = 0
        json_dump(d, db)


@bot.group()
async def help(c):
    if c.invoked_subcommand is None:
        e = Embed(title='Use `e.help <command name>` to receive helpful information about that specific command!',
                  description='It\'s highly recommended to run `e.help` before using a command.', color=embed_color())
        e.set_author(name='These are the available commands')
        e.add_field(name='1. Utilities',
                    value='`info` `mod` `ping`\n'
                          '~~`uptime`~~')
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
async def water(c):
    e = Embed(title='Tells you when is the real water hours.',
              description='Quick and simple.', color=embed_color())
    e.set_author(name='Water')
    e.add_field(name='Usages', value='`e.water`: Tells you when is the real water hours.', inline=False)
    e.add_field(name='Examples', value='`e.water`')
    await c.send(embed=e)


@help.command(aliases=['gp'])
async def givepoints(c):
    if c.author.id in authorized:
        e = Embed(title='e.givepoints', description='Gives Infraction Points to a user.', color=embed_color())
        e.set_author(name='Givepoints')
        e.add_field(name='Usages', value='`e.givepoints @someone`: Gives Infraction Points to someone.', inline=False)
        e.add_field(name='Examples', value='`e.givepoints @Pikalex#8877`')
        e.add_field(name='Alias', value='`gp`')
        await c.send(embed=e)


@help.command(aliases=['p'])
async def points(c):
    if c.author.id in authorized:
        e = Embed(title='e.points', description='Shows a user\'s Infraction Points.', color=embed_color())
        e.set_author(name='Points')
        e.add_field(name='Usages', value='`e.points @someone`: Shows someone\'s Infraction Points.', inline=False)
        e.add_field(name='Examples', value='`e.points @Pikalex#8877`')
        e.add_field(name='Alias', value='`p`')
        await c.send(embed=e)


@help.command(aliases=['rp'])
async def removepoints(c):
    if c.author.id in authorized:
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
    e.add_field(name='Latest Version', value='1.0.5 (2020-10-09)')
    e.add_field(name='First Version', value='1.0 (2020-09-28)')
    e.add_field(name='Developers', value='Pikalex04 and Ermelber')
    e.add_field(name='Discord API Libraries', value='discord.py')
    e.add_field(name='Languages', value='Python, JSON and Markdown')
    e.set_footer(text='This bot was made by Pikalex. Still Hosted on Pika\'s Ubuntu Server.\n'
                      'This bot was ispired by Ermelber\'s bot. Not Anymore Hosted on Szymmy\'s Pi.')
    await c.send(embed=e)


@bot.command()
async def water(c):
    a = c.author
    r = get_role(c, 764196084415201321)
    if r in a.roles:
        e = Embed(title='the real water hours at 23:29 (Italian Time).',
                  description='You got the <&764196084415201321> role removed. You\'ll not be mentioned anymore when '
                              'it\'s the real water hours.', color=embed_color())
        e.set_footer(text='You can add the Real Water Hours Gang role back by running this command again.')
        await a.remove_roles(r)
        await c.send(embed=e)
    else:
        e = Embed(title='the real water hours at 23:29 (Italian Time).',
                  description='You now received the <&764196084415201321> role. You\'ll be mentioned when it\'s the '
                              'real water hours.', color=embed_color())
        e.set_footer(text='You can remove the Real Water Hours Gang role by running this command again.')
        await a.add_roles(r)
        await c.send(embed=e)


@bot.command(aliases=['gp'])
async def givepoints(c, p):
    a = c.author
    m = c.message
    if a.id in authorized:
        if not m.mentions:
            await c.send(
                f'**{a.mention}**, you forgot to mention someone (`e.givepoints <points> <@someone>`)!')
            return
        if p.isdigit() is False:
            await c.send(
                f'**{a.mention}**, you didn\'t choose a valid amount of points! (`e.givepoints <points> <@someone>`)!')
            return
        r = m.mentions[0]
        i = str(r.id)
        update_data(i)
        db = json_load('bjson/db.json')
        db[i] += int(p)
        json_dump('bjson/db.json', db)
        m = f'**{a.mention}**, gave **{p}** points to **{r.mention}**.'
        await c.send(m)
        await get_channel(566327770108657698).send(m)


@givepoints.error
async def givepoints_mra(c, e):
    a = c.author
    if a.id not in authorized:
        if isinstance(e, commands.MissingRequiredArgument):
            await c.send(f'**{a.mention}**, you forgot to specify the points (`e.givepoints <points> <@someone>`)!')


@bot.command(aliases=['rp'])
async def removepoints(c, p):
    a = c.author
    m = c.message
    if a.id in authorized:
        if not m.mentions:
            await c.send(
                f'**{a.mention}**, you forgot to mention someone (`e.reducepoints <points> <@someone>`)!')
            return
        if p.isdigit() is False:
            await c.send(
                f'**{a.mention}**, you didn\'t choose a valid amount of points! (`e.reducepoints <points> '
                '<@someone>`)!')
            return
        r = m.mentions[0]
        i = str(r.id)
        update_data(i)
        d = 'bjson/db.json'
        db = json_load(d)
        db[i] -= int(p)
        json_dump(d, db)
        m = f'**{a.mention}**, removed **{p}** points from **{r.mention}**.'
        await c.send(m)
        await get_channel(566327770108657698).send(m)


@removepoints.error
async def removepoints_mra(c, e):
    a = c.author
    if a.id not in authorized:
        if isinstance(e, commands.MissingRequiredArgument):
            await c.send(f'**{a.mention}**, you forgot to specify the points (`e.removepoints <points> <@someone>`)!')


@bot.command(aliases=['p'])
async def points(c):
    a = c.author
    m = c.message
    if a.id in authorized:
        if not m.mentions:
            await c.send(f'**{a.mention}**, you forgot to mention someone (`e.points <@someone>`)!')
            return
        r = m.mentions[0]
        i = str(r.id)
        update_data(i)
        db = json_load('bjson/db.json')
        await c.send(f'**{a.mention}**, **{r.mention}** has **{db[i]}** points.')


@bot.command()
async def ping(c):
    before = monotonic()
    msg = await c.send('*Calculating...*')
    await msg.edit(content=f'I suffer of `{int((monotonic() - before) * 1000)}ms` of latency, by the way.')


async def real_water_hour():
    while not bot.is_closed():
        if datetime.now().minute == 29 and datetime.now(tz=timezone.utc).hour == 19:
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
            m = await get_channel(398674318101446678).send('<@&764196084415201321>')
            await m.edit(embed=e)
            return
        await sleep(60)


@bot.event
async def on_ready():
    bot.bg_task = await bot.loop.create_task(real_water_hour())


@bot.event
async def on_message(m):
    if m.author.id in authorized:
        d = 'bjson/db.json'
        db = json_load(d)
        t = datetime.now().day
        if t in [1, 8, 16, 22]:
            if db['rp'] == 0:
                for u in db:
                    p = floor(db[u] / 15)
                    p = 1 if p == 0 else p
                    db[u] -= p
                    m = f'Removed {p} points from <@{u}>.'
                    await get_channel(658737556023672852).send(m)
                    await get_channel(566327770108657698).send(m)
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
    await get_channel(566327770108657698).send(embed=e)
    await get_channel(566327770108657698).send('fix your shit lmao <@552615180450660360>')


bot.run(open('token/epb.txt', 'r').readline())
