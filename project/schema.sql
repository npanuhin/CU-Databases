CREATE TABLE players (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  display_name TEXT,
  rating INTEGER DEFAULT 1500,
  country TEXT
);

CREATE TABLE games (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  winner_id INTEGER,
  wind TEXT CHECK (wind IN ('East', 'South')),
  dealer_id INTEGER,
  FOREIGN KEY (winner_id) REFERENCES players(id),
  FOREIGN KEY (dealer_id) REFERENCES players(id)
);

CREATE TABLE player_status (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  game_id INTEGER,
  player_id INTEGER,
  wind TEXT CHECK (wind IN ('East', 'South', 'West', 'North')),
  cur_score INTEGER DEFAULT 25000,
  declared_riichi BOOLEAN,
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE yaku (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  han_value INTEGER,
  menzenchin_only BOOLEAN,
  description TEXT
);

CREATE TABLE player_yakus (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_status_id INTEGER,
  yaku_id INTEGER,
  FOREIGN KEY (player_status_id) REFERENCES player_status(id),
  FOREIGN KEY (yaku_id) REFERENCES yaku(id)
);

CREATE TABLE tiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tile_code TEXT UNIQUE NOT NULL
);

CREATE TABLE hand_tile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_status_id INTEGER,
  tile_id INTEGER,
  is_in_meld BOOLEAN,
  position INTEGER,
  FOREIGN KEY (player_status_id) REFERENCES player_status(id),
  FOREIGN KEY (tile_id) REFERENCES tiles(id),
  CHECK (is_in_meld = TRUE OR position IS NOT NULL)
);


CREATE UNIQUE INDEX unique_hand_position
ON hand_tile(player_status_id, position)
WHERE is_in_meld = FALSE;

CREATE INDEX idx_games_winner_id ON games(winner_id);
CREATE INDEX idx_games_dealer_id ON games(dealer_id);
CREATE INDEX idx_player_status_game_id ON player_status(game_id);
CREATE INDEX idx_player_status_player_id ON player_status(player_id);
CREATE INDEX idx_player_yakus_status_id ON player_yakus(player_status_id);
CREATE INDEX idx_player_yakus_yaku_id ON player_yakus(yaku_id);
CREATE INDEX idx_hand_tile_player_status_id ON hand_tile(player_status_id);
CREATE INDEX idx_hand_tile_tile_id ON hand_tile(tile_id);
