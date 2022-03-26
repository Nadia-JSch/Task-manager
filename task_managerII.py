# =====importing libraries========
import copy       # for use in copying and editing nested lists
import datetime   # for use in calculating if a task is overdue

# ====Login Section====

credentials = []
with open("user.txt", 'r') as obj_users:
    Lines = obj_users.readlines()
    for line in Lines:
        # string formatting to remove the new line marker with split
        contents = line.strip()
        # get the formatted contents into a list
        contents = contents.split(", ")
        credentials.append(contents)

# a while loop to continue until a valid username and password are entered
login_success = False
while not login_success:
    # get input from user to compare to the text file data
    login_user = input("Please enter your username: ")
    login_pass = input("Please enter your password: ")

    for cred in credentials:
        # check if both the username and password match
        if login_user == cred[0] and login_pass == cred[1]:
            login_success = True
            print("\nWelcome to the Task Manager :)\n")
            break  # add a break to stop the for and while loops when match
    if not login_success:
        print("Please enter valid credentials.")


# =====Global Constants and Variables========
# defining the keys, and it's formatting, for a dictionary
TASKS_KEYS_LIST = ["Assigned to:\t\t",
                   "Task:\t\t\t\t",
                   "Task description:\t",
                   "Date assigned:\t\t",
                   "Due date:\t\t\t",
                   "Task complete?\t\t",
                   "Task number:\t\t"]

# creating a list of usernames for reg_user() to check if a new name is taken
usernames_list = [element[0] for element in credentials]

# ===== Defining Functions ========


# the admin user can select (enter "r") to add new users
def reg_user():

    # checking if the new username is in the usernames list
    is_unique = False
    while not is_unique:
        # - Request input of a new username
        new_user = input("Please enter a new username to register: ")

        if new_user in usernames_list:
            print(f"\"{new_user}\" is not available. "
                  f"Please enter a different username to register.")
        else:
            # append the new username to the usernames list to update it
            usernames_list.append(new_user)

            # if the username is unique continue to password entry
            is_unique = True
            print(credentials)

            # - Request input of a new password
            new_pass = input("Please enter a new password: ")
            # - Request input of password confirmation.
            confirm_pass = input("Please confirm the password: ")

            # - Check if the new password and confirmed password are the same.
            if new_pass == confirm_pass:
                # - If they are the same, add them to the user.txt file
                obj_users = open("user.txt", "a")
                # write the new login details to the file
                obj_users.write(f"{new_user}, {new_pass} \n")
                obj_users.close()  # close the file again
                # confirmation message after user is added
                print("\n----- A new user has been registered -----")
            else:
                print("Passwords did not match. Please try again")


# add_task() gets details about a new task and appends it to task.txt
def add_task():
    task_username = input("Please enter the username assigned to the task: ")
    task_title = input("Please enter the title of the task to be completed: ")
    task_describe = input("Please enter a short description of the task: ")

    # make sure the user doesn't enter the due date in a different format
    is_format = False
    while not is_format:
            task_due_date = input("Please enter the task's due date (e.g. 17 Aug 2022): ")
            try:
                datetime.datetime.strptime(task_due_date, "%d %b %Y")
                is_format = True
            except ValueError:
                print("The date format should be DD-mmm-YYYY (e.g. 17 Apr 2022)")

    # automatically add today's date
    task_enter_date = datetime.datetime.now().strftime("%d %b %Y")

    # assign new consecutive task number:
    # call the function returning tasks.txt as a list
    # adding one to the last item of the last entry
    task_number = int(read_tasks_as_list()[-1][6]) + 1

    # write input data to file
    # - include the 'No' to indicate the task isn't complete
    obj_tasks = open("tasks.txt", "a")
    obj_tasks.write(f"{task_username}, {task_title}, {task_describe}, "
                    f"{task_enter_date}, {task_due_date}, No, {task_number}\n")
    obj_tasks.close()
    print("\nYou have successfully recorded a new task!")


