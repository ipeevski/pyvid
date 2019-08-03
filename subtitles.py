import speech_recognition as sr
import subprocess
import os.path
import wave
import math
import audioop
import progressbar
import sys

import pysrt
import six

from audio_chunks import AudioChunks

# video processing: https://github.com/Zulko/moviepy

PATH = sys.argv[1]
AUDIO_RATE = "41000"

def percentile(arr, percent):
    """
    Calculate the given percentile of arr.
    """
    arr = sorted(arr)
    index = (len(arr) - 1) * percent
    floor = math.floor(index)
    ceil = math.ceil(index)
    if floor == ceil:
        return arr[int(index)]
    low_value = arr[int(floor)] * (ceil - index)
    high_value = arr[int(ceil)] * (index - floor)
    return low_value + high_value

def find_speech_regions(filename, frame_width=4096, min_region_size=0.5, max_region_size=10):
    """
    Perform voice activity detection on a given audio file.
    """
    reader = wave.open(filename)
    sample_width = reader.getsampwidth()
    rate = reader.getframerate()
    n_channels = reader.getnchannels()
    chunk_duration = float(frame_width) / rate

    n_chunks = int(math.ceil(reader.getnframes()*1.0 / frame_width))
    energies = []

    for _ in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold = percentile(energies, 0.2)

    elapsed_time = 0

    regions = []
    region_start = None

    for energy in energies:
        is_silence = energy <= threshold
        max_exceeded = region_start and elapsed_time - region_start >= max_region_size

        if (max_exceeded or is_silence) and region_start:
            if elapsed_time - region_start >= min_region_size:
                regions.append((region_start, elapsed_time))
                region_start = None

        elif (not region_start) and (not is_silence):
            region_start = elapsed_time
        elapsed_time += chunk_duration
    return regions

def srt_formatter(subtitles, padding_before=0, padding_after=0):
    """
    Serialize a list of subtitles according to the SRT format, with optional time padding.
    """
    sub_rip_file = pysrt.SubRipFile()
    for i, ((start, end), text) in enumerate(subtitles, start=1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = six.text_type(text)
        item.start.seconds = max(0, start - padding_before)
        item.end.seconds = end + padding_after
        sub_rip_file.append(item)
    return '\n'.join(six.text_type(item) for item in sub_rip_file)

def generate_subtitles(source_path):

#        concurrency=DEFAULT_CONCURRENCY,
#        src_language=DEFAULT_SRC_LANGUAGE,
#        dst_language=DEFAULT_DST_LANGUAGE,
#        subtitle_file_format=DEFAULT_SUBTITLE_FORMAT,
#        api_key=None,
    """
    Given an input audio/video file, generate subtitles in the specified language and format.
    """

    regions = find_speech_regions(source_path)
    converter = AudioChunks(source_path)
    recognizer = sr.Recognizer()

    # Adjust for noise
    with sr.WavFile(source_path) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.25)

    # pool = multiprocessing.Pool(concurrency)
    # converter = FLACConverter(source_path=audio_filename)
    # recognizer = SpeechRecognizer(language=src_language, rate=audio_rate, api_key=GOOGLE_SPEECH_API_KEY)

    transcripts = []
    if regions:
        try:
            widgets = [
                "Converting speech regions to text: ",
                progressbar.Counter(), ' of ' + str(len(regions)), ' (',
                progressbar.Percentage(), ') ',
                progressbar.Bar(), ' ',
                progressbar.ETA()
            ]
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=len(regions)).start()
            i = 0
            for region in regions[:]:
                i += 1
                extracted_region_file = converter(region)

                with sr.WavFile(extracted_region_file.name) as source:   # use "test.wav" as the audio source
                    recognizer.adjust_for_ambient_noise(source, duration=0.25)
                    audio = recognizer.record(source)

                try:
                    # recognize speech using Google Speech Recognition
                    transcript = recognizer.recognize_google(audio_data = audio)
                    transcripts.append(transcript)

                    pbar.update(i) # transcript
                except LookupError:
                    # "Error: Could not understand audio"
                    pbar.update(i)
                    regions.remove(region)
                except sr.UnknownValueError:
                    # "Error: Unknown Value Error"
                    pbar.update(i)
                    regions.remove(region)

                extracted_region_file.close()
                os.unlink(extracted_region_file.name)

            pbar.finish()

            # if src_language.split("-")[0] != dst_language.split("-")[0]:
            #     if api_key:
            #         google_translate_api_key = api_key
            #         translator = Translator(dst_language, google_translate_api_key,
            #                                 dst=dst_language,
            #                                 src=src_language)
            #         prompt = "Translating from {0} to {1}: ".format(src_language, dst_language)
            #         widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
            #         pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()
            #         translated_transcripts = []
            #         for i, transcript in enumerate(pool.imap(translator, transcripts)):
            #             translated_transcripts.append(transcript)
            #             pbar.update(i)
            #         pbar.finish()
            #         transcripts = translated_transcripts
            #     else:
            #         print(
            #             "Error: Subtitle translation requires specified Google Translate API key. "
            #             "See --help for further information."
            #         )
            #         return 1

        except KeyboardInterrupt:
            pbar.finish()
            # pool.terminate()
            # pool.join()
            print("Cancelling transcription")
            raise

    timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]
    formatted_subtitles = srt_formatter(timed_subtitles)

    base = os.path.splitext(source_path)[0]
    dest = "{base}.srt".format(base=base)

    with open(dest, 'wb') as output_file:
        print('Writing subtitles to', dest)
        output_file.write(formatted_subtitles.encode("utf-8"))

    return dest

def process(file):
    base = os.path.splitext(file)[0]
    if os.path.exists(base + '.srt'):
        return

    if not os.path.exists(base + '.wav'):
        command = "bin\\ffmpeg -i " + file + " -ab 160k -ac 2 -ar " + AUDIO_RATE + " -vn " + base + ".wav"
        FNULL = open(os.devnull, 'w')
        subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

    generate_subtitles(base + '.wav')
    os.remove(base + '.wav')

# Shell / ffmpeg

if os.path.isdir(PATH):
    for filename in os.listdir(PATH):
        if os.path.isfile(PATH + '\\' + filename):
            ext = os.path.splitext(filename)[1][1:]
            if ext in ['mpg', 'mp4', 'mkv', 'avi', 'mov', 'ts']:
                print('Processing file', filename)
                process(PATH + '\\' + filename)
else:
    process(PATH)
