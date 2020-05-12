from baangt.base.Faker import Faker

lFaker = Faker()


def test_fakerProxy_csv():
    # Will create 20 fake csv lines and will verify.
    csv_lines = lFaker.fakerProxy("csv", num_rows=19)
    csv_list = csv_lines.split('\r\n')
    assert len(csv_list) == 20
    print("Fake Csv Test succeeded.")


def test_fakerProxy_email():
    # Will get a fake email with domain test_baangt.com
    fake_email = lFaker.fakerProxy("email", domain="test_baangt.com")
    assert "@test_baangt.com" in fake_email
    print("Fake mail test succeed")