# view_all() calls read_tasks_as_list() and prints all task information
def view_all():
    # this function reads tasks.txt and makes a list of all its contents
    read_tasks_as_list()

    # create a task dictionary
    # uses the keys list and the returned contents list
    for i in read_tasks_as_list():
        # using zip() to make the new key: value pairs
        temp_tasks_dictionary = dict(zip(TASKS_KEYS_LIST, i))
        # displaying the value pairs to the console
        for key in temp_tasks_dictionary:
            print(f"{key} \t{temp_tasks_dictionary[key]}")
        print(
            f"\n-----------------------------------------------"
            f"-----------------------------------------\n")


def view_mine():
    # this function reads tasks.txt and makes a list of all its contents
    read_tasks_as_list()

    # check the list for tasks with the login user's name in it
    for task_line in read_tasks_as_list():
        if login_user == task_line[0]:
            # make it into a dictionary with the keys list
            temp_tasks_dictionary = dict(zip(TASKS_KEYS_LIST, task_line))
            # display the new dictionary with its keys which explain the values
            for key in temp_tasks_dictionary:
                print(f"{key} \t{temp_tasks_dictionary[key]}")
            print(f"---------------------------------------------------------\n")


# a function that opens tasks.txt and makes a list of all the contents
def read_tasks_as_list():
    full_task_list = []
    with open("tasks.txt", "r") as obj_tasks:
        # use a for loop to read each line of the text file
        for each_line in obj_tasks:
            strip_lines = each_line.strip()
            split_lines = strip_lines.split(", ")
            full_task_list.append(split_lines)
    return full_task_list


#  this function returns the total number of tasks
def task_total():
    # since tasks are numbered consecutively, the last task's number is the total
    total_tasks = int(read_tasks_as_list()[-1][6])
    return total_tasks


# function to count the number of tasks marked complete
def marked_complete_total():
    # counting the total number of completed tasks using indexing and a counter
    count_complete = 0
    for i in read_tasks_as_list():
        if i[5] == "Yes":
            count_complete += 1
    return count_complete

# create task_overview.txt, calculates stats and writes it to file
def task_overview():
    task_total()
    marked_complete_total()

    # compute the incomplete tasks by subtracting completed tasks from the total
    count_incomplete = task_total() - marked_complete_total()

    # finding the number of overdue tasks
    # initializing today's date and overdue counter
    now = datetime.datetime.now()
    overdue_count = 0

    # convert the str dates to .datetime type
    for a_line in read_tasks_as_list():
        due_date = datetime.datetime.strptime(a_line[4], "%d %b %Y")
        # compare each task's due date to today's one
        # count a task as overdue when it's marked "No" and due date has passed
        if now > due_date and a_line[5] == "No":
            overdue_count += 1

    # find the percentage of incomplete tasks
    percent_incomplete = round(count_incomplete / task_total() * 100)

    # find the percentage of overdue tasks
    percent_overdue = round(overdue_count / task_total() * 100)

    # write results to task_overview.txt.txt
    with open("task_overview.txt", "w") as obj_task_overview:
        obj_task_overview.write(f"Number of total tasks tracked: \t\t{task_total()}\n"
                                f"Number of completed tasks: \t\t\t{marked_complete_total()}\n"
                                f"Number of incomplete tasks: \t\t{count_incomplete}\n"
                                f"Number of overdue tasks: \t\t\t{overdue_count}\n"
                                f"Percentage of incomplete tasks: \t{percent_incomplete}%\n"
                                f"Percentage of overdue tasks: \t\t{percent_overdue}%\n")


