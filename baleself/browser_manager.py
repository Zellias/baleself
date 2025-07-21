from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import json
import functools
from typing import Callable, Dict, Any, List, Pattern
from dataclasses import dataclass
from enum import Enum
import re
import base64
from selenium.webdriver.common.action_chains import ActionChains

def get_chrome_driver(user_data_dir=None):
    # Place chrome user data in module folder named bale_session by default
    if user_data_dir is None:
        module_dir = os.path.dirname(os.path.abspath(__file__))
        user_data_dir = os.path.join(module_dir, "bale_session")
    abs_user_data_dir = os.path.abspath(user_data_dir)
    os.makedirs(abs_user_data_dir, exist_ok=True)
    options = Options()
    options.add_argument(f"--user-data-dir={abs_user_data_dir}")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    # options.add_argument("--headless=new")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--disk-cache-dir=" + os.path.join(abs_user_data_dir, "cache"))
    options.add_argument("--disable-notifications")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-features=TranslateUI,site-per-process,AutofillServerCommunication,IsolateOrigins,PaintHolding,BackForwardCache,Prerender2")
    # ENABLE images loading (remove --blink-settings=imagesEnabled=false)
    options.add_argument("--blink-settings=imagesEnabled=false")  # Don't load images for max speed
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-prompt-on-repost")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-domain-reliability")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--safebrowsing-disable-auto-update")
    options.add_argument("--password-store=basic")
    options.add_argument("--use-mock-keychain")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "profile.default_content_setting_values.popups": 2,
        "profile.default_content_setting_values.cookies": 1,
        "profile.default_content_setting_values.plugins": 1,
        "profile.default_content_setting_values.images": 1,  # 1=allow, 2=block, but not blocking images as per instruction
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.background_sync": 2,
        "profile.default_content_setting_values.autoplay": 2,
        "profile.default_content_setting_values.mixed_script": 2,
        "profile.default_content_setting_values.ads": 2,
        "profile.default_content_setting_values.javascript": 1,
        "profile.default_content_setting_values.sound": 2,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(5)
    return driver

def wait_and_click(driver, by, value, timeout=5):
    # Lower timeout for speed
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element

def wait_and_get(driver,value:str):
    # Lower timeout for speed
    element = driver.find_element(By.XPATH, value)
    return element.text


def wait_and_write(driver, by, value, text, timeout=10):
    # Lower timeout for speed
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )
    element.clear()
    element.send_keys(text)
    return element

def wait_and_find(driver, by, value, timeout=3):
    """
    Waits for an element to be present in the DOM and returns it.
    Lower timeout for speed.
    """
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    return element

def get_html_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def get_element_text(driver, by, value, timeout=3):
    """
    Gets the text content of an element after waiting for it to be present.
    """
    element = wait_and_find(driver, by, value, timeout)
    return element.text

def get_image_as_base64(driver, by, value, timeout=3):
    """
    Gets an image element and converts it to base64 string.
    Fastest way to get base64 encoded image.
    """
    element = wait_and_find(driver, by, value, timeout)
    src = element.get_attribute('src')
    
    # If already base64, return as-is
    if src.startswith('data:image'):
        return src
        
    # Get src directly as base64 if possible
    if src.startswith('http'):
        return src
        
    # Fallback to screenshot only if needed
    img_binary = element.screenshot_as_png
    return f"data:image/png;base64,{base64.b64encode(img_binary).decode('utf-8')}"

def right_click_element(driver, by, value, timeout=3):
    """
    Right clicks on an element after waiting for it to be present.
    """
    element = wait_and_find(driver, by, value, timeout)
    ActionChains(driver).context_click(element).perform()
    return element


