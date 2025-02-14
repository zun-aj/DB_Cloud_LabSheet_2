import sqlite3

# Connecting to database (and/or create it if it doesn't yet exist)
conn = sqlite3.connect('flight_management.db')

#Protects against deletion of data used as foreign keys e.g. destination_id rows that impact the flights table
conn.execute("PRAGMA foreign_keys = ON;")

print("Database ready >>>")

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

print("Tables ready >>>")

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

#15 sample rows for Pilots
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
print("Data ready >>> \n \n")

#conn.close()

#Most function names are quite self-explanatory and are used to execute fairly simple queries that relate to the function name

def all_flight_details(conn):
    all_flights_details_query = """
    SELECT
        f.flight_id,
        f.date,
        f.time,
        f.status,
        o.airport AS origin_airport,
        o.city AS origin_city,
        d.airport AS destination_airport,
        d.city AS destination_city,
        p.pilot_id AS pilot_id,
        p.forename AS pilot_forename,
        p.surname AS pilot_surname
    FROM flights f
    LEFT JOIN destinations o ON f.origin_id = o.destination_id
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
    """
    cursor = conn.execute(all_flights_details_query)
    rows = cursor.fetchall()
    print_flight_details(rows)
    print("All flight details retrieved and displayed. Now returning to main menu... \n")
    

def flights_by_airport(conn, airport):
    filter_destination_query = """
    SELECT
        f.flight_id,
        f.date,
        f.time,
        f.status,
        o.airport AS origin_airport,
        o.city AS origin_city,
        d.airport AS destination_airport,
        d.city AS destination_city,
        p.pilot_id AS pilot_id,
        p.forename AS pilot_forename,
        p.surname AS pilot_surname
    FROM flights f
    LEFT JOIN destinations o ON f.origin_id = o.destination_id
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
    WHERE d.airport = ?
    """
    cursor = conn.execute(filter_destination_query, (airport,))
    rows = cursor.fetchall()
    print_flight_details(rows)
    print("\nQuery complete. Results retrieved.\nIf you see no results displayed, there were either no matches for your search criteria or you may need to double check for typos in your input and try again.\n")

def flights_by_city(conn, city):
    filter_destination_query = """
    SELECT
        f.flight_id,
        f.date,
        f.time,
        f.status,
        o.airport AS origin_airport,
        o.city AS origin_city,
        d.airport AS destination_airport,
        d.city AS destination_city,
        p.pilot_id AS pilot_id,
        p.forename AS pilot_forename,
        p.surname AS pilot_surname
    FROM flights f
    LEFT JOIN destinations o ON f.origin_id = o.destination_id
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
    WHERE d.city = ?
    """
    cursor = conn.execute(filter_destination_query, (city,))
    rows = cursor.fetchall()
    print_flight_details(rows)
    print("\nQuery complete. Results retrieved.\nIf you see no results displayed, there were either no matches for your search criteria or you may need to double check for typos in your input and try again.\n")

def flights_by_status(conn, status):
    filter_flight_status_query = """
    SELECT
        f.flight_id,
        f.date,
        f.time,
        f.status,
        o.airport AS origin_airport,
        o.city AS origin_city,
        d.airport AS destination_airport,
        d.city AS destination_city,
        p.pilot_id AS pilot_id,
        p.forename AS pilot_forename,
        p.surname AS pilot_surname
    FROM flights f
    LEFT JOIN destinations o ON f.origin_id = o.destination_id
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
    WHERE f.status = ?
    """
    cursor = conn.execute(filter_flight_status_query, (status,))
    rows = cursor.fetchall()
    print_flight_details(rows)
    print("\nQuery complete. Results retrieved.\nIf you see no results displayed, there were either no matches for your search criteria or you may need to double check for typos in your input and try again.\n")

def flights_filtered_by_date(conn, date):
    filter_by_date = """
    SELECT
        f.flight_id,
        f.date,
        f.time,
        f.status,
        o.airport AS origin_airport,
        o.city AS origin_city,
        d.airport AS destination_airport,
        d.city AS destination_city,
        p.pilot_id AS pilot_id,
        p.forename AS pilot_forename,
        p.surname AS pilot_surname
    FROM flights f
    LEFT JOIN destinations o ON f.origin_id = o.destination_id
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
    WHERE f.date = ?
    """
    cursor = conn.execute(filter_by_date, (date,))
    rows = cursor.fetchall()
    print_flight_details(rows)
    print("\nQuery complete. Results retrieved.\nIf you see no results displayed, there were either no matches for your search criteria or you may need to double check for typos in your input and try again.\n")
    
