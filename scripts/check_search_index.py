#!/usr/bin/env python3
"""Guard the built search index against silent breakage.

Two failure modes this catches, both of which build fine but leave the search
box returning zero results:

1. Material issues search queries as prefix wildcards (``scheduling*``), and
   wildcard clauses bypass the search pipeline. If the index pipeline stems
   tokens (the ``zh`` locale ships ``search.config.pipeline: "stemmer"``), the
   index stores ``schedul`` while the query asks for ``scheduling*`` — so every
   stemmed word silently disappears. ``mkdocs.yml`` pins ``pipeline: []``.

2. Chinese is only segmented when the optional ``jieba`` dependency is
   installed. Without it the whole sentence is one token, so any Chinese
   query misses. ``requirements.txt`` pins jieba.

Run after ``mkdocs build`` (reads ``site/search/search_index.json``).
"""

import json
import sys
from pathlib import Path

INDEX = Path("site/search/search_index.json")


def fail(message: str) -> None:
    print(f"SEARCH INDEX CHECK FAILED: {message}")
    sys.exit(1)


def main() -> None:
    if not INDEX.exists():
        fail(f"{INDEX} not found — run `mkdocs build` first")

    data = json.loads(INDEX.read_text(encoding="utf-8"))
    config = data["config"]
    docs = data["docs"]

    # 1. No pipeline function may transform indexed terms.
    pipeline = config.get("pipeline") or []
    if pipeline:
        fail(
            f"search pipeline {pipeline} transforms tokens, but queries are "
            "prefix wildcards that bypass the pipeline, so transformed words "
            "become unsearchable — keep `pipeline: []` in mkdocs.yml"
        )

    # 2. jieba must be installed for Chinese segmentation.
    try:
        import jieba  # noqa: F401
    except ImportError:
        fail(
            "jieba is not installed — Chinese text will not be segmented; "
            "add it to requirements.txt / install requirements"
        )

    # 3. Segmentation must actually be present in the generated index.
    segmented = sum(1 for doc in docs if "\u200b" in doc.get("text", ""))
    if segmented == 0:
        fail(
            "no zero-width-space segmentation in any document — jieba did "
            "not run while building the index"
        )

    # 4. Spot-check that a common Chinese query term is a standalone token.
    marker = "\u200b调度\u200b"
    if not any(marker in doc.get("text", "") for doc in docs):
        fail(f"expected segmented token {marker!r} not found in the index")

    # 5. Spot-check that an English stemmed word survived intact.
    async_docs = [
        doc for doc in docs
        if doc.get("location", "").startswith("engine-args/async-scheduling/")
    ]
    if not async_docs or "scheduling" not in async_docs[0].get("text", ""):
        fail(
            "expected unstemmed token 'scheduling' on the async-scheduling "
            "page — stemming appears to be active again"
        )

    # 6. Both locales must be represented.
    if not any(doc.get("location", "").startswith("en/") for doc in docs):
        fail("no English documents in the index (i18n build may have failed)")

    print(
        "SEARCH INDEX OK: pipeline empty, {n}/{total} docs segmented with "
        "jieba, zh + en present".format(n=segmented, total=len(docs))
    )


if __name__ == "__main__":
    main()
