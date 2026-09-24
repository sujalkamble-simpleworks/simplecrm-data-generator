from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import requests
import faker_utils
import csv
import os
import time

os.makedirs('data', exist_ok=True)

class RecordCreator:
    tokens: list = []
    baseurl: str
    moduleData: dict = {}
    moduleObjects: dict = {}

    def __init__(self, user: dict, baseurl: str):
        self.baseurl = baseurl
        users = [user]
        for user in users:
            response = requests.post(
                baseurl + "/auth/login",
                params={"timestamp": int(time.time() * 1000)},
                data={
                    "username": user["username"],
                    "password": user["password"],
                    "grant_type": "password",
                    "client_id": "741227e4-64d3-b2cd-0318-5f64953a436c",
                    "client_secret": "ritesh",
                },
            )

            if response.status_code == 200:
                print(response.text)
                data = response.json()
                self.tokens.append(data["access_token"])
            else:
                raise Exception(f"Failed to get token: {response.text}")
            
    def process_modules(self, modules: dict,mode:str = "api"):
        for module in modules.values():
            self.set_module_fields(module,mode)
            
    def generate_csv(self, modules: dict, progress_callback=None) -> list[str]:
        filenames = []
        completed_records = 0
        for module in modules.values():
            filename = f"data/{module['name']}_{module['records']}_data.csv"
            filenames.append(filename)
            
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header
                headers = self.moduleData[module['backend_name']].keys()
                writer.writerow(headers)
                
                # Write data rows
                for _ in range(module['records']):
                    row = faker_utils.get_module_data(self.moduleData[module['backend_name']])
                    writer.writerow(row.values())
                    completed_records += 1
                    if progress_callback is not None:
                        progress_callback(completed_records)

        return filenames
            
    def create_records(self, modules: dict):

        # Prepare all tasks
        tasks = []
        for module in modules.values():
            for i in range(module["records"]):
                record_data = module.copy()
                record_data["record_number"] = i + 1
                tasks.append((module))

        # Execute in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_task = {executor.submit(self.create_record, t): t for t in tasks}
        
            for future in as_completed(future_to_task):
                result = future.result()
                yield result   # ✅ yields one result at a time

    def create_record(self, module: dict):
        #sleep for 1 second to simulate network delay
        # time.sleep(0.5)
        # return {"status": "success","module" : f"{module['name']}", "response": f"Record created in {module['backend_name']}"}
        
        backend_name = module["backend_name"]
        url = f"{self.baseurl}/module"
        data = {
            "data": {
                "type": backend_name,
                "attributes": faker_utils.get_module_data(
                    self.moduleData[backend_name]
                ),
            }
        }
        headers = {
            "Authorization": f"Bearer {random.choice(self.tokens)}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post(url, json=data, headers=headers)
        print(response)

        if response.status_code == 201:
            print(f"Record created in {backend_name}: {response.json()}")
            return {"status": "success", "module": module['name'], "response": response.json()}
        else:
            print(f"Failed to create record in {backend_name}: {response.text}")
            return {"status": "failed", "module": module['name'], "response": response.json()}


    def set_module_fields(self, module: dict,mode:str = "api"):
        backend_name = module["backend_name"]

        headers = {
            "Authorization": self.tokens[0],
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        url = f"{self.baseurl}/layout/CreateView/{backend_name}/1"
        response = requests.get(url, headers=headers)

        fields = []

        if response.status_code == 200:
            try:
                data = response.json()
                print("data", data)

                panels = data.get("data", {}).get("templateMeta", {}).get("data", [])

                if panels:
                    for panel in panels:
                        rows = panel.get("attributes", [])
                        for row in enumerate(rows):
                            for field in enumerate(row[1]):
                                fields.append(field[1])
            except Exception as e:
                print("Error parsing JSON:", e)
                raise ValueError("Invalid JSON response") from e
        else:
            raise Exception(f"Failed to get module fields: {response.text}")

        self.moduleData[backend_name] = faker_utils.create_module_template(fields,mode)
