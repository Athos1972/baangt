import pytest


def test_getRandomAddress():
    import baangt.base.GlobalConstants as GC
    from baangt.base.AddressCreate import AddressCreate

    addressCreate = AddressCreate(addressFilterCriteria={GC.ADDRESS_COUNTRYCODE:"AT"})

    assert addressCreate.returnAddress()[GC.ADDRESS_COUNTRYCODE] == "AT"
    assert addressCreate.returnAddress()[GC.ADDRESS_POSTLCODE] == "1020"

    addressCreate = AddressCreate(addressFilterCriteria={GC.ADDRESS_COUNTRYCODE:"CY"})

    assert addressCreate.returnAddress()[GC.ADDRESS_COUNTRYCODE] == "CY"
    assert addressCreate.returnAddress()[GC.ADDRESS_POSTLCODE] == "6020"

if __name__ == '__main__':
    test_getRandomAddress()