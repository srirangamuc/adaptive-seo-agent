from __future__ import annotations

import io
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_text_from_pdf(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    return _clean_text(" ".join(pages))


def _extract_text_from_html(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return _clean_text(soup.get_text(" "))


def fetch_source_text(source_url: str, source_type: Optional[str] = None) -> str:
    response = requests.get(source_url, timeout=30)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "").lower()

    if source_type == "pdf" or "application/pdf" in content_type:
        return _extract_text_from_pdf(response.content)

    if source_type == "html" or "text/html" in content_type:
        return _extract_text_from_html(response.content)

    return _clean_text(response.text)


def chunk_text(text: str, chunk_size: int = 1200) -> list[str]:
    if not text:
        return []
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
