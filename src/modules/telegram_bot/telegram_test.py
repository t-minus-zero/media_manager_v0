from telegram import Bot
import os
import asyncio

# Replace 'YOUR_BOT_TOKEN' with the token you got from @BotFather
bot_token = ''

# Replace with the actual chat ID (e.g., your user ID or group chat ID)
chat_id = ''

# Initialize the bot
bot = Bot(token=bot_token)

# Async function to send image file
async def send_image(image_path):
    if os.path.exists(image_path):
        # Await the send_document method because it is asynchronous
        await bot.send_document(chat_id=chat_id, document=open(image_path, 'rb'))
        print(f"Image {image_path} sent successfully!")
    else:
        print(f"File {image_path} does not exist!")

# Asynchronous function to send images from a list of string paths (URLs)
async def send_images_from_urls(image_urls):
    # Convert the list of string paths to actual paths and start sending images
    tasks = [send_image(image_url) for image_url in image_urls]
    await asyncio.gather(*tasks)