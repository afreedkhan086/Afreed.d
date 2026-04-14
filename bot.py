import random
import time
import socket
import asyncio
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8694146346:AAFFFxc5lnEwG6k3sBqij4WGQv2Eq44i5A4"

cooldowns = {}

# 🌐 SAFE API (IP INFO)
def get_ip_info(ip):
    try:
        res = requests.get(f"964797c634a10558e51456616c1a17cfcb6763d83e07a6f9ad8644615ff645ab").json()
        if res["status"] == "success":
            return (
                f"🌍 Country: {res['country']}\n"
                f"🏙️ City: {res['city']}\n"
                f"📡 ISP: {res['isp']}"
            )
        else:
            return "❓ Unknown IP"
    except:
        return "⚠️ API Error"

# 🎭 Final result
def generate_result(ip, port, duration, info):
    success = random.choice([True, False])

    if success:
        return (
            "✅ ATTACK COMPLETED\n\n"
            f"🎯 TARGET: {ip}:{port}\n"
            f"🔥 METHOD: CHAOS\n"
            f"⏱️ DURATION: {duration}s\n\n"
            f"{info}\n\n"
            f"🕒 COMPLETED: {time.strftime('%I:%M:%S %p')}"
        )
    else:
        return (
            "❌ ATTACK FAILED\n\n"
            f"{info}\n\n"
            "Error: Simulation instability detected\n"
            "Try again."
        )

# 🤖 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚔️ START", callback_data="attack")],
        [InlineKeyboardButton("📊 STATUS", callback_data="status")]
    ]

    await update.message.reply_text(
        "🔓 AUTO MODE ACTIVE\n\n"
        "🧠 Just send IP\n"
        "⚡ Or: IP PORT TIME",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🎮 Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "attack":
        await query.message.reply_text("⚡ Send IP or IP PORT TIME")

    elif query.data == "status":
        await query.message.reply_text(
            "📊 STATUS:\n\n"
            "🟢 System Stable\n"
            "🧿 Oracle Active\n"
            "🎭 Simulation Mode"
        )

# 💬 MAIN LOGIC (AUTO DETECT)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    parts = text.split()

    # ❄️ Cooldown
    if user_id in cooldowns and time.time() - cooldowns[user_id] < 60:
        await update.message.reply_text("❄️ COOLDOWN ACTIVE... wait")
        return

    # 🧠 Defaults
    ip = None
    port = "80"
    duration = 10

    # 📥 Input logic
    if len(parts) == 1:
        ip = parts[0]

    elif len(parts) == 3:
        ip, port, duration = parts
        try:
            duration = int(duration)
        except:
            await update.message.reply_text("⚠️ Time must be number")
            return
    else:
        await update.message.reply_text("⚠️ Send: IP or IP PORT TIME")
        return

    # ✅ Validate IP
    try:
        socket.inet_aton(ip)
    except:
        await update.message.reply_text("⚠️ Invalid IP")
        return

    cooldowns[user_id] = time.time()

    # 🌐 API INFO
    info = get_ip_info(ip)

    # 🎬 Start
    msg = await update.message.reply_text(
        f"⚔️ ATTACK STARTED...\n\n🎯 {ip}:{port}\n⏳ {duration}s"
    )

    # ⏳ Countdown loop
    for remaining in range(duration, 0, -1):
        await asyncio.sleep(1)

        try:
            bar = "█" * (duration - remaining) + "░" * remaining

            await msg.edit_text(
                f"⚔️ ATTACK IN PROGRESS...\n\n"
                f"🎯 TARGET: {ip}:{port}\n"
                f"🔥 METHOD: CHAOS\n"
                f"⏳ Time Left: {remaining}s\n\n"
                f"[{bar}]"
            )
        except:
            pass

    # 🎭 Final
    result = generate_result(ip, port, duration, info)
    await msg.edit_text(result)

# 🚀 RUN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🌀 Chaos Auto Bot Running...")
app.run_polling()