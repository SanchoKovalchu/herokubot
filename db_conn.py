import pymysql.cursors
# Функция возвращает connection.
def getConnection():
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='s2.thehost.com.ua',
                                 user='MySQLBot',
                                 password='MySQLBot1',
                                 db='WeatherTEST',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection