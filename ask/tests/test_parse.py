from ..parse import parse


def test_extract_code_block():
    markdown = """
Hello

```html
<html></html>
```
        """
    assert parse(markdown) == [("html", "<html></html>")]
