# Mandatory Exercise 6 in DTE-2501 code by Abdullah Karagoez

import numpy as np



# Serie names
serie_names = ['Vikings', 'Breaking Bad', 'The Sopranos', 'Westworld',
                        'Game of Thrones', 'The Witcher', 'Skam', 'Les bureau']


# Vector for all useres except the active user to predict its vote
user_vectors = np.array([[5,5,None,3,4,None,None,None],
                         [4,3,3,4,5,2,3,3],
                         [1,3,3,2,2,3,4,1],
                         [None,3,None,None,None,5,None,None],
                         [3,4,None,4,5,5,1,None],
                         [4,5,2,5,3,2,2,3],
                         [1,1,None,None,2,1,None,None]
                         ], dtype=np.float64)


# Function to predict vote for a product given user vector and active users and serie names above

# Here, rather than passing serie names and user vectors as parameters, we get them outside the function.
# As parameters we only pass active user vector and the product name to predict the vote on.
def predict_vote(active_user, product_name, kappa=1):
    
    # We put the active user vector and other users' vectors into a single Numpy 2D array
    all_users = np.append(user_vectors, [active_user], axis=0)

    # We calculate mean vote for each user (taking nansum divided by number of non-nan values on each user)
    mean_votes = np.nansum(all_users, axis=1) / np.sum(~np.isnan(all_users), axis=1)
    
    # We reshape the mean votes array to make the subtraction easier
    mean_votes = mean_votes.reshape(-1,1)
    
    # We substract user votes from their mean votes, get Numpy 2D array for variances
    variances = all_users - mean_votes
    
    correlations = list()
    
    # For each user we calculate the correlation coefficients, and append it to correlations list
    for i in range(len(user_vectors)):
        # We use np.ma module and masked arrays to ignore nan values and calculate
        # correlation coefficients between active user and each user on the user vectors
        correlation = np.ma.corrcoef(np.ma.masked_invalid(variances[i,:]),
                                     np.ma.masked_invalid(variances[-1,:]))[0][1]
        
        correlations.append(correlation)
        

    correlations = np.array(correlations)
    
    # Taking sum of correlation coefficient multiplied by variance for
    # each user (except the variance of active user)
    sum_correlation_variance = np.nansum(correlations * variances[:-1, serie_names.index(product_name)])
    
    # Calculating the predicted vote by using mean of active user vote pluss 
    # kappa multiplied by sum_correlation_variance (which was calculated above)
    predicted_vote = mean_votes[-1][0] + kappa*sum_correlation_variance
    
    return predicted_vote



# The vector for the active user, or user to predict its votes
new_user = np.array([3,2,3,None,4,1,None,5], dtype=np.float64)


# Predicting for Westworld and Skam (and printing the results)

title = 'Westworld'
print("Predicted vote for %s is %.4f" % (title, predict_vote(new_user, title)))

title = 'Skam'
print("Predicted vote for %s is %.4f" % (title, predict_vote(new_user, title)))

# RESULTS:
# Predicted vote for Westworld is 4.65
# Predicted vote for Skam is 1.99


