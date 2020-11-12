import time
import os
import argparse
import fitz  # this is pymupdf
# import PyPDF2  # deprecated
import gtts
from gtts import gTTS
import signal
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'   # to hide pygame hello msg
from pygame import mixer


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    mixer.music.stop()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF reader')
    parser.add_argument('pdf_file', type=str, help="PDF filename")
    parser.add_argument('--show', action="store_true", default=False, help="show each page as read")
    parser.add_argument('--metadata', action="store_true", default=False, help="show document metadata")
    parser.add_argument('--play', action="store_true", default=False)

    parser.add_argument('--mp3', dest="save", action="store_true", help="save MP3 (default)")
    parser.add_argument('--no-mp3', dest="save", action="store_false", help="dont save MP3")
    parser.set_defaults(save=True)

    parser.add_argument('--language', type=str, default="en", help="language of the PDF used by the PDF reader")

    args = parser.parse_args()
    langs = gtts.lang.tts_langs()
    assert args.language in langs.keys()

    # creating an object
    with fitz.open(args.pdf_file) as doc:
        if args.metadata:
            for k, v in doc.metadata.items():
                if v is not None:
                    print(f"{k}: {v}")
        all_text = ""
        print("Start converting...")
        for page in doc:
            text = page.getText()
            if args.show:
                print(text)
            all_text += text

        if args.save:
            output = os.path.basename(args.pdf_file)
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
