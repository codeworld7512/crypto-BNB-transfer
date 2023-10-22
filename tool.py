from web3 import Web3
import sys, os
import math
import random
import json

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

FORM_CLASS,_ = loadUiType(resource_path("Tool.ui"))

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.Handle_Buttons()
        self.token_filename = False
        
    def Handle_Buttons(self):
        self.WalletsButton.clicked.connect(self.GET_WALLETS)
        self.StartButton.clicked.connect(self.START_SENDING)
        self.TokenButton.clicked.connect(self.GET_TOKEN_INFO)

    def GET_TOKEN_INFO(self) :
        path = QFileDialog.getOpenFileName()
        self.token_filename = path[0]
        basename =self.token_filename.split("/")
        self.TokenLabel.setText(basename[len(basename)-1])

    def GET_WALLETS(self) :
        path = QFileDialog.getOpenFileName()
        self.filename = path[0]
        basename =self.filename.split("/")
        self.FilenameLabel.setText(basename[len(basename)-1])
    
    def START_SENDING(self) :
        fromAddress =  self.WalletLineEdit.text()
        private_key = self.PrivateKeyEditText.text()
        amount = 0
        if self.FixedRadioButton.isChecked() == True :
            amount = int(self.FixedLineEdit.text())
        else:
            fromAmount = int(self.FromLineEdit.text())
            toAmount = int(self.ToLineEdit.text())
            amount = math.floor(random.random() * (toAmount - fromAmount)) + toAmount
        print(fromAddress)
        print(private_key)

        Lines = []
        if self.token_filename:
            tokenFile = open(self.token_filename, 'r')
            Lines = tokenFile.readlines()

        tokenAddress = ''
        tokenAbi = ''
        if len(Lines) == 2:
            tokenAddress = Lines[0]
            tokenAbi = Lines[1]

        walletFile = open(self.filename, 'r')
        Lines = walletFile.readlines()

        chainId = 56 
        bsc = "https://bsc-dataseed1.binance.org:443"

        # chainId = 97 
        # bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"

        web3 = Web3(Web3.HTTPProvider(bsc))        

        gasPrice = web3.toWei('10','gwei')

        for line in Lines:
            try:
                toAddress = line.replace("\n", "")
                nonce = web3.eth.getTransactionCount(fromAddress)
                transaction = {}
                if tokenAddress:
                    # web3.eth.defaultAccount = web3.eth.accounts[0]
                    contract = web3.eth.contract(address=tokenAddress, abi=json.loads(tokenAbi))
                    print("1")
                    transaction = contract.functions.transfer(toAddress, amount).buildTransaction({
                        'chainId': chainId,
                        'from': fromAddress,
                        'nonce': nonce,
                        'value': int(amount),
                        'gas': 21000,
                        'gasPrice': gasPrice
                        })
                    print("2")
                else:
                    transaction = {
                        'chainId': chainId,
                        'nonce': nonce,
                        'to': toAddress,
                        'value': int(amount),
                        'gas': 21000,
                        'gasPrice': gasPrice
                    }
                signed_tx = web3.eth.account.signTransaction(transaction, private_key)            
                tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                trans = web3.toHex(tx_hash)
                transaction = web3.eth.get_transaction(trans)
                self.LogsTextEdit.appendPlainText("To : {}, Status : Success\n".format(toAddress))
            except Exception as e:
                self.LogsTextEdit.appendPlainText("To : {}, Status : Fail, {}\n".format(toAddress, str(e)))

def main():
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main() 

# print("---------------------------------------------------------------------------------------")
# # bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"

# print(' 1. mainnet(default)')
# print(' 2. testnet')
# bscType = input(" Enter net type or press enter to keep it default : ")
# chainId = 56
# bsc = "https://bsc-dataseed1.binance.org:443"
# if bscType == "2":
#     bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
#     chainId = 97

# print(" Connecting...", end = "\r")

# web3 = Web3(Web3.HTTPProvider(bsc))
# if (web3.isConnected()) == False:
#     print(" Not connected!")
#     sys.exit()
# else:
#     print(" Connected to BEP20 (BSC) network")

# account_1 = input(" Enter from Address : ")
# private_key = input(" Enter private key of from address : ")
# # private_key = "0x45ee35fdaaa67bbdefd0857b8a821f1f6bd49149901f7536f5130c9ee69a0b9b"

# print(" Checking balance...", end = "\r")
# balance = web3.eth.get_balance(account_1)
# print(" Balance: {}        ".format(balance))

# account_2 = input(" Enter to Address : ")

# print(' 1. Random set From and To amounts ( from 1000 to 10000 )')
# print(' 2. Fixed set the exact amount ( 5000 )')
# amountType = input("Enter amount type : ")
# amount = 5000
# if amountType == "1":
#     amount = math.floor(random.random() * 10000)

# gasPrice = int(web3.toWei('5','gwei'))

# # if balance > amount + gasPrice: # min BNB tax - 5 GWEI

# gas = 21000 # gasLimit
# gwei = 5 # gasPrice in gwei

# nonce = web3.eth.getTransactionCount(account_1)
# transaction = {
#     'chainId': chainId,
#     'nonce': nonce,
#     'to': account_2,
#     'value': int(amount),
#     'gas': 21000,
#     'gasPrice': web3.toWei('10','gwei')
# }

# signed_tx = web3.eth.account.signTransaction(transaction, private_key)
# try:
#     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#     trans = web3.toHex(tx_hash)
#     transaction = web3.eth.get_transaction(trans)
#     print("Transaction: {}".format(transaction))    
#     print("DONE! Signed transaction has been sent to the blockchain.")
# except Exception as e:
#     print(e)
# else:
    # print("The balance is less than {}".format((amount + gasPrice)))