# data_storage.py
import sqlite3
from docx import Document
from typing import List


def made_data(docx_path: str, db_name: str = "data_names.db") -> None:
    try:
        words_list_end = []
        doc = Document(docx_path)

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                for word in paragraph.text.split(","):
                    cleaned_word = word.strip()
                    if cleaned_word:
                        words_list_end.append((cleaned_word,))

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data (
                Names TEXT NOT NULL
            )
            """
        )

        if words_list_end:
            cursor.executemany("INSERT INTO data (Names) VALUES (?)", words_list_end)

        conn.commit()
        conn.close()
        print("Successfully created database and stored names.")
    except FileNotFoundError:
        print(f"⚠️ File not found at path: {docx_path}")
    except sqlite3.Error as e:
        print(f"⚠️ SQLite database error: {e}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred while storing data: {e}")


def add_manual_names(names: List[str], db_name: str = "data_names.db") -> None:
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data (
                Names TEXT NOT NULL
            )
            """
        )
        rows = [(name.strip(),) for name in names if name.strip()]
        if rows:
            cursor.executemany("INSERT INTO data (Names) VALUES (?)", rows)

        conn.commit()
        conn.close()
        print("Successfully added manual names to database.")
    except sqlite3.Error as e:
        print(f"⚠️ SQLite database error: {e}")
    except Exception as e:
        print(f"⚠️ An error occurred while adding manual names: {e}")
