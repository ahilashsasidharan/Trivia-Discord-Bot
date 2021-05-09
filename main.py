import discord
import os
import random
from replit import db
from pingtorun import keep_alive

previousnum = 1000

fhandle = open('question.txt')

status = 0
answer = ''
client = discord.Client()

@client.event

async def on_ready() :
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message) :
    if message.author == client.user:
        return

    if message.content.startswith('$trivia') :
        global previousnum
        global status
        global answer 
        status = 1
        question = ''
        outercount = 0
        num = random.randint(0, 29)
        while previousnum == num:
            num = random.randint(0, 29)
        previousnum = num
        fhandle.seek(0, 0)
        for line in fhandle:
            outercount = outercount + 1
            if (6*num) < outercount < (6*num + 6): 
                question = question + line
            if (6*num + 6) == outercount:
                answer = line.rstrip()
        await message.channel.send(question.rstrip())

    if message.content.startswith('$answer') :
        if status == 0:
            await message.channel.send("This Question Has Already Been Answered")
        else:
            idt = str(message.author.id)
            useranswer = message.content.split("$answer ")[1]
            if idt in db:
                print('')
            else:
                db[idt] = 0
            if useranswer == answer:
                status = 0
                await message.channel.send("You're Correct Great Job")
                db[idt] += 1
            else: 
                await message.channel.send("You Are Incorrect") 

    if message.content.startswith('$score'):
        embed = discord.Embed(color = discord.Colour.green())
        embed.set_author(name = 'Score')
        for comp in db.keys():
            temporaryid = await client.fetch_user(int(comp))
            embed.add_field(name = temporaryid, value = db[comp])
        await message.channel.send(embed=embed)

    if message.content.startswith('$end'):
        embed = discord.Embed(color = discord.Colour.green())
        embed.set_author(name = 'Results')
        for comp in db.keys():
            temporaryid = await client.fetch_user(int(comp))
            embed.add_field(name = temporaryid, value = db[comp])
        await message.channel.send(embed=embed)
        db.clear()

    if message.content.startswith('$commands'):
        embed = discord.Embed(color = discord.Colour.green())
        embed.set_author(name = 'Commands')
        embed.add_field(name = '$trivia', value = 'displays a question with four options a,b,c,d', inline = False)
        embed.add_field(name = '$answer', value = 'allows a user to answer a question displayed using $trivia', inline = False)
        embed.add_field(name = '$score', value = 'displays the score of users who have answered questions', inline = False)
        embed.add_field(name = '$end', value = 'displays final score of users who have answered a question and clears score data', inline = False)
        await message.channel.send(embed=embed)

keep_alive()
client.run(os.getenv('TOKEN'))
