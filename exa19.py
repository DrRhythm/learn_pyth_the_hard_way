def top_jungle(top_count, jungle_count):
    print(f"There are currently {top_count} viable top laners.")
    print(f"Currently, there are {jungle_count} viable junglers.")
    print("That is more than enough to have a stable champion pool.")
    print("Get your tent out and we'll camp toplane.\n")

print("This is the basic count:")
top_jungle(6,10)

print("We could also break them out in long form:")
number_of_tops = 3
number_of_jungs = 7

top_jungle(number_of_tops, number_of_jungs)

print("Here it is with mathz:")
top_jungle(23 - 12, 3 + 4)
