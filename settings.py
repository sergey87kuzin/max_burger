import os
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

REAL_DATABASE_URL = os.getenv(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://sergey:11@localhost:5432/maxburger",
)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://sergey:11@localhost:5432/maxburger_test",
)
