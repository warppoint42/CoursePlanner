#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 20:28:56 2018

@author: nantanick
"""

#import main
import csv 


class course:
    """  
    Format
         
    course_code: BIOC109B
    course_title: The Human Genome and Disease: Genetic Diversity and Personalized Medicine (BIO 109B)
    degree: UG
    school: MED
    requirements: ||:WAY-SMA||GER: DB-NatSci
    gradings: Letter or Credit/No Credit
    units: 3
    status: Active
    intensity:0.25,0.75,-1,-1,-1,-1,-1,-1,0.07,0.53,0.2,0.05,0.07,0.05,0.02,0.01,0.0,0.0,0.0,0.0
    """
    def __init__(self, line):
        self.course_code = line[0]
        self.course_title = line[1]
        self.degree = line[2]
        self.school = line[3]
        self.requirement = line[4]
        self.grading = line[5]
        self.units = line[6]
        self.status = line[7]
        self.intensity = line[8]
        
class course_list:
    def __init__(self):
        self.course_list = []
               
    def read_file(self,file):
        f = open(file, 'r')
        reader = csv.reader(f)
        for line in reader:
            c = course(line)
            self.course_list.append(c)
    
