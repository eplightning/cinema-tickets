from cinema_tickets.app import app
from cinema_tickets.queries import buy_ticket
import time
import uuid

def stress_process(session, times, user, pipe):
    with app.app_context():
        for i in range(0, times):
            pipe.send('Kupowanie biletu {}'.format(i))
            timestamp = time.time()
            buy_ticket(session, user, uuid.uuid1(), timestamp)

        pipe.close()

