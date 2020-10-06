from json import load, dump
from discord import Embed
from discord.ext import commands
from discord.utils import get
from time import monotonic
from datetime import datetime
from math import floor
from sys import exc_info

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
    return get(g, id=r)


def update_data(a):
    d = r'bjson\db.json'
    db = json_load(d)
    if a not in db:
        db[a] = 0
        json_dump(d, db)


@bot.command(aliases=['gp'])
async def givepoints(ctx, p):
    a = ctx.author
    m = ctx.message
    if a.id in authorized:
        if not m.mentions:
            await ctx.send(
                f'**{a.mention}**, you forgot to mention someone (`e.givepoints <points> <@someone>`)!')
            return
        if p.isdigit() is False:
            await ctx.send(
                f'**{a.mention}**, you didn\'t choose a valid amount of points! (`e.givepoints <points> <@someone>`)!')
            return
        r = m.mentions[0]
        i = str(r.id)
        update_data(i)
        db = json_load('bjson\\db.json')
        db[i] += int(p)
        json_dump('bjson\\db.json', db)
        m = f'**{a.mention}**, gave **{p}** points to **{r.mention}**.'
        await ctx.send(m)
        await get_channel(566327770108657698).send(m)


@givepoints.error
async def givepoints_mra(ctx, error):
    a = ctx.author
    if a.id not in authorized:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'**{a.mention}**, you forgot to specify the points (`e.givepoints <points> <@someone>`)!')


@bot.command(aliases=['rp'])
async def removepoints(ctx, p):
    a = ctx.author
    m = ctx.message
    if a.id in authorized:
        if not m.mentions:
            await ctx.send(
                f'**{a.mention}**, you forgot to mention someone (`e.reducepoints <points> <@someone>`)!')
            return
        if p.isdigit() is False:
            await ctx.send(
                f'**{a.mention}**, you didn\'t choose a valid amount of points! (`e.reducepoints <points> '
                '<@someone>`)!')
            return
        r = m.mentions[0]
        i = str(r.id)
        update_data(i)
        d = r'bjson\db.json'
        db = json_load(d)
        db[i] -= int(p)
        json_dump(d, db)
        m = f'**{a.mention}**, removed **{p}** points from **{r.mention}**.'
        await ctx.send(m)
        await get_channel(566327770108657698).send(m)


@removepoints.error
async def removepoints_mra(ctx, error):
    a = ctx.author
    if a.id not in authorized:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'**{a.mention}**, you forgot to specify the points (`e.removepoints <points> <@someone>`)!')


@bot.command(aliases=['p'])
async def points(ctx):
    a = ctx.author
    m = ctx.message
    if a.id in authorized:
        if not m.mentions:
            await ctx.send(f'**{a.mention}**, you forgot to mention someone (`e.points <@someone>`)!')
            return
        r = m.mentions[0]
        i = str(r.id)
        update_data(i)
        db = json_load(r'bjson\db.json')
        await ctx.send(f'**{a.mention}**, **{r.mention}** has **{db[i]}** points.')


@bot.command()
async def ping(ctx):
    before = monotonic()
    msg = await ctx.send('*Calculating...*')
    await msg.edit(content=f'I suffer of `{int((monotonic() - before) * 1000)}ms` of latency, by the way.')


@bot.event
async def on_message(msg):
    if msg.author.id in authorized:
        d = r'bjson\db.json'
        db = json_load(d)
        t = datetime.now().day
        if t in [1, 8, 16, 22]:
            if db['rp'] == 0:
                for u in db:
                    p = floor(db[u] / 10)
                    db[u] -= p
                    m = f'Removed {p} points from <@{u}>.'
                    await get_channel(658737556023672852).send(m)
                    await get_channel(566327770108657698).send(m)
                db['rp'] = 1
        elif t in [2, 9, 17, 23]:
            if db['rp'] == 1:
                db['rp'] = 0
        json_dump(d, db)
    await bot.process_commands(msg)


@bot.event
async def on_error(event, *args, **kwargs):
    exc_type, value, traceback = exc_info()
    e = Embed(title='Error', description='This messages is sent every time an error happens.',
              color=0xFFFF00)
    e.set_author(name='Log', url=e.Empty, icon_url=e.Empty)
    e.add_field(name='Event', value=event, inline=False)
    e.add_field(name='Arguments', value=args, inline=False)
    e.add_field(name='Keyword Arguments', value=kwargs, inline=False)
    e.add_field(name="Exception type:", value="{}".format(exc_type), inline=False)
    e.add_field(name="Exception value:", value="{}".format(value), inline=False)
    e.add_field(name="Exception traceback object:", value="{}".format(traceback), inline=False)
    await get_channel(640235517811621888).send(embed=e)
    await get_channel(640235517811621888).send('fix your shit lmao <@552615180450660360>')


bot.run(open(r'token\epb.txt', 'r').readline())
