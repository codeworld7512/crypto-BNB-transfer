from web3 import Web3
bsc = "https://bsc-dataseed.binance.org/bnb"
w3 = Web3(Web3.HTTPProvider(bsc))
print(w3.isConnected())

account_1 = "0xFF76Fe18ad1312EF9d90d786E6E3Af923E04B870"
account_2 = "0x69bF8D17c11031948abFb3ac60ea421f0eFE8CAd"

balance = w3.eth.get_balance(account_1)
readable = w3.fromWei(balance,'ether')
print(balance)

nonce = w3.eth.getTransactionCount(account_1)
tx = {
    'chainId':4,
    'nonce':nonce,
    'to':account_2,
    'value': 5000,
    'gas':21000,
    'gasPrice':w3.toWei('5','gwei')
}

signed_tx = w3.eth.account.signTransaction(tx, '0x45ee35fdaaa67bbdefd0857b8a821f1f6bd49149901f7536f5130c9ee69a0b9b')

try:
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(w3.toHex(tx_hash))
except Exception as e:
    print(e)

# my_account = w3.eth.account.create('test account')
# print(my_account._address)
# print(my_account._private_key)