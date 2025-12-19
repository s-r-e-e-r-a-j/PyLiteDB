## PyLiteDB

**PyLiteDB** is a small, lightweight database engine written in Python. It stores data as JSON-like records. You can store, update, get, and delete records in tables. It also supports optional encryption to keep your data safe.

## Features:

- Create tables and store JSON-like data

- Insert, update, delete, and fetch records by ID

- Get all records from a table

- Filter records using a key and value

- Optional AES-GCM encryption with SHA3-based keys
  
- A salt file (`.salt`) is used to help with encryption and decryption
  

- Write-Ahead Logging (WAL) for crash-safe operations

- Metadata stored in `.meta.json` files
  
- Includes an easy-to-use CLI mode for managing databases

## Installation:
**Ensure that Python 3.10 or newer is installed on your system.**

**You can install PyLiteDB using pip or pip3:**
```bash
pip3 install pylitedb-engine
# or
pip install pylitedb-engine
```

## Usage Example

```python
from PyLiteDB import Database

# Create or open database with optional passphrase
db = Database("test.db", "mypassword")

# Create a table
db.create_table("users")

# Insert records
uid1 = db.insert("users", {"name": "Sreeraj", "age": 21})
uid2 = db.insert("users", {"name": "Sreereshmi", "age": 17})
uid3 = db.insert("users", {"name": "Alex", "age": 25})

# Fetch a record by ID
record = db.get("users", uid1)
print("Single record:", record)

# Access single pieces of data from the record
print("Name:", record["name"])
print("Age:", record["age"])

# Update a record
# You can change existing fields or add new ones
db.update("users", uid1, {
    "name": "Sreekuttan",
    "role": "developer",
    "email": "sreekuttan@example.com"
})

# Fetch the updated record to confirm changes
updated_record = db.get("users", uid1)
print("\nUpdated record:", updated_record)

# Delete a record
db.delete("users", uid2)

# Fetch all records
all_records = db.find_all("users")
print("\nAll records:", all_records)

# Filter records by key/value
filtered = db.find_by_filter("users", "name", "Alex")
print("\nFiltered (name='Alex'):", filtered)

# Accessing filtered data
if filtered:
    # Print entire row of filtered data
    print("\nFiltered row:", filtered)
    
    # Print single pieces of data from filtered
    print("Filtered name:", filtered[0]["name"])
    print("Filtered age:", filtered[0]["age"])

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
python3 -m PyLiteDB
```
This command will open the PyLiteDB shell with a new or existing database named `pylitedb.db` (unencrypted by default).

If you want to use a specific database file **with encryption enabled**, provide a passphrase:
```bash
python3 -m PyLiteDB mydatabase.db mysecret
```

If the database file (`mydatabase.db`) does not exist, it will be created automatically.

If the file already exists, the same passphrase used during creation must be provided to access it.

If no passphrase is provided, the database will operate in **unencrypted mode**.

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

### Using the CLI Programmatically (Inside a Python Script)

You can also run the PyLiteDB CLI directly from a Python file by importing it:
```python
from PyLiteDB.cli import main

# Example 1: Run with the default database (unencrypted)
main([])

# Example 2: Run with a specific database file (unencrypted)
main(["mydatabase.db"])

# Example 3: Run with encryption using a passphrase
main(["mydatabase.db", "mysecret"])
```

This is useful when you want to embed the interactive PyLiteDB shell inside another Python-based project or provide a scripted interface for database management.

## Notes:

- Always use the Database API, do not edit `.db`, `.meta.json` or `.salt` manually.

- Encryption works only if you provide a passphrase.

## License
This project is licensed under the MIT License
