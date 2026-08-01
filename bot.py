import telebot
from telebot import types

TOKEN = '8710197095:AAGcdkvFLkQV8eHCRFcFoOyHkZ3WASf5vrM'
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_order = types.InlineKeyboardButton("🚀 মেটা ভেরিফিকেশন (ব্লু টিক) নিন", callback_data='order')
    btn_pricing = types.InlineKeyboardButton("💰 প্রাইসিং ও পেমেন্ট মেথড", callback_data='pricing')
    btn_help = types.InlineKeyboardButton("❓ কীভাবে কাজ করে?", callback_data='help')
    markup.add(btn_order, btn_pricing, btn_help)
    
    welcome_text = (
        "🌟 **স্বাগতম! Meta Verified (Blue Tick) সার্ভিসে আপনাকে স্বাগতম।** 💙\n\n"
        "আপনার ফেসবুক প্রোফাইল বা পেজকে খুব সহজেই ভেরিফাইড করে নিন। "
        "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == 'order':
        bot.answer_callback_query(call.id)
        user_data[chat_id] = {}
        bot.send_message(chat_id, "📌 দয়া করে আপনার **ফেসবুক প্রোফাইল বা পেজের সঠিক লিংকটি** এখানে পাঠান:")
        bot.register_next_step_handler(call.message, get_profile_link)
        
    elif call.data == 'pricing':
        bot.answer_callback_query(call.id)
        pricing_text = (
            "💰 **প্রাইসিং ও পেমেন্ট তথ্য:**\n\n"
            "• ফেসবুক প্রোফাইল ভেরিফিকেশন ফি: নির্দিষ্ট চার্জ প্রযোজ্য।\n"
            "• পেমেন্ট মাধ্যম: বিকাশ, নগদ, রকেট (Personal).\n\n"
            "বিকাশ/নগদ সেন্ড মানি করুন:\n`01XXXXXXXXX`\n\n"
            "টাকা পাঠিয়ে ট্রানজেকশন আইডি এবং স্ক্রিনশট আমাদের দিন।"
        )
        bot.send_message(chat_id, pricing_text, parse_mode="Markdown")
        
    elif call.data == 'help':
        bot.answer_callback_query(call.id)
        help_text = (
            "📌 **ব্লু টিক পাওয়ার সহজ ধাপসমূহ:**\n\n"
            "১. 'মেটা ভেরিফিকেশন নিন' বাটনে ক্লিক করুন।\n"
            "২. আপনার ফেসবুক প্রোফাইল লিংক ও নাম দিন।\n"
            "৩. পেমেন্ট সম্পন্ন করে TrxID বা স্ক্রিনশট দিন।\n"
            "৪. আমাদের টিম চেক করে আপনার প্রোফাইল ভেরিফাই করে দেবে!"
        )
        bot.send_message(chat_id, help_text, parse_mode="Markdown")

def get_profile_link(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'link': message.text}
    bot.send_message(chat_id, "✍️ ধন্যবাদ! এবার আপনার প্রোফাইলে থাকা **সঠিক নামটি** (Profile Name) এখানে লিখুন:")
    bot.register_next_step_handler(message, get_profile_name)

def get_profile_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    payment_instruction = (
        "💳 **শেষ ধাপ - পেমেন্ট কনফার্মেশন:**\n\n"
        "আমাদের বিকাশ/নগদ নাম্বারে (`01XXXXXXXXX`) ফি পাঠিয়ে দিন।\n"
        "এরপর আপনার **পেমেন্টের ট্রানজেকশন আইডি (TrxID)** অথবা **স্ক্রিনশটটি** এই বটে পাঠিয়ে দিন।"
    )
    bot.send_message(chat_id, payment_instruction, parse_mode="Markdown")
    bot.register_next_step_handler(message, get_payment_proof)

def get_payment_proof(message):
    chat_id = message.chat.id
    confirmation_text = (
        "🎉 **আপনার অর্ডারটি সফলভাবে সাবমিট হয়েছে!**\n\n"
        "আপনার দেওয়া তথ্যগুলো আমাদের টিম ম্যানুয়ালি যাচাই করছে। খুব শীঘ্রই আপনার প্রোফাইলে ব্লু টিক প্রসেস সম্পন্ন করা হবে। ধন্যবাদ আমাদের সাথে থাকার জন্য! 💙"
    )
    bot.send_message(chat_id, confirmation_text, parse_mode="Markdown")

print("Bot is running smoothly on cloud...")
bot.infinity_polling()