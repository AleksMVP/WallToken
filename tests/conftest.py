#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # выполнять откат цепи после завершения каждого теста, чтобы обеспечить надлежащую изоляцию
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(WallToken, accounts):
    return WallToken.deploy({'from': accounts[0]})


@pytest.fixture(scope="module")
def registered_token(token, accounts):
    token.register(accounts[0], {
        "from": accounts[1], 
        "amount": token.current_price() * token.min_entry_stake(),
    })

    return token


@pytest.fixture(scope="module")
def with_format_token(token, accounts):
    token.addFormat("html", {"from": accounts[0]})

    return token

