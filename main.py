import subprocess
import time

# Function to format the elapsed time
def format_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Function to print the current time with a message
def print_with_time(message):
    elapsed_time = format_elapsed_time(start_time)
    print(f"[{elapsed_time}] {message}")

# Start time
start_time = time.time()

def get_bluestacks_device_id():
    """
    Get the device ID for BlueStacks.
    """
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    
    for line in lines:
        if 'localhost:5555' in line and 'device' in line:
            return 'localhost:5555'
    
    return None

def connect_adb():
    """
    Connect ADB to BlueStacks.
    """
    try:
        # Check if already connected
        result = subprocess.run(['adb', 'connect', 'localhost:5555'], capture_output=True, text=True)
        if "already connected" in result.stdout:
            print_with_time("Already connected to localhost:5555")
        else:
            print_with_time("ADB connected to BlueStacks.")
    except Exception as e:
        print_with_time(f"Error connecting ADB to BlueStacks: {e}")

def adb_tap(device_id, x, y):
    """
    Send a tap event to the specified coordinates using ADB.
    """
    adb_command = f'adb -s {device_id} shell input tap {x} {y}'
    try:
        subprocess.run(adb_command, shell=True, check=True)
        print(" " * 11 + f"Tapped at ({x}, {y}) via ADB")
    except Exception as e:
        print(" " * 11 + f"Error tapping at ({x}, {y}) via ADB: {e}")

def adb_swipe(device_id, x1, y1, x2, y2, duration=6000):
    """
    Send a swipe event from (x1, y1) to (x2, y2) using ADB.
    """
    adb_command = f'adb -s {device_id} shell input swipe {x1} {y1} {x2} {y2} {duration}'
    try:
        subprocess.run(adb_command, shell=True, check=True)
        print_with_time(f"Swiped from ({x1}, {y1}) to ({x2}, {y2}) via ADB")
        time.sleep(1)  # Adding a delay to ensure the game processes the swipe
    except Exception as e:
        print_with_time(f"Error swiping from ({x1}, {y1}) to ({x2}, {y2}) via ADB: {e}")


def click_close_button(device_id):
    """
    Click the Close button at the specified location using ADB.
    """
    # Coordinates of the "Close" button
    button_x = 906
    button_y = 868
    
    print_with_time(f"Clicking at ({button_x}, {button_y}) using ADB on device {device_id}")
    adb_tap(device_id, button_x, button_y)

def choose_server(device_id):
    """
    Perform actions to choose the server and start the game.
    """
    # Coordinates for the "Choose Server" button
    choose_server_x = 1000
    choose_server_y = 800
    
    print_with_time(f"Clicking Choose Server button at ({choose_server_x}, {choose_server_y})")
    adb_tap(device_id, choose_server_x, choose_server_y)
    time.sleep(2)  # Wait for the server list to appear
    
    # Coordinates to scroll and find the server
    swipe_start_x = 1000
    swipe_start_y = 800
    swipe_end_x = 1000
    swipe_end_y = 300

    num_swipes = 6  # Number of times to swipe
    
    for i in range(num_swipes):
        print_with_time(f"Scrolling to find the server (Swipe {i+1}/{num_swipes}) from ({swipe_start_x}, {swipe_start_y}) to ({swipe_end_x}, {swipe_end_y})")
        adb_swipe(device_id, swipe_start_x, swipe_start_y, swipe_end_x, swipe_end_y)
        time.sleep(1)  # Wait for the scroll to complete
    
    # Coordinates of the target server
    target_server_x = 985
    target_server_y = 487
    
    print_with_time(f"Clicking target server at ({target_server_x}, {target_server_y})")
    adb_tap(device_id, target_server_x, target_server_y)
    time.sleep(2)  # Wait for the server to be selected
    
    # Coordinates of the "Play" button
    play_button_x = 1000
    play_button_y = 970
    
    print_with_time(f"Clicking Play button at ({play_button_x}, {play_button_y})")
    adb_tap(device_id, play_button_x, play_button_y)