def print_flight_details(rows):
    print("\n -- All Flights Details: -- \n")
    for row in rows:
        flight_id, date, time, status, origin_airport, origin_city, dest_airport, dest_city, pilot_id, pilot_forename, pilot_surname = row

        print(f"Flight ID:           {flight_id}")
        print(f"Date:                {date}")
        print(f"Time:                {time}")
        print(f"Status:              {status}")
        print(f"Origin Airport:      {origin_airport}")
        print(f"Origin City:         {origin_city}")
        print(f"Destination Airport: {dest_airport}")
        print(f"Destination City:    {dest_city}")
        print(f"Pilot ID:            {pilot_id}")
        print(f"Pilot Forename:      {pilot_forename}")
        print(f"Pilot Surname:       {pilot_surname}")
        print("\n---\n")
    
def insert_new_flight_record(conn, date, time, origin_id, destination_id, pilot_id, status):
    add_flight = """
    INSERT INTO flights (date, time, origin_id, destination_id, pilot_id, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conn.execute(add_flight, (date, time, origin_id, destination_id, pilot_id, status))
    conn.commit()
    new_flight_id = cursor.lastrowid
    print(f"New flight {new_flight_id} addition successful")
    print()
    print("The following information has been stored in the database: \n")
    cursor = conn.execute("SELECT * FROM flights WHERE flight_id = ?", (new_flight_id,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_flight_date(conn, flight_id, new_date):
    update_flight_date_query = """
    UPDATE flights
    SET date = ?
    WHERE flight_id = ?
    """
    cursor = conn.execute(update_flight_date_query, (new_date, flight_id))
    conn.commit()
    print()
    print(f"Flight {flight_id} date updated to {new_date}")

def update_flight_time(conn, flight_id, new_time):
    update_flight_time_query = """
    UPDATE flights
    SET time = ?
    WHERE flight_id = ?
    """
    cursor = conn.execute(update_flight_time_query, (new_time, flight_id))
    conn.commit()
    print()
    print(f"Flight {flight_id} time updated to {new_time}")

def update_flight_status(conn, flight_id, new_status):
    update_flight_status_query = """
    UPDATE flights
    SET status = ?
    WHERE flight_id = ?
    """
    cursor = conn.execute(update_flight_status_query, (new_status, flight_id))
    conn.commit()
    print()
    print(f"Flight {flight_id} status updated to {new_status}")

def assign_pilot_to_flight(conn, flight_id, pilot_id):
    assign_pilot_to_flight_query = """
    UPDATE flights
    SET pilot_id = ?
    WHERE flight_id = ?
    """
    cursor = conn.execute(assign_pilot_to_flight_query, (pilot_id, flight_id))
    conn.commit()
    print()
    print(f"Pilot {pilot_id} assigned to flight {flight_id}")

def delete_flight_record(conn, flight_id):
    delete_flight_query = """
    DELETE FROM flights
    WHERE flight_id = ?
    """
    cursor = conn.execute(delete_flight_query, (flight_id,))
    conn.commit()
    print()
    print(f"Flight {flight_id} deleted")

def add_destination(conn, airport, city, country):
    add_destination_query = """
    INSERT INTO destinations (airport, city, country)
    VALUES (?, ?, ?)
    """
    cursor = conn.execute(add_destination_query, (airport, city, country))
    conn.commit()
    print()
    print(f"New destination: {airport} - {city} - {country} added to database\n")

def delete_destination(conn, airport):
    delete_destination_query = """
    DELETE FROM destinations
    WHERE airport = ?
    """
    cursor = conn.execute(delete_destination_query, (airport,))
    conn.commit()
    print()
    print(f"Airport: {airport} deleted from database\n")

def update_flight_destination(conn, flight_id, new_destination_id):
    update_flight_destination_query = """
    UPDATE flights
    SET destination_id = ?
    WHERE flight_id = ?
    """
    cursor = conn.execute(update_flight_destination_query, (new_destination_id, flight_id))
    conn.commit()
    print()
    print(f"Flight {flight_id} destination updated to {new_destination_id}")

def view_all_destinations(conn):
    view_all_destinations_query = """
    SELECT * FROM destinations
    """
    cursor = conn.execute(view_all_destinations_query)
    rows = cursor.fetchall()
    print("\n -- All Destinations: -- \n")
    for row in rows:
        destination_id, airport, city, country = row
        print(f"destination_id: {destination_id}")
        print(f"airport: {airport}")
        print(f"city:    {city}")
        print(f"country: {country}")
        print("\n---\n")

def filter_by_pilot(conn, pilot_id):
    filter_by_pilot_query = """
    SELECT
        p.pilot_id AS pilot_id,
        p.forename AS pilot_forename,
        p.surname AS pilot_surname,
        f.flight_id,
        f.date,
        f.time,
        f.status,
        o.airport AS origin_airport,
        o.city AS origin_city,
        d.airport AS destination_airport,
        d.city AS destination_city
    FROM pilots p
    LEFT JOIN flights f ON f.pilot_id = p.pilot_id
    LEFT JOIN destinations o ON f.origin_id = o.destination_id
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    WHERE p.pilot_id = ?
    """
    cursor = conn.execute(filter_by_pilot_query, (pilot_id,))
    rows = cursor.fetchall()
    print("\nFlights for Pilot:\n")
    for row in rows:
        pilot_id, pilot_forename, pilot_surname, flight_id, date, time, status, origin_airport, origin_city, destination_airport, destination_city = row

        print(f"pilot_id:            {pilot_id}")
        print(f"pilot_forename:      {pilot_forename}")
        print(f"pilot_surname:       {pilot_surname}")
        print(f"flight_id:           {flight_id}")
        print(f"date:                {date}")
        print(f"time:                {time}")
        print(f"status:              {status}")
        print(f"origin_airport:      {origin_airport}")
        print(f"origin_city:         {origin_city}")
        print(f"destination_airport: {destination_airport}")
        print(f"destination_city:    {destination_city}")
        print("\n---\n")

def view_all_pilots(conn):
    view_all_pilots_query = """
    SELECT * FROM pilots
    """
    cursor = conn.execute(view_all_pilots_query)
    rows = cursor.fetchall()
    print("\n -- All Pilots: -- \n")
    for row in rows:
        pilot_id, pilot_forename, pilot_surname, license_no, years_of_xp, email, phone = row
        print(f"pilot_id:            {pilot_id}")
        print(f"pilot_forename:      {pilot_forename}")
        print(f"pilot_surname:       {pilot_surname}")
        print(f"license_no:          {license_no}")
        print(f"years_of_xp:         {years_of_xp}")
        print(f"email:               {email}")
        print(f"phone:               {phone}")
        print("\n---\n")

def count_flights_by_pilot(conn):
    pilot_flight_count = """
    SELECT p.pilot_id, p.forename, p.surname, COUNT(*) AS total_flights
    FROM flights f
    LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
    GROUP BY p.pilot_id
    ORDER BY total_flights DESC;
    """
    cursor = conn.execute(pilot_flight_count)
    rows = cursor.fetchall()
    print("\nFormat: pilot_id, pilot_forename, pilot_surname, count_of_assigned_flights")
    for row in rows:
        print(row)

def most_experienced_pilots(conn):
    most_experienced_pilots = """
    SELECT forename, surname, years_of_xp
    FROM pilots
    ORDER BY years_of_xp DESC
    LIMIT 3
    """
    cursor = conn.execute(most_experienced_pilots)
    rows = cursor.fetchall()
    print("\nFormat: forename, surname, years_of_xp")
    for row in rows:
        print(row)
    print()

def least_experienced_pilots(conn):
    least_experienced_pilots = """
    SELECT forename, surname, years_of_xp
    FROM pilots
    ORDER BY years_of_xp ASC
    LIMIT 3
    """
    cursor = conn.execute(least_experienced_pilots)
    rows = cursor.fetchall()
    print("\nFormat: forename, surname, years_of_xp")
    for row in rows:
        print(row)
    print()
    

def most_popular_destinations(conn):
    most_popular_destination_query = """
    SELECT d.country, d.airport, d.city, COUNT(*) AS total_flights
    FROM flights f
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    GROUP BY d.country, d.airport, d.city
    ORDER BY total_flights DESC
    LIMIT 3;
    """
    cursor = conn.execute(most_popular_destination_query)
    rows = cursor.fetchall()
    print("\nFormat: country, airport, city, count_of_flights")
    for row in rows:
        print(row)

def least_popular_destinations(conn):
    least_popular_destination_query = """
    SELECT d.country, d.airport, d.city, COUNT(*) AS total_flights
    FROM flights f
    LEFT JOIN destinations d ON f.destination_id = d.destination_id
    GROUP BY d.country, d.airport, d.city
    ORDER BY total_flights ASC
    LIMIT 3;
    """
    cursor = conn.execute(least_popular_destination_query)
    rows = cursor.fetchall()
    print("\nFormat: country, airport, city, count_of_flights")
    for row in rows:
        print(row)
    

while True:
    print(" \n --- Welcome to the Flight Information Tool --- \n")
    print("Select an option from the menu below: \n")
    print("1) View All Flight Information - Enter '1'")
    print("2) View Flight Information by Specific Criteria - Enter '2'")
    print("3) Add a New Flight - Enter '3'")
    print("4) Update Flight Information (Including Pilot Assignment) - Enter '4'")
    print("5) Update Destination Information - Enter '5'")
    print("6) View Pilot Information & Schedule - Enter '6'")
    print("7) View Most and Least Popular Destinations - Enter '7'")
    print("8) Exit - Enter '8'")
    print()
    selection = input("Select an option: \n")
    
    if selection == '1':
        all_flight_details(conn)

    elif selection == '2':
        while True:
            print("\nPlease select a criteria by entering the corresponding number\n")
            print("1) Filter Flights by Destination Airport - Enter '1'")
            print("2) Filter Flights by Destination City - Enter '2'")
            print("3) Filter Flights by Status - Enter '3'")
            print("4) Filter Flights by Date - Enter '4'")
            print("5) Return to main menu - Enter '5'")
            print()
            criteria_selection = input("Select a criteria:\n")
            if criteria_selection == '1':
                airport = input("\nEnter the airport name (case sensitive):\n")
                flights_by_airport(conn, airport)
            elif criteria_selection == '2':
                city = input("\nEnter the city name (case sensitive):\n")
                flights_by_city(conn, city)
            elif criteria_selection == '3':
                status = input("\nEnter the flight status ('Arrived', 'Cancelled', 'Departed', 'Boarding', 'Scheduled'):\n")
                flights_by_status(conn, status)
            elif criteria_selection == '4':
                date = input("\nEnter the date (YYYY-MM-DD):\n")
                flights_filtered_by_date(conn, date)
            elif criteria_selection == '5':
                print("\nReturning to main menu\n")
                break
            else:
                print("\nInvalid input. Please try again.\n")

    
    elif selection == '3':
        print("\n Enter the following information to add a new flight record: \n")
        date = input("Date (YYYY-MM-DD): ")
        time = input("Time - 24hr Clock Format (HH:MM): ")
        origin_id = int(input("Origin ID: "))
        destination_id = int(input("Destination ID: "))
        pilot_id = int(input("Pilot ID: "))
        status = input("Status (Arrived, Cancelled, Boarding, Departed, Scheduled): ")
        insert_new_flight_record(conn, date, time, origin_id, destination_id, pilot_id, status)
        print()

    #Update flight information functions (sub-menu)
    elif selection == '4':
        while True:
            print("\nPlease select an option by entering the corresponding number\n")
            print("1) Update Flight Date - Enter '1'")
            print("2) Update Flight Time - Enter '2'")
            print("3) Update Flight Status - Enter '3'")
            print("4) Assign Pilot to Flight - Enter '4'")
            print("5) Delete a Flight Record - Enter '5'")
            print("6) Return to main menu - Enter '6'")
            print()
            option_selection = input("Select one of the following:\n")
            if option_selection == '1':
                flight_id = int(input("\nEnter the flight ID:\n"))
                new_date = input("\nEnter the new date (YYYY-MM-DD):\n")
                update_flight_date(conn, flight_id, new_date)
            elif option_selection == '2':
                flight_id = int(input("\nEnter the flight ID:\n"))
                new_time = input("\nEnter the new time - 24hr Clock Format (HH:MM):\n")
                update_flight_time(conn, flight_id, new_time)
            elif option_selection == '3':
                flight_id = int(input("\nEnter the flight ID:\n"))
                new_status = input("\nEnter the new status ('Arrived', 'Cancelled', 'Boarding', 'Departed', 'Scheduled'):\n")
                update_flight_status(conn, flight_id, new_status)
            elif option_selection == '4':
                flight_id = int(input("\nEnter the flight ID:\n"))
                pilot_id = int(input("\nEnter the pilot ID:\n"))
                assign_pilot_to_flight(conn, flight_id, pilot_id)
            elif option_selection == '5':
                flight_id = int(input("\nEnter the flight ID:\n"))
                delete_flight_record(conn, flight_id)
            elif option_selection == '6':
                print("\nReturning to main menu\n")
                break

    #Update Destinations functions (sub-menu)
    elif selection == '5':
        while True:
            print("\nPlease select an option by entering the corresponding number\n")
            print("1) View All Destinations - Enter '1'")
            print("2) Add New Destination - Enter '2'")
            print("3) Delete A Destination - Enter '3'")
            print("4) Update a Flight Destination - Enter '4'")
            print("5) Return to Main Menu - Enter '5'")
            print()
            option_selection = input("Select one of the following:\n")
            if option_selection == '1':
                view_all_destinations(conn)
            elif option_selection == '2':
                airport = input("\nEnter the airport name (case sensitive):\n")
                city = input("\nEnter the city name (case sensitive):\n")
                country = input("\nEnter the country name (case sensitive):\n")
                add_destination(conn, airport, city, country)
            elif option_selection == '3':
                airport = input("\nEnter the airport name (case sensitive):\n")
                delete_destination(conn, airport)
            elif option_selection == '4':
                flight_id = int(input("\nEnter the flight ID:\n"))
                destination_id = int(input("\nEnter the new destination_id:\n"))
                update_flight_destination(conn, flight_id, destination_id)
            elif option_selection == '5':
                print("\nReturning to main menu\n")
                break
            else:
                print("\nInvalid input. Please try again.\n")
                

    #View Pilot Schedule & Information (sub-menu)
    elif selection == '6':
        while True:
            print("\nPlease select an option by entering the corresponding number\n")
            print("1) View All Pilot Information - Enter '1'")
            print("2) View Schedule for a Specific Pilot - Enter '2'")
            print("3) View Number of Flights Assigned to Each Pilot - Enter '3'")
            print("4) View Most Experienced Pilots - Enter '4'")
            print("5) View Least Experienced Pilots - Enter '5'")
            print("6) Return to Main Menu - Enter '6'")
            print()
            option_selection = input("Select one of the following:\n")
            if option_selection == '1':
                view_all_pilots(conn)
            elif option_selection == '2':
                pilot_id = int(input("\nEnter the pilot ID:\n"))
                filter_by_pilot(conn, pilot_id)
            elif option_selection == '3':
                count_flights_by_pilot(conn)
            elif option_selection == '4':
                most_experienced_pilots(conn)
            elif option_selection == '5':
                least_experienced_pilots(conn)
            elif option_selection == '6':
                print("\nReturning to main menu\n")
                break
            else:
                print("\nInvalid input. Please try again.\n")
    

    #View Most and Least Popular Destinations functions (sub-menu)  
    elif selection == '7':
        while True:
            print("\nPlease select an option by entering the corresponding number\n")
            print("1) View Most Popular Destinations - Enter '1'")
            print("2) View Least Popular Destinations - Enter '2'")
            print("3) Return to Main Menu - Enter '3'")
            print()
            option_selection = input("Select one of the following:\n")
            if option_selection == '1':
                most_popular_destinations(conn)
            elif option_selection == '2':
                least_popular_destinations(conn)
            elif option_selection == '3':
                print("\nReturning to main menu\n")
                break
            else:
                print("\nInvalid input. Please try again.\n")
            
    elif selection == '8':
        print("\nExiting the program...")
        print("Exited. Thank you for using the Flight Information Tool!")
        break
        
    else:
        print("Invalid selection. Please try again.\n")
        
        
    
#-----------------------------------------------------------------------#

#SQL Query Planning Documented in the Section Below Prior to Writing Python Functions
        
#Query to view all flight information
'''
all_flights_details_query = """
SELECT
    f.flight_id,
    f.date,
    f.time,
    f.status,
    o.airport AS origin_airport,
    o.city AS origin_city,
    d.airport AS destination_airport,
    d.city AS destination_city,
    p.pilot_id AS pilot_id,
    p.forename AS pilot_forename,
    p.surname AS pilot_surname
