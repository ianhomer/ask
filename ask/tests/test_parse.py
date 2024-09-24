from ..parse import parse_markdown_for_code_blocks


def test_extract_code_block():
    markdown = """
Hello

```html
<html></html>
```
        """
    assert parse_markdown_for_code_blocks(markdown) == [("html", "<html></html>")]
