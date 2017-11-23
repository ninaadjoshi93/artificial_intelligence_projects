#!/usr/bin/env python
# put your group assignment problem here!
# This is problem 2 - where you need to assign members to team in such a way that it would lower the time taken by
# the grader to grade the assignment.
# Have discussed on a high level with saurabh agrawal but no code or design was shared among us.
'''
Abstraction:

Here for each iteration, based on the input configuration which is possible grouping of users in a team
i.e A state, we are finding the total cost for this current state along with cost of each person when kept alone.
For example: if n students give the survey
The initial configuration is: [[nth user][nth - 1 user][nth - 2 user]....[]]
So for 4 students intial configuration will be : [[user1][user2][user3][user4]]

This is an input to the cost function and we find the total cost for the state and cost of each user.
Based on result, the user with max cost, we try to place that user with other users in such a way that the overall
cost might be reduced and a team of size n or 3 might be created.

Placing the removed user with each other team, we create a list of all possible states and pick the one which has the
least cost.

Once the user is placed in another team, we assign that configuration as the best one obtained till now and try to place
another user in the above achieved configuration in a way the total cost gets reduced.

We keep on trying to do the same thing till every user has been taken into consideration once. i.e May be assigned in
a particular team or might be kept alone.

Initial State: A team configuration where in each user belongs to exactly one team. So here the initial teams equal to
                the number of students who have given the survey

State Space: Possible team configurations from the current configurations

Goal State: Every user belongs to a team only once and is not present in more than one team along with the cost for the
            team to be as low as possible.

successor function: Each user removed based on the cost function, the possible arrangement of the user with respect to
                    other teams

Cost: For each configuration, we find the total grading time based on input k, m and n values based on the time for
      time size, desired members, undesired members for each user preference.
'''

import warnings
import sys
import copy

# This method loads the data from the file and creates a dictionary of keys which are usernames
# and list of survey answers given by each student where the 1st element is the team preference size followed by
# desired members followed by undesired member
# If the file is not found, then it throws and Exception and prints the appropriate message
def load_data(file):
    try:
        file = open(file,"r")
        dict = {}
        for line in file:
            data = line.split();
            dict[data[0]] = data[1:]
        return dict
    except IOError:
        print "File not found. Please provide valid file name"
        exit(0)


#This method creates a list of all the usernames from the dictionary of survey results
def create_username(dict):
    username_list = []
    for username in dict:
        username_list.append(username)
    return username_list

# This method creates an initial configuration of the teams where in each member is assigned in team of size 1 and total
# number of groups equal the number of student to start with.
def create_initial_teams(dict):
    username_list = []
    for username in dict:
        username_list.append([username])
    return username_list

# This method remove the element which has the maximum score i.e the maximum time from the input dictionary.
# The dictionary has keys as to time and values as list of usernames which take that much amount of time.
# This sorts the keys and removes the last element which is a username of the student
# Reference : https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
def remove_unhappy_user(dict):
    key_list = dict.keys()
    key_list.sort()
    time = key_list.pop()
    received_username_list = dict[time]
    for user in received_username_list:
         return user

# This method calculates the total time taken to grade the assignment based on the groups created and k m and n values
# The inputs are dictionary of survey answers, the groups configuration as List of List where each list is one team
# username list which has the usernames which have not be considered for grouping
def calculate_time(dict,teams,username,k,m,n):
    dict_of_time_to_student = {}
    total_time = 0
    team_size_count = 0
    time_for_wanted_students = 0
    time_for_unwanted_student = 0
    number_of_groups = len(teams)
    # the number of teams equal the number of groups, so multiplying ito k times
    time_wasted_for_checking = k*number_of_groups
    # looping in all the teams
    for team in teams:
        # number of students assigned in one team is team_size
        team_size = len(team)
        #looping on each student in the team to finds how much time one student takes
        for student in team:
            student_preference = int(dict[student][0])
            team_preference_count = 0
            # student preference doesn't match with its assigned team size, then add 1 to time
            if student_preference != 0 and student_preference != team_size:
                team_preference_count = 1
                team_size_count+=team_preference_count

            #Student' s desired team members
            student_wants_to_team_list = dict[student][1].split(",")

            # Reference: https://stackoverflow.com/questions/2864842/common-elements-comparison-between-2-lists
            # finding the number of students common in the student's preference vs student's assigned team
            common_list_for_needed = list(set(team).intersection(student_wants_to_team_list))
            length_of_desired_students = len(common_list_for_needed)

            # if the student gave no desired team size
            length_of_student_wanted_list = 0 if(student_wants_to_team_list[0] == '_') \
                else len(student_wants_to_team_list)
            # number of students did not be a part of the student's desired team
            number_of_students_did_not_get = length_of_student_wanted_list - length_of_desired_students
            time_wasted_desired_student = number_of_students_did_not_get*n
            time_for_wanted_students+=time_wasted_desired_student

            # Student's undesired team members
            student_does_not_want_in_team = dict[student][2].split(",")
            lengthOfStudentNotWantedList = 0 if (student_does_not_want_in_team[0] == '_') \
                else len(student_does_not_want_in_team)

            # finding the number of students common in the student's undesired list vs student's assigned team
            common_list_for_not_needed = list(set(team).intersection(student_does_not_want_in_team))
            # number of undesired students which became part of student's desired team
            number_of_student_not_wanted = len(common_list_for_not_needed)
            time_wasted_for_undesired_student = number_of_student_not_wanted*m
            time_for_unwanted_student+= time_wasted_for_undesired_student

            # Calculating time wasted for each user based on its preference, desired members and undesired members
            time_for_each_student = team_preference_count + time_wasted_desired_student + \
                                    time_wasted_for_undesired_student

            # creating a dictionary of key value pairs where key is the time taken by the students and values is the
            # list of users which take the same time
            for rem_student_list in username:
                student_name = rem_student_list
                if student_name == student:
                    dict_of_time_to_student.setdefault(time_for_each_student, [])
                    dict_of_time_to_student[time_for_each_student].append(student)

    total_time = time_wasted_for_checking + team_size_count + time_for_wanted_students + time_for_unwanted_student

    # returning a dictionary of time to student with the total cost
    return dict_of_time_to_student, total_time

