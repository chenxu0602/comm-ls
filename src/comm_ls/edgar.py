"""
SEC EDGAR filing download and text extraction pipeline.

Downloads 10-K and 10-Q filings as plain text for a given set of tickers,
dating back to a configurable start year.  Uses only public www.sec.gov
endpoints that require no API key or registration.
"""

from __future__ import annotations

import html as html_mod
import json
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

logger = logging.getLogger(__name__)

BASE_URL = "https://www.sec.gov"
COMPANY_TICKERS_URL = f"{BASE_URL}/files/company_tickers.json"
BROWSE_EDGAR_URL = f"{BASE_URL}/cgi-bin/browse-edgar"
ARCHIVES_URL = f"{BASE_URL}/Archives/edgar/data"
USER_AGENT = "comm-ls/0.1 chen.xu.wq@gmail.com"

_RATE_LIMIT_SEC = 0.15
_BATCH_PAUSE_SEC = 1.0
_BATCH_SIZE = 100
_MAX_RETRIES = 3


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FilingEntry:
    """One row in the EDGAR filing index."""

    ticker: str
    cik: str
    accession: str
    form_type: str
    filing_date: str
    fiscal_year: int | None
    fiscal_period: str | None  # "FY", "Q1", "Q2", "Q3"
    index_url: str  # full URL to the -index.htm page
    doc_url: str | None = None  # resolved after parsing index page
    doc_filename: str | None = None


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _http_get(url: str, *, timeout: int = 30) -> bytes:
    """GET *url* and return response body bytes, with retry and rate-limiting."""
    last_exc: Exception | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:
            last_exc = exc
            if attempt < _MAX_RETRIES:
                wait = 2 ** attempt
                logger.debug("retry %d/%d for %s after %.1fs", attempt, _MAX_RETRIES, url, wait)
                time.sleep(wait)
    raise RuntimeError(f"Failed to fetch {url} after {_MAX_RETRIES} retries") from last_exc


def _http_get_text(url: str, *, timeout: int = 30) -> str:
    data = _http_get(url, timeout=timeout)
    # SEC pages are usually utf-8; fall back to latin-1
    for enc in ("utf-8", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# CIK mapping
# ---------------------------------------------------------------------------


def _cik10(cik: str) -> str:
    """Pad CIK to 10 digits with leading zeros."""
    return str(int("".join(c for c in str(cik) if c.isdigit()))).zfill(10)


def _cik_raw(cik: str) -> str:
    """CIK as an integer string (no leading zeros), used in archive URLs."""
    return str(int(_cik10(cik)))


def fetch_company_tickers(cache_path: Path | None = None) -> dict[str, str]:
    """Return ``{TICKER: cik10}`` mapping from SEC company_tickers.json.

    If *cache_path* is provided and exists, load from cache instead of
    downloading.
    """
    if cache_path is not None and cache_path.exists():
        logger.info("Loading CIK map from cache %s", cache_path)
        raw = json.loads(cache_path.read_text(encoding="utf-8"))
    else:
        logger.info("Downloading CIK map from %s", COMPANY_TICKERS_URL)
        raw = json.loads(_http_get_text(COMPANY_TICKERS_URL))
        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(raw, indent=2), encoding="utf-8")

    # SEC format: {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
    mapping: dict[str, str] = {}
    for entry in raw.values():
        ticker = str(entry.get("ticker", "")).strip().upper()
        cik = str(entry.get("cik_str", ""))
        if ticker and cik:
            mapping[ticker] = _cik10(cik)
    return mapping


# ---------------------------------------------------------------------------
# Filing index scraping
# ---------------------------------------------------------------------------


def _parse_browse_table(html_text: str) -> list[dict[str, str]]:
    """Parse the ``tableFile2`` rows from a browse-edgar results page."""
    rows: list[dict[str, str]] = []

    # Find the filings table body
    table_match = re.search(
        r'<table[^>]*class="tableFile2"[^>]*>(.*?)</table>',
        html_text,
        re.DOTALL,
    )
    if not table_match:
        return rows

    table = table_match.group(1)
    # Each filing row has the accession in an <a> href
    tr_blocks = re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.DOTALL)

    for tr in tr_blocks:
        # First <td> is form type
        td_match = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)
        if len(td_match) < 4:
            continue

        form_type = re.sub(r"<[^>]+>", "", td_match[0]).strip()
        documents_cell = td_match[1]
        description_cell = td_match[2]
        filing_date = re.sub(r"<[^>]+>", "", td_match[3]).strip()

        # Extract accession number from description
        acc_match = re.search(r"Acc-no:\s*([\d\-]+)", description_cell)
        if not acc_match:
            continue
        accession = acc_match.group(1)

        # Extract documents URL
        url_match = re.search(r'href="([^"]+)"', documents_cell)
        if not url_match:
            continue
        index_path = url_match.group(1)
        if not index_path.endswith("-index.htm"):
            continue
        index_url = f"{BASE_URL}{index_path}" if index_path.startswith("/") else index_path

        rows.append(
            {
                "form_type": form_type,
                "accession": accession,
                "filing_date": filing_date,
                "index_url": index_url,
            }
        )

    return rows


