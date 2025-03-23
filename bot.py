import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
from pprint import pprint

TOKEN = ''

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        'Привет! Отправьте ID игрока в формате: <code>1170923497</code> и я предоставлю информацию о нем',
        parse_mode='HTML')


@dp.message()
async def filter_messages(message: Message):
    try:
        if message.text.isdigit():

            account_id = message.text
            headers = {'accept': 'application/json', }
            params = {'limit': 20, }
            match_params = {'limit': 1, }

            base_info = requests.get(f'https://api.opendota.com/api/players/{account_id}/', headers=headers)
            wl_info = requests.get(f'https://api.opendota.com/api/players/{account_id}/wl', headers=headers,
                                   params=params)
            total_wl = requests.get(f'https://api.opendota.com/api/players/{account_id}/wl', headers=headers)
            mathes = requests.get(f'https://api.opendota.com/api/players/{account_id}/matches', headers=headers,
                                  params=match_params)

            data_base_info = base_info.json()
            data_wl_info = wl_info.json()
            data_total_wl = total_wl.json()
            data_matches = mathes.json()

            pprint(data_base_info)
            st_id = data_base_info['profile']['account_id']
            name = data_base_info['profile']['personaname']
            avatar = data_base_info['profile']['avatarfull']
            profile_url = data_base_info['profile']['profileurl']
            loccountrycode = data_base_info['profile']['loccountrycode']
            plus = data_base_info['profile']['plus']
            rank = data_base_info['rank_tier']
            if plus:
                dota_plus = '🟢'
            else:
                dota_plus = '🔴'

            pprint(data_wl_info)
            win = data_wl_info['win']
            lose = data_wl_info['lose']
            try:
                winrate = win / (win + lose) * 100
            except:
                winrate = 0

            pprint(data_total_wl)
            total_wins = data_total_wl['win']
            total_loses = data_total_wl['lose']
            total_games = total_wins + total_loses
            try:
                total_winrate = total_wins / (total_wins + total_loses) * 100
                if total_winrate > 50:
                    emoji = '🟢'
                else:
                    emoji = '🔴'
            except:
                total_winrate = 0
                emoji = '🟠'

            pprint(data_matches)
            try:
                kills = data_matches[0]['kills']
                deaths = data_matches[0]['deaths']
                assists = data_matches[0]['assists']
            except:
                kills = 0
                deaths = 0
                assists = 0

            text = (
                f"<b>{name} | {emoji} {int(total_winrate)}% WR</b>\n\n"
                f"Rank Tier:  <code>{rank}</code>\n"
                f"Total matches:  <code>{total_games} (🔺{total_wins} 🔻{total_loses})</code>\n"
                f"Last 20 games winrate:  <code>{int(winrate)}%</code>\n"
                f"Last match KDA:  <code>{kills}/{deaths}/{assists}</code>\n"
                f"Dota Plus:  {dota_plus}\n\n"
                f"Account id:  <code>{st_id}</code>\n"
                f"Country:  <code>{loccountrycode}</code>\n"
            )

            builder = InlineKeyboardBuilder()
            button1 = types.InlineKeyboardButton(text="Steam profile", url=profile_url)
            builder.row(button1)

            await bot.send_photo(chat_id=message.chat.id, photo=avatar, caption=text, parse_mode="HTML",
                                 reply_markup=builder.as_markup())
    except:
        await message.answer('ID не найден. Отправьте ID в формате: <code>1170923497</code>', parse_mode='HTML')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