# This method creates the configuration by placing the removed user with each other combinations except with itself and
# generates a list of different team configurations with respect to the removed user
# input to the function: name of the user to be placed
# input to the function: configuration
# for example : consider 4 students giving the survey : djcran , kapadia, fan6 and chen464
# input configuration was [djcran][kapadia,fan6][chen464] and user is chen464
# this method will create new configurations as
# first conf: [djcran, chen464][kapadia,fan6]
# second conf: [djcran][kapadia,fan6,chen464]
# and appends them to the final list
def form_team_combination(removed_user, list_of_teams):
    new_list = []
    copy_of_list_of_team = copy.deepcopy(list_of_teams)
    for list_number in range(len(copy_of_list_of_team)):
        temp = []
        if removed_user not in copy_of_list_of_team[list_number]:
            temp.append(copy.deepcopy(copy_of_list_of_team[list_number]))
            for j in range(len(copy_of_list_of_team)):
                if j != list_number and removed_user not in copy_of_list_of_team[j]:
                    temp.append(copy_of_list_of_team[j])
            if len(temp[0]) < 3:
                temp[0].append(removed_user)
            else:
                temp.append([removed_user])
            new_list.append(temp)

    return new_list

# this method removes the username from the available usernames based on the username which was assigned a team
# input: username - name of the student
#        input_team - the configuration
#        username_list - the list of usernames
def remove_element_from_list(username, input_team, username_list):
    copy_of_user_list = copy.deepcopy(username_list)
    for team in input_team:
        if username in team:
            for each_user in team:
                for user in username_list:
                    if user == each_user:
                        copy_of_user_list.remove(user)
    return copy_of_user_list

# prints the final selected configuration as one line per team followed by total time on the last time
def print_output(final_team_conf, time):
    return "\n".join([" ".join([user for user in team]) for team in final_team_conf]) +"\n"+ str(time)

# main function
if __name__=="__main__":
    warnings.filterwarnings('ignore')

    # if len of argument is not 5 then incorrect arguments provided
    if len(sys.argv) != 5:
        print "Incorrect argument provided"
    else:
        # reading the inputs from command-line
        fileName = sys.argv[1]
        res = load_data(fileName)
        k = int(sys.argv[2])
        m = int(sys.argv[3])
        n = int(sys.argv[4])
        # assigning intial cost as the maximum cost
        max_cost = sys.maxint
        # creating username list
        list_of_username = create_username(res)

        # creating initial team configuration where each username is in one team
        initial_team_configuration = create_initial_teams(res)

        #looping until the username list doesn't become 0
        while len(list_of_username) > 0:

            # returns the dictionary of time to student names, and total time for this configuration
            dict_of_cost_of_each_user, totalCost = calculate_time(res,initial_team_configuration,list_of_username,k,m,n)

            # this method removes the most unhappy user based on the map and tries to fit him in one team
            removed_user = remove_unhappy_user(dict_of_cost_of_each_user)

            # compares the newly generated cost with the previous best cost
            max_cost = min(max_cost,totalCost)

            # creates a possible states of different team configurations based on the removed user i.e the most unhappy
            new_formed_list = form_team_combination(removed_user, initial_team_configuration)

            # loops in all possible team configurations and selected the one with least cost
            selected_team = []
            for each_team_combination in new_formed_list:

                # calculate total cost and time to student dictionary
                dict_of_cost_of_each_user, totalCost = calculate_time(res, each_team_combination, list_of_username, k, m, n)

                # if total cost is less than previous best cost
                if totalCost < max_cost:
                    max_cost = totalCost
                    selected_team = each_team_combination
                    initial_team_configuration = selected_team

            # remove the user from the user list which was assigned a team
            list_of_username = remove_element_from_list(removed_user, selected_team, list_of_username)

        # final team configuration
        final_team_conf = initial_team_configuration

        # print the output
        print print_output(final_team_conf,max_cost)