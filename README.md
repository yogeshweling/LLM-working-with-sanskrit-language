# Can a Language Model Apply Sanskrit Pronunciation Rules?


A practical experiment in using a language model to build a small tool for Sanskrit text, tested on the Lalita Sahasranama. Claude wrote the programs in this repo; plain scripts, not the model, apply the rules every time.

## Who this is for

This is for Sanskrit scholars, teachers, learners and readers interested in the language, as well as people researching or building language models and their applications. Sanskrit readers can examine the text and marking conventions; AI readers can examine how instructions became an executable tool and where errors or uncertainty entered the process. I asked Claude to turn an old-font PDF of the Lalita Sahasranama into color-marked Devanagari using three pronunciation-related rules I defined. The model recognized the text well enough to decode a legacy font that extracted as Latin-looking gibberish, then wrote the programs that decoded and marked the text.


## Why I ran this experiment
I wanted to explore whether a language model could help make language-specific rules visible and usable. Many languages carry information through pronunciation, spelling, grammatical structure and other conventions that a short translation or paraphrase may not capture. My working belief was that explicit rules, examples and tools could help make some of those features accessible. I wanted to investigate how that would work in practice.


Read the full write-up: **[In Process]**

## 1. What this demonstrates

**The problem.** Sanskrit has language-specific rules in which pronunciation depends on where certain letters fall: an aspirated consonant carries extra breath, and conjuncts (two or more consonants joined) change how the syllable before them is read. A reader who does not know these rules can easily mispronounce the script. This project marks those places in the text with colors and underlining, so the script is easier to pronounce.

**The question.** Could a model interpret the rules I supplied, translate them into a useful transformation, and preserve the original text? Where would it need correction? More broadly, how does a text-generating model work with linguistic features that require precise treatment?

I used the three language rules defined below, based on my understanding of Sanskrit grammar and language structure. There are many other rules that are not considered here. I used the Lalita Sahasranama as the Sanskrit text and applied the rules to it. The experiment covers source recovery and annotation only. It does not show general Sanskrit proficiency.


## 2. What is provided

**The code**, shared so others can read it, learn from the approach and test the idea. It is not open-source licensed; to reuse or build on it, please contact me (see License below).

| File | What it does |
|---|---|
| `src/marklib.py` | The classifier. Applies the three rules to Unicode Devanagari text. |
| `src/mark_text.py` | Command line tool: text file in, marked HTML (and optional PDF) out. |
| `src/decode.py`, `src/build_text.py` | Decoder for one specific legacy font ("Ancient Sanskrit 99") that turns `pdftotext` output into Unicode. Specific to that font; another PDF needs a new table. |
| `src/make_pdf.py`, `src/print_template.html` | Builds a paged PDF from a decoded text file. |

### The three rules

| Rule | What it marks | Color |
|---|---|---|
| Mahaprana | The aspirates ख घ छ झ ठ ढ थ ध फ भ, plus ष and ह (श and स are not marked). A conjunct containing one of these is colored as a whole letter. | Pink, bold |
| Samyuktakshara | Any conjunct: two or more consonants joined, including reph forms | Yellow highlight |
| Dirgha Samyukta | The long-vowel letter immediately before a conjunct; the conjunct itself stays yellow only | Green underline |

Reading is continuous: a long letter at the end of a word counts if the next word begins with a conjunct. The pink group (ष and ह in addition to the ten aspirates) is the author's own convention, not a standard one.

## 3. Evidence

A snapshot only: the marked output for verses 1 to 10.

- `examples/verses_1-10_input.txt`: the ten verses as Unicode text
- `examples/verses_1-10_marked.html` and `.png`: the marked result
- `examples/sample_*`: a two-line test (the "sarve bhavantu sukhinah" verse)

![Verses 1 to 10, marked](examples/verses_1-10_marked.png)

The source PDF and the full decoded and marked files are intentionally not included; they are not needed to evaluate the approach.

## Run it on your own text

```bash
pip install -r requirements.txt && playwright install chromium   # Chromium only needed for --pdf
python src/mark_text.py my_text.txt my_text_marked.html --pdf my_text_marked.pdf
```

Input must be Unicode Devanagari, one line of text per line. The FreeSerif and FreeSans fonts are used for rendering if installed.

## Status: please read

- The classifier has been tested only on this stotra and a short sample. It should work on other Unicode Devanagari text, but that is untested. Please try it and open an issue with failures.
- The output counts are not accuracy scores. No Sanskrit teacher has reviewed the text or the marking conventions.
- The ten verses in the sample were decoded from a PDF whose edition is not identified, and have not been compared with a printed edition. Treat them as illustrative.

## License

- **Code, sample marking and README:** Copyright (c) 2026 Yogesh Weling. All rights reserved; no open-source license is granted. You are welcome to read the code and run it locally to evaluate it. If you want to reuse, modify, redistribute or build on it, please get in touch first: open an issue on this repository or contact me through the Substack article linked above.
- **Sanskrit text:** the Lalita Sahasranama is a traditional text. No license is asserted over the verses in `examples/`; they are a small excerpt shown for demonstration, provided as-is. If you are a rights holder and want the excerpt credited differently or removed, please open an issue.
