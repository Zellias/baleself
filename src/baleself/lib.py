
from selenium.webdriver.common.by import By

import time
import os
import sys

import json
import functools
from typing import Callable, Dict, Any, List, Pattern
from enum import Enum
import re
from .browser_manager import get_chrome_driver,wait_and_click,wait_and_write,wait_and_find,get_html_text,emulate_type,get_element_text,get_image_as_base64,extract_user_info,extract_group_info,extract_channel_info,right_click_element,wait_and_get
from .models import Message, Event, EventType,User,Group,Channel
from selenium.webdriver import ActionChains

# Use cache file in module folder
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_data_sid.txt")
cached_sids = set()

class EventType(Enum):
    NEW_MESSAGE = "new_message"

class Bot:
    def __init__(self):
        self._handlers: List[tuple[Event, Callable]] = []
    
    def on(self, event: Event):
        def decorator(func: Callable):
            self._handlers.append((event, func))
            return func
        return decorator

    def _handle_message(self, message_data):
        try:
            # Convert dict to Message if needed
            if isinstance(message_data, dict):
                message = Message.from_dict(message_data)
            elif isinstance(message_data, Message):
                message = message_data
            else:
                print(f"Invalid message format in bot handler: {message_data}")
                return

            for event, handler in self._handlers:
                if event.type == EventType.NEW_MESSAGE:
                    if event.pattern is None or event.pattern.match(message.text):
                        handler(message)
        except Exception as e:
            print(f"Error in message handler: {e}")

bot = Bot()

driver = get_chrome_driver()

def get_user(user_id):
    """
    Gets user information for the specified user ID.
    
    Args:
        user_id: The ID of the user to get info for
        
    Returns:
        User: A User object containing the user's information
    """
    open_chat(user_id)
    wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[2]/div[1]")
    user_data = extract_user_info(driver)
    wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[1]/div[1]/div/div")
    return User.from_dict(user_data)

def get_group(group_id):
    """
    Gets group information for the specified group ID.
    
    Args:
        group_id: The ID of the group to get info for
        
    Returns:
        Group: A group object containing the group's information
    """
    open_chat(group_id)
    wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[2]/div[1]")
    group_data = extract_group_info(driver)
    wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[1]/div[1]/div/div")
    return Group.from_dict(group_data)

def get_channel(channel_id):

    """
    Gets channel information for the specified channel ID.
    
    Args:
        channel_id: The ID of the channel to get info for
        
    Returns:
        Channel: A channel object containing the channel's information
    """
    open_chat(channel_id)
    wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[2]/div[1]")
    channel_data = extract_channel_info(driver)
    wait_and_click(driver, By.XPATH, "/html/body/div[5]/div/div/div[1]/div[1]/div/div")
    return Channel.from_dict(channel_data)

def get_current_url(driver):
    return driver.current_url

