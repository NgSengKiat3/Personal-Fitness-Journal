import pandas as pd
from datetime import datetime

#File location
data_file = "fitness_journal.csv"

#Initialize a DataFrame for data storage
try:
    activities = pd.read_csv(data_file)
except FileNotFoundError:
    print(f"{data_file} not found. Starting with an empty journal.")
    activities = pd.DataFrame(columns=["Activity", "Type", "Duration", "Distance", "Calorie", "Date", "Notes"])

# Function for input validation
def getInput(prompt, error_message, parser, validator=None):
    while True:
        #Always get string
        user_input = input(prompt).strip()  
        if user_input == "":
            #Keep empty input
            return None  
        try:
            #Parse the input to desired type
            value = parser(user_input)  
            #Validate if a validator is provided
            if validator is None or validator(value):
                return value
            else:
                print(error_message)
        except (ValueError, TypeError):
            print(error_message)

#Main function
def main():
    while True:
        print("\nPersonal Fitness Journal")
        print("-" * 40)
        print("1. Add Activity")
        print("2. Edit Activity")
        print("3. Delete Activity")
        print("4. View Details")
        print("5. Search Activities")
        print("6. Summary")
        print("7. Exit")

        #Get user's input
        choice = getInput(
            "Enter your choice (1-7): ",
            "Please enter a number between 1 and 7.",
            int,
            lambda x: x in range(1, 8),
        )
        
        #Call the chosen function
        if choice == 1:
            add()
        elif choice == 2:
            edit()
        elif choice == 3:
            delete()
        elif choice == 4:
            details()
        elif choice == 5:
            search()
        elif choice == 6:
            display_summary()
        elif choice == 7:
           save_data()
           print("Data has been saved. Would you like to exit or return to the main menu?")
           exit_choice = input("Type 'exit' to quit or 'menu' to return to the main menu: ").strip().lower()
           if exit_choice == 'exit':
             print("Exiting the program. Goodbye!")
             break
           elif exit_choice == 'menu':
             print("Returning to the main menu.")
           else:
             print("Invalid choice. Returning to the main menu.")
        else:
            print("Invalid choice. Please enter a number between 1 to 7.")

#Save data to the CSV file
def save_data():
    global activities
    activities.to_csv(data_file, index=False)