FROM flights f
LEFT JOIN destinations o ON f.origin_id = o.destination_id
LEFT JOIN destinations d ON f.destination_id = d.destination_id
LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
"""
cursor = conn.execute(all_flights_details_query)
rows = cursor.fetchall()

print()
print("All Flights Details:")
print()
for row in rows:
    flight_id, date, time, status, origin_airport, origin_city, dest_airport, dest_city, pilot_id, pilot_forename, pilot_surname = row

    print(f"Flight ID:           {flight_id}")
    print(f"Date:                {date}")
    print(f"Time:                {time}")
    print(f"Status:              {status}")
    print(f"Origin Airport:      {origin_airport}")
    print(f"Origin City:         {origin_city}")
    print(f"Destination Airport: {dest_airport}")
    print(f"Destination City:    {dest_city}")
    print(f"Pilot ID:            {pilot_id}")
    print(f"Pilot Forename:      {pilot_forename}")
    print(f"Pilot Surname:       {pilot_surname}")
    print("\n---\n")
'''

#Query to filter flight information by destination airport and city
'''
filter_destination_query = """
SELECT
    f.flight_id,
    f.date,
    f.time,
    f.status,
    o.airport AS origin_airport,
    o.city AS origin_city,
    d.airport AS destination_airport,
    d.city AS destination_city,
    p.pilot_id AS pilot_id,
    p.forename AS pilot_forename,
    p.surname AS pilot_surname