def close_announcements_and_events(device_id):
    """
    Close the Announcements and Event Ranking screens by clicking the X buttons.
    """
    # Coordinates of the "X" button for Announcements
    announcements_x = 1520
    announcements_y = 167
    
    print_with_time(f"Clicking Announcements X button at ({announcements_x}, {announcements_y})")
    adb_tap(device_id, announcements_x, announcements_y)
    time.sleep(1)  # Wait for the screen to close

    # Coordinates of the "X" button for Event Ranking
    events_x = 1480
    events_y = 85
    
    print_with_time(f"Clicking Event Ranking X button at ({events_x}, {events_y})")
    adb_tap(device_id, events_x, events_y)
    time.sleep(1)  # Wait for the screen to close

def collect_money_from_buildings(device_id):
    """
    Collect money from all buildings by tapping on them and swiping to view the next set of buildings.
    """
    # Coordinates of the 3 buildings on the first screen
    buildings = [
        (300, 600),  # Building 1
        (885, 660),  # Building 2
        (1490, 600)  # Building 3
    ]
    
    # Swipe coordinates to move to the next set of buildings
    swipe_start_x = 1900
    swipe_start_y = 540  # Middle of the screen vertically
    swipe_end_x = 50
    swipe_end_y = 540  # Middle of the screen vertically

    num_swipes = 3  # Number of swipes needed to view all 12 buildings

    for i in range(num_swipes + 1):  # Including the initial screen
        print_with_time(f"Collecting money from buildings on screen {i+1}")
        for building in buildings:
            adb_tap(device_id, building[0], building[1])
            time.sleep(0.5)  # Short delay between taps
        
        if i < num_swipes:  # Perform swipe if there are more buildings to collect from
            print_with_time(f"Swiping to next set of buildings (Swipe {i+1}/{num_swipes})")
            adb_swipe(device_id, swipe_start_x, swipe_start_y, swipe_end_x, swipe_end_y)
            time.sleep(1)  # Wait for the swipe to complete

def swipe_to_first_building_screen(device_id):
    """
    Swipe back to the first screen of buildings.
    """
    # Swipe coordinates to move back to the first set of buildings
    swipe_start_x = 50
    swipe_start_y = 540  # Middle of the screen vertically
    swipe_end_x = 1900
    swipe_end_y = 540  # Middle of the screen vertically

    num_swipes_back = 4  # Number of swipes needed to return to the first screen

    for i in range(num_swipes_back):
        print_with_time(f"Swiping back to the first set of buildings (Swipe {i+1}/{num_swipes_back})")
        adb_swipe(device_id, swipe_start_x, swipe_start_y, swipe_end_x, swipe_end_y)
        time.sleep(1)  # Wait for the swipe to complete

