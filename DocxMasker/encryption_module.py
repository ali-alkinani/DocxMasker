# encryption_module.py
import sqlite3
import json
import re
from pathlib import Path
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from typing import List, Dict


def used_data(db_path: str, query: str = "SELECT * FROM data") -> List[str]:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall() if row[0]]
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"⚠️ Database query error: {e}")
        return []
    except Exception as e:
        print(f"⚠️ Error reading database: {e}")
        return []


def Word_storage(
    target_file2: str,
    db_path: str,
    coding_word: str,
    target_of_user: str,
) -> Dict[str, str]:
    try:
        names_list = used_data(db_path)
        if not names_list:
            print("⚠️ No names were found in the specified database.")
            return {}

        # Sort names by length descending to match full names before substrings
        names_list = sorted(set(names_list), key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(name) for name in names_list))

        the_file_of_storage = {}
        counter = 1
        content = Document(target_file2)

        def replace_and_store(match: re.Match) -> str:
            nonlocal counter
            original_word = match.group(0)
            new_word = f"{coding_word}{counter}"
            the_file_of_storage[new_word] = original_word
            counter += 1
            return new_word

        def process_paragraphs(paragraphs):
            for p in paragraphs:
                if pattern.search(p.text):
                    p.text = pattern.sub(replace_and_store, p.text)

        def process_table(table):
            for row in table.rows:
                for cell in row.cells:
                    process_block_elements(cell._tc)
                    for nested_table in cell.tables:
                        process_table(nested_table)

        def process_block_elements(parent_element):
            for child in parent_element:
                if child.tag.endswith('p'):
                    p = Paragraph(child, content)
                    if pattern.search(p.text):
                        p.text = pattern.sub(replace_and_store, p.text)
                elif child.tag.endswith('tbl'):
                    table = Table(child, content)
                    process_table(table)

        # Process main body elements in strict chronological order
        process_block_elements(content.element.body)

        # Process headers and footers
        for section in content.sections:
            for attr in ("header", "footer"):
                part = getattr(section, attr)
                process_block_elements(part._element)

        content.save(target_of_user)

        json_path = Path(target_of_user).with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(the_file_of_storage, f, ensure_ascii=False, indent=4)

        return the_file_of_storage
    except FileNotFoundError:
        print(f"⚠️ Target file not found: {target_file2}")
        return {}
    except Exception as e:
        print(f"⚠️ Encryption processing error: {e}")
        return {}
