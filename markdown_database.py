import sqlite3
import re
from datetime import datetime

# Connect to your SQLite database
conn = sqlite3.connect('knowledge_base.db')
cursor = conn.cursor()

# Get all rows with content
cursor.execute("SELECT id, content FROM markdown_chunks")
rows = cursor.fetchall()

# Pattern to extract metadata
pattern = r'---title: "(.*?)" original_url: "(.*?)" downloaded_at: "(.*?)" ---'

for row in rows:
    row_id, content = row
    match = re.search(pattern, content)

    if match:
        doc_title = match.group(1)
        original_url = match.group(2)
        downloaded_at = match.group(3)

        # Optional: convert to datetime object
        try:
            downloaded_at_dt = datetime.fromisoformat(downloaded_at)
        except ValueError:
            downloaded_at_dt = None

        # Update the row with extracted values
        cursor.execute("""
            UPDATE markdown_chunks
            SET doc_title = ?, original_url = ?, downloaded_at = ?
            WHERE id = ?
        """, (doc_title, original_url, downloaded_at, row_id))

# Save changes and close connection
conn.commit()
conn.close()
