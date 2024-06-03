import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from ocr import  image2text
from aiogram.utils.markdown import code
import cv2
import os

API_TOKEN = '7064039713:AAFLE8cWuxc3rn94clJv7X7hPWlvI12IwPw'

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hello. With this bot, you can copy text from the image. Only send image.\nПривет. С помощью этого бота вы можете копировать текст с изображения. Отправить изображение.")

class OCRState(StatesGroup):
    waiting_for_image = State()


@dp.message_handler(content_types=['photo'], state=None)
async def handle_photo(message: types.Message, state: FSMContext):
    await message.reply("Processing image...")
    await state.set_state(OCRState.waiting_for_image)

    file_info = await bot.get_file(message.photo[-1].file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    with open("temp.jpg", "wb") as f:
        f.write(downloaded_file.read())
    text = image2text("temp.jpg")

    await message.reply(text)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)