import telebot
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta

# Bot token
BOT_TOKEN = '7217012373:AAHFRCmGs10I0jFE3qCHAjS4db3eE6ewn_c'
OWNER_USER_ID = 7303810912
PROOF_CHANNEL_ID = -1002113563800 #Replace With The Chat Id Of The Channel Which Will Be Proof Channel
FORWARD_CHANNEL_IDS = [-1002224203739, -1001974696244, -1002113563800] #Replace With The Ids Of The Channel To Be Posted

bot = telebot.TeleBot(BOT_TOKEN)

required_channels = ["@TheSmartDev", "@modviprmbackup", "@modDirect_download"]
buttons = [
    ("🔗SmartDev", "https://t.me/TheSmartDev"),
    ("🔗 ModVipRM Backup", "https://t.me/modviprmbackup"),
    ("📂 ModVipRM APK", "https://t.me/modDirect_download")
]

# Dictionary to store the mapping of forwarded messages to original users
forwarded_messages = {}

# Define promo links for different services
promo_links = {
    "YouTube": [
        "https://families.google.com/join/promo/StTMvLwjgxuEhNMIIqeUPQA9ZzjJuQ?pli=1",
        "https://families.google.com/join/promo/hIx3V_H3WcEHbgv8Vr9h1YMG5ceGkw?pli=1",
        "https://families.google.com/join/promo/DSgghlmPq1nVoB5npLTqhQJSUq_CGw?pli=1",
        "https://families.google.com/join/promo/-6qah32kH-4yORY2993Wc2qfNRSaBA?pli=1",
        "https://families.google.com/join/promo/nvNKCIgHPNeh3ORtIb0r0FSISxPERw?pli=1"
    ],
    "Crunchyroll": [
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@"
    ],
    "Canva": [
        "Email: example1@canva.com Pass: password1",
        "Email: example2@canva.com Pass: password2"
    ],
    "Hostinger": [
        "Email: example1@hostinger.com Pass: password1",
        "Email: example2@hostinger.com Pass: password2"
    ],
    "Netflix": [
        "Email: example1@netflix.com Pass: password1",
        "Email: example2@netflix.com Pass: password2"
    ],
    "PrimeVideo": [
        "Email: example1@primevideo.com Pass: password1",
        "Email: example2@primevideo.com Pass: password2"
    ],
    "Spotify": [
        "Email: example1@spotify.com Pass: password1",
        "Email: example2@spotify.com Pass: password2"
    ]
}

# Define image URLs for different services
service_images = {
    "YouTube": "https://t.me/BotsDevZone/269",
    "Crunchyroll": "https://t.me/BotsDevZone/270",
    "Netflix": "https://t.me/BotsDevZone/271",
    "PrimeVideo": "https://t.me/BotsDevZone/272",
    "Canva": "https://t.me/BotsDevZone/273",
    "Spotify": "https://t.me/BotsDevZone/274"
}

# Storage for generated codes and redeemed information
generated_codes = {}
redeemed_codes = {}
# Storage for user IDs
user_ids = set()
# Bot start time
start_time = datetime.now()