def login():
    driver.get("https://web.bale.ai/login?redirectTo=/chat?uid=11")
    wait_and_click(driver, By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/button')
    wait_and_click(driver,By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div[3]/div[2]/div/button")
    phone = input("Phone number: ")
    wait_and_write(driver,By.XPATH,"/html/body/div[1]/div[1]/div/div/div[1]/div/div[4]/div/fieldset/div/input",phone)
    wait_and_click(driver,By.XPATH,"/html/body/div[1]/div[1]/div/div/div[2]/div/button")
    code = input("Code: ")
    time.sleep(2)
    wait_and_write(driver,By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[2]/fieldset/div/input",code)
    time.sleep(2)
    wait_and_click(driver,By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div[2]/div/button")
    open_chat(11)

def open_chat(user_id):
    driver.get(f"https://web.bale.ai/chat?uid={user_id}")

def open_uchat(username):
    driver.execute_script("window.location.href = arguments[0];", f"https://web.bale.ai/@{username.split('@')[1]}")

def send_message(message_text):
    while True:
        try:
            emulate_type(driver, By.ID, "editable-message-text", message_text)
            break
        except:
            pass

def make_room(room_name):
        start_index = "ble.ir"
        wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div[1]/div[3]")
        wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div/ul/div[5]")
        wait_and_write(driver, By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/fieldset/div/input",room_name)
        wait_and_click(driver, By.XPATH, "/html/body/div[4]/div/div/div[3]/button[1]")
        wait_and_click(driver, By.XPATH, "/html/body/div[5]/div/div/div[2]/div[2]/div/div/div[1]")
        wait_and_click(driver, By.XPATH, '//*[@aria-label="ساخت گروه"]')
        time.sleep(0.5)
        invite_link = wait_and_get(driver,'//*[@placeholder="متن ارسالی را بنویسید"]')
        open_chat(11)
        return str(invite_link).replace("\n"," ")

def join_room(username):
        try:
            driver.execute_script("window.location.href = arguments[0];", f"https://web.bale.ai/@{username.split('@')[1]}")
            wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[3]/button")
        except:
            print(f"Cannot Join {username}. But I Saw Messages!")
            time.sleep(0.5)
            open_chat(486910547)

def send_voice(length):
        if length<=10:
            wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div/div[7]")
            time.sleep(length)
            wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div/div[1]/div[3]/button[3]")
        else:
            send_message("<=10s")

def join_voice():
        wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[1]/div[2]/div/div/button")
        # time.sleep()
        wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div/div[3]/button")
        wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[1]/div/div[1]/div[1]")

def leave_voice():
    # wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[3]/div/div[2]/div[1]/div")
    open_chat(6168101635)

def welcome():
    wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[2]/div[1]/div/div[2]")

def reply_message(data_sid,message):
    """
    Replies to a message with the given data_sid.

    Args:
        message: The message text to reply with.
        data_sid: The data-sid attribute of the message to reply to.
    """
    actions = ActionChains(driver)
    message_elem = wait_and_find(driver, By.CSS_SELECTOR, f"div[data-sid='{data_sid}']")
    actions.move_to_element(message_elem).perform()
    wait_and_click(driver, By.CSS_SELECTOR, f"div[data-sid='{data_sid}'] .action-menu .ActionMenu_reply_icon__-kKkn")
    emulate_type(driver, By.ID, "editable-message-text", message)

def send_gift(amount):
    wait_and_click(driver,By.XPATH,'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div/div[1]')
    wait_and_click(driver,By.XPATH,'/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div/ul/li[4]')
    time.sleep(0.2)
    wait_and_write(driver,By.XPATH,'/html/body/div[6]/div/div/div[2]/div[1]/div[1]/div/fieldset/div/input',str(amount))
    wait_and_write(driver,By.XPATH,'/html/body/div[6]/div/div/div[2]/div[1]/div[3]/div/div/textarea','By @RollBack')
    wait_and_click(driver,By.XPATH,'/html/body/div[6]/div/div/div[3]/button')
    time.sleep(0.2)
    wait_and_click(driver,By.XPATH,'/html/body/div[6]/div/div/div[5]/button')
    wait_and_click(driver,By.XPATH,'/html/body/div[7]/div/div/button')

def load_cached_sids():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                sid = line.strip()
                if sid:
                    cached_sids.add(sid)
def add_user(username,channel_id):
        try:
            open_uchat(username)
            send_message(".")
            open_chat(channel_id)
            wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div[2]")
            wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div/div/table/div[4]")
            wait_and_write(driver, By.XPATH, "/html/body/div[7]/div/div/div[2]/div[2]/div/input",username)
            wait_and_click(driver, By.XPATH, "/html/body/div[7]/div/div/div[2]/div[3]/div/div")
            wait_and_click(driver, By.XPATH, "/html/body/div[7]/div/div/div[3]/button[1]")
            open_chat(11)
        except:
            send_message("مسخره کردی؟")

def delete_room(channel_id):
        open_chat(channel_id)
        wait_and_click(driver, By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div[2]")
        wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/div[2]/div")
        wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/div[2]/div[2]/div[2]")
        wait_and_click(driver, By.XPATH, "/html/body/div[7]/div/div/div[2]/div/button[1]")

        open_chat(11)

def add_sid_to_cache(sid):
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{sid}\n")

def current_channel_id():
    return driver.current_url.split("/")[-1].split("=")[1]

def message_handler(func: Callable[[Message], None]):
    """
    Decorator for handling messages in the chat.
    Provides error handling and message validation.
    """
    @functools.wraps(func)
    def wrapper(message_data):
        try:
            # Handle both dict and Message objects
            if isinstance(message_data, dict):
                if 'text' not in message_data:
                    print(f"Message missing text field: {message_data}")
                    return
                message = Message.from_dict(message_data)
            elif isinstance(message_data, Message):
                message = message_data
            else:
                print(f"Invalid message format: {message_data}")
                return
                
            return func(message)
        except Exception as e:
            print(f"Error processing message: {e}")
            return None
    return wrapper

def read_last_messages(handle_message):
    try:
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]").click()
            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[2]/div[3]/div").click()
            except:
                pass
        except:
            pass
        try:
            message_list = driver.find_element(By.CSS_SELECTOR, ".message_list_scroller_id")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", message_list)
        except:
            pass
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[3]/div/div[2]").click()
        except:
            pass

        
        message_items = driver.find_elements(By.CSS_SELECTOR, ".message-item")
        if not message_items:
            return

        last_messages = message_items[-5:]

        for message in last_messages:
            data_sid = message.get_attribute("data-sid")
            if data_sid in cached_sids:
                continue

            cached_sids.add(data_sid)
            add_sid_to_cache(data_sid)

            is_gift = False
            try:
                message.find_element(By.CSS_SELECTOR, ".GiftMessage_BubbleWrapper__70RDR")
                is_gift = True
            except:
                pass

            if is_gift:
                try:
                    btns = message.find_elements(By.CSS_SELECTOR, ".message-button,button")
                    for btn in btns:
                        try:
                            btn.click()
                            time.sleep(0.8)
                            open_chat("6168101635")
                        except:
                            continue
                    for _ in range(2):
                        try:
                            driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[1]/div").click()
                            break
                        except:
                            continue
                except:
                    pass

            text_spans = message.find_elements(By.CSS_SELECTOR, ".Text_text__0QjN9 span")
            text_lines = [span.text for span in text_spans]
            direction = text_spans[0].get_attribute("dir") if text_spans else "ltr"

            try:
                timestamp = message.find_element(By.CSS_SELECTOR, ".Info_date__icEjb").text
            except:
                timestamp = ""
            channel_id = driver.current_url.split("/")[-1].split("=")[1]
            message_data = {
                "data_sid": data_sid,
                "text": "\n".join(text_lines),
                "direction": direction,
                "timestamp": timestamp,
                "is_gift": is_gift,
                "channel_id": channel_id
            }

            if is_gift:
                try:
                    message.find_element(By.TAG_NAME, "button").click()
                    wait_and_click(driver, By.XPATH, "/html/body/div[6]/div/div/div[1]/div")
                    break
                except:
                    pass

            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[3]/div[3]/div[3]/div/div[2]").click()
                try:
                    driver.execute_script("arguments[0].scrollTop += 100;", message_container)
                    message_container = driver.find_element(By.CSS_SELECTOR, ".Messages_container__1pU1T")
                except:
                    driver.execute_script("window.scrollBy(0, 100);")
            except:
                pass
            
            
            
            if handle_message:
                handle_message(message_data)

    except Exception as e:
        print(f"Error in read_last_messages: {e}")

def run():
    """
    Continuously watch for new messages and handle them.
    This function runs in an infinite loop until interrupted.
    """
    load_cached_sids()
    open_chat(11)
    print("Starting to watch messages...")
    while True:
        try:
            read_last_messages(lambda msg: bot._handle_message(msg))
        except KeyboardInterrupt:
            print("\nStopping message watch...")
            break
        except Exception as e:
            print(f"Error in message watch loop: {e}")

# open_chat(2087331576)
# watch_chat(2087331576)
# send_gift(10000)
