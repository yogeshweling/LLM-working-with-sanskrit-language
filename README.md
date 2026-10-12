# Marking Sanskrit text by pronunciation rules, using a language model (Claude in this case)

A practical experiment to explore possibility of making specific linguistic features and the knowledge preserved in texts easier to be available for language usage.

Many languages carry features through pronunciation, spelling and grammatical structure that a short translation or paraphrase may not capture. I wanted to explore whether a model could help make some of those features visible and usable.
I chose the Lalita Sahasranama - a Sanskrit hymn text as a practical test. I gave Claude an old-font PDF and three marking conventions I defined: pink for a selected group of consonants, yellow for conjuncts, and green underlining for a long-vowel-bearing unit before a conjunct.

I asked Claude to help build the tool without writing the code myself. my question was broader: could a model interpret explicit linguistic rules, turn them into code, and preserve the source text?
The experiment involved recovering readable Devanagari from a legacy font, clarifying ambiguous instructions, and revising the programs that applied the markings.

Model and environment: mostly Claude Sonnet 5.5 at medium effort (a few responses ran on Sonnet 4.6), working in an agent environment with shell, file, PDF and document tools.
Claude proposed the decoding map, wrote the decoder and classifier, and revised the code when I clarified or changed the rules. The programs performed the repeated decoding, marking and rendering. The output text therefore came from executing the decoder, with a mapping proposed by the model; it was not simply a new transcription generated in a chat response.
The practical value was that I could describe a specialized task and iteratively build a tool. Once the text and rules are verified, a program can apply those rules repeatedly. This project did not require a vector database or retrieval system, and I did not measure its cost.

My key takeaway: language models can help turn language-specific rules into practical tools—with code and outputs checked against trusted examples.


Read the full write-up: **[Substack link]**

## 1. What this demonstrates

How an LLM such as Claude can work with a language like Sanskrit and produce useful work by applying rules you give it: here, visual marking of letters for chanting practice. The test text was the Lalita Sahasranama. The experiment covers source recovery and annotation only. It does not show general Sanskrit proficiency.

## 2. What is provided

**The code**, under the MIT License, so anyone can take the idea and extend it.

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

- **Code, sample marking and README:** MIT License, see `LICENSE`.
- **Sanskrit text:** the Lalita Sahasranama is a traditional text. No license is asserted over the verses in `examples/`; they are a small excerpt shown for demonstration, provided as-is. If you are a rights holder and want the excerpt credited differently or removed, please open an issue.
