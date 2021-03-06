import io
import re

import pafy
from gtts import gTTS
from PIL import Image

from ubot.fixes.fast_telethon import upload_file
from ubot import ldr


@ldr.add("jokes", help="Fetches the most funny jokes you've ever read.")
async def dadjoke(event):
    async with ldr.aioclient.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}) as response:
        if response.status == 200:
            dad_joke = (await response.json())["joke"]
        else:
            await event.reply(f"An error occurred: **{response.status}**")
            return

    await event.reply(dad_joke)


@ldr.add("fact", help="Fetches random facts.")
async def randomfact(event):
    async with ldr.aioclient.get("https://uselessfacts.jsph.pl/random.json", params={"language": "en"}) as response:
        if response.status == 200:
            random_fact = (await response.json())["text"].replace("`", "'")
        else:
            await event.reply(f"An error occurred: **{response.status}**")
            return

    await event.reply(random_fact)


@ldr.add("fakeword", help="Fetches random fake words.")
async def fakeword(event):
    async with ldr.aioclient.get("https://www.thisworddoesnotexist.com/api/random_word.json") as response:
        if response.status == 200:
            random_word_json = (await response.json())["word"]
            word = random_word_json["word"]
            definition = random_word_json["definition"]
            example = random_word_json["example"]
        else:
            await event.reply(f"An error occurred: **{response.status}**")
            return

    await event.reply(f"**{word}:** __{definition}__\n\n**Example:** __{example}__")


@ldr.add("tts", help="Text to speech.")
async def text_to_speech(event):
    text, reply = await event.get_text(return_msg=True)

    if not text:
        await event.reply("Give me text or reply to text to use TTS.")
        return

    tts_bytesio = io.BytesIO()
    tts_bytesio.name = "tts.mp3"

    try:
        tts = gTTS(text)
        tts.write_to_fp(tts_bytesio)
        tts_bytesio.seek(0)
    except AssertionError:
        await event.reply('The text is empty.')
        return
    except RuntimeError:
        await event.reply('Error loading the languages dictionary.')
        return

    await event.client.send_file(event.chat, file=tts_bytesio, voice_note=True, reply_to=reply)


@ldr.add("ip", help="IP lookup.")
async def ip_lookup(event):
    ip = await event.get_text()

    if not ip:
        await event.reply("Provide an IP!")
        return

    async with ldr.aioclient.get(f"http://ip-api.com/json/{ip}") as response:
        if response.status == 200:
            lookup_json = await response.json()
        else:
            await event.reply(f"An error occurred when looking for **{ip}**: **{response.status}**")
            return

    fixed_lookup = {}

    for key, value in lookup_json.items():
        special = {"lat": "Latitude", "lon": "Longitude", "isp": "ISP", "as": "AS", "asname": "AS name"}
        if key in special:
            fixed_lookup[special[key]] = str(value)
            continue

        key = re.sub(r"([a-z])([A-Z])", r"\g<1> \g<2>", key)
        key = key.capitalize()

        if not value:
            value = "None"

        fixed_lookup[key] = str(value)

    text = ""

    for key, value in fixed_lookup.items():
        text = text + f"**{key}:** {value}\n"

    await event.reply(text)


@ldr.add("corona", help="Fetches Coronavirus stats, takes an optional country name as an argument.")
async def corona(event):
    if event.args:
        async with ldr.aioclient.get(f"https://disease.sh/v3/covid-19/countries/{event.args}", headers={"accept": "application/json"}) as response:
            if response.status == 200:
                response = await response.json()
            else:
                await event.reply(f"An error occurred, response code: **{response.status}**")
                return

        response_list = [
            f"Corona stats for **{response['country']}**\n",
            f"**Cases**\n   {response['cases']} total\n   {response['todayCases']} today\n   {response['active']} active\n   {round(response['cases'] / response['population'] * 100, 2)}% of population",
            f"**Tests**\n   {response['tests']} total\n   {round(response['cases'] / response['tests'] * 100, 2) if response['tests'] != 0 else 0.0}% positive\n   {round(response['tests'] / response['population'] * 100, 2)}% of population",
            f"**Deaths**\n   {response['deaths']} total\n   {response['todayDeaths']} today\n   {round(response['deaths'] / response['cases'] * 100, 2) if response['cases'] != 0 else 0.0}% of cases\n   {round(response['deaths'] / response['population'] * 100, 2)}% of population",
            f"**Recoveries**\n   {response['recovered']} total"
        ]

        await event.reply("\n".join(response_list))
    else:
        async with ldr.aioclient.get("https://disease.sh/v3/covid-19/all", headers={"accept": "application/json"}) as response:
            if response.status == 200:
                response = await response.json()
            else:
                await event.reply(f"`An error occurred, response code: `**{response.status}**")
                return

        response_list = [
            "Global Corona stats\n",
            f"**Cases**\n   {response['cases']} total\n   {response['todayCases']} today\n   {response['active']} active\n   {round(response['cases'] / response['population'] * 100, 2)}% of population",
            f"**Tests**\n   {response['tests']} total\n   {round(response['cases'] / response['tests'] * 100, 2) if response['tests'] != 0 else 0.0}% positive\n   {round(response['tests'] / response['population'] * 100, 2)}% of population",
            f"**Deaths**\n   {response['deaths']} total\n   {response['todayDeaths']} today\n   {round(response['deaths'] / response['cases'] * 100, 2) if response['cases'] != 0 else 0.0}% of cases\n   {round(response['deaths'] / response['population'] * 100, 2)}% of population",
            f"**Recoveries**\n   {response['recovered']} total"
        ]

        await event.reply("\n".join(response_list))


