import sqlite3

# Connecting to database (and creating it if it doesn't yet exist)
conn = sqlite3.connect('flight_management.db')
print("Database ready...")

# Dropping any old tables prior to creating new ones
conn.execute("DROP TABLE IF EXISTS flights")
conn.execute("DROP TABLE IF EXISTS destinations")
conn.execute("DROP TABLE IF EXISTS pilots")

# Creates the Destinations table
conn.execute("""
CREATE TABLE destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL
)
""")

# Creates the Pilots table
conn.execute("""
CREATE TABLE pilots (
    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    forename TEXT NOT NULL,
    surname TEXT NOT NULL,
    license_no TEXT NOT NULL,
    years_of_xp INTEGER NOT NULL,
    email TEXT,
    phone TEXT
)
""")

# Creates  Flights table 
conn.execute("""
CREATE TABLE flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    origin_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    pilot_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (origin_id) REFERENCES destinations(destination_id),
    FOREIGN KEY (destination_id) REFERENCES destinations(destination_id),
    FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id)
)
""")

print("Tables ready...")

#15 sample rows for Destinations
destinations_data = [
    ("Heathrow",               "London",        "UK"),
    ("JFK International",      "New York",      "USA"),
    ("Haneda",                 "Tokyo",         "Japan"),
    ("Charles de Gaulle",      "Paris",         "France"),
    ("Frankfurt Airport",      "Frankfurt",     "Germany"),
    ("Dubai International",    "Dubai",         "UAE"),
    ("Changi",                 "Singapore",     "Singapore"),
    ("Sydney Kingsford Smith", "Sydney",        "Australia"),
    ("Incheon",                "Seoul",         "South Korea"),
    ("Suvarnabhumi",           "Bangkok",       "Thailand"),
    ("Amsterdam Schiphol",     "Amsterdam",     "Netherlands"),
    ("Barcelona El Prat",      "Barcelona",     "Spain"),
    ("Toronto Pearson",        "Toronto",       "Canada"),
    ("Los Angeles Intl",       "Los Angeles",   "USA"),
    ("Beijing Capital",        "Beijing",       "China")
]

conn.executemany("""
INSERT INTO destinations (airport, city, country)
VALUES (?, ?, ?)
""", destinations_data)

#15 sample rows for pilots
pilots_data = [
    ("John",       "Smith",    "LIC12345",  5,  "john.smith@example.com",    "555-1111"),
    ("Sarah",      "Johnson",  "LIC67890", 12,  "sarah.j@example.com",       "555-2222"),
    ("Michael",    "Brown",    "LIC54321",  8,  "michael.b@example.com",     "555-3333"),
    ("Emily",      "Davis",    "LIC98765",  3,  "emily.d@example.com",       "555-4444"),
    ("David",      "Wilson",   "LIC13579", 10,  "david.w@example.com",       "555-5555"),
    ("Jessica",    "Garcia",   "LIC24680", 15,  "jessica.g@example.com",     "555-6666"),
    ("Robert",     "Miller",   "LIC11223",  6,  "robert.m@example.com",      "555-7777"),
    ("Linda",      "Martinez", "LIC44556", 20,  "linda.m@example.com",       "555-8888"),
    ("Paul",       "Robinson", "LIC77889",  2,  "paul.r@example.com",        "555-9999"),
    ("Karen",      "Clark",    "LIC99000",  7,  "karen.c@example.com",       "555-0000"),
    ("Steven",     "Lewis",    "LIC99991",  9,  "steven.l@example.com",      "555-0101"),
    ("Nancy",      "Lee",      "LIC88882",  4,  "nancy.l@example.com",       "555-0202"),
    ("Richard",    "Walker",   "LIC77773", 11,  "richard.w@example.com",     "555-0303"),
    ("Elizabeth",  "Hall",     "LIC66664", 13,  "elizabeth.h@example.com",   "555-0404"),
    ("Daniel",     "Allen",    "LIC55555",  1,  "daniel.a@example.com",      "555-0505")
]

conn.executemany("""
INSERT INTO pilots (forename, surname, license_no, years_of_xp, email, phone)
VALUES (?, ?, ?, ?, ?, ?)
""", pilots_data)

#15 sample rows for Flights.
flights_data = [
    ("2025-01-01", "08:00", 1,  2,  1,  "Arrived"),
    ("2025-01-02", "09:30", 3,  5,  2,  "Cancelled"),
    ("2025-01-03", "14:15", 5,  6,  3,  "Arrived"),
    ("2025-01-04", "11:00", 2,  1,  4,  "Cancelled"),
    ("2025-01-05", "16:45", 6,  7,  5,  "Arrived"),
    ("2025-01-06", "07:20", 4,  3,  6,  "Arrived"),
    ("2025-01-07", "19:00", 8,  9,  7,  "Departed"),
    ("2025-01-08", "05:10", 9,  10, 8,  "Departed"),
    ("2025-01-09", "12:30", 11, 13, 9,  "Departed"),
    ("2025-01-10", "18:25", 7,  12, 10, "Boarding"),
    ("2025-01-11", "20:00", 14, 2,  11, "Scheduled"),
    ("2025-01-12", "06:15", 10, 4,  12, "Scheduled"),
    ("2025-01-13", "13:50", 2,  14, 13, "Scheduled"),
    ("2025-01-14", "10:10", 15, 2,  14, "Scheduled"),
    ("2025-01-15", "15:05", 3,  15, 15, "Scheduled")
]

conn.executemany("""
INSERT INTO flights (date, time, origin_id, destination_id, pilot_id, status)
VALUES (?, ?, ?, ?, ?, ?)
""", flights_data)

conn.commit()
print("Data ready...")
conn.close()
