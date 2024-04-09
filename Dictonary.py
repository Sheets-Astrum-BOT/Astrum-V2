import re
import requests

def get_meaning(word):
    url = "https://dictionary-by-api-ninjas.p.rapidapi.com/v1/dictionary"
    headers = {
        "X-RapidAPI-Key": "1cd68ddeb1mshb590a11eaf553edp111b0bjsn640bd1591c6c",
        "X-RapidAPI-Host": "dictionary-by-api-ninjas.p.rapidapi.com"
    }
    querystring = {"word": word}
    response = requests.get(url, headers=headers, params=querystring)
    meaning = response.json()
    if "definition" in meaning:
        definitions = re.split(r"\d+\. ", meaning["definition"])
        formatted_definitions = [definition.strip() for definition in definitions if definition.strip()]
        return formatted_definitions
    else:
        return ["Definition Not Found."]

