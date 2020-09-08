import pytest
import baangt.base.GlobalConstants as GC
from baangt.base.AddressCreate import AddressCreate


@pytest.mark.parametrize("CountryCode, PostalCode", [("AT", "1020"), ("CY", "6020")])
def test_getRandomAddress(CountryCode, PostalCode):
    addressCreate = AddressCreate(addressFilterCriteria={GC.ADDRESS_COUNTRYCODE:CountryCode})
    address = addressCreate.returnAddress()
    assert address[GC.ADDRESS_COUNTRYCODE] == CountryCode
    assert address[GC.ADDRESS_POSTLCODE] == PostalCode
