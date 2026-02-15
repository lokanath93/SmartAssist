"""Tests for smartassist.voice."""
import pytest

from smartassist.voice import parse_type_command


def test_parse_type_command_returns_phrase():
    assert parse_type_command("type hello world") == "hello world"
    assert parse_type_command("type foo") == "foo"


def test_parse_type_command_no_type_returns_none():
    assert parse_type_command("click") is None
    assert parse_type_command("hello") is None


def test_parse_type_command_type_only_returns_none():
    """No text after 'type' returns None (nothing to type)."""
    assert parse_type_command("type") is None
    assert parse_type_command("type   ") is None


def test_parse_type_command_extra_before():
    assert parse_type_command("please type hello") == "hello"


def test_parse_type_command_first_type_wins():
    assert parse_type_command("type type x") == "type x"