FROM flights f
LEFT JOIN destinations o ON f.origin_id = o.destination_id
LEFT JOIN destinations d ON f.destination_id = d.destination_id
LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
WHERE d.airport IS NOT NULL  AND d.city = 'New York'
"""
cursor = conn.execute(filter_destination_query)
rows = cursor.fetchall()

print()
print("All Flights Details:")
print()
for row in rows:
    flight_id, date, time, status, origin_airport, origin_city, dest_airport, dest_city, pilot_id, pilot_forename, pilot_surname = row

    print(f"Flight ID:           {flight_id}")
    print(f"Date:                {date}")
    print(f"Time:                {time}")
    print(f"Status:              {status}")
    print(f"Origin Airport:      {origin_airport}")
    print(f"Origin City:         {origin_city}")
    print(f"Destination Airport: {dest_airport}")
    print(f"Destination City:    {dest_city}")
    print(f"Pilot ID:            {pilot_id}")
    print(f"Pilot Forename:      {pilot_forename}")
    print(f"Pilot Surname:       {pilot_surname}")
    print("\n---\n")
'''

#Query to filter flight information by status
'''
filter_flight_status_query = """
SELECT
    f.flight_id,
    f.date,
    f.time,
    f.status,
    o.airport AS origin_airport,
    o.city AS origin_city,
    d.airport AS destination_airport,
    d.city AS destination_city,
    p.pilot_id AS pilot_id,
    p.forename AS pilot_forename,
    p.surname AS pilot_surname
