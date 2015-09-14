import psycopg2
import pickle
import csv

def pickle_stuff(filename, data):
    ''' open file '''
    with open(filename, 'w') as picklefile:
        pickle.dump(data, picklefile)

def unpickle(filename):
    ''' save file '''
    with open(filename, 'r') as picklefile:
        old_data = pickle.load(picklefile)
    return old_data

def make_recs_table(cur, conn):
    cur.execute("CREATE TABLE recs ( id serial PRIMARY KEY, track_id text UNIQUE NOT NULL, title text, artist text, recommend integer, cluster integer);")
    conn.commit()

def populate_recs_table(cur, conn, infofile):
    #for cn in class_names:
    with open(infofile, 'r') as infocsv:
        infocsv.next() #get rid of headers
        inforeader = csv.reader(infocsv, delimiter=',')
        for row in inforeader:
            #print row
            vals = tuple(row)
            cur.execute("INSERT INTO recs VALUES ( %s, '%s', '%s', '%s', %s, %s );" %vals)
    conn.commit()

if __name__ == "__main__":

    params = unpickle("params.pkl")
    
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    make_recs_table(cur, conn)
    populate_recs_table(cur, conn, "./pkls/trackinfo.csv")

    cur.close()
    conn.close()

