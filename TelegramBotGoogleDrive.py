import os
import pprint
import io
from datetime import datetime

import telebot
from telebot import types

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build

# First you need to create a technical account in Google Account
# Follow this link to find out how to do this https://support.google.com/a/answer/7378726?hl=en

# TOKEN of your telegram bot
BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

SCOPES = ['https://www.googleapis.com/auth/drive']

# Path to JSON file Google Drive Key your technical account
SERVICE_ACCOUNT_FILE = ''

# Path to folder on Google Drive where files should be saved
folder_id = ''

# Folder for saving temporary files on the server
srcFolder = ''


# This is a list of message types in telegram
@bot.message_handler(content_types=["document","photo","audio","video"])


# # This function is for saving documents and files with extensions
def saveDocument(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = srcFolder + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        pp = pprint.PrettyPrinter(indent=4)

        credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        file_path_download = src

        media = MediaFileUpload(file_path_download, resumable=True)
        name = message.document.file_name

        file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        pp.pprint(r)

    except:
        saveAudio(message)


# This function is for saving audio files
def saveAudio(message):
    try:
        chat_id = message.chat.id
        print(bot.get_file(message.audio.file_id))

        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = srcFolder + message.audio.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        pp = pprint.PrettyPrinter(indent=4)

        credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        file_path_download = src

        media = MediaFileUpload(file_path_download, resumable=True)
        name = message.audio.file_name

        file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        pp.pprint(r)

    except:
        savePhoto(message)


# This function is for saving photos and pictures
def savePhoto(message):
    try:
        photoSave = message.photo[-1].file_id
        file_info = bot.get_file(photoSave)

        downloaded_file = bot.download_file(file_info.file_path)

        now = datetime.now()

        file_name = "photo_" + now.strftime("%d_%m_%Y_%H-%M-%S") + ".jpg"

        src = srcFolder + file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        pp = pprint.PrettyPrinter(indent=4)

        credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        file_path_download = src

        media = MediaFileUpload(file_path_download, resumable=True)

        file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        pp.pprint(r)

    except:
        saveVideo(message)


# This function is for saving video files
def saveVideo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = srcFolder + message.video.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        pp = pprint.PrettyPrinter(indent=4)

        credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        file_path_download = src

        media = MediaFileUpload(file_path_download, resumable=True)
        name = message.video.file_name

        file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        pp.pprint(r)

    except Exception as e:
        bot.reply_to(message, e)


# Launching the file saving function
def handle_docs(message):
    saveDocument(message)


bot.infinity_polling()