import csv
import time
import os
from os import system, name

NoOfItems = 0   # Number Of Items
Cap_k = 0       # Limit of Knapsack
w_I = [0]       # List of Weight of items
Val = [0]       # List of Value of items
User_input = 'nothing'
choice = 'nothing'
tab = []        # DP table
m_input= -1
print('WELCOME TO THE KNAPSACK PROBLEM OPTIMAL SOLUTION SIMULATOR ')
print('___________________________________________________________')
print('STUDENT ID: 2499888\n'
      'DATE: 9/04/2020\n'
      'COMPUTER SCIENCE PROJECT\n')


def clear():        #Clear terminal screen
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
def ReadCSV():      #Import CSV File
    with open(CSVfile) as csvfile:
        CSV = csv.reader(csvfile, delimiter=',') #Reads name od CSV file
        w_I = [0]
        Val = [0]
        Weight = []
        Items = []

        for row in CSV:
            try:
                Weight.append(int(row[0]))  # Adds Capacity of Knapsack and weights of items to a list
                Val.append(int(row[1]))  # Adds the corresponding values to a list
            except:
                pass

    Cap_k = Weight[0]  # Takes the Capacity of Knapsack from the first row

    for i in Weight[1:]:  # Removes Capacity of Knapsack and adds weights to list
        w_I.append(i)

    NoOfItems = len(w_I)-1  #Calculate Number of items present
    tab = [[0 for x in range(Cap_k + 1)] for x in range(NoOfItems + 1)] #Create 2 dimensional array to store calculated values

    return w_I, Val, Cap_k, NoOfItems, tab

def failproof(user):        #Validation of user input
    while m_input < 0:      #Runs till valid input is received
        try:
            value = int(input(user))
            return value
        except:
            print('Invalid input')

def InputValues():          #Stores User input
	clear()
	count = 0
	global Cap_k,w_I,Val,tab,NoOfItems
	NoOfItems = int(failproof('How many Items are available?\n'))
	Cap_k = int(failproof('What is the capacity of the knapsack?\n'))
	w_I = [0]
	Val = [0]
	tab = [[0 for x in range(Cap_k + 1)] for x in range(NoOfItems + 1)]  #Create 2 dimensional array to store calculated values
	Items = []


	while count != NoOfItems: #Runs till all values have been entered
		clear()
		try:
			Weight = int(input('Enter weight \n'))
			w_I.append(Weight)      # Add Weights entered by user to list
		except ValueError:
			print('Invalid Float. Enter a valid number \n')
			continue

		try:
			Value = int(input('Enter item value \n'))
			Val.append(Value)        # Add Values entered by user to list
			count += 1
		except ValueError:
			print('Invalid Float. Enter a valid number \n')
			continue
	return NoOfItems,Cap_k,w_I,Val,tab

def Main_Menu():

    print('\nMAIN MENU\n'
          '1. Select CSV file\n'
          '2. Input Values Manually\n'
          '3. Run program\n'
          '4. Reset\n'
          'q. Quit \n')

def RunProgram():
    print('\n1. Dynamic programming Approach\n'
          '2. Brute force Approach\n'
          '3. Greedy Method\n'
          'q. Go back to main menu\n')

def DynamicProgramming(NoOfItems,Cap_k,tab,w_I,Val):
    t1 = time.perf_counter_ns() #Start time Counter
    if NoOfItems == 0:  #If items are not available
        print('No Items are present')
        pass
    else:
        for i in range(1, NoOfItems + 1):  # Row-Items available
            for w in range(1, Cap_k + 1):  # Column- Max Capacities of knapsack

                notTaking = tab[i - 1][w]  # Takes item one row above with same Capacity of knapsack
                take = 0

                if w_I[i] <= w:  # If item weight is less than the capacity of knapsack
                    take = Val[i] + tab[i - 1][w - w_I[i]]  # Add value of item to the max value of previous items able to fit

                tab[i][w] = max(notTaking, take)  # Take the max value

            w = Cap_k
            T_weight = 0

        print('Item taking      Item Weight      Item Value')
        print('___________     _____________    _____________')

        for n in range(NoOfItems, 0, -1):

            if tab[n][w] != 0 and tab[n][w] != tab[n - 1][w]:  # Pick the items choosing
                print('%4d               %4d              %4d' % (n, w_I[n], Val[n])) #Print results
                w = w - w_I[n]      #Knapsack limit - item weight

                T_weight += w_I[n]  #Add weight of item

        print('\nTotal benefit: %d' % tab[NoOfItems][Cap_k])
        print('Total weight: %d' % T_weight)
        t2 = time.perf_counter_ns() #End time Counter
        t3 = (t2 - t1) #Finds the difference in time difference
        print('Time Complexity: ', t3), ' ns'


