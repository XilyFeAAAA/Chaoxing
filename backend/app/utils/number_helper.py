#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import random


def generate_random_num(num_digits: int) -> str:
    """utils to generate random string of numbers"""
    random_num = ''.join(random.choice('0123456789') for _ in range(num_digits))
    return random_num
