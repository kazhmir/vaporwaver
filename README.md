# ＶＡＰＯＲＷＡＶＥＲ

## Description

This is a simple script that transforms songs into vaporwave. It can download a video from youtube and save it as .wav, implement live delay and change playback speed.

To understand the basic theory behind the delay, refer to [theory](#theory).

## Prerequisites

You'll need to install portaudio, pyaudio, youtube-dl and ffmpeg:

    conda install portaudio
    conda install pyaudio
    conda install -c conda-forge youtube-dl
    conda install -c conda-forge ffmpeg

Note: portaudio can't be installed through pip.

## Usage

To download a song from youtube:

    vaporwaver.ytDownload(link)

To play the song:

    vaporwaver.play(filename)

or, to play a list of matches to a term:

    vaporwaver.playMatch(term)

Refer to the function source code for more information.

## Important Varibles

    speed = 0.75

Speed multiplier, in this case 75% the original speed.

    feedback = 0.5

The feedback gain multiplier, each sample in the buffer is multiplied by this value before being fed back to the buffer.

    feedfoward = 0.3

The feedfoward gain multiplier, each sample is multiplied by this value before being added to the sound to be played.

    delay = 0.2

The amount of time (in seconds) that will be continously overlayed in the song.

## Theory <a name ="theory"></a>

[The computer records sound by measuring the eletrical signal of a microphone](https://www.youtube.com/watch?v=d_crXXbuEKE), the signal corresponds directly to the amplitude at that given time and is stored as a number. This number is referred as sample. 

The final array containing all the numbers measured by the computer can be ploted in a graph to visually reveal the sound waves recorded.

<a href="https://www.mediacollege.com/audio/images/tone-1khz.gif">![image](https://www.mediacollege.com/audio/images/tone-1khz.gif)</a>

When you overlay two frequencies, you are creating a [wave interference](https://en.wikipedia.org/wiki/Wave_interference). In a wave interference, the amplitude of each wave is added together to form the final wave.

<a href="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Interference_of_two_waves.svg/1200px-Interference_of_two_waves.svg.png">![image](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Interference_of_two_waves.svg/1200px-Interference_of_two_waves.svg.png)</a>

Each sample in a .wav file is a number corresponding the amplitude of the wave in that particular point. Finally, when you overlay the delay over the original music, you're essentially adding the value of every delay sample with the value of the original audio sample. 

The buffer holds an array with all the delay samples to be added to the original sound. The variable 'k' points to the current sample in the buffer to be overlayed. The sample is overlayed and then immediatly fed back to the buffer, overlaying with itself again.