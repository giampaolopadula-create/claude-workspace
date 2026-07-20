#!/usr/bin/env python3
"""Legge i commenti (note in giallo) da un file Word"""

import sys
from docx import Document
from docx.oxml.ns import qn

def read_word_comments(file_path):
    """Legge i commenti da un file Word .docx"""
    doc = Document(file_path)

    print("=== COMMENTI/NOTE NEL DOCUMENTO ===\n")

    # Leggi i commenti dalla parte finale del documento (parts)
    comments_part = None
    for rel in doc.part.rels.values():
        if "comments" in rel.reltype:
            comments_part = rel.target_part
            break

    if comments_part:
        comments_xml = comments_part.element
        for comment in comments_xml.findall(qn('w:comment')):
            comment_id = comment.get(qn('w:id'))
            comment_author = comment.get(qn('w:author'))
            comment_date = comment.get(qn('w:date'))

            # Leggi il testo del commento
            comment_text = ""
            for p in comment.findall(qn('w:p')):
                for t in p.findall(qn('w:t')):
                    if t.text:
                        comment_text += t.text

            if comment_text:
                print(f"📝 Commento #{comment_id}")
                print(f"   Autore: {comment_author}")
                print(f"   Data: {comment_date}")
                print(f"   Testo: {comment_text}\n")
    else:
        print("Nessun commento trovato nel documento.")

        # Prova a leggere i "track changes" o "revisions"
        print("\n=== PARAGRAFI CON EVIDENZIAZIONE ===\n")
        for i, para in enumerate(doc.paragraphs):
            # Cerca paragrafi con evidenziazione (giallo)
            for run in para.runs:
                shd = run._element.get(qn('w:shd'))
                highlight = run.font.highlight_color
                if highlight or shd:
                    print(f"Paragrafo {i}: {para.text[:100]}...")
                    if highlight:
                        print(f"  Highlight color: {highlight}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python read_word_comments.py <file.docx>")
        sys.exit(1)

    read_word_comments(sys.argv[1])
