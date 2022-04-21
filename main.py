import datetime
import time

import discord
from discord import utils
from discord.ext import commands
import random

import config
from data import db_session
from data.user import User
from sea_battle import SeaBattle

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.event
async def on_ready():
  print('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_raw_reaction_add(payload):
        if payload.message_id == config.POST_ID:
            channel = bot.get_channel(payload.channel_id)  # получаем объект канала
            message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
            member = payload.member

            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)
                if role.id == 958387381067739156:
                    print(1)
                    db_sess = db_session.create_session()
                    if not db_sess.query(User).filter(User.id_discord == payload.user_id).first():
                        user = User()
                        user.id_discord = payload.user_id
                        db_sess.add(user)
                        db_sess.commit()

                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))


            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)  # получаем объект канала
    message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
    member = list(filter(lambda x: x.id == payload.user_id, bot.get_all_members()))[0]

    try:
        emoji = str(payload.emoji)  # эмоджик который выбрал юзер
        role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)

        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))

dict ={}


class Client(commands.Bot):
    @bot.command(pass_context=True)
    async def help(ctx):
        emb = discord.Embed(title='Навигация по командам', color=discord.Color.green())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        emb.add_field(name='!timely', value='Выдача коинов раз в 6 часов', inline=False)
        emb.add_field(name='!balance', value='Узнать баланс', inline=False)
        #emb.add_field(name='!top', value='Топ игроков', inline=False)
        emb.add_field(name='!rps', value='Мини-игра Камень-Ножницы-Бумага', inline=False)
        emb.add_field(name='!coin', value='Мини-игра Орел-Решка', inline=False)
        emb.add_field(name='!roulette', value='Мини-игра Рулетка', inline=False)
        #emb.add_field(name='!capitals', value='Мини-игра Угадай столицу страны', inline=False)
        #emb.add_field(name='!country', value='Мини-игра Угадай страну', inline=False)
        emb.add_field(name='!ttt', value='Мини-игра Крестики-Нолики', inline=False)
        emb.add_field(name='!place', value='Команда для игры в Крестики-Нолики (от 1 до 9)', inline=False)
        emb.add_field(name='!sb', value='Игра Морской бой', inline=False)
        emb.add_field(name='!ball', value='Хрустальный шар', inline=False)

        await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def timely(ctx):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id_discord == ctx.author.id, ).first()
        sub = datetime.datetime.now() - user.give_coin
        if sub >= datetime.timedelta(hours=6):
            user.balance += 1250
            user.give_coin = datetime.datetime.now()
            db_sess.commit()
            emb = discord.Embed(title='Баланс', color=discord.Color.green())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Успешно', value='Вы получили свои 1250', inline=False)
            emb.add_field(name='Ваш баланс:', value=user.balance, inline=False)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title='Ошибка', color=discord.Color.red())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Неудачно', value='Время после последнего запроса, не вышло.', inline=False)
            emb.add_field(name='Ваш баланс:', value=user.balance, inline=False)
            await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def balance(ctx):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id_discord == ctx.author.id).first()
        emb = discord.Embed(title='Баланс', color=discord.Color.green())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        emb.add_field(name='Ваш баланс:', value=user.balance)
        await ctx.send(embed=emb)


    @bot.command(pass_context=True)
    async def rps(ctx):
        rpsGame = ['rock', 'paper', 'scissors']
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id_discord == ctx.author.id).first()
            bet = int(ctx.message.content.split()[1])
            if user.balance < bet or bet < 0:
                raise Exception()


            emb = discord.Embed(title='Выбор...', color=discord.Color.light_grey())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Выберите:', value="Rock, paper, или scissors? Выбирай с умом...")
            await ctx.send(embed=emb)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

            user_choice = (await bot.wait_for('message', check=check)).content.lower()

            comp_choice = random.choice(rpsGame)
            if user_choice == 'rock':
                if comp_choice == 'rock':
                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.gold())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Хорошо, это довольно странно. Мы сыграли в ничью.")
                    await ctx.send(embed=emb)

                elif comp_choice == 'paper':
                    user.balance -= bet

                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Неплохо, но в этот раз я выиграл!!")
                    await ctx.send(embed=emb)

                elif comp_choice == 'scissors':
                    user.balance += bet

                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Эх, ты победил меня. Этого больше не повториться!")
                    await ctx.send(embed=emb)

            elif user_choice == 'paper':
                if comp_choice == 'rock':
                    user.balance += bet

                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Говорят, перо побеждает меч? Звучит, как бумага побеждает камень...")
                    await ctx.send(embed=emb)
                elif comp_choice == 'paper':
                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.gold())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Оу, ничья..")
                    await ctx.send(embed=emb)
                elif comp_choice == 'scissors':
                    user.balance -= bet

                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Да уж, легкая была победа, ну ничего, может в следующий раз повезет..")
                    await ctx.send(embed=emb)

            elif user_choice == 'scissors':
                if comp_choice == 'rock':
                    user.balance -= bet

                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"ХА! Я ТОЛЬКО ЧТО УНИЧТОЖИЛ ТЕБЯ!! у меня камень!!")
                    await ctx.send(embed=emb)
                elif comp_choice == 'paper':
                    user.balance += bet

                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Пфф..")
                    await ctx.send(embed=emb)
                elif comp_choice == 'scissors':
                    emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.gold())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                                  value=f"Ох, хорошо, Мы сыграли в ничью.")
                    await ctx.send(embed=emb)
            db_sess.commit()
        except Exception as e:
            emb = discord.Embed(title='Ошибка', color=discord.Color.red())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Неудачно:', value="Вторым значением введите целое число")
            await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def coin(ctx):
        coinGame = ['up', 'down']
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id_discord == ctx.author.id).first()
            bet = int(ctx.message.content.split()[1])
            if user.balance < bet or bet < 0:
                raise Exception()

            emb = discord.Embed(title='Выбор...', color=discord.Color.light_grey())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Выберите:', value="Up или Down, выбор за вами...")
            await ctx.send(embed=emb)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in coinGame


            user_choice = (await bot.wait_for('message', check=check)).content.lower()
            comp_choice = random.choice(coinGame)
            if user_choice == 'up':
                if comp_choice == 'up':
                    user.balance += bet

                    emb = discord.Embed(title='Монетка', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice}, Удача на вашей стороне!")
                    emb.set_image(
                        url='https://cdn.discordapp.com/attachments/899632867452256297/962694644938997790/-155555.png')
                    await ctx.send(embed=emb)
                elif comp_choice == 'down':
                    user.balance -= bet

                    emb = discord.Embed(title='Монетка', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice}, Неудача!")
                    emb.set_image(
                        url='https://cdn.discordapp.com/attachments/899632867452256297/962694645169655808/-166666666.png')
                    await ctx.send(embed=emb)

            if user_choice == 'down':
                if comp_choice == 'down':
                    user.balance += bet

                    emb = discord.Embed(title='Монетка', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice}, Удача на вашей стороне!")
                    emb.set_image(
                        url='https://cdn.discordapp.com/attachments/899632867452256297/962694645169655808/-166666666.png')
                    await ctx.send(embed=emb)
                elif comp_choice == 'up':
                    user.balance -= bet

                    emb = discord.Embed(title='Монетка', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice}, Неудача!")
                    emb.set_image(
                        url='https://cdn.discordapp.com/attachments/899632867452256297/962694644938997790/-155555.png')
                    await ctx.send(embed=emb)
            db_sess.commit()
        except Exception as e:
            emb = discord.Embed(title='Ошибка', color=discord.Color.red())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Неудачно:', value="Вторым значением введите целое число")
            await ctx.send(embed=emb)


    @bot.command(pass_context=True)
    async def roulette(ctx):
        rouletteGame = ['black', 'red', 'green']
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id_discord == ctx.author.id).first()
            bet = int(ctx.message.content.split()[1])
            if user.balance < bet or bet < 0:
                raise Exception()
            emb = discord.Embed(title='Выбор...', color=discord.Color.light_grey())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Выберите:', value="Black, red или green выбирай с умом...")
            await ctx.send(embed=emb)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rouletteGame

            user_choice = (await bot.wait_for('message', check=check)).content.lower()
            comp_choice = random.randint(0, 36)
            if user_choice == 'black':
                if comp_choice % 2 == 0 and comp_choice != 0:
                    user.balance += bet

                    emb = discord.Embed(title='Рулетка', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Black, Поздравляем, вы выиграли!")
                    await ctx.send(embed=emb)
                elif comp_choice % 2 == 1:
                    user.balance -= bet

                    emb = discord.Embed(title='Рулетка', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    if comp_choice == 0:
                        emb.add_field(name='Выпало:', value=f"{comp_choice} - Green, Да уж, не вовремя!!")
                        await ctx.send(embed=emb)
                    else:
                        emb.add_field(name='Выпало:', value=f"{comp_choice} - Red, Неудача!")
                        await ctx.send(embed=emb)

            if user_choice == 'red':
                if comp_choice % 2 == 0:
                    user.balance -= bet

                    emb = discord.Embed(title='Рулетка', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    if comp_choice == 0:
                        emb.add_field(name='Выпало:', value=f"{comp_choice} - Green, Да уж, не вовремя!!")
                        await ctx.send(embed=emb)
                    else:
                        emb.add_field(name='Выпало:', value=f"{comp_choice} - Black, Неудача!")
                        await ctx.send(embed=emb)

                elif comp_choice % 2 == 1:
                    user.balance += bet

                    emb = discord.Embed(title='Рулетка', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Red, Поздравляем, вы выиграли!")
                    await ctx.send(embed=emb)

            if user_choice == 'green':
                if comp_choice == 0:
                    user.balance += bet * 14

                    emb = discord.Embed(title='Рулетка', color=discord.Color.green())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Green, ВАУ! Да вы везунчик, поздравляем с крупным выигрышим!")
                    await ctx.send(embed=emb)
                else:
                    user.balance -= bet

                    emb = discord.Embed(title='Рулетка', color=discord.Color.red())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    if comp_choice % 2 == 0:
                        emb.add_field(name='Выпало:', value=f"{comp_choice} - Black, Неудача!")
                        await ctx.send(embed=emb)
                    else:
                        emb.add_field(name='Выпало:', value=f"{comp_choice} - Red, Неудача!")
                        await ctx.send(embed=emb)
            db_sess.commit()
        except Exception as e:
            emb = discord.Embed(title='Ошибка', color=discord.Color.red())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Неудачно:', value="Вторым значением введите целое число")
            await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def capitals(ctx):
        pass

    @bot.command(pass_context=True)
    async def country(ctx):
        pass

    @bot.command()
    async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # вывод доски
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # кто начинает первый
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("Ваш <@" + str(player1.id) + "> ход.")
            elif num == 2:
                turn = player2
                await ctx.send("Ваш <@" + str(player2.id) + "> ход.")
        else:
            await ctx.send("Игра уже началась! Когда закончиться, тогда вы сможете начать новую игру.")

    @bot.command()
    async def place(ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        def checkWinner(winningConditions, mark):
            global gameOver
            for condition in winningConditions:
                if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                    gameOver = True

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # вывод доски
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # смена сторон
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Выберите число от 1 до 9 (включительно) и не выбранную плитку")
            else:
                await ctx.send("Сейчас не ваш ход")
        else:
            await ctx.send("Пожалуйста, начните новую игру командой !tictactoe.")



    @tictactoe.error
    async def tictactoe_error(ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Пожалуйста, укажите 2 участников через @")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Не забудь упоминуть игроков (ie. <@688534433879556134>).")

    @place.error
    async def place_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Пожалуйста, введите позицию, которую вы хотели бы отметить")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Пожалуйста, не забудьте ввести целое число")

    @bot.command(pass_context=True)
    async def sb(ctx):
        dict[ctx.author.id] = SeaBattle(side=2, boats=[1])
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id_discord == ctx.author.id).first()
            bet = int(ctx.message.content.split()[1])
            if user.balance < bet or bet < 0:
                raise Exception()

            emb = discord.Embed(title='Какие параметры игры применить?', color=discord.Color.light_grey())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Выберите:', value="3 - классика (ставка * 1)\n"
                                                  "1 - поле 6*6, 4 1-палубных, 2 2-палубных, 1 3-палубный "
                                                  "(ставка * 0.3)\n"
                                                  "2 - поле 8*8, 4 1-палубных, 3 2-палубных, 2 3-палубных, 1 4-палубный"
                                                  " (ставка * 0.7)\n"
                                                  "4 - поле 10*10, 5 1-палубных, 4 2-палубных, ..., 1 5-палубный "
                                                  "(ставка * 1.5)\n"
                                                  "5 - поле 14*14, 6 1-палубных, 5 2-палубных, ..., 1 6-палубный "
                                                  "(ставка * 2)\n"
                                                  "6 - поле 16*16, 7 1-палубных, 6 2-палубных, ..., 1 7-палубный "
                                                  "(ставка * 3)\n"
                                                  "7 - поле 20*20, 8 1-палубных, 7 2-палубных, ..., 1 8-палубный "
                                                  "(ставка * 6)\n"
                                                  "8 - поле 10*10, 6 1-палубных, 9 2-палубных, 2 3-палубных "
                                                  "(ставка * 1)\n"
                                                  "9 - поле 15*15, 7 1-палубных, 16 2-палубных, 8 3-палубных "
                                                  "(ставка * 1.5)")
            vars_1 = [[6, [4, 2, 1], 1.3], [8, [4, 3, 2, 1], 1.7], [10, [4, 3, 2, 1], 2], [10, [5, 4, 3, 2, 1], 2.5],
                      [14, [6, 5, 4, 3, 2, 1], 3], [16, [7, 6, 5, 4, 3, 2, 1], 4], [20, [8, 7, 6, 5, 4, 3, 2, 1], 7],
                      [10, [6, 9, 2], 2], [15, [7, 16, 8], 2.5]]
            await ctx.send(embed=emb)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower().isdigit() and int(msg.content.lower()) > 0 and int(msg.content.lower()) < 10

            def check2(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and " " in msg.content.lower() and len(msg.content.lower().split(" ")) == 2 and msg.content.lower().split(" ")[0].isdigit() and msg.content.lower().split(" ")[1].isdigit() and int(msg.content.lower().split(" ")[0]) > 0 and int(msg.content.lower().split(" ")[0]) <= vars_1[int(user_num) - 1][0] and int(msg.content.lower().split(" ")[1]) > 0 and int(msg.content.lower().split(" ")[1]) <= vars_1[int(user_num) - 1][0] or msg.content.lower() == "stop"

            user_num = (await bot.wait_for('message', check=check)).content.lower()
            dict[ctx.author.id] = SeaBattle(side=vars_1[int(user_num) - 1][0], boats=vars_1[int(user_num) - 1][1])
            game = dict[ctx.author.id]
            await ctx.send('Игра запущена! для досрочного завершения отправте "stop", но тогда ваша ставка сгорит')

            def pr(f, who):
                b = (f.draw(my_map=False, map_shots=True)).split("\n")
                a = (f.draw(my_map=False, map_shots=False)).split("\n")
                a[0] = a[0] + " "
                str_22 = ""
                if who:
                    for q in range(len(a)):
                        str_22 += a[q]
                        str_22 += "\n"
                else:
                    for q in range(len(a)):
                        str_22 += b[q]
                        str_22 += "\n"
                str_22 = "```excel\n" + str_22 + "\n```"
                return str_22

            await ctx.send("Ваше поле:")
            await ctx.send(pr(game, True))
            await ctx.send("Поле ИИ:")
            await ctx.send(pr(game, False))
            emb = discord.Embed(title="Стреляйте!", color=discord.Color.gold())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            await ctx.send(embed=emb)

            while 1:
                try:

                    hit = (await bot.wait_for('message', check=check2)).content.lower()
                    if hit == "stop":
                        emb = discord.Embed(title="Игра прервана, ваша ставка сгорела", color=discord.Color.red())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        user.balance -= bet
                        emb = discord.Embed(title="Ваш баланс " + str(user.balance), color=discord.Color.red())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        break
                    hit = hit.split(" ")
                    stat = game.enemy_shot(int(hit[0]), int(hit[1]))
                    if stat == "miss":

                        emb = discord.Embed(title="Мимо, Ход ИИ", color=discord.Color.blue())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        # карта печатается потом
                    exit_t = False
                    while stat == "hit" or stat == "kill" or stat == "not_shot_already_hit" or \
                            stat == "not_shot_no_ships" or stat == "input_error":
                        if stat == "hit" or stat == "kill":
                            if stat == "hit":

                                emb = discord.Embed(title="Отличное попадание! Ваш ход", color=discord.Color.gold())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                                await ctx.send(pr(game, False))
                            if stat == "kill":

                                emb = discord.Embed(title="Корабль потоплен! Ваш ход", color=discord.Color.gold())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                                await ctx.send(pr(game, False))
                        if stat == "not_shot_already_hit" or stat == "not_shot_no_ships" or stat == "input_error":
                            if stat == "not_shot_already_hit":

                                emb = discord.Embed(title="Ошибка! Сюда уже стреляли", color=discord.Color.orange())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                            elif stat == "not_shot_no_ships":

                                emb = discord.Embed(title="Ошибка! Здесь нет корабля", color=discord.Color.orange())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                            else:

                                emb = discord.Embed(title="Ошибка ввода", color=discord.Color.orange())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                            await ctx.send(pr(game, False))

                        hit = (await bot.wait_for('message', check=check2)).content.lower()
                        if hit == "stop":
                            emb = discord.Embed(title="Игра прервана, ваша ставка сгорела", color=discord.Color.red())
                            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                            await ctx.send(embed=emb)

                            user.balance -= bet
                            emb = discord.Embed(title="Ваш баланс " + str(user.balance), color=discord.Color.red())
                            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                            await ctx.send(embed=emb)

                            exit_t = True
                            break
                        hit = hit.split(" ")

                        stat = game.enemy_shot(int(hit[0]), int(hit[1]))
                        if stat == "miss":

                            emb = discord.Embed(title="Мимо, ход ИИ", color=discord.Color.blue())
                            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                            await ctx.send(embed=emb)

                    if exit_t:
                        break

                    if stat == "game_over":

                        emb = discord.Embed(title="Вы выиграли! Поздравляем)", color=discord.Color.green())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        await ctx.send(pr(game, False))

                        user.balance += int(vars_1[int(user_num) - 1][-1] * bet // 1)
                        emb = discord.Embed(
                            title="Засчитано " + str(int(vars_1[int(user_num) - 1][-1] * bet // 1)) + ", ваш баланс " + str(
                                user.balance), color=discord.Color.green())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        break

                    stat = game.my_shot
                    if stat == "miss":

                        await ctx.send(pr(game, True))

                        emb = discord.Embed(title="ИИ стреляет " + str(game.get_last_my_shot()[0]) + " " + str(game.get_last_my_shot()[1]) + " - мимо, ваш ход", color=discord.Color.gold())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        await ctx.send(pr(game, False))
                    while stat == "hit" or stat == "kill" or stat == "not_shot_already_hit" or \
                            stat == "not_shot_no_ships" or stat == "input_error":
                        if stat == "hit" or stat == "kill":
                            if stat == "hit":

                                await ctx.send(pr(game, True))

                                emb = discord.Embed(title="В наш корабль попали! " + "ИИ стрелял " + str(game.get_last_my_shot()[0]) + " " + str(game.get_last_my_shot()[1]) + ". Ход ИИ", color=discord.Color.blue())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                            if stat == "kill":
                                await ctx.send(pr(game, True))

                                emb = discord.Embed(title="Наш корабль потоплен! " + "ИИ стрелял " + str(game.get_last_my_shot()[0]) + " " + str(game.get_last_my_shot()[1]) + ". Ход ИИ", color=discord.Color.blue())
                                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                                await ctx.send(embed=emb)

                            time.sleep(1)
                        stat = game.my_shot
                        if stat == "miss":

                            await ctx.send(pr(game, True))

                            emb = discord.Embed(title="ИИ стреляет " + str(game.get_last_my_shot()[0]) + " " + str(
                                game.get_last_my_shot()[1]) + " - мимо, ваш ход", color=discord.Color.gold())
                            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                            await ctx.send(embed=emb)

                            await ctx.send(pr(game, False))
                    if stat == "game_over":

                        emb = discord.Embed(title="ИИ выиграл! Что ж, повезёт в следующий раз", color=discord.Color.red())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        await ctx.send(pr(game, True))

                        user.balance -= bet
                        emb = discord.Embed(title="Вы потеряли " + str(bet) + ", ваш баланс " + str(user.balance),
                                            color=discord.Color.red())
                        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                        await ctx.send(embed=emb)

                        break

                except:
                    emb = discord.Embed(title="Ошибка ввода 1", color=discord.Color.orange())
                    emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                    await ctx.send(embed=emb)

                    await ctx.send(pr(game))
            db_sess.commit()
        except Exception as e:

            emb = discord.Embed(title='Ошибка', color=discord.Color.orange())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Исключение:', value="Что-то пошло не так, пожалуйста, попробуйте ещё раз")
            await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def shot(ctx):
        try:
            coord_x = int(ctx.message.content.split()[1])
            coord_y = int(ctx.message.content.split()[2])
            game = dict[ctx.author.id]

            game.enemy_shot(coord_x, coord_y)
            game.my_shot()

            game.draw()
        except Exception:
            emb = discord.Embed(title='Ошибка', color=discord.Color.red())
            emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
            emb.add_field(name='Неудачно:', value="введите координаты ячейки поля через пробел")
            await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def ball(ctx):
        phrases = ['Сконцентрируйся и спроси опять', 'Вероятнее всего','Вероятно нет',
                   'Определённо да','Спроси позже', 'Весьма сомнительно',
                   'Мне кажется — да', 'Мой ответ — нет', 'Можешь быть уверен в этом',
                   'Перспективы не очень хорошие', 'Сейчас нельзя предсказать',]
        emb = discord.Embed(title='Хрустальный шар!', color=discord.Color.blue())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        emb.add_field(name='Ответ:', value=random.choice(phrases))
        emb.set_image(url='https://cdn.discordapp.com/attachments/399095328596557828/964228300828463214/Magic_eight_ball.png')
        await ctx.send(embed=emb)


db_session.global_init("db/info.db")

bot.run(config.TOKEN)


