#!/usr/bin/env python
# coding: utf-8

# # This workbook was made for use in UCC Physics and Astronomy Society Annual General Meeting Election

# In[208]:


# Importing necessary modules
import pandas as pd
import tabulate as tb
import math


# ### Importing the ballots and cleaning up the file

# In[215]:


# Imports a data file named "Ballots.csv"
ballots = pd.read_csv("Ballots.csv").fillna(0)

# Removing timestamp
ballots.drop('Timestamp', inplace=True, axis=1)

# Converting to integer values
ballots = ballots.astype('Int64')


# ### Seperating the combined ballots into ballots for each position

# In[216]:


candidates = ballots.columns.values.tolist()
for i in candidates:
    name = str(input("What is the candidate name for " + str(i) + ": "))
    ballots = ballots.rename({str(i) : name}, axis=1)


# #### Initialising total number of preferences

# In[217]:


num_preferences = len(ballots.columns.values.tolist())


# ### Defining the methods for counting the votes

# #### Counts the number of preferences each candidate received

# In[192]:


def tally(ballots, candidate):
    
    # Initialising preference counts
    pref_1 = 0
    pref_2 = 0
    pref_3 = 0
    pref_4 = 0
    pref_5 = 0
    pref_6 = 0
    pref_7 = 0
    pref_8 = 0
    pref_9 = 0
    pref_10 = 0
    
    # Counting number of preferences
    for j in ballots[candidate]:
        if j == 1:
            pref_1 += 1
        if j == 2:
            pref_2 += 1
        if j == 3:
            pref_3 += 1
        if j == 4:
            pref_4 += 1
        if j == 5:
            pref_5 += 1
        if j == 6:
            pref_6 += 1
        if j == 7:
            pref_7 += 1
        if j == 8:
            pref_8 += 1
        if j == 9:
            pref_9 += 1
        if j == 10:
            pref_10 += 1
    
    return pref_1, pref_2, pref_3, pref_4, pref_5, pref_6, pref_7, pref_8, pref_9, pref_10


# #### Gets the candidate(s) with the lowest value pref

# In[193]:


def get_indexes_min_value(list):
    
    # Removing 0's from the list
    for i in list:
        if i == 0:
            list.pop(i)
    # What is the minimum value
    min_value = min(list)
    
    # If there are more than one minimum value (tied last) then return both indices
    if list.count(min_value) > 1:
        return [i for i, x in enumerate(list) if x == min(list)]
    
    # Else return the index of the minimum value
    else:
        return list.index(min(list))


# #### Gets the candidate(s) with the highest value pref

# In[194]:


def get_indexes_max_value(list):
    
    # Wat is the maximum value
    max_value = max(list)
    
    # If there are more than one maximum value then return both indices
    if list.count(max_value) > 1:
        return [i for i, x in enumerate(list) if x == max(list)]
    
    # Else return the index of the maximum value
    else:
        return list.index(max(list))


# #### Calculates the valid poll and droop quota

# In[195]:


def quota(ballots):
    
    candidates = ballots.columns.values.tolist()
    votes_with_no_first_preference = ballots.copy()
    
    # Calculating how many votes have no preferences
    for i in candidates:
        votes_with_no_first_preference = votes_with_no_first_preference[votes_with_no_first_preference[i] != 1]
    total_invalid_votes = len(votes_with_no_first_preference)
        
    # Calculate the valid poll and droop quota
    valid_poll = len(ballots) - total_invalid_votes
    droop_quota = math.floor(valid_poll / 2) + 1
    
    return droop_quota, valid_poll


# #### Prints the tallies as they stand

# In[196]:


def print_results(ballots):
    
    # Gets the list of Candidates
    candidates = ballots.columns.values.tolist()
    # Initialises the output table with the headings
    output = [["Candidate", "1st Preference", "2nd Preference", "3rd Preference", "4th Preference", "5th Preference", "6th Preference", "7th Preference", "8th Preference", "9th Preference", "10th Preference"]]
    
    #Calculates the total pref for each candidate and appends it to output table
    for i in candidates:
        pref_1, pref_2, pref_3, pref_4, pref_5, pref_6, pref_7, pref_8, pref_9, pref_10 = tally(ballots, i)
        output.append([i, str(pref_1), str(pref_2), str(pref_3), str(pref_4), str(pref_5), str(pref_6), str(pref_7), str(pref_8), str(pref_9), str(pref_10)])
        
    print(tb.tabulate(output, headers="firstrow") + "\n")


