import re


def sanitize_md(raw_content: str) -> str:
    

    if raw_content.startswith("markdown\\n"):
        raw_content = raw_content[len("markdown\\n"):]

    elif raw_content.startswith("markdown\n"):
        raw_content = raw_content[len("markdown\n"):]

    raw_content = re.sub(r"^```markdown\s*", "", raw_content)
    raw_content = re.sub(r"^```\s*", "", raw_content)
    raw_content = re.sub(r"\n*```[\s]*$", "", raw_content)

    raw_content = raw_content.replace("\\n", "\n")

    try:
        raw_content = raw_content.encode("latin1").decode("utf-8")
    except Exception:
        pass

    sanitized_md = raw_content.strip()


    return sanitized_md
