# movienator_server
## INITIALIZE
fetch data
```bash
mkdir data
python fetch.py
```

initialize db
```bash
rm data/database.db
sqlite3 data/database.db < database.sql
python create_db.py 
```