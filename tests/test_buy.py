#!/usr/bin/python3

import pytest

def test_buy_unregister(token, accounts):
    tx = token.buy({
        "from": accounts[1], 
        "amount": 100,
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_buy_without_remainder(token, accounts):
    amount = 100
    assert(amount % token.current_price() == 0)

    eth_balance = accounts[0].balance()

    balance_before = token.balanceOf(accounts[0])
    token.buy({"from": accounts[0], "amount": amount})
    balance_after = token.balanceOf(accounts[0])

    assert(eth_balance - accounts[0].balance() == amount)
    assert(balance_after - balance_before == amount // token.current_price())


def test_buy_with_remainder(token, accounts):
    amount = 101
    assert(amount % token.current_price() != 0)

    eth_balance = accounts[0].balance()

    balance_before = token.balanceOf(accounts[0])
    token.buy({"from": accounts[0], "amount": amount})
    balance_after = token.balanceOf(accounts[0])

    assert(eth_balance - accounts[0].balance() == amount - amount % token.current_price())
    assert(balance_after - balance_before == amount // token.current_price())
