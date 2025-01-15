from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


# Объект Engine, отвечающий за все соединения
engine = create_engine("sqlite:///delivery.db", echo=True)

# Базовый класс
Base = declarative_base()

# Теперь объекты самой таблицы:

class Courier(Base):
    __tablename__ = 'couriers'
    
    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    second_name = Column(String)
    passport_number = Column(String)
    date_of_birth = Column(String)
    date_of_employment = Column(String)
    clock_in_time = Column(String)
    clock_out_time = Column(String)
    city = Column(String)
    street = Column(String)
    house_number = Column(Integer)
    apartment_number = Column(Integer)
    phone_number = Column(String)

class Transport(Base):
    __tablename__ = 'transport'

    number = Column(Integer, primary_key=True)
    model = Column(String)
    date_of_registration = Column(String)
    colour = Column(String)

class Sender(Base):
    __tablename__ = 'senders'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    second_name = Column(String)
    date_of_birth = Column(String)
    index = Column(Integer)
    city = Column(String)
    street = Column(String)
    house_number = Column(Integer)
    apartment_number = Column(Integer)
    phone_number = Column(String)

class Receiver(Base):
    __tablename__ = 'receivers'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    second_name = Column(String)
    date_of_birth = Column(String)
    index = Column(Integer)
    city = Column(String)
    street = Column(String)
    house_number = Column(Integer)
    apartment_number = Column(Integer)
    phone_number = Column(String)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)

    id_sender = Column(Integer, ForeignKey('senders.id'))
    sender = relationship('Sender')

    id_receiver = Column(Integer, ForeignKey('receivers.id'))
    receiver = relationship('Receiver')

    date_of_order = Column(String)
    date_of_delivery = Column(String)
    price_of_delivery = Column(Float)
    
    id_courier = Column(Integer, ForeignKey('couriers.id'))
    courier = relationship('Courier')

    transport_number = Column(Integer, ForeignKey('transport.number'))
    transport = relationship('Transport')

# Метаданные
Base.metadata.create_all(engine)

# Сессия
Session = sessionmaker(bind=engine) 
session = Session()

# Создание записей:

sender1 = Sender(id=1, surname='Ivanov', name='Ivan', second_name='Ivanovich', date_of_birth='02.02.2002', index=891289, city='Moscow', street='Krasnaya', house_number=59, apartment_number=201, phone_number='+78005553535')
session.add(sender1)

sender2 = Sender(id=2, surname='Jackson', name='Samuel', second_name='Leroy', date_of_birth='21.12.1948', index=503290, city='Los Angeles', street='Babcock Avenue', house_number=26, apartment_number=151, phone_number='589341121')
session.add(sender2)

receiver1 = Receiver(id=1, surname='Dmitriev', name='Dmitry', second_name='Dmitrievich', date_of_birth='03.03.2003', index=471122, city='Saint Petersburg', street='Lesnaya', house_number=124, apartment_number=41, phone_number='+750940231')
session.add(receiver1)

receiver2 = Receiver(id=2, surname='Simmons', name='Jonathan', second_name='Kimble', date_of_birth='09.01.195', index=589012, city='Grosse Pointe', street='Baker Street', house_number=19, apartment_number=55, phone_number='220402141')
session.add(receiver2)

session.commit()

order1 = Order(id=1, id_sender=1, id_receiver=2, date_of_order='20.10.24', date_of_delivery='20.11.24', price_of_delivery=150, id_courier=1, transport_number=50918)
session.add(order1)

order2 = Order(id=2, id_sender=1, id_receiver=1, date_of_order='18.10.24', date_of_delivery='22.11.24', price_of_delivery=200, id_courier=1, transport_number=50918)
session.add(order2)

session.commit()

