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
test.db           # Stores the main database data
test.meta.json    # Stores table metadata
test.db.wal       # Write-Ahead Log for crash recovery
test.salt         # Stores the cryptographic salt used for encryption
```

## Usage(CLI Mode) 

You can start the interactive PyLiteDB shell using:
```bash
python3 -m PyLiteDB.cli
```
or (if you have a specific database file and passphrase):
```bash
python3 -m PyLiteDB.cli mydatabase.db mysecret
```
Once started, you’ll see the prompt:
```bash
pylite>
```

### Supported CLI Commands

| Command                                   | Description                                                          |
|-------------------------------------------|----------------------------------------------------------------------|
| `CREATE TABLE <name>`                     | Create a new table in the database.                                  |
| `INSERT INTO <table> VALUES <json>`       | Insert a JSON-formatted record into the specified table.             |
| `SELECT * FROM <table>`                   | Display all records from the specified table.                        |
| `UPDATE <table> <row_id> <json>`          | Update the record with the given row ID in the specified table.      |
| `DELETE <table> <row_id>`                 | Delete the record with the given row ID from the specified table.    |
| `FILTER <table> <key>=<value>`            | Display records where the given key matches the specified value.     |
| `EXIT` or `QUIT`                          | Exit the PyLiteDB interactive shell.                                 |

### Example Session 
```bash
pylite> CREATE TABLE users
Created table 'users'
pylite> INSERT INTO users VALUES{"name":"sreeraj","age":21}
Inserted row ID: c75ad045fbd449be9591ddab93fe204a
pylite> SELECT * FROM users
{'name': 'sreeraj', 'age': 21}
pylite> UPDATE users c75ad045fbd449be9591ddab93fe204a {"name":"sreereshmi","age":17}
Updated successfully
pylite> SELECT * FROM users
{'name': 'sreereshmi', 'age': 17}
pylite> UPDATE users c75ad045fbd449be9591ddab93fe204a {"name":"sreeraj","age":21,"role":"developer"}
Updated successfully
pylite> SELECT * FROM users
{'name': 'sreeraj', 'age': 21, 'role': 'developer'}
pylite> FILTER users name=sreeraj
{'name': 'sreeraj', 'age': 21, 'role': 'developer'}
pylite> DELETE users c75ad045fbd449be9591ddab93fe204a
Deleted successfully
pylite> SELECT * FROM users
pylite> EXIT
```
## Notes:

- Always use the Database API; do not edit `.db` or `.meta.json` manually.

- Encryption works only if you provide a passphrase.

## License
This project is licensed under the MIT License
