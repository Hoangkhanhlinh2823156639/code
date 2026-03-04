import hashlib
import datetime
import json

#Tài khoản
class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return self.__dict__

#BLOCK
class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

#Blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, self.get_latest_block().hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
            if self.chain[i].hash != self.chain[i].calculate_hash():
                return False
        return True


#Main
accounts = {}
blockchain = Blockchain()

while True:
    print("\n===== NGÂN HÀNG BLOCKCHAIN =====")
    print("1. Tạo tài khoản")
    print("2. Nạp tiền")
    print("3. Chuyển tiền")
    print("4. Xem số dư")
    print("5. Xem Blockchain")
    print("6. Kiểm tra Blockchain")
    print("0. Thoát")

    choice = input("Chọn: ")

    if choice == "1":
        name = input("Tên tài khoản: ")
        accounts[name] = Account(name)
        print("Tạo thành công!")

    elif choice == "2":
        name = input("Tên tài khoản: ")
        amount = float(input("Số tiền nạp: "))
        if name in accounts:
            accounts[name].balance += amount
            print("Nạp thành công!")
        else:
            print("Không tồn tại tài khoản!")

    elif choice == "3":
        sender = input("Người gửi: ")
        receiver = input("Người nhận: ")
        amount = float(input("Số tiền: "))

        if sender in accounts and receiver in accounts:
            if accounts[sender].balance >= amount:
                accounts[sender].balance -= amount
                accounts[receiver].balance += amount

                tx = Transaction(sender, receiver, amount)
                blockchain.add_block([tx])

                print("Chuyển tiền thành công!")
            else:
                print("Không đủ tiền!")
        else:
            print("Sai tài khoản!")

    elif choice == "4":
        name = input("Tên tài khoản: ")
        if name in accounts:
            print("Số dư:", accounts[name].balance)
        else:
            print("Không tồn tại!")

    elif choice == "5":
        for block in blockchain.chain:
            print("\nBlock:", block.index)
            print("Transactions:", [t.to_dict() for t in block.transactions])
            print("Hash:", block.hash)
            print("Previous:", block.previous_hash)

    elif choice == "6":
        if blockchain.is_valid():
            print("Blockchain hợp lệ!")
        else:
            print("Blockchain bị thay đổi!")

    elif choice == "0":
        break
    else:
        print("Chọn sai!")