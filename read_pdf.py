import os
import argparse
import fitz  # this is pymupdf
# import PyPDF2  # deprecated
import gtts
from gtts import gTTS

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'   # to hide pygame hello msg
from pygame import mixer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF reader')
    parser.add_argument('pdf_file', type=str, help="PDF filename")
    parser.add_argument('--show', action="store_true", default=False, help="show each page as read")
    parser.add_argument('--metadata', action="store_true", default=False, help="show document metadata")
    parser.add_argument('--play', action="store_true", default=False)

    parser.add_argument('--mp3', dest="save", action="store_true", help="save MP3")
    parser.add_argument('--no-mp3', dest="save", action="store_false", help="save MP3")
    parser.set_defaults(save=True)

    parser.add_argument('--language', type=str, default="en", help="language of the PDF used by the PDF reader")

    args = parser.parse_args()
    assert args.language in gtts.lang.tts_langs().keys()

    # creating an object
    with fitz.open(args.pdf_file) as doc:
        if args.metadata:
            for k, v in doc.metadata.items():
                if v is not None:
                    print(f"{k}: {v}")
        all_text = ""
        for page in doc:
            text = page.getText()
            if args.show:
                print(text)
            all_text += text

        if args.save:
            output = os.path.basename(args.pdf_file)
            output = output.replace('.pdf', '.mp3')
            myobj = gTTS(text=all_text, lang=args.language, slow=False)
            myobj.save(output)

    if args.play:
        mixer.init()
        mixer.music.load(output)
        mixer.music.play()
