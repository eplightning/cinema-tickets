from cinema_tickets.app import app
from cinema_tickets.db import db_session

with app.app_context():
    getMovies = db_session.prepare('SELECT * FROM movies')
    getCinemas = db_session.prepare('SELECT * FROM cinemas')
    getMovie = db_session.prepare('SELECT * FROM movies WHERE id = ?')
    getSession = db_session.prepare('SELECT * FROM sessions WHERE id = ?')
    getSessions = db_session.prepare('SELECT * FROM sessions WHERE movie_id = ? AND date = ?')
    getCinemaSessions = db_session.prepare('SELECT * FROM sessions_by_cinema WHERE movie_id = ? AND date = ? AND cinema_id = ?')
    getTicketsCount = db_session.prepare('SELECT sold_count, session_id FROM tickets_counter WHERE movie_id = ?')
    getTickets = db_session.prepare('SELECT * FROM tickets WHERE session_id = ? LIMIT ?')
    buyTicket = db_session.prepare('INSERT INTO tickets (session_id, id, user, timestamp) VALUES (?, ?, ?, ?) USING TIMESTAMP ?')
    updateTicketCounter = db_session.prepare('UPDATE tickets_counter SET sold_count = sold_count + 1 WHERE movie_id = ? AND session_id = ?')
    addMovie = db_session.prepare('INSERT INTO movies (id, name, cover, description) VALUES (uuid(), ?, ?, ?)')
    addCinema = db_session.prepare('INSERT INTO cinemas (id, name) VALUES (uuid(), ?)')
    addSession = db_session.prepare('INSERT INTO sessions (movie_id, date, time, cinema_id, id, hall_capacity, hall_name) VALUES (?, ?, ?, ?, ?, ?, ?)')
    addCinemaSession = db_session.prepare('INSERT INTO sessions_by_cinema (movie_id, date, time, cinema_id, id, hall_capacity, hall_name) VALUES (?, ?, ?, ?, ?, ?, ?)')