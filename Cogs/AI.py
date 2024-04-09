import discord
from discord.ext import commands
import aiohttp
import base64
import json

class AIChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not (self.bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel)):
            return

        async with aiohttp.ClientSession() as session:
            url = 'http://127.0.0.1:5000/generate-response'  
            data = {
                'channel_id': str(message.channel.id),
                'input_text': message.content
            }
            if message.attachments:
                image_data = await message.attachments[0].read()
                image_data_base64 = base64.b64encode(image_data).decode('utf-8')  # Encode image data as base64
                data['image_data'] = image_data_base64

            async with session.post(url, json=data) as resp:
                response_data = await resp.json()
                response_text = response_data.get('response')

            await message.channel.send(response_text)
def setup(bot):
    bot.add_cog(AIChatCog(bot))
