vals = {}
#(username, password, host, database)
with open("params.csv", 'r') as pf:
    for line in pf:
        kvs = line.strip().split(",")
        vals[kvs[0]] = kvs[1]       
params = (vals["user"], vals["password"], vals["host"], vals["database"])
