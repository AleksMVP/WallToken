#!/usr/bin/python3

import pytest

def test_format_already_exist(with_format_token, accounts):
    tx = with_format_token.addFormat(
        "html", 
        {
            "from": accounts[0],
            "required_confs": 0,
        }
    )

    assert(tx.status == -1)


def test_format_not_owner(registered_token, accounts):
    tx = registered_token.addFormat(
        "html", 
        {
            "from": accounts[1],
            "required_confs": 0,
        }
    )

    assert(tx.status == -1)


def test_format(token, accounts):
    forma = "html"
    token.addFormat(forma, {"from": accounts[0]})

    assert(token.supported_formats(forma, {"from": accounts[0]}))


def test_format_event(token, accounts):
    forma = "html"
    tx = token.addFormat(forma, {"from": accounts[0]})

    event = tx.events["FormatAdded"][0]

    assert(event["format"] == forma)




    