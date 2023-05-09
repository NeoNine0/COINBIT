import hashlib
import datetime

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = str(self.timestamp) + str(self.data) + str(self.previous_hash)
        block_hash = hashlib.sha256(block_contents.encode()).hexdigest()
        return block_hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def new_block(self, data):
        previous_block = self.get_last_block()
        previous_hash = previous_block.hash
        new_block = Block(data, previous_hash)
        self.chain.append(new_block)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def proof_of_work(self, block, difficulty):
        nonce = 0
        block.nonce = nonce
        hash_output = block.calculate_hash()

        while hash_output[:difficulty] != "0" * difficulty:
            nonce += 1
            block.nonce = nonce
            hash_output = block.calculate_hash()

        return hash_output

    def add_transaction(self, sender, recipient, amount):
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        self.transactions.append(transaction)

    def mine_block(self, miner_address, difficulty):
        reward = 1
        self.add_transaction("0", miner_address, reward)

        last_block = self.get_last_block()
        new_block = Block(self.transactions, last_block.hash)
        proof = self.proof_of_work(new_block, difficulty)
        new_block.hash = proof
        self.chain.append(new_block)

        self.transactions = []

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for transaction in block.data:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
                elif transaction["recipient"] == address:
                    balance += transaction["amount"]

        return balance
