import pytest


def test_getRandomIBAN():
    """ test RandomIBAN genrate and validate 
    """
    from baangt.base.IBAN import IBAN as b_IBAN
    
    # generate random IBAN
    ran_iban = b_IBAN().getRandomIBAN()

    assert ran_iban
    assert len(ran_iban) > 10
