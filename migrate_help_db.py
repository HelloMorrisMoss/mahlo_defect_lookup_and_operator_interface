import sqlite3

from app import create_app
from app.extensions import db
from app.models import ContentVersion


def migrate():
    app = create_app()
    with app.app_context():
        # Get the engine for the help_system bind
        engine = db.get_engine(app, bind='help_system')
        db_url = str(engine.url)

        # SQLite URLs are typically sqlite:///path/to/db
        if db_url.startswith('sqlite:///'):
            db_path = db_url[10:]
        else:
            # Fallback for other URL formats if any
            db_path = engine.url.database

        print(f"Target database path: {db_path}")

        # Check if parent_id exists
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(content_versions)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'parent_id' not in columns:
            print("Adding parent_id column to content_versions table...")
            # In SQLite, we can just add the column.
            cursor.execute("ALTER TABLE content_versions ADD COLUMN parent_id INTEGER REFERENCES content_versions(id)")
            conn.commit()
        else:
            print("parent_id column already exists.")
        conn.close()

        # Update parent_id for existing records
        # Assuming linear history for existing versions as requested
        versions = ContentVersion.query.order_by(ContentVersion.id).all()
        updated = 0
        for i in range(1, len(versions)):
            if versions[i].parent_id is None:
                versions[i].parent_id = versions[i - 1].id
                updated += 1

        if updated > 0:
            db.session.commit()
            print(f"Updated {updated} records with parent_id.")
        else:
            print("No records needed parent_id update.")


if __name__ == "__main__":
    migrate()
