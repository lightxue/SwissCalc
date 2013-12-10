#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  lightxue
# Email:   bkmgtp@gmail.com
# Version: 1.1.0
# Website: https://github.com/lightxue/SwissCalc

import vim
import json

class History(object):
    '''
    Reord history command and sessions
    '''
    def __init__(self):
        self.cmds = []
        self.cmd_idx = 0
        self.cmd_tmp = ''
        self.cmd_max = vim.vars['scalc_max_history']
        self.prompt = vim.vars['scalc_prompt']

    def jump_to_prompt(self, insert_mode):
        last = vim.current.buffer[-1]
        if not last.startswith(self.prompt):
            vim.current.buffer.append(self.prompt)
        vim.current.window.cursor = len(vim.current.buffer), len(last)
        if insert_mode:
            vim.command('startinsert!')

    def record_cmd(self, expr):
        if not expr.strip():
            return
        self.cmds.append(expr)
        if len(self.cmds) > self.cmd_max:
            self.cmds = self.cmds[-self.cmd_max:]
        self.cmd_idx = len(self.cmds)
        self.cmd_tmp = ''

    def pre_cmd(self):
        if not self.cmds or self.cmd_idx <= 0:
            self.jump_to_prompt(True)
            return

        if self.cmd_idx == len(self.cmds):
            line = vim.current.line
            if not line.startswith(self.prompt):
                self.cmd_tmp = ''
            else:
                self.cmd_tmp = line[len(self.prompt):]

        self.cmd_idx -= 1
        vim.current.line = self.prompt + self.cmds[self.cmd_idx]
        self.jump_to_prompt(True)

    def next_cmd(self):
        if self.cmd_idx > len(self.cmds) - 1:
            pass
        elif self.cmd_idx == len(self.cmds) - 1:
            self.cmd_idx += 1
            vim.current.line = self.prompt + self.cmd_tmp
        else:
            self.cmd_idx += 1
            vim.current.line = self.prompt + self.cmds[self.cmd_idx]
        self.jump_to_prompt(True)
