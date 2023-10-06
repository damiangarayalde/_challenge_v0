CREATE DATABASE ${POSTGRES_DB}

create table if not exists testdata (
                flight_date         date,
                flight_status       character varying,
                departure_airport   character varying,
                departure_timezone  character varying,
                arrival_airport     character varying,
                arrival_timezone    character varying,
                arrival_terminal    character varying,
                airline_name        character varying,
                flight_number       character varying,
                primary key (flight_number);