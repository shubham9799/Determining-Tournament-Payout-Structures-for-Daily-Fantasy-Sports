import numpy as np
from numpy import dot
from math import ceil, floor
import csv

#binary search given a function and two extreme values
#finding a value for which the particular function is zero
#if a function is continuous we will always have a value for which f(c) == 0  if f(a)<0 and f(b)>0 por vice versa. 
def binary(fun, a, b):
    # Ensure that we have the right interval
    while fun(a)*fun(b) > 0:
        b += 1
    
    c = (a+b)/2.0
    while abs(fun(c)) > 0.001:              #Accepted difference in the total sum(less than 1 paisa(if INR))
        if fun(a)*fun(c) < 0:
            b = c
        else:
            a = c
        c = (a+b)/2.0
    return c

def get_unperfect_prize(N, B, P1, E):
    if B <= N*E:
        raise NameError("Prize pool is very less. Please change")
    def sum_to_optimize(alpha):
        count = 0
        for i in range(1,N+1):
            count += 1/(i**alpha)
        return B - N*E - (P1-E)*count             #As close to 0
    
    b = 1 - np.log((B-(N*E))/(P1 - E))/np.log(N)  #Starting value since for this func might be less than 0, we will modify it if not check binary function
    
    alpha = binary(sum_to_optimize, 0, b)
    return [E + (P1 - E)/(x**alpha) for x in range(1, N+1)]

def init_buck_size(num_wins, num_bucks, singleton_bucks):
    """ (int, int) -> list of int

    Return an ordered list of bucket size of length num_bucks such that the sum equals num_wins.
    """
    if singleton_bucks < 1:
        raise NameError("Prize pool is very less. Please change")
    if num_wins < singleton_bucks:
        # Must be at least number of singleton bucket
        return [] 
    if num_wins < num_bucks:
        # Must be more or an equal number of winners than the number of buckets.
        return []
    if num_wins > singleton_bucks and num_bucks <= singleton_bucks:
        # singleton buckets should not be less than number of buckets
        return []
    
    #Getting Beta from heurestics
    def b_to_optimize(beta):
        # This is for the first singleton buckets size = 1
        count = 0
        for i in range(1, num_bucks-singleton_bucks+1):
            count += beta**i
        return count - num_wins + singleton_bucks
    
    beta = binary(b_to_optimize, 1, 10)       #binary search to find the closest beta
    bucket_sizes = [1 for i in range(0, singleton_bucks)] # First assign singleton buckets of size 1
    
    #Base case if number of wins is 1 greater than number of singleton buckets
    if num_wins - sum(bucket_sizes) == 1:
        bucket_sizes.append(1) # Size of next bucket = 1
        return bucket_sizes 
    
    sum_buck = singleton_bucks #because each contain one
    i = 1
    
    #Base cases if number of buckets equal to number of winners
    if num_wins == num_bucks:
        bucket_sizes += [1 for i in range(0, num_wins-singleton_bucks)]
        return bucket_sizes

    sum_buck = singleton_bucks #because each contain one
    i = 1
    
    while sum_buck>=num_wins or sum_buck+ceil(beta*bucket_sizes[-1])+ceil(beta*beta*bucket_sizes[-1])<num_wins:
        this_buck_size = ceil(beta*bucket_sizes[-1])
        bucket_sizes.append(this_buck_size)
        sum_buck += this_buck_size
        i += 1
    
    this_buck_size = floor((num_wins - sum_buck)/2)
    bucket_sizes.append(this_buck_size)
    this_buck_size = ceil((num_wins - sum_buck)/2)
    bucket_sizes.append(this_buck_size)                                                                           
    
    return bucket_sizes

def get_nice_num(max_num):
    """ (num) -> list
    Return a list of sorted list of nice numbers 
    """
    nice_numbers = []
    for i in range(1, int(max_num)+1):
        if is_nice_num(i):
            nice_numbers.append(i)
    return nice_numbers

#This is basically to get a rounded to nearest integer(called nice number) You can modify it according to your need
def is_nice_num(num):
    """ (num) -> bool
    Return True if num is a nice number, otherwise return False
    """
    #Change this if you want some otehr nearest integers to be called as nice numbers
    #like if you want a competition to give price in the multiple of 7 or something
    while num > 1000:
        num = num/10
    # Conditions :
    if num >= 250:
        return num%50 == 0
    elif num >= 100:
        return num%25 == 0
    elif num >= 10:
        return num%5 == 0
    elif num > 0:
        return isinstance(num, int)
    else:
        return False

