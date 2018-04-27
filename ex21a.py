#!/usr/bin/python
import logging
log = logging.getLogger(name=__name__)

def divide(a,b):
    return a / b

math_problem = divide(9,3)

print(f"{math_problem}")


#try:
#    math_problem = divide(9,3)
#except ex:
#    log.exception()
#    exit(1)
#finally:
#    pass