def collect_daily_reward(device_id):
    """
    Automate the process of collecting the daily reward.
    """
    # Coordinates for the Daily Event button
    daily_event_x = 1650
    daily_event_y = 90
    
    # Coordinates for the Daily Reward button
    daily_reward_x = 660
    daily_reward_y = 560
    
    # Coordinates range for the boxes of the daily reward
    start_x = 530
    end_x = 1490
    start_y = 380
    end_y = 850
    num_boxes_x = 7  # Assuming 7 boxes in each row
    num_boxes_y = 4  # Assuming 4 rows

    # Calculate the step size between boxes
    step_x = (end_x - start_x) // (num_boxes_x - 1)
    step_y = (end_y - start_y) // (num_boxes_y - 1)
    
    # Coordinates of the OK button
    ok_button_x = 960
    ok_button_y = 860
    
    # Coordinates of the "X" button to close Daily Reward screen
    close_daily_reward_x = 1650
    close_daily_reward_y = 120
    
    # Coordinates of the "X" button to close Daily Event screen
    close_daily_event_x = 1700
    close_daily_event_y = 140
    
    # Click Daily Event
    print_with_time("Clicking Daily Event button")
    adb_tap(device_id, daily_event_x, daily_event_y)
    time.sleep(2)  # Wait for the Daily Event screen to load
    
    # Click Daily Reward
    print_with_time("Clicking Daily Reward button")
    adb_tap(device_id, daily_reward_x, daily_reward_y)
    time.sleep(2)  # Wait for the Daily Reward screen to load
    
    # Click reward boxes
    day_counter = 1
    for row in range(num_boxes_y):
        for col in range(num_boxes_x):
            x = start_x + col * step_x
            y = start_y + row * step_y
            print_with_time(f"Clicking Daily Reward {day_counter} at ({x}, {y})")
            adb_tap(device_id, x, y)
            day_counter += 1

    # Click OK button
    print_with_time("Clicking OK button")
    adb_tap(device_id, ok_button_x, ok_button_y)
    time.sleep(1)  # Wait for the confirmation
    
    # Close Daily Reward screen
    print_with_time("Clicking X button to close Daily Reward screen")
    adb_tap(device_id, close_daily_reward_x, close_daily_reward_y)
    time.sleep(1)  # Wait for the screen to close
    
    # Close Daily Event screen
    print_with_time("Clicking X button to close Daily Event screen")
    adb_tap(device_id, close_daily_event_x, close_daily_event_y)
    time.sleep(1)  # Wait for the screen to close


