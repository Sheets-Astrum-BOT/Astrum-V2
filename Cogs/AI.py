import re
import json
import shelve
import aiohttp
import discord
import traceback
from discord.ext import commands
from typing import Optional, Dict
import google.generativeai as genai

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
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

bot_template = [
    # {'role':'user','parts': ["Hi!"]},
    # {'role':'model','parts': ["Hello! I am a Discord bot!"]},
    # {'role':'user','parts': ["Please give short and concise answers!"]},
    # {'role':'model','parts': ["I will try my best!"]},
]

# --------------------------------------------- AI Configuration ------------------------------------------------- #

genai.configure(api_key="AIzaSyDbd7pQNZRnbG7dbmEIGLhgOrDszwQ6Ctw")

text_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=text_generation_config,
    safety_settings=safety_settings,
)

image_model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=image_generation_config,
    safety_settings=safety_settings,
)

message_history: Dict[int, genai.ChatSession] = {}
tracked_threads = []

with open("AIChannels.json", "r") as file:
    tracked_channels = json.load(file)

chatdata_path = "AIChatLogs/chatdata"

with shelve.open(chatdata_path) as file:
    if "tracked_threads" in file:
        tracked_threads = file["tracked_threads"]
    for key in file.keys():
        if key.isnumeric():
            message_history[int(key)] = text_model.start_chat(history=file[key])

# --------------------------------------------- AI Generation Functions ------------------------------------------------- #


async def generate_response_with_image_and_text(image_data, text):
    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
    prompt_parts = [
        image_parts[0],
        f"\n{text if text else 'What is this picture of?'}",
    ]

    response = image_model.generate_content(prompt_parts)
    if response._error:
        return "❌" + str(response._error)

    return response.text


async def generate_response_with_text(channel_id, message_text):
    try:
        formatted_text = format_discord_message(str(message_text))

        if channel_id not in message_history:
            message_history[channel_id] = text_model.start_chat(history=bot_template)

        response = message_history[channel_id].send_message(formatted_text)

        return response.text

    except Exception as e:
        with open("AIChatLogs/Errors.log", "a+") as errorlog:
            errorlog.write("\n##########################\n")
            errorlog.write("Message: " + str(message_text) + "\n")
            errorlog.write("Traceback:\n" + traceback.format_exc() + "\n")
            if channel_id in message_history:
                errorlog.write(
                    "History:\n" + str(message_history[channel_id].history) + "\n"
                )
            errorlog.write("Parts:\n" + str(response.parts) + "\n")
        raise


# --------------------------------------------- Discord Code ------------------------------------------------------- #


class TextGenerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_history = message_history
        self.tracked_threads = tracked_threads

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.mention_everyone:
            return
        if not (
            message.content.startswith("Astra")
            or self.bot.user.mentioned_in(message)
            or isinstance(message.channel, discord.DMChannel)
            or message.channel.id in tracked_channels
            or message.channel.id in tracked_threads
        ):
            return

        try:
            async with message.channel.typing():
                if message.attachments:
                    for attachment in message.attachments:
                        if any(
                            attachment.filename.lower().endswith(ext)
                            for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]
                        ):
                            await message.add_reaction("🎨")
                            async with aiohttp.ClientSession() as session:
                                async with session.get(attachment.url) as resp:
                                    if resp.status != 200:
                                        await message.channel.send(
                                            "Unable To Get The Image"
                                        )
                                        return
                                    image_data = await resp.read()
                                    response_text = (
                                        await generate_response_with_image_and_text(
                                            image_data, message.content
                                        )
                                    )
                                    await split_and_send_messages(
                                        message, response_text, 1700
                                    )
                                    return
                else:

                    instructions = "You are AI Companion named Astra created by SOHAM. Any message given to you is in format [user_id] - [message], just keep a note of the [user_id] u can use it to track the conversation with people and use it to ping users using <@[user_id]> but focus more on message, and reply according to [message]. You are a ery helpful and caring AI companion who loves to chat and fun fun with people"

                    query = f"{instructions} \n{message.author.name} - {message.clean_content}"

                    response_text = await generate_response_with_text(
                        message.channel.id, query
                    )

                    await split_and_send_messages(message, response_text, 1700)

                    with shelve.open("AIChatLogs/chatdata") as file:
                        file[str(message.channel.id)] = message_history[
                            message.channel.id
                        ].history

        except Exception as e:
            traceback.print_exc()
            await message.reply("An Error Occurred! Please Check The LOGS!")


    @commands.slash_command(
        name="forget", description="Forget The Message Histroy For The Channel."
    )
    async def forget(self, interaction):

        try:
            message_history.pop(interaction.channel_id, None)
            await interaction.respond("Message Histroty Forgotten!")

        except Exception as e:
            await interaction.respond(
                "An Error Occuered While Forgetting The Message History! Please Check The LOGS!"
            )

    @commands.slash_command(
        name="createchat", description="Create A New Chat With The AI."
    )
    async def createchat(self, interaction, name: str):
        try:
            thread = await interaction.channel.create_thread(
                name=name, auto_archive_duration=60
            )
            tracked_threads.append(thread.id)

            await thread.send(f"Hello <@{interaction.author.id}> \nI am Astra, Your AI Companion! Let's Chat!")
            await interaction.respond(f"Thread <#{thread.id}> Created!", ephemeral=True)

            with shelve.open("AIChatLogs/chatdata") as file:
                file["tracked_threads"] = tracked_threads

        except Exception as e:
            await interaction.respond("Error Creating The Thread! Please Check The LOGS!")


# --------------------------------------------- Helper Functions ----------------------------------------- #


async def split_and_send_messages(
    message_system: discord.Message, text: str, max_length: int
):
    messages = [text[i : i + max_length] for i in range(0, len(text), max_length)]
    for string in messages:
        message_system = await message_system.reply(string)


def format_discord_message(input_string: str) -> str:
    bracket_pattern = re.compile(r"<[^>]+>")
    cleaned_content = bracket_pattern.sub("", input_string)

    return cleaned_content


# --------------------------------------------- Run Bot ------------------------------------------------- #


def setup(bot):
    bot.add_cog(TextGenerationCog(bot))
