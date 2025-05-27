import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)
import asyncio

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
SELECTING_PRODUCT, SELECTING_PAYMENT, AWAITING_PAYMENT = range(3)

# Product list
PRODUCTS = {
    "2000": {"name": "💳 $2000_🛒$25", "price": 25},
    "3500": {"name": "💳 $3500_🛒$40", "price": 40},
    "5000": {"name": "💳 $5000_🛒$60", "price": 60},
    "7000": {"name": "💳 $7000_🛒$85", "price": 85},
    "10000": {"name": "💳 $10,000_🛒$120", "price": 120},
}



# Wallet addresses (replace with real addresses)
WALLET_ADDRESSES = {
    "trc20": "TDUWP6emBMt1wzgdKodMm6J7m2vAUueSQb",
    "erc20": "0x5bb2e4a240dc95230dbc6d3dc6a512b1dd59b035",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /start command and show welcome message with Order Now button."""
    keyboard = [[InlineKeyboardButton("Order Now", callback_data="order_now")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        """    Welcome to the USA CC Store! 😎🛒
           📱 USA CC AAAAAA+ available 😎🛒
         🔤🔤🌐  

         💳💳card levels sent below

         visa classic / premier / signature
         mastercard world / platinum
         american express
         discover


        • 𝗗𝗲𝗹𝗶𝘃𝗲𝗿𝘆

        Delivery is made here on Telegram once 
        the payment is made, you will receive : 

        • Your CC details + CCs owners' FULLZ infos 

        cvv data format: cvv number | exp | cvv | name | address | city
        | zip | state | country | phone | ssn | dob | 
        mmn | available balance

         all cc sent are 100% LIVE
         low balance cards approve for replacement
         replacement time 24h



        Click below to start your order:""",
        reply_markup=reply_markup,
    )
    return SELECTING_PRODUCT

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the product list as inline buttons."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(product["name"], callback_data=f"product_{key}")]
        for key, product in PRODUCTS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "📱 USA CC AAAAAA+ available 😎🛒\n🔤🔤🌐\nSelect the CC you want to buy:",
        reply_markup=reply_markup,
    )
    return SELECTING_PRODUCT

async def select_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle product selection and show payment options."""
    query = update.callback_query
    await query.answer()

    product_key = query.data.replace("product_", "")
    if product_key not in PRODUCTS:
        await query.message.reply_text("Invalid selection. Please try again.")
        return SELECTING_PRODUCT

    context.user_data["selected_product"] = product_key
    product = PRODUCTS[product_key]

    # Create payment method buttons
    keyboard = [
        [InlineKeyboardButton("Select Your Payment Method", callback_data="payment")],
        [
            InlineKeyboardButton("USDT TRC20", callback_data="pay_trc20"),
            InlineKeyboardButton("USDT ERC20", callback_data="pay_erc20"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"You selected: {product['name']}\nPrice: ${product['price']}\n\nPlease select your payment method:",
        reply_markup=reply_markup,
    )
    return SELECTING_PAYMENT

async def select_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle payment method selection and show wallet address with countdown."""
    query = update.callback_query
    await query.answer()

    payment_method = query.data.replace("pay_", "")
    if payment_method not in WALLET_ADDRESSES:
        await query.message.reply_text("Invalid payment method. Please try again.")
        return SELECTING_PAYMENT

    wallet_address = WALLET_ADDRESSES[payment_method]
    product_key = context.user_data.get("selected_product")
    product = PRODUCTS[product_key]

    # Send wallet address and countdown message
    await query.message.reply_text(
        f"Please send ${product['price']} to the following {payment_method.upper()} address:\n{wallet_address}\n\n"
        "You have 30 minutes to complete the payment.\nPayment will be confirmed shortly after.\n waiting for payment......"
    )

    # Simulate 1-minute wait for order confirmation (replace with payment gateway in production)
    await asyncio.sleep(1800)

    await query.message.reply_text(
        f"Your Payment isn't success ✅✅✅\n Your order is cancelled"
        
    )


    await asyncio.sleep(6989778786767566767776767)

    # Order completion message
    keyboard = [
        [InlineKeyboardButton("Exit", callback_data="exit")],
        [InlineKeyboardButton("New Order", callback_data="order_now")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"Order completed!\nDetails: {product['name']} for ${product['price']}\nPayment method: {payment_method.upper()}\n\nOrder Content:\nhttps://privnote.com/jQ6l9DIv#bonzVIXJY\n\nWhat would you like to do next?",
        reply_markup=reply_markup,
    )
    return AWAITING_PAYMENT

async def exit_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle exit button."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Thank you for using the USA CC Store! 😎")
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Run the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("8003450739:AAGOMFIDxuT43J7NnnNpFzW5zIIlO1YXJt0").build()

    # Set up conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_PRODUCT: [
                CallbackQueryHandler(show_products, pattern="^order_now$"),
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
        fallbacks=[],
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()