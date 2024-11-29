import pandas as pd
from datetime import datetime

data_file = "fitness_journal.csv"

# Initialize a DataFrame for activities
try:
    activities = pd.read_csv(data_file)
except FileNotFoundError:
    print(f"{data_file} not found. Starting with an empty journal.")
    activities = pd.DataFrame(columns=["Activity", "Type", "Duration", "Distance", "Calorie", "Date", "Notes"])


# Main function
def main():
    while True:
        print("\nPersonal Fitness Journal")
        print("1. Add Activity")
        print("2. Edit Activity")
        print("3. Delete Activity")
        print("4. View Details")
        print("5. Search Activities")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add()
        elif choice == '2':
            edit()
        elif choice == '3':
            delete()
        elif choice == '4':
            details()
        elif choice == '5':
            search()
        elif choice == '6':
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
            print("Invalid choice. Please enter a number between 1 and 7.")
            
            
# Save data to the CSV file
def save_data():
    global activities
    activities.to_csv(data_file, index=False)
    print("Data saved successfully!")

def add():
    global activities
    
    # Prompt user to enter activity
    print("Choose the activity:")
    print("1. Running")
    print("2. Yoga")
    print("3. Cycling")
    print("4. Enter a new activity")
    answer = input("Enter your choice (1, 2, 3, or 4): ").strip()

    #Option for activity name
    if answer == '1':
        activity = "Running".lower()
    elif answer == '2':
        activity = "Yoga".lower()
    elif answer == '3':
        activity = "Cycling".lower()
    elif answer == '4':
        activity = input("Enter the name of the new activity: ").strip().lower()
    else:
        answer = input("Enter your choice (1, 2, 3, or 4): ").strip()
        return

    #Option for type of activity
    print("Choose the type of activity:")
    print("1. Cardio")
    print("2. Flexibility")
    print("3. Enter a new type")
    answer_type = input("Enter your choice (1, 2, or 3): ").strip()

    if answer_type == '1':
        activity_type = "Cardio".lower()
    elif answer_type == '2':
        activity_type = "Flexibility".lower()
    elif answer_type == '3':
        activity_type = input("Enter the new type of activity: ").strip().lower()
    else:
        activity_type = input("Enter the new type of activity: ").strip().lower()
        return

    #Other details for the activity
    try:
        duration = int(input("Enter the duration of the activity (in minutes): "))
        distance = float(input("Enter the distance (in km, enter 0 if not applicable): "))
        calorie = float(input("Enter the calories burned during the activity: "))
        #Checking whether the date input is valid
        while True:
            try:
                date_input = input("Enter the date (YYYY-MM-DD): ").strip()
                date = datetime.strptime(date_input, "%Y-%m-%d").date()
                break  # Exit the loop if the date is valid
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                date_input = input("Enter the date (YYYY-MM-DD): ").strip()
        
        notes = input("Enter any additional notes: ")

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

        # Add to the activities DataFrame
        global activities
        activities = pd.concat([activities, pd.DataFrame([new_entry])], ignore_index=True)
        print("New activity added!")
        save_data()
    except ValueError:
        print("Invalid input. Please try again.")


# Edit an activity
def edit():
    if activities.empty:
        print("No activities found to edit.")
        return

    print("Available activities:")
    print(activities)

    try:
        index = int(input("Enter the index of the activity you want to edit: "))
        if index in activities.index:
            activity = activities.loc[index]

            new_activity = input(f"Enter the new activity name (or press Enter to keep '{activity['Activity']}'): ")
            new_type = input(f"Enter the new type (or press Enter to keep '{activity['Type']}'): ")
            new_duration = input(f"Enter the new duration (or press Enter to keep '{activity['Duration']}'): ")
            new_distance = input(f"Enter the new distance (or press Enter to keep '{activity['Distance']}'): ")
            new_calorie = input(f"Enter the new calorie count (or press Enter to keep '{activity['Calorie']}'): ")
            new_date = input(f"Enter the new date (or press Enter to keep '{activity['Date']}'): ")
            new_notes = input(f"Enter the new notes (or press Enter to keep '{activity['Notes']}'): ")

            # Update fields if new values are provided
            if new_activity:
                activities.loc[index, "Activity"] = new_activity
            if new_type:
                activities.loc[index, "Type"] = new_type
            if new_duration:
                activities.loc[index, "Duration"] = int(new_duration)
            if new_distance:
                activities.loc[index, "Distance"] = float(new_distance)
            if new_calorie:
                activities.loc[index, "Calorie"] = float(new_calorie)
            if new_date:
                activities.loc[index, "Date"] = new_date
            if new_notes:
                activities.loc[index, "Notes"] = new_notes

            print("Activity updated successfully!")
            save_data()
        else:
            print("Invalid index.")
            
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Delete an activity
def delete():
    if activities.empty:
        print("No activities found to delete.")
        return

    print("Available activities:")
    print(activities[["Activity", "Date"]].reset_index())

    try:
        index = int(input("Enter the index of the activity you want to delete: "))
        if index in activities.index:
            activities.drop(index, inplace=True)
            activities.reset_index(drop=True, inplace=True)
            print("Activity deleted successfully!")
            save_data()
        else:
            print("Invalid index.")
           
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# View details of all activities
def details():
    if activities.empty:
        print("No activities found.")
        return

    print("\nActivity Details:")
    print("-" * 40)
    
    # Reset index and display with index starting from 1
    details_df = activities.reset_index(drop=True)
    details_df.index += 1  # Adjust index to start from 1

    print(details_df[["Activity", "Date"]])
    
    
# Search for activities
def search():
    
    try:
        # Raise an error if the DataFrame is empty
        if activities.empty:
            raise ValueError("No activities found to search.")
        
        query = input("Enter a keyword to search (e.g., activity name, type, or date): ").strip().lower()
        
        # Raise an error if the search query is empty
        if not query:
            raise ValueError("Search query cannot be empty.")
        
        # Perform a case-insensitive search across all rows and columns
        results = activities[
            activities.apply(lambda row: query in str(row.values).lower(), axis=1)
        ]
        
        if results.empty:
            print("No matching activities found.")
        else:
            print("\nSearch Results:")
            print(results[["Activity", "Type", "Date"]])  # Display selected columns
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Run the program
if __name__ == "__main__":
    main()
