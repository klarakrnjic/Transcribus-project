# Transcribus-project

> A small collection of scripts for computing speech transcription error metrics (CER/WER), classifying errors, and plotting results.

## Summary

This repository contains Python scripts used to compute Character Error Rate (CER) and Word Error Rate (WER), classify transcription errors, and generate simple graphs from results. It was used with normalized reference/hypothesis text files and produces CSV/JSON outputs and plots.

## Files of interest

- `cer_wer_mestrija.py` — compute CER/WER and per-page metrics.
- `classify_errors.py` — classify and summarize transcription errors.
- `graph-digital.py` — generate digital/automatic-analysis graphs.
- `graph-manual.py` — generate manual/annotator graphs.
- `reference_normalized.txt` — reference transcripts (normalized).
- `hypothesis_normalized.txt` — hypothesis transcripts (normalized).
- `moj_rezultat_char_subs.csv`, `moj_rezultat_errors.csv`, `moj_rezultat_stats.json`, `page_level_cer_wer.csv` — example outputs already in the repo.

## Requirements

Install Python 3.8+ and the typical data packages. If you don't have a `requirements.txt`, install the common dependencies:

```bash
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install pandas matplotlib seaborn numpy jiwer
```

Adjust the packages to match your environment or the scripts' imports.

## Quickstart

1. Place your normalized reference and hypothesis files in the repo root (or update script paths):

   - `reference_normalized.txt`
   - `hypothesis_normalized.txt`

2. Run the CER/WER script:

```bash
python cer_wer_mestrija.py
```

3. Run error classification:

```bash
python classify_errors.py
```

4. Create plots (these scripts typically read the produced CSV/JSON outputs):

```bash
python graph-digital.py
python graph-manual.py
```

Check the generated files like `moj_rezultat_stats.json`, `moj_rezultat_errors.csv`, and `page_level_cer_wer.csv` for results.

## Notes

- The exact CLI arguments (if any) depend on how each script is implemented. If a script expects arguments, run `python script.py -h` or open the script to inspect usage.
- If you want, I can add a `requirements.txt` or make small wrappers that accept `--reference` and `--hypothesis` arguments for clearer CLI usage.

## Contributing

Open an issue or submit a PR with improvements, additional documentation, or a requirements file.

## License

Add your preferred license or leave it unlicensed.
