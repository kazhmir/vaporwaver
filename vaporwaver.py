# conda install portaudio
# conda install pyaudio
import pyaudio
from wave import open as openWav
from struct import pack, unpack
from os import path, listdir
# conda install -c conda-forge youtube-dl
# conda install -c conda-forge ffmpeg
import youtube_dl
from re import search

root = path.dirname(__file__)
directory = root + r"\musics"

def clamp(n):
    return max(min(+32767, n), -32767)

def playMatch(term, speed = 0.75, feedback = 0.5, feedfoward = 0.3, delay = 0.2):
    output = []
    for item in listdir(directory):
        if search(term.lower(), item.lower()):
            output.append(item)
    for item in output:
        play(item, speed=speed, feedback=feedback, feedfoward=feedfoward, delay=delay)

def ytDownload(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': directory + '/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def play(filename, speed = 0.75, feedback = 0.5, feedfoward = 0.3, delay = 0.2):
    pa = pyaudio.PyAudio()

    feedbackGain = feedback
    feedfowardGain = feedfoward
    directpathGain = 0.65

    filepath = r"%s/%s" % (directory, filename)
    file = openWav(filepath, "rb")
    samplerate = int(file.getframerate() * speed)
    delaysamples = int(samplerate * delay)      # the amount of samples in the specified delay time
    buffer0 = [0 for x in range(delaysamples)]  # channel 0
    buffer1 = [0 for x in range(delaysamples)]  # channel 1

    headphones = pa.open(format=pa.get_format_from_width(file.getsampwidth()), 
                channels = file.getnchannels(), 
                rate = samplerate, 
                output = True, 
                input_device_index = pa.get_default_output_device_info()["index"])

    data = file.readframes(1)                # gets the data in bytes type
    k = 0                                    # buffer index

    while data:
        unpackedata = unpack("hh", data)       # unpacked stereo input
        c0 = unpackedata[0]                           # unpacked channel 0
        c1 = unpackedata[1]                           # unpacked channel 1
        
        unout0 = int(directpathGain * c0 + feedfowardGain * buffer0[k])       # unpacked output of channel 0
        unout1 = int(directpathGain * c1 + feedfowardGain * buffer1[k])       # unpacked output of channel 1

        buffer0[k] = c0 + buffer0[k] * feedbackGain            # update buffer
        buffer1[k] = c1 + buffer1[k] * feedbackGain

        k += 1

        if k == delaysamples:           # reached buffer end (end of delay chunk)
            k = 0                       # resets

        packed_output = pack("hh", clamp(unout0), clamp(unout1))
        headphones.write(packed_output)
        data = file.readframes(1)

    headphones.stop_stream()
    headphones.close()
    pa.terminate()