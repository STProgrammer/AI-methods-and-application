# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 09:17:31 2021

@author: abdka
"""

coins = (1, 5, 10, 20)  #Available coins to use in exchange
sum_amount = 1040528 #The sum amount to exchange

def coin_changer(s, coins):
    # Check if amount is negative. 
    # We could check if any coins are negative too but we just drop that
    if s < 0: 
        print("the amount can't be negative integer")
        return
    coin_change = list() # The list to be used in tabular approach
    # The first is zero, if the amount is zero, we need 0 coins to exchange, that's obvious.
    # It's from there we iterate and answer the question
    coin_change.append(0)
    rest_amount = 0
    rest_amount = s % min(coins) # the amount that can't be exchanged, can be commented to save from 
    # execution time since we don't need it in this case. I just put the value 0 since we will return it anyway.
    for i in range(1, s+1):
        # We set the value inf if the amount is less than the value of coin, then we choose the
        # minimum value among those values
        min_val = min([float('Inf') if (i - j < 0) else coin_change[i - j] for j in coins])
        # If minimum value is Inf, we put 0, that is to avoid Inf if the amount is not 0 but less than any
        # coin available (like if we didn't had any coin valued 1). Else we add min_val + 1, that is because
        # the coin we exchange is 1 more than the minimum exchange rate we used
        min_val = 0 if min_val == float('Inf') else min_val+1
        # We append the minimum value
        coin_change.append(min_val)
    # Now we have a list that shows nr of coins to exchange all amounts from 0 to chosen amount
    # We return the last item on array since that's what we are after - nr of coins needed to exchange 
    # the chosen amount.
    return coin_change, rest_amount
    


def which_coins(coin_change, coins):
    coins_to_use = dict()
    # initialize the dict of coins
    for i in coins:
        coins_to_use[i] = 0
    i = len(coin_change)-1  # the max index is i, it's the amount to exchange
    while i > 0: # while some amount is still left
        # array of values
        values = [float('Inf') if (i - j < 0) else coin_change[i - j] for j in coins]
        
        # choose the minimum in the array
        min_val = min(values)
        
        # break if it's INF, it means there's some rest money that can't be changed
        if min_val == float('Inf'):
            break
        
        # the corresponding coin to use that gives the minimum number of coins to change
        min_coin = coins[values.index(min_val)]
        
        # increase the coin in the dict
        coins_to_use[min_coin] += 1
        
        # reduce the i by the amount of coin used to change
        i = i - min_coin
        
    return coins_to_use



coin_change, rest_amount = coin_changer(sum_amount, coins)

coins_to_use = which_coins(coin_change, coins)

print("The minimum coins needed to exchange %d is %d \n" %(sum_amount, coin_change[-1]),
      "when the avialable coins are", coins, 
      "\n The amount that is left after changing is %d" %(rest_amount))

print("The coins to use for change are", coins_to_use)

