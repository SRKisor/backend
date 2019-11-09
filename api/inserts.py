from datetime import date

from api.database import db_session

from api.items.models import Items
from api.distributors.models import Distributors
from api.clients.models import Clients
from api.payments.models import Payment_Types, Payment_Methods, Payments
from api.bill.models import Bills
from api.users.models import User, Role, RolesUsers

# When adding object contaning another object, In the first object there should be
# backref to second object. For more information see Payment model.

# Execute these commands in 'flask shell'


item1 = Items(item_code=100, name="Baby Soap", qty=10, retail_price=45,
              wholesale_price=40, mfd_date=date(2019, 4, 20), exp_date=date(2020, 4, 20))
item2 = Items(item_code=101, name="Rice", qty=100, retail_price=80,
              wholesale_price=75, mfd_date=date(2019, 6, 15), exp_date=date(2020, 6, 1))
item3 = Items(item_code=102, name="Sugar", qty=5, retail_price=120,
              wholesale_price=110, mfd_date=date(2019, 8, 1), exp_date=date(2020, 8, 1))

db_session.add(item1)
db_session.add(item2)
db_session.add(item3)
db_session.commit()

distributor1 = Distributors(
    name="Distributor 1", address="Address 1", telephone="123456789", email="admin@admin.com")

distributor2 = Distributors(name="Distributor 2", address="Address 2",
                            telephone="123456789", email="admin@admin.com")

distributor3 = Distributors(name="Distributor 3", address="Address 3",
                            telephone="123456789", email="admin@admin.com")

db_session.add(distributor1)
db_session.add(distributor2)
db_session.add(distributor3)
db_session.commit()

client1 = Clients(name="Client 1", address="Address 1",
                  telephone="123456789", email="admin@admin.com")

client2 = Clients(name="Client 2", address="Address 2",
                  telephone="123456789", email="admin@admin.com")

client3 = Clients(name="Client 3", address="Address 3",
                  telephone="123456789", email="admin@admin.com")

db_session.add(client1)
db_session.add(client2)
db_session.add(client3)
db_session.commit()

payment_type1 = Payment_Types(type_name="Bill Payment")
payment_type2 = Payment_Types(type_name="Invoice Payment")
payment_type3 = Payment_Types(type_name="Distributor Payment")

db_session.add(payment_type1)
db_session.add(payment_type2)
db_session.add(payment_type3)
db_session.commit()

payment_method1 = Payment_Methods(method_name="Cash Payment")
payment_method2 = Payment_Methods(method_name="Cheque")
payment_method3 = Payment_Methods(method_name="Credit Card")
payment_method4 = Payment_Methods(method_name="Paypal")

db_session.add(payment_method1)
db_session.add(payment_method2)
db_session.add(payment_method3)
db_session.add(payment_method4)
db_session.commit()

payment1 = Payments(date=date(2019, 10, 10), due_date=date(2019, 10, 30), amount=10000,
                    paid=False, payment_types=payment_type1, payment_methods=payment_method1)
payment2 = Payments(date=date(2019, 5, 1), due_date=date(2019, 5, 1), amount=20000,
                    paid=True, payment_types=payment_type3, payment_methods=payment_method3)
payment3 = Payments(date=date(2019, 7, 15), due_date=date(2019, 7, 15), amount=30000,
                    paid=False, payment_types=payment_type2, payment_methods=payment_method4)


db_session.add(payment1)
db_session.add(payment2)
db_session.add(payment3)
db_session.commit()

bill1 = Bills(bill_number="100", client=client1, cashier="Cashier 1",
              paid=False, date=date(2019, 10, 15), amount=10000)
bill2 = Bills(bill_number="101", client=client3, cashier="Cashier 1",
              paid=False, date=date(2019, 10, 15), amount=10000)
bill3 = Bills(bill_number="102", client=client2, cashier="Cashier 1",
              paid=False, date=date(2019, 10, 15), amount=10000)

db_session.add(bill1)
db_session.add(bill2)
db_session.add(bill3)
db_session.commit()

role1 = Role(name="admin", description="Administration Privileges")
role2 = Role(name="user", description="User Privileges")

db_session.add(role1)
db_session.add(role2)
db_session.commit()

user1 = User(email="admin@admin.com", username="admin",
             password="$2b$12$JhqH7FrewPUE54uKRuZ7xukkwr0Tj1ZUtaqQe/M.p.WDQF.QMti7C")
user2 = User(email="user@user.com", username="user",
             password="$2b$12$cZaCVMjqM86ofALQgzlyiuqUybgZhEQDba2SIGg9yOlCZdBL6.oPC")

db_session.add(user1)
db_session.add(user2)
db_session.commit()

role_user1 = RolesUsers(user=user1, role=role1)
role_user2 = RolesUsers(user=user2, role=role2)

db_session.add(role_user1)
db_session.add(role_user2)
db_session.commit()
