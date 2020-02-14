import pytest


def test_getRandomIBAN():
    """ test RandomIBAN genrate and validate 
    """
    # keep both IBAN class separate
    from baangt.base.IBAN import IBAN as b_IBAN
    from schwifty import IBAN as o_IBAN
    
    # generate random IBAN
    ran_iban = o_IBAN(b_IBAN().getRandomIBAN())

    assert ran_iban.country_code == "AT"
    assert ran_iban.bank_code == "20151"
    
    
    
    
