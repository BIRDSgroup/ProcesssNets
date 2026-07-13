#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:32:06 2024

@author: sugyani
"""

import os

def setThreads(threads = 10):
    '''
    This function sets environment variables to limit number of threads to 10. 
    Even though we set these values to 10, our code as well as the library functions that we use from scipy, pandas, and numpy do not use multiple parallel
    cores by default. This ensures that our benchmark comparisions are sequential as required. 
    '''
    os.environ["OMP_NUM_THREADS"] = str(threads)
    os.environ["MKL_NUM_THREADS"] = str(threads)
    os.environ["NUMEXPR_NUM_THREADS"] = str(threads)
    os.environ["OPENBLAS_NUM_THREADS"] = str(threads)
    os.environ["VECLIB_MAXIMUM_THREADS"] = str(threads)