def _infer_fiscal_period(form_type: str, filing_date_str: str) -> tuple[int | None, str | None]:
    """Infer fiscal year and period from form type and filing date."""
    fiscal_period: str | None
    if form_type.upper() in ("10-K", "10-K/A", "10-KT", "10-K405", "20-F", "20-F/A", "40-F", "40-F/A"):
        fiscal_period = "FY"
    elif form_type.upper() in ("10-Q", "10-Q/A", "10-QT"):
        fiscal_period = None  # will be set below
    else:
        return None, None

    try:
        fd = pd.Timestamp(filing_date_str)
    except Exception:
        return None, fiscal_period

    if fiscal_period == "FY":
        # 10-K filed in early next year → fiscal year = filing year − 1
        if fd.month <= 3:
            return fd.year - 1, "FY"
        return fd.year, "FY"
    else:  # 10-Q
        # Map month to quarter
        # Q1: filed in Apr–Jun  → fiscal Q1
        # Q2: filed in Jul–Sep  → fiscal Q2
        # Q3: filed in Oct–Dec  → fiscal Q3
        # Q4: filed in Jan–Mar → Q4 (fiscal year − 1)
        fy = fd.year
        if fd.month in (1, 2, 3):
            fy -= 1
            q = 4
        elif fd.month in (4, 5, 6):
            q = 1
        elif fd.month in (7, 8, 9):
            q = 2
        else:
            q = 3
        return fy, f"Q{q}"


def fetch_filing_index_for_cik(
    cik: str,
    form_types: tuple[str, ...] = ("10-K", "10-Q"),
    max_count: int = 100,
) -> list[dict[str, str]]:
    """Return raw filing rows for a single CIK, across multiple form types."""
    all_rows: list[dict[str, str]] = []
    for form_type in form_types:
        url = (
            f"{BROWSE_EDGAR_URL}?action=getcompany"
            f"&CIK={cik}&type={form_type}&count={max_count}"
        )
        html_text = _http_get_text(url)
        rows = _parse_browse_table(html_text)
        for row in rows:
            row["cik"] = cik
        all_rows.extend(rows)
        time.sleep(_RATE_LIMIT_SEC)
    return all_rows


