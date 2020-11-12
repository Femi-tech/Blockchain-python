import subprocess
import json
import os
from constants import *
from dotenv import load_dotenv
from web3 import Web3
from pathlib import Path
from getpass import getpass
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware

load_dotenv()

from eth_account import Account



def derive_wallets(mnemonic, coin, numderive):
    command = f'php ./hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json' 
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    keys = json.loads(output)
    return  keys
#Generate accounts and keys for coin in coins
keys = {}
coins = {"eth","btc-test"}
mnemonic = os.getenv('MNEMONIC_KEY')
numderives = 3

for coin in coins:
    keys[coin]= derive_wallets(mnemonic, coin, numderive=2)




w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#coins= { ETH: derive_wallets(coin = ETH), BTCTEST: derive_wallets(coin =BTCTEST)}

#Priv_key_to_account function
eth_PrivateKey = keys["eth"][0]['privkey']
btc_PrivateKey = keys['btc-test'][0]['privkey']
print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))

def priv_key_to_account(coin,priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate=w3.eth.estimateGas(
        {"from":account.address,"to":recipient,"value":amount}
        )
        return {
            "from":account.address,
            "to":recipient,
            "value":amount,
            "gasPrice":w3.eth.gasPrice,
            "gas":gasEstimate,
            "nonce":w3.eth.getTransactionCount(account.address),
            }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


def send_tx(coin,account, to, amount):
    tx = create_tx(coin, account, to, amount)
    if coin == ETH:
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()

    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, to, amount)
    if coin == ETH:
        signed_tx = account.sign_transaction(tx)
        signed_tx = account.sign_transaction(tx)
        print(signed_tx)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
#create account
eth_acc = priv_key_to_account(ETH, eth_PrivateKey)
btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)

#Example of using functions to send BTC-test 
create_tx(BTCTEST,btc_acc,"0x8d6F0115E6565Bb5659c614FC590Ea26D0bC7151", 0.000000001)
send_tx(BTCTEST,btc_acc,"0x8d6F0115E6565Bb5659c614FC590Ea26D0bC7151", 0.000000001)

#Example of using functions to send ETH
create_tx(ETH,eth_acc,"0x8d6F0115E6565Bb5659c614FC590Ea26D0bC7151", 0.00001)
send_tx(ETH,eth_acc,"0x8d6F0115E6565Bb5659c614FC590Ea26D0bC7151", 0.00001)


print(eth_key.get_transactions())

print(btc_key.get_transactions())
