from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import configparser
import asyncio
import nest_asyncio
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

# 应用 nest_asyncio
nest_asyncio.apply()

global redis1

from telegram.ext import filters  # 确保引用正确

from telegram.ext import filters  # 确保引用正确

async def main():
    # Load your token and create an Application for your Bot
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['TELEGRAM']['ACCESS_TOKEN']
    
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    
    # Create Application instance
    application = ApplicationBuilder().token(token).build()
    
    global redis1
    redis1 = redis.Redis(
        host=config['REDIS']['HOST'],
        port=config['REDIS']['PORT'],
        decode_responses=config['REDIS']['DECODE_RESPONSES'],
        username=config['REDIS']['USERNAME'],
        password=config['REDIS']['PASSWORD']
    )
    
    # Set logging configuration
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # Register handlers
    chatgpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), equiped_chatgpt)
    application.add_handler(chatgpt_handler)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("help", help_command))
    
    # Start the bot
    await application.run_polling()

async def echo(update: Update, context: CallbackContext) -> None:
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Helping you helping you.')

async def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword
        redis1.incr(msg)  # 递增关键词计数
        value = redis1.get(msg)  # 获取当前计数
        
        if value is None:
            value = '0'  # 如果没有返回值，则设置为默认值
        else:
            value = str(value)  # 确保将字节转换为字符串
        
        await update.message.reply_text(f'You have said {msg} for {value} times.')
        
    except (IndexError, ValueError):
        await update.message.reply_text('Usage: /add <keyword>')

async def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__ == '__main__':
    asyncio.run(main())