def enter_trial(device_id, building_x, building_y, num_swipes, enter_button_x, enter_button_y):
    """
    Perform the steps to enter a trial, click Enter, Quit, and OK buttons.
    """
    # Swipe coordinates to move to the building
    swipe_start_x = 1900
    swipe_start_y = 540  # Middle of the screen vertically
    swipe_end_x = 50
    swipe_end_y = 540  # Middle of the screen vertically

    # Coordinates of the Quit button
    quit_button_x = 1530
    quit_button_y = 1020
    
    # Coordinates of the OK button
    ok_button_x = 950
    ok_button_y = 660

    # Coordinates of the Next Floor button
    next_floor_button_x = 600
    next_floor_button_y = 1030
    
    # Coordinates of the Speed button
    speed_button_x = 950
    speed_button_y = 1000
    
    # Coordinates of the Acquire button
    acquire_button_x = 1730
    acquire_button_y = 920

    # Coordinates for the Temporary Retreat button
    temporary_retreat_x = 1400
    temporary_retreat_y = 915

    # Coordinates for the "X" button to close the trial screen
    close_trial_x = 1850
    close_trial_y = 60

    for i in range(num_swipes):
        # Swipe to the set of buildings
        print_with_time(f"Swiping to the set of buildings (Swipe {i+1}/{num_swipes})")
        adb_swipe(device_id, swipe_start_x, swipe_start_y, swipe_end_x, swipe_end_y)
        time.sleep(1)  # Wait for the swipe to complete

    # Tap on the trial building
    print_with_time("Clicking on the trial building")
    adb_tap(device_id, building_x, building_y)
    time.sleep(2)  # Wait for the building screen to load

    # Tap on the Enter button
    print_with_time("Clicking the Enter button")
    adb_tap(device_id, enter_button_x, enter_button_y)
    time.sleep(2)  # Wait for the trial to start

    # Tap on the Quit button
    print_with_time("Clicking the Quit button")
    adb_tap(device_id, quit_button_x, quit_button_y)
    time.sleep(2)  # Wait for the quit confirmation

    # Tap on the OK button
    print_with_time("Clicking the OK button")
    adb_tap(device_id, ok_button_x, ok_button_y)
    time.sleep(2)  # Wait for the action to complete
    
    # Tap on the trial building again
    print_with_time("Clicking on the trial building again")
    adb_tap(device_id, building_x, building_y)
    time.sleep(2)  # Wait for the building screen to load

    # Tap on the Enter button again
    print_with_time("Clicking the Enter button again")
    adb_tap(device_id, enter_button_x, enter_button_y)
    time.sleep(2)  # Wait for the trial to start

    # Tap on the Enter button to enter the trial
    print_with_time("Clicking the Enter button to start the trial")
    adb_tap(device_id, next_floor_button_x, next_floor_button_y)
    time.sleep(2)  # Wait for the trial to start

    # Tap on the Next Floor button
    print_with_time("Clicking the Next Floor button")
    adb_tap(device_id, next_floor_button_x, next_floor_button_y)
    time.sleep(8)  # Wait for the action to complete

    # Tap on the Speed button (only once)
    print_with_time("Clicking the Speed button")
    adb_tap(device_id, speed_button_x, speed_button_y)

    # Number of times to re-enter the trial
    i = 40

    # Repeat the process
    for trial in range(i):  
        # Continuously tap on the Acquire and Next Floor button every 5 seconds
        print_with_time(f"Trying Trial {i - trial} left")
        for _ in range(10):  # Adjust the number of repetitions as needed
            time.sleep(5)  # Wait for 5 seconds before tapping again
            print_with_time("Clicking the Acquire button")
            adb_tap(device_id, acquire_button_x, acquire_button_y)
            time.sleep(0.5)  # Wait for 1 second before tapping again
            print_with_time("Clicking the Next Floor button")
            adb_tap(device_id, next_floor_button_x, next_floor_button_y)

    for attempt in range(10):
        time.sleep(2)  # Wait for the action to complete
        # Attempt to click Temporary Retreat
        print_with_time(f"Attempt {attempt+1}: Clicking Temporary Retreat button")
        adb_tap(device_id, temporary_retreat_x, temporary_retreat_y)
        time.sleep(5)  # Wait for the action to complete
        
        # Check if the battle is still ongoing
        # If battle is still ongoing, it will attempt again; otherwise, it will proceed

        # Attempt to click the Acquire button (if necessary)
        print_with_time("Clicking the Acquire button")
        adb_tap(device_id, acquire_button_x, acquire_button_y)
        time.sleep(2)  # Short delay after clicking Acquire button

    # After the trial looping is finished
    # Click Temporary Retreat
    print_with_time("Clicking Temporary Retreat button")
    adb_tap(device_id, temporary_retreat_x, temporary_retreat_y)
    time.sleep(2)  # Wait for the action to complete

    # Click the "X" button to close the trial screen
    print_with_time("Clicking X button to close trial screen")
    adb_tap(device_id, close_trial_x, close_trial_y)
    time.sleep(2)  # Wait for the screen to close

    # Back to the first screen (the first 3 buildings)
    swipe_to_first_building_screen(device_id)

# Function to enter Senior Ninja Trial using the common function
def enter_senior_ninja_trial(device_id):
    enter_trial(device_id, 300, 600, 2, 289, 275)

# Function to enter God Shinobi Tower using the common function
def enter_god_shinobi_tower(device_id):
    enter_trial(device_id, 1490, 600, 3, 1500, 180)


# Main function
def main():
    print_with_time("Starting Ninja Heroes bot...")
    connect_adb()
    device_id = get_bluestacks_device_id()
    
    if device_id:
        click_close_button(device_id)
        time.sleep(8)  # Wait for the announcement to close
        choose_server(device_id)
        time.sleep(5)  # Wait for the game to load and display announcements
        close_announcements_and_events(device_id)
        time.sleep(2)  # Wait for screens to close
        collect_money_from_buildings(device_id)
        swipe_to_first_building_screen(device_id)
        collect_daily_reward(device_id)
        enter_senior_ninja_trial(device_id)
        enter_god_shinobi_tower(device_id)
    else:
        print_with_time("BlueStacks device ID not found.")

if __name__ == "__main__":
    main()