def add():
    global activities
    
    # Prompt user to enter activity
    print("Choose the activity:")
    print("-" * 40)
    print("1. Running")
    print("2. Yoga")
    print("3. Cycling")
    print("4. Enter a new activity")
    
    activity_choice = None
    while activity_choice is None:
        try:
            activity_choice = int(input("Enter your choice (1-4): ").strip())
            if activity_choice not in range(1, 5):
                print("Please enter a valid choice (1-4).")
                activity_choice = None
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")

    # Set activity name (either by choice given or type a new one)
    if activity_choice == 1:
        activity = "Running".lower()
    elif activity_choice == 2:
        activity = "Yoga".lower()
    elif activity_choice == 3:
        activity = "Cycling".lower()
    elif activity_choice == 4:
        activity = ""
        while not activity.strip():
            activity = input("Enter the name of the new activity: ").strip()
            if not activity:
                print("Activity name cannot be empty. Please try again.")

    # Set type of activity
    print("Choose the type of activity:")
    print("-" * 40)
    print("1. Cardio")
    print("2. Flexibility")
    print("3. Enter a new type")
    
    type_choice = None
    while type_choice is None:
        try:
            type_choice = int(input("Enter your choice (1-3): ").strip())
            if type_choice not in range(1, 4):
                print("Please enter a valid choice (1-3).")
                type_choice = None
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")

    if type_choice == 1:
        activity_type = "Cardio".lower()
    elif type_choice == 2:
        activity_type = "Flexibility".lower()
    elif type_choice == 3:
        activity_type = ""
        while not activity_type.strip():
            activity_type = input("Enter the new type of activity: ").strip()
            if not activity_type:
                print("Activity type cannot be empty. Please try again.")

    # Set activity details
    duration = None
    while duration is None:
        raw_input = input("Enter the duration of the activity (in minutes): ").strip()
        # Handle "Enter" (blank input)
        if raw_input == "":  
            print("Duration cannot be empty. Please enter a positive value.")
            continue
        try:
            #Convert input to integer
            duration = int(raw_input)  
            if duration <= 0:
                print("Please enter a positive integer.")
                # Reset to re-prompt
                duration = None  
        except ValueError:
            print("Please enter a valid number.")
    
    distance = getInput(
        "Enter the distance (in km, enter 0 if not applicable): ",
        "Please enter a non-negative number.",
        float,
        lambda x: x >= 0
    )
    
    calorie = None
    while calorie is None:
        try:
            calorie = float(input("Enter the calories burned during the activity: ").strip())
            if calorie < 0:
                print("Calories burned cannot be negative.")
                calorie = None
        except ValueError:
            print("Invalid input. Please enter a non-negative number.")
    
    
    # Checking whether date input is valid
    date = None
    while date is None:
        date_input = input("Enter the date (DD/MM/YYYY): ").strip()
        if not date_input:
            print("Date cannot be empty. Please try again.")
            continue
        try:
            date = datetime.strptime(date_input, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            print("Invalid date format. Please enter the date in DD/MM/YYYY format.")

    notes = input("Enter any additional notes: ").strip()

    # Create a new entry
    new_entry = {
        "Activity": activity,
        "Type": activity_type,
        "Duration": duration,
        "Distance": distance,
        "Calorie": calorie,
        "Date": date,
        "Notes": notes
    }

    # Add the new data to DataFrame and save
    activities = pd.concat([activities, pd.DataFrame([new_entry])], ignore_index=True)
    save_data()
    print("New activity added!")

#Function to edit data to journal
def edit():
    global activities
    if activities.empty:
        print("No activities found to edit.")
        return

    #Reset index for display purposes and show current records
    details_df = activities.reset_index(drop=True)
    # Start index from 1
    details_df.index += 1  
    print("Record of activities:")
    print("-" * 40)
    print(details_df)

    #Get the index of the activity to edit (adjust to zero-based index for DataFrame access)
    index = getInput(
        "Enter the index of the activity you want to edit: ",
        "Please enter a valid index.",
        int,
        lambda x: 1 <= x <= len(details_df)
    ) - 1

    #Access the current row
    current_row = activities.iloc[index]

    #Prompt for new values (keep existing if no input is given)
    new_activity = input(f"Rename this activity name (or press Enter to keep '{current_row['Activity']}'): ").strip()
    new_type = input(f"Rename this activity type (or press Enter to keep '{current_row['Type']}'): ").strip()
    new_duration = getInput(
        f"Enter the new duration (or press Enter to keep '{current_row['Duration']}'): ",
        "Please enter a positive integer.",
        lambda x: int(x) if x.strip() else current_row['Duration'],
        lambda x: x > 0
    )

    new_distance = getInput(
        f"Enter the new distance (or press Enter to keep '{current_row['Distance']}'): ",
        "Please enter a positive number.",
        lambda x: float(x) if x.strip() else current_row['Distance'],
        lambda x: x >= 0
    )

    new_calorie = getInput(
        f"Enter the new calorie count (or press Enter to keep '{current_row['Calorie']}'): ",
        "Please enter a positve number.",
        lambda x: float(x) if x.strip() else current_row['Calorie'],
        lambda x: x >= 0
    )
    new_date = getInput(
        f"Enter the new date (DD/MM/YYYY) (or press Enter to keep '{current_row['Date']}'): ",
        "Please enter a valid date in DD/MM/YYYY format.",
        lambda x: datetime.strptime(x, "%d/%m/%Y").date() if x else current_row['Date'],
        lambda x: x or x == "" 
    )

    if new_date == None:
        new_date = current_row['Date']
    else:
        new_date = new_date.strftime("%d/%m/%Y")
        
    new_notes = input(f"Enter new additional notes (or press Enter to keep '{current_row['Notes']}'): ").strip()

    #Update the row directly in the DataFrame
    if new_activity:
        activities.at[index, 'Activity'] = new_activity
    if new_type:
        activities.at[index, 'Type'] = new_type
    if new_duration:
        activities.at[index, 'Duration'] = float(new_duration)
    if new_distance:
        activities.at[index, 'Distance'] = float(new_distance)
    if new_calorie:
        activities.at[index, 'Calorie'] = float(new_calorie)
    if new_date:
        try:
            #Validate and reformat the date
            formatted_date = datetime.strptime(new_date, "%d/%m/%Y").strftime("%d/%m/%Y")
            activities.at[index, 'Date'] = formatted_date
        except ValueError:
            print("Invalid date format. Keeping the existing date.")
    if new_notes:
        activities.at[index, 'Notes'] = new_notes

    #Save changes to file
    save_data()
    print("Activity updated successfully!")


#Function to delete data from journal
def delete():
    global activities
    if activities.empty:
        print("No activities found to delete.")
        return
    
    #Display available activities
    details_df = activities.reset_index(drop=True)
    details_df.index += 1
    print("Available activities:")
    print("-" * 40)
    print(details_df)

    index = getInput(
        "Enter the index of the activity you want to delete: ",
        "Please enter a valid index.",
        int,
        lambda x: 1 <= x <= len(details_df)
    )

    actual_index = index - 1
    
    activities.drop(activities.index[actual_index], inplace=True)
    activities.reset_index(drop=True, inplace=True)
    save_data()
    print("Activity deleted successfully!")

#Function to view activity details in journal
def details():
    #Check if DataFrame is empty
    if activities.empty:
        #Output if no activities
        print("No activities found.")
        return

    print("\nRecord of activities:")
    print("-" * 40)

    details_df = activities.reset_index(drop=True)
    details_df.index += 1  

    #Display details
    print(details_df)

#Function to search desired data in journal
def search():
    global activities
    
    try:
        if activities.empty:
            raise ValueError("No activities found to search.")
        
        query = getInput(
            "Enter a keyword to search (e.g., activity name, type, or date): ",
            "Search query cannot be empty.",
            lambda x: x.strip().lower(),
            lambda x: len(x) > 0
        )
        
        results = activities[
            activities.apply(lambda row: query in str(row.values).lower(), axis=1)
        ]

        #Display if no results
        if results.empty:
            print("No matching activities found.")
        else:
            #Display if data found
            print("\nSearch Results:")
            print("-" * 40)
            results_df = results.reset_index(drop=True)
            results_df.index += 1
            #Output filtered results
            print(results_df)
    #Occur for ValueError
    except ValueError as e:
        print(f"Error: {e}")
    #Occur for unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#Function to display summary between chosen periods
def display_summary():
    if activities.empty:
        print("No activities found to summarize.")
        return

    #Prompt the user for the date range
    start_date = getInput(
        "Enter the start date (DD/MM/YYYY): ",
        "Invalid date format. Please enter in DD/MM/YYYY format.",
        lambda x: datetime.strptime(x.strip(), "%d/%m/%Y"),
    )

    end_date = getInput(
        "Enter the end date (DD/MM/YYYY): ",
        "Invalid date format. Please enter in DD/MM/YYYY format.",
        lambda x: datetime.strptime(x.strip(), "%d/%m/%Y"),
    )

    #Filter activities within the date range
    def within_date_range(row):
        activity_date = datetime.strptime(row, "%d/%m/%Y")
        return start_date <= activity_date <= end_date

    filtered_activities = activities[activities['Date'].apply(within_date_range)]

    if filtered_activities.empty:
        print("No activities found in the specified date range.")
        return

    #Calculate total distance, total calories burned, and average duration
    total_distance = filtered_activities['Distance'].sum()
    total_calories = filtered_activities['Calorie'].sum()
    avg_duration = filtered_activities['Duration'].mean()

    #Display the summary
    print("\nSummary of Fitness Data:")
    print("-" * 40)
    print(f"Total Distance Covered: {total_distance:.2f} km")
    print(f"Total Calories Burned: {total_calories:.2f}")
    print(f"Average Workout Duration: {avg_duration:.2f} minutes")
    print("-" * 40)

#Run the program
if __name__ == "__main__":
    main()
