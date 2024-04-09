import re
import aiohttp
import discord
from discord.ext import commands
import google.generativeai as genai

genai.configure(api_key='AIzaSyDbd7pQNZRnbG7dbmEIGLhgOrDszwQ6Ctw')

text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}

image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 512,
}

safety_settings = [{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
}, {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
}, {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
}, {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
}]

text_model = genai.GenerativeModel(model_name="gemini-pro",
                                   generation_config=text_generation_config,
                                   safety_settings=safety_settings)

image_model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                    generation_config=image_generation_config,
                                    safety_settings=safety_settings)

message_history = {}

class TextGenerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_history = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not (self.bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel)):
            return

        async with message.channel.typing():
            if message.attachments:
                print("New Image Message FROM:" + str(message.author.id) + ": " + message.content)

                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        await message.add_reaction('🎨')

                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    await message.channel.send('Unable To Get The Image')
                                    return
                                image_data = await resp.read()
                                response_text = await self.generate_response_with_image_and_text(image_data, message.content)

                        await self.split_and_send_messages(message, response_text, 1700)
                        return

            elif message.content.startswith('chattie'):
                print("New Text Message FROM:" + str(message.author.id) + ": " + message.content)
                response_text = await self.generate_response_with_text(message.channel.id, message.content)
                await self.split_and_send_messages(message, response_text, 1700)
                return

            else:
                print("New Message FROM:" + str(message.author.id) + ": " + message.content)
                response_text = await self.generate_response_with_text(message.channel.id, message.content)
                await self.split_and_send_messages(message, response_text, 1700)

    async def generate_response_with_text(self, channel_id, input_text):
        cleaned_text = clean_discord_message(input_text)
        if not (channel_id in message_history):
            message_history[channel_id] = text_model.start_chat(history=[])
        response = message_history[channel_id].send_message(cleaned_text)
        return response.text

    async def generate_response_with_image_and_text(self, image_data, text):
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [
            image_parts[0], f"\n{text if text else 'What is this a picture of?'}"
        ]
        response = image_model.generate_content(prompt_parts)
        if (response._error):
            return "❌" + str(response._error)
        return response.text

    async def split_and_send_messages(self, message_system, text, max_length):
        messages = [text[i:i + max_length] for i in range(0, len(text), max_length)]

        for string in messages:
            await message_system.reply(string)

def clean_discord_message(input_string):
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

def setup(bot):
    bot.add_cog(TextGenerationCog(bot))
