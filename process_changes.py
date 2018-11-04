# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 16:44:26 2018

@author: aneta sokolowska
@student number: 10379935

"""
# importing the relevant libraries
# 1. pandas - for data manipulation and analysis. Pandas offers data structures 
# and operations for manipulating numerical tables and time series
# 2. importing Counter from collections for counting hashable objects
# 3. matplotlib.pyplot for plots
import pandas as pd 
from collections import Counter
import matplotlib.pyplot as plt

class Commit(object):
    
    def read_file(self,changes_file):
        data = [line.strip() for line in open(changes_file,'r')]
        return data
        # Using strip to strip out spaces and trim the line. 
        # Opening the file called 'changes_file' and assigning it to new variable 
        # called 'data' which is not fully cleaned yet, 'data' type is a list
        
    def get_commits(self,data):
        sep = 72*'-' 
        commits = [] 
        # Creating new list called 'commits' to assign our new/cleaned file into it. 
        index = 0
        while index < len(data):
            try:
                #I can see in the file A, D and M, for the purpose of this assignment 
                #I assume that A is for Add, D is for delete and M is for modify.
                #Calculating the foloowing tasks: add, modify, delete. 
                task_index=index+3
                #To get to 3rd line of the file where A, D and M appears I need to assign
                #'task_index' to be equal 'index' + 3
                #'index' as per above line 31 starts at 0 which means 'task_index' will start at 3
                count_Add=0
                count_Delete=0
                count_Modify=0
                #Starting point for counting Add, Delete and Mofify  is zero as per above.
                check_task=1
                #Creating condition/variable called 'check_task' which is equal 1, 
                #this is for the purpose of the while loop below.
                #While loop will loop as long as 1 is not equal to 0 and it will stop
                #when it gets to 0, this means it will stop after counting all of the required letters.
                while check_task != 0:
                    letter = data[task_index][0]
                    #Creating new variabke called 'letter', this is assigned to the data file 
                    #called changes_file and the 'task_index' which as oer line 44 starts from 3
                    #This will start as letter=data[3][0]. This will read the third position in data 
                    #and the index 0
                    if letter == 'A':
                        count_Add += 1
                        #Counting the appearance of letter A in the changes_file log
                    elif letter == 'D':
                        count_Delete += 1
                        #Counting the appearance of letter D in the changes_file log
                    elif letter == 'M':
                        count_Modify += 1
                        #Counting the appearance of letter M in the changes_file log
                    task_index = task_index + 1   
                    find_space = data[task_index]
                    check_task = len(find_space)
                    #When 'check_task' reach the length of 'find_space' equal to 0 
                    #then the loop will stop looping.
                # parse lines that start with: r1551925
                details = data[index + 1].split('|')
                #'details' is my new list that will be created with the 'changes_file' log
                # with the split '|' 
                # the author with spaces at end removed.
                #creating 'commi' dictionary and stripping information not relevant fr the assesment.
                commit = {'revision': details[0].strip(),
                          #In the first part of the 'changes_log' removing space after the 
                          #'revision'
                    'author': details[1].strip(),
                    #In the second part removing space that appears after the 'name' 
                    'date': details[2].strip(),
                    #In the third part removing space after the 'date'
                    'number_of_lines': details[3].strip().split(' ')[0],
                    #In the next part removing space after 'number_of_lines' and splitting 
                    #the remaining part from it
                    'add': count_Add,
                    #Counting Add
                    'modify': count_Modify,
                    #Counting Modify
                    'delete': count_Delete
                    #Counting Delete
                    }
                commits.append(commit)
                #Appending the list 'commits' with the information from the dictionary 'commit'
                index = data.index(sep,index + 1)
            except IndexError:
                break
        df = pd.DataFrame(data=commits) #Reading the dataset in a dataframe using pandas
        return df
        
    
    #the below function was created to get dates from the  list of: commit['date']
    def get_dates(self,dates):
        plus_index="+"
        date_list=[]
        for i in range(len(dates)):
            index=dates[i].index(plus_index)
            #print(index)
            checking_dates=dates[i][0:index-10] # as per print(index) the index is 20 pulling 10 characters
            date_list.append(checking_dates) #list of dates
        return date_list
        
        
    
if __name__ == '__main__':
    # open the file - and read all of the lines.
    call_object=Commit()
    changes_file='changes_python.log'
    data=call_object.read_file(changes_file)
    commits=call_object.get_commits(data)
    print('The cleaned dataset amount of lines is now equal to ' + str(len(commits)) +'.')
    print()
             
    #checking dates when the tasks were performed by calling get_dates function
    dates_in_the_log=call_object.get_dates(commits['date'])
    print(dates_in_the_log) #checking the dates 
    checking_dates=pd.unique(dates_in_the_log)
    #pd.unique will return unique values from 'dates_in_the_log' in order of appearance
    checking_dates.sort()
    #sort() function will sort the order of the dates
    print()
    print('The log tasks dates are between ' + str(checking_dates[0]) + ' and ' + checking_dates[len(checking_dates)-1])
    #because the dates were sorted we can now get the first date calling it by the 0 index
    #and the last date by calling the last date 
    print()
    
    #statystical analysis of the tasks add, delete and modify
    print('Please see below the statistical analysis of the log: ')
    print()
    statystical_analysis = commits.describe() # describe() function would provide count,
    #mean, standard deviation (std), min, quartiles and max in its output
    print(statystical_analysis)
    print()
    
    #checking names in the file
    checking_names=pd.unique(commits['author'])  #get unique names from commits['author']
    list_unique_names=checking_names.tolist() #changing 'checking_names' to list
    print ('These names in the file: ' + str(checking_names))
    print()
    authors_list=commits['author']
    proper_list_of_authros=authors_list.tolist() #converting proper_list_of_authors to a list
    print ('Please see below all of the names appearing in the file along with their activity number:')
    counts=Counter(authors_list) #using counter function to calculate how many times name appears in the file
    print(counts)
    print()

    #below bar chart ilustrates the user names and their frequency 
    name_counts = Counter(authors_list)
    df = pd.DataFrame.from_dict(name_counts,orient='index')
    ax = df.plot(kind='barh', title = 'NAMES AND THEIR AMOUNT OF LOG', legend = False,figsize=(12,4), color='#9c9ede')
    #the bar char is kind of 'barh' which means it is going to be horizontal
    ax.set_xlabel('FREQUENCY',fontsize=9) 
    #assigning name to x as 'FREQUENCY'
    ax.set_ylabel('NAMES',fontsize=9)
    #assigning name to y as 'NAMES'
      
    #below pie chart ilustrates the tasks 
    add = sum(commits['add'])
    delete = sum(commits['delete'])
    modify = sum(commits['modify'])
    labels = ['ADD','DELETE','MODIFY']
    values = [add,delete,modify]
    colors = ['#ad494a','#d6616b','#e7969c']
    explode = (0.1, 0.1, 0.1) # explode all parts 
    plt.figure(figsize=(6,6))
    bx = plt.pie(values, explode=explode, labels=labels, colors=colors,autopct='%2.2f%%', shadow=True, startangle=10)
    plt.title('FREQUENCY OF TASKS')
    plt.axis('equal')
    plt.show()
    
    #below plot ilustrates the task 'delete' per name
    dfchart=pd.DataFrame({'xvalues': commits['author'],'yvalues': commits['delete']})
    plt.bar('xvalues','yvalues',data=dfchart,color='#bd9e39')
    plt.xticks(rotation='vertical')
    plt.margins(0.1)# to keep spaces at the beginning and the end of chart 
    plt.subplots_adjust(bottom=0.1)
    plt.title('TASK DELETE SORTED BY NAME')
    plt.show()
    
    #below plot ilustrates the task 'add' per name
    dfchart=pd.DataFrame({'xvalues':commits['author'],'yvalues':commits['add']})
    plt.bar('xvalues','yvalues',data=dfchart,color='green')
    plt.xticks(rotation='vertical') # keeping vertical for better visability
    plt.margins(0.1)# to keep spaces
    plt.subplots_adjust(bottom=0.1)
    plt.title('TASK ADD SORTED BY NAME')
    plt.show()
    
    #below plot ilustrates the task 'modify' per name
    dfchart=pd.DataFrame({'xvalues':commits['author'],'yvalues':commits['modify']})
    plt.bar('xvalues','yvalues',data=dfchart,color='orange')
    plt.xticks(rotation='vertical')
    plt.margins(0.1) # to keep spaces
    plt.subplots_adjust(bottom=0.1)
    plt.title('TASK MODIFY SORTED BY NAME')
    plt.show()
  
  

    
    
    