V = 'v2.6.2'
botinfo = (f'**AM4 ACDB bot** {V}\n'
           f'made by **favorit1**\n'
           f'database and profit formula by **Scuderia Airlines**')


import discord
from discord.ext import commands, tasks

import mysql.connector

bot = commands.Bot(command_prefix = '$')

acdb = mysql.connector.connect(user='***REMOVED***',
                               passwd='***REMOVED***',
                               host='***REMOVED***',
                               database='***REMOVED***')

cursor = acdb.cursor(buffered = True)

from sys import executable, argv
from os import execl, path
def restart_program():
    execl(executable, path.abspath(__file__), * argv)

from random import randint
from time import gmtime, time
import json

today = gmtime()[7]
infoC = 0
compareC = 0
searchC = 0
seeallC = 0
priceC = 0
websiteC = 0
sheetC = 0
airportC = 0
def counter(cmd):
    global infoC, compareC, searchC, seeallC, priceC, websiteC, sheetC, airportC, today
    if cmd == 'info':
        infoC += 1
    elif cmd == 'compare':
        compareC += 1
    elif cmd == 'search':
        searchC += 1
    elif cmd == 'seeall':
        seeallC += 1
    elif cmd == 'price':
        priceC += 1
    elif cmd == 'website':
        websiteC += 1
    elif cmd == 'sheet':
        sheetC += 1
    elif cmd == 'airport':
        airportC += 1
    else:
        pass
    
    if today != gmtime()[7]:
        print(f"Today's bot usage:\ninfo: {infoC}\ncompare: {compareC}\nseeall: {seeallC}\nsearch: {searchC}\nairport: {airportC}\nwebsite: {websiteC}\nsheet: {sheetC}\n"
              f"Total: {infoC+compareC+seeallC+searchC+airportC+websiteC+sheetC}\n_______________________________\nprice: {priceC}")
        today = gmtime()[7]
        infoC = 0
        compareC = 0
        searchC = 0
        seeallC = 0
        priceC = 0
        websiteC = 0
        sheetC = 0
        airportC = 0
    else:
        pass
        
@bot.event
async def on_ready():
    if gmtime()[7] >= 311:
        acotd = randint(1, 310)
    else:
        acotd = gmtime()[7]
        
    #cursor.execute(f'SELECT `aircraft` FROM `am4bot` WHERE `acId` = {acotd}')
    #for ac in cursor:
    #    await bot.change_presence(activity = discord.Activity(type = 3, name = f'AC of the day: {ac[0]}'))
    print(f'ACDB Bot {V} is online, latency is {round(bot.latency * 1000)}ms')
    acdb.close()

@bot.event
async def on_command_error(ctx, error):    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing arguments. See $help for proper command usage.')
    elif isinstance(error, commands.MissingRole):
        await ctx.send(f'You do not have the required roles to use this command.')
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(f'This command cannot be used in a private message.')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You're doing that too fast! Try again in {round(error.retry_after)} seconds.")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(f"Command has been temporarily disabled. We are working on enabling it again.")
    else:
        print(error)

@bot.command(aliases = ['tools', 'web'], help = 'Links to Scuderia\'s AM4 Tools Website')
async def website(ctx):
    if paused == False:
        counter('website')
        await ctx.send(f'Here\'s the link to the AM4 Tools Website, created by Scuderia Airlines:\nhttps://scuderiaairlines.github.io/AM4-Guides-and-Tools/index.html')

@bot.command(aliases = ['excel', 'sheet'], help = 'Links to the AM4 AC Spreadsheet')
async def spreadsheet(ctx):
    if paused == False:
        counter('sheet')
        await ctx.send(f'Here\'s the link to the AM4 AC spreadsheet, created by Scuderia Airlines, and the rest of the Guide Development team:\nhttps://docs.google.com/spreadsheets/d/1YInKDK8fHmetOO1n9ZSyn8--gZhNmsY6BIjBoEhInTQ/edit?usp=sharing')
    