def round_to_nice(num_to_round, nice_numbers):
    """ (float, list of int) -> int

    Return the nearest nice number less than num_to_round.

    >>> round_to_nice(6, [1, 2, 5, 10, 15, 20])
    5
    >>> round_to_nice(1, [1, 2])
    1
    >>> round_to_nice(1001, [1, 2, 100, 1000, 10000])
    1000
    """
    if len(nice_numbers) == 0:
        return []
    if num_to_round >= nice_numbers[-1]:
        return nice_numbers[-1]
    if num_to_round < nice_numbers[0]:
        return []
    min_idx = 0
    max_idx = len(nice_numbers) - 1
    idx = (max_idx + min_idx)//2
    curr_val = nice_numbers[idx]
    next_val = nice_numbers[idx+1]
    while curr_val > num_to_round or num_to_round >= next_val:
        # Increase the index. 
        if curr_val < num_to_round:
            min_idx = idx
        elif curr_val > num_to_round:
            max_idx = idx
        idx = (max_idx + min_idx)//2
        curr_val = nice_numbers[idx]
        next_val = nice_numbers[idx+1]
    return curr_val

#Use this function and below direcly to use random bucket sizes(sum of them should equal to the length of unperfect prize(basically N) )
def init_prizes(unperfect_prize, bucket_sizes):    
    """ (list, list) -> list
    Return a list of nice numbers for the prize corresponding to the bucket_sizes such that the sum is less or equal to pool and the leftover.
    """
    # We need to check the sum of bucket sizes matches the unperfect prize 
    if sum(bucket_sizes) != len(unperfect_prize):
        raise NameError('Bucket sizes is incompatible with the number of prizes')
        
    # Take the first unperfect_prize and generate nice numbers list upto that number
    #Like for 500 it will generate list like [500,450,400,350,300,250,225,200,175,150,125,100,90 and so on]
    nice = get_nice_num(int(unperfect_prize[0]))
    prizes = [] # Will contains the first attempt of good prizes this will have leftovers too
    
    curr_nice = round_to_nice(unperfect_prize[0], nice)           #This is pie_T
    prizes.append(curr_nice)
    
    leftover = unperfect_prize[0] - curr_nice
    pos = 1
    
    #bucket is bucket size we will find best number for that bucket which will have some leftover
    for bucket in bucket_sizes[1:]:
        # rounding the first unperfect prize to nearest nice number prizes
        curr_num = (sum(unperfect_prize[pos:pos+bucket]) + leftover)/bucket
        curr_nice = round_to_nice(curr_num, nice)           #This is pie_T
        if curr_nice >= prizes[-1]:
            curr_nice = prizes[-1]
        prizes.append(curr_nice)                            
        # Then compute leftover
        leftover =  (curr_num - curr_nice)*bucket
        pos += bucket
    
    new_prizes       = [prizes[0]]
    new_bucket_sizes = [bucket_sizes[0]]
    for key,value in enumerate(prizes[1:]):
        if prizes[key] > value:
            new_prizes.append(value)
            new_bucket_sizes.append(bucket_sizes[key+1])
        else:
            new_bucket_sizes[-1] += bucket_sizes[key+1]
    return new_prizes, leftover, new_bucket_sizes

#this one will reassign the leftovers to the buckets
#this will also modify bucket sizes for that(Excluding singleton buckets)
def spend_leftover(prizes, bucket_sizes, leftover, singleton_bucks):
    """ (list, list, float) -> (list, list, float)
    Return the finale prizes list along with the bucket_sizes and leftover when all the leftover is spend.
    """
    nice_numbers = get_nice_num(prizes[0])
    # First : Spend as much of possible leftover on singleton buckets
    for i in range(1, singleton_bucks):
        min_val = min(prizes[i] + leftover, (prizes[i-1] + prizes[i])/2)
        nice_val = round_to_nice(min_val, nice_numbers)
        leftover += prizes[i] - nice_val
        prizes[i] = nice_val
        if leftover == 0: #Could choose another value if you are okay with leftover like 1,2,3 or any other value change this
            return prizes, bucket_sizes, leftover    #If at any point leftover turns to 0
    #Now we try to adjust leftovers starting form the final bucket.
    bucket_num = len(bucket_sizes)-1
    
    while bucket_num > 0:
        #If leftover is less than bucket size we won't able to assign equal value to all inside a bucket
        while leftover >= bucket_sizes[bucket_num]:
            prizes[bucket_num] += 1 # Could lead to nice number violations
            leftover -= bucket_sizes[bucket_num] #basically leftover - 1*size of bucket
            
            if leftover == 0: # Could choose another value if you are okay with leftover like 1,2,3 or any other value change this
                return prizes, bucket_sizes, leftover   #If at any point leftover turns to 0
        
        bucket_num -= 1  #Next bucket
        
    return prizes, bucket_sizes, leftover

