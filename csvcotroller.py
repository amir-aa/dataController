import csv
import mmap
def append_batch_to_csv(file_path,data):

    with open(file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in data:
            csv_writer.writerow(item)

def append_to_csv(file_path, data):
    """
    Append data to a CSV file.

    Parameters:
    - file_path: Path to the CSV file.
    - data: List containing data to be appended (e.g., [id, name, status]).
    """
    with open(file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

def search_in_csv(file_path, target_id):
    """
    Search for a specific id in the CSV file.

    Parameters:
    - file_path: Path to the CSV file.
    - target_id: The id to search for.

    Returns:
    - If found, returns the entire row as a list; otherwise, returns None.
    """
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row and row[0] == str(target_id):
                return row
    return None

def change_status_by_id(file_path, target_id, new_status):
    """
    Change the status in the CSV file based on the id.

    Parameters:
    - file_path: Path to the CSV file.
    - target_id: The id to search for.
    - new_status: The new status value.
    """
    with open(file_path, 'r+', newline='') as csv_file:
        # Use mmap for efficient searching
        mmapped_file = mmap.mmap(csv_file.fileno(), 0)
        
        # Find the target_id in the file
        index = mmapped_file.find(bytes(str(target_id), 'utf-8'))
        if index != -1:
            # Move the cursor to the beginning of the line containing the target_id
            mmapped_file.seek(index)
            
            # Read the entire line and split it into columns
            line = mmapped_file.readline().decode('utf-8').strip()
            columns = line.split(',')
            
            # Update the status (assuming the status is the second column)
            columns[1] = str(new_status)
            
            # Move the cursor back to the beginning of the line and write the updated line
            mmapped_file.seek(index)
            mmapped_file.write(bytes(','.join(columns) + '\n', 'utf-8'))
            
        # Close the mmap
        mmapped_file.close()
def change_multiple_status_by_ip(file_path,targets:list):
    for item in targets:
        target_id=item[0]
        new_status=item[2]
        with open(file_path, 'r+', newline='') as csv_file:
            # Use mmap for efficient searching
            mmapped_file = mmap.mmap(csv_file.fileno(), 0)
            
            # Find the target_id in the file
            index = mmapped_file.find(bytes(str(target_id), 'utf-8'))
            if index != -1:
                # Move the cursor to the beginning of the line containing the target_id
                mmapped_file.seek(index)
                
                # Read the entire line and split it into columns
                line = mmapped_file.readline().decode('utf-8').strip()
                columns = line.split(',')
                
                # Update the status (assuming the status is the second column)
                columns[1] = str(new_status)
                
                # Move the cursor back to the beginning of the line and write the updated line
                mmapped_file.seek(index)
                mmapped_file.write(bytes(','.join(columns) + '\n', 'utf-8'))
                
            # Close the mmap
            mmapped_file.close()

def get_last_row(csv_file_path):
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    if rows:
        return rows[-1]
    else:
        return None

# Example usage:
# Append data to CSV
#append_to_csv('data.csv', ['12235513513213515311', 'John', 'Active'])
#append_to_csv('data.csv', ['35132132155555554441', 'Alice', 'Inactive'])

# Search for data in CSV
result = search_in_csv('data.csv', 351321)
print("Search Result:", result)
print(get_last_row('data.csv'))
# Change status by id
#change_status_by_id('data.csv', 35132132155555554441, 1)