FROM flights f
LEFT JOIN destinations o ON f.origin_id = o.destination_id
LEFT JOIN destinations d ON f.destination_id = d.destination_id
LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
WHERE f.status IN ("Boarding", "Departed", "Cancelled")
"""
cursor = conn.execute(filter_flight_status_query)
rows = cursor.fetchall()

print()
print("All Flights Details:")
print()
for row in rows:
    flight_id, date, time, status, origin_airport, origin_city, dest_airport, dest_city, pilot_id, pilot_forename, pilot_surname = row

    print(f"Flight ID:           {flight_id}")
    print(f"Date:                {date}")
    print(f"Time:                {time}")
    print(f"Status:              {status}")
    print(f"Origin Airport:      {origin_airport}")
    print(f"Origin City:         {origin_city}")
    print(f"Destination Airport: {dest_airport}")
    print(f"Destination City:    {dest_city}")
    print(f"Pilot ID:            {pilot_id}")
    print(f"Pilot Forename:      {pilot_forename}")
    print(f"Pilot Surname:       {pilot_surname}")
    print("\n---\n")
'''

#Query to filter flight information by departure date
'''
filter_by_date = """
SELECT
    f.flight_id,
    f.date,
    f.time,
    f.status,
    o.airport AS origin_airport,
    o.city AS origin_city,
    d.airport AS destination_airport,
    d.city AS destination_city,
    p.pilot_id AS pilot_id,
    p.forename AS pilot_forename,
    p.surname AS pilot_surname
