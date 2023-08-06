from ClickHouse import ClickHouse

ch = ClickHouse(login='click', password='click')

t  = ch.check_connection_to_database()
print(t)