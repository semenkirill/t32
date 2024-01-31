```bash
 pyinstaller -y --clean  --hidden-import=asyncpg.pgproto.pgproto  --additional-hooks-dir extra-hooks main.py --onefile
```