def GreedyMethod(capacity, weight,values,Item_no):
    if Item_no == 0:
        print('There is no item present')
        pass

    else:
        t1 = time.perf_counter_ns()     #Start time Counter
        Items = []
        value = 0  # Total profit
        v = 0
        c = 0
        values.pop(0)  # Remove 0 from original values list to avoid Zero division
        weight.pop(0)  # Remove 0 from original weight list to avoid Zero division
        density = sorted([[values[i] / weight[i], weight[i], values[i]] for i in range(Item_no)],
                         reverse=True)  # Sorts number in decreasing order

        # Note that list is arranged in this format (Density,Weight,Value)
        while capacity > 0 and Item_no > 0:
            max = 0  # Maximum profit per weight
            index = None
            for i in range(Item_no):
                if density[i][1] > 0 and max < density[i][0]:  # Choose the maximum density form the list
                    max = density[i][0]  # Maximum profit per weight
                    index = i  # Stores index of the item

            if density[index][1] <= capacity:  # Checks whether weight is less than Knapsack limit
                value += density[index][2]  # Adds cumulative sum of values to the knapsack
                v = density[index][2] # Records the value of item to print in list
                c = density[index][1] # Records the weight of item to print in list
                capacity -= density[index][1]  # Subtracts the weight of item from total capacity
                Items.append((density[index][0], density[index][1], v, value, c,capacity))  # Creates a list of profit per weight, weight of item, value of item, Total value, Capacity of item taken, Capacity of knapsack remaining

            else:
                if density[index][1] > 0:  # If item is still present
                    value += (capacity / density[index][1]) * density[index][1] * density[index][0]  # Takes fraction of the item
                    v = (capacity / density[index][1]) * density[index][1] * density[index][0] #Records the fraction taken
                    c = capacity
                    capacity -= c
                    Items.append((density[index][0], density[index][1], v, value, c, capacity)) #Adds data to a list
                    break

            density.pop(index)  # Removes item from the list
            Item_no -= 1  # Reduces number of items

        print('Profit per weight     Weight     Value      Profit in Knapsack     Weight Taken    Capacity remaining')
        print('___________________  ________   _______    ____________________   ______________   ___________________')
        for i in Items:
            print('%+6.5e          %4d       %4d            %4d                %4d              %4d' % (
                i[0], i[1], i[2], i[3], i[4], i[5])
                  )

        print('\nTotal profit: ', value)
        t2 = time.perf_counter_ns() #End time Counter
        t3 = t2 - t1 #Find the time difference
        print('Time Complexity: ', t3)
        values.insert(0, 0)
        weight.insert(0, 0)



class BruteForce: # Class for Brute Force Method
    def __init__(self,Weight,Value,NoOfItems,Cap_k): #Initialze system variavles
        self.Weight = Weight        # Weight of item
        self.Value = Value          # Value of item
        self.NoOfItems = NoOfItems  # Number of items
        self.Cap_k = Cap_k          # Capacity of knapsack


    def setMaker(self): #Creates a list to store item, weight and value
        set = []
        for i in range(0,self.NoOfItems):  #Loops till all items are considered
            set.append((i,self.Weight[i],self.Value[i])) #Adds data to a list
        return set



    def power_set(self,input):
        # returns a list of all subsets of the list
        count = 0
        if (len(input) == 0): #If list is empty returns empty sey
            return [[]]
        else:
            m_subset = []  #Initialize list to store all subsets
            for s_subset in self.power_set(input[1:]):  #Loops till all items are considered for every possiblity
                m_subset += [s_subset] # Add current item to list
                m_subset += [[input[0]] + s_subset] # Add remaining items to form subsets
            return m_subset



    def knapsack(self,input):
        knapsack = [] #Initialize list to store selected items
        total_weight = 0  # Total weight of optimal solution
        best_value = 0    # Best profit
        for i_set in input:     #Loops till all subsets are considered
            initial_weight = sum([i[1] for i in i_set]) #Add all weights of items in each subset
            initial_value = sum([i[2] for i in i_set])  #Add all values of items in each subset
            if initial_value > best_value and initial_weight < self.Cap_k: # Constraints of knapsack
                best_value = initial_value
                total_weight = initial_weight
                knapsack = i_set
        return knapsack,total_weight,best_value


##________MAIN PROGRAM STARTS HERE______________________##

while User_input != 'q': # Main program runs till user decides to quit

    Main_Menu()
    User_input = input('')

    if User_input == '1':
        clear() #Clears screen terminal
        CSVfile = input('Type the name of your CSV File here')
        x = os.path.isfile(CSVfile) #Checks for CSV file path
        if x: #If CSV file is found in current path
            print('File successfuly retrieved')
            w_I,Val,Cap_k,NoOfItems,tab = ReadCSV()
        else: #IF CSV file cant be found in current path
            print('File not available')
            continue

    if User_input == '2':
        clear() #Clears terminal screen
        InputValues()

    while User_input == '3':
        RunProgram()

        choice = input('Please pick the method you would like to use.')
        if choice == '1':
            DynamicProgramming(NoOfItems,Cap_k,tab,w_I,Val) # Dynamic Programming algorithm


        if choice == '2':
            clear()     #Clears terminal screen
            if NoOfItems == 0: #If No items are available
                print('Items not available')
                pass
            else:
                t1 = time.perf_counter_ns() #Starts to time algorithm
                knapsack = BruteForce(w_I, Val, NoOfItems, Cap_k) #Brute Force Algorithm
                U_set = knapsack.setMaker() #Main set of items
                Subsets = knapsack.power_set(U_set) #All subsets of items
                Items, OptWeight, OptProfit = knapsack.knapsack(Subsets)

                print('Item taking      Item Weight      Item Value')
                print('___________     _____________    _____________')
                for i in Items:
                    print('%4d               %4d              %4d' % (i[0], i[1], i[2]))

                print('\nBest profit : %4d' % OptProfit) #Print best profit
                print('Total weight: %4d' % OptWeight)    #Print total weight
                t2 =  time.perf_counter_ns() #End timer
                t3 = (t2 - t1) # Find the difference in time
                print('Time Complexity: ', t3, ' s')    #Print time


        if choice == '3':
            clear()     #Clears terminal screen
            GreedyMethod(Cap_k,w_I,Val,NoOfItems)   #Greedy Method algorithm



        if choice == 'q': #Goes back to the main menu
            clear()     #Clears terminal screen
            break

    if User_input == '4': #Resets algorithms. Clears list of all items
        clear()     #Clears terminal screen
        NoOfItems = 0
        Cap_k = 0
        w_I = [0]
        Val = [0]
        Items = []
        tab = [[0 for x in range(Cap_k + 1)] for x in range(NoOfItems + 1)]


print('Program successfully ended')




















































