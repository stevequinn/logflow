import secrets

from app.database import SessionLocal, engine
from models.orm import Base, Project


def init():
    # 1. Create Tables (Idempotent: won't recreate if they exist)
    print("Checking database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables verified.")

    # 2. Initialize Session
    db = SessionLocal()

    try:
        # 3. Check if we have any projects
        existing_project = db.query(Project).first()

        if not existing_project:
            print("No projects found. Creating default project...")

            # Generate a secure 32-character hex key
            new_api_key = secrets.token_hex(32)

            default_project = Project(
                name="default-project", api_key=new_api_key, is_active=True
            )

            db.add(default_project)
            db.commit()

            print("---------------------------------------------------------")
            print("SUCCESS: Default Project Created")
            print(f"Project Name: default-project")
            print(f"API KEY:      {new_api_key}")
            print("---------------------------------------------------------")
            print("Use this key in your X-API-Key header.")
        else:
            print(
                f"System already initialized. Existing Project: {existing_project.name}"
            )
            print(f"Existing Key (First 10 chars): {existing_project.api_key[:10]}...")

    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init()
