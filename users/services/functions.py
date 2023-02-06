import csv
from faker import Faker
from eth_account import Account

fake = Faker()

def main():
    with open("users1.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["user_name", "ethereum_address"])
        for _ in range(128):
            user_name = fake.name()
            ethereum_address = Account.create().address
            writer.writerow([user_name, ethereum_address])

def get_addresses_from_csv(file_name):
    addresses = []
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader) # skip the header
        for row in reader:
            addresses.append(row[1])
    return addresses

if __name__ == "__main__":
    main()
    a = get_addresses_from_csv("users1.csv")
    print(a)
