#!/usr/bin/python3

import pytest

def test_wall_unregister(with_format_token, accounts):
    tx = with_format_token.make_wall_post(
        "html", 
        "something", 
        {
            "from": accounts[1],
            "required_confs": 0,
        },
    )

    assert(tx.status == -1)


def test_wall_unsupported_format(with_format_token, accounts):
    tx = with_format_token.make_wall_post(
        "css", 
        "something", 
        {
            "from": accounts[0],
            "required_confs": 0,
        },
    )

    assert(tx.status == -1)


def test_wall_without_balance(with_format_token, accounts):
    with_format_token.make_wall_post("html", "something", {"from": accounts[0]})
    tx = with_format_token.make_wall_post(
        "html", 
        "something", 
        {
            "from": accounts[0],
            "required_confs": 0,
        },
    )

    assert(tx.status == -1)


def test_wall_event(with_format_token, accounts):
    forma = "html"
    post = "something"
    tx = with_format_token.make_wall_post(forma, post, {"from": accounts[0]})
    event = tx.events["PostCreated"][0]

    assert(event["format"] == forma and event["post"] == post)