import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SOURCE_CHANNEL_ID = int(os.environ.get("SOURCE_CHANNEL_ID"))
DEST_CHANNEL_IDS = [int(x) for x in os.environ.get("DEST_CHANNEL_IDS").split(",")]

def forward_message(update: Update, context: CallbackContext):
    if update.channel_post and update.channel_post.chat.id == SOURCE_CHANNEL_ID:
        for dest_id in DEST_CHANNEL_IDS:
            try:
                context.bot.forward_message(
                    chat_id=dest_id,
                    from_chat_id=SOURCE_CHANNEL_ID,
                    message_id=update.channel_post.message_id
                )
            except Exception as e:
                print(f"Error forwarding to {dest_id}: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.channel_posts, forward_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