# create task_overview.txt, calculate stats and write them to file
def user_overview():

    # creating a list of usernames from the credentials list
    cred_usernames = []
    for x in credentials:
        cred_usernames.append(x[0])

    # creating a list of usernames from the tasks.txt file
    tasks_usernames = []
    for i in read_tasks_as_list():
        tasks_usernames.append(i[0])

    # the number of registered users is = the number of usernames on the list
    total_users = len(cred_usernames)

    # the total tasks is taken from the last task's task number in tasks.txt
    task_total()

    # overwrite the user overview file with these general stats
    with open("user_overview.txt", "w") as obj_user_overview:
        obj_user_overview.write(f"Number of registered users: "
                                f"\t\t\t\t{total_users}\n"
                                f"Number of total tasks tracked: "
                                f"\t\t\t\t{task_total()}\n\n")

    # write with append to add the user's individual stats to the text file
    with open("user_overview.txt", "a") as obj_user_overview:
        # comparing users from user.txt to tasks.txt to compute stats
        # if a username appears on a task then count how many times
        for user in cred_usernames:
            if user in tasks_usernames:
                how_many_matches = tasks_usernames.count(user)
                # -------------------------------------------------------------------

                obj_user_overview.write(f"------------------ {user}'s Statistics ------------------\n")
                obj_user_overview.write(f"\nTotal assigned tasks: "
                                        f"\t\t\t\t\t\t{how_many_matches}\n")
                obj_user_overview.write(f"Percentage of total tasks assigned: "
                                        f"\t\t{round(how_many_matches / task_total() * 100)}%\n")

                # count the number of completed tasks for each user in the list
                count_complete_user = 0
                for i in read_tasks_as_list():
                    if i[5] == "Yes" and i[0] == user:
                        count_complete_user += 1

                obj_user_overview.write(f"Percentage of completed assigned tasks: "
                                        f"\t{round(count_complete_user / how_many_matches * 100)}"
                                        f"%\n")
                obj_user_overview.write(f"Percentage of incomplete assigned tasks: "
                                        f"\t{round((how_many_matches - count_complete_user) / how_many_matches * 100)}"
                                        f"%\n")

                # finding the number of overdue tasks
                # - initializing today's date and overdue counter
                now = datetime.datetime.now()
                overdue_count = 0
                # convert the str dates to .datetime type
                for a_line in read_tasks_as_list():
                    due_date = datetime.datetime.strptime(a_line[4], "%d %b %Y")
                    # compare each task's due date to today's one
                    # count a task as overdue when it's marked "No" and overdue
                    if now > due_date and a_line[5] == "No" and a_line[0] == user:
                        overdue_count += 1

                obj_user_overview.write(f"Percentage of overdue assigned tasks: "
                                        f"\t\t{round(overdue_count / how_many_matches * 100)}%"
                                        f"\n\n")

            # if there are no matches then the user has no assigned tasks
            else:
                obj_user_overview.write(f"------------------ {user}'s Statistics ------------------\n")
                obj_user_overview.write(f"0 assigned tasks\n\n")

