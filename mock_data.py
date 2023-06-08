import sqlite3
import contextlib as cl 

DATABASE_URL= 'file:database1.sqlite?mode=rw'
ALLTABLES = ['administrator','course_offerings','student_enrollment_request',
             'students','tutor_availability','tutor_teaching_request','tutors']

def create_request(line): 
    typevals = line.split(' ',1)
    values = typevals[1].split(' ')
    request2 = '('
    for value in values: 
        request2+= value 
        if(value != values[len(values)-1]): 
            request2+=','
    request2+=')'
    return [typevals[0], request2]

def insert(): 
    
    with sqlite3.connect(DATABASE_URL, isolation_level=None,
        uri= True) as connection: 
        with cl.closing(connection.cursor()) as cursor: 
            with open('mock_data','r') as mock_data: 
                mock_lines = mock_data.readlines()
                for line in mock_lines: 
                    request = create_request(line)
                    stmt = "INSERT INTO "+request[0]+" VALUES "+request[1]
                    cursor.execute(stmt)

def clear_tables(): 
    stmt = "DELETE FROM "
    with sqlite3.connect(DATABASE_URL, isolation_level=None,
        uri= True) as connection: 
        with cl.closing(connection.cursor()) as cursor: 
            for table in ALLTABLES: 
                cursor.execute(stmt +table)
def main(): 
   clear_tables()
   insert()
   

if __name__ == '__main__': 
    main()