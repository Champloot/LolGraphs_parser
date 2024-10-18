from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

parse_button = KeyboardButton("/parse")
start_button = KeyboardButton("/start")
cancel_button = KeyboardButton("/cancel")
all_parse_buttons = KeyboardButton("LOL_Graphs")
LolGraphs_buttons = [KeyboardButton("Paranoic"), KeyboardButton("SVIN"), KeyboardButton("Ru"), KeyboardButton("Pyke"),
                     [KeyboardButton("All"),
                      KeyboardButton("Rank"),
                      KeyboardButton("Score"),
                      KeyboardButton("Rating_score"),
                      KeyboardButton("Rating_score_country"),
                      KeyboardButton("Games_played"),
                      KeyboardButton("Winrate"),
                      KeyboardButton("KDA")]]

kb_LolGraphs_1_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[0]).add(cancel_button)
kb_LolGraphs_2_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[1]).add(cancel_button)
kb_LolGraphs_3_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[2]).add(cancel_button)
kb_LolGraphs_4_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(LolGraphs_buttons[3]).add(cancel_button)
kb_LolGraphs_5_step_FSMParse = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_button)
for i in LolGraphs_buttons[4]:
    kb_LolGraphs_5_step_FSMParse.add(i)

all_kb = ReplyKeyboardMarkup(resize_keyboard=True)
all_kb.add(parse_button).add(start_button)

games_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(all_parse_buttons)