# ==== Main Menu Loop ====
while True:
    # users that are not admin will view the standard menu options
    if login_user != "admin":
        # present the menu to the user converting the input to lower case.
        menu = input('''\nPlease select one of the following Options below: \n
r  - \tRegistering a user (permission only)
a  - \tAdding a task
va - \tView all tasks
vm - \tView my tasks
e  - \tExit
 : ''').lower()

    # user "admin" will see the stats option in their menu
    else:
        menu = input('''\nSelect one of the following Options below: \n
r  - \tRegistering a user (permission only)
a  - \tAdding a task
va - \tView all tasks
vm - \tView my tasks
gr - \tGenerate reports
vs - \tView statistics
e  - \tExit
: ''').lower()

    if menu == 'r':
        # only allow the user "admin" to register users
        if login_user == "admin":
            # call the reg_user function
            reg_user()
        else:
            print("You do not have register user permission.")
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        # call view_all function
        view_all()

    elif menu == 'vm':
        # call view_mine function
        view_mine()
        edit_task_num = input("Enter a task number to edit it, "
                              "or 'mm' to return to the main menu: ")
        print(edit_task_num)

        # test: deepcopy list so changes stick?
        deepcopy_full_tasks = copy.deepcopy(read_tasks_as_list())
        for task_line in deepcopy_full_tasks:
            if edit_task_num == task_line[6]:
                temp_tasks_dictionary = dict(zip(TASKS_KEYS_LIST, task_line))

                # display the new dictionary with its keys explaining the values
                for key in temp_tasks_dictionary:
                    print(f"{key} \t{temp_tasks_dictionary[key]}")
                print(f"---------------------------------------------------------\n")

                # check if task is marked as "No" so it can be edited
                if temp_tasks_dictionary["Task complete?\t\t"] == "No":
                    vm_options = ""
                    while vm_options != "sr":
                        vm_options = input(f"\nPlease select one of the following Options below:\n"
                                           f"\nm   - \tMark task as complete\n"
                                           f"u   - \tEdit task's username\n"
                                           f"dd  - \tEdit task's due date\n"
                                           f"sr  - \tSave and Return to Main Menu\n"
                                           f": ").lower()

                        # mark task as complete'
                        if vm_options == "m":
                            confirm = input(f"Mark as task {edit_task_num} as complete? "
                                            f"Enter 'yes' to confirm: ").lower()
                            if confirm == "yes":
                                temp_tasks_dictionary["Task complete?\t\t"] = "Yes"
                            else:
                                print(f"Task {edit_task_num} not marked as complete")

                        # edit task's username
                        elif vm_options == "u":
                            print("----Editing username----")
                            edit_username = input("Please enter the new username for the task: ")
                            temp_tasks_dictionary["Assigned to:\t\t"] = edit_username

                        # edit task's due date
                        elif vm_options == "dd":
                            print("----Editing due date----")
                            edit_date = input("Please enter the new due date (e.g. 27 Apr 2022): ")
                            temp_tasks_dictionary["Due date:\t\t\t"] = edit_date

                        # save changes and return to main menu
                        elif vm_options == "sr":
                            print("----Saving & Returning to Main Menu----")
                            # remove dictionary keys to get values
                            values = temp_tasks_dictionary.values()
                            # remove the "dict_values(" from the front of the line
                            # and ")" from the back
                            new_task_values = list(values)

                            # get index of original line
                            get_index = deepcopy_full_tasks.index(task_line)

                            # replace original line with edited line
                            deepcopy_full_tasks[get_index] = new_task_values

                            # formatting:
                            # convert tasks into str
                            tasks_str = ""
                            for item in deepcopy_full_tasks:
                                tasks_str += ", ".join(item) + "\n"
                            # formatting:
                            # remove the new line at then end of the last line
                            tasks_str = tasks_str.strip("\n")

                            # write the task content back to the file
                            obj_tasks = open("tasks.txt", "w")
                            obj_tasks.write(tasks_str)
                            obj_tasks.close()
                            break
                        else:
                            print("Please enter a valid menu option.")
                else:
                    print("You can only edit tasks that have not been completed yet.")

    # this option requires entering the option "gr" and logging in as "admin"
    elif menu == "gr" and login_user == "admin":
        task_overview()
        user_overview()
        print("------Task and user stats have been generated and saved to file------")

    # this option requires entering "st" and having a login username of "admin"
    elif menu == 'vs' and login_user == "admin":
        # call the task_overview.txt function to generate text files and stats
        task_overview()
        print(f"-------------------- Task Statistics --------------------\n")

        # read from task_overview.txt.txt and display its contents
        with open("task_overview.txt", "r") as obj_tasks_overview:
            for stat in obj_tasks_overview:
                print(stat.strip("\n"))
            print("")

        # call the user_overview.txt function to generate text files and stats
        user_overview()

        print(f"-------------------- User Statistics --------------------\n")

        # read from user_overview.txt.txt and display its contents
        with open("user_overview.txt", "r") as obj_user_overview:
            for stat in obj_user_overview:
                print(stat.strip("\n"))
        print(f"---------------------------------------------------------\n")

    elif menu == 'e':
        print("Thank you for using the task manager :) ")
        exit()

    else:
        print("You have made a wrong choice. Please try again")

# ---END---