def build_filing_index(
    tickers: list[str],
    *,
    cik_map: dict[str, str] | None = None,
    form_types: tuple[str, ...] = ("10-K", "10-Q"),
    start_year: int = 2005,
    cache_dir: Path | None = None,
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Build a complete filing index for *tickers*.

    Returns ``(DataFrame, cik_map)`` where cik_map is ``{TICKER: cik10}``.
    """
    if cik_map is None:
        cik_map = fetch_company_tickers(
            cache_dir / "company_tickers.json" if cache_dir else None
        )

    tickers_upper = [t.upper() for t in tickers]
    missing = [t for t in tickers_upper if t not in cik_map]
    if missing:
        logger.warning("No CIK found for tickers: %s", ", ".join(missing))

    entries: list[dict[str, object]] = []
    request_count = 0

    for ticker in tickers_upper:
        cik = cik_map.get(ticker)
        if cik is None:
            continue

        logger.info("Scraping filing index for %s (CIK %s)", ticker, cik)
        rows = fetch_filing_index_for_cik(cik, form_types=form_types)
        for row in rows:
            fy, fp = _infer_fiscal_period(row["form_type"], row["filing_date"])
            if fy is not None and fy < start_year:
                continue
            entries.append(
                {
                    "ticker": ticker,
                    "cik": cik,
                    "accession": row["accession"],
                    "form_type": row["form_type"],
                    "filing_date": row["filing_date"],
                    "fiscal_year": fy,
                    "fiscal_period": fp,
                    "index_url": row["index_url"],
                }
            )
            request_count += 1
            if request_count % _BATCH_SIZE == 0:
                logger.debug("Pausing after %d requests", request_count)
                time.sleep(_BATCH_PAUSE_SEC)

    df = pd.DataFrame(entries)
    if not df.empty:
        df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
        df = df.sort_values(["ticker", "fiscal_year", "fiscal_period"], ascending=[True, False, False]).reset_index(drop=True)

    logger.info("Filing index built: %d rows for %d tickers", len(df), df["ticker"].nunique() if not df.empty else 0)
    return df, cik_map


# ---------------------------------------------------------------------------
# Document index page parsing
# ---------------------------------------------------------------------------


def _parse_document_index(html_text: str) -> dict[str, str]:
    """Parse the filing index page (-index.htm) to find the primary document.

    Returns ``{"doc_url": ..., "doc_filename": ...}`` for the first row
    (Seq=1) in the <table class="tableFile">, which is always the primary
    filing document.
    """
    table_match = re.search(
        r'<table[^>]*class="tableFile"[^>]*>(.*?)</table>',
        html_text,
        re.DOTALL,
    )
    if not table_match:
        raise ValueError("Could not find tableFile in document index page")

    table = table_match.group(1)
    # Find the first data row (not header <th>)
    tr_blocks = re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.DOTALL)
    for tr in tr_blocks:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)
        if len(tds) < 4:
            continue
        # First td is sequence number; 3rd td has the document link
        seq = re.sub(r"<[^>]+>", "", tds[0]).strip()
        if seq != "1":
            continue
        doc_cell = tds[2]
        href_match = re.search(r'href="([^"]+)"', doc_cell)
        if not href_match:
            raise ValueError("No document href in first tableFile row")
        href = href_match.group(1)
        # Handle iXBRL viewer links: /ix?doc=/Archives/edgar/data/.../file.htm
        if href.startswith("/ix?doc="):
            href = href[len("/ix?doc="):]
        filename = href.rsplit("/", 1)[-1]
        doc_url = f"{BASE_URL}{href}" if href.startswith("/") else href
        return {"doc_url": doc_url, "doc_filename": filename}

    raise ValueError("No Seq=1 document row in tableFile")


def resolve_document_url(index_url: str) -> dict[str, str]:
    """Fetch a filing index page and return the primary document URL + filename."""
    html_text = _http_get_text(index_url)
    time.sleep(_RATE_LIMIT_SEC)
    return _parse_document_index(html_text)


# ---------------------------------------------------------------------------
# Text extraction from iXBRL / HTML filings
# ---------------------------------------------------------------------------


def _clean_xbrl_text(html_text: str) -> str:
    """Convert an iXBRL / HTML filing into readable plain text."""
    # 1. Remove the <ix:header> block (XBRL metadata, references, contexts)
    text = re.sub(r"<ix:header>.*?</ix:header>", "", html_text, flags=re.DOTALL)

    # 2. Remove <script> and <style> blocks
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # 3. Remove entire <head> section
    text = re.sub(r"<head[^>]*>.*?</head>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # 4. Remove all remaining HTML tags (but keep their inner text)
    text = re.sub(r"<[^>]+>", " ", text)

    # 5. Decode HTML entities
    text = html_mod.unescape(text)

    # 6. Remove zero-width and other invisible characters
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u200b-\u200f\u2028-\u202f\u00a0]", " ", text)

    # 7. Collapse runs of whitespace into single spaces
    text = re.sub(r"\s+", " ", text)

    # 8. Split into lines at natural paragraph boundaries
    #    Look for places where there were block-level elements
    lines = [line.strip() for line in text.split("\n")]
    # Further split on double+ space clusters that likely mark paragraph breaks
    refined: list[str] = []
    for line in lines:
        # Split on 3+ spaces (common paragraph separators in stripped HTML)
        parts = re.split(r"\s{3,}", line)
        refined.extend(p.strip() for p in parts if p.strip())

    # Remove empty lines, join with double newlines for readability
    return "\n\n".join(line for line in refined if line)


def extract_filing_text(html_path: Path) -> str:
    """Read a downloaded HTML filing and return cleaned plain text."""
    html_text = html_path.read_text(encoding="utf-8", errors="replace")
    return _clean_xbrl_text(html_text)



# ---------------------------------------------------------------------------
# Section extraction
# ---------------------------------------------------------------------------

SECTION_SPEC = {
    "10-K": {
        "1":  {"find": r"ITEM\s+1[\.\s]|Item\s+1[\.\s]", "stop": r"ITEM\s+1A|Item\s+1A"},
        "1A": {"find": r"ITEM\s+1A[\.\s]|Item\s+1A[\.\s]", "stop": r"ITEM\s+1B|Item\s+1B|ITEM\s+2[\.\s]|Item\s+2[\.\s]"},
        "7":  {"find": r"ITEM\s+7[\.\s]|Item\s+7[\.\s]", "stop": r"ITEM\s+7A|Item\s+7A"},
        "7A": {"find": r"ITEM\s+7A[\.\s]|Item\s+7A[\.\s]", "stop": r"ITEM\s+8[\.\s]|Item\s+8[\.\s]"},
    },
    "10-Q": {
        "2":  {"find": r"ITEM\s+2[\.\s]|Item\s+2[\.\s]", "stop": r"ITEM\s+3[\.\s]|Item\s+3[\.\s]"},
        "3":  {"find": r"ITEM\s+3[\.\s]|Item\s+3[\.\s]", "stop": r"ITEM\s+4[\.\s]|Item\s+4[\.\s]"},
    },
    "20-F": {
        "4":  {"find": r"ITEM\s+4[\.\s]|Item\s+4[\.\s]", "stop": r"ITEM\s+4A|Item\s+4A|ITEM\s+5[\.\s]|Item\s+5[\.\s]"},
        "5":  {"find": r"ITEM\s+5[\.\s]|Item\s+5[\.\s]", "stop": r"ITEM\s+6[\.\s]|Item\s+6[\.\s]"},
        "11": {"find": r"ITEM\s+11[\.\s]|Item\s+11[\.\s]", "stop": r"ITEM\s+12[\.\s]|Item\s+12[\.\s]"},
    },
}


def extract_section(text: str, form_type: str, item_id: str, min_chars: int = 300) -> str | None:
    """Extract a numbered section (Item 1, 7A, etc.) from EDGAR filing text.

    Picks the match with the most content to skip table-of-contents entries.
    Returns *None* if no matching section is found.
    """
    import re as _re
    spec = SECTION_SPEC.get(form_type, {}).get(item_id)
    if spec is None:
        return None

    candidates: list[tuple[int, str]] = []

    for m in _re.finditer(spec["find"], text):
        start = m.start()
        # Find next section boundary
        for sm in _re.finditer(spec["stop"], text[start + 10:]):
            end = start + 10 + sm.start()
            break
        else:
            end = min(len(text), start + 100_000)

        content_slice = text[start:end]
        if len(content_slice) >= min_chars:
            candidates.append((start, content_slice))

    if not candidates:
        return None

    # Pick the latest-in-document match that is not absurdly large
    # (mid-document references can span hundreds of KB before the next section).
    # A well-bounded section should exist; prefer the one that starts latest
    # among those with reasonable size (< 100 KB or not 3x larger than the
    # shortest well-bounded candidate).
    if len(candidates) >= 2:
        sizes = [len(c) for _, c in candidates]
        min_size = min(sizes)
        # Filter: keep only candidates not more than 5x the minimum size
        reasonable = [(pos, c) for pos, c in candidates if len(c) <= max(min_size * 5, 50_000)]
        if reasonable:
            # Pick the one that starts latest in the document
            return max(reasonable, key=lambda x: x[0])[1]
        # Fallback: pick latest
        return max(candidates, key=lambda x: x[0])[1]
    return candidates[0][1]


def extract_form_sections(
    text: str,
    form_type: str,
    *,
    item_ids: tuple[str, ...] | None = None,
    min_chars: int = 300,
) -> dict[str, str]:
    """Return ``{item_id: content}`` for all applicable sections of *form_type*."""
    ids = item_ids or tuple(SECTION_SPEC.get(form_type, {}).keys())
    out: dict[str, str] = {}
    for item_id in ids:
        content = extract_section(text, form_type, item_id, min_chars=min_chars)
        if content is not None:
            out[item_id] = content
    return out

# ---------------------------------------------------------------------------
# Filing download orchestration
# ---------------------------------------------------------------------------


def _accession_clean(accession: str) -> str:
    """Remove hyphens from accession number for archive URL path."""
    return accession.replace("-", "")


def download_one_filing(entry: FilingEntry, output_path: Path) -> bool:
    """Download and clean one EDGAR filing.

    Returns True on success, False if the filing was already cached or failed.
    """
    if output_path.exists():
        logger.debug("%s already exists, skipping", output_path.name)
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Resolve document URL if not already known
    if entry.doc_url is None:
        try:
            info = resolve_document_url(entry.index_url)
            entry = FilingEntry(
                ticker=entry.ticker,
                cik=entry.cik,
                accession=entry.accession,
                form_type=entry.form_type,
                filing_date=entry.filing_date,
                fiscal_year=entry.fiscal_year,
                fiscal_period=entry.fiscal_period,
                index_url=entry.index_url,
                doc_url=info["doc_url"],
                doc_filename=info["doc_filename"],
            )
        except Exception:
            logger.warning("Failed to resolve doc URL for %s %s", entry.ticker, entry.accession)
            return False

    if entry.doc_url is None:
        return False

    # Download the filing
    try:
        logger.debug("Downloading %s -> %s", entry.doc_url, output_path)
        html_bytes = _http_get(entry.doc_url, timeout=60)
        time.sleep(_RATE_LIMIT_SEC)
    except Exception:
        logger.warning("Failed to download %s", entry.doc_url)
        return False

    # Write raw HTML to a temp location
    raw_path = output_path.with_suffix(".raw.html")
    raw_path.write_bytes(html_bytes)

    # Extract text
    try:
        html_text = html_bytes.decode("utf-8", errors="replace")
        clean = _clean_xbrl_text(html_text)
    except Exception:
        logger.warning("Failed to extract text from %s", raw_path)
        clean = ""

    if not clean or len(clean) < 500:
        logger.warning("Extracted text for %s is too short (%d chars), may be binary/PDF filing",
                       output_path.name, len(clean))

    output_path.write_text(clean, encoding="utf-8")
    # Remove raw HTML after successful extraction to save disk
    raw_path.unlink(missing_ok=True)
    return True


def download_filings(
    index: pd.DataFrame,
    output_dir: Path,
    *,
    form_types: tuple[str, ...] = ("10-K", "10-Q"),
    dry_run: bool = False,
) -> dict[str, int]:
    """Download and extract filings from *index* into *output_dir*.

    Directory layout::

        output_dir/
          filings/
            AAPL/
              10-K/
                2025.txt
                2024.txt
              10-Q/
                2025-Q1.txt
                ...

    Returns ``{"downloaded": N, "skipped": N, "would_download": N,
    "failed": N}``.
    """
    stats = {"downloaded": 0, "skipped": 0, "would_download": 0, "failed": 0}
    filings_dir = output_dir / "filings"

    if index.empty:
        logger.warning("Empty index; nothing to download")
        return stats

    for _, row in index.iterrows():
        form = str(row["form_type"])
        # Only handle exact requested forms. Amendments such as 10-K/A remain
        # in the index but are not downloaded into the same fiscal filename.
        if form not in form_types:
            continue
        form_base = form.strip()

        ticker = str(row["ticker"])
        fy = row["fiscal_year"]
        fp = row.get("fiscal_period")

        if pd.isna(fy):
            continue

        fy = int(fy)
        fp_str = str(fp) if not pd.isna(fp) and fp else ""
        if fp_str in ("FY", ""):
            out_name = f"{fy}.txt"
        else:
            out_name = f"{fy}-{fp_str}.txt"

        output_path = filings_dir / ticker / form_base / out_name

        if output_path.exists():
            stats["skipped"] += 1
            continue

        if dry_run:
            stats["would_download"] += 1
            continue

        entry = FilingEntry(
            ticker=ticker,
            cik=str(row.get("cik", "")),
            accession=str(row["accession"]),
            form_type=form,
            filing_date=str(row["filing_date"]),
            fiscal_year=fy,
            fiscal_period=fp_str or None,
            index_url=str(row["index_url"]),
        )

        success = download_one_filing(entry, output_path)
        if success:
            stats["downloaded"] += 1
            logger.debug("Downloaded %s/%s/%s", ticker, form_base, out_name)
        else:
            stats["failed"] += 1

        if (stats["downloaded"] + stats["failed"]) % _BATCH_SIZE == 0:
            logger.info("Progress: %d downloaded, %d failed, %d skipped",
                        stats["downloaded"], stats["failed"], stats["skipped"])
            time.sleep(_BATCH_PAUSE_SEC)

    return stats
