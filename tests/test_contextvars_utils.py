"""Tests for contextvars_utils."""

import unittest

from contextvars_utils import Context, ContextVar, Token, copy_context


class TestContextvarsUtils(unittest.TestCase):
    def test_contextvar_get_set(self):
        var = ContextVar("x", default=0)
        self.assertEqual(var.get(), 0)
        token = var.set(42)
        self.assertEqual(var.get(), 42)
        var.reset(token)
        self.assertEqual(var.get(), 0)

    def test_contextvar_missing_default_raises(self):
        var = ContextVar("y")
        with self.assertRaises(LookupError):
            var.get()

    def test_token_type(self):
        var = ContextVar("z", default=1)
        token = var.set(2)
        self.assertIsInstance(token, Token)

    def test_copy_context(self):
        var = ContextVar("w", default=0)
        var.set(7)
        ctx = copy_context()
        self.assertIsInstance(ctx, Context)
        self.assertEqual(ctx[var], 7)

    def test_context_run(self):
        var = ContextVar("v", default=0)
        var.set(1)

        def fn():
            return var.get()

        ctx = copy_context()
        self.assertEqual(ctx.run(fn), 1)

    def test_contextvars_independent(self):
        var = ContextVar("u", default=0)
        var.set(5)
        ctx = copy_context()
        ctx.run(lambda: var.set(99))
        self.assertEqual(var.get(), 5)
