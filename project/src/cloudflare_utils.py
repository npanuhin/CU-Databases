import json

from cloudflare._types import NotGiven, NOT_GIVEN
from cloudflare import Cloudflare


with open('cloudflare-config.json', 'r') as file:
    CONFIG = json.load(file)

d1_client = Cloudflare(api_token=CONFIG['api_token'])


def run_query(sql: str, params: list[str] | NotGiven = NOT_GIVEN):
    try:
        response = d1_client.d1.database.query(
            database_id=CONFIG['database_id'],
            account_id=CONFIG['account_id'],
            sql=sql,
            params=params
        ).result[0]

        assert response.success

        return response.results

    except Exception as e:
        print(f'Error inserting batch: {e}')
        print(f'SQL: {sql}')
        print(f'Params: {params}')
        exit()


def batch_insert(sql_template: str, values: list[str], max_params_per_query: int = 100):
    if not values:
        return

    num_columns = len(values[0])

    rows_per_query = max_params_per_query // num_columns

    for i in range(0, len(values), rows_per_query):
        batch = values[i:i + rows_per_query]
        placeholders = ', '.join(['(' + ', '.join(['?'] * num_columns) + ')'] * len(batch))
        params = [item for row in batch for item in row]

        print(f'Batch-inserting {i}/{len(values)} values...')

        run_query(sql_template.format(placeholders), params)


def clear_all_tables():
    run_query("""
        DELETE FROM hand_tile;
        DELETE FROM player_yakus;
        DELETE FROM player_status;
        DELETE FROM games;
        DELETE FROM yaku;
        DELETE FROM players;
    """)
