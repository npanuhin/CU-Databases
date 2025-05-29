from cloudflare_utils import run_query


def get_top_winner():
    sql = """
        SELECT p.username, p.display_name, COUNT(g.id) AS win_count
        FROM games g
        JOIN players p ON g.winner_id = p.id
        GROUP BY g.winner_id
        ORDER BY win_count DESC
        LIMIT 1;
    """
    result = run_query(sql)[0]
    print(
        f'Top winner: Username: '
        f'{result["username"]}, Display name: {result["display_name"]}, Wins: {result["win_count"]}'
    )


def get_most_common_yaku():
    sql = """
        SELECT y.name, COUNT(py.id) AS count
        FROM player_yaku py
        JOIN yaku y ON py.yaku_id = y.id
        GROUP BY py.yaku_id
        ORDER BY count DESC
        LIMIT 5;
    """
    result = run_query(sql)
    print('Top 5 most common Yaku:')
    for row in result:
        print(f'{row["name"]}: {row["count"]} times')


def get_most_common_tiles():
    sql = """
        SELECT ht.tile_code, COUNT(*) AS usage_count
        FROM hand_tile ht
        GROUP BY ht.tile_code
        ORDER BY usage_count DESC
        LIMIT 10;
    """
    result = run_query(sql)
    print('Top 10 most used tiles:')
    for row in result:
        print(f'{row["tile_code"]}: {row["usage_count"]} times')


def get_most_common_meld_tiles():
    sql = """
        SELECT ht.tile_code, COUNT(*) AS meld_count
        FROM hand_tile ht
        WHERE ht.is_in_meld == "true"
        GROUP BY ht.tile_code
        ORDER BY meld_count DESC
        LIMIT 10;
    """
    result = run_query(sql)
    print('Top 10 tiles used in melds:')
    for row in result:
        print(f'{row["tile_code"]}: {row["meld_count"]} times')


def main():
    get_top_winner()
    print()
    get_most_common_yaku()
    print()
    get_most_common_tiles()
    print()
    get_most_common_meld_tiles()


if __name__ == '__main__':
    main()
