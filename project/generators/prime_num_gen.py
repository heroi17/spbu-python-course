import math

def prime_number_generator():
    count = 2
    #maybe not the fastest solution, we can use memory to make it faster.
    while True:
        isprime = True
        
        for x in range(2, int(math.sqrt(count) + 1)):
            if count % x == 0: 
                isprime = False
                break
        
        if isprime:
            yield count
        
        count += 1