# Blockchain-python

## Setup


1.Create a project directory called wallet and cd into it.


2. Clone the hd-wallet-derive tool into this folder and install it using the instructions on its README.md.

 a. git clone https://github.com/dan-da/hd-wallet-derive
 
 b. cd hd-wallet-derive
 
 c. php -r "readfile('https://getcomposer.org/installer');" | php
 
 d. php composer.phar install



3. Create a symlink called derive for the hd-wallet-derive/hd-wallet-derive.php script into the top level project
directory like so: ln -s hd-wallet-derive/hd-wallet-derive.php derive
This will clean up the command needed to run the script in our code, as we can call ./derive
instead of ./hd-wallet-derive/hd-wallet-derive.php.


4. Test that you can run the ./derive script properly, use one of the examples on the repo's README.md


5. Create a file called wallet.py -- this will be your universal wallet script. You can use this starter code as a starting point.





## Setup constants


1. In a separate file, constants.py, set the following constants:

BTC = 'btc'
ETH = 'eth'
BTCTEST = 'btc-test'



2. In wallet.py, import all constants: from constants import *


3.Use these anytime you reference these strings, both in function calls, and in setting object keys.




## Generate a Mnemonic


1. Generate a new 12 word mnemonic using hd-wallet-derive or by using this tool.


2. Set this mnemonic as an environment variable, and include the one you generated as a fallback using:
mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here')


## Deriving the wallet keys


1. Use the subprocess library to call the ./derive script from Python. Make sure to properly wait for the process.


2. The following flags must be passed into the shell command as variables:

3. Mnemonic (--mnemonic) must be set from an environment variable, or default to a test mnemonic
Coin (--coin)
Numderive (--numderive) to set number of child keys generated



4. Set the --format=json flag, then parse the output into a JSON object using json.loads(output)


5. You should wrap all of this into one function, called derive_wallets


6. Create an object called coins that derives ETH and BTCTEST wallets with this function.
When done properly, the final object should look something like this (there are only 3 children each in this image):


![derive](screenshots/derive function.png)


## Linking the transaction signing libraries

Now, we need to use bit and web3.py to leverage the keys we've got in the coins object.
You will need to create three more functions:


1. priv_key_to_account -- this will convert the privkey string in a child key to an account object
that bit or web3.py can use to transact.
This function needs the following parameters:


coin -- the coin type (defined in constants.py).

priv_key -- the privkey string will be passed through here.

You will need to check the coin, then return one of the following functions based on the library:

For ETH, return Account.privateKeyToAccount(priv_key)

This function returns an account object from the private key string. You can read more about this object here.


2. For BTCTEST, return PrivateKeyTestnet(priv_key)

This is a function from the bit libarary that converts the private key string into a WIF (Wallet Import Format) object. WIF is a special format bitcoin uses to designate the types of keys it generates.
You can read more about this function here.





3. create_tx -- this will create the raw, unsigned transaction that contains all metadata needed to transact.
This function needs the following parameters:


coin -- the coin type (defined in constants.py).

account -- the account object from priv_key_to_account.

to -- the recipient address.

amount -- the amount of the coin to send.

You will need to check the coin, then return one of the following functions based on the library:

4. For ETH, return an object containing to, from, value, gas, gasPrice, nonce, and chainID.
Make sure to calculate all of these values properly using web3.py!
For BTCTEST, return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])




5. send_tx -- this will call create_tx, sign the transaction, then send it to the designated network.
This function needs the following parameters:


coin -- the coin type (defined in constants.py).

account -- the account object from priv_key_to_account.

to -- the recipient address.

amount -- the amount of the coin to send.

6. You may notice these are the exact same parameters as create_tx. send_tx will call create_tx, so it needs
all of this information available.
You will need to check the coin, then create a raw_tx object by calling create_tx. Then, you will need to sign
the raw_tx using bit or web3.py (hint: the account objects have a sign transaction function within).
Once you've signed the transaction, you will need to send it to the designated blockchain network.

For ETH, return w3.eth.sendRawTransaction(signed.rawTransaction)

For BTCTEST, return NetworkAPI.broadcast_tx_testnet(signed)

![privkey](screenshots/prev key function.png)



## Send some transactions!
Now, you should be able to fund these wallets using testnet faucets. Open up a new terminal window inside of wallet,
then run python. Within the Python shell, run from wallet import * -- you can now access the functions interactively.
You'll need to set the account with  priv_key_to_account and use send_tx to send transactions.

Bitcoin Testnet transaction


1. Fund a BTCTEST address using this testnet faucet.


2. Use a block explorer to watch transactions on the address.


3. Send a transaction to another testnet address (either one of your own, or the faucet's).




## Local PoA Ethereum transaction


1.Add one of the ETH addresses to the pre-allocated accounts in your networkname.json.


2.Delete the geth folder in each node, then re-initialize using geth --datadir nodeX init networkname.json.
This will create a new chain, and will pre-fund the new account.


3. Add the following middleware
to web3.py to support the PoA algorithm:


from web3.middleware import geth_poa_middleware

w3.middleware_onion.inject(geth_poa_middleware, layer=0)


4.Due to a bug in web3.py, you will need to send a transaction or two with MyCrypto first, since the
w3.eth.generateGasPrice() function does not work with an empty chain. You can use one of the ETH address privkey,
or one of the node keystore files.


5. Last step is to send a transaction from the pre-funded address within the wallet to another.

![ganache](screenshots/transaction.PNG)













