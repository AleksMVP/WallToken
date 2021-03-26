#!/usr/bin/python3

import pytest

def test_register_reward(token, accounts):
    balance_before = token.balanceOf(accounts[0])
    token.register(accounts[0], {
        "from": accounts[1], 
        "amount": token.current_price() * token.min_entry_stake(),
    })
    balance_after = token.balanceOf(accounts[0])

    assert(balance_after - balance_before == token.invite_reward())


def test_register_new_user_balance(token, accounts):
    token.register(accounts[0], {
        "from": accounts[1], 
        "amount": token.current_price() * token.min_entry_stake(),
    })

    assert(token.balanceOf(accounts[1]) == token.min_entry_stake())


def test_register_price_rised_up(token, accounts):
    price_before = token.current_price()
    token.register(accounts[0], {
        "from": accounts[1], 
        "amount": token.current_price() * token.min_entry_stake(),
    })
    price_after = token.current_price()

    assert(price_after - price_before == token.price_increase_amount())


def test_register_inviter_not_exist(token, accounts):
    tx = token.register(accounts[2], {
        "from": accounts[1], 
        "amount": token.current_price() * token.min_entry_stake(),
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_register_sender_already_exist(token, accounts):
    tx = token.register(accounts[0], {
        "from": accounts[0], 
        "amount": token.current_price() * token.min_entry_stake(),
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_register_not_enough_eth(token, accounts):
    amount = 0
    assert(amount < token.min_entry_stake())

    tx = token.register(accounts[0], {
        "from": accounts[1], 
        "amount": amount,
        "required_confs": 0,
    })

    assert(tx.status == -1)


def test_register_emit_event(token, accounts):
    tx = token.register(accounts[0], {
        "from": accounts[1], 
        "amount": token.current_price() * token.min_entry_stake(),
    })

    event = tx.events["UserRegistered"][0]

    assert(event["user"] == accounts[1].address)