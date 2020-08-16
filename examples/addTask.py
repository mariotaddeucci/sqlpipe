from sqlpipe import SqlPipeBuilder

if __name__ == "__main__":
    con_str = 'postgres://user:pass@host:port/dbname'
    pipe = SqlPipeBuilder(con_str, connections_limit=5)

    pipe.add_task(
        id='id_2',
        script='queries/data/foo.sql',
        file=True,
        parent_id='id_1'
    )
    pipe.add_task(
        sid='id_1',
        script='queries/tables/t1.sql',
        file=True
    )
    pipe.add_task(
        id='id_4',
        script='insert into t2 values (4), (5);',
        parent_id='id_3'
    )
    pipe.add_task(
        id='id_3',
        script='drop table if exists t2; create table t2 (bar int);'
    )
    pipe.execute()
