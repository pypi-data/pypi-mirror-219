from PostgreSQL import PostgreSQL

pg = PostgreSQL(port=1)

# df = pg.execute_to_df('select 1 as one')

# check = pg.check_connection_to_database()

# print(check)

# pg.generate_on_conflict_sql_query(
#     # source_table_schema_name='stg',
#     source_table_name='tmp_test_pk',
#     # target_table_schema_name='dds',
#     target_table_name='test_pk',
#     list_columns=['id', 'value'],
#     # pk=['id','username'],
#     replace=True
# )

t = pg.check_connection_to_database()

print(t)
