"""
- Converting wma audio files to mp3 and changing/adding id3 tags (Artist, title etc)
- files to convert have to be in the directory level of THIS file as "~/Artist/Album/.."
- Currently keeps wma, wav and mp3 files
TODO: Delete wma and wav when finished
"""
import librosa
# import soundfile as sf
import eyed3
import os
import re
from pydub import AudioSegment

folder = os.path.abspath("Volbeat/The Strength _ The Sound _ The Songs")
print(folder)
for song in os.listdir(folder):
    album = folder.split("/")[-1]
    artist = os.path.abspath(os.path.join(folder, os.pardir)).split("/")[-1]
    print(album)
    print(artist)
    songname = re.sub("\d\d |\.wma", "", song)
    print(songname)
    track = re.search("(\d\d)", song).group(0)
    if track.startswith("0"):
        track = track[1:]
    print(track)

    wav_file = os.path.join(folder, song.replace("wma", "wav"))
    mp3_file = os.path.join(folder, song.replace("wma", "mp3"))

    y, sr = librosa.load(os.path.join(folder, song), sr=44100, mono=False)
    librosa.output.write_wav(wav_file, y, sr=44100)

    wma_file = AudioSegment.from_file(wav_file, "wav")
    wma_file.export(mp3_file, format="mp3")

    audiofile = eyed3.load(mp3_file)
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.album_artist = artist
    audiofile.tag.title = songname
    audiofile.tag.track_num = int(track)

    audiofile.tag.save()
    #
    # print(audiofile.tag.artist)
