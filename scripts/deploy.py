#!/usr/bin/python3

from brownie import WallToken, accounts


def main():
    return WallToken.deploy({'from': accounts[0]})