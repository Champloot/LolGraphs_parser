import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bs4 import BeautifulSoup

from keyboard import *


# Основная функция

def LeagueGraphs_parse(data_0: dict) -> str:
    data = {k: v.lower() for k, v in data_0.items()}
    lolgraphs_url = f"https://www.leagueofgraphs.com/summoner/champions/{data['country']}/{data['player']}-{data['postfix']}"
    headers = {"Accept": "*/*",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    req = requests.get(url=lolgraphs_url, headers=headers)

    soup = BeautifulSoup(req.text, 'lxml')
    try:
        champ_column = soup.find(class_='summoner_champions_details_table').find_all('tr')
    except AttributeError:
        return "Check data!"
    answer = {}
    for champ in champ_column[1:]:
        all_about_champ = champ.find_all('td')
        champ_name = all_about_champ[0].find('span', class_='name').text.strip().lower()
        about_champ = all_about_champ[0].find('div', class_='relative requireTooltip').get('tooltip')

        champ_rank, champ_score = ('Mastery level: ' + about_champ[about_champ.find('Mastery Level') + 14],
                                   about_champ[about_champ.find('Points:'):about_champ.rfind('<br/><br/>')])

        rating_score, rating_score_country = None, None
        if 'Rank - Mastery Points:' in about_champ:
            rating_score, rating_score_country = [
                about_champ[about_champ.find('Rank - Mastery Points:'):about_champ.rfind('<br/>')],
                about_champ[about_champ.find(f"Rank - Mastery Points ({data['country'][:-1].upper()}):"):]]

        games_played = 'Played: ' + str(int(all_about_champ[1].get('data-sort-value')))
        h = round(float(all_about_champ[2].find('progressbar').get('data-value')), 2)
        variants_winrate = (
            str(h + 99.0)[:3] + '%', str(h)[2:] + '%', str(h)[2:4] + '%', str(h)[2:] + '0%', 'error -_-')
        winrate = 'Winrate: '
        if str(h)[0] == '1':
            winrate += variants_winrate[0]
        elif str(h)[2] == '0':
            winrate += variants_winrate[1]
        elif len(str(h)[2:]) == 2:
            winrate += variants_winrate[2]
        elif len(str(h)[2:]) == 1:
            winrate += variants_winrate[3]
        else:
            winrate = variants_winrate[4]
        del (h)

        champ_KDA = f'KDA: {float(champ.find("span", class_="kills").text.strip())} | ' \
                    f'{float(champ.find("span", class_="deaths").text.strip())} | ' \
                    f'{float(champ.find("span", class_="assists").text.strip())}'

        answer[f'{champ_name}'] = {'champ_name': "Champion: " + champ_name.title(),
                                   'rank': champ_rank,
                                   'score': champ_score,
                                   'rating_score': rating_score,
                                   f'rating_score{data["country"]}': rating_score_country,
                                   'games_played': games_played,
                                   'winrate': winrate,
                                   'kda': champ_KDA,
                                   'all': f'Champion: {champ_name.title()}\n'
                                          f'{champ_rank}\n'
                                          f'{champ_score}\n'
                                          f'{rating_score}\n'
                                          f'{rating_score_country}\n'
                                          f'{games_played}\n'
                                          f'{winrate}\n'
                                          f'{champ_KDA}\n'}
    try:
        return answer[f"{data['champ']}"][f"{data['champ_parameter']}"]
    except KeyError:
        return "Check data!"


async def cmd_start(message: types.Message):
    await message.reply('Hi!', reply_markup=all_kb)


# Общая FSM
class FSMWhat_parse(StatesGroup):
    what_parse = State()


# Lol FSM
class FSMParse_LolGraphs(StatesGroup):
    which_player_LG = State()
    which_postfix_LG = State()
    country_LG = State()
    what_champion_LG = State()
    what_champion_parameter_LG = State()


# Функция-стартер
async def what_parse_start(message: types.Message):
    await FSMWhat_parse.what_parse.set()
    await message.reply('Что парсить?', reply_markup=games_kb)


# Функция-роутер
async def what_parse(message: types.Message):
    if message.text.lower() == "lol_graphs":
        await LGparse_cmd_start(message)


'''League of Legends'''


# 1-ая стадия - ник
async def LGparse_cmd_start(message: types.Message):
    await FSMParse_LolGraphs.which_player_LG.set()
    await message.reply('Ник игрока ->', reply_markup=kb_LolGraphs_1_step_FSMParse)


# Промежуточная стадия - отмена
async def LGparse_cancel_handeler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отмена')


# 2-ая стадия - постфикс ника (после решетки)
async def LGparse_which_player(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['player'] = message.text
    await FSMParse_LolGraphs.next()
    await message.reply('Постфикс ника (то что после решетки)?', reply_markup=kb_LolGraphs_2_step_FSMParse)


# 2-ая стадия - сервер
async def LGparse_what_postfix(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['postfix'] = message.text
    await FSMParse_LolGraphs.next()
    await message.reply('Сервер какой страны?', reply_markup=kb_LolGraphs_3_step_FSMParse)


# 3-ья стадия - персонаж
async def LGparse_which_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await FSMParse_LolGraphs.next()
    await message.reply('Какой чемпион?', reply_markup=kb_LolGraphs_4_step_FSMParse)


# 4-ая стадия - параметр
async def LGparse_what_champion(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['champ'] = message.text
    await FSMParse_LolGraphs.next()
    await message.reply('Какой его параметр?', reply_markup=kb_LolGraphs_5_step_FSMParse)


# 5-ая стадия - конец
async def LGparse_champ_parameter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['champ_parameter'] = message.text
    async with state.proxy() as data:
        await message.reply(text=LeagueGraphs_parse(data))
    await state.finish()


# Регистрация общих функций
def register_handlers_all_parse(dp: Dispatcher):
    dp.register_message_handler(what_parse_start, state="*", commands='parse')
    dp.register_message_handler(what_parse, state=FSMWhat_parse.what_parse)


# Регистрация функций Lol
def register_handlers_parse(dp: Dispatcher):
    dp.register_message_handler(LGparse_cancel_handeler, state="*", commands='cancel')
    dp.register_message_handler(LGparse_which_player, state=FSMParse_LolGraphs.which_player_LG)
    dp.register_message_handler(LGparse_what_postfix, state=FSMParse_LolGraphs.which_postfix_LG)
    dp.register_message_handler(LGparse_which_country, state=FSMParse_LolGraphs.country_LG)
    dp.register_message_handler(LGparse_what_champion, state=FSMParse_LolGraphs.what_champion_LG)
    dp.register_message_handler(LGparse_champ_parameter, state=FSMParse_LolGraphs.what_champion_parameter_LG)
    dp.register_message_handler(cmd_start, commands='start')
