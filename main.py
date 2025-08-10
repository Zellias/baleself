from baleself import lib
@lib.bot.on(lib.Event(lib.EventType.NEW_MESSAGE))
@lib.message_handler
def handle_all_messages(message: lib.Message):
    if message.text:
        if message.text == "سلام":
            lib.reply_message(message.data_sid,"سلام")
lib.run()