import discord
from discord import utils
from discord.ext import commands
import random

import os, sqlite3

import config
from data import db_session
from data.user import User

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

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
        emb.add_field(name='!sb', value='Игра Морской бой', inline=False)
        emb.add_field(name='!ball', value='Хрустальный шар', inline=False)

        await ctx.send(embed=emb)

    @bot.command(pass_context=True)
    async def timely(ctx):
        pass

    @bot.command(pass_context=True)
    async def balance(ctx):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id_discord == ctx.author.id).first()
        await ctx.send(user.balance)


    @bot.command(pass_context=True)
    async def rps(ctx):
        rpsGame = ['rock', 'paper', 'scissors']
        await ctx.send(f"Rock, paper, или scissors? Выбирай с умом...")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

        user_choice = (await bot.wait_for('message', check=check)).content.lower()

        comp_choice = random.choice(rpsGame)
        if user_choice == 'rock':
            if comp_choice == 'rock':
                await ctx.send(f'Хорошо, это довольно странно. Мы сыграли в ничью.\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Неплохо, но в этот раз я выиграл!!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(
                    f"Эх, ты победил меня. Этого больше не повториться!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}")

        elif user_choice == 'paper':
            if comp_choice == 'rock':
                await ctx.send(
                    f'Говорят, перо побеждает меч? Звучит, как бумага побеждает камень...\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(
                    f'Оу, ничья..\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(
                    f"Да уж, легкая была победа, ну ничего, может в следующий раз повезет.. \nТвой выбор: {user_choice}\nМой выбор: {comp_choice}")

        elif user_choice == 'scissors':
            if comp_choice == 'rock':
                await ctx.send(
                    f'ХА! Я ТОЛЬКО ЧТО УНИЧТОЖИЛ ТЕБЯ!! у меня камень!!\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Пфф.. >: |\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Ох, хорошо, Мы сыграли в ничью.\nТвой выбор: {user_choice}\nМой выбор: {comp_choice}")

    @bot.command(pass_context=True)
    async def coin(ctx):
        coinGame = ['up', 'down']
        await ctx.send(f"Up или down? Подумай перед выбором...")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in coinGame


        user_choice = (await bot.wait_for('message', check=check)).content.lower()
        comp_choice = random.choice(coinGame)
        if user_choice == 'up':
            if comp_choice == 'up':
                await ctx.send(f'Выпало: {comp_choice}\n Удача на вашей стороне!')
            elif comp_choice == 'down':
                await ctx.send(f'Выпало: {comp_choice}\n Эх, ну ничего, поражения делают нас сильней!!')

        if user_choice == 'down':
            if comp_choice == 'down':
                await ctx.send(f'Выпало: {comp_choice}\n Победа за вами!')
            elif comp_choice == 'up':
                await ctx.send(f'Выпало: {comp_choice}\n Неудача!')

    @bot.command(pass_context=True)
    async def roulette(ctx):
        rouletteGame = ['black', 'red', 'green']
        await ctx.send(f"Black, red или green? Выбирай с умом...")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rouletteGame

        user_choice = (await bot.wait_for('message', check=check)).content.lower()
        comp_choice = random.randint(0, 36)
        if user_choice == 'black':
            if comp_choice % 2 == 0 and comp_choice != 0:
                await ctx.send(f'Выпало: {comp_choice}\n Поздравляем, вы выиграли!')
            elif comp_choice % 2 == 1:
                await ctx.send(f'Выпало: {comp_choice}\n Неудача!')

        if user_choice == 'red':
            if comp_choice % 2 == 0 and comp_choice != 0:
                await ctx.send(f'Выпало: {comp_choice}\n Неудача!')
            elif comp_choice % 2 == 1:
                await ctx.send(f'Выпало: {comp_choice}\n Поздравляем, вы выиграли!')
        if user_choice == 'green':
            if comp_choice == 0:
                await ctx.send(f'Выпало: {comp_choice}\n ВАУ! Да вы везунчик, поздравляем с крупным выигрышим!')
            else:
                await ctx.send(f'Выпало: {comp_choice}\n Неудача!')

    @bot.command(pass_context=True)
    async def ball(ctx):
        phrases = ['Сконцентрируйся и спроси опять', 'Вероятнее всего','Вероятно нет',
                   'Определённо да','Спроси позже', 'Весьма сомнительно',
                   'Мне кажется — да', 'Мой ответ — нет', 'Можешь быть уверен в этом',
                   'Перспективы не очень хорошие', 'Сейчас нельзя предсказать',]
        emb = discord.Embed(title='Хрустальный шар!', color=discord.Color.blue())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        emb.add_field(name='Ответ:', value=random.choice(phrases))
        await ctx.send(embed=emb)


db_session.global_init("db/info.db")

bot.run(config.TOKEN)