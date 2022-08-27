import telegram
from telegram.ext import CallbackContext
from logger import logger
import mongo
import piratebay



def control_leaking(context: CallbackContext):
    queries = mongo.find_search_terms()

    for query in queries:
        results = piratebay.search(query)

        if results:
            logger.info(f"Found new results for ~{query}~")
            users = mongo.find_users(query)
            notify_users(context, query, users)
            mongo.delete(query)
        else:
            logger.info(f"Still no result for ~{query}~")


def notify_users(context: CallbackContext, query, users):
    for user in users:
        try:
            context.bot.send_message(chat_id=user,
                                     text=f'I found out <code>{query}</code> might be leaked. '
                                          f'Be careful against spoilers!',
                                     parse_mode=telegram.ParseMode.HTML)
            logger.info(f"Message has been sent to {user}")

        except telegram.error.Unauthorized:
            logger.info(f"Couldn't deliver the message to {user}")


def clear_db():
    # TODO Implement it to clear expired queries from database!
    pass