@bot.command(aliases = ['all', 'allac'], help = 'Links to a spreadsheet containing all short names of ACs to be used with the $info command', brief = 'Sends all short names of ACs')
async def seeall(ctx):
    if paused == False:
        counter('seeall')
        await ctx.send(f'Here\'s the link to all AC short names. These are to be used in almost all commands.\nhttps://docs.google.com/spreadsheets/d/1KfMM5N52mIIii_cwRFcHsjbo491DkTanBlC7piFofWk/edit?usp=sharing')

def profit(ac):
    tpriceE = round(((0.4 * ac[2]) + 170) * 1.10)
    tpriceR = round(((0.3 * ac[2]) + 150) * 1.10)
    co2 = float(ac[3]) * ac[6] * ac[2] * 0.13
    fuel = float(ac[4]) * ac[2] * 0.85
    fpdE = 24 / (ac[2] / (ac[5] * 1.5))
    fpdR = 24 / (ac[2] / ac[5])
    
    ppfE = round((tpriceE * ac[6]) - co2 - fuel)
    ppfR = round((tpriceR * ac[6]) - co2 - fuel)

    ppdE = round(ppfE * fpdE)
    ppdR = round(ppfR * fpdR)

    return (ppfR, fpdR, ppdR, ppfE, fpdE, ppdE)


@bot.command(aliases = ['ac'], help = 'Sends stats of a selected AC. Usage: $info <short name of an AC>', brief = 'Sends stats of a selected AC')
async def info(ctx, plane):
    if paused == False:
        counter('info')
        succ = False
        injection = False
        if plane[0] == "'":
            injection = True
        if injection == False:
            try:
                acdb.reconnect(attempts = 5, delay = 0.5)
                cursor.execute(f"SELECT `manf`, `aircraft`, `rng`, `co2`, `fuel`, `spd`, `cap`, `model`, `cost` FROM `am4bot` WHERE `shortname` = '{plane}'")
                acdb.close()
            except mysql.connector.Error as error:
                await ctx.send(f'Database error. Contact <@243007616714801157> if this happens.```python\n{error}```')
        for ac in cursor:
            pro = profit(ac)
    
            message = (f'**{ac[1]}** stats:```python\n           Price: ${ac[8]} million\n        Capacity: {ac[6]} pax\n'
                       f'           Range: {ac[2]} km\n           Speed: {ac[5]} km/h\nFuel Consumption: {ac[4]} lbs/km\n   CO2 Emmisions: {ac[3]} kg/pax/km\n'
                       f'Profit per flight (Realism): ${pro[0]:,}\n  Flights per day (Realism): {round(pro[1], 2)}\n   Profit per day (Realism): ${pro[2]:,}\n'
                       f'   Profit per flight (Easy): ${pro[3]:,}\n     Flights per day (Easy): {round(pro[4], 2)}\n      Profit per day (Easy): ${pro[5]:,}```'
                       f'Data and Profit Formula provided by Scuderia Airlines\' AC database.')
            await ctx.send(message)
            succ = True
        if injection:
            await ctx.send('SQL Injection detected. Stop it. Bad.')
        elif succ == False:
            await ctx.send('Aircraft not found. You can see all AC abbreviations with the command $seeall')
    
