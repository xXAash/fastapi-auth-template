from microservices.database import engine
from microservices.auth.models import Base

# This will create all tables defined using Base.metadata.create_all()
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
