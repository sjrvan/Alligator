# -*- coding: utf-8 -*-
import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
import settings
from game import Game

logger = None
games = {}
conn = sqlite3.connect("rating.db")
cursor = conn.cursor()

def get_or_create_game(chat_id: int) -> Game:
    global games
    game = games.get(chat_id, None)
    if game is None:
        game = Game()
        games[chat_id] = game
    return game

def setup_logger():
    global logger
    file_handler = logging.FileHandler('crocodile.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def get_message(chat_id: int, key: str):
    # Bu fonksiyon, dil dosyasındaki metinleri çekmek için kullanılır
    # İlgili dilin metinlerini burada ekleyebilirsiniz.
    # Şu anda sadece İngilizce (en) ve Azerbaycanca (az) destekleniyor.
    messages = {
        'en': {
            'addme_btn': '➕ Add Me to a Group ➕',
            'support_btn': '⛑ Support Group',
            'updates_btn': '📲 Updates Channel',
            'admin_btn': 'Crazy MMC',
            'welcome_msg': 'Hello!👋 I am a game bot designed to play a word guessing game in your group. You can play by adding me to a group.',
            'game_started': 'Word Game Started ⚡',
            'set_master_msg': '{} is the master now! ({})',
            'show_word_btn': '✅ Show the Word',
            'change_word_btn': '🔄 Change the Word',
            'wait_master_msg': 'Wait for {} seconds to become the master. ⏳',
            'correct_answer_msg': '*{}* was guessed by {}! 🔥'
        },
        'az': {
            'addme_btn': '➕ Qrupa Əlavə Et ➕',
            'support_btn': '⛑ Dəstək Qrupu',
            'updates_btn': '📲 Yeniliklər Kanalı',
            'admin_btn': 'Crazy MMC',
            'welcome_msg': 'Salam!👋 Mən sizin qurupunuzda insan adları tapmağ üçün yaradılmış Oyun botuyam. Məni qurupa əlavə edərək oynaya bilərsiz.',
            'game_started': 'Ad Oyunu Başladı ⚡',
            'set_master_msg': '{} adı başa salır! ({})',
            'show_word_btn': '✅ Ada bax',
            'change_word_btn': '🔄 Adı dəyiş',
            'wait_master_msg': 'Aparıcı olmaq üçün {} saniyə qalıb ⏳',
            'correct_answer_msg': '*{}* adını {} tapdı 🔥'
        }
    }

    language = {
        'tr': {
            'addme_btn': '➕ Qrupa Əlavə Et ➕',
            'support_btn': '⛑ Dəstək Qrupu',
            'updates_btn': '📲 Yeniliklər Kanalı',
            'admin_btn': 'Crazy MMC',
            'welcome_msg': 'Salam!👋 Mən sizin qurupunuzda insan adları tapmağ üçün yaradılmış Oyun botuyam. Məni qurupa əlavə edərək oynaya bilərsiz.',
            'game_started': 'Ad Oyunu Başladı ⚡',
            'set_master_msg': '{} adı başa salır! ({})',
            'show_word_btn': '✅ Ada bax',
            'change_word_btn': '🔄 Adı dəyiş',
            'wait_master_msg': 'Aparıcı olmaq üçün {} saniyə qalıb ⏳',
            'correct_answer_msg': '*{}* adını {} tapdı 🔥'
        }
    }

    language_code = 'en'  # Varsayılan olarak İngilizce
    # Şu anda sadece İngilizce ve Azerbaycanca destekleniyor, diğer dillere eklemek isterseniz, dil kodlarına ve metinlere uygun şekilde eklemeler yapabilirsiniz.

    if chat_id in language:
        language_code = language[chat_id]

    if key in messages[language_code]:
        return messages[language_code][key]
    else:
        return messages['en'][key]

def help(update, context):
    update.message.reply_text(get_message(update.message.chat.id, 'help'))

# Diğer kodlar aynı kalıyor...

# Ana işlev
def main():
    setup_logger()
    updater = Updater(settings.TOKEN, use_context=True)
    bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("game", command_start))
    dp.add_handler(CommandHandler("master", command_master))
    dp.add_handler(CommandHandler("show_word", command_show_word))
    dp.add_handler(CommandHandler("change_word", command_change_word))
    dp.add_handler(CommandHandler("rating", command_rating))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", command_start))

    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(MessageHandler(Filters.text, is_word_answered))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