@bot.command(help = 'Compares two selected AC stats back to back. Usage: $compare <AC1> <AC2>', brief = 'Compares two selected AC stats back to back')
async def compare(ctx, plane1, plane2):
    if paused == False:
        counter('compare')
        succ1 = False
        succ2 = False
        injection = False
        if plane1[0] == "'" or plane2[0] == "'":
            injection = True
        ac1 = ''
        ac2 = ''
        if injection == False:
            try:
                acdb.reconnect(attempts = 5, delay = 0.5)
                cursor.execute(f"SELECT `manf`, `aircraft`, `rng`, `co2`, `fuel`, `spd`, `cap`, `model`, `cost` FROM `am4bot` WHERE `shortname` = '{plane1}'")
            except mysql.connector.Error as error:
                await ctx.send(f'Database error. Contact <@243007616714801157> if this happens.```python\n{error}```')    
            for ac in cursor:
                ac1 = ac
                succ1 = True

            try:
                cursor.execute(f"SELECT `manf`, `aircraft`, `rng`, `co2`, `fuel`, `spd`, `cap`, `model`, `cost` FROM `am4bot` WHERE `shortname` = '{plane2}'")
                acdb.close()
            except mysql.connector.Error as error:
                await ctx.send(f'Database error. Contact <@243007616714801157> if this happens.```python\n{error}```')
            for ac in cursor:
                ac2 = ac
                succ2 = True
        
        if injection == True:
            await ctx.send('SQL Injection detected. Stop it. Bad.')
        elif succ1 == False and succ2 == False:
            await ctx.send('Neither of the aircraft found. You can see all AC abbreviations with the command $seeall')    
        elif succ1 == False:
            await ctx.send('First aircraft not found. You can see all AC abbreviations with the command $seeall')
        elif succ2 == False:
            await ctx.send('Second aircraft not found. You can see all AC abbreviations with the command $seeall')
    
        pro1 = profit(ac1)
        pro2 = profit(ac2)
        
        
        await ctx.send(f'Comparison:\n**{ac1[1]}** vs. **{ac2[1]}**```python\nPrice: ${ac1[8]} M | ${ac2[8]} M\nCapacity: {ac1[6]} pax | {ac2[6]} pax\n'
                       f'Range: {ac1[2]} km | {ac2[2]} km\nSpeed: {ac1[5]} km/h | {ac2[5]} km/h\nFuel Consumption: {ac1[4]} lbs/km | {ac2[4]} lbs/km\n'
                       f'CO2 Emmisions: {ac1[3]} kg/p/km | {ac2[3]} kg/p/km\n'
                       f'Profit per flight (Realism): ${pro1[0]:,} | ${pro2[0]:,}\nFlights per day (Realism): {round(pro1[1], 2)} | {round(pro2[1], 2)}\n'
                       f'Profit per day (Realism): ${pro1[2]:,} | ${pro2[2]:,}\nProfit per flight (Easy): ${pro1[3]:,} | ${pro2[3]:,}\n'
                       f'Flights per day (Easy): {round(pro1[4], 2)} | {round(pro2[4], 2)}\nProfit per day (Easy): ${pro1[5]:,} | ${pro2[5]:,}'
                       f'```Data and profit formula provided by Scuderia Airlines')

@bot.command(help = 'Shows info of a selected airport. Usage: $airport <IATA or ICAO code of selected airport>', brief = 'Shows info of a selected airport.', enabled = False)
async def airport(ctx, code):
    if paused == False:
        counter('airport')
        succ = False
        nsucc = False
        name = ''
        injection = False
        if code[0] == "'":
            injection = True
        if injection == False:
            try:
                acdb.reconnect(attempts = 5, delay = 0.5)
                cursor.execute(f"SELECT `Name` FROM `airports` WHERE `ICAO` = '{code}' OR `IATA` = '{code}'")
                acdb.close()
            except mysql.connector.Error as error:
                await ctx.send(f'Database error. Contact <@243007616714801157> if this happens.```python\n{error}```')
            for ap in cursor:
                nsucc = True
                name = ap[0]
            try:
                acdb.reconnect(attempts = 5, delay = 0.5)
                cursor.execute(f"SELECT `id`, `arpt`, `region`, `IATA`, `ICAO`, `rwy`, `mrkt` FROM `arpt` WHERE `ICAO` = '{code}' OR `IATA` = '{code}'")
                acdb.close()
            except mysql.connector.Error as error:
                await ctx.send(f'Database error. Contact <@243007616714801157> if this happens.```python\n{error}```')
            for ap in cursor:
                succ = True
                if nsucc == False:
                    name = ap[1] + " Airport"
                await ctx.send(f'**{name.encode("iso-8859-1", "replace").decode("utf8", "replace")}** Stats```python\n         City: {ap[1]}, {ap[2]}'
                               f'\n         IATA: {ap[3]}\n         ICAO: {ap[4]}\nRunway Length: {ap[5]:,} ft.\n Market Value: {ap[6]}%\n```')    
            if succ == False:
                await ctx.send('Airport not found. You may have misspelled its IATA/ICAO or it isn\'t in the game.')

