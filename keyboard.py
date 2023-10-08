from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

parse_button = KeyboardButton("/parse")
start_button = KeyboardButton("/start")
lol_button = KeyboardButton('LOL')
all_parse_buttons = [KeyboardButton("LOL")]
LolGraphs_buttons = [KeyboardButton("Champloot"), KeyboardButton("Ru"), KeyboardButton("Pyke"),
                     [KeyboardButton("All"),
                      KeyboardButton("Rank"),
                      KeyboardButton("Score"),
                      KeyboardButton("Rating_score"),
                      KeyboardButton("Rating_score_country"),
                      KeyboardButton("Games_played"),
                      KeyboardButton("Winrate"),
                      KeyboardButton("KDA")]]

kb_LolGraphs_1_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[0])
kb_LolGraphs_2_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[1])
kb_LolGraphs_3_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[2])
kb_LolGraphs_4_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True)
for i in LolGraphs_buttons[3]:
 kb_LolGraphs_4_step_FSMParse.add(i)



all_kb = ReplyKeyboardMarkup(resize_keyboard=True)
all_kb.add(parse_button).add(start_button)

gamse_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(lol_button)