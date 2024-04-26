import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler

from api_token import API_TOKEN
from data.game_data import GameData
from data.bot_files import BotPhrases
from data.generate_random_event import Room, get_random_dice


logging.basicConfig(
    filename='logs/project.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


keyboard_path = [
        [
            InlineKeyboardButton("⬅", callback_data="roomL"),
            InlineKeyboardButton("⬆", callback_data="roomF"),
            InlineKeyboardButton("➡", callback_data="roomR"),
            InlineKeyboardButton("⬇", callback_data="roomB")
            
        ],
        
    ]

markup_path = InlineKeyboardMarkup(keyboard_path)


keyboard_medicine = [
        [
            InlineKeyboardButton("Да ✅", callback_data="yes"),
            InlineKeyboardButton("Нет ❌", callback_data="no")
        ],
        
    ]

markup_medicine = InlineKeyboardMarkup(keyboard_medicine)


reply_keyboard_fight = [[KeyboardButton(text='/fight')]]
markup_fight = ReplyKeyboardMarkup(reply_keyboard_fight, one_time_keyboard=False)


reply_keyboard_start_game = [[KeyboardButton(text='/start_game')]]
markup_start_game = ReplyKeyboardMarkup(reply_keyboard_start_game, one_time_keyboard=False)


keyboard_weapon_choice = [
        [
            InlineKeyboardButton("Меч ⚔", callback_data="sword"),
            InlineKeyboardButton("Лук 🏹", callback_data="bow"),
            InlineKeyboardButton("Зелье 🧪", callback_data="potion")
        ]
]

markup_weapon_choice = InlineKeyboardMarkup(keyboard_weapon_choice)


stop_reply_keyboard = [['/stop']]
stop_markup = ReplyKeyboardMarkup(stop_reply_keyboard, one_time_keyboard=False)


# В словаре хранятся значения игровой сессии, ключом от которой является id пользователя  
users_game_data = {}
botResponses = BotPhrases()


async def start(update, context):
    chat_id = update.effective_message.chat_id
    await update.message.reply_text(botResponses.get_greeting(), reply_markup=markup_start_game)
    return "start"

    
async def help(update, context):
    await update.message.reply_text(botResponses.get_help())
    

async def stop(update, context):
    await update.message.reply_text("Игра завершена", reply_markup=markup_start_game)
    return "start"

    
async def rules(update, context):
    await update.message.reply_text(botResponses.get_rules())


async def start_game(update, context):
    chat_id = update.effective_message.chat_id    
    users_game_data[chat_id] = GameData()
        
    with open("data/images/лес.jpg", "rb") as photo:
        await context.bot.send_photo(chat_id, photo, caption=botResponses.get_start_game_phras(), reply_markup=ReplyKeyboardRemove())        
    
    await context.bot.send_message(chat_id, text=botResponses.get_choice_path(), reply_markup=markup_path)
    return "start_adventure"


async def choice_room(update, context):
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    
    # Переход героя в другую комнату и получение результата этого перехода
    result = users_game_data[chat_id].change_room(query.data)
    
    if not result:
        await query.edit_message_text(text=f"Этот тонель тоже завален, выберите другой", reply_markup=markup_path)
        return "start_adventure"
    
    if users_game_data[chat_id].kind_room == "Комната с монстром":
        await query.edit_message_text(text=f"Вы зашли в комнату с монстром")
        enemy = users_game_data[chat_id].enemy.kind
                  
        with open("data/images/" + enemy + ".jpg", "rb") as photo:
            await context.bot.send_photo(chat_id, photo, 
                                         caption=botResponses.get_beginning_fight(users_game_data[chat_id].enemy), 
                                         reply_markup=markup_fight)
        return "preparing_fight"
    
    if users_game_data[chat_id].kind_room == "Медпункт":
        with open("data/images/Медпункт.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id, photo)       
            
        await query.edit_message_text(text=f"Вы зашли в медпункт")
        await context.bot.send_message(chat_id, text=botResponses.get_need_kit(), reply_markup=markup_medicine)    
        return "need_get_kit"
    
    if users_game_data[chat_id].kind_room == "Кладовая":
        with open("data/images/кладовая.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id, photo)                
        await query.edit_message_text(text=f"Вы зашли в кладовую")
        found = users_game_data[chat_id].level.this_room.data
        await context.bot.send_message(chat_id, text=botResponses.get_weapon(found['item'], found['count_items']))
        users_game_data[chat_id].hero.add_weapon(found["item"], found["count_items"])
        await context.bot.send_message(chat_id, text=botResponses.get_choice_path(), reply_markup=markup_path)
        return "start_adventure"        
        
    if users_game_data[chat_id].kind_room == "Выход":
        
        with open("data/images/выход.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id, photo)        
        
        await query.edit_message_text(text=botResponses.get_exit_text())
        await context.bot.send_message(chat_id, text=botResponses.get_next_game_text(), reply_markup=markup_start_game)
        return "start"
    
    if users_game_data[chat_id].kind_room == "Пустая комната":
        await query.edit_message_text(text=f"Вы зашли в пустую пещеру")
        await context.bot.send_message(chat_id, text=botResponses.get_choice_path(), reply_markup=markup_path)
        return "start_adventure"
             
             
async def start_fight(update, context):
    chat_id = update.effective_message.chat_id
    
    await update.message.reply_text("Удачи в битве!")
        
    health = users_game_data[chat_id].hero.health
    count_bow = users_game_data[chat_id].hero.bow.count
    count_potion = users_game_data[chat_id].hero.potion.count
    
    await context.bot.send_message(chat_id, text=botResponses.get_arsenal_with_health_phrases(health, count_bow, count_potion), 
                                   reply_markup=markup_weapon_choice)    

    return "fight"

    
async def choice_weapon(update,  context):
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    
    count_bow = users_game_data[chat_id].hero.bow.count
    count_potion = users_game_data[chat_id].hero.potion.count    
    
    # Выбор оружия и результат выбора
    users_game_data[chat_id].hero.change_weapon(query.data)
    dice_result = get_random_dice()
    
    # В зависимости от значения игральной кости будет проведена атака
    result = users_game_data[chat_id].delivery_impact(dice_result)
    
    if not result:
        await query.edit_message_text(text="Этот тип оружия у вас закончился, выберите другой")
        await context.bot.send_message(chat_id, text=botResponses.get_arsenal_phrases(count_bow, count_potion), 
                                       reply_markup=markup_weapon_choice)            
        return "fight"
                
    # Получение результата боя
    result = users_game_data[chat_id].result_fight()
    
    await query.edit_message_text(text=f"Вы взяли {botResponses.get_weapon_name(query.data)}")
    
    if result[0] not in ["Противник победил", "Вы победили!"]: 
        await context.bot.send_message(chat_id, text=botResponses.get_post_fight_results(result))   
        await context.bot.send_message(chat_id, text=botResponses.get_arsenal_phrases(count_bow, count_potion), 
                                       reply_markup=markup_weapon_choice)    
        
        return "fight"
    
    if result[0] == "Вы победили!":
        await context.bot.send_message(chat_id, text=botResponses.get_post_fight_results(result), reply_markup=ReplyKeyboardRemove())  
        await context.bot.send_message(chat_id, text=botResponses.get_choice_path(), reply_markup=markup_path)
                
        return "start_adventure"
    
    elif result[0] == "Противник победил":
        await context.bot.send_message(chat_id, text=botResponses.get_post_fight_results(result), reply_markup=ReplyKeyboardRemove())
        await context.bot.send_message(chat_id, text=botResponses.get_hero_lost_text(), reply_markup=markup_start_game)
        return "start"
                
                
async def need_get_kit(update, context):
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    result_choise = ""
    if query.data == "no":
        result_choise = botResponses.not_get_kit()
    else:
        dice_result = get_random_dice()
        result_choise = botResponses.get_kit(dice_result)
        users_game_data[chat_id].hero.add_health(dice_result)
    
    await query.edit_message_text(text=result_choise)
    await context.bot.send_message(chat_id, text=botResponses.get_choice_path(), reply_markup=markup_path)
    return "start_adventure"
        

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            "start": [CommandHandler('start_game', start_game)],
            "preparing_fight": [CommandHandler('fight', start_fight)],
            'fight': [CallbackQueryHandler(choice_weapon)],
            "start_adventure": [CallbackQueryHandler(choice_room)],
            "need_get_kit": [CallbackQueryHandler(need_get_kit)]
        },
        fallbacks=[CommandHandler('stop', stop), CommandHandler('help', help), CommandHandler('rules', rules)]
    )


def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(conv_handler)    
    application.run_polling()


if __name__ == '__main__':
    main()