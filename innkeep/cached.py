from innkeep.hearthstone import (
    Cards,
)

CARDS = None

def refresh():
    """
    Refresh the cache.
    """
    global CARDS

    print('Rebuilding cache...')

    try:
        card_resp = Cards().all()
    except Exception:
        print('NetrunnerDB requests failed. Aborting cache refresh.')
        return

    CARDS = {c['name']: c for c in card_resp if 'name' in c and c.get('collectible')}
    print('Cache rebuilt')

refresh()
