#!/bin/bash

# alembic init migrations

# sed -i "s#sqlalchemy.url = driver://user:pass@localhost/dbname#sqlalchemy.url = ${POSTGRES_HOST}#" alembic.ini
# sed -i "s#target_metadata = None#from models import Base\ntarget_metadata = Base.metadata#" migrations/env.py

# alembic revision --autogenerate -m "initial migration"
# alembic revision -m "initial migration"

# alembic upgrade head
# alembic upgrade $revision_id # upgrade to a specific revision

# alembic downgrade -1 # rollback one step
# alembic downgrade $revision_id