# main_interface.py
import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path

import data_storage
import encryption_module
import recovery_encryptor
import recovery_decryptor
import word_restoration

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.title("🔐 DocxMasker")
        self.geometry("1000x750")
        self.resizable(True, True)
        self.configure(fg_color="#1E1E2E")

        # Fonts
        self.title_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        self.label_font = ctk.CTkFont(family="Segoe UI", size=16)
        self.entry_font = ctk.CTkFont(family="Segoe UI", size=13)

        self.container = ctk.CTkFrame(self, fg_color="#1E1E2E")
        self.container.pack(fill="both", expand=True)

        # Top Navigation
        self.nav_frame = ctk.CTkFrame(
            self.container, fg_color="#1E1E2E", corner_radius=0
        )
        self.nav_frame.pack(side="top", fill="x", padx=10, pady=10)

        self.segmented_button = ctk.CTkSegmentedButton(
            self.nav_frame,
            values=["📦 Database", "🔄 Encryption", "🔓 Recovery"],
            command=self.show_section,
            fg_color="#313244",
            selected_color="#89B4FA",
            unselected_color="#313244",
            text_color="#FFFFFF",
            font=self.label_font,
        )
        self.segmented_button.pack(side="top", fill="x", padx=5, pady=10)
        self.segmented_button.set("📦 Database")

        # Section Containers - using ScrollableFrame for Recovery to fix layout overflow
        self.sections = {
            "database": ctk.CTkFrame(
                self.container, fg_color="#1E1E2E", corner_radius=12
            ),
            "encryption": ctk.CTkFrame(
                self.container, fg_color="#1E1E2E", corner_radius=12
            ),
            "recovery": ctk.CTkScrollableFrame(
                self.container, fg_color="#1E1E2E", corner_radius=12
            ),
        }

        self.build_database_section()
        self.build_encryption_section()
        self.build_recovery_section()

        self.show_section("📦 Database")

    def show_section(self, section_name: str) -> None:
        """Hide inactive frames and show selected section."""
        mapping = {
            "📦 Database": "database",
            "🔄 Encryption": "encryption",
            "🔓 Recovery": "recovery",
        }

        for frame in self.sections.values():
            frame.pack_forget()

        key = mapping.get(section_name)
        if key and key in self.sections:
            self.sections[key].pack(fill="both", expand=True, padx=20, pady=10)

    # ------------------ SECTION 1: DATABASE ------------------
    def build_database_section(self) -> None:
        frame = self.sections["database"]

        title = ctk.CTkLabel(
            frame,
            text="📦 Database Management",
            font=self.title_font,
            text_color="#89B4FA",
        )
        title.pack(anchor="w", padx=15, pady=(15, 10))

        # DOCX file selector
        ctk.CTkLabel(
            frame,
            text="Select DOCX file (names separated by comma):",
            font=self.label_font,
        ).pack(anchor="w", padx=15, pady=(5, 2))
        f_docx = ctk.CTkFrame(frame, fg_color="transparent")
        f_docx.pack(fill="x", padx=15, pady=2)

        self.db_docx_entry = ctk.CTkEntry(
            f_docx, font=self.entry_font, placeholder_text="Path to .docx file..."
        )
        self.db_docx_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        btn_browse_docx = ctk.CTkButton(
            f_docx,
            text="Browse",
            width=100,
            command=self.browse_db_docx,
            fg_color="#3B8ED0",
        )
        btn_browse_docx.pack(side="right")

        # DB file path
        ctk.CTkLabel(frame, text="Database Path (.db):", font=self.label_font).pack(
            anchor="w", padx=15, pady=(10, 2)
        )
        f_db = ctk.CTkFrame(frame, fg_color="transparent")
        f_db.pack(fill="x", padx=15, pady=2)

        self.db_path_entry = ctk.CTkEntry(
            f_db, font=self.entry_font, placeholder_text="Path to .db file..."
        )
        self.db_path_entry.insert(0, "data_names.db")
        self.db_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        btn_browse_db = ctk.CTkButton(
            f_db,
            text="Browse / Create",
            width=100,
            command=self.browse_db_path,
            fg_color="#3B8ED0",
        )
        btn_browse_db.pack(side="right")

        # Manual entry toggle & text box
        self.manual_toggle_btn = ctk.CTkButton(
            frame,
            text="Toggle Manual Name Input",
            command=self.toggle_manual_textbox,
            fg_color="#313244",
        )
        self.manual_toggle_btn.pack(anchor="w", padx=15, pady=10)

        self.manual_textbox = ctk.CTkTextbox(frame, height=120, font=self.entry_font)
        self.manual_textbox.insert("1.0", "Type names here (one name per line)...")
        self.manual_textbox_visible = False

        # Create Database Action Button
        btn_create = ctk.CTkButton(
            frame,
            text="Create / Update Database",
            font=self.label_font,
            fg_color="#89B4FA",
            text_color="#1E1E2E",
            command=self.run_create_database,
        )
        btn_create.pack(anchor="w", padx=15, pady=15)

        self.db_status_label = ctk.CTkLabel(
            frame, text="", font=self.label_font, text_color="#A6E3A1"
        )
        self.db_status_label.pack(anchor="w", padx=15, pady=5)

    def browse_db_docx(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if path:
            self.db_docx_entry.delete(0, tk.END)
            self.db_docx_entry.insert(0, path)

    def browse_db_path(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".db", filetypes=[("SQLite Database", "*.db")]
        )
        if path:
            self.db_path_entry.delete(0, tk.END)
            self.db_path_entry.insert(0, path)

    def toggle_manual_textbox(self) -> None:
        if self.manual_textbox_visible:
            self.manual_textbox.pack_forget()
            self.manual_textbox_visible = False
        else:
            self.manual_textbox.pack(fill="x", padx=15, pady=5)
            self.manual_textbox_visible = True

    def run_create_database(self) -> None:
        try:
            docx_path = self.db_docx_entry.get().strip()
            db_path = self.db_path_entry.get().strip()

            if not db_path:
                self.db_status_label.configure(
                    text="⚠️ Please specify a database file path.",
                    text_color="#F388BA",
                )
                return

            performed = False
            if docx_path and os.path.exists(docx_path):
                data_storage.made_data(docx_path, db_path)
                performed = True

            if self.manual_textbox_visible:
                raw_text = self.manual_textbox.get("1.0", tk.END).strip()
                lines = [
                    line.strip()
                    for line in raw_text.splitlines()
                    if line.strip() and not line.startswith("Type names here")
                ]
                if lines:
                    data_storage.add_manual_names(lines, db_path)
                    performed = True

            if performed:
                self.db_status_label.configure(
                    text="Database successfully updated!", text_color="#A6E3A1"
                )
            else:
                self.db_status_label.configure(
                    text="⚠️ Please provide a valid DOCX file or manual names.",
                    text_color="#F388BA",
                )
        except Exception as e:
            self.db_status_label.configure(text=f"⚠️ Error: {e}", text_color="#F388BA")

    # ------------------ SECTION 2: ENCRYPTION ------------------
    def build_encryption_section(self) -> None:
        frame = self.sections["encryption"]

        title = ctk.CTkLabel(
            frame,
            text="🔄 Text Masking & Encryption",
            font=self.title_font,
            text_color="#89B4FA",
        )
        title.pack(anchor="w", padx=15, pady=(15, 5))

        # Select Database Path
        ctk.CTkLabel(frame, text="Database Path (.db):", font=self.label_font).pack(
            anchor="w", padx=15, pady=2
        )
        f_db = ctk.CTkFrame(frame, fg_color="transparent")
        f_db.pack(fill="x", padx=15, pady=2)

        self.enc_db_entry = ctk.CTkEntry(
            f_db, font=self.entry_font, placeholder_text="Path to .db file..."
        )
        self.enc_db_entry.insert(0, "data_names.db")
        self.enc_db_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        btn_browse_enc_db = ctk.CTkButton(
            f_db,
            text="Browse",
            width=100,
            command=self.browse_enc_db,
            fg_color="#3B8ED0",
        )
        btn_browse_enc_db.pack(side="right")

        # Input DOCX File (Text to Block)
        ctk.CTkLabel(
            frame,
            text="Input DOCX File (Text to Block):",
            font=self.label_font,
        ).pack(anchor="w", padx=15, pady=2)
        f_target = ctk.CTkFrame(frame, fg_color="transparent")
        f_target.pack(fill="x", padx=15, pady=2)

        self.enc_target_entry = ctk.CTkEntry(
            f_target, font=self.entry_font, placeholder_text="Input DOCX path..."
        )
        self.enc_target_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        btn_browse_target = ctk.CTkButton(
            f_target,
            text="Browse",
            width=100,
            command=self.browse_enc_target,
            fg_color="#3B8ED0",
        )
        btn_browse_target.pack(side="right")

        # Save Output DOCX
        ctk.CTkLabel(
            frame, text="Save Output Path (.docx):", font=self.label_font
        ).pack(anchor="w", padx=15, pady=2)
        f_save = ctk.CTkFrame(frame, fg_color="transparent")
        f_save.pack(fill="x", padx=15, pady=2)

        self.enc_save_entry = ctk.CTkEntry(
            f_save, font=self.entry_font, placeholder_text="Output DOCX path..."
        )
        self.enc_save_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        btn_browse_save = ctk.CTkButton(
            f_save,
            text="Browse",
            width=100,
            command=self.browse_enc_save,
            fg_color="#3B8ED0",
        )
        btn_browse_save.pack(side="right")

        # Replacement Code Word (Full Width)
        ctk.CTkLabel(
            frame,
            text="Replacement Code Word (e.g. CODENAME):",
            font=self.label_font,
        ).pack(anchor="w", padx=15, pady=2)
        self.coding_word_entry = ctk.CTkEntry(
            frame,
            font=self.entry_font,
            placeholder_text="Coding word...",
        )
        self.coding_word_entry.insert(0, "CODENAME")
        self.coding_word_entry.pack(fill="x", padx=15, pady=2)

        # Recovery File Password
        ctk.CTkLabel(frame, text="Recovery File Password:", font=self.label_font).pack(
            anchor="w", padx=15, pady=2
        )
        self.enc_pwd_entry = ctk.CTkEntry(frame, font=self.entry_font, show="*")
        self.enc_pwd_entry.pack(fill="x", padx=15, pady=2)

        # Action & Progress
        btn_run = ctk.CTkButton(
            frame,
            text="Run Encryption",
            font=self.label_font,
            fg_color="#89B4FA",
            text_color="#1E1E2E",
            command=self.run_encryption,
        )
        btn_run.pack(anchor="w", padx=15, pady=10)

        self.progress_bar = ctk.CTkProgressBar(frame, progress_color="#89B4FA")
        self.progress_bar.pack(fill="x", padx=15, pady=5)
        self.progress_bar.set(0)

        self.enc_status_label = ctk.CTkLabel(
            frame, text="", font=self.label_font, text_color="#A6E3A1"
        )
        self.enc_status_label.pack(anchor="w", padx=15, pady=5)

    def browse_enc_db(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
        if path:
            self.enc_db_entry.delete(0, tk.END)
            self.enc_db_entry.insert(0, path)

    def browse_enc_target(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if path:
            self.enc_target_entry.delete(0, tk.END)
            self.enc_target_entry.insert(0, path)

    def browse_enc_save(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]
        )
        if path:
            self.enc_save_entry.delete(0, tk.END)
            self.enc_save_entry.insert(0, path)

    def run_encryption(self) -> None:
        try:
            self.progress_bar.set(0.2)
            db_path = self.enc_db_entry.get().strip()
            target_docx = self.enc_target_entry.get().strip()
            save_docx = self.enc_save_entry.get().strip()
            coding_word = self.coding_word_entry.get().strip() or "CODENAME"
            password = self.enc_pwd_entry.get().strip()

            if not target_docx or not save_docx or not db_path:
                self.enc_status_label.configure(
                    text="⚠️ Target path, save path, and DB path are required.",
                    text_color="#F388BA",
                )
                self.progress_bar.set(0)
                return

            self.progress_bar.set(0.5)
            # استدعاء الدالة بحسب المعاملات الصحيحة الخاصة بها
            mapping = encryption_module.Word_storage(
                target_file2=target_docx,
                db_path=db_path,
                coding_word=coding_word,
                target_of_user=save_docx,
            )

            if not mapping:
                self.enc_status_label.configure(
                    text="⚠️ Encryption failed or no names found in database.",
                    text_color="#F388BA",
                )
                self.progress_bar.set(0)
                return

            self.progress_bar.set(0.8)
            json_path = str(Path(save_docx).with_suffix(".json"))

            # التشفير وحذف الأصلي فقط في حال إدخال كلمة مرور
            if password:
                enc_json_path = json_path + ".enc"
                success = recovery_encryptor.encrypt_recovery_file(
                    json_path, password, enc_json_path
                )
                if success:
                    status_text = (
                        "Encryption complete! DOCX and encrypted JSON (.enc) saved."
                    )
                else:
                    status_text = "⚠️ DOCX saved, but JSON encryption failed."
            else:
                status_text = "Encryption complete! DOCX and plain JSON saved (No password provided)."

            self.progress_bar.set(1.0)
            self.enc_status_label.configure(
                text=status_text,
                text_color="#A6E3A1",
            )
        except Exception as e:
            self.enc_status_label.configure(
                text=f"⚠️ Encryption failed: {e}", text_color="#F388BA"
            )
            self.progress_bar.set(0)

    # ------------------ SECTION 3: RECOVERY ------------------
    def build_recovery_section(self) -> None:
        frame = self.sections["recovery"]

        title = ctk.CTkLabel(
            frame,
            text="🔓 Key Restoration & Document Recovery",
            font=self.title_font,
            text_color="#89B4FA",
        )
        title.pack(anchor="w", padx=15, pady=(10, 5))

        # Sub-task A: Decrypt Recovery Key File
        card_a = ctk.CTkFrame(frame, fg_color="#24253A", corner_radius=8)
        card_a.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            card_a,
            text="1. Decrypt Recovery Key",
            font=self.label_font,
            text_color="#89B4FA",
        ).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(card_a, text="Decryption Password:", font=self.label_font).pack(
            anchor="w", padx=10, pady=2
        )
        self.rec_pwd_entry = ctk.CTkEntry(
            card_a, font=self.entry_font, show="*", placeholder_text="Enter password..."
        )
        self.rec_pwd_entry.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(card_a, text="Encrypted File (.enc):", font=self.label_font).pack(
            anchor="w", padx=10, pady=2
        )
        f_enc = ctk.CTkFrame(card_a, fg_color="transparent")
        f_enc.pack(fill="x", padx=10, pady=2)
        self.rec_enc_entry = ctk.CTkEntry(
            f_enc, font=self.entry_font, placeholder_text="Select .enc file..."
        )
        self.rec_enc_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_browse_enc = ctk.CTkButton(
            f_enc,
            text="Browse",
            width=80,
            command=self.browse_rec_enc,
            fg_color="#3B8ED0",
        )
        btn_browse_enc.pack(side="right")

        ctk.CTkLabel(card_a, text="Output JSON File:", font=self.label_font).pack(
            anchor="w", padx=10, pady=2
        )
        f_dec_out = ctk.CTkFrame(card_a, fg_color="transparent")
        f_dec_out.pack(fill="x", padx=10, pady=2)
        self.rec_dec_out_entry = ctk.CTkEntry(
            f_dec_out, font=self.entry_font, placeholder_text="Save decrypted json..."
        )
        self.rec_dec_out_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_browse_dec_out = ctk.CTkButton(
            f_dec_out,
            text="Browse",
            width=80,
            command=self.browse_rec_dec_out,
            fg_color="#3B8ED0",
        )
        btn_browse_dec_out.pack(side="right")

        btn_decrypt = ctk.CTkButton(
            card_a,
            text="Decrypt Key",
            fg_color="#89B4FA",
            text_color="#1E1E2E",
            command=self.run_decryption,
        )
        btn_decrypt.pack(anchor="w", padx=10, pady=8)

        self.decrypt_status_label = ctk.CTkLabel(
            card_a, text="", font=self.label_font, text_color="#A6E3A1"
        )
        self.decrypt_status_label.pack(anchor="w", padx=10, pady=2)

        # Sub-task B: Restore Original DOCX
        card_b = ctk.CTkFrame(frame, fg_color="#24253A", corner_radius=8)
        card_b.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            card_b,
            text="2. Restore Original Document",
            font=self.label_font,
            text_color="#89B4FA",
        ).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(card_b, text="Mapping JSON File:", font=self.label_font).pack(
            anchor="w", padx=10, pady=2
        )
        f_json = ctk.CTkFrame(card_b, fg_color="transparent")
        f_json.pack(fill="x", padx=10, pady=2)
        self.rest_json_entry = ctk.CTkEntry(
            f_json, font=self.entry_font, placeholder_text="Select mapping json..."
        )
        self.rest_json_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_browse_json = ctk.CTkButton(
            f_json,
            text="Browse",
            width=80,
            command=self.browse_rest_json,
            fg_color="#3B8ED0",
        )
        btn_browse_json.pack(side="right")

        ctk.CTkLabel(card_b, text="Modified DOCX File:", font=self.label_font).pack(
            anchor="w", padx=10, pady=2
        )
        f_mod = ctk.CTkFrame(card_b, fg_color="transparent")
        f_mod.pack(fill="x", padx=10, pady=2)
        self.rest_mod_entry = ctk.CTkEntry(
            f_mod, font=self.entry_font, placeholder_text="Select modified docx..."
        )
        self.rest_mod_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_browse_mod = ctk.CTkButton(
            f_mod,
            text="Browse",
            width=80,
            command=self.browse_rest_mod,
            fg_color="#3B8ED0",
        )
        btn_browse_mod.pack(side="right")

        ctk.CTkLabel(card_b, text="Restored Output File:", font=self.label_font).pack(
            anchor="w", padx=10, pady=2
        )
        f_out = ctk.CTkFrame(card_b, fg_color="transparent")
        f_out.pack(fill="x", padx=10, pady=2)
        self.rest_out_entry = ctk.CTkEntry(
            f_out,
            font=self.entry_font,
            placeholder_text="Save restored docx...",
        )
        self.rest_out_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_browse_out = ctk.CTkButton(
            f_out,
            text="Browse",
            width=80,
            command=self.browse_rest_out,
            fg_color="#3B8ED0",
        )
        btn_browse_out.pack(side="right")

        btn_restore = ctk.CTkButton(
            card_b,
            text="Restore Document",
            fg_color="#89B4FA",
            text_color="#1E1E2E",
            command=self.run_restoration,
        )
        btn_restore.pack(anchor="w", padx=10, pady=8)

        self.restore_status_label = ctk.CTkLabel(
            card_b, text="", font=self.label_font, text_color="#A6E3A1"
        )
        self.restore_status_label.pack(anchor="w", padx=10, pady=2)

    def browse_rec_enc(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[("Encrypted Recovery", "*.enc;*.json.enc"), ("All Files", "*.*")]
        )
        if path:
            self.rec_enc_entry.delete(0, tk.END)
            self.rec_enc_entry.insert(0, path)

    def browse_rec_dec_out(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON File", "*.json")]
        )
        if path:
            self.rec_dec_out_entry.delete(0, tk.END)
            self.rec_dec_out_entry.insert(0, path)

    def run_decryption(self) -> None:
        enc_file = self.rec_enc_entry.get().strip()
        pwd = self.rec_pwd_entry.get().strip()
        out_file = self.rec_dec_out_entry.get().strip()

        if not enc_file or not pwd or not out_file:
            self.decrypt_status_label.configure(
                text="⚠️ All decryption fields are required.", text_color="#F388BA"
            )
            return

        success = recovery_decryptor.decrypt_recovery_file(enc_file, pwd, out_file)
        if success:
            self.decrypt_status_label.configure(
                text="Recovery file decrypted successfully!", text_color="#A6E3A1"
            )
            self.rest_json_entry.delete(0, tk.END)
            self.rest_json_entry.insert(0, out_file)
        else:
            self.decrypt_status_label.configure(
                text="⚠️ Password is incorrect", text_color="#F388BA"
            )

    def browse_rest_json(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON Mapping", "*.json")])
        if path:
            self.rest_json_entry.delete(0, tk.END)
            self.rest_json_entry.insert(0, path)

    def browse_rest_mod(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if path:
            self.rest_mod_entry.delete(0, tk.END)
            self.rest_mod_entry.insert(0, path)

    def browse_rest_out(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".docx", filetypes=[("Word Documents", "*.docx")]
        )
        if path:
            self.rest_out_entry.delete(0, tk.END)
            self.rest_out_entry.insert(0, path)

    def run_restoration(self) -> None:
        json_file = self.rest_json_entry.get().strip()
        mod_docx = self.rest_mod_entry.get().strip()
        out_docx = self.rest_out_entry.get().strip()

        if not json_file or not mod_docx or not out_docx:
            self.restore_status_label.configure(
                text="⚠️ All restoration fields are required.", text_color="#F388BA"
            )
            return

        success = word_restoration.Word_restoration(mod_docx, json_file, out_docx)
        if success:
            self.restore_status_label.configure(
                text="Document restored successfully!", text_color="#A6E3A1"
            )
        else:
            self.restore_status_label.configure(
                text="⚠️ Document restoration failed.", text_color="#F388BA"
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()
