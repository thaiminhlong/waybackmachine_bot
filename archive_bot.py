import requests
import time
import csv
from datetime import datetime, timezone

## Constants 
file_path = r"File-Path-Here" ## Example: C:\...\...
outCSVFile = r"File-Path-Here" ## Example: C:\...\...

## Read File
def readFileOfLinks(file_path):
    ListOfLinks = []
    with open(file_path) as file: ## Opening the file
        for link in file: ## Read each line
            if link.strip(): ## Check empty after stripping leading whitespace
                ListOfLinks.append(link.strip()) ## Append links into ListofLinks
    return ListOfLinks


## Upload Link To Way Back Machine
def UploadToWayback(link):
    maxRetry = 5 ## Maximum number of retry when the program fail
    trial = 0 ## Starter
    delay = 10 ## Delaying time

    while trial < maxRetry: 
        print(f"Attempt {trial+1}: Saving {link} to Way Back Machine")
        try: ## Trying
            upload = requests.get(f"https://web.archive.org/save/{link}", timeout = 60) ## Sending GET requests
            if upload.status_code == 200: ## If succeeds, status code will be 200
                print(f"{link} has been succesffuly saved")
                return {"Original Link": link,
                        "WayBackMachine Link": f"https://web.archive.org/save/{link}",
                        "Timestamp": datetime.now(timezone.utc).isoformat(),
                        "Status": "Success"}
            else:
                print(f"{link} did not get saved. Error: {upload.status_code}")
        except Exception as e: ## If fails
            print(f"Failing due to {e}")

        trial += 1
        
        if trial < maxRetry:
            print(f"Waiting {delay} before retrying")
            time.sleep(delay)

    if trial == maxRetry:
        print(f"All attempts failed: {link}")
        return {"Original Link": link,
                "WayBackMachine Link": "",
                "Timestamp": datetime.now(timezone.utc).isoformat(),
                "Status": "Failed"}

## Archive Result into CSV File
def ResultInCSV(results, file):
    with open(file, "w", newline="") as file:
        fields = ["Original Link", "WayBackMachine Link", "Timestamp", "Status"]
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(results)
    

## Main
def main():
    List_of_Links = readFileOfLinks(file_path) ## Get all links in file
    results = []

    for link in List_of_Links: ## Going through each link
        result = UploadToWayback(link) ## Upload to WayBackMachine and return result
        results.append(result) ## Each result get compiled into a list containing result
        time.sleep(10) ## delay 10 seconds everytime to avoid overload server
    
    ResultInCSV(results, outCSVFile) ## Put result in a structured CSV file
    print(f"Done. See archived results in {outCSVFile}")


## Run
if __name__ == "__main__":
    main()