FROM flights f
LEFT JOIN destinations o ON f.origin_id = o.destination_id
LEFT JOIN destinations d ON f.destination_id = d.destination_id
LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
WHERE f.date = '2025-01-03' OR f.date = '2025-01-04'
"""
cursor = conn.execute(filter_by_date)
rows = cursor.fetchall()

print()
print("All Flights Details:")
print()
for row in rows:
    flight_id, date, time, status, origin_airport, origin_city, dest_airport, dest_city, pilot_id, pilot_forename, pilot_surname = row

    print(f"Flight ID:           {flight_id}")
    print(f"Date:                {date}")
    print(f"Time:                {time}")
    print(f"Status:              {status}")
    print(f"Origin Airport:      {origin_airport}")
    print(f"Origin City:         {origin_city}")
    print(f"Destination Airport: {dest_airport}")
    print(f"Destination City:    {dest_city}")
    print(f"Pilot ID:            {pilot_id}")
    print(f"Pilot Forename:      {pilot_forename}")
    print(f"Pilot Surname:       {pilot_surname}")
    print("\n---\n")
'''

#Update flight status
'''
select_flight_id = 15
revised_status = "Cancelled"

update_status = """
UPDATE flights
SET status = ?
WHERE flight_id = ?
"""

conn.execute(update_status, (revised_status, select_flight_id))

conn.commit()

print(f"Flight #{select_flight_id} status updated to '{revised_status}'.")

cursor = conn.execute("SELECT * FROM flights WHERE flight_id = ?", (select_flight_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Update flight destination
'''
select_flight_id = 13
revised_destination_id = 15

update_destination = """
UPDATE flights
SET destination_id = ?
WHERE flight_id = ?
"""

conn.execute(update_destination, (revised_destination_id, select_flight_id))
conn.commit()

print(f"Flight #{select_flight_id} destination ID updated to '{revised_destination_id}'.")

cursor = conn.execute("SELECT * FROM flights WHERE flight_id = ?", (select_flight_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Update flight time
'''
select_flight_id = 13
revised_time = "20:55"

update_time = """
UPDATE flights
SET time = ?
WHERE flight_id = ?
"""

conn.execute(update_time, (revised_time, select_flight_id))
conn.commit()

print(f"Flight #{select_flight_id} time updated to '{revised_time}'.")

cursor = conn.execute("SELECT * FROM flights WHERE flight_id = ?", (select_flight_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Update flight date
'''
select_flight_id = 15
revised_date = "2025-02-17"

update_date = """
UPDATE flights
SET date = ?
WHERE flight_id = ?
"""

conn.execute(update_date, (revised_date, select_flight_id))
conn.commit()

print(f"Flight #{select_flight_id} date updated to '{revised_date}'.")

cursor = conn.execute("SELECT * FROM flights WHERE flight_id = ?", (select_flight_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Query to view flights by pilot
'''
filter_by_pilot = """
SELECT
    p.pilot_id AS pilot_id,
    p.forename AS pilot_forename,
    p.surname AS pilot_surname,
    f.flight_id,
    f.date,
    f.time,
    f.status,
    o.airport AS origin_airport,
    o.city AS origin_city,
    d.airport AS destination_airport,
    d.city AS destination_city
