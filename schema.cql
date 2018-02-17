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
  date timestamp,
  id uuid,
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
