from sqlpipe import SqlPipeBuilder

if __name__ == "__main__":
    con_str = 'postgres://user:pass@host:port/dbname'
    pipe = SqlPipeBuilder(con_str, connections_limit=5)
    pipe.map_directory('queries')
    pipe.execute()
