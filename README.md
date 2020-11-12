# pdf_reader

This project contains a python module that extracts pages from PDF and reads them aloud.


## Dependencies

```
pip install -r requirements.py
```


## Program

```
usage: read_pdf.py [-h] [--show] [--metadata] [--play] [--mp3] [--no-mp3]
                   [--language LANGUAGE]
                   pdf_file

PDF reader

positional arguments:
  pdf_file             PDF filename

optional arguments:
  -h, --help           show this help message and exit
  --show               show each page as read
  --metadata           show document metadata
  --play
  --mp3                save MP3 (default)
  --no-mp3             dont save MP3
  --language LANGUAGE  language of the PDF used by the PDF reader
```
