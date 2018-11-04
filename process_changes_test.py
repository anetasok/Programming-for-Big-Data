# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 23:20:34 2018

@author: aneta sokolowska
@student number: 10379935

"""

import unittest
from process_changes import Commit

class TestCommit(unittest.TestCase):

    def setUp(self):
        self.check = Commit()

    def test(self):
        file=self.check.read_file('changes_python.log')
        result=len(file) #testing the lenght of the file
        self.assertEqual(5255,result)
        commits = self.check.get_commits(file)
        self.assertEqual(422, len(commits)) # testing the length of file after cleaning 
        date=self.check.get_dates(commits['date'])
        commits['date']=date
        result=len(commits['date'][20])
        self.assertEqual(10,result)
        
        
if __name__ == '__main__':
    unittest.main()
