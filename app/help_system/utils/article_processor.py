from typing import List, Dict, Any


def ensure_article_integrity(data: List[Dict[str, Any]], title: str = "Untitled") -> List[Dict[str, Any]]:
    """
    Enforces structural rules for help articles:
    1. Must start with a 'title' block.
    2. Moves existing title block to start if found elsewhere.
    3. Converts first header to title if no title block exists.
    """
    if not data:
        return [{"type": "title", "content": title}]

    # Check if first block is title
    if data[0].get("type") == "title":
        return data

    # Check if title exists elsewhere and move it to front
    title_idx = -1
    for i, block in enumerate(data):
        if block.get("type") == "title":
            title_idx = i
            break

    if title_idx != -1:
        title_block = data.pop(title_idx)
        data.insert(0, title_block)
    else:
        # Try to convert first header to title
        header_idx = -1
        for i, block in enumerate(data):
            if block.get("type") == "header":
                header_idx = i
                break

        if header_idx != -1:
            header_block = data.pop(header_idx)
            header_block["type"] = "title"
            data.insert(0, header_block)
        else:
            # Add a title block at the start
            data.insert(0, {"type": "title", "content": title})

    return data
