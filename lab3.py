from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
import logging
import configparser
import asyncio
import nest_asyncio

# 应用 nest_asyncio
nest_asyncio.apply()

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

async def echo(update: Update, context: CallbackContext) -> None:
    # 回应用户发送的消息
    reply_message = update.message.text.upper()  # 将用户消息转为大写
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

async def main():
    # 读取配置文件，获取访问令牌
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['TELEGRAM']['ACCESS_TOKEN']

    # 创建 Application 实例
    application = ApplicationBuilder().token(token).build()

    # 注册处理消息的函数
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 启动机器人
    await application.run_polling()

# 主程序入口
if __name__ == '__main__':
    asyncio.run(main())