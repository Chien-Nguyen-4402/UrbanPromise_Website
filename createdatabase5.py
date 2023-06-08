import alpha_database as database5
import sys

import sqlalchemy
import sqlalchemy.orm
import os

def main():

    DATABASE_URL_ = os.getenv('DATABASE_URL')
    DATABASE_URL_ =  DATABASE_URL_.replace('postgres://', 'postgresql://')
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL_)

        database5.Base.metadata.drop_all(engine)
        database5.Base.metadata.create_all(engine)

        engine.dispose()

    except Exception as ex:
        print(ex,file=sys.stderr)
        sys.exit(1)
if __name__=='__main__':
    main()
