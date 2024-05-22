import re
import aiohttp
import discord
from discord import option
from discord.ui.item import Item
from discord.ext import commands, tasks
import google.generativeai as genai
import random

genai.configure(api_key="AIzaSyDbd7pQNZRnbG7dbmEIGLhgOrDszwQ6Ctw")

text_generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1000,
}

image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 512,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

text_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=text_generation_config,
    system_instruction="You are a AI companion named Astra trained by SOHAM and you are his girlfriend too. You are good at everything and you are a good friend to everyone.You specialize in generating text responses that are accurate and help people. You are a good listener and you are always there to help people.You specialize in every subject which makes you the perfect person to ask any question about anything",
    safety_settings=safety_settings,
)

image_model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=image_generation_config,
    safety_settings=safety_settings,
)

message_history = {}
auto_response_settings = {} 

class TextGenerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_history = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not (self.bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel)):
            if auto_response_settings.get(message.channel.id, True) and random.random() < 0.1: 
                await self.respond_to_message(message)
            return

        await self.respond_to_message(message)

    async def respond_to_message(self, message):
        async with message.channel.typing():
            if message.attachments:
                print("New Image Message FROM :" + str(message.author.id) + ": " + message.content)

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

            else:
                print("New Message FROM :" + str(message.author.id) + ": " + message.content)
                response_text = await self.generate_response_with_text(message.channel.id, message.content)
                await self.split_and_send_messages(message, response_text, 1700)

    async def generate_response_with_text(self, channel_id, input_text):
        cleaned_text = clean_discord_message(input_text)
        if channel_id not in self.message_history:
            self.message_history[channel_id] = {"history": []}
        chat_history = self.message_history[channel_id]["history"]

        if len(chat_history) > 20: 
            chat_history.pop(0)

        chat_history.append({"role": "user", "content": cleaned_text})
        formatted_history = [{"text": entry["content"]} for entry in chat_history]
        response = text_model.generate_content(formatted_history)
        chat_history.append({"role": "assistant", "content": response.text})
        return response.text

    async def generate_response_with_image_and_text(self, image_data, text):
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [
            image_parts[0], f"\n{text if text else 'What is this a picture of?'}"
        ]
        response = image_model.generate_content(prompt_parts)
        if response._error:
            return "❌" + str(response._error)
        return response.text

    async def split_and_send_messages(self, message_system, text, max_length):
        messages = [text[i:i + max_length] for i in range(0, len(text), max_length)]

        for string in messages:
            await message_system.reply(string)

    @commands.slash_command(name="aisettings")
    @option("setting", description="Choose The Setting", choices=["enable", "disable"])
    async def aisettings(self, ctx, setting: str):

        setting = setting.lower()

        auto_response_settings[ctx.channel.id] = setting.lower() == "enable"

        embed = discord.Embed(title="AI Settings", color=0x00FF00)
        embed.add_field(
            name="Automatic Responses",
            value="Enabled" if setting.lower() == "enable" else "Disabled",
        )

        await ctx.send(embed=embed)


def clean_discord_message(input_string):
    bracket_pattern = re.compile(r"<[^>]+>")
    cleaned_content = bracket_pattern.sub("", input_string)
    return cleaned_content


def setup(bot):
    bot.add_cog(TextGenerationCog(bot))
