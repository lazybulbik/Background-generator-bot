from os import remove, listdir

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TELEGRAM_TOKEN
from replacebg import main

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)

count_of_backgrounds = 10


@dp.message_handler(commands=['settings'])
async def setting(message: types.Message):
    global count_of_backgrounds

    value = message.text.split()[1]
    await message.answer(f'Количетсво фонов изменено на {value}')
    count_of_backgrounds = int(value)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Отправьте фотографию для замены фона')


@dp.message_handler(content_types=['photo'])
async def image(message: types.Message):
    print(message)
    await message.photo[-1].download(destination_file='media/image.jpg')

    group1 = main('media/image.jpg', message.caption, count_of_backgrounds)

    for photo in group1:
        await bot.send_photo(message.from_user.id, photo=types.InputFile(photo))


    result_images = list(map(lambda x: 'media/result/' + x, listdir('media/result/')))
    for i in result_images:
        remove(i)

executor.start_polling(dp)