@bot.command()
async def search(ctx, value):
    if paused == False:
        counter('search')
        try:
            if len(value) >= 5:
                value = float(value) / 1000000
            elif float(value) < 0:
                await ctx.send('Value negative. Planes are never free!')
            else:
                value = float(value)
        except:
            await ctx.send(f'Value not a number. You can\'t have {value} dollars!')
        output = ''
        injection = False
        try:
            acdb.reconnect(attempts = 5, delay = 0.5)
            cursor.execute(f"SELECT `manf`, `aircraft`, `rng`, `co2`, `fuel`, `spd`, `cap`, `model`, `cost` FROM `am4bot` WHERE `cost` <= {float(value)} ORDER BY `Cost` DESC LIMIT 10")
            acdb.close()
        except mysql.connector.Error as error:
            await ctx.send(f'Database error. Contact <@243007616714801157> if this happens.```python\n{error}```')
        for ac in cursor:
                output = output + f'\n{ac[1]} ($info {ac[7]})\n${ac[8]}M; {ac[6]} pax; {ac[2]}km; {ac[5]}km/h; {ac[4]}l/km\n'
        if output != '':
            await ctx.send(f'Showing planes under **${value} Million**:```python\n{output}```')

def correct_channel(ctx):
    return ctx.message.channel.id == 554503485765189642, 484644663471636481

with open('ass.json') as infile:
    shit = json.load(infile)

@bot.command()
@commands.check(correct_channel)
@commands.cooldown(1, 900)
async def price(ctx, *cost):
    counter('price')
    role = discord.utils.get(ctx.guild.roles, name = 'PriceNotify')
    if len(cost) > 2:
        await ctx.send("Too many numbers in there!")
        price.reset_cooldown(ctx)
    elif len(cost) == 0:
        await ctx.send(f'Missing arguments. See $help for proper command usage.')
        price.reset_cooldown(ctx)
    else:
        output = f""
        fuel = 9999
        co2 = 9999
        for i in cost:
            if i[0] == 'f':
                try:
                    fuel = int(i.replace('f', ''))
                    output += f"Fuel price is ${fuel}. "
                except:
                    await ctx.send("Given price isn't a number!")
                    price.reset_cooldown(ctx)
            elif i[0] == 'c':
                try:
                    co2 = int(i.replace('c', ''))
                    output += f"CO2 price is ${co2}. "
                except:
                    await ctx.send("Given price isn't a number!")
                    price.reset_cooldown(ctx)
            else:
                await ctx.send("Formatting error.")
                price.reset_cooldown(ctx)
        if fuel <= 900 or co2 <= 140:
            await role.edit(mentionable = True)
            await ctx.send(output + role.mention + f" (Price sent by {ctx.message.author.display_name})")
            await role.edit(mentionable = False)
        elif output != f"":
            await ctx.send(output + f"(Price sent by {ctx.message.author.display_name})")
        else:
            pass
    
    shit[f'{time()}'] = {'fuel' : f'{fuel}', 'co2' : f'{co2}'}
    with open('ass.json', 'w') as outfile:
        json.dump(shit, outfile)
    
    await ctx.message.delete()
        
        
        

@bot.command(aliases = ['reset'], hidden = True)
@commands.has_role(646148607636144131)
async def restart(ctx):
    restart_program()

@bot.command(aliases = ['recon'], hidden = True)
@commands.has_role(646148607636144131)
async def reconnect(ctx):
    acdb.reconnect(attempts = 5, delay = 0.5)

@bot.command(hidden = True)
@commands.has_role(646148607636144131)
async def resetcool(ctx):
    price.reset_cooldown(ctx)

@bot.command(aliases = ['botinfo'], hidden = True)
async def version(ctx):
    if paused == False:
        await ctx.send(botinfo)

paused = False
@bot.command()
@commands.has_role(646148607636144131)
async def pause(ctx):
    global paused
    if paused:
        paused = False
        await ctx.send('Bot has been resumed')
    else:
        paused = True
        await ctx.send('Bot has been suspended')

    
bot.run('***REMOVED***')
