# -*- coding: utf-8 -*-

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


orders = []
order_number = 1 


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global order_number
    message_text = update.message.text

   
    if "заказ" in message_text.lower():
       
        order = f"{message_text} - №{order_number:04}"
        orders.append(order)
        

        logger.info(f"Новый заказ зарегистрирован: {order}")
        
       
        await update.message.reply_text(f"Заказ зарегистрирован! Номер заказа: №{order_number:04}")
        
      
        order_number += 1


async def orders_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Запрос списка всех заказов")
    if not orders:
        await update.message.reply_text("Нет зарегистрированных заказов.")
    else:
       
        orders_text = "\n".join(orders)
        await update.message.reply_text(f"Список заказов:\n{orders_text}")


async def order_by_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Запрос заказа по номеру")
    try:
       
        number = int(context.args[0])
        
       
        for order in orders:
            if f"№{number:04}" in order:
                await update.message.reply_text(order)
                logger.info(f"Заказ найден и отправлен: {order}")
                return
        
       
        await update.message.reply_text("Заказ с таким номером не найден.")
        logger.warning(f"Заказ с номером {number} не найден")
    except (IndexError, ValueError):
        await update.message.reply_text("Укажите номер заказа после команды.")
        logger.error("Некорректный запрос: не указан номер заказа или он неверный")

def main():
    
    application = Application.builder().token("7837681058:AAHt1lec81873SVtNl5m1FKHacyJmeb5hXA").build()
    
  
    logger.info("Бот успешно запущен и готов к работе.")
    
 
    application.add_handler(CommandHandler("orders", orders_list)) 
    application.add_handler(CommandHandler("order", order_by_number)) 
    
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    
    application.run_polling()

if __name__ == "__main__":
    main()

