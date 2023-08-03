# **Distributed Systems Assignment 2**
## **Report**
**P Shiridi Kumar**

**2021121005**
***
- **Q2** :
    - The given input is formatted in the runner script in the form of [n,m,row,column,value,matrix_num] where n and m are the dimensions of the resultant matrix(i.e, rows in matrix 1 and columns matrix 2)

    - The given input is then passed to matrix and mapper outputs in such a way that the keys are the indices of resultant matrix and values are its dependednt values in matrix A and matrix B (one key will have multiple values)

    - reducer ensures that all the entries with same key will be handled by a same reducer and since the order is sorted we can calculate corresponding entries in result matrix in one traversal of the output of mapper.py.

    - Time complexity : output of mapper contains $$(2*n*m*p) $$ entries which will be traversed once by reducer therefore timecomplexity is  $$O(n*m*p)$$

- **Q3** :
    - Given input  n is formated in runner script such that the input containe multiple lines , because of which the input might be processed multiple mappers and because of mutliple splits for sufficiently large input

    - In the mapper code it just performs the given task the number of times as in the number of lines in the input. which would be then forwarded to reducer with keys being same for all the values so that all values got to the same reducer in order to calculate the expectation.

    - Analysis of number of runs (Program is simulated 50 times for each run input):


	|number of runs |	ERROR(RMSE of 50 simulations)|	Confidence 50%|	Confidence 98%|
    |---------------|--------------------------------|-----------------|-----------   |
    |10	|0.2753	|2.7044 - 2.7433|	2.6857 - 2.762
    |100 |	0.2672|	2.7041 - 2.7419	|2.686 - 2.76
    |200 |	0.2591|	2.7048 - 2.7414	|2.6872 - 2.759
    |500 |	0.2516|	2.7045 - 2.7401	|2.6874 - 2.7572
    |1000 |	0.2446	|2.7045 - 2.7391	|2.6879 - 2.7557
    |10000 |	0.2381|	2.7048 - 2.7384	|2.6886 - 2.7546
    |100000	|0.2321|	2.705 - 2.7379|	2.6893 - 2.7536


    ***