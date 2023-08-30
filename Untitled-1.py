import logging, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram. dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram. types import InlineKeyboardMarkup, InlineKeyboardButton
from lao import *
from random import randint
TOKEN = os.getenv('ur token')
logging.basicConfig(level=logging. INFO)
bot = Bot(token='ur token')
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = [5041207042]
films = {
    "Правила": {
        "rules": "Потрібно відгадати слово, яке складається з 5 букв, є n спроб відгадати, якщо слово неправильне, воно показує, які букви правлильні та чи на своєму місці.",
    },
    "Гра": {
        "i": "я сігма крутой я сігма сігма сігма сігма",
    "Рекорди": {
        "x": "hihihiha"
    }
    }


}

words = [
    "MANGO", "BEACH", "FUNNY", "CLOCK", "APPLE",
    "MUSIC", "HAPPY", "WATER", "TIGER", "SPORT",
    "SUNNY", "FLUTE", "DANCE", "CLOUD", "PIZZA",
    "PLANT", "GREEN", "BRAIN", "LIGHT", "CHAIR",
    "DREAM", "MAGIC", "RIVER", "HEART", "SMILE",
    "HONEY", "CROWN", "CANDY", "STARS", "LUCKY",
    "GHOST", "SNAKE", "MONEY", "FROST", "SPACE",
    "STORM", "WINDY", "OCEAN", "SWORD", "GREAT",
    "BLAZE", "CRAFT", "GRACE", "BRICK", "ROCKY",
    "POWER", "GALAX", "FLAME", "FLASH", "HORSE",
    "BEAST", "ROYAL", "FABLE", "QUEST", "FIGHT",
    "WORLD", "MIGHT", "LAUGH", "WATCH", "HAPPY",
    "RADIO", "CLOUD", "SHINE", "QUICK", "LOVEL",
    "SMART", "MAGIC", "STEEL", "FRESH", "FROZE",
    "SOLID", "STILL", "KINGS", "LIONS", "EAGLE",
    "TIGER", "HAWKS", "DREAM", "FIERY", "LEMON",
    "BERRY", "LILAC", "GEMSY", "VASTS", "BLUES",
    "PEACH", "GLOWY", "FROST", "SPICE", "BLISS"
]


baza={}

@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    if message.from_user.id not in baza:
        baza[message.from_user.id]=[]
    choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text ="Правила" , callback_data = "rules")
    choice.add(button)
    button1 = InlineKeyboardButton(text="Гра", callback_data="game")
    choice.add(button1)
    await message. answer( text = 'Привіт, Я - бот-вордл,\n Пропоную зіграти!:', reply_markup=choice)
    await States.begin.set()
@dp.callback_query_handler(state = States.begin)
async def get_film_info(call: types.CallbackQuery, state: FSMContext):
    choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Правила", callback_data="rules")
    choice.add(button)
    button1 = InlineKeyboardButton(text="Гра", callback_data="game")
    choice.add(button1)
    if call. data == "rules":
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id
                                    , text='Потрібно відгадати слово, яке складається з 5 букв, якщо буква відгадана, воно показує місце букви.',
                                    reply_markup=choice)
        await state.finish()
        await States.begin.set()
    elif call.data == "game":
        slovo = randint(0, len(words) - 1)
        if len(baza[call.from_user.id])==0:
            baza[call.from_user.id].append(list(words[slovo]))
            baza[call.from_user.id].append(['*', '*', '*', '*', '*'])
            baza[call.from_user.id].append(0)
            baza[call.from_user.id].append(100)
        else:
            baza[call.from_user.id][0] = (list(words[slovo]))
            baza[call.from_user.id][1] = (['*', '*', '*', '*', '*'])
            baza[call.from_user.id][2] = 0
        print(baza)
        await bot.send_message(call.message.chat.id,'Ось ваше слово ' + str(baza[call.from_user.id][1]))
        await bot.send_message(call.message.chat.id, 'Напишіть одну букву')
        await state.finish()
        await States.game.set()
    else:
        await bot.send_message(call.message.chat.id,'Error')

@dp.message_handler(state = States.game, content_types=types.ContentTypes.TEXT)
async def gra(message: types.Message, state: FSMContext):
    baza[message.from_user.id][2] += 1
    if message.text.upper() in baza[message.from_user.id][0]:
        for i in range(5):
            if  baza[message.from_user.id][0][i] == message.text.upper():
                baza[message.from_user.id][1][i] = message.text.upper()
        await message.answer("Буква відгадана. Прогрес: " + str(baza[message.from_user.id][1]))
        print(baza)
        await state.finish()
        await States.game.set()
        if '*' not in baza[message.from_user.id][1]:
            choice = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton(text="Гра", callback_data="game")
            choice.add(button1)
            await bot.send_message(message.chat.id, 'Ви виграли за ' + str(baza[message.from_user.id][2]) + ' спроб!')
            if baza[message.from_user.id][2] < baza[message.from_user.id][3]:
                baza[message.from_user.id][3] = baza[message.from_user.id][2]
                await message.answer("Новий рекорд: " + str(baza[message.from_user.id][3]),reply_markup=choice)
            baza[message.from_user.id][1] = ['*', '*', '*', '*', '*']
            baza[message.from_user.id][2] = 0
            await state.finish()
            await States.begin.set()

    else:
        await message.answer("Не вгадали "  + str(baza[message.from_user.id][1]))
        await state.finish()
        await States.game.set()


if __name__ == '__main__':
    executor.start_polling(dp)