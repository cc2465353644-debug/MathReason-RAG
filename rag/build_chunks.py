from pathlib import Path
import json


KNOWLEDGE_DIR = Path("data/knowledge_base")
OUTPUT_FILE = Path("data/chunks.jsonl")


def read_markdown_files():
    md_files = sorted(KNOWLEDGE_DIR.glob("*.md"))
    documents = []

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")

        documents.append({
            "source": md_file.name,
            "content": content
        })

    return documents


def split_markdown_by_headings(content):
    """
    简单按照二级标题 ## 切分 Markdown。
    这是 v0.1 版本，不追求完美，先保证能跑。
    """
    parts = content.split("\n## ")
    chunks = []

    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue

        if i == 0:
            chunks.append(part)
        else:
            chunks.append("## " + part)

    return chunks


def build_chunks():
    documents = read_markdown_files()
    all_chunks = []

    for doc in documents:
        source = doc["source"]
        content = doc["content"]

        title = content.split("\n")[0].replace("#", "").strip()
        chunks = split_markdown_by_headings(content)

        for idx, chunk in enumerate(chunks, start=1):
            chunk_data = {
                "chunk_id": f"{source.replace('.md', '')}_{idx:03d}",
                "source": source,
                "title": title,
                "content": chunk
            }
            all_chunks.append(chunk_data)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Built {len(all_chunks)} chunks.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    build_chunks()
