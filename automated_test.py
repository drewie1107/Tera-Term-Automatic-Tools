import pyautogui
import time
import csv

pyautogui.PAUSE = .3
serial_number = ""
mac_address = ""

log_file_path = "teraterm.log"

last_sn = None
last_mac = None

config_commands = [
    "set_max_watt 3 400",
    "set_cv 3 0"

]

testing_commands = [
    "set_ws 2 100 0",
    "set_ws 0"
]

logging_commands = [
    "get_sn",
    "get_mac"
]

ending_commands = [
    "set_max_watt 3 100",
    "set_cv 3 0"
]

def find_mac_and_sn(lines):
    mac_found = False
    sn_found = False
    for line in lines:
    # Check if the line contains "MAC: "
        if "MAC: " in line:
            # Find the index of "MAC: "
            mac_index = line.index("MAC: ")
            # Extract and print the rest of the line after "MAC: "
            mac_address = line[mac_index + len("MAC: "):].strip()
            mac_found = True
        if "SN: " in line:
            # Find the index of "SN: "
            serial_number_index = line.index("SN: ")
            serial_number = line[serial_number_index + len("SN: "):].strip()
            sn_found = True
    
        if sn_found & mac_found == True:
            break
    if sn_found & mac_found == False:
        serial_number = None
        mac_address = None
    return mac_address, serial_number

def run_commands(command_list, wait_time = 0.1):
    for command in command_list:
        pyautogui.hotkey('ctrl','c')
        pyautogui.write(command, interval = 0.075)
        pyautogui.hotkey('enter')
        time.sleep(wait_time)

def write_to_csv(sn_to_csv, mac_to_csv):
    global last_mac
    global last_sn
    # Write the serial number and MAC address to a CSV file
    csv_file_path = "output.csv"

    with open(csv_file_path, 'r') as csvfile:
        lines = csvfile.readlines()
        final_sn = sn_to_csv
        final_mac = mac_to_csv
        for line in lines:
            if mac_address in line:
                print("MAC repeated")
                final_mac = "Repeated"
            if serial_number in line:
                print("SN repeated")
                final_sn = "Repeated"
    if final_sn is not final_mac:
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['Serial Number', 'MAC Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty; if yes, write the header
            file_empty = csvfile.tell() == 0
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if file_empty:
                writer.writeheader()
                
            writer.writerow({'Serial Number': final_sn, 'MAC Address': final_mac})
            last_sn = sn_to_csv
            last_mac = mac_to_csv

        print("Data has been written to", csv_file_path)
    else: print("NO DATA HAS BEEN WRITTEN.")

# V THIS IS WHERE THE MAGIC HAPPENS V

#pyautogui.click(x=1350, y=1070) # Switch windows. Very ghetto.
pyautogui.click(x=200, y=500)

run_commands(["update_db"], 8)
run_commands(config_commands, 0.75)
time.sleep(3)
run_commands(testing_commands, 0.75)
run_commands(logging_commands, 0.75)
run_commands(ending_commands, 0.75)

try: # Reads TeraTerm log and returns MAC and SN
    with open(log_file_path, "r") as tera_term:
        tera_term_parsed = tera_term.readlines()
        tera_term_parsed.reverse()
        # print(log_contents) # Replace with finding MAC and SN
        mac_address, serial_number = find_mac_and_sn(tera_term_parsed)
except FileNotFoundError:
    print("Log file not found. Please check the file path.")

pyautogui.click(x=1350, y=1070)

print(serial_number)
print(mac_address)

write_to_csv(serial_number,mac_address)

pyautogui.click(x=1350, y=800)
pyautogui.hotkey('up')