#Stage 3 of algorithm to adjust monotonicity of the sizes of the buckets
def post_process(bucket_sizes, singleton_bucks):
    change = True
    while change:
        change = False
        i=1
        while i < len(bucket_sizes):
            if  i < singleton_bucks and bucket_sizes[i] != 1 and i < len(bucket_sizes)-1:
                bucket_sizes[i+1] += bucket_sizes[i] - 1
                bucket_sizes[i] = 1
                change = True
            if bucket_sizes[i] < bucket_sizes[i-1]:
                diff = (bucket_sizes[i] + bucket_sizes[i-1])/2
                bucket_sizes[i-1]    = floor(diff)
                bucket_sizes[i]      = ceil(diff)
                change = True
            i+=1
    return bucket_sizes

def write_to_csv_and_ret_json(prizes, bucket_size, file_name='result.csv'):
    csvData   = [['Position', 'Prize']]
    curr_buck = 0
    ret       = {}
    for i in range(0, len(prizes)):
        curr_buck += bucket_size[i]
        if bucket_size[i] == 1:
            csvData.append([str(curr_buck), str(prizes[i])])
            ret[str(curr_buck)] = str(prizes[i])
        else:
            low_num = curr_buck - bucket_size[i] + 1
            pos_range = str(low_num)+'-'+str(curr_buck)
            csvData.append([pos_range, str(prizes[i])])
            ret[pos_range] = str(prizes[i])
    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
        writer.writerow([])
        writer.writerow(['Total Prize', str(dot(prizes, bucket_size))])
        writer.writerow(['Total Winners', str(sum(bucket_size))])
    csvFile.close()
    
    return ret

def payout(winners, prize_pool, first_prize, entry_fee, num_buck, singleton_bucks, save_file='payout.csv'):
    unperfect_prizes = get_unperfect_prize(winners, prize_pool, first_prize, entry_fee)
    bucket_sizes = init_buck_size(winners, num_buck,singleton_bucks)
    initial_prizes, leftover, bucket_sizes = init_prizes(unperfect_prizes, bucket_sizes)
    leftover = prize_pool - dot(initial_prizes,bucket_sizes)
    bucket_sizes = post_process(bucket_sizes, singleton_bucks)
    leftover = prize_pool - dot(initial_prizes,bucket_sizes)
    
    #define leftover here
    singleton_bucks = 0
    for size in bucket_sizes:
        if size == 1:
            singleton_bucks += 1
            
    final_prizes, final_bucket_sizes, final_leftover = spend_leftover(initial_prizes, bucket_sizes, leftover, singleton_bucks)
    Leftover = prize_pool - dot(final_prizes,final_bucket_sizes)
    print (Leftover)
    ret = write_to_csv_and_ret_json(final_prizes, final_bucket_sizes, 'result.csv')
    return ret

if __name__== "__main__":
    B                      = int(input('Total Prize : '))
    N                      = int(input('Total Winners : '))
    P1                     = int(input('First Prize Winner Amount in percentage : '))
    E                      = int(input('Entry Fees or the minimum payout : '))
    num_bucks              = int(input('Total Buckets : '))
    singleton_bucks        = int(input('Total Singleton Buckets at starting : '))

    #Alternatively This
#     B = 125000               #Total Prize
#     N = 2000                   #Total winners  
#     P1 = 25                  #First Prize winner 
#     E =  20                  #Entry fees or the lowest bucker members will get at least this number
#     num_bucks = 20           #Total buckets   
#     singleton_bucks = 10      #Total singleton buckets
    #P1 = 8000000
    P1  = int(B*P1/100)
    ret = payout(N, B, P1, E, num_bucks, singleton_bucks)        
    print (ret)