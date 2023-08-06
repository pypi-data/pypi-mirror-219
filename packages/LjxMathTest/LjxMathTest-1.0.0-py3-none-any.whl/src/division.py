#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/7/17  16:18
# @Author : 卢健轩
def divide(x, y):
    if y != 0:
        return x / y
    else:
        raise ValueError("Cannot divide by zero.")
