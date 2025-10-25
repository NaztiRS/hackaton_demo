import reflex as rx
import os
from pathlib import Path
import logging

DOCS_DIR = Path("uploaded_docs")


class DocsState(rx.State):
    doc_files: list[str] = []
    selected_doc: str = ""
    selected_doc_content: str = ""
    is_loading: bool = False

    def _ensure_docs_dir(self):
        DOCS_DIR.mkdir(exist_ok=True)

    @rx.event
    def on_load(self):
        return DocsState.load_doc_list

    @rx.event
    def load_doc_list(self):
        self._ensure_docs_dir()
        try:
            self.doc_files = sorted([f.name for f in DOCS_DIR.iterdir() if f.is_file()])
        except Exception as e:
            logging.exception(f"Error loading document list: {e}")
            yield rx.toast.error("Failed to load document list.")

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self._ensure_docs_dir()
        if not files:
            yield rx.toast.error("No files selected for upload.")
            return
        try:
            for file in files:
                upload_data = await file.read()
                file_path = DOCS_DIR / file.name
                with file_path.open("wb") as f:
                    f.write(upload_data)
            yield rx.toast.success(f"Successfully uploaded {len(files)} document(s).")
            yield DocsState.load_doc_list
            yield rx.clear_selected_files("docs_upload")
        except Exception as e:
            logging.exception(f"Error handling file upload: {e}")
            yield rx.toast.error("File upload failed.")

    @rx.event
    def select_doc(self, filename: str):
        self.is_loading = True
        self.selected_doc = filename
        self.selected_doc_content = ""
        yield
        try:
            file_path = DOCS_DIR / filename
            with file_path.open("r", encoding="utf-8") as f:
                self.selected_doc_content = f.read()
        except Exception as e:
            logging.exception(f"Error reading document {filename}: {e}")
            self.selected_doc_content = f"Error: Could not read file '{filename}'."
            yield rx.toast.error(f"Failed to read {filename}.")
        finally:
            self.is_loading = False