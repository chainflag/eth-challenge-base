import sys

from typing import List

from helper.account import Account
from helper.auth import Paseto
from helper.build import Build
from helper.contract import Contract

menu: str = '''
We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code
Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after the event is triggered.
Option 4, use this option to get source code.
You can finish this challenge in a lot of connections.
'''


class _MenuBase:
    def __init__(self, auth: Paseto, build: Build) -> None:
        self._auth: Paseto = auth
        self._build: Build = build
        self._contract: Contract = Contract(self._build.items()[0][1])
        self._option: List = [None, self.create_game_account, self.deploy_contract, self.request_flag,
                              self.get_contract_source]

    def __str__(self) -> str:
        return menu

    def select_option(self, choice: int) -> None:
        if choice <= 0 or choice > 4:
            print("Invalid option")
            sys.exit(0)
        self._option[choice]()

    def create_game_account(self) -> None:
        account: Account = Account()
        print("[+]Your game account:{}".format(account.address))
        token: str = self._auth.create_token({"private_key": account.private_key})
        print("[+]token: {}".format(token))
        estimate_gas: int = self._contract.deploy.estimate_gas("HelloWorld")
        print("[+]Deploy will cost {} gas".format(estimate_gas))
        print("[+]Make sure that you have enough ether to deploy!!!!!!")

    def deploy_contract(self) -> None:
        token = input("[-]input your token: ")
        message: dict = self._auth.parse_token(token.strip())
        account: Account = Account(message["private_key"])
        if account.balance() == 0:
            print("Insufficient balance of {}".format(account.address))
            sys.exit(0)

        contract_addr: str = account.get_contract_address()
        new_token: str = self._auth.create_token({"private_key": account.private_key, "contract_addr": contract_addr})
        print("[+]new token: {}".format(new_token))
        print("[+]Contract address: {}".format(contract_addr))
        tx_hash: str = account.deploy(self._contract, "HelloWorld")
        print("[+]Transaction hash: {}".format(tx_hash))

    def request_flag(self) -> None:
        new_token = input("[-]input your new token: ")
        message: dict = self._auth.parse_token(new_token.strip())
        print(message["contract_addr"])

    def get_contract_source(self) -> None:
        for key, data in self._build.items():
            print(f"{key}.sol")
            print(data["source"])
