import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")  # read from env variable

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("clear"))
async def clear_messages(message: types.Message):
    chat_id = message.chat.id
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("This command only works in groups/supergroups.")
        return

    await message.reply("Deleting messages...")

    async for msg in bot.get_chat_history(chat_id, limit=100):
        try:
            await bot.delete_message(chat_id, msg.message_id)
        except Exception as e:
            print(f"Could not delete {msg.message_id}: {e}")

    await message.answer("✅ Cleanup complete!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
