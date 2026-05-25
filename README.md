# Transcribus-project

> Mala zbirka skripti za izračunavanje metrika pogrešaka u transkripciji govora (CER/WER), klasifikaciju pogrešaka i iscrtavanje grafikona rezultata.

## Sažetak

Ovaj repozitorij sadrži Python skripte koje se koriste za izračunavanje stope pogrešnih znakova (CER) i stope pogrešnih riječi (WER), klasifikaciju pogrešaka u transkripciji te generiranje jednostavnih grafikona na temelju rezultata. Korišten je s normaliziranim tekstualnim datotekama referentnog teksta i hipoteze te generira CSV/JSON izlazne datoteke i grafikone.

## Važne datoteke

- `cer_wer_mestrija.py` — izračunava CER/WER i metrike po stranici.
- `classify_errors.py` — klasificira i sažima pogreške u transkripciji.
- `graph-digital.py` — generira grafikone za digitalnu/automatsku analizu.
- `graph-manual.py` — generira grafikone za ručnu analizu/analizu anotatora.
- `reference_normalized.txt` — referentni transkripti (normalizirani).
- `hypothesis_normalized.txt` — transkripti hipoteze (normalizirani).
- `moj_rezultat_char_subs.csv`, `moj_rezultat_errors.csv`, `moj_rezultat_stats.json`, `page_level_cer_wer.csv` — primjeri izlaznih datoteka koje se već nalaze u repozitoriju.

## Preduvjeti

Instalirajte Python 3.8+ i uobičajene pakete za obradu podataka. Ako nemate datoteku `requirements.txt`, instalirajte uobičajene zavisnosti:

```bash
python -m venv .venv
source .venv/bin/activate    # na Windowsima: .venv\Scripts\activate
pip install pandas matplotlib seaborn numpy jiwer
Prilagodite pakete tako da odgovaraju vašem okruženju ili uvozima (imports) unutar skripti.

Brzi početak
Postavite svoje normalizirane datoteke referentnog teksta i hipoteze u korijensku mapu repozitorija (ili ažurirajte staze u skriptama):

reference_normalized.txt

hypothesis_normalized.txt

Pokrenite skriptu za izračun CER/WER metrika:

Bash
python cer_wer_mestrija.py
Pokrenite klasifikaciju pogrešaka:

Bash
python classify_errors.py
Izradite grafikone (ove skripte obično čitaju generirane CSV/JSON izlazne datoteke):

Bash
python graph-digital.py
python graph-manual.py