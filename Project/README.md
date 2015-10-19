# 4511W Project: The Tower Of Hanoi
Name: Wen Chuan Lee
x500: leex7095

## Running the Python Script

Script should be executed on Python 3.4 or later, if on a CSELabs machine, first do

`module load soft/python/3.4`

This is required to load the modules or else the timer module way have syntax errors.

After that, *execute the script with*: `python3 hanoi.py` 

This will solve an instance of the Tower of Hanoi Problem and provide verbose output, edit the integer passed to `runTestsInteractive(number)` where `number` is the number of disks (at least 3).

To run a range of tests and generate CSV files that contain metrics (which I am doing to collect experimental data), execute the function `runAllTests(start,end)` with the `start` value being at least 3 disks, and any end value. This will run every algorithm implemented and save output. 

## Approach

I still based this Tower of Hanoi problem using the previously provided problem framework, as it was easy to abstract the problem from the algorithm, this allowed me to later implement bi-directional BFS after BFS and then Iterative DFS as well as Iterative Deepening DFS.

## State of Code

All code is functional. Some tiny performance improvements can be made by removing certain assertions but all the algorithms and additional ones have been **correctly** implemented. 