# #### Checks if a candidate has reached a quota and eliminates the candidate with the lowest 1st preference if not

# In[197]:


def eliminate(ballots):
    
    candidates = ballots.columns.values.tolist()
    count = []
    
    for i in candidates:
        pref_1, pref_2, pref_3, pref_4, pref_5, pref_6, pref_7, pref_8, pref_9, pref_10 = tally(ballots, i)        
        count.append([i, pref_1, pref_2, pref_3, pref_4, pref_5, pref_6, pref_7, pref_8, pref_9, pref_10])
    
    # Checks the first preferences
    all_pref_1 = [row[1] for row in count]
    
    # Check if any candidate has reached the quota
    highest = max(all_pref_1)
    droop_quota, valid_poll = quota(ballots)
    
    if highest >= droop_quota:
        highest_candidate = get_indexes_max_value(all_pref_1)
        print(candidates[highest_candidate] + " has reached the quota and is deemed elected \n")
        return True
    
    # Get the lowest candidate(s) if no winner
    eliminated = get_indexes_min_value(all_pref_1)
    
    # If only one candidate has the lowest 1st preferences then eliminate them and redistribute preferences
    if type(eliminated) == int:
        # Prints elimination
        print(candidates[eliminated] + " is eliminated as they have the lowest 1st preferences of remaining candidates \n")
        # Redistributes preferences
        eliminated_ballots = redistribute_preferences(ballots, candidates[eliminated])
        # Removes candidate
        eliminated_ballots.pop(candidates[eliminated])
        
    # If multiple candidates have tied lowest 1st preferences then tally their second and eliminate
    elif len(eliminated) > 1:
        all_pref_2 = [row[2] for row in count]
        eliminated_2 = get_indexes_min_value(all_pref_2)
        
        if type(eliminated_2) == int:
            # Prints elimination
            print(candidates[eliminated[0]] + " & " + candidates[eliminated[1]] + " had a tied 1st preference so " + candidates[eliminated_2] + " was eliminated on 2nd preferences \n")
            # Redistributes preferences
            eliminated_ballots = redistribute_preferences(ballots, candidates[eliminated_2])
            # Removes candidate
            eliminated_ballots.pop(candidates[eliminated_2])
        
        # If still tied then print below as coin flip will have to be done
        else:
            print("Multiple candidates have tied preferences \n")
            return False
    
    return eliminated_ballots


# #### Redistributes the preferences of the eliminated candidate

# In[198]:


def redistribute_preferences(ballots, candidate):
    
    updated_ballots = ballots.copy()
    
    for p in range(1, len(updated_ballots.columns.values.tolist()) + 1):
        # Getting the index of each vote that has the eliminated candidate as 1st preference
        votes_to_distribute_index = updated_ballots.loc[updated_ballots[candidate] == p].index.tolist()
        
        # Dataframe with all votes for that candidate
        votes_to_distribute = updated_ballots.loc[votes_to_distribute_index, :]
        
        # Replacing 2nd Pref with 1st Pref etc.
        # For every vote
        for i in range(len(votes_to_distribute)):
            # For every preference in that vote
            for j in range(len(updated_ballots.columns.values.tolist())):
                # For every value that preference can be
                for k in range(p, num_preferences + 1):
                    # Add one to every preference
                    if votes_to_distribute.iloc[i, j] == k:
                        votes_to_distribute.iloc[i, j] = k-1

        updated_ballots.update(votes_to_distribute)
        
    return updated_ballots


# ### Main function

# In[206]:


def main(ballots):
    
    active_ballots = ballots
    
    for i in range(0, len(ballots.columns) - 1):
        
        # Print Count
        print("Count " + str(i+1))
        
        # Print Quota
        droop_quota, valid_poll = quota(active_ballots)
        print("Total valid poll is = " + str(valid_poll))
        print("Quota is = " + str(droop_quota) + "\n")
        
        # Print Results
        print_results(active_ballots)
        
        #Check for winner and eliminate if none
        active_ballots = eliminate(active_ballots)
        
        # True is if winner is found. False is if a winner couldn't be determined
        if type(active_ballots) == bool:
            if active_ballots == True:
                print("Winner has been found")
                return
            if active_ballots == False:
                print("No winner could be determined")
                return


# # The Count

# In[218]:


main(ballots)

