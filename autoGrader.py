#Created Fall 2019
#This should be used to grade sql assignments by checking output from student files against the output from an answer file
#You will need mysql installed and will need to have python 3.8 and the mysql connector library installed to run

#This only works as long as the student has no syntax errors in there mysql file

import collections
import mysql.connector as mysql
#Connect to mysql this values are subject to change depending on how your mysql is set up
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "1234",
    auth_plugin ='mysql_native_password',
    database = "clearwater" #subject to change if we use a different database per assignment
)
#This will open the sql script and split it on "--" then clean the commands of /n and " "
#Then it runs the commands and saves the answer as a list of tuples.
#executeScripts takes the sql file name you are running
def executeScripts(filename):
    #empty list to return
    returnlist = []
    #opens the file and reads the data from it
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    #splits the commands apart on "--" under each question numbered
    sqlCommands = sqlFile.split('--')

    #num is a stepper variable used to grab the command at a certain index so it can replace any newline characters with a space
    num = 0
    #cleanCommands is the new list after going throught the cleaning process
    cleanCommands = []

    #This for loop is what checks if a newline is in the index and replaces it with a space
    for command in sqlCommands:
        if '\n' in command:
            sqlCommands[num] = sqlCommands[num].replace('\n', ' ')
            num += 1
    #This loop is used to go through and grab all of the indexes that have a select statement and adds it to cleanCommands
    for command in sqlCommands:
        command = command.lower()
        if ('select' in command):
            cleanCommands.append(command)
        
    #Finally this runs the nonempty commands and saves the results to returnlist
    for command in cleanCommands:
        if command != None:
            cursor.execute(command)
            Results = cursor.fetchall()
        returnlist.append(Results)
    #passes returnlist back to the call
    return returnlist

#Grader is where the list of results from the answer file and the test file are compared and then printed if the answer is correct or not
def grader(answer, test):
    #varibles: Checker is a var that will increment if the columns are in a differnt order
    #counter is for steping through the lists
    #stepCount is for if the result is in a different order to compare if the number it checks are still correct to the numbe rin the list
    checker = 0
    counter = 0
    stepCount = 0
    #for loop that checks every answer in the answer list to that in the test list
    for thing in answer:
        #this checks the overall result at the counter index and return a statement if it is correct
        if answer[counter] == test[counter]:
            print("Correct answer for qestion #" + str(counter + 1))
        #if the answer is not the same it will check each index in the list and compare them throught to see if it is in there
        elif answer[counter] != test[counter]:
            for i in test[counter]:
                for j in answer[counter]:
                    if i == j:
                        checker += 1
                stepCount += 1
            if (checker == stepCount):
                print("Correct answer for #" + str(counter + 1) + " but in a differnt location.")

            else:     
                print("Not Correct answer for question #" + str(counter + 1))
                print("Student answer:")
                print(test[counter])
                print("Correct answer:")
                print(answer[counter])
        
        counter += 1

#this just runs the code with the answer key and the student file then calls grader to check the results
answer = []
test = []

cursor = db .cursor()

answer = executeScripts('SQLAssignment2Key.sql')
test = executeScripts('BollamA02.sql')

grader(answer, test)


