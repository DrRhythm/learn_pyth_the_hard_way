for i in range(1,101):
  if (i % 4 == 0) and (i % 6 == 0):
    print "{}: Linked In".format(i)
  elif (i % 4 == 0):
    print "{}: Linked".format(i)
  elif (i % 6 == 0):
    print "{}: In".format(i)
