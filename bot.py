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

# বাংলা মূল মেনু: উপরে-নিচে লম্বালম্বিভাবে ৫টি সম্পূর্ণ নামের বাটন
def get_main_buttons_bn():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("◆ ১. মেটা ভেরিফাই", callback_data="meta_verify_bn"),
        InlineKeyboardButton("◆ ২. পেমেন্ট ও নিয়মাবলী", callback_data="payment_rules_bn"),
        InlineKeyboardButton("◆ ৩. সুবিধা ও শর্তাবলী", callback_data="benefits_bn"),
        InlineKeyboardButton("◆ ৪. লাইভ সাপোর্ট", callback_data="live_support_bn"),
        InlineKeyboardButton("◆ ৫. কিভাবে কাজ করে", callback_data="how_it_works_bn")
    )
    return markup

# ইংরেজি মূল মেনু: উপরে-নিচে লম্বালম্বিভাবে ৫টি সম্পূর্ণ নামের বাটন
def get_main_buttons_en():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("◆ 1. Meta Verify", callback_data="meta_verify_en"),
        InlineKeyboardButton("◆ 2. Payment & Rules", callback_data="payment_rules_en"),
        InlineKeyboardButton("◆ 3. Benefits & Terms", callback_data="benefits_en"),
        InlineKeyboardButton("◆ 4. Live Support", callback_data="live_support_en"),
        InlineKeyboardButton("◆ 5. How It Works", callback_data="how_it_works_en")
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

