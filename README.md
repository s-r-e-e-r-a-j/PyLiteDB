## PyLiteDB

**PyLiteDB** is a small, lightweight database engine written in Python. It stores data as JSON-like records. You can store, update, get, and delete records in tables. It also supports optional encryption to keep your data safe.

## Features:

- Create tables and store JSON-like data

- Insert, update, delete, and fetch records by ID

- Get all records from a table

- Optional AES-GCM encryption with SHA3-based keys

- Write-Ahead Logging (WAL) for crash-safe operations

- Metadata stored in `.meta.json` files

## Installation / Setup:
**Ensure that Python 3.9 or newer is installed on your system.**
1. **Go to your project folder:**
```bash
cd /path/to/your/project
```
2. **Clone the PyLiteDB folder inside your project:**
```bash
git clone https://github.com/s-r-e-e-r-a-j/PyLiteDB.git
```
3. **Install the dependency for encryption:**
```bash
pip3 install cryptography
```
## Usage Example

```python
from PyLiteDB import Database

# Create/open database with optional passphrase
db = Database("test.db", "mypassword")  # passphrase optional

# Create a table
db.create_table("users")

# Insert records
uid1 = db.insert("users", {"name": "Sreeraj", "age": 21})
uid2 = db.insert("users", {"name": "Sreereshmi", "age": 17})

# Fetch a record
print(db.get("users", uid1))

# Update a record (change name or other fields)
db.update("users", uid1, {"name": "Sreekuttan", "role": "developer"})

# Delete a record
db.delete("users", uid2)

# Fetch all records
print(db.find_all("users"))

# Commit changes
db.commit()

```

## File Structure:
```bash
test.db         # stores the data
test.meta.json  # stores table metadata
.wal            # write-ahead log for crash recovery
```

## Notes:

- Always use the Database API; do not edit `.db` or `.meta.json` manually.

- Encryption works only if you provide a passphrase.

## License
This project is licensed under the MIT License
