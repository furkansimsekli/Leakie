import telegram
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import piratebay
import mongo




def search_start(update: Update, context: CallbackContext):
    update.message.reply_text("What are you looking for? Write down below and send me!\n\n"
                              "<b>Example:</b> <i>House of The Dragon S01E02</i>\n"
                              "<b>Example:</b> <i>house of the dragon season 1 episode 2</i>\n"
                              "<b>Example:</b> <i>game of thrones s03e09</i>\n\n"
                              "You can /cancel the process if you want.",
                              parse_mode=telegram.ParseMode.HTML)
    return 1


def search_end(update: Update, context: CallbackContext):
    text = update.message.text
    results = piratebay.search(text)

    if results:
        samples = piratebay.generate_sample_text(results)
        update.message.reply_text(f"It might be leaked, here are the some results I've found:\n\n"
                                  f"{samples}",
                                  parse_mode=telegram.ParseMode.HTML)
    else:
        update.message.reply_text(f"There is no sign from it!")
        mongo.update(text.lower(), update.effective_user.id)
        update.message.reply_text(f"You will be notified when there is a possible leak!")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Process has been cancelled!")
    return ConversationHandler.END


def start_bot(update: Update, context: CallbackContext):
    update.message.reply_text(f"Hello {update.effective_user.first_name}! "
                              f"I'm Leakie, I will help you to set alarms for any leaking documents!\n\n"
                              f"For more information, please see /help :)")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(f"Leakie currently searches on only PirateBay. Don't worry, it's a great "
                              f"place to find movies, tv shows and stuff like that! However, "
                              f"I'm not encouraging you to use piracy for copyrighted products. So, "
                              f"I won't be sending torrent URLs for you to download them. I'm just a "
                              f"smart alarm!\n\n"
                              f"You can use Menu down below to choose commands easily. Also you can write them.\n"
                              f"/search -> Search whatever you are looking for\n"
                              f"/donate -> Buy a coffee for the developer")


def donate(update: Update, context: CallbackContext):
    update.message.reply_text("If you're happy with the experience on Leakie, you can support the developer.\n\n"
                              '<a href="https://www.buymeacoffee.com/finch">Buy me a coffee</a>',
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)