@ldr.add_inline_article("corona", default="corona")
async def corona_inline(event):
    if event.args:
        async with ldr.aioclient.get(f"https://disease.sh/v3/covid-19/countries/{event.args}", headers={"accept": "application/json"}) as response:
            if response.status == 200:
                response = await response.json()
            else:
                return

        response_list = [
            f"Corona stats for **{response['country']}**\n",
            f"**Cases**\n   {response['cases']} total\n   {response['todayCases']} today\n   {response['active']} active\n   {round(response['cases'] / response['population'] * 100, 2)}% of population",
            f"**Tests**\n   {response['tests']} total\n   {round(response['cases'] / response['tests'] * 100, 2) if response['tests'] != 0 else 0.0}% positive\n   {round(response['tests'] / response['population'] * 100, 2)}% of population",
            f"**Deaths**\n   {response['deaths']} total\n   {response['todayDeaths']} today\n   {round(response['deaths'] / response['cases'] * 100, 2) if response['cases'] != 0 else 0.0}% of cases\n   {round(response['deaths'] / response['population'] * 100, 2)}% of population",
            f"**Recoveries**\n   {response['recovered']} total"
        ]

        return [{"title": "Corona Stats", "description": response['country'], "text": "\n".join(response_list)}]
    else:
        async with ldr.aioclient.get("https://disease.sh/v3/covid-19/all", headers={"accept": "application/json"}) as response:
            if response.status == 200:
                response = await response.json()
            else:
                return

        response_list = [
            "Global Corona stats\n",
            f"**Cases**\n   {response['cases']} total\n   {response['todayCases']} today\n   {response['active']} active\n   {round(response['cases'] / response['population'] * 100, 2)}% of population",
            f"**Tests**\n   {response['tests']} total\n   {round(response['cases'] / response['tests'] * 100, 2) if response['tests'] != 0 else 0.0}% positive\n   {round(response['tests'] / response['population'] * 100, 2)}% of population",
            f"**Deaths**\n   {response['deaths']} total\n   {response['todayDeaths']} today\n   {round(response['deaths'] / response['cases'] * 100, 2) if response['cases'] != 0 else 0.0}% of cases\n   {round(response['deaths'] / response['population'] * 100, 2)}% of population",
            f"**Recoveries**\n   {response['recovered']} total"
        ]

        return [{"title": "Corona Stats", "description": "Global", "text": "\n".join(response_list)}]


@ldr.add("yt", userlocking=True)
async def youtube_cmd(event):
    video = pafy.new(event.args)
    video_stream = video.getbest(preftype="mp4")

    try:
        await event.reply(file=video_stream.url)
    except:
        await event.reply(f"Download failed, the video was probably over 20MB: [URL]({video_stream.url})")


@ldr.add("yta", userlocking=True)
async def youtube_audio_cmd(event):
    video = pafy.new(event.args)
    audio_stream = video.getbestaudio(preftype="m4a")

    try:
        async with ldr.aioclient.get(audio_stream.url) as response:
            if response.status == 200:
                if int(response.headers["content-length"]) >= 20000000:
                    await event.reply("File Too big!!\nCancelling...")
                    return

                audio_data = io.BytesIO(await response.read())
                audio_data.name = "audio.m4a"
            else:
                raise Exception

        file_handle = await upload_file(event.client, audio_data)
        await event.reply(file=file_handle)
    except:
        await event.reply(f"Download failed: [URL]({audio_stream.url})")
