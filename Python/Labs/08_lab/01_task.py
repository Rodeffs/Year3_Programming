import sqlite3 as sq


def main():
    
    # Создаём БД и устанавливаем соединение
    conn = sq.connect("delivery.db")

    # Курсор
    cur = conn.cursor()
    
    # Создание таблицы через SQL запрос:
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Couriers(
                id_courier INT PRIMARY KEY,
                surname TEXT,
                name TEXT,
                second_name TEXT,
                passport_number TEXT,
                date_of_birth TEXT,
                date_of_employment TEXT,
                clock_in_time TEXT,
                clock_out_time TEXT,
                city TEXT,
                street TEXT,
                house_number INT,
                apartment_number INT,
                phone_number TEXT
                );
                """)
    # Номер паспорта может начинаться с нуля, т.е. если сделать через int, то 0100 и 100 одно и то же, а это неверно
    # Номер телефона может включать в себя: +, -, пробелы
    
    # Внесение изменений
    conn.commit()
    
    # Аналогично для второй таблицы:
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Transport(
                vehicle_number INT PRIMARY KEY,
                vehicle_model TEXT,
                date_of_registration TEXT,
                colour TEXT
                );
                """)

    conn.commit()

    # Внесение данных
    cur.execute("""
                INSERT INTO Couriers(id_courier, surname, name, second_name, passport_number, date_of_birth, date_of_employment, clock_in_time, clock_out_time, city, street, house_number, apartment_number, phone_number)
                VALUES('1', 'House', 'Robert', 'Edwin', '77738', '25.05.2020', '20.11.2274', '09:00', '17:00', 'Las Vegas', 'Las Vegas Strip', '38', '1', '478901');
                """)

    conn.commit()

    cur.execute("""
                INSERT INTO Transport(vehicle_number, vehicle_model, date_of_registration, colour)
                VALUES('50918', 'Highwayman', '20.11.2024', 'red');
                """)

    conn.commit()

    # Изменение данных
    cur.execute("""
                UPDATE Transport SET colour = 'black' WHERE vehicle_number = 50918; 
                """)

    conn.commit()

    # Закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()
