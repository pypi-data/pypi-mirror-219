CREATE TABLE timer(id NUMERIC, name TEXT);
CREATE TABLE time_event(timer_id NUMERIC, type TEXT, created TEXT);
CREATE TABLE timer_relation(timer_id NUMERIC, relationship TEXT, target NUMERIC);