CREATE KEYSPACE cinemadb
  WITH REPLICATION = { 
    'class' : 'SimpleStrategy', 
    'replication_factor' : 1 
  };

USE cinemadb;

CREATE TABLE cinemas (
  id uuid,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE movies (
  id uuid,
  name text,
  description text,
  cover blob,
  PRIMARY KEY ((id), name)
);

CREATE TABLE sessions (
  movie_id uuid,
  cinema_id uuid,
  date date,
  id uuid,
  time time,
  hall_name text,
  hall_capacity int,
  PRIMARY KEY ((movie_id), date, cinema_id, id)
);

CREATE INDEX ON sessions (id);

CREATE TABLE tickets (
  session_id uuid,
  id timeuuid,
  user text,
  timestamp timestamp,
  PRIMARY KEY ((session_id), id, user)
);
