from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import paramiko

TOKEN = "8903038115:AAFQ2l_Ga-DRwBaUuhGMrB59_QspWgY5jE8"

user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_store[update.effective_user.id] = {}
    await update.message.reply_text("IP yaz:")
    context.user_data["step"] = "ip"

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    step = context.user_data.get("step")

    if step == "ip":
        user_data_store[uid]["ip"] = text
        context.user_data["step"] = "password"
        await update.message.reply_text("VPS şifresi:")
        return

    if step == "password":
        user_data_store[uid]["password"] = text

        keyboard = [
            [
                InlineKeyboardButton("Admin goş", callback_data="add"),
                InlineKeyboardButton("Admin aýyr", callback_data="delete")
            ]
        ]

        await update.message.reply_text(
            "Marzban Admin goş/aýyr",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "add":
        context.user_data["action"] = "add"
        await query.message.reply_text("Username:")
        context.user_data["step"] = "username"

    elif query.data == "delete":
        context.user_data["action"] = "delete"
        await query.message.reply_text("Username:")
        context.user_data["step"] = "delete_username"

async def ssh_connect(ip, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=ip,
        username="root",
        password=password
    )

    return ssh

async def process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    step = context.user_data.get("step")

    if step == "username":
        user_data_store[uid]["username"] = text

        keyboard = [
            [
                InlineKeyboardButton("Uly Admin", callback_data="super_yes"),
                InlineKeyboardButton("Klient", callback_data="super_no")
            ]
        ]

        await update.message.reply_text(
            "Admin tipi:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif step == "admin_password":
        user_data_store[uid]["admin_password"] = text
        context.user_data["step"] = "confirm_password"

        await update.message.reply_text("Emin misin? Şifreyi tekrar yaz:")

    elif step == "confirm_password":
        ip = user_data_store[uid]["ip"]
        vps_pass = user_data_store[uid]["password"]
        username = user_data_store[uid]["username"]
        admin_pass = user_data_store[uid]["admin_password"]
        superuser = user_data_store[uid]["superuser"]

        ssh = await ssh_connect(ip, vps_pass)

        shell = ssh.invoke_shell()

        shell.send("marzban cli admin create\n")
        shell.send(f"{username}\n")
        shell.send(f"{superuser}\n")
        shell.send(f"{admin_pass}\n")
        shell.send(f"{text}\n")
        shell.send("\n")
        shell.send("\n")

        ssh.close()

        await update.message.reply_text("Admin goşuldy ✅")

    elif step == "delete_username":
        ip = user_data_store[uid]["ip"]
        vps_pass = user_data_store[uid]["password"]

        ssh = await ssh_connect(ip, vps_pass)

        shell = ssh.invoke_shell()

        shell.send("marzban cli admin delete\n")
        shell.send(f"{text}\n")

        ssh.close()

        await update.message.reply_text("Admin aýryldy ❌")

async def super_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "super_yes":
        context.user_data["step"] = "admin_password"

        uid = query.from_user.id
        user_data_store[uid]["superuser"] = "y"

        await query.message.reply_text("Password:")

    elif query.data == "super_no":
        context.user_data["step"] = "admin_password"

        uid = query.from_user.id
        user_data_store[uid]["superuser"] = "n"

        await query.message.reply_text("Password:")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons, pattern="^(add|delete)$"))
app.add_handler(CallbackQueryHandler(super_buttons, pattern="^(super_yes|super_no)$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

app.run_polling()
