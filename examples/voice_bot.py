from baleself import lib
@lib.bot.on(lib.Event(lib.EventType.NEW_MESSAGE))
@lib.message_handler
def handle_all_messages(message: lib.Message):
    if message.text:
        if message.text == "join":
            lib.join_voice() #join to running voice call
            lib.reply_message(message.data_sid,"joined") #joined reply message
        if message.text == "leave":
            lib.leave_voice() #leave from running voice call
            lib.reply_message(message.data_sid,"left") #left reply message
        if message.text == "send vc":
            lib.send_voice(2) #record a voice with 2s length (must be < 10s)
            lib.reply_message(message.data_sid,"sent") #sent reply message
lib.run()