
#!/usr/bin/env python3
from src.sustiai.db import apply_ddl_and_mockdata

if __name__ == '__main__':
    print('Creating SQLite DB: event_emissions.db')
    apply_ddl_and_mockdata()
    print('Done.')
