import mysql.connector
import const

def create_connection():
    # Update these parameters with your PostgreSQL connection details
    connection_params = {
        'host': const.HOST,
        'database': const.DATABASE,
        'user': const.USER,
        'password': const.PASSWORD,
    }

    try:
        # Create a connection
        connection = mysql.connector.connect(**connection_params)

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
            # You can perform database operations here

    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Create a table if it doesn't exist
def create_table_if_not_exists():
        # Connect to the database
    connection = create_connection()
    if connection is None:
        exit()

    # Create a cursor
    cursor = connection.cursor()

    table_creation_query = """
      CREATE TABLE IF NOT EXISTS research_papers (
        id INT AUTO_INCREMENT,
        Year VARCHAR(255),
        Title VARCHAR(255),
        Link VARCHAR(255),
        Authors VARCHAR(255),
        PRIMARY KEY (id)
    );
    """

    print("Database connection established. Creating table...")
    cursor.execute(table_creation_query)
    connection.commit()

    connection.close()
    cursor.close()
    

# Insert data into the table
def insert_data(data):
    # Connect to the database
    connection = create_connection()
    if connection is None:
        exit()

    # Create a cursor
    cursor = connection.cursor()
    # # Validate the data here (replace this with your validation logic)
    if data['Year'] is None or data['Title'] is None:
        print("Invalid data. Missing required fields.")
        return

    print(data['Title'])
    try:
        # Check if the data already exists
        check_query = "SELECT * FROM research_papers WHERE Title = %(Title)s AND Year = %(Year)s;"
        cursor.execute(check_query, data)
        existing_row = cursor.fetchone()

        if existing_row:
            print("Data already exists. Skipping insertion.")

        else:
            # Insert the data
            insert_query = """
                INSERT INTO research_papers (Year, Title, Link, Authors)
                VALUES (%(Year)s, %(Title)s, %(Link)s, %(Authors)s)
            """
            
            cursor.execute(insert_query, data)
            connection.commit()
            print("Data inserted successfully.")

    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()

# Function to search data in MySQL
def search_query(search_term):
    # Connect to the database
    connection = create_connection()
    if connection is None:
        exit()

    # Create a cursor
    cursor = connection.cursor()
    
    query = ("SELECT Year, Title, Link, Authors FROM research_papers"
             " WHERE Title LIKE %(search_term)s")
    
    data= {'search_term': f'%{search_term}%'}

    cursor.execute(query,  data)
    results = cursor.fetchall()

    connection.close()
    cursor.close()

    formatted_results = []
    for row in results:
        if isinstance(row, dict):
            formatted_result = {
                'year': row['Year'],
                'title': row['Title'],
                'link': row['Link'],
                'authors': row['Authors']
            }
        else:
            formatted_result = {
                'year': row[0],
                'title': row[1],
                'link': row[2],
                'authors': row[3]
            }

        formatted_results.append(formatted_result)


    return formatted_results