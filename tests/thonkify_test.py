from __future__ import annotations

from thonkify import thonkify


def test_lowercase_i():
    final = thonkify.thonkify('i')
    assert final == ':spin_thonk:\n:thi:\n:iii:\n:ink:'


def test_lowercase_p():
    final = thonkify.thonkify('p')
    expected = '''\
:think1::iii::think2:
:iii::nothing::iii:
:iii::iii::thonkbow4:
:iii:
:ink:'''
    assert final == expected


def test_minify_line_removes_items():
    output = thonkify.minify_line(':thi::nothing:')
    assert output == ':thi:'


def test_minify_line_removes_ending_nothings():
    output = thonkify.minify_line(':iii::nothing::nothing:')
    assert output == ':iii:'


def test_minify_line_removes_items_including_space():
    output = thonkify.minify_line(':thi::nothing: :nothing:')
    assert output == ':thi:'


def test_minify_line_keeps_string():
    output = thonkify.minify_line(':thi::ink:')
    assert output == ':thi::ink:'
