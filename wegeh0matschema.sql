CREATE TABLE
    people
    (
	id integer not null,
	nickname text,
	jid text,
	primary key (id)
    );

CREATE TABLE
    participants
    (
        event_id INTEGER NOT NULL,
        people_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        PRIMARY KEY (event_id, people_id)
    );

CREATE TABLE
    event
    (
        id INTEGER not null references participants(event_id) on delete cascade,
        name TEXT not null,
        begin_date timestamp,
	end_date timestamp,
        comment TEXT,
        creator INTEGER,
        meeting_point TEXT,
	create_date timestamp,
        PRIMARY KEY (id)
    );