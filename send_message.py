"""Script for sending a message in Whatsapp Web"""
import time
import os
import argparse
from argparse import Namespace
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


def parse_args() -> Namespace:
    """
    Parse arguments
    """

    parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
    parser.add_argument('--chrome_driver_path',
                        action='store',
                        type=str,
                        default='./chromedriver',
                        help='chromedriver executable path')
    parser.add_argument('--message',
                        action='store',
                        type=str,
                        required=True,
                        help='Enter the msg you want to send')
    parser.add_argument('--session_path',
                        action='store',
                        type=str,
                        default='./chrome_profile',
                        help='Enter the msg path to store profile settings')
    parser.add_argument('--contact',
                        action='store',
                        type=str,
                        required=True,
                        help='Enter the person to send the msg')
    parser.add_argument('--remove_cache',
                        action='store',
                        type=str,
                        default='False',
                        help='Remove Cache | Scan QR again or Not')
    args = parser.parse_args()

    return args


def send_message(message: str, element) -> None:
    """
    Get an element and send a message over it
    """

    element.send_keys(message)
    element.send_keys(Keys.ENTER)
    time.sleep(5)


def get_search_element(driver) -> WebElement:
    """
    Search for the search box
    """

    return driver.find_element(By.CLASS_NAME, "_13NKt")


def get_text_box(driver) -> WebElement:
    """
    Search for the text box
    """

    return driver.find_element(By.CLASS_NAME,
                               "fd365im1.to2l77zo.bbv8nyr4.mwp4sxku.gfz4du6o.ag5g9lrv")


def get_search_box_when_page_loaded(driver) -> WebElement:
    """
    Wait until the page is loaded and look for the search element when done
    """

    while True:
        try:
            get_search_element(driver)
            print("Page loaded.")
            return get_search_element(driver)
        except NoSuchElementException:
            print("Page not loaded yet.")
            time.sleep(1)


def play_sound() -> None:
    """
    Play beep sound
    """
    os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")


def main():
    """
    Main function
    """

    args = parse_args()

    name = args.contact
    msg = args.message
    chrome_driver_path = args.chrome_driver_path
    session_path = args.session_path


    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={session_path}")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url='https://web.whatsapp.com')

    search_box = get_search_box_when_page_loaded(driver)
    play_sound()

    search_box.send_keys(name)
    search_box.send_keys(Keys.ENTER)

    msg_box = get_text_box(driver)
    send_message(message=msg, element=msg_box)

    driver.close()

if __name__ == "__main__":
    main()
