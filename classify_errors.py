#!/usr/bin/env python3
"""
HTR Error Classifier: Detailed error analysis between gold-standard and automatic transcriptions.

Usage:
    python classify_errors.py reference.txt hypothesis.txt output_prefix

Assumes input files are normalized plain text (UTF-8):
- lowercased, digits/brackets removed, whitespace collapsed
- page-aligned (one file per document, same logical segmentation)

Outputs:
- stats.json: Global error statistics by category
- errors.csv: Detailed error log with page/line context and classifications
- char_subs.csv: Most frequent character substitution pairs
"""

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import groupby
from typing import List, Dict, Tuple, Optional, NamedTuple
from difflib import SequenceMatcher


@dataclass
class EditOp:
    """Character-level edit operation."""
    ref_char: str
    hyp_char: str
    operation: str  # 'S', 'D', 'I', '='


@dataclass
class WordEditOp:
    """Word-level edit operation."""
    ref_words: List[str]
    hyp_words: List[str]
    operation: str  # 'S', 'D', 'I', '=', 'MERGE', 'SPLIT'


class ErrorType(Enum):
    CHAR_SUB = "char_substitution"
    CHAR_DEL = "char_deletion"
    CHAR_INS = "char_insertion"
    WORD_MERGE = "word_merge"
    WORD_SPLIT = "word_split"
    LEX_SUB = "lexical_substitution"
    ABBR_EXP = "abbrev_expansion"


def levenshtein_align(ref: str, hyp: str) -> List[EditOp]:
    """Compute character-level Levenshtein alignment."""
    n, m = len(ref), len(hyp)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if ref[i-1] == hyp[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # deletion
                dp[i][j-1] + 1,      # insertion
                dp[i-1][j-1] + cost  # substitution
            )
    

    ops = []
    i = n
    j = m
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref[i-1] == hyp[j-1]:
            ops.append(EditOp(ref[i-1], hyp[j-1], '='))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            ops.append(EditOp(ref[i-1], hyp[j-1], 'S'))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            ops.append(EditOp(ref[i-1], '', 'D'))
            i -= 1
        else:
            ops.append(EditOp('', hyp[j-1], 'I'))
            j -= 1
    
    return ops[::-1]


def word_align(ref_words: List[str], hyp_words: List[str]) -> List[WordEditOp]:
    """Simplified word-level alignment using difflib."""
    ref_str = ' '.join(ref_words)
    hyp_str = ' '.join(hyp_words)
    
    matcher = SequenceMatcher(None, ref_str, hyp_str)
    ops = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        ref_slice = ref_str[i1:i2].split()
        hyp_slice = hyp_str[j1:j2].split()
        
        if tag == 'equal':
            ops.append(WordEditOp(ref_slice, hyp_slice, '='))
        elif tag == 'delete':
            ops.append(WordEditOp(ref_slice, [], 'D'))
        elif tag == 'insert':
            ops.append(WordEditOp([], hyp_slice, 'I'))
        elif tag == 'replace':
            ops.append(WordEditOp(ref_slice, hyp_slice, 'S'))
    
    return ops


def classify_char_errors(ops: List[EditOp]) -> tuple[Dict, Dict]:
    """Classify character-level errors."""
    stats = defaultdict(int)
    sub_pairs = Counter()
    
    for op in ops:
        if op.operation == 'S':
            stats[ErrorType.CHAR_SUB.value] += 1
            sub_pairs[(op.ref_char, op.hyp_char)] += 1
        elif op.operation == 'D':
            stats[ErrorType.CHAR_DEL.value] += 1
        elif op.operation == 'I':
            stats[ErrorType.CHAR_INS.value] += 1
    
    return dict(stats), dict(sub_pairs)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Simple Levenshtein distance implementation."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def is_merge(ref_words: List[str], hyp_words: List[str], max_dist: int = 2) -> bool:
    """Check if hypothesis word is merge of multiple reference words."""
    if len(ref_words) < 2 or len(hyp_words) != 1:
        return False
    
    merged_ref = ''.join(ref_words)
    return levenshtein_distance(merged_ref, hyp_words[0]) <= max_dist


def is_split(ref_words: List[str], hyp_words: List[str], max_dist: int = 2) -> bool:
    """Check if reference word is split into multiple hypothesis words."""
    if len(ref_words) != 1 or len(hyp_words) < 2:
        return False
    
    merged_hyp = ''.join(hyp_words)
    return levenshtein_distance(ref_words[0], merged_hyp) <= max_dist


def is_abbrev_expansion(ref_word: str, hyp_word: str, min_ratio: float = 1.5) -> bool:
    """Detect abbreviation/expansion errors based on length ratio and prefix match."""
    if len(ref_word) == 0 or len(hyp_word) == 0:
        return False
    
    # Hypothesis is expansion (ref shorter)
    if len(hyp_word) > len(ref_word) * min_ratio and ref_word in hyp_word[:len(ref_word)+2]:
        return True
    # Reference is expansion (hyp shorter)
    if len(ref_word) > len(hyp_word) * min_ratio and hyp_word in ref_word[:len(hyp_word)+2]:
        return True
    
    return False


