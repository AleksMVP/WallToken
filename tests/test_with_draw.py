#!/usr/bin/python3

import pytest

def test_withdraw_not_owner(registered_token, accounts):
    amount = 1
    assert(amount <= registered_token.balance())

    tx = registered_token.withdraw(amount, {
        "from": accounts[1],
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_withdraw_more(registered_token, accounts):
    amount = 99999
    assert(amount > registered_token.balance())
    tx = registered_token.withdraw(99999999, {
        "from": accounts[0],
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_withdraw(registered_token, accounts):
    amount = 1
    assert(amount <= registered_token.balance())

    balance_before = accounts[0].balance()
    registered_token.withdraw(amount, {
        "from": accounts[0],
    })
    balance_after = accounts[0].balance()

    assert(balance_after - balance_before == amount)


def test_withdraw_to(registered_token, accounts):
    amount = 1
    assert(amount <= registered_token.balance())

    balance_before = accounts[1].balance()
    registered_token.withdraw(
        accounts[1],
        amount, 
        {
            "from": accounts[0],
        },
    )
    balance_after = accounts[1].balance()

    assert(balance_after - balance_before == amount)