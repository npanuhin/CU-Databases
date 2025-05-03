import random

from faker import Faker

from cloudflare_utils import run_query, batch_insert, clear_all_tables


fake = Faker()

NUM_PLAYERS = 10
NUM_GAMES = 100


TILES = [
    # Man (characters)
    '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
    # Pin (dots)
    '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
    # Sou (bamboo)
    '1b', '2b', '3b', '4b', '5b', '6b', '7b', '8b', '9b',
    # Winds
    'E', 'S', 'W', 'N',
    # Dragons
    'C', 'B', 'D'
]

YAKUS = [
    ('Riichi', 1, True, 'Declared Riichi'),
    ('Tanyao', 1, False, 'All simples'),
    ('Pinfu', 1, False, 'No points for hand'),
    ('Honitsu', 3, False, 'One suit and honor tiles'),
    ('Iipeikou', 1, True, 'Single Identical Sequence'),
    ('SanshokuDoujun', 2, False, 'Three Color Sequence'),
    ('Ikkitsuukan', 2, False, 'Full Straight'),
    ('Ryanpeikou', 3, False, 'Double Identical Sequences'),
    ("Hon'itsu", 3, False, 'Half Flush'),
    ("Chin'itsu", 6, False, 'Full Flush'),
    ('Toitoi', 2, False, 'All Triplets'),
    ('Sanankou', 2, True, 'Three Concealed Triplets'),
    ('SanshokuDoukou', 2, False, 'Mixed Triplets'),
    ('Sankantsu', 2, False, 'Three Quads'),
    ('Yakuhai', 1, False, 'Honor Tiles'),
    ('Honroutou', 2, False, 'All Terminals'),
    ('Shousangen', 2, False, 'Little Three Dragons'),
    ('Daisangen', 13, False, 'Big Three Dragons'),
    ('Tsuuisou', 13, False, 'All Honors'),
    ('Chinroutou', 13, False, 'Pure Terminal Hand'),
    ('KokushiMusou', 13, False, 'Thirteen Orphans'),
    ('Suuankou', 13, False, 'Four Concealed Triplets'),
    ('DaisuuShii', 13, False, 'Big Four Winds'),
    ('Chinshouko', 6, False, 'Pure Straight'),
    ('Sankou', 2, False, '3 Concealed Pungs'),
    ('Tsumo', 1, False, 'Self-Drawn'),
    ('Ippatsu', 1, False, 'One-Shot'),
    ('HaiteiRaoyue', 1, False, 'Last Tile Draw'),
    ('HouteiRaoyui', 1, False, 'Last Tile Claim'),
    ('RinshanKaihou', 1, False, 'Dead Wall Draw'),
    ('Chankan', 1, False, 'Robbing a Kong'),
    ('Chiitoitsu', 2, False, 'Seven Pairs'),
    ('AkaDora', 1, False, 'Red Dora'),
    ('UraDora', 1, False, 'Uradora'),
]


def generate_players(n: int) -> list[tuple[str, str, int, str]]:
    players = []
    for _ in range(n):
        username = fake.unique.user_name()
        display_name = fake.name()
        rating = random.randint(1200, 1800)
        country = fake.country()
        players.append((username, display_name, rating, country))
    return players


def generate_games(player_ids: list[int], n: int) -> list[tuple[str, str | None, int, str, int]]:
    games = []
    for _ in range(n):
        start_time = fake.date_this_year().isoformat()
        end_time = fake.date_this_year().isoformat() if random.choice([True, False]) else None
        winner_id = random.choice(player_ids)
        wind = random.choice(['East', 'South'])
        dealer_id = random.choice(player_ids)
        games.append((start_time, end_time, winner_id, wind, dealer_id))
    return games


def generate_player_statuses(game_ids: list[int], player_ids: list[int]) -> list[tuple[int, int, str, int, bool]]:
    player_statuses = []
    winds = ['East', 'South', 'West', 'North']
    for game_id in game_ids:
        for player_id in player_ids:
            wind = random.choice(winds)
            cur_score = random.randint(-30000, 100000)
            declared_riichi = random.choice([True, False])
            player_statuses.append((game_id, player_id, wind, cur_score, declared_riichi))
    return player_statuses


def generate_player_yakus(player_status_ids: list[int], yaku_ids: list[int]) -> list[tuple[int, int]]:
    player_yakus = []
    for status in player_status_ids:
        if random.choice([True, False]):  # Player can either have a yaku or not (not winning)
            yaku = random.choice(yaku_ids)
            player_yakus.append((status, yaku))
    return player_yakus


def generate_hand_tiles(player_status_ids: list[int], tile_ids: list[int]) -> list[tuple[int, int, bool, int]]:
    hand_tiles = []
    for status in player_status_ids:
        for pos in range(14):
            tile = random.choice(tile_ids)
            is_in_meld = random.choice([True, False])
            hand_tiles.append((status, tile, is_in_meld, pos))
    return hand_tiles


# ======================================================================================================================

def main():
    print('Clearing all tables...')
    clear_all_tables()

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting tiles...')
    sql = 'INSERT INTO tiles (tile_code) VALUES {}'
    batch_insert(sql, [[tile] for tile in TILES])

    tile_ids = [row['id'] for row in run_query('SELECT id FROM tiles')]

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting yakus...')
    sql = 'INSERT INTO yaku (name, han_value, menzenchin_only, description) VALUES {}'
    batch_insert(sql, YAKUS)

    yaku_ids = [row['id'] for row in run_query('SELECT id FROM yaku')]

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting players...')
    sql = 'INSERT INTO players (username, display_name, rating, country) VALUES {}'
    batch_insert(sql, generate_players(NUM_PLAYERS))

    username_to_id = {row['username']: row['id'] for row in run_query('SELECT id, username FROM players')}

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting games...')
    sql = 'INSERT INTO games (start_time, end_time, winner_id, wind, dealer_id) VALUES {}'
    batch_insert(sql, generate_games(list(username_to_id.values()), NUM_GAMES))

    game_ids = [row['id'] for row in run_query('SELECT id FROM games')]

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting player statuses...')
    sql = 'INSERT INTO player_status (game_id, player_id, wind, cur_score, declared_riichi) VALUES {}'
    batch_insert(sql, generate_player_statuses(game_ids, list(username_to_id.values())))

    player_status_ids = [row['id'] for row in run_query('SELECT id FROM player_status')]

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting player yakus...')
    sql = 'INSERT INTO player_yakus (player_status_id, yaku_id) VALUES {}'
    batch_insert(sql, generate_player_yakus(player_status_ids, yaku_ids))

    # ------------------------------------------------------------------------------------------------------------------

    print('Inserting hand tiles...')
    sql = 'INSERT INTO hand_tile (player_status_id, tile_id, is_in_meld, position) VALUES {}'
    batch_insert(sql, generate_hand_tiles(player_status_ids, tile_ids))


if __name__ == '__main__':
    main()
