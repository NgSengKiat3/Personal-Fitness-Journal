import pandas as pd
from datetime import datetime

data_file = "fitness_journal.csv"

# Initialize a DataFrame for activities
try:
    activities = pd.read_csv(data_file)
except FileNotFoundError:
    print(f"{data_file} not found. Starting with an empty journal.")
    activities = pd.DataFrame(columns=["Activity", "Type", "Duration", "Distance", "Calorie", "Date", "Notes"])

# Utility function for input validation
def getInput(prompt: str, error_message: str, converter=None, validator=None):
    while True:
        try:
            value = input(prompt).strip()
            if converter is not None:
                value = converter(value)
            if validator is not None and not validator(value):
                raise ValueError
            return value
        except ValueError:
            print("Invalid input: " + error_message)

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

        choice = getInput(
            "Enter your choice (1-6): ",
            "Please enter a number between 1 and 6.",
            int,
            lambda x: x in range(1, 7),
        )

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
            save_data()
            print("Data has been saved. Exiting the program. Goodbye!")
            break

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
    
    activity_choice = getInput(
        "Enter your choice (1-4): ",
        "Please enter 1, 2, 3, or 4.",
        int,
        lambda x: x in range(1, 5)
    )
    
    if activity_choice == 1:
        activity = "Running".lower()
    elif activity_choice == 2:
        activity = "Yoga".lower()
    elif activity_choice == 3:
        activity = "Cycling".lower()
    elif activity_choice == 4:
        activity = getInput("Enter the name of the new activity: ", "Activity name cannot be empty.")

    # Option for type of activity
    print("Choose the type of activity:")
    print("1. Cardio")
    print("2. Flexibility")
    print("3. Enter a new type")
    
    type_choice = getInput(
        "Enter your choice (1-3): ",
        "Please enter 1, 2, or 3.",
        int,
        lambda x: x in range(1, 4)
    )
    
    if type_choice == 1:
        activity_type = "Cardio".lower()
    elif type_choice == 2:
        activity_type = "Flexibility".lower()
    elif type_choice == 3:
        activity_type = getInput("Enter the new type of activity: ", "Activity type cannot be empty.")

    # Other details for the activity
    duration = getInput(
        "Enter the duration of the activity (in minutes): ",
        "Please enter a positive integer.",
        int,
        lambda x: x > 0
    )
    distance = getInput(
        "Enter the distance (in km, enter 0 if not applicable): ",
        "Please enter a non-negative number.",
        float,
        lambda x: x >= 0
    )
    calorie = getInput(
        "Enter the calories burned during the activity: ",
        "Please enter a non-negative number.",
        float,
        lambda x: x >= 0
    )
    
    # Checking whether the date input is valid
    date = getInput(
        "Enter the date (YYYY-MM-DD): ",
        "Please enter a valid date in YYYY-MM-DD format.",
        lambda x: datetime.strptime(x, "%Y-%m-%d").date()
    )

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

    # Add to the activities DataFrame
    activities = pd.concat([activities, pd.DataFrame([new_entry])], ignore_index=True)
    print("New activity added!")

# Edit an activity
def edit():
    global activities
    if activities.empty:
        print("No activities found to edit.")
        return

    print("Available activities:")
    print(activities[["Activity", "Date"]].reset_index())

    index = getInput(
        "Enter the index of the activity you want to edit: ",
        "Please enter a valid index.",
        int,
        lambda x: x in activities.index
    )

    activity = activities.loc[index]

    new_activity = input(f"Enter the new activity name (or press Enter to keep '{activity['Activity']}'): ").strip()
    new_type = input(f"Enter the new type (or press Enter to keep '{activity['Type']}'): ").strip()
    new_duration = input(f"Enter the new duration (or press Enter to keep '{activity['Duration']}'): ").strip()
    new_distance = input(f"Enter the new distance (or press Enter to keep '{activity['Distance']}'): ").strip()
    new_calorie = input(f"Enter the new calorie count (or press Enter to keep '{activity['Calorie']}'): ").strip()
    new_date = input(f"Enter the new date (or press Enter to keep '{activity['Date']}'): ").strip()
    new_notes = input(f"Enter the new notes (or press Enter to keep '{activity['Notes']}'): ").strip()

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

# Delete an activity
def delete():
    global activities
    if activities.empty:
        print("No activities found to delete.")
        return

    print("Available activities:")
    print(activities[["Activity", "Date"]].reset_index())

    index = getInput(
        "Enter the index of the activity you want to delete: ",
        "Please enter a valid index.",
        int,
        lambda x: x in activities.index
    )

    activities.drop(index, inplace=True)
    activities.reset_index(drop=True, inplace=True)
    print("Activity deleted successfully!")

# View details of all activities
def details():
    if activities.empty:
        print("No activities found.")
        return

    print("\nActivity Details:")
    print("-" * 40)
    print(activities[["Activity", "Date"]].reset_index(drop=False).rename(columns={"index": "ID"}))

# Search for activities
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

        if results.empty:
            print("No matching activities found.")
        else:
            print("\nSearch Results:")
            print(results)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the program
if __name__ == "__main__":
    main()
