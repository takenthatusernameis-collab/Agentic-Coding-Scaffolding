"""Tests for argparse_utils."""

import argparse

import argparse_utils as au


def test_make_parser():
    p = au.make_parser(prog="x", description="d")
    assert p.prog == "x"
    assert p.description == "d"


def test_add_flag():
    p = au.make_parser()
    au.add_flag(p, "--verbose", "v")
    ns = p.parse_args(["--verbose"])
    assert ns.verbose is True


def test_add_option():
    p = au.make_parser()
    au.add_option(p, "--count", type_=int, default=1)
    ns = p.parse_args(["--count", "5"])
    assert ns.count == 5


def test_add_positional():
    p = au.make_parser()
    au.add_positional(p, "name")
    ns = p.parse_args(["alice"])
    assert ns.name == "alice"


def test_int_positive():
    assert au.int_positive("3") == 3
    try:
        au.int_positive("0")
    except argparse.ArgumentTypeError:
        pass
    else:
        raise AssertionError("expected error")


def test_float_range():
    conv = au.float_range(0.0, 1.0)
    assert conv("0.5") == 0.5
    try:
        conv("2.0")
    except argparse.ArgumentTypeError:
        pass
    else:
        raise AssertionError("expected error")


def test_subparsers():
    p = au.make_parser()
    sp = au.add_subparsers(p)
    sub = sp.add_parser("run")
    au.add_flag(sub, "--fast")
    ns = p.parse_args(["run", "--fast"])
    assert ns.command == "run"
    assert ns.fast is True
