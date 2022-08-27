import os
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import config
import conversation as conv
import task



def main():
    TOKEN = config.API_KEY
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('search', conv.search_start)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, conv.search_end)]
        },
        fallbacks=[CommandHandler('cancel', conv.cancel)]
    ))

    dispatcher.add_handler(CommandHandler('start', conv.start_bot))
    dispatcher.add_handler(CommandHandler('help', conv.help))
    dispatcher.add_handler(CommandHandler('donate', conv.donate))

    updater.job_queue.run_repeating(task.control_leaking, interval=3600, first=10)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=config.WEBHOOK_URL)
    updater.idle()


if __name__ == '__main__':
    main()
