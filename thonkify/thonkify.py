from __future__ import annotations

import re

letter_dict = {
    'A': [
        ':think1::iii::iii::think2:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::iii:',
        ':iii::nothing::nothing::iii:',
        ':ink::nothing::nothing::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'B': [
        ':iii::iii::iii::think2:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::iii:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'C': [
        ':think1::iii::iii::thonkways:',
        ':iii::nothing::nothing::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':thonkbow1::iii::iii::thonkways:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'D': [
        ':iii::iii::iii::think2:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'E': [
        ':think1::iii::iii::thonkways:',
        ':iii::nothing::nothing::nothing:',
        ':iii::iii::thonkways::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':thonkbow1::iii::iii::thonkways:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'F': [
        ':think1::iii::iii::thonkways:',
        ':iii::nothing::nothing::nothing:',
        ':iii::iii::thonkways::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':ink::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'G': [
        ':think1::iii::iii::think2:',
        ':iii::nothing::nothing::ink:',
        ':iii::nothing::think1::think2:',
        ':iii::nothing::ink::iii:',
        ':thonkbow1::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'H': [
        ':thi::nothing::nothing::thi:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::iii:',
        ':iii::nothing::nothing::iii:',
        ':ink::nothing::nothing::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'I': [
        ':thinkways::iii::thonkways:',
        ':nothing::iii::nothing:',
        ':nothing::iii::nothing:',
        ':nothing::iii::nothing:',
        ':thinkways::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'J': [
        ':thinkways::iii::iii::thonkways:',
        ':nothing::nothing::iii::nothing:',
        ':nothing::nothing::iii::nothing:',
        ':thi::nothing::iii::nothing:',
        ':thonkbow1::iii::thonkbow4::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'K': [
        ':thi::nothing::nothing::thi:',
        ':iii::think1::iii::thonkbow4:',
        ':iii::iii::nothing::nothing:',
        ':iii::thonkbow1::iii::think2:',
        ':ink::nothing::nothing::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'L': [
        ':thi::nothing::nothing::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':iii::nothing::nothing::nothing:',
        ':thonkbow1::iii::iii::thonkways:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'M': [
        ':think1::iii::think2::think1::iii::think2:',
        ':iii::nothing::iii::iii::nothing::iii:',
        ':iii::nothing::iii::iii::nothing::iii:',
        ':iii::nothing::iii::iii::nothing::iii:',
        ':ink::nothing::think3::think4::nothing::ink:',
        ':nothing::nothing::nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing::nothing::nothing:',
    ],
    'N': [
        ':think1::think2::nothing::thi:',
        ':iii::iii::nothing::iii:',
        ':iii::thonkbow1::think2::iii:',
        ':iii::nothing::iii::iii:',
        ':ink::nothing::think3::think4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'O': [
        ':think1::iii::iii::think2:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':thonkbow1::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'P': [
        ':think1::iii::iii::think2:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::thonkbow4:',
        ':iii::nothing::nothing::nothing:',
        ':ink::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'Q': [
        ':think1::iii::iii::think2::nothing:',
        ':iii::nothing::nothing::iii::nothing:',
        ':iii::nothing::nothing::iii::nothing:',
        ':iii::nothing::thi::iii::nothing:',
        ':thonkbow1::iii::iii::iii::thonkways:',
        ':nothing::nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing::nothing:',
    ],
    'R': [
        ':iii::iii::iii::think2:',
        ':iii::nothing::nothing::iii:',
        ':iii::iii::iii::thonkbow4:',
        ':iii::thonkbow1::iii::think2:',
        ':ink::nothing::nothing::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'S': [
        ':think1::iii::iii::thonkways:',
        ':iii::nothing::nothing::nothing:',
        ':thonkbow1::iii::iii::think2:',
        ':nothing::nothing::nothing::iii:',
        ':thinkways::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'T': [
        ':thinkways::iii::thonkways:',
        ':nothing::iii::nothing:',
        ':nothing::iii::nothing:',
        ':nothing::iii::nothing:',
        ':nothing::ink::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'U': [
        ':thi::nothing::nothing::thi:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':thonkbow1::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'V': [
        ':thi::nothing::nothing::thi:',
        ':iii::nothing::nothing::iii:',
        ':thonkbow1::think2::think1::thonkbow4:',
        ':nothing::iii::iii::nothing:',
        ':nothing::think3::think4::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'W': [
        ':thi::nothing::nothing::nothing::nothing::thi:',
        ':iii::nothing::think1::think2::nothing::iii:',
        ':iii::nothing::iii::iii::nothing::iii:',
        ':iii::nothing::iii::iii::nothing::iii:',
        ':thonkbow1::iii::thonkbow4::thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing::nothing::nothing:',
    ],
    'X': [
        ':thi::nothing::nothing::thi:',
        ':thonkbow1::think2::think1::thonkbow4:',
        ':nothing::iii::iii::nothing:',
        ':think1::thonkbow4::thonkbow1::think2:',
        ':ink::nothing::nothing::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'Y': [
        ':thi::nothing::nothing::thi:',
        ':thonkbow1::think2::think1::thonkbow4:',
        ':nothing::iii::iii::nothing:',
        ':nothing::iii::iii::nothing:',
        ':nothing::think3::think4::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'Z': [
        ':thinkways::iii::iii::iii:',
        ':nothing::nothing::think1::thonkbow4:',
        ':nothing::think1::thonkbow4::nothing:',
        ':think1::thonkbow4::nothing::nothing:',
        ':iii::iii::iii::thonkways:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'a': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::iii:',
        ':iii::thonkwards::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'b': [
        ':thi::nothing::nothing:',
        ':iii::nothing::nothing:',
        ':iii::iii::think2:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'c': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::thonkways:',
        ':iii::nothing::nothing:',
        ':thonkbow1::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'd': [
        ':nothing::nothing::thi:',
        ':nothing::nothing::iii:',
        ':think1::iii::iii:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'e': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::think2:',
        ':iii::iii::thonkbow4:',
        ':thonkbow1::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'f': [
        ':think1::thonkways:',
        ':iii::nothing:',
        ':iii::thonkways:',
        ':iii::nothing:',
        ':ink::nothing:',
        ':nothing::nothing:',
        ':nothing::nothing:',
    ],
    'g': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::think2:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::iii:',
        ':thinkways::iii::thonkbow4:',
    ],
    'h': [
        ':thi::nothing::nothing:',
        ':iii::nothing::nothing:',
        ':iii::iii::think2:',
        ':iii::nothing::iii:',
        ':ink::nothing::ink:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'i': [
        ':nothing:',
        ':spin_thonk:',
        ':thi:',
        ':iii:',
        ':ink:',
        ':nothing:',
        ':nothing:',
    ],
    'j': [
        ':nothing::nothing:',
        ':nothing::spin_thonk:',
        ':nothing::thi:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':thinkways::thonkbow4:',
    ],
    'k': [
        ':thi::nothing::nothing:',
        ':iii::nothing::thi:',
        ':iii::iii::thonkbow4:',
        ':iii::thonkbow1::think2:',
        ':ink::nothing::ink:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'l': [
        ':thi:',
        ':iii:',
        ':iii:',
        ':iii:',
        ':ink:',
        ':nothing:',
        ':nothing:',
    ],
    'm': [
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':think1::think2::think1::think2:',
        ':iii::iii::iii::iii:',
        ':ink::think3::think4::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'n': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':iii::iii::think2:',
        ':iii::nothing::iii:',
        ':ink::nothing::ink:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'o': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::think2:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'p': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::think2:',
        ':iii::nothing::iii:',
        ':iii::iii::thonkbow4:',
        ':iii::nothing::nothing:',
        ':ink::nothing::nothing:',
    ],
    'q': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::think2:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::iii:',
        ':nothing::nothing::ink:',
    ],
    'r': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thi::think1::thonkways:',
        ':iii::thonkbow4::nothing:',
        ':ink::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    's': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':think1::iii::thonkways:',
        ':thonkbow1::iii::think2:',
        ':thinkways::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    't': [
        ':nothing::nothing::nothing:',
        ':nothing::thi::nothing:',
        ':thinkways::iii::thonkways:',
        ':nothing::iii::nothing:',
        ':nothing::thonkbow1::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'u': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thi::nothing::thi:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'v': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thi::nothing::thi:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'w': [
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':thi::think1::think2::thi:',
        ':iii::iii::iii::iii:',
        ':think3::think4::think3::think4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    'x': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thinkways::think2::thi:',
        ':think1::iii::thonkbow4:',
        ':ink::thonkbow1::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'y': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thi::nothing::thi:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::iii:',
        ':thinkways::iii::thonkbow4:',
    ],
    'z': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thinkways::iii::iii:',
        ':think1::iii::thonkbow4:',
        ':iii::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '\xdc': [
        ':spin_thonk::nothing::nothing::spin_thonk:',
        ':thi::nothing::nothing::thi:',
        ':iii::nothing::nothing::iii:',
        ':iii::nothing::nothing::iii:',
        ':thonkbow1::iii::iii::thonkbow4:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    '\xfc': [
        ':nothing::nothing::nothing:',
        ':spin_thonk::nothing::spin_thonk:',
        ':thi::nothing::thi:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '0': [
        ':think1::iii::think2:',
        ':iii::nothing::iii:',
        ':iii::nothing::iii:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '1': [
        ':think1::iii::nothing:',
        ':ink::iii::nothing:',
        ':nothing::iii::nothing:',
        ':nothing::iii::nothing:',
        ':thinkways::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '2': [
        ':think1::iii::think2:',
        ':ink::nothing::iii:',
        ':nothing::think1::thonkbow4:',
        ':think1::thonkbow4::nothing:',
        ':iii::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '3': [
        ':think1::iii::think2:',
        ':ink::nothing::iii:',
        ':nothing::thinkways::iii:',
        ':thi::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '4': [
        ':thi::nothing::thi:',
        ':iii::nothing::iii:',
        ':thonkbow1::iii::iii:',
        ':nothing::nothing::iii:',
        ':nothing::nothing::ink:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '5': [
        ':iii::iii::thonkways:',
        ':iii::nothing::nothing:',
        ':thonkbow1::iii::think2:',
        ':thi::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '6': [
        ':think1::iii::think2:',
        ':iii::nothing::ink:',
        ':iii::iii::think2:',
        ':iii::thonkwards::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '7': [
        ':thinkways::iii::think2:',
        ':nothing::nothing::iii:',
        ':nothing::think1::thonkbow4:',
        ':think1::thonkbow4::nothing:',
        ':ink::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '8': [
        ':think1::iii::think2:',
        ':iii::thonkwards::iii:',
        ':iii::iii::iii:',
        ':iii::thonkwards::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '9': [
        ':think1::iii::think2:',
        ':iii::thonkwards::iii:',
        ':thonkbow1::iii::iii:',
        ':thi::nothing::iii:',
        ':thonkbow1::iii::thonkbow4:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '@': [
        ':think1::iii::iii::iii::iii::iii::think2:',
        ':iii::nothing::nothing::nothing::nothing::nothing::iii:',
        ':iii::nothing::think1::iii::think2::nothing::iii:',
        ':iii::nothing::iii::nothing::iii::nothing::iii:',
        ':iii::nothing::thonkbow1::iii::iii::iii::thonkbow4:',
        ':iii::nothing::nothing::nothing::nothing::nothing::nothing:',
        ':thonkbow1::iii::iii::iii::iii::iii::thonkways:',
    ],
    '#': [
        ':nothing::nothing::nothing::nothing::nothing:',
        ':nothing::thi::nothing::thi::nothing:',
        ':thinkways::iii::iii::iii::thonkways:',
        ':nothing::iii::thonkwards::iii::nothing:',
        ':thinkways::iii::iii::iii::thonkways:',
        ':nothing::ink::nothing::ink::nothing:',
        ':nothing::nothing::nothing::nothing::nothing:',
    ],
    '-': [
        ':nothing::nothing:',
        ':nothing::nothing:',
        ':thinkways::thonkways:',
        ':nothing::nothing:',
        ':nothing::nothing:',
        ':nothing::nothing:',
        ':nothing::nothing:',
    ],
    '+': [
        ':nothing::nothing::nothing:',
        ':nothing::thi::nothing:',
        ':thinkways::iii::thonkways:',
        ':nothing::ink::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '*': [
        ':nothing:',
        ':nothing:',
        ':eight_spoked_asterisk:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
    ],
    '=': [
        ':nothing::nothing:',
        ':thinkways::thonkways:',
        ':nothing::nothing:',
        ':thinkways::thonkways:',
        ':nothing::nothing:',
        ':nothing::nothing:',
        ':nothing::nothing:',
    ],
    '_': [
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':thinkways::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '[': [
        ':iii::thonkways:',
        ':iii::nothing:',
        ':iii::nothing:',
        ':iii::nothing:',
        ':iii::nothing:',
        ':iii::thonkways:',
        ':nothing::nothing:',
    ],
    ']': [
        ':thinkways::iii:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':thinkways::iii:',
        ':nothing::nothing:',
    ],
    '{': [
        ':nothing::iii::thonkways:',
        ':nothing::iii::nothing:',
        ':think1::thonkbow4::nothing:',
        ':thonkbow1::think2::nothing:',
        ':nothing::iii::nothing:',
        ':nothing::iii::thonkways:',
        ':nothing::nothing::nothing:',
    ],
    '}': [
        ':thinkways::iii::nothing:',
        ':nothing::iii::nothing:',
        ':nothing::thonkbow1::think2:',
        ':nothing::think1::thonkbow4:',
        ':nothing::iii::nothing:',
        ':thinkways::iii::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '(': [
        ':think1::thonkways:',
        ':iii::nothing:',
        ':iii::nothing:',
        ':iii::nothing:',
        ':iii::nothing:',
        ':thonkbow1::thonkways:',
        ':nothing::nothing:',
    ],
    ')': [
        ':thinkways::think2:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':nothing::iii:',
        ':thinkways::thonkbow4:',
        ':nothing::nothing:',
    ],
    '/': [
        ':nothing::nothing::nothing::thi:',
        ':nothing::nothing::think1::thonkbow4:',
        ':nothing::think1::thonkbow4::nothing:',
        ':think1::thonkbow4::nothing::nothing:',
        ':ink::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    '\\': [
        ':thi::nothing::nothing::nothing:',
        ':thonkbow1::think2::nothing::nothing:',
        ':nothing::thonkbow1::think2::nothing:',
        ':nothing::nothing::thonkbow1::think2:',
        ':nothing::nothing::nothing::ink:',
        ':nothing::nothing::nothing::nothing:',
        ':nothing::nothing::nothing::nothing:',
    ],
    ' ': [
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
    ],
    '\'': [
        ':nothing:',
        ':thi:',
        ':ink:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
    ],
    '"': [
        ':nothing:  :nothing:',
        ':thi:  :thi:',
        ':ink:  :ink:',
        ':nothing:  :nothing:',
        ':nothing:  :nothing:',
        ':nothing:  :nothing:',
        ':nothing:  :nothing:',
    ],
    ',': [
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':thi:',
        ':ink:',
        ':nothing:',
    ],
    '.': [
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':nothing:',
        ':spin_thonk:',
        ':nothing:',
        ':nothing:',
    ],
    ':': [
        ':nothing:',
        ':nothing:',
        ':spin_thonk:',
        ':nothing:',
        ':spin_thonk:',
        ':nothing:',
        ':nothing:',
    ],
    ';': [
        ':nothing:',
        ':nothing:',
        ':spin_thonk:',
        ':nothing:',
        ':thi:',
        ':ink:',
        ':nothing:',
    ],
    '!': [
        ':thi:',
        ':iii:',
        ':iii:',
        ':ink:',
        ':spin_thonk:',
        ':nothing:',
        ':nothing:',
    ],
    '?': [
        ':think1::iii::think2:',
        ':ink::nothing::iii:',
        ':nothing::think1::thonkbow4:',
        ':nothing::ink::nothing:',
        ':nothing::spin_thonk::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    '¯': [
        ':thinkways::iii::thonkways:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
        ':nothing::nothing::nothing:',
    ],
    'ツ': [
        ':nothing::nothing:',
        ':nothing::nothing:',
        ':think1::think2:',
        ':think3::think4:',
        ':nothing::nothing:',
        ':nothing::nothing:',
        ':nothing::nothing:',
    ],
}


def minify_line(text: str) -> str:
    if text.endswith(':nothing:'):
        m = re.match(r'^(.+[^g]\:)(\:nothing\:| )+$', text)
        return m.group(1)
    return text


def thonkify(text: str) -> str:
    word_list = []
    for letter in text:
        try:
            thonk_letter = letter_dict[letter]
            word_list.append(thonk_letter)
        except KeyError:
            print(f'Missing mapping for character {letter}')
            pass
    prelim_final_word = ([], [], [], [], [], [], [])
    for letter in word_list:
        for index, letter_line in enumerate(letter):
            prelim_final_word[index].append(letter_line)
    final_word = []
    for line in prelim_final_word:
        if len(''.join(line).replace(':nothing:', '')) > 0:
            final_word.append(' '.join(line))
    final_word_minified = []
    for line in final_word:
        final_word_minified.append(minify_line(line))
    return '\n'.join(final_word_minified)