def classify_word_errors(word_ops: List[WordEditOp]) -> tuple[Dict, Dict]:
    """Classify word-level errors."""
    stats = defaultdict(int)
    examples = defaultdict(list)
    
    for op in word_ops:
        if op.operation == '=':
            continue
        
        r_words, h_words = op.ref_words, op.hyp_words
        
        # Check for merge/split
        if is_merge(r_words, h_words):
            stats[ErrorType.WORD_MERGE.value] += 1
            examples[ErrorType.WORD_MERGE.value].append((r_words, h_words))
        elif is_split(r_words, h_words):
            stats[ErrorType.WORD_SPLIT.value] += 1
            examples[ErrorType.WORD_SPLIT.value].append((r_words, h_words))
        elif len(r_words) == 1 and len(h_words) == 1:
            ref_w, hyp_w = r_words[0], h_words[0]
            if len(ref_w) >= 3 and len(hyp_w) >= 3:  # Ignore very short tokens
                if is_abbrev_expansion(ref_w, hyp_w):
                    stats[ErrorType.ABBR_EXP.value] += 1
                    examples[ErrorType.ABBR_EXP.value].append((ref_w, hyp_w))
                else:
                    stats[ErrorType.LEX_SUB.value] += 1
                    examples[ErrorType.LEX_SUB.value].append((ref_w, hyp_w))
        elif op.operation in ('D', 'I'):
            stats[f"word_{op.operation.lower()}"] += 1
    
    return dict(stats), dict(examples)


def parse_pages(text: str) -> List[str]:
    """Simple page splitting by double newlines or numbered sections."""
    # Split by double newlines or page-like patterns
    pages = re.split(r'\n\s*\n|\n\d+\.\s*\n', text.strip())
    return [p.strip() for p in pages if p.strip()]


def analyze_pages(ref_file: str, hyp_file: str) -> Tuple[Dict, List, Dict]:
    """Main analysis function working page by page."""
    try:
        with open(ref_file, 'r', encoding='utf-8') as f:
            ref_text = f.read()
        with open(hyp_file, 'r', encoding='utf-8') as f:
            hyp_text = f.read()
    except FileNotFoundError as e:
        print(f"Greška: Datoteka nije pronađena - {e}")
        print("Provjerite postoje li datoteke 'reference' i 'hypothesis' direktoriju.")
        return {}, [], {}
    
    ref_pages = parse_pages(ref_text)
    hyp_pages = parse_pages(hyp_text)
    
    all_stats = defaultdict(int)
    all_errors = []
    all_sub_pairs = Counter()
    
    min_pages = min(len(ref_pages), len(hyp_pages))
    
    print(f"Analiziram {min_pages} stranica...")
    
    for page_idx in range(min_pages):
        ref_page = ref_pages[page_idx]
        hyp_page = hyp_pages[page_idx]
        
        # Character alignment
        char_ops = levenshtein_align(ref_page, hyp_page)
        char_stats, sub_pairs = classify_char_errors(char_ops)
        
        for k, v in char_stats.items():
            all_stats[k] += v
        all_sub_pairs.update(sub_pairs)
        
        # Word alignment
        ref_words = ref_page.split()
        hyp_words = hyp_page.split()
        word_ops = word_align(ref_words, hyp_words)
        word_stats, word_examples = classify_word_errors(word_ops)
        
        for k, v in word_stats.items():
            all_stats[k] += v
        
        # Log errors with page context
        page_errors = []
        for op in word_ops:
            if op.operation != '=':
                error_row = {
                    'page': page_idx + 1,
                    'ref_context': ' '.join(op.ref_words),
                    'hyp_context': ' '.join(op.hyp_words),
                    'error_type': op.operation
                }
                page_errors.append(error_row)
        
        all_errors.extend(page_errors)
    
    return dict(all_stats), all_errors, dict(all_sub_pairs)


def save_outputs(stats: Dict, errors: List, sub_pairs: Dict, prefix: str):
    """Save statistics and error logs."""
    
    total_chars_ref = stats.get(ErrorType.CHAR_SUB.value, 0) + stats.get(ErrorType.CHAR_DEL.value, 0)
    total_chars_hyp = stats.get(ErrorType.CHAR_SUB.value, 0) + stats.get(ErrorType.CHAR_INS.value, 0)
    
    with open(f'{prefix}_stats.json', 'w', encoding='utf-8') as f:
        json.dump({
            'error_counts': stats,
            'total_chars_ref': total_chars_ref,
            'total_chars_hyp': total_chars_hyp
        }, f, indent=2, ensure_ascii=False)
    
    # Detailed errors CSV
    if errors:
        with open(f'{prefix}_errors.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['page', 'ref_context', 'hyp_context', 'error_type'])
            writer.writeheader()
            writer.writerows(errors)
    else:
        print("Nema word-level grešaka za logiranje")
    
    # Character substitutions CSV - UVIJEK napiši
    with open(f'{prefix}_char_subs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ref_char', 'hyp_char', 'count', 'napomena'])
        
        if sub_pairs:
            for (ref_c, hyp_c), count in sorted(sub_pairs.items(), key=lambda x: x[1], reverse=True):
                writer.writerow([ref_c, hyp_c, count, ''])
        else:
            writer.writerow(['', '', '0', 'Nema karakter zamjena - provjeri normalizaciju tekstova'])
    
    print(f"Sve datoteke spremljene: {prefix}_*.csv/json")


def main():
    parser = argparse.ArgumentParser(description="HTR Error Classifier")
    parser.add_argument('reference', help="Gold-standard transcription (.txt)")
    parser.add_argument('hypothesis', help="HTR/Transkribus transcription (.txt)") 
    parser.add_argument('output_prefix', help="Output file prefix")
    
    args = parser.parse_args()
    
    print("Analyzing transcriptions...")
    stats, errors, sub_pairs = analyze_pages(args.reference, args.hypothesis)
    
    save_outputs(stats, errors, sub_pairs, args.output_prefix)
    
    print("\n=== SUMMARY ===")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print(f"\nDetailed logs saved to {args.output_prefix}_*.csv/json")


if __name__ == "__main__":
    main()
