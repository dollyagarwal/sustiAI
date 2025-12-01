__version__ = '0.1.0'

# Load environment variables early so submodules (agents / ADK clients)
# can pick up values like GOOGLE_API_KEY from a local .env file.
try:
	# prefer python-dotenv when available and be defensive so tests don't fail
	# if the package isn't installed in minimal environments.
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	# If python-dotenv isn't installed, rely on the environment already being
	# configured by the caller. Keep imports quiet for test/CI environments.
	pass

from .db import get_db_connection, query, apply_ddl_and_mockdata

__all__ = ['get_db_connection', 'query', 'apply_ddl_and_mockdata']
