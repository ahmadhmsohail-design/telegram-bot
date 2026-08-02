import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# গিটহব সিক্রেট থেকে টোকেন নেওয়া
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# সাপোর্ট আইডি
SUPPORT_ID = "@aratboos16"

# মূল মেনু বাটন তৈরি (নতুন ডিজাইন ও শর্ট প্রিফিক্স সহ)
def main_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("◆ 1. মেটা ভেরিফাই", callback_data="meta_verify"),
        InlineKeyboardButton("◆ 2. পেমেন্ট ও নিয়মাবলী", callback_data="payment_rules"),
        InlineKeyboardButton("◆ 3. সুবিধা ও শর্তাবলী", callback_data="benefits"),
        InlineKeyboardButton("◆ 4. লাইভ সাপোর্ট", callback_data="live_support"),
        InlineKeyboardButton("◆ 5. কিভাবে কাজ করে", callback_data="how_it_works")
    )
    return markup

# ব্যাক বাটন
def back_to_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Back to Bot", callback_data="main_menu"))
    return markup

# লিংক ভুল হলে রিট্রাই বাটন
def retry_link_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 আবার চেষ্টা করুন", callback_data="meta_verify"),
        InlineKeyboardButton("🔙 Back to Bot", callback_data="main_menu")
    )
    return markup

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ **স্বাগতম আমাদের বটের দুনিয়ায়!** ✨\n\n"
        "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

# বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "meta_verify":
        text = (
            "🛡️ **মেটা ভেরিফাই আবেদন প্রক্রিয়া:**\n\n"
            "দয়া করে আপনার ফেসবুক প্রোফাইল বা পেজের সঠিক লিংকটি এখানে পাঠান।\n"
            "*(সিস্টেম স্বয়ংক্রিয়ভাবে লিংকের শুরু বা প্রিফিক্স যাচাই করবে)*"
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())
        # স্টেট বা ফ্ল্যাগ সেট করা যেতে পারে যে ইউজার এখন লিংক পাঠাবে

    elif call.data == "payment_rules":
        text = "💳 **পেমেন্ট ও নিয়মাবলী:**\n\nএখানে আপনার পেমেন্টের বিস্তারিত নিয়ম থাকবে।"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())

    elif call.data == "benefits":
        text = "⭐ **সুবিধা ও শর্তাবলী:**\n\nআমাদের সার্ভিসের সুবিধাগুলো এখানে দেখতে পাবেন।"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())

    elif call.data == "live_support":
        text = f"📞 **লাইভ সাপোর্ট:**\n\nযেকোনো সমস্যায় সরাসরি যোগাযোগ করুন: {SUPPORT_ID}"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())

    elif call.data == "how_it_works":
        text = "⚙️ **কীভাবে কাজ করে:**\n\nবট ব্যবহারের নিয়মাবলী এখানে দেওয়া আছে।"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())

    elif call.data == "main_menu":
        text = "✨ **মূল মেনু:**\n\nনিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu_keyboard())

# টেক্সট মেসেজ হ্যান্ডলার (লিংক ভ্যালিডেশন লজিক সহ)
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    user_text = message.text.strip()
    
    # শট কী বা প্রথম অক্ষর দিয়ে চ্যাট বা কমান্ড ফিল্টারিং
    if user_text.lower().startswith(('মে', 'meta', '1')):
        bot.send_message(message.chat.id, "দয়া করে আপনার ফেসবুক প্রোফাইল বা পেজের সঠিক লিংকটি পাঠান।")
        return

    # স্মার্ট লিংক ভ্যালিডেশন চেক (লিংকের প্রথম অংশ বা প্রিফিক্স যাচাই)
    valid_prefixes = ("https://www.facebook.com/", "https://facebook.com/", "https://fb.com/", "https://m.facebook.com/")
    
    if user_text.startswith("http://") or user_text.startswith("https://"):
        if user_text.startswith(valid_prefixes):
            # লিংক সঠিক হলে প্রসেসিং শুরু
            success_msg = (
                "✅ **লিংক সফলভাবে গৃহীত হয়েছে!**\n\n"
                "আপনার প্রসেসিং শুরু হয়েছে। কাজটি সম্পন্ন হতে আনুমানিক ১ ঘণ্টা ৩০ মিনিট থেকে ১ ঘণ্টা ৪০ মিনিট সময় লাগতে পারে।"
            )
            bot.send_message(message.chat.id, success_msg, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())
        else:
            # ভুল বা অন্য কোনো ওয়েবসাইটের লিংক দিলে ওয়ার্নিং
            error_msg = (
                "❌ **অবাধে লিংক বা ভুল ফরম্যাট!**\n\n"
                "আপনার প্রদানকৃত লিংকের প্রথম অংশ বা ফরম্যাটটি সঠিক নয়। এটি ফেসবুকের সঠিক লিংক নয়। দয়া করে সঠিক লিংক দিয়ে আবার চেষ্টা করুন।"
            )
            bot.send_message(message.chat.id, error_msg, parse_mode="Markdown", reply_markup=retry_link_keyboard())
    else:
        # সাধারণ উল্টোপাল্টা টেক্সট দিলে মূল মেনুতে গাইড করা
        bot.send_message(message.chat.id, "দয়া করে নিচের মেনু ব্যবহার করুন অথবা সঠিক ফেসবুক লিংক পাঠান।", reply_markup=main_menu_keyboard())

# বট রান করা
print("Bot is running...")
bot.infinity_polling()
