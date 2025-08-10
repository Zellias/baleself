from baleself import lib
@lib.bot.on(lib.Event(lib.EventType.NEW_MESSAGE))
@lib.message_handler
def handle_all_messages(message: lib.Message):
    if message.text:
        if message.text == "make room":
            link = lib.make_room("room1") #create a private group with name room1 & save invite link in link var
            lib.reply_message(message.data_sid,f"{link}") #send group link with reply
        if message.text == "join room":
            lib.join_room("baleself") #join in @baleself group/channel in bale
            lib.reply_message(message.data_sid,"left") #left reply message
        if message.text == "add user":
            lib.add_user("user1",message.channel_id) #add user1 to sent message channel
            lib.reply_message(message.data_sid,"added user1") #added reply message
        if message.text == "delete room":
            lib.delete_room(message.channel_id) #delete sent message channel
lib.run()