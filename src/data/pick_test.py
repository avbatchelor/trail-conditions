# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 14:27:11 2018

@author: Alex
"""

from pick import pick

title = 'Please choose your favorite programming language: '
options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
option, index = pick(options, title)
print(option)
print(index)