import os

if os.path.exists('storage_state.json'):
        if os.path.getsize('storage_state.json') > 0:
            print('exist')