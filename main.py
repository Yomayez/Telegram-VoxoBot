from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
import asyncio
import os
from dotenv import load_dotenv
from data_scrapper import voxo_status, voxo_stats

load_dotenv()

START_PHOTO = FSInputFile('photo/start_bg.jpg')
INFO_PHOTO = FSInputFile('photo/info_bg.png')
STATUS_PHOTO = FSInputFile('photo/status_bg.png')

TOKEN_KEY = os.getenv('TOKEN')

bot = Bot(token=TOKEN_KEY)
dp = Dispatcher()
rt = Router()

dp.include_router(rt)

@rt.message(CommandStart())
async def menu_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text = 'Инфо',
        callback_data = 'info')
    )
    builder.row(types.InlineKeyboardButton(
        text = 'Статус',
        callback_data = 'status')
    )

    await message.answer_photo(
        photo=START_PHOTO,
        caption='Привет!\nЭто бот проекта <a href="https://vo-xo.com/"><b>Voxoria</b></a>',
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup()
    )

@rt.callback_query(F.data == 'info')
async def info(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='Меню',
        callback_data='menu')
    )
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=INFO_PHOTO,
        caption="""<a href="https://vo-xo.com/"><b>Сайт</b></a>
<a href="https://vo-xo.com/wiki/start/rules"><b>Правила</b></a>
<a href="https://discord.gg/FYEbHRfdn"><b>Дискорд</b></a>
<a href="https://t.me/voxoria"><b>Тгк</b></a>
<b>IP:</b> <code>mc.vo-xo.com</code>""",
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup()
    )

@rt.callback_query(F.data == 'menu')
async def menu_call(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text = 'Инфо',
        callback_data = 'info')
    )

    builder.row(types.InlineKeyboardButton(
        text = 'Статус',
        callback_data = 'status')
    )

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=START_PHOTO,
        caption='Привет!\nЭто бот проекта <a href="https://vo-xo.com/"><b>Voxoria</b></a>',
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup()
    )


@rt.callback_query(F.data == 'status')
async def status(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text = 'Меню',
        callback_data = 'menu')
    )

    data_status = await voxo_status()
    data_stats = await voxo_stats()

    upt_h = data_status['uptime']//3600
    upt_m = data_status['uptime']%3600//60
    upt_s = data_status['uptime']%60

    playtime_s = data_stats['playtime']//1000

    plt_h = playtime_s//3600
    plt_m = playtime_s%3600//60
    plt_s = playtime_s%60


    if data_status['status']:
        status_text = f"""<b>Статус сервера:</b>
<blockquote><b>Сервер онлайн</b>
<b>Количество игроков онлайн: {data_status['online']}</b>
<b>Пик онлайна за сегодня: {data_status['peak_online']}</b>
<b>Аптайм: Часов: {upt_h}, Минут: {upt_m}, Секунд: {upt_s}</b></blockquote>\n\n"""

    else:
        status_text = """<b>Статус сервера:</b>
<blockquote>Сервер оффлайн</blockquote>\n\n"""

    stats_text = f"""<b>Статистика сервера</b>:
<blockquote><b>Зарегистрированных игроков: {data_stats['users']}</b>
<b>Кланов: {data_stats['clans']}</b>
<b>Плейтайм: Часов: {plt_h}, Минут: {plt_m}, Секунд: {plt_s}</b></blockquote>"""

    res_text = status_text + stats_text

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=STATUS_PHOTO,
        caption=res_text,
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup()
    )


async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Бот запущен')
    asyncio.run(main())