def extract_channel_info(driver):
    """
    Extracts channel information from the provided By selectors.
    Returns a dictionary containing channel details.
    """
    channel_info = {}
    
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "p.UserGroupInfo_Name__JTED2")
        channel_info['name'] = name_element.text.strip()
    except:
        pass

    try:
        subscribers_element = driver.find_element(By.CSS_SELECTOR, "p.UserGroupInfo_Status__9xprt")
        subscribers_text = subscribers_element.text.strip().split(" ")[0].replace(",", "")
        channel_info['subscribers'] = int(subscribers_text)
    except:
        pass

    try:
        description_element = driver.find_element(By.CSS_SELECTOR, "li[data-testid='about-group'] div.Text_text__0QjN9")
        channel_info['description'] = description_element.text.strip()
    except:
        pass

    try:
        channel_id_element = driver.find_element(By.CSS_SELECTOR, "li.Detail_ListItem__CJHS5.css-1itu66x.e16eonh70 div.Text_text__0QjN9 span")
        channel_info['channel_id'] = channel_id_element.text.strip()
    except:
        pass

    try:
        avatar_img = driver.find_element(By.CSS_SELECTOR, "img.BaseAvatar_AvatarImage__zq0Ou")
        channel_info['avatar'] = get_image_as_base64(driver, By.CSS_SELECTOR, "img.BaseAvatar_AvatarImage__zq0Ou")
    except:
        pass

    return channel_info

def extract_group_info(driver):
    """
    Extracts group information from the provided By selectors.
    Returns a dictionary containing group details.
    """
    group_info = {}
    
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "p.UserGroupInfo_Name__JTED2")
        group_info['name'] = name_element.text.strip()
    except:
        pass

    try:
        status_element = driver.find_element(By.CSS_SELECTOR, "p.UserGroupInfo_Status__9xprt")
        status_text = status_element.text.strip().split(" ")[0]
        group_info['total_members'] = int(status_text)
    except:
        pass

    try:
        description_element = driver.find_element(By.CSS_SELECTOR, "li[data-testid='about-group'] div.Text_text__0QjN9")
        group_info['description'] = description_element.text.strip()
    except:
        pass

    try:
        group_id_element = driver.find_element(By.CSS_SELECTOR, "li.Detail_ListItem__CJHS5.css-1itu66x.e16eonh70 div.Text_text__0QjN9 span")
        group_info['group_id'] = group_id_element.text.strip()
    except:
        pass

    try:
        avatar_img = driver.find_element(By.CSS_SELECTOR, "img.BaseAvatar_AvatarImage__zq0Ou") 
        group_info['avatar'] = get_image_as_base64(driver, By.CSS_SELECTOR, "img.BaseAvatar_AvatarImage__zq0Ou")
    except:
        pass

    return group_info


def extract_user_info(driver):
    """
    Extracts user information from the provided By selectors.
    Returns a dictionary containing user details.
    """
    user_info = {}
    
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "p.UserGroupInfo_Name__JTED2")
        user_info['name'] = name_element.text.strip()
    except:
        pass
    
    try:
        status_element = driver.find_element(By.CSS_SELECTOR, "p.UserGroupInfo_Status__9xprt")
        user_info['status'] = status_element.text.strip()
    except:
        pass
    
    try:
        username_element = driver.find_element(By.CSS_SELECTOR, "li[data-testid='username'] span")
        user_info['username'] = username_element.text.strip()
    except:
        pass
    
    try:
        about_element = driver.find_element(By.CSS_SELECTOR, "li[data-testid='about'] div.Text_text__0QjN9")
        user_info['bio'] = about_element.text.strip()
    except:
        pass
    
    try:
        avatar_img = driver.find_element(By.CSS_SELECTOR, "img.BaseAvatar_AvatarImage__zq0Ou")
        user_info['avatar'] = get_image_as_base64(driver, By.CSS_SELECTOR, "img.BaseAvatar_AvatarImage__zq0Ou")
    except:
        pass
        
    return user_info


def emulate_type(driver,by,value,text):
    element = wait_and_find(driver,by,value)
    element.click()
    element.send_keys(text)
    element.send_keys(Keys.ENTER)