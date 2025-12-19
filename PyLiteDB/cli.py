# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import sys
from .engine import Database
from .parser import Parser

def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    path = argv[0] if len(argv) > 0 else "pylitedb.db"
    passphrase = argv[1] if len(argv) > 1 else None
    db = Database(path, passphrase)
    p = Parser()
    try:
        while True:
            line = input("pylite> ").strip()
            if not line:
                continue
            if line.lower() in {"quit", "exit"}:
                break
            cmd = line.strip().split()[0].upper()

            if cmd == "CREATE":
                name, _ = p.parse_create(line)
                db.create_table(name)
                print(f"Created table '{name}'")

            elif cmd == "INSERT":
                name, payload = p.parse_insert(line)
                rid = db.insert(name, payload)
                print(f"Inserted row ID: {rid}")

            elif cmd == "SELECT":
                name, _ = p.parse_select(line)
                rows = db.find_all(name)
                for r in rows:
                    print(r)

            elif cmd == "UPDATE":
                name, rid, payload = p.parse_update(line)
                ok = db.update(name, rid, payload)
                print("Updated successfully" if ok else "Update failed")

            elif cmd == "DELETE":
                name, rid = p.parse_delete(line)
                ok = db.delete(name, rid)
                print("Deleted successfully" if ok else "Delete failed")

            elif cmd == "FILTER":
                 name, key, value = p.parse_filter(line)
                 results = db.find_by_filter(name, key, value)
                 for r in results:
                      print(r)
            else:
                print("Unknown command. Supported: CREATE, INSERT, SELECT, UPDATE, DELETE, FILTER, EXIT")

    except (EOFError, KeyboardInterrupt):
        return 0
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
