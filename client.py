import asyncio
import json
import random
import re
print("loading models...")

from TTS.api import TTS
ttscoqui = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)

import websockets
from NBSapi import NBSapi
from audioplayer import AudioPlayer
import os

configFile = open("config.json")
config = json.load(configFile)
configFile.close()

port = str(config['port']) #PORT NUMBER FOR WEBSOCKET
rate = config['sapirate'] #SAPI5 TTS SPEECH RATE, -10 to 10

tts = NBSapi()
tts.SetRate(rate)


# YOU CAN DOWNLOAD MORE MICROSOFT SAPI TTS VOICES FROM YOUR COMPUTER SETTINGS
male = []
female = []

for index, voice in enumerate(tts.GetVoices()):
    if "Microsoft" in voice['Name'] and "Mary" not in voice['Name'] and "Mike" not in voice['Name']:
        if "Female" in voice['Gender']:
            female.append(index)
        else:
            male.append(index)
                 
defaultvoice = male[0]

api_calls = 0
audio_time = 0

AP = None
file_swap = 0

async def main():
    print("connecting to ws://localhost:"+port+"/Messages...")
    async with websockets.connect("ws://localhost:"+port+"/Messages") as websocket:
        print("connection established!")
        print("warming up model...")
        ttscoqui.tts_to_file("test123", speaker_wav="data/estinien.wav", language="en", file_path="temp/warmup.wav")
        os.system('cls')
        try:
            while True:
                rsp = await websocket.recv()
                data = json.loads(rsp)
                if data['Type'] == 'Say':
                    say(data)
                if data['Type'] == 'Cancel':
                    cancel()
        except KeyboardInterrupt:
            pass
        
def say(data):
    
    speaker = data['Speaker']
    payload = data['Payload']
    voice = data['Voice']
    global AP
    if AP:
        AP.stop()
    try:
        coquiSpeaker = speaker.lower()
        coquiSpeaker = re.sub(r"[^a-z]+", '', coquiSpeaker)
        global playback
        global file_swap
        ttscoqui.tts_to_file(payload, speaker_wav="data/"+coquiSpeaker+".wav", language="en", file_path="temp/temp"+str(file_swap)+".wav")
        AP = AudioPlayer("temp/temp"+str(file_swap)+".wav")
        AP.play()
        if file_swap:
            file_swap = 0
        else:
            file_swap = 1
        return
    except:
        pass
    
    if 'Name' in voice:
        tts.SetVoice(defaultvoice)
        if not speaker: 
            speaker = "Narrator"
        if voice['Name'] == 'Male':
            random.seed(speaker)
            voiceIndex = random.choice(male)
            tts.SetVoice(voiceIndex)
            print(speaker+ "(" + str(voiceIndex) + ")" + ": " + payload)
        elif voice['Name'] == 'Female':
            random.seed(speaker)
            voiceIndex = random.choice(female)
            tts.SetVoice(voiceIndex)
            print(speaker+ "(" + str(voiceIndex) + ")" + ": " + payload)
        else:
            print(speaker+ "(" + str(defaultvoice) + ")" + ": " + payload)
    
    tts.Speak(payload, 1) # SAPI
    
def cancel():
    global AP
    tts.Stop() # SAPI
    if AP:
        AP.stop()

def play_audio(file_path):
    global playback
    playback = AudioPlayer(file_path)
    playback.play()
    
asyncio.run(main())
if AP:
    AP.close()