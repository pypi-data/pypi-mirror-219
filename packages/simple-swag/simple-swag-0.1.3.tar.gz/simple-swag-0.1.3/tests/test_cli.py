import os

import swag

# https://stackoverflow.com/questions/13493288/python-cli-program-unit-testing

def test_entrypoint():
    exit_status = os.system('swag --help')
    assert exit_status == 0
