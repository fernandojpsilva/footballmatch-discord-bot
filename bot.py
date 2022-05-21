import discord

TOKEN = ''

client = discord.Client()


def requestType(msg):
    if msg.startswith('!lol '):
        return 'lol_summoner'
    elif msg.startswith('!lolgame'):
        return 'lolgame'
    elif msg.startswith('!help'):
        return 'help'
    else:
        return False


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content).lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'testing':
        if requestType(user_message) == 'lol_summoner':
            await message.channel.send("Hi")
            return
        elif requestType(user_message) == 'lolgame':
            await message.channel.send("Hi2")
            return
        elif requestType(user_message) == 'help':
            await message.channel.send('!lol [username] - para veres o teu perfil\n'
                                       '!lolgame [username] - para ver informação ingame')
            return


client.run(TOKEN)
