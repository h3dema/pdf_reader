import os
import re
import sys
import time
import argparse
import fitz  # this is pymupdf
# import PyPDF2  # deprecated
import gtts
from gtts import gTTS
import signal

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'   # to hide pygame hello msg
from pygame import mixer


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    mixer.music.stop()
    sys.exit(0)


def clean_line(s):
    # remove references, like [11]
    s1 = re.sub(r'[\[\d+\]]', '', s)
    return s1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF reader')
    parser.add_argument('input_file', type=str, help="PDF or txt filename")
    parser.add_argument('--show', action="store_true", default=False, help="show each page as read")
    parser.add_argument('--metadata', action="store_true", default=False, help="show document metadata")
    parser.add_argument('--play', action="store_true", default=False)

    parser.add_argument('--text', action="store_true", help="save PDF as TXT")

    parser.add_argument('--from-pdf', dest="source_pdf", action="store_true", help="convert from PDF")
    parser.add_argument('--from-txt', dest="source_pdf", action="store_false", help="convert from TXT")
    parser.set_defaults(source_pdf=True)

    parser.add_argument('--mp3', dest="save", action="store_true", help="save MP3 (default)")
    parser.add_argument('--no-mp3', dest="save", action="store_false", help="dont save MP3")
    parser.set_defaults(save=True)

    parser.add_argument('--language', type=str, default="en", help="language of the PDF used by the PDF reader")

    args = parser.parse_args()
    langs = None
    # retries = 0
    # while langs is not None or retries > 3:
    #     try:
    #         langs = gtts.lang.tts_langs()
    #     except (TypeError, RuntimeError):
    #         # sometimes need a second call to get the result (bug !!!)
    #         langs = gtts.tts.tts_langs()
    #     retries += 1
    # assert args.language in langs.keys()
    # if args.language not in langs.keys():
    #     print("Unknown language")
    #     sys.exit(0)

    # creating an object
    all_text = ""
    if args.source_pdf:
        with fitz.open(args.input_file) as doc:
            if args.metadata:
                for k, v in doc.metadata.items():
                    if v is not None:
                        print(f"{k}: {v}")
            print("Start converting...")
            for page in doc:
                text = page.getText()
                if args.show:
                    print(text)
                all_text += clean_line(text)
        # only save PDF as TXT
        if args.text:
            output = os.path.basename(args.input_file)
            output = output.replace('.pdf', '.txt')
            print("\tCreating TXT file")
            with open(output, 'w', encoding="utf-8") as f:
                f.write(all_text)
    else:
        print("Read txt file...")
        with fitz.open(args.input_file) as doc:
            for text in doc:
                all_text += clean_line(text)

    if args.save:
        output = os.path.basename(args.input_file)
        output = output.replace('.pdf', '.mp3')
        print("\tCreating MP3 file")
        myobj = gTTS(text=all_text, lang=args.language, slow=False)
        print("\tSaving MP3 file")
        myobj.save(output)
    print("Conversion finished")

    if args.play:
        mixer.init()
        mixer.music.load(output)

        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C to stop the playback')

        mixer.music.play()
        while mixer.music.get_busy() == 1:
            time.sleep(1)  # check each second if the player finished to end program
