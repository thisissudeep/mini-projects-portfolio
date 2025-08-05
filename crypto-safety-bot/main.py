from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
import pandas as pd
import joblib
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("TELEGRAM_USERNAME")


LENGTH, WEIGHT, COUNT, LOOPED, NEIGHBORS, INCOME = range(6)

user_data = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start command to introduce the bot and begin collecting features.
    """
    await update.message.reply_text(
        "Welcome to Crypto Fraud Detection Bot!\n"
        "I will ask you for the following transaction features one by one:\n"
        "1. Length\n"
        "2. Weight\n"
        "3. Count\n"
        "4. Looped\n"
        "5. Neighbors\n"
        "6. Income\n\n"
        "Let's get started! Please provide the Length/Position. (Sample Format: 5)"
    )
    return LENGTH


async def collect_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["length"] = int(update.message.text)
        await update.message.reply_text(
            "Got it! Now, please provide the Weight. (Sample Format: 1096.05)"
        )
        return WEIGHT
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a numeric value for Length/Position. (Sample Format: 5)"
        )
        return LENGTH


async def collect_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["weight"] = float(update.message.text)
        await update.message.reply_text(
            "Weight recorded! Next, provide the Count (Sample Format: 8)."
        )
        return COUNT
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a Float value for Weight.(Sample Format: 1096.05)"
        )
        return WEIGHT


async def collect_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["count"] = int(update.message.text)
        await update.message.reply_text(
            "Count noted! Please provide the Looped value (1 for Yes, 0 for No)."
        )
        return LOOPED
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a numeric value for Count. (Sample Format: 8)"
        )
        return COUNT


async def collect_looped(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["looped"] = int(update.message.text)
        if user_data["looped"] not in (0, 1):
            raise ValueError("Looped must be 0 (No) or 1 (Yes).")
        await update.message.reply_text(
            "Looped value recorded! Now, provide the number of Neighbors (Sample Format: 4)."
        )
        return NEIGHBORS
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Looped must be 0 (No) or 1 (Yes)."
        )
        return LOOPED


async def collect_neighbors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["neighbors"] = int(update.message.text)
        await update.message.reply_text(
            "Neighbors recorded! Finally, provide the Income in dollars (Sample Format: 4931)."
        )
        return INCOME
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a numeric value for Neighbors (Sample Format: 4)."
        )
        return NEIGHBORS


async def collect_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data["income"] = int(update.message.text)
        await update.message.reply_text(
            "Income recorded! Processing your data for fraud detection..."
        )

        result = predict_fraud(user_data)

        await update.message.reply_text(
            f"Analysis Complete!\n\nTransaction Details:\n"
            f"Length: {user_data['length']}\n"
            f"Weight: {user_data['weight']}\n"
            f"Count: {user_data['count']}\n"
            f"Looped: {user_data['looped']}\n"
            f"Neighbors: {user_data['neighbors']}\n"
            f"Income: {user_data['income']}\n\n"
            f"Prediction: {result}"
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a dollar value for Income (Sample Format: 4931.63) ."
        )
        return INCOME


def predict_fraud(raw_features: dict) -> str:

    print("Raw Transaction Format:\n", raw_features)

    df_features = pd.DataFrame([raw_features])
    print("DF Transaction Format:\n", df_features)

    scaler = joblib.load("scaler.pkl")
    scaled_features = scaler.transform(df_features)
    scaled_features = pd.DataFrame(scaled_features, columns=df_features.columns)
    print("Standardized Data Format:\n", scaled_features)

    model = joblib.load("model.pkl")
    prediction = model.predict(scaled_features)

    if prediction[0] == 1:
        return "Fraudulent Transaction"
    else:
        return "Transaction appears legitimate"


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancel the conversation.
    """
    await update.message.reply_text(
        "Transaction analysis cancelled. Feel free to start again!"
    )
    return ConversationHandler.END


if __name__ == "__main__":
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_length)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_weight)],
            COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_count)],
            LOOPED: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_looped)],
            NEIGHBORS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, collect_neighbors)
            ],
            INCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_income)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Polling...")
    app.run_polling()