# Function to check channel join status
def is_user_in_channels(user_id):
    try:
        for channel in required_channels:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except Exception as e:
        print(f"Error checking channel status: {e}")
        return False

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Store user ID for broadcasting later
    user_ids.add(user_id)
    try:
        if not is_user_in_channels(user_id):
            keyboard = InlineKeyboardMarkup()
            # Arrange buttons in 2-2-1 formation
            keyboard.row(InlineKeyboardButton(text="🔗 SmartDev", url="https://t.me/TheSmartDev"),
                         InlineKeyboardButton(text="🔗 ModVipRM Backup", url="https://t.me/modviprmbackup"))
            keyboard.row(InlineKeyboardButton(text="📂 ModVipRM APK", url="https://t.me/modDirect_download"))
            keyboard.add(InlineKeyboardButton(text="✅ Joined", callback_data="joined_check"))
            
            bot.send_photo(
                message.chat.id,
                photo="https://t.me/BotsDevZone/275",
                caption=("*Welcome to Redeem Code ABIR XD Bot!*\n\n"
                         "*You can now use the bot.*\n"
                         "*Use /redeem <code> to redeem a code.*\n"
                         "*OWNER: @ISmartDevs*\n"
                         "*Join: ModVipRM*"),
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            bot.send_message(message.chat.id, "*Welcome back! You are already joined! Use /redeem <code> to redeem.*", parse_mode="Markdown")
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 403:
            print(f"User {user_id} has blocked the bot.")
        else:
            print(f"Error: {e}")

# Callback handler for joined button
@bot.callback_query_handler(func=lambda call: call.data == "joined_check")
def joined_check(call):
    user_id = call.from_user.id
    if is_user_in_channels(user_id):
        bot.answer_callback_query(call.id, "You have joined the channels!")
        bot.send_message(call.message.chat.id, "*You can now use the bot. Use /redeem <code> to redeem a code.*", parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "Please join all required channels first.", show_alert=True)

# Generate redeem codes (Owner only)
@bot.message_handler(commands=['gen'])
def generate_codes(message):
    if message.from_user.username != "ISmartDevs":
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    try:
        _, count, service_name = message.text.split()
        count = int(count)
    except ValueError:
        bot.reply_to(message, "*Usage: /gen <number_of_codes> <service_name>*", parse_mode="Markdown")
        return

    valid_services = [
        "YouTube", "Crunchyroll", "Canva", "Hostinger", "Netflix", "PrimeVideo", "Spotify"
    ]

    if service_name not in valid_services:
        bot.reply_to(message, f"*Invalid service name. Please choose from: {', '.join(valid_services)}*", parse_mode="Markdown")
        return

    codes = []
    for _ in range(count):
        code = f"{service_name.upper()}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        if code not in generated_codes:  # Ensure unique codes
            generated_codes[code] = None
            codes.append(code)

    # Format the codes as per the new requirement
    formatted_codes = "\n".join([f"➔ `{code}` ☑️" for code in codes])

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🧾 Updates Channel ☑️", url="https://t.me/ModVipRM"))
    keyboard.add(InlineKeyboardButton(text="🤖 Bot Owner ☑️", url="https://t.me/ISmartDevs"))

    bot.reply_to(
        message,
        f"*Hey Bro All The Codes Generated Are Below For {service_name}.*\n\n{formatted_codes}\n\n*Need help? Join our channels or contact the bot owner for assistance!*",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Post command handler
@bot.message_handler(commands=['post'])
def post_announcement(message):
    if message.from_user.username != "ISmartDevs":
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    if not generated_codes:
        bot.reply_to(message, "No codes have been generated yet.")
        return

    # Extract the service name from the first code
    first_code = next(iter(generated_codes.keys()))
    service_name = first_code.split('-')[0].capitalize()

    # Special case for "PrimeVideo"
    if service_name.lower() == "primevideo":
        service_name = "PrimeVideo"

    # Format the codes for the post
    formatted_codes = "\n".join([f"➔ `{code}` ☑️" for code in generated_codes.keys()])

    # Create the post content
    post_content = (
        f"➡️ ✨ *{service_name} Premium Account Giveaway* ✨ ⬅️\n\n"
        f"🟢 *Generated {len(generated_codes)} Redeem Codes* 🟢:\n\n"
        f"{formatted_codes}\n\n"
        f"➡️ *Redeem The Code By Sending This Command- /redeem {first_code.split('-')[0]}-XXXX-XXXX-XXXX*\n\n"
        f"➡️ *Redeem From This Bot-  Xtreme Redeem ⚡️ [Open Bot To Redeem](https://t.me/Redeem_Ultimate_Bot)*\n\n"
        "🔹 *First 05 Users Will Win It* 🔺\n"
        "🔹 *Hurry Up! Only The First 5 Users Will Win This Giveaway !* ⌛️\n\n"
        "❤️ *Send Screenshot There- @ISmartDevs* ✅ ✔️\n\n"
        "➡️ *Share Our Channel For More Exciting Giveaways* ✅\n"
        "➡️ *For More Enquiry —— ❤️ @ISmartDevs* ✔️\n"
        "➡️ *For More Information Check @ModVipRM* ☝️\n\n"
        "❤️ *Thank You For Staying With Us* ❤️"
    )

    # Get the image URL for the service
    image_url = service_images.get(service_name, "https://t.me/abir_x_official_developer/82")

    # Define the keyboard
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="✅ Open Bot To Redeem", url="https://t.me/Redeem_Ultimate_Bot"))

    # Send the post to the main channel
    try:
        bot.send_photo(
            message.chat.id,
            photo=image_url,
            caption=post_content,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.reply_to(message, f"Error sending post to the main channel: {e}")

    # Forward the post to other channels
    for channel_id in FORWARD_CHANNEL_IDS:
        try:
            bot.send_photo(
                channel_id,
                photo=image_url,
                caption=post_content,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error forwarding post to channel {channel_id}: {e}")

# Function to handle the /redeem command
@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    """ Redeem the code provided by the user """
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    full_name = message.from_user.full_name or "N/A"

    if not is_user_in_channels(user_id):
        bot.send_message(message.chat.id, "Please join all required channels first.")
        return

    try:
        _, code = message.text.split()
    except ValueError:
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/BotsDevZone/275",
            caption="Please provide a code to redeem."
        )
        return

    if code not in generated_codes:
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/BotsDevZone/275",
            caption="Invalid redeem code. Please try again with a valid code."
        )
        return

    if generated_codes[code] is not None:
        redeemer = generated_codes[code]
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/BotsDevZone/275",
            caption=(f"🎉 *Code Already Redeemed!*\n"
                     f"👤 *Name:* {redeemer['full_name']}\n"
                     f"📛 *Username:* {redeemer['username']}\n"
                     f"🆔 *ID:* {redeemer['user_id']}\n"
                     f"⏰ *Time:* {redeemer['time']}"),
            parse_mode="Markdown"
        )
        return

    if user_id in [data['user_id'] for data in generated_codes.values() if data]:
        bot.send_message(message.chat.id, "*You have already redeemed a code.*", parse_mode="Markdown")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    generated_codes[code] = {
        'user_id': user_id,
        'username': username,
        'full_name': full_name,
        'time': timestamp
    }

    # Determine the service from the code and select a promo link and image
    service_name = code.split('-')[0].title()

    if service_name == "Youtube":
        promo_link = random.choice(promo_links["YouTube"])  # Get a link from the predefined list for YouTube
    else:
        promo_link = random.choice(promo_links.get(service_name, ["Email: example@default.com Pass: password"]))  # Default email-pass format if service not found

    image_url = service_images.get(service_name, "https://t.me/BotsDevZone/269")  # Default to YouTube image if service not found

    # Check if the promo link is an email/pass format or a URL
    if service_name == "Youtube" or "Email:" not in promo_link:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f"🔗 Open {service_name} Premium Link", url=promo_link))
        keyboard.add(InlineKeyboardButton(text="📜 How To Leave Old Family", url="https://t.me/ModVipRM/3530"))

        bot.send_photo(
            message.chat.id,
            photo=image_url,
            caption=(f"🎉 *Code Redeemed Successfully!*\n"
                     f"👤 *Name:* {full_name}\n"
                     f"📛 *Username:* {username}\n"
                     f"🆔 *ID:* {user_id}\n"
                     f"⏰ *Time:* {timestamp}\n"
                     f"🔗 *Your {service_name} Premium link:* {promo_link}"),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        promo_text = f"🔗 *Your {service_name} Premium account:* {promo_link}"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="📜 How To Leave Old Family", url="https://t.me/ModVipRM/3530"))

        bot.send_photo(
            message.chat.id,
            photo=image_url,
            caption=(f"🎉 *Code Redeemed Successfully!*\n"
                     f"👤 *Name:* {full_name}\n"
                     f"📛 *Username:* {username}\n"
                     f"🆔 *ID:* {user_id}\n"
                     f"⏰ *Time:* {timestamp}\n"
                     f"{promo_text}"),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    proof_message = (f"🎉 *Code Redeemed Successfully!*\n"
                     f"👤 *Name:* {full_name}\n"
                     f"📛 *Username:* {username}\n"
                     f"🆔 *ID:* {user_id}\n"
                     f"⏰ *Time:* {timestamp}\n\n"
                     f"*Use the bot to get your own {service_name} Premium account!*\n"
                     f"*Join our channels for more updates and giveaways!*")

    proof_keyboard = InlineKeyboardMarkup()
    proof_keyboard.add(InlineKeyboardButton(text="🤖 Get Premium Account Now ☑️", url="https://t.me/Redeem_Ultimate_Bot"))
    proof_keyboard.add(InlineKeyboardButton(text="📜 Get Redeem Codes ☑️", url="https://t.me/addlist/wskLZdSg8K02NzVl"))

    bot.send_message(PROOF_CHANNEL_ID, proof_message, reply_markup=proof_keyboard, parse_mode="Markdown")

    # Forward the proof message to the owner
    try:
        bot.send_message(OWNER_USER_ID, proof_message, reply_markup=proof_keyboard, parse_mode="Markdown")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error sending message to owner: {e}")
        
# Send command handler to broadcast messages
@bot.message_handler(commands=['send'])
def ask_broadcast_message(message):
    if message.from_user.id != OWNER_USER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    msg = bot.reply_to(message, "*Please Enter A Message To Broadcast To Users*", parse_mode="Markdown")
    bot.register_next_step_handler(msg, broadcast_message)

def broadcast_message(message):
    if message.from_user.id != OWNER_USER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    broadcast_text = f"*📢 [ Broadcast From Owner ] 📢*\n\n{message.text}\n\n*For More Updates, [Join Now](https://t.me/ModVipRM)*"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="☑️ Join Our All Community 🥰", url="https://t.me/addlist/wskLZdSg8K02NzVl"))

    for user_id in user_ids:
        try:
            bot.send_message(user_id, broadcast_text, reply_markup=keyboard, parse_mode="Markdown", disable_web_page_preview=True)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error sending message to user {user_id}: {e}")

    # Notify the owner that the broadcast was successful
    bot.send_message(OWNER_USER_ID, "*Broadcast successful!*", parse_mode="Markdown")

# Start the bot
print("Bot is running...")
bot.polling()
