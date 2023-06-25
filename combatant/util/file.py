import sys, os

import regex
import logging
import asyncio

class NoFileError(Exception):
    def __init__(self, f):
        self.message = f"File '{f}' does not exist."
        super(Exception, self).__init__(self.message)

class File:
    @staticmethod
    async def open(f):
        file = open(f, 'r', encoding='utf-8')
        filec = file.read()
        file.close()

        return (f, filec)

    async def write(f, c):
        try:
            file = open(f, 'w', encoding='utf-8')
            file.write(c)
            file.close()

        except:
            raise

        return (f, 0)
