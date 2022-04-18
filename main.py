import datetime

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
                    if not db_sess.query(User).filter(User.id_discord == bot.user.id).first():
                        user = User()
                        user.id_discord = message.author.id
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
    @commands.has_permissions(administrator=True)
    async def help(ctx):
        emb = discord.Embed(title='Навигация по командам', color=discord.Color.green())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        emb.add_field(name='!timely', value='Выдача коинов раз в 6 часов', inline=False)
        emb.add_field(name='!balance', value='Узнать баланс', inline=False)
        emb.add_field(name='!top', value='Топ игроков', inline=False)
        emb.add_field(name='!rps', value='Мини-игра Камень-Ножницы-Бумага', inline=False)
        emb.add_field(name='!coin', value='Мини-игра Орел-Решка', inline=False)
        emb.add_field(name='!roulette', value='Мини-игра Рулетка', inline=False)
        emb.add_field(name='!capitals', value='Мини-игра Угадай столицу страны', inline=False)
        emb.add_field(name='!country', value='Мини-игра Угадай страну', inline=False)
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
                emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.red())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                              value=f"Неплохо, но в этот раз я выиграл!!")
                await ctx.send(embed=emb)

            elif comp_choice == 'scissors':
                emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.green())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                              value=f"Эх, ты победил меня. Этого больше не повториться!")
                await ctx.send(embed=emb)

        elif user_choice == 'paper':
            if comp_choice == 'rock':
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
                emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.red())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                              value=f"Да уж, легкая была победа, ну ничего, может в следующий раз повезет..")
                await ctx.send(embed=emb)

        elif user_choice == 'scissors':
            if comp_choice == 'rock':
                emb = discord.Embed(title='Камень-Ножницы-Бумага', color=discord.Color.red())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name=f'Твой выбор: {user_choice}\n Мой выбор: {comp_choice}',
                              value=f"ХА! Я ТОЛЬКО ЧТО УНИЧТОЖИЛ ТЕБЯ!! у меня камень!!")
                await ctx.send(embed=emb)
            elif comp_choice == 'paper':
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
                emb = discord.Embed(title='Рулетка', color=discord.Color.green())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name='Выпало:', value=f"{comp_choice} - Black, Поздравляем, вы выиграли!")
                await ctx.send(embed=emb)
            elif comp_choice % 2 == 1:
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
                emb = discord.Embed(title='Рулетка', color=discord.Color.red())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                if comp_choice == 0:
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Green, Да уж, не вовремя!!")
                    await ctx.send(embed=emb)
                else:
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Black, Неудача!")
                    await ctx.send(embed=emb)

            elif comp_choice % 2 == 1:
                emb = discord.Embed(title='Рулетка', color=discord.Color.green())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name='Выпало:', value=f"{comp_choice} - Red, Поздравляем, вы выиграли!")
                await ctx.send(embed=emb)

        if user_choice == 'green':
            if comp_choice == 0:
                emb = discord.Embed(title='Рулетка', color=discord.Color.green())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                emb.add_field(name='Выпало:', value=f"{comp_choice} - Green, ВАУ! Да вы везунчик, поздравляем с крупным выигрышим!")
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title='Рулетка', color=discord.Color.red())
                emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                if comp_choice % 2 == 0:
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Black, Неудача!")
                    await ctx.send(embed=emb)
                else:
                    emb.add_field(name='Выпало:', value=f"{comp_choice} - Red, Неудача!")
                    await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def capitals(ctx):
        pass

    @bot.command(pass_context=True)
    async def country(ctx):
        pass

    @bot.command(pass_context=True)
    async def ttt(ctx):
        pass

    @bot.command(pass_context=True)
    async def sb(ctx):
        dict[ctx.author.id] = SeaBattle(side=8, boats=[4, 3, 2, 1])

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


