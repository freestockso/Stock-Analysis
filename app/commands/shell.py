#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.stk.util.Shell import Shell
def run(conf = {}):
    shell = Shell(conf)
    shell.handle()