FROM pilots p
LEFT JOIN flights f ON f.pilot_id = p.pilot_id
LEFT JOIN destinations o ON f.origin_id = o.destination_id
LEFT JOIN destinations d ON f.destination_id = d.destination_id
WHERE p.pilot_id = ?
"""
cursor = conn.execute(filter_by_pilot)
rows = cursor.fetchall()

print()
print("Flights for Pilot:")
print()
for row in rows:
    pilot_id, pilot_forename, pilot_surname, flight_id, date, time, status, origin_airport, origin_city, dest_airport, dest_city = row

    print(f"Pilot ID:            {pilot_id}")
    print(f"Pilot Forename:      {pilot_forename}")
    print(f"Pilot Surname:       {pilot_surname}")
    print(f"Flight ID:           {flight_id}")
    print(f"Date:                {date}")
    print(f"Time:                {time}")
    print(f"Status:              {status}")
    print(f"Origin Airport:      {origin_airport}")
    print(f"Origin City:         {origin_city}")
    print(f"Destination Airport: {dest_airport}")
    print(f"Destination City:    {dest_city}")
    print("\n---\n")
'''

#Adding a flight
'''
temp_date = "2025-03-26"
temp_time = "12:00"
temp_origin_id = 11
temp_destination_id = 15
temp_pilot_id = 7
temp_status = "Scheduled"

add_flight = """
INSERT INTO flights (date, time, origin_id, destination_id, pilot_id, status)
VALUES (?, ?, ?, ?, ?, ?)
"""

cursor = conn.execute(add_flight, (temp_date, temp_time, temp_origin_id, temp_destination_id, temp_pilot_id, temp_status))

conn.commit()

new_flight_id = cursor.lastrowid

print(f"New flight {new_flight_id} addition successful")

cursor = conn.execute("SELECT * FROM flights WHERE flight_id = ?", (new_flight_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Deleting a flight
'''
deletion_flight_id = 14

delete_flight = """
DELETE FROM flights
WHERE flight_id = ?
"""

conn.execute(delete_flight, (deletion_flight_id,))
conn.commit()

print(f"Flight #{deletion_flight_id} has been deleted.")
'''

#Assign Pilot
'''
select_flight_id = 15
revised_pilot_id = 3

assign_pilot = """
UPDATE flights
SET pilot_id = ?
WHERE flight_id = ?
"""

conn.execute(assign_pilot, (revised_pilot_id, select_flight_id))
conn.commit()

print(f"Flight #{select_flight_id} pilot changed to '{revised_pilot_id}'.")

cursor = conn.execute("SELECT * FROM flights f LEFT JOIN pilots p ON p.pilot_id = f.pilot_id  WHERE flight_id = ?", (select_flight_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Adding a destination
'''
temp_airport = "Gatwick"
temp_city = "London" 
temp_country = "UK"

add_destination = """
INSERT INTO destinations (airport, city, country)
VALUES (?, ?, ?)
"""

cursor = conn.execute(add_destination, (temp_airport, temp_city, temp_country))

conn.commit()

new_destination_id = cursor.lastrowid

print(f"New destination {new_destination_id} addition successful")

cursor = conn.execute("SELECT * FROM destinations WHERE destination_id = ?", (new_destination_id,))
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Deleting a destination
'''
deletion_destination_id = 16

delete_destination = """
DELETE FROM destinations
WHERE destination_id = ?
"""

conn.execute(delete_destination, (deletion_destination_id,))
conn.commit()

print(f"Destination #{deletion_destination_id} deletion complete.")
'''

#Most Popular Destinations
'''
destination_popularity_high = """
SELECT d.country, d.city, d.airport, COUNT(*) AS total_flights
FROM flights f
LEFT JOIN destinations d ON f.destination_id = d.destination_id
GROUP BY d.country, d.city, d.airport
ORDER BY total_flights DESC;
"""
cursor = conn.execute(destination_popularity_high)
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Least Popular Destinations
'''
destination_popularity_low = """
SELECT d.country, d.city, d.airport, COUNT(*) AS total_flights
FROM flights f
JOIN destinations d ON f.destination_id = d.destination_id
GROUP BY d.country, d.city, d.airport
ORDER BY total_flights ASC;
"""
cursor = conn.execute(destination_popularity_low)
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Most Experienced Pilot
'''
most_experienced_pilots = """
SELECT forename, surname, years_of_xp
FROM pilots
ORDER BY years_of_xp DESC
LIMIT 3
"""
cursor = conn.execute(most_experienced_pilots)
rows = cursor.fetchall()
for row in rows:
    print(row)

print()
'''

#Least Experienced Pilot
'''
least_experienced_pilots = """
SELECT forename, surname, years_of_xp
FROM pilots
ORDER BY years_of_xp ASC
LIMIT 3
"""
cursor = conn.execute(least_experienced_pilots)
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

#Number of Flights Assigned to a Pilot
'''
pilot_flight_count = """
SELECT p.pilot_id, p.forename, p.surname, COUNT(*) AS total_flights
FROM flights f
LEFT JOIN pilots p ON f.pilot_id = p.pilot_id
GROUP BY p.pilot_id
ORDER BY total_flights DESC;
"""
cursor = conn.execute(pilot_flight_count)
rows = cursor.fetchall()
for row in rows:
    print(row)
'''

