"""
包含常用常量与各种工具类
"""
import math
import random as rd
from . import data
import bisect

PI = math.pi
E = math.e

ALPHABET_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"

def num(a, b):
    '''
    生成 [a,b] 范围内的随机整数。
    PS：函数内部自动转整数，自动处理大小关系。
    '''
    a = int(a)
    b = int(b)
    if a < b:
        return rd.randint(a, b)
    else:
        return rd.randint(b, a)
    
def prime(a, b):
    '''
    获取 [a,b] 范围内的所有质数。
    PS：函数内部自动转整数，自动处理大小关系。
    '''
    a = int(a)
    b = int(b)
    if a > b:
        (a,b) = (b,a)
    ia = bisect.bisect_left(data.PRIMARY, a)
    ib = bisect.bisect_right(data.PRIMARY, b)
    if ib == ia:
        if data.PRIMARY[ia] == a:
            return [a]
        return []
    return data.PRIMARY[ia: ib]