# বাটন ক্লিক হ্যান্ডলার (মেসেজ এডিট সিস্টেম)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "lang_bn":
        user_states[chat_id] = {"lang": "bn", "step": "main_menu"}
        markup = get_main_buttons_bn()
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "lang_en":
        user_states[chat_id] = {"lang": "en", "step": "main_menu"}
        markup = get_main_buttons_en()
        text = "✨ **Main Menu:**\n\nPlease choose your required service from the options below:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ১. মেটা ভেরিফাই (বাংলা) ---
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

    # --- ২. পেমেন্ট ও নিয়মাবলী (বাংলা) ---
    elif call.data == "payment_rules_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "💳 **পেমেন্ট ও নিয়মাবলী:**\n\n"
            "১. **অগ্রিম পেমেন্ট নেই:** কাজের আগে আমাদের পক্ষ থেকে কোনো প্রকার টাকা বা ফি নেওয়া হয় না। সম্পূর্ণ কাজটি সফলভাবে শেষ হওয়ার পরেই পেমেন্ট প্রযোজ্য।\n"
            "২. **কোম্পানির যোগাযোগ ও পেমেন্ট আদায়:** কাজ সম্পূর্ণ হওয়ার পর আমাদের কোম্পানির অফিশিয়াল প্রতিনিধি নিজে আপনার সাথে সরাসরি যোগাযোগ করবেন এবং আপনার কাছ থেকে পেমেন্ট আদায় করবেন।\n"
            "৩. **নিরাপত্তা ও সতর্কতা:** কাজের আগে বা অন্য কেউ টাকা দাবি করলে তা দেওয়া থেকে বিরত থাকুন। শুধুমাত্র আমাদের কোম্পানির নির্ধারিত প্রতিনিধি যোগাযোগ করার পরেই পেমেন্ট সম্পন্ন করুন।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৩. সুবিধা ও শর্তাবলী (বাংলা) ---
    elif call.data == "benefits_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "⭐ **সুবিধা ও শর্তাবলী:**\n\n"
            "🛡️ **সুবিধাসমূহ:**\n"
            "• ফেসবুক প্রোফাইল বা পেজে অফিশিয়াল ব্লু টিক (Verified Badge) যুক্ত হবে।\n"
            "• প্রিমিয়াম সাপোর্ট এবং উন্নত অ্যাকাউন্ট সিকিউরিটি।\n\n"
            "📋 **শর্তাবলী:**\n"
            "• অ্যাকাউন্টের নাম ও এনআইডি কার্ডের তথ্য হুবহু মিল থাকতে হবে।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৪. লাইভ সাপোর্ট (বাংলা) ---
    elif call.data == "live_support_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            f"📞 **লাইভ সাপোর্ট:**\n\n"
            f"সেবা নিতে গিয়ে কোনো সমস্যা হলে সরাসরি আমাদের অফিশিয়াল সাপোর্ট আইডিতে যোগাযোগ করুন:\n\n"
            f"👉 সাপোর্ট আইডি: {SUPPORT_ID}"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৫. কিভাবে কাজ করে (বাংলা) ---
    elif call.data == "how_it_works_bn":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "⚙️ **কিভাবে কাজ করে (নির্দেশিকা):**\n\n"
            "১. মেটা ভেরিফাই অপশন সিলেক্ট করে প্যাকেজ বেছে নিন।\n"
            "২. সিকিউর লিংকে প্রবেশ করে ফেসবুক অ্যাকাউন্ট লগইন ও লিংক দিন।\n"
            "৩. এনআইডি এবং সেলফি আপলোড করে আবেদন সম্পন্ন করুন।"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 পেছনে যান", callback_data="main_menu_bn"),
            InlineKeyboardButton("🏠 হোম পেজ", callback_data="main_menu_bn")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- হোম পেজে ফিরে যাওয়া (বাংলা) ---
    elif call.data == "main_menu_bn":
        user_states[chat_id]["step"] = "main_menu"
        markup = get_main_buttons_bn()
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ১. মেটা ভেরিফাই (ইংরেজি - সম্পূর্ণ বিবরণসহ) ---
    elif call.data == "meta_verify_en":
        user_states[chat_id]["step"] = "verify_step_1_en"
        text = (
            "🛡️ **Meta Verify Application (Step 1/4):**\n\n"
            "Select your preferred package from below:\n"
            "• 1 Month – 300 BDT\n"
            "• 3 Months – 900 BDT\n"
            "• 5 Months – 1500 BDT\n"
            "• 1 Year – 3000 BDT\n\n"
            "Please type your package number (e.g., 1, 2, 3, or 4) in the chat box."
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ২. পেমেন্ট ও নিয়মাবলী (ইংরেজি - সম্পূর্ণ বিবরণসহ) ---
    elif call.data == "payment_rules_en":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "💳 **Payment & Rules:**\n\n"
            "1. **No Advance Payment:** We do not take any kind of money before the work is done. Payment is applicable only after the work is fully completed.\n"
            "2. **Contact & Collection:** After the work is finished, our company representative will directly contact you and collect the payment.\n"
            "3. **Security & Precaution:** Do not pay anyone before the work starts. Complete the payment only after our authorized representative contacts you."
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৩. সুবিধা ও শর্তাবলী (ইংরেজি - সম্পূর্ণ বিবরণসহ) ---
    elif call.data == "benefits_en":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "⭐ **Benefits & Terms:**\n\n"
            "🛡️ **Benefits:**\n"
            "• Official Verified Blue Badge on Facebook profile or page.\n"
            "• Premium support and enhanced account security.\n\n"
            "📋 **Terms:**\n"
            "• Account name and NID card information must match completely."
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৪. লাইভ সাপোর্ট (ইংরেজি - সম্পূর্ণ বিবরণসহ) ---
    elif call.data == "live_support_en":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            f"📞 **Live Support:**\n\n"
            f"If you face any issues, contact our official support ID directly:\n\n"
            f"👉 Support ID: {SUPPORT_ID}"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- ৫. কিভাবে কাজ করে (ইংরেজি - সম্পূর্ণ বিবরণসহ) ---
    elif call.data == "how_it_works_en":
        user_states[chat_id]["step"] = "main_menu"
        text = (
            "⚙️ **How It Works:**\n\n"
            "1. Select Meta Verify and choose your package.\n"
            "2. Access the secure link, log in to Facebook, and provide your profile link.\n"
            "3. Upload your NID and selfie to complete the application."
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🔙 Back", callback_data="main_menu_en"),
            InlineKeyboardButton("🏠 Home", callback_data="main_menu_en")
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # --- হোম পেজে ফিরে যাওয়া (ইংরেজি) ---
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
    if current_step in ["verify_step_1", "verify_step_1_en"]:
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
            bot.send_message(chat_id, "❌ দয়া করে সঠিক প্যাকেজ নম্বরটি দিন (যেমন: ১, ২, ৩ বা ৪) / Please provide a valid package number.")

    # ধাপ ২: শুধুমাত্র https:// চেক করা
    elif current_step == "verify_step_2":
        if "https://" in user_text:
            user_states[chat_id]["step"] = "verify_step_3"
            next_text = (
                "🆔 **ধাপ ৩/৪: এনআইডি বা জন্ম সনদ আপলোড**\n\n"
                "✅ লিংক গ্রহণ করা হয়েছে!\n\n"
                "দয়া করে আপনার জন্ম সনদ বা এনআইডি (NID) কার্ডের একটি পরিষ্কার ছবি তুলে এখানে আপলোড করুন।"
            )
            bot.send_message(chat_id, next_text, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "❌ **Wrong!** সঠিক নিয়মে `https://` দিয়ে লিংকটি দিন।")

    else:
        bot.send_message(chat_id, "দয়া করে প্রথমে `/start` লিখে মেনু ওপেন করুন। / Please type `/start` to open the menu.")

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
        bot.send_message(chat_id, "দয়া করে প্রথমে `/start` লিখে ভেরিফাই অপشن শুরু করুন।")

print("Bot is running smoothly...")
bot.infinity_polling()
