# In the future, if we were to add the ability to have surge pricing to your system, what would need to change? 
# For example, maybe we want to surge the prices when there’s a lot of demand in one area at one time
## What tables need changing and/or adding?
### I would add a pricing table that would have fares for rides based on the demand.
### I would also have to update the locations table with a column called demand that will measure the demand level of a given location
## What API methods would you provide?
### I would add an api method to measure the demand level based on the number of available drivers and riders looking for rides
### I would have to add a method called surge pricing that adjusts fares based on the demand level
### I would also add a view demand method that will show the demand level for rides 
## How might existing API methods change?
### I would have to change the add_fare method so it adds the correct fare from the prices table based on the demand 

# In the future, if we were to add the ability to have future scheduling to your system, what would need to change? For example, a user would want to book a fare several days in advance
## What tables need changing and/or adding?
### The rides table would need to be updated with the start date of the scheduled ride and add a boolean to determine if it is a scheduled in advance
## What API methods would you provide?
### I would have to add a method called book_future_ride that will update the rides table with future rides
### another method I would add is the updcoming_rides method to give a rider and driver a list of future rides in order of ascending dates 
## How might existing API methods change?
### the add_ride method needs to be updated so it can account for the boolean that will help us differentiate from a normal ride and a ride scheduled in advance