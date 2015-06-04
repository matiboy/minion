# Pocketsphinx post processor

| Input type                  | Output type |
|-----------------------------|-------------|
| Audio data (wav, 1 channel) | Text        |

## Category

Speech To Text

## Description

[Pocketsphinx](http://cmusphinx.sourceforge.net/) is one of the choices of speech to text post processors. Its main advantage is that the speech to text process is handled locally on the same device. This means that it is very fast compared to the Google API or API.ai processors.

It expects data passed from the sensor (or the previous preprocessor) to be raw wav, one channel audio data. It writes the data to a temporary file and passes the file to the shell command. The temporary file will be deleted automatically upon completion, unless *delete_audio_file* is set to `false` in the [configuration](#configuration)

The main problem encountered with this post processor is that it is not as accurate as the above two. However if a custom, not too complex language model is provided, Pocketsphinx becomes much better. Therefore, you may want to use [this tool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) to create your own language model and dictionary.

At this moment, the Pocketsphinx post processor calls the shell corresponding shell script, although we are looking into the [Python package by Dmitry Prazdnichnov](https://github.com/bambocher/pocketsphinx-python)

## Installation

Please refer to [Pocketsphinx's official installation tutorial](http://cmusphinx.sourceforge.net/wiki/tutorialpocketsphinx) for installation details.

The post processor itself does not have any other requirements

## Configuration

- **delete_audio_file**  
Delete the temporary audio file created with the passed audio data. Defaults to `true`. Use mainly for debugging
