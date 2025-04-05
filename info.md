you need to modify:
`venv/lib/python3.11/site-packages/gradio_client/utils.py`
In line 897:
you need to add

```
if isinstance(schema, bool):
		return "boolean"
```

```
def get_type(schema: dict):
    if isinstance(schema, bool):
        return "boolean"
    if "const" in schema:
```

docker run --rm \
 -d -p 8080:8080 \
 -v "${PWD}/searxng:/etc/searxng" \
 -e "BASE_URL=http://localhost:8080/" \
 -e "INSTANCE_NAME=my-instance" \
 -e "UWSGI_WORKERS=8" \
 searxng/searxng
