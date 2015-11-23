INFORMATION on what this program is:

This program runs multiple simulations at once and then graphs these simulaltions

The simulation being run is a simulated ward with the size being X by X
an infection is randomly put in the population and is spread based on a percentage
and a vaccination is being given out and its successfulness is based on another 
percentage

after k amount of days, the infected will become healed, thus immune to more sickness

HOW TO RUN: *********************************
The values used for this script are:

k = days a person can be infected
tau = infection spread rate (0-1) (percentage)
nu = vaccination rate (0-1) (percentage)
gridsize = a value that is both the amount of rows and columns
total = total amount of threads/simulations to run

To run this script, just run it how you would normally and the values will be put
in for you with these default values:

k = 20
tau = .2
nu = .1
gridsize = 10
total = 100

Changing the script:::::
********************************************************************
BUT if you want to change values, you add parameters to change them with params: 
-nu (change nu)
-tau (change tau)
-k (change k)
-grid (change gridsize)
-threads (change total)

Example:
    if you want to change k to 30 you type ./cwill159_hw10.py -k 30

Example 2:
    if you want to change k to 30, tau to .5 nu to .2
        ./cwill159_hw10.py -k 30 -tau .5 -nu .2


