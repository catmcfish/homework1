import mysql.connector
import glob
import json
import csv
import os
from io import StringIO
import itertools
import datetime
class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query="SELECT CURDATE()", parameters=None):
        """Execute a database query with proper error handling and result management.
        
        Args:
            query (str): SQL query to execute
            parameters (tuple, optional): Parameters for the query
            
        Returns:
            list: Query results as a list of dictionaries
        """
        cnx = None
        cur = None
        try:
            cnx = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
                charset='utf8mb4',
                allow_local_infile=True
            )
            cur = cnx.cursor(dictionary=True)
            
            # Execute the statement
            if parameters is not None:
                cur.execute(query, parameters)
            else:
                cur.execute(query)
            
            # Commit the transaction for INSERT, UPDATE, DELETE operations
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                cnx.commit()
                if cur.lastrowid:
                    return [{'LAST_INSERT_ID()': cur.lastrowid}]
                return []
            
            # For SELECT and other operations that return results
            try:
                result = cur.fetchall()
                return result if result else []
            except mysql.connector.Error as fetch_err:
                # Some statements don't return results
                return []
            
        except mysql.connector.Error as err:
            if cnx:
                cnx.rollback()
            print(f"Database error: {err}")
            raise
        except Exception as e:
            print(f"Unexpected error in query: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if cnx and cnx.is_connected():
                cnx.close()

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path='flask_app/database/'):
        """Create database tables and populate them with initial data.
        
        Args:
            purge (bool): If True, drop existing tables before creating new ones
            data_path (str): Path to the database files directory
        """
        try:
            if purge:
                # Drop tables one by one in reverse dependency order
                self.query("DROP TABLE IF EXISTS skills")
                self.query("DROP TABLE IF EXISTS experiences")
                self.query("DROP TABLE IF EXISTS positions")
                self.query("DROP TABLE IF EXISTS institutions")
                self.query("DROP TABLE IF EXISTS feedback")

            # Create tables in order of dependencies
            table_order = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql', 'feedback.sql']
            for table_file in table_order:
                file_path = os.path.join(data_path, 'create_tables', table_file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        sql = file.read()
                        if sql.strip():  # Only execute if SQL is not empty
                            # Split and execute each statement separately
                            statements = [s.strip() for s in sql.split(';') if s.strip()]
                            for stmt in statements:
                                self.query(stmt)

            # Define the order for data insertion to respect foreign key constraints
            data_order = ['institutions', 'positions', 'experiences', 'skills', 'feedback']
            
            # Store all data first to handle foreign key relationships
            data_cache = {}
            for table in data_order:
                csv_path = os.path.join(data_path, 'initial_data', f'{table}.csv')
                if os.path.exists(csv_path):
                    with open(csv_path, 'r') as file:
                        csv_data = list(csv.DictReader(file))
                        data_cache[table] = csv_data
            
            # Insert data in the correct order
            for table in data_order:
                if table in data_cache:
                    rows_to_insert = []
                    for row in data_cache[table]:
                        # Handle NULL values
                        processed_row = {k: None if v == 'NULL' else v 
                                       for k, v in row.items()}
                        columns = list(processed_row.keys())
                        values = [processed_row[col] for col in columns]
                        rows_to_insert.append(values)
                    
                    if rows_to_insert:
                        try:
                            self.insertRows(table, columns, rows_to_insert)
                        except Exception as e:
                            print(f"Error inserting into {table}: {e}")
                            raise

        except Exception as e:
            print(f"Error in createTables: {e}")
            raise


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        """Insert multiple rows into a table efficiently using batch insert.

        Args:
            table (str): Name of the table to insert into
            columns (list): List of column names
            parameters (list): List of value lists to insert

        Returns:
            list: List of inserted row IDs
        """
        if not parameters:
            return []

        try:
            # For single row insertion, use a simpler approach
            if len(parameters) == 1:
                placeholders = '(' + ', '.join(['%s'] * len(columns)) + ')'
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES {placeholders}"
                
                # Execute single row insert
                result = self.query(query, parameters[0])
                
                # Return the inserted ID if available
                if result and isinstance(result, list) and len(result) > 0:
                    return [result[0].get('LAST_INSERT_ID()', None)]
                return []
            else:
                # Build the INSERT query for batch insert
                placeholders = ', '.join(['(%s)' % ', '.join(['%s'] * len(columns))] * len(parameters))
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES {placeholders}"
                
                # Flatten parameters for batch insert
                flat_params = [val for param_set in parameters for val in param_set]
                
                # Execute batch insert
                result = self.query(query, flat_params)
                
                # Get the ID of the first inserted row
                if result and isinstance(result, list) and len(result) > 0:
                    first_id = result[0].get('LAST_INSERT_ID()', None)
                    if first_id:
                        # Return list of all inserted IDs
                        return list(range(first_id, first_id + len(parameters)))
                return []
            
        except mysql.connector.Error as err:
            print(f"Error inserting rows into {table}: {err}")
            if err.errno == 1452:  # Foreign key constraint failure
                print(f"Foreign key constraint failed. Make sure referenced records exist.")
            elif err.errno == 1062:  # Duplicate entry
                print(f"Duplicate entry found. The record may already exist.")
            raise


    def getResumeData(self):
        """Retrieve complete resume data with all related information efficiently using JOINs.

        Returns:
            dict: Hierarchical structure of resume data organized by institution
        """
        try:
            # Get all data in a single query using JOINs
            query = """
                SELECT 
                    i.*, 
                    p.position_id, p.title, p.responsibilities, 
                    p.start_date as position_start, p.end_date as position_end,
                    e.experience_id, e.name as experience_name, e.description, 
                    e.hyperlink, e.start_date as exp_start, e.end_date as exp_end,
                    s.skill_id, s.name as skill_name, s.skill_level
                FROM institutions i
                LEFT JOIN positions p ON i.inst_id = p.inst_id
                LEFT JOIN experiences e ON p.position_id = e.position_id
                LEFT JOIN skills s ON e.experience_id = s.experience_id
                ORDER BY 
                    i.inst_id, 
                    p.start_date DESC, 
                    e.start_date DESC, 
                    s.skill_level DESC
            """
            
            rows = self.query(query)
            
            # Initialize the result structure
            result = {}
            
            # Process each row and build the hierarchical structure
            for row in rows:
                inst_id = row['inst_id']
                pos_id = row['position_id']
                exp_id = row['experience_id']
                skill_id = row['skill_id']
                
                # Initialize institution if not exists
                if inst_id not in result:
                    result[inst_id] = {
                        'inst_id': inst_id,
                        'type': row['type'],
                        'name': row['name'],
                        'department': row['department'],
                        'address': row['address'],
                        'city': row['city'],
                        'state': row['state'],
                        'zip': row['zip'],
                        'positions': {}
                    }
                
                # Skip if no position (empty institution)
                if pos_id is None:
                    continue
                    
                # Initialize position if not exists
                if pos_id not in result[inst_id]['positions']:
                    result[inst_id]['positions'][pos_id] = {
                        'position_id': pos_id,
                        'title': row['title'],
                        'responsibilities': row['responsibilities'],
                        'start_date': row['position_start'],
                        'end_date': row['position_end'],
                        'experiences': {}
                    }
                
                # Skip if no experience (empty position)
                if exp_id is None:
                    continue
                    
                # Initialize experience if not exists
                if exp_id not in result[inst_id]['positions'][pos_id]['experiences']:
                    result[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                        'experience_id': exp_id,
                        'name': row['experience_name'],
                        'description': row['description'],
                        'hyperlink': row['hyperlink'],
                        'start_date': row['exp_start'],
                        'end_date': row['exp_end'],
                        'skills': {}
                    }
                
                # Skip if no skill (empty experience)
                if skill_id is None:
                    continue
                    
                # Add skill
                result[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                    'skill_id': skill_id,
                    'name': row['skill_name'],
                    'skill_level': row['skill_level']
                }
            
            return result
            
        except mysql.connector.Error as err:
            print(f"Database error in getResumeData: {err}")
            raise
        except Exception as e:
            print(f"Unexpected error in getResumeData: {e}")
            raise

    def getFeedbackData(self, only_displayed=True):
        """Retrieve feedback data from the database.

        Args:
            only_displayed (bool): If True, only return feedback marked for display

        Returns:
            list: List of feedback entries ordered by creation time
        """
        try:
            query = """
                SELECT 
                    comment_id,
                    name,
                    email,
                    comment,
                    created_at,
                    is_displayed
                FROM feedback
                WHERE 1=1
            """
            
            if only_displayed:
                query += " AND is_displayed = TRUE"
                
            query += " ORDER BY created_at DESC"
            
            return self.query(query)
            
        except mysql.connector.Error as err:
            print(f"Database error in getFeedbackData: {err}")
            raise
        except Exception as e:
            print(f"Unexpected error in getFeedbackData: {e}")
            raise

    def addFeedback(self, name, email, comment):
        """Add a new feedback entry to the database.

        Args:
            name (str): Name of the person providing feedback
            email (str): Email address of the person
            comment (str): The feedback comment

        Returns:
            int: ID of the newly created feedback entry
        """
        try:
            # Validate inputs
            if not name or not email or not comment:
                raise ValueError("Name, email, and comment are required")
                
            # Basic email validation
            if '@' not in email or '.' not in email:
                raise ValueError("Invalid email format")
                
            # Insert the feedback
            query = """
                INSERT INTO feedback (name, email, comment)
                VALUES (%s, %s, %s)
            """
            
            result = self.query(query, [name, email, comment])
            
            # Get the ID of the inserted feedback
            if result and isinstance(result, list) and len(result) > 0:
                return result[0].get('LAST_INSERT_ID()')
            return None
            
        except mysql.connector.Error as err:
            print(f"Database error in addFeedback: {err}")
            raise
        except Exception as e:
            print(f"Error in addFeedback: {e}")
            raise
