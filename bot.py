import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# টোকেন ও সাপোর্ট আইডি
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
SUPPORT_ID = "@aratboos16"

# ভাষা নির্বাচনের কিবোর্ড (শুরুতে)
def language_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )
    return markup

# বাংলা মূল মেনু (৫টি বাটন)
def main_menu_bn():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("◆ 1. মেটা ভেরিফাই", callback_data="meta_verify_bn"),
        InlineKeyboardButton("◆ 2. পেমেন্ট ও নিয়মাবলী", callback_data="payment_rules_bn"),
        InlineKeyboardButton("◆ 3. সুবিধা ও শর্তাবলী", callback_data="benefits_bn"),
        InlineKeyboardButton("◆ 4. লাইভ সাপোর্ট", callback_data="live_support_bn"),
        InlineKeyboardButton("◆ 5. কিভাবে কাজ করে", callback_data="how_it_works_bn")
    )
    return markup

# ইংরেজি মূল মেনু (৫টি বাটন)
def main_menu_en():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("◆ 1. Meta Verify", callback_data="meta_verify_en"),
        InlineKeyboardButton("◆ 2. Payment & Rules", callback_data="payment_rules_en"),
        InlineKeyboardButton("◆ 3. Benefits & Terms", callback_data="benefits_en"),
        InlineKeyboardButton("◆ 4. Live Support", callback_data="live_support_en"),
        InlineKeyboardButton("◆ 5. How It Works", callback_data="how_it_works_en")
    )
    return markup

# ব্যাক বাটন (বাংলা)
def back_to_menu_bn():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 মূল মেনুতে ফিরুন", callback_data="main_menu_bn"))
    return markup

# ব্যাক বাটন (ইংরেজি)
def back_to_menu_en():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu_en"))
    return markup

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ **স্বাগতম! অনুগ্রহ করে আপনার পছন্দের ভাষা নির্বাচন করুন:**\n\n"
        "✨ **Please select your preferred language:**"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=language_keyboard())

# বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "lang_bn":
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_bn())

    elif call.data == "lang_en":
        text = "✨ **Main Menu:**\n\nPlease choose your required service from the options below:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_en())

    # --- বাংলা অপশনসমূহ ---
    elif call.data == "meta_verify_bn":
        text = "🛡️ **মেটা ভেরিফাই আবেদন প্রক্রিয়া:**\n\nদয়া করে আপনার ফেসবুক প্রোফাইল বা পেজের সঠিক লিংকটি এখানে পাঠান।"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_bn())

    elif call.data == "payment_rules_bn":
        text = "💳 **পেমেন্ট ও নিয়মাবলী:**\n\nআমাদের সার্ভিস চার্জ এবং পেমেন্ট করার বিস্তারিত নিয়মাবলি এখানে দেওয়া হলো..."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_bn())

    elif call.data == "benefits_bn":
        text = "⭐ **সুবিধা ও শর্তাবলী:**\n\nমেটা ভেরিফাই বা ব্লু টিক পাওয়ার পর আপনি কী কী সুবিধা পাবেন তা এখানে দেখুন..."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_bn())

    elif call.data == "live_support_bn":
        text = f"📞 **লাইভ সাপোর্ট:**\n\nযেকোনো প্রয়োজনে সরাসরি আমাদের সাপোর্ট আইডিতে যোগাযোগ করুন: {SUPPORT_ID}"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_bn())

    elif call.data == "how_it_works_bn":
        text = "⚙️ **কিভাবে কাজ করে:**\n\nবট ব্যবহারের ধাপে ধাপে নির্দেশিকা এখানে দেওয়া হলো..."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_bn())

    elif call.data == "main_menu_bn":
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_bn())

    # --- ইংরেজি অপশনসমূহ ---
    elif call.data == "meta_verify_en":
        text = "🛡️ **Meta Verify Application Process:**\n\nPlease send the correct link of your Facebook profile or page here."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_en())

    elif call.data == "payment_rules_en":
        text = "💳 **Payment & Rules:**\n\nDetailed rules and service charges for payment are provided here..."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_en())

    elif call.data == "benefits_en":
        text = "⭐ **Benefits & Terms:**\n\nCheck out the benefits and terms after getting Meta Verify..."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_en())

    elif call.data == "live_support_en":
        text = f"📞 **Live Support:**\n\nFor any assistance, contact our support ID directly: {SUPPORT_ID}"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_en())

    elif call.data == "how_it_works_en":
        text = "⚙️ **How It Works:**\n\nStep-by-step guidelines for using the bot are listed here..."
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_en())

    elif call.data == "main_menu_en":
        text = "✨ **Main Menu:**\n\nPlease choose your required service from the options below:"
        bot.edit_message_text(text, chat_id, message_id, parse_node="Markdown", reply_markup=main_menu_en())

# মেসেজ ও লিংক হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_text = message.text.strip()
    valid_prefixes = ("https://www.facebook.com/", "https://facebook.com/", "https://fb.com/", "https://m.facebook.com/")
    
    if user_text.startswith("http://") or user_text.startswith("https://"):
        if user_text.startswith(valid_prefixes):
            bot.send_message(message.chat.id, "✅ **লিংক সফলভাবে গৃহীত হয়েছে!** প্রসেসিং চলছে (সময় লাগবে প্রায় ১ ঘণ্টা ৩০ মিনিট)।", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "❌ **অবৈধ লিংক!** দয়া করে সঠিক ফেসবুক লিংক দিন।", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "দয়া করে `/start` লিখে মেনু থেকে ভাষা ও অপশন সিলেক্ট করুন।")

# বট রান করা
print("Bot is running...")
bot.infinity_polling()
