#!/usr/bin/python3

import pytest

def test_mint_not_owner(token, accounts):
    tx = token.mint(100, {
        "from": accounts[1],
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_mint_owner(token, accounts):
    amount = 100
    balance_before = token.balanceOf(accounts[0])
    token.mint(amount, {"from": accounts[0]})
    balance_after = token.balanceOf(accounts[0])

    assert(balance_after - balance_before == amount)


def test_mint_not_exist_account(token, accounts):
    tx = token.mint(accounts[1], 100, {
        "from": accounts[0],
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_mint_another_account(registered_token, accounts):
    amount = 100
    balance_before = registered_token.balanceOf(accounts[1])
    registered_token.mint(accounts[1], amount, {"from": accounts[0]})
    balance_after = registered_token.balanceOf(accounts[1])

    assert(balance_after - balance_before == amount)

