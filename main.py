import logging
from telegram.ext import (
    Application,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# Enable logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states
SELECTING_PRODUCT, SELECTING_PAYMENT, AWAITING_PAYMENT = range(3)

# Placeholder functions (replace with your actual implementations)
async def select_product(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Product selected. Please choose a payment method.")
    return SELECTING_PAYMENT

async def select_payment(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Payment method selected. Proceed or exit.")
    return AWAITING_PAYMENT

async def show_products(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Showing products again.")
    return SELECTING_PRODUCT

async def exit_conversation(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Conversation ended.")
    return ConversationHandler.END

async def error_handler(update, context):
    """Handle errors and notify the user."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred. Please try again later.",
        )

def main():
    # Initialize the application with your bot token
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Define the conversation handler with per_message=True to avoid warning
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_product, pattern="^product_")],
        states={
            SELECTING_PRODUCT: [
                CallbackQueryHandler(select_product, pattern="^product_"),
            ],
            SELECTING_PAYMENT: [
                CallbackQueryHandler(select_payment, pattern="^pay_"),
            ],
            AWAITING_PAYMENT: [
                CallbackQueryHandler(show_products, pattern="^order_now$"),
                CallbackQueryHandler(exit_conversation, pattern="^exit$"),
            ],
        },
        fallbacks=[
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda update, context: context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Please use the provided buttons to proceed.",
                ),
            )
        ],
        per_message=True,  # Explicitly set to avoid PTBUserWarning
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    # Ensure webhook is disabled before starting polling
    async def disable_webhook():
        await application.bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook disabled, starting polling.")

    # Run disable_webhook and start polling
    application.run_polling(
        allowed_updates=[Update.CALLBACK_QUERY, Update.MESSAGE],
        bootstrap_retries=3,  # Retry in case of network issues
        bootstrap_callback=disable_webhook,  # Ensure webhook is disabled
    )

if __name__ == "__main__":
    main()
