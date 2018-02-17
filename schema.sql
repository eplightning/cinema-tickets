CREATE KEYSPACE cinemadb
  WITH REPLICATION = { 
    'class' : 'SimpleStrategy', 
    'replication_factor' : 1 
  };

USE cinemadb;

CREATE TABLE cinemas (
  id text,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE movies (
  id text,
  name text,
  description text,
  cover blob,
  PRIMARY KEY ((id), name)
);

CREATE TABLE sessions (
  movie_id text,
  cinema_id text,
  date timestamp,
  id uuid,
  hall_id text,
  hall_name text,
  hall_capacity int,
  PRIMARY KEY ((movie_id), cinema_id, date, id)
);

CREATE TABLE tickets (
  session_id uuid,
  timestamp timestamp,
  user text,
  PRIMARY KEY ((session_id), timestamp)
);
