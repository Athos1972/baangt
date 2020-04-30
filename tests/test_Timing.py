import pytest
from baangt.base.Timing.Timing import Timing

def test_timing_name():
    timer = Timing()
    names = ['test', 'hello', 'world']
    for name in names:
        assert timer.takeTime(name) == name

def test_timing_force_new():
    timer = Timing()
    names = ['test', 'hello', 'world']
    for k in range(101):
        for name in names:
            assert timer.takeTime(name, forceNew = True) == f'{name}_{k}'

def test_timing_add_attribute():
    timer = Timing()
    timer.takeTime('test')
    # Additional Attributes now possible:
    timer.addAttribute('franzi', 'fritzi', 'test')
    timer.takeTime('test')

    lResult = timer.returnTime()
    print(lResult)
    assert "franzi" in lResult


def test_timing_take_time_sum_output():
    timer = Timing()
    names = ['test', 'hello', 'world']
    for name in names:
        timer.takeTime(name)

    assert timer.takeTimeSumOutput() is None

def test_timing_return_time():
    timer = Timing()
    names = ['test', 'hello', 'world']
    for name in names:
        timer.takeTime(name)

    assert type(timer.returnTime()) is str 

def test_timing_reset_time():
    timer = Timing()
    names = ['test', 'hello', 'world']
    for name in names:
        timer.takeTime(name)

    timer.resetTime('test')
    assert timer.returnTime() == ''

def test_timing___format_time():
    # naming due to private method name hiding
    assert Timing._Timing__format_time(1) == '00:00:01'
    assert Timing._Timing__format_time(59) == '00:00:59'
    assert Timing._Timing__format_time(60) == '00:01:00'
    assert Timing._Timing__format_time(60 * 59) == '00:59:00'
    assert Timing._Timing__format_time(60 * 60) == '01:00:00'
    assert Timing._Timing__format_time(60 * 60 * 23) == '23:00:00'
    assert Timing._Timing__format_time(60 * 60 * 24) == '00:00:00'
