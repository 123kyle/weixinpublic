#！／usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

def random_string(length=16):
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return ''.join(rand_list)
