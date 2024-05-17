import aiohttp
import discord
import requests
from discord import option
from deep_translator import *
from discord.ext import commands

LANGUAGES = {
            "af": "afrikaans",
            "sq": "albanian",
            "am": "amharic",
            "ar": "arabic",
            "hy": "armenian",
            "az": "azerbaijani",
            "eu": "basque",
            "be": "belarusian",
            "bn": "bengali",
            "bs": "bosnian",
            "bg": "bulgarian",
            "ca": "catalan",
            "ceb": "cebuano",
            "ny": "chichewa",
            "zh-cn": "chinese (simplified)",
            "zh-tw": "chinese (traditional)",
            "co": "corsican",
            "hr": "croatian",
            "cs": "czech",
            "da": "danish",
            "nl": "dutch",
            "en": "english",
            "eo": "esperanto",
            "et": "estonian",
            "tl": "filipino",
            "fi": "finnish",
            "fr": "french",
            "fy": "frisian",
            "gl": "galician",
            "ka": "georgian",
            "de": "german",
            "el": "greek",
            "gu": "gujarati",
            "ht": "haitian creole",
            "ha": "hausa",
            "haw": "hawaiian",
            "iw": "hebrew",
            "he": "hebrew",
            "hi": "hindi",
            "hmn": "hmong",
            "hu": "hungarian",
            "is": "icelandic",
            "ig": "igbo",
            "id": "indonesian",
            "ga": "irish",
            "it": "italian",
            "ja": "japanese",
            "jw": "javanese",
            "kn": "kannada",
            "kk": "kazakh",
            "km": "khmer",
            "ko": "korean",
            "ku": "kurdish (kurmanji)",
            "ky": "kyrgyz",
            "lo": "lao",
            "la": "latin",
            "lv": "latvian",
            "lt": "lithuanian",
            "lb": "luxembourgish",
            "mk": "macedonian",
            "mg": "malagasy",
            "ms": "malay",
            "ml": "malayalam",
            "mt": "maltese",
            "mi": "maori",
            "mr": "marathi",
            "mn": "mongolian",
            "my": "myanmar (burmese)",
            "ne": "nepali",
            "no": "norwegian",
            "or": "odia",
            "ps": "pashto",
            "fa": "persian",
            "pl": "polish",
            "pt": "portuguese",
            "pa": "punjabi",
            "ro": "romanian",
            "ru": "russian",
            "sm": "samoan",
            "gd": "scots gaelic",
            "sr": "serbian",
            "st": "sesotho",
            "sn": "shona",
            "sd": "sindhi",
            "si": "sinhala",
            "sk": "slovak",
            "sl": "slovenian",
            "so": "somali",
            "es": "spanish",
            "su": "sundanese",
            "sw": "swahili",
            "sv": "swedish",
            "tg": "tajik",
            "ta": "tamil",
            "te": "telugu",
            "th": "thai",
            "tr": "turkish",
            "uk": "ukrainian",
            "ur": "urdu",
            "ug": "uyghur",
            "uz": "uzbek",
            "vi": "vietnamese",
            "cy": "welsh",
            "xh": "xhosa",
            "yi": "yiddish",
            "yo": "yoruba",
            "zu": "zulu",
        }

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="translate", description="Translate Text To Other Language"
    )
    async def translate(self, ctx, lang, *, text):

        translated = GoogleTranslator(source="auto", target=lang).translate(text)

        embed = discord.Embed(
            title="Translated Text",
            color=discord.Color.random(),
        )

        embed.add_field(name="Original Text", value=text, inline=False)
        embed.add_field(name="Translated Text", value=translated, inline=False)

        await ctx.respond(embed=embed, view=LanguageList())

    @commands.slash_command(name="detect", description="Detect Language Of Text")
    async def detect(self, ctx, *, text):

        lang = single_detection(text, api_key="4b39db11245e53a126a7b62d2de3fed6")

        lang = LANGUAGES[lang].capitalize()

        embed = discord.Embed(
            title="Detected Language", description=lang, color=discord.Color.random()
        )

        await ctx.respond(embed=embed)

def create_language_embed():

        language_list = list(LANGUAGES.items())

        description = ""
        for i, (code, name) in enumerate(language_list, start=1):
            description += f"`{code}` - {name.capitalize()}\n"

        embed = discord.Embed(title="Languages", description=description, color=discord.Color.blurple())
        
        return embed

class LanguageList(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Language List",emoji="🌐", style=discord.ButtonStyle.secondary)
    async def language_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        
        await interaction.response.send_message(embed=create_language_embed(), ephemeral=True)

def setup(bot):
    bot.add_cog(Translate(bot))
