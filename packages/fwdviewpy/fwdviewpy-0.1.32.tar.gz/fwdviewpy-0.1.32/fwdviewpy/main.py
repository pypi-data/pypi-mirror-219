import logging
import sys
import requests
import time 
import json
import datetime
import subprocess

class RunScriptManager:
    def __init__(self,databaseType,DATABASE_NAME,PROJECT_NAME,SERVER_NAME_AND_INSTANCE=None,TNS_ENTRY=None,slackEndpoint=None):
        """
        This class is used to execute the pre and post scripts for the masking runs. 

        Args:
            databaseType (str): This should be either 'MSSQL' or 'Oracle'. 
            DATABASE_NAME (str): This is the name of the Database. 
            PROJECT_NAME (str): This is the name of the Masking Run. 
            SERVER_NAME_AND_INSTANCE (str, optional): This is the name of the Server and Instance, needed for MSSQL databases. Defaults to None.
            TNS_ENTRY (str, optional): This is the TNS Entry, needed for Oracle databases. Defaults to None.
            slackEndpoint (str, optional): This is the endpoint for the slack channel you want to send your alerts to. Defaults to None.
        """        
        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d")
        logging.basicConfig(filename=f'DelphixEngineSessionManager_{formatted_date_time}.log',
                            level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', filemode='a')
        self.databaseType = databaseType 
        self.DATABASE_NAME = DATABASE_NAME
        self.PROJECT_NAME = PROJECT_NAME
        self.slackEndpoint = slackEndpoint
        self.SERVER_NAME_AND_INSTANCE = SERVER_NAME_AND_INSTANCE
        self.TNS_ENTRY = TNS_ENTRY

    def log_timings(func): 
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = int(end_time - start_time)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_formatted = f"{hours:02d} Hours {minutes:02d} Minutes {seconds:02d} Seconds"
            logging.info(f"Duration: {duration_formatted}.\n\n")
            return result
        return wrapper

    def send_slack_message(self,message):
        if self.slackEndpoint != None:
            payload = '{"text":"%s"}' % message
            response = requests.post(self.slackEndpoint,
                                    data = payload)
    
    def runScript(self,command):
        """
        This function is run in the runScriptStep function.
        Args: 
            command: This function takes the command to be run on the command line as the argument. 
        Returns: 
            True if there is not an Error and False if there is. 
        """
        splitCommand = command.split()
        if self.databaseType == "MSSQL": 
            result = subprocess.run(
                splitCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        elif self.databaseType == "Oracle": 
            result = subprocess.run(
                splitCommand, input="\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else: 
            print(f"ERROR: {self.databaseType} is an invalid database type. Please use either 'MSSQL' or 'Oracle'.")   
            logging.error(f"ERROR: {self.databaseType} is an invalid database type. Please use either 'MSSQL' or 'Oracle'.")
            self.send_slack_message(f"ERROR: {self.databaseType} is an invalid database type. Please use either 'MSSQL' or 'Oracle'.")
        
        logging.info(f"Command: {command}")
        logging.info(f"Return Code: {result.returncode}")
        if result.stderr:
            logging.info(f"Error: {result.stderr.strip()}\n")
        if "error" in result.stdout.lower():
            self.send_slack_message(f"ERROR: {command} ----- SQL script output contains error message.")
        logging.info(f"Output:\n{result.stdout}\n")
        if result.returncode == 1 and result.stderr.strip() != "None": 
            return False 
        else: 
            return True 
    
    @log_timings
    def runScriptStep(self,step,scriptName,scriptPath):
        """
        This function calls the runScript function. 
        Args: 
            step: This is the step of the masking run which is currently executing. 
            scriptName: This is the name of the script which is being executed. 
            scriptPath: This is the path of the script which is being executed. 
        Returns: 
            This function does not return anything. It sends a slack message logging if it was successful or not and logs in the logging file. 
        """
        try: 
            logging.info(f'{self.PROJECT_NAME} STEP {step}: Running Script "{scriptName}"')
            if self.databaseType == 'MSSQL':
                if self.runScript(f"sqlcmd -S {self.SERVER_NAME_AND_INSTANCE} -i {scriptPath} -d {self.DATABASE_NAME} -E"):
                    self.send_slack_message(f"{self.PROJECT_NAME} Step {step} is successful!")
                else: 
                    self.send_slack_message(f"ERROR: {self.PROJECT_NAME} Step {step} has failed. {scriptName} has failed.")
                    sys.exit()
            if self.databaseType == "Oracle":
                if self.runScript(f"sqlplus {self.TNS_ENTRY} @{scriptPath}"):
                    self.send_slack_message(f"{self.PROJECT_NAME} Step {step} is successful!")
                else: 
                    self.send_slack_message(f"ERROR: {self.PROJECT_NAME} Step {step} has failed. {scriptName} has failed.")
                    sys.exit()
        except Exception as e: 
            self.send_slack_message(f"ERROR: {self.PROJECT_NAME} Step {step} has failed. An Error occurred: {e}.")
            sys.exit()

class VirtualisationEngineSessionManager:
    def __init__(self, address, username, password, major, minor, micro, PROJECT_NAME, CONTAINER_NAME, slackEndpoint=None):
        """
        This class is used to execute actions on the Delphix Virtualisation Engine. 
    
        Args:
            address (str): This is the IP address of the Delphix Engine. 
            username (str): Username needed to log into the Delphix Engine. 
            password (str): Password needed to log into the Delphix Engine.
            major (int): This is the major number associated with the Delphix Engine Version.
            minor (int): This is the minor number associated with the Delphix Engine Version.
            micro (int): This is the micro number associated with the Delphix Engine Version.
            PROJECT_NAME (str): This is the name of the Masking Run. 
            CONTAINER_NAME (str): The name of the self-service Delphix container you want to perform actions on. 
            slackEndpoint (str, optional): This is the endpoint for the slack channel you want to send your alerts to. Defaults to None.
        """        
        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d")
        logging.basicConfig(filename=f'DelphixEngineSessionManager_{formatted_date_time}.log',
                            level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', filemode='a')
        self.address = address
        self.username = username
        self.password = password
        self.major = major
        self.minor = minor
        self.micro = micro
        self.slackEndpoint = slackEndpoint
        self.CONTAINER_NAME = CONTAINER_NAME
        self.PROJECT_NAME = PROJECT_NAME

    def __str__(self):
        return f'Virtualisation Engine Session Manager: {self.address}'

    def log_timings(func): 
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = int(end_time - start_time)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_formatted = f"{hours:02d} Hours {minutes:02d} Minutes {seconds:02d} Seconds"
            logging.info(f"Duration: {duration_formatted}.\n\n")
            return result
        return wrapper
    
    def send_slack_message(self,message):
        if self.slackEndpoint != None:
            payload = '{"text":"%s"}' % message
            response = requests.post(self.slackEndpoint,
                                    data = payload)
    def _login(self):
        "This function logs into the Virtualisation Engine."
        
        session = requests.session()
        session_url = f"http://{self.address}/resources/json/delphix/session"
        data = {
            "type": "APISession",
            "version": {
                "type": "APIVersion",
                "major": self.major,
                "minor": self.minor,
                "micro": self.micro
            }
        }
        response = session.post(session_url, json=data)
        if not response.ok:
            logging.info(f"Session FAILED to established on {self.address}. Response: {response.status_code}")
            sys.exit()
        url = f"http://{self.address}/resources/json/delphix/login"
        data = {
            "type": "LoginRequest",
            "username": self.username,
            "password": self.password
        }
        response = session.post(url, json=data)
        if not response.ok:
            logging.error(f"login FAILED - Response: {response.status_code}")
            sys.exit()
        return session

    def replicate(self, replicationName): 
        """
        This method executes a replication job. 
        
        Args:
            replicationName: This is the name of the replication job. 
        
        Returns: 
            This method returns True if the replication was successful and False if it fails. 
        """
        session = self._login() 
        spec_url = f"http://{self.address}/resources/json/delphix/replication/spec" 
        APIQuery = session.get(spec_url)
        for replication in APIQuery.json()["result"]:
            if replication['name'] == replicationName: 
                replicationSpec = replication['reference']   
        replication_url = f"http://{self.address}/resources/json/delphix/replication/spec/{replicationSpec}/execute"
        data = {}
        response = session.post(replication_url,json=data)
        action = response.json()['action']
        if self._checkActionLoop(action):
            session.close()
            logging.info(f"Replication Successful!\n\n Replication Name: {replicationName}\n Engine: {self.address}")
            return True
        else:
            session.close()
            return False 
    
    def refreshContainer(self, containerName): 
        """
        This method refreshes the container on the Delphix Engine. 

        Args: 
            containerName: This is the name of the container to be refreshed on the Delphix Engine.

        Returns: 
            This method returns True is the refresh was made successfully & returns False if it failed to refresh.
        """
        session = self._login()
        container_url = f"http://{self.address}/resources/json/delphix/selfservice/container"
        APIQuery = session.get(container_url)
        for container in APIQuery.json()["result"]:
            if container['name'] == containerName: 
                containerReference = container['reference']
        refresh_url = f"http://{self.address}/resources/json/delphix/selfservice/container/{containerReference}/refresh"
        data = {"type": "JSDataContainerRefreshParameters", "forceOption": False}
        response = session.post(refresh_url,json=data)
        action = response.json()['action']
        if self._checkActionLoop(action):
            session.close()
            logging.info(f"Refresh Successful!\n\n Container Name: {containerName}\n Engine: {self.address}")
            return True
        else:
            session.close()
            return False 

    def createBookmark(self, containerName, bookmarkName):
        # Set up the session object
        """ 
        This method creates a bookmark on the container of the Delphix Engine. 

        Args: 
            containerName: This is the name of the container to be bookmarked on the Delphix Engine. 
            bookmarkName: This argument is the name of the bookmark to be made on the containerName.
        
        Returns: 
            This method returns True is the bookmark was made successfully & returns False if it failed to create a bookmark. 
        """
        containerReference, containerBranch = self._getTemplateBranch(containerName)
        # Send a POST request to the bookmark endpoint with cookies set from the session
        bookmark_url = f"http://{self.address}/resources/json/delphix/selfservice/bookmark"
        data = {
            "type": "JSBookmarkCreateParameters",
            "bookmark": {
                "type": "JSBookmark",
                "name": bookmarkName,
                "branch": containerBranch
            },
            "timelinePointParameters": {
                "type": "JSTimelinePointLatestTimeInput",
                "sourceDataLayout": containerReference
            }
        }
        session = self._login()
        response = session.post(bookmark_url, json=data)
        action = response.json()['action']
        if self._checkActionLoop(action):
            session.close()
            logging.info(f"Bookmark has been created!")
            logging.info(f"Bookmark Name: {bookmarkName}")
            logging.info(f"Container Name: {containerName}")
            logging.info(f"Engine Name: {self.address}\n\n")
            return True
        else:
            session.close()
            return False 

    def _checkActionLoop(self, action): 
        while True:
            if self._checkAction(action):
                return True
            elif self._checkAction(action) == "FAILED":
                logging.error("Failed to create Bookmark. Please see Engine logs.")
                return False
            else:
                print("Not yet Completed, check again in 10 seconds")
                time.sleep(10)

    def _checkAction(self, action):
        session = self._login()
        action_url = f"http://{self.address}/resources/json/delphix/action"
        APIQuery = session.get(action_url)
        for actions in APIQuery.json()["result"]:
            if actions['reference'] == action:
                state = actions['state']
                if state == "COMPLETED":
                    session.close()
                    return True
                elif state == "FAILED":
                    state = "FAILED"
                    session.close()
                    return state
                else:
                    return False
    
    def _getTemplateBranch(self, containerName):
        # Log in and obtain the session object
        session = self._login()   
        # Send a GET request to the selfservice/template endpoint with cookies set from the session
        template_url = f"http://{self.address}/resources/json/delphix/selfservice/container"
        response = session.get(template_url)
        # Extract the template reference and active branch from the API response
        container_reference = None
        container_branch = None
        for container in response.json()["result"]:
            if container['name'] == containerName:
                container_reference = container["reference"]
                container_branch = container["activeBranch"]
                break
        logging.debug(f"container reference: {container_reference} & Template branch: {container_branch}")
        session.close()
        return container_reference, container_branch 
    
    def _getFormattedYearAndMonth(self):
        # Get the current time as a struct_time object
        current_time = time.localtime()

        # Extract the year and month values from the time object
        year = str(current_time.tm_year)[-2:]
        month = '{:02d}'.format(current_time.tm_mon)

        # Format the date as a string in the desired format
        date_str = f"{year}M{month}"

        # Print the formatted date
        return date_str
    
    @log_timings
    def createBookmarkStep(self,step,name):
        formatted_month = self._getFormattedYearAndMonth()
        try:
            logging.info(f'{self.PROJECT_NAME} STEP {step}: Create Bookmark "{name}"')
            if self.createBookmark(containerName=self.CONTAINER_NAME,bookmarkName=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {formatted_month} {name}'):
                self.send_slack_message(f"{self.PROJECT_NAME} Step {step} is successful!")
            else: 
                self.send_slack_message(f"ERROR: {self.PROJECT_NAME} Step {step} has failed. Failed to create bookmark {name}")
                sys.exit()
        except Exception as e: 
            self.send_slack_message(f"ERROR: {self.PROJECT_NAME} Step {step} has failed. An Error occurred: {e}.")
            sys.exit()
    
class MaskingEngineSessionManager: 
    def __init__(self, address, username, password, PROJECT_NAME, ENVIRONMENT_NAME, slackEndpoint=None): 
        """
        This class is used to execute actions on the Delphix Continuous Compliance Engine.

        Args:
            address (str): This is the IP address of the Delphix Engine.
            username (str): Username needed to log into the Delphix Engine.
            password (str): Password needed to log into the Delphix Engine.
            PROJECT_NAME (str): This is the name of the Masking Run. 
            ENVIRONMENT_NAME (str): This is the name of the Environment. 
            slackEndpoint (str, optional): This is the endpoint for the slack channel you want to send your alerts to. Defaults to None.
        """        
        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d")
        logging.basicConfig(filename=f'DelphixEngineSessionManager_{formatted_date_time}.log',
                            level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', filemode='a')
        self.address=address 
        self.username=username
        self.password=password
        self.PROJECT_NAME=PROJECT_NAME
        self.ENVIRONMENT_NAME=ENVIRONMENT_NAME
        self.slackEndpoint=slackEndpoint

    def __str__(self):
        return f'Masking Engine Session Manager: {self.address}'
    
    def log_timings(func): 
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = int(end_time - start_time)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_formatted = f"{hours:02d} Hours {minutes:02d} Minutes {seconds:02d} Seconds"
            logging.info(f"Duration: {duration_formatted}.\n\n")
            return result
        return wrapper
    
    def login(self) -> str:
        """
        This method logs in to the Delphix Masking Engine. 
        
        Returns: 
            str: Authentication key used to send API requests to the engine. 
        """ 
        url = f"http://{self.address}/masking/api/v5.1.14/login"

        payload = json.dumps({"username": self.username, "password": self.password})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        responseDict = response.json()
        authKey = responseDict['Authorization']
        return authKey
    
    def runMaskingJob(self, environment, maskingRule, connectorName=None) -> bool:
        """
        This method executes pre-configured masking jobs on the masking engine.

        Args: 
            environment: This is the environent on the Delphix masking engine on which to run the masking job. 
            maskingRule: This is the ruleset that we want to run on the delphix engine. 
            connectorName: This is the name of the connector for which connects the masking job to the data. This variable need only be provided if the masking job is mulit-tennant and can be omitted if this is not the case.
        
        Returns: 
            bool: This returns True if it has run successfully and False if there is an Error. 
        """
        
        authKey = self.login()
        envID = self._getEnvironment(authKey, environment)
        ruleID = self._getJobId(authKey, maskingRule, envID)
        if connectorName != None: 
            targetConnectorID = self._getTargetConnectorID(authKey, connectorName, envID)
            self._execute_job(authKey, ruleID, targetConnectorID)
        else: 
            self._execute_job(authKey, ruleID)
        logging.info(f"Masking job triggered. Job: {maskingRule}")
        executionID = self._getExecutionID(authKey, ruleID)
        jobStatus = self._checkStatus(executionID) 

        if jobStatus == "SUCCEEDED":
            logging.info(f"Masking Successful. Job: {maskingRule}\n\n")
            return True
        else:
            logging.error(f"Please check error logs for masking job: {maskingRule}\n\n")
            return False
    
    def _getEnvironment(self, authKey, envName) -> int:
        """API call to get an environment ID from the environment name

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            envName (int): Name of the environment.

        Returns:
            int: ID of the environment
        """        
        response = self._getRequest(authKey, "environments")
        response = json.loads(response)
        for env in response["responseList"]:
            if env["environmentName"] == envName:
                envID = env["environmentId"]
        return envID
    

    def _getRequest(self, authKey, endPoint) -> str:
        """Generic get request blueprint

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            endPoint (str): HTTP endpoint of chosen API call.

        Returns:
            str: Text response from API request.
        """        
        url = f"http://{self.address}/masking/api/v5.1.14/{endPoint}"
        payload = {}
        headers = {
            'Authorization': authKey
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def _getExecutionID(self, authKey, jobID) -> int:
        """API call to get an execution ID from the job ID.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            jobID (int): ID of the job.

        Returns:
            int: ID of the execution
        """        
        endPoint = f"executions?job_id={jobID}&page_number=1&execution_status=RUNNING"
        response = self._getRequest(authKey, endPoint)
        response = json.loads(response)
        executionID = response['responseList'][0]['executionId']
        return executionID

    def _getJobId(self, authKey, jobName, envID) -> int:
        """API call to get a job ID from the job name and environment ID.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            jobName (str): Name of the job.
            envID (int): ID of the environment.

        Returns:
            int: ID of the job.
        """        
        endPoint = f"masking-jobs?environment_id={envID}"
        response = self._getRequest(authKey, endPoint)
        response = json.loads(response)
        for job in response["responseList"]:
            if job["jobName"] == jobName:
                jobID = job['maskingJobId']
        return jobID

    def _getTargetConnectorID(self, authKey, connectorName, environmentId) -> int:
        """API call to get a target connector ID from the connector name and environment ID.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            connectorName (str): Name of the connector.
            environmentId (int): ID of the environment.

        Returns:
            int: ID of the target connector.
        """        
        response = self._getRequest(authKey, "database-connectors")
        response = json.loads(response)
        for connectors in response["responseList"]:
            if connectors["connectorName"] == connectorName and connectors["environmentId"] == environmentId:
                targetConnectorID = connectors["databaseConnectorId"]
        return targetConnectorID
     
    def _execute_job(self, auth_key, job_id, targetConnectorID=None) -> str:
        """API call to get a target connector ID from the connector name and environment ID.

        Args:
            auth_key (str): Authentication key used to send API requests to the engine. 
            job_id (_type_): ID of the job.
            targetConnectorID (int, optional): ID of the target connector. Used for multi-tenant jobs. Defaults to None.

        Returns:
            str: Text response from API request.
        """        
        url = f"http://{self.address}/masking/api/v5.1.14/executions"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_key
        }
        if targetConnectorID != None: 
            data = {
                'jobId': job_id, 
                'targetConnectorId': targetConnectorID
            }
        else:
            data = {'jobId': job_id}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.text
    
    def _getStatus(self,authKey,executionID) -> str: 
        """API call to get the status of a running job.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            executionID (int): ID of the execution.

        Returns:
            str: Status of the execution.
        """        
        response = self._getRequest(authKey, f"executions/{executionID}")
        response = json.loads(response)
        status = response["status"]
        return status    
    
    def _checkStatus(self, executionID) -> str:
        """Checks the status of an execution.

        Args:
            executionID (int): ID of the execution.

        Returns:
            str: Status of the execution
        """        
        authKey = self.login()
        timeBetweenChecks=60
        while True:
            status = self._getStatus(authKey, executionID)
            
            if status == "RUNNING":
                time.sleep(timeBetweenChecks)
                print(f"Job is still running, check again in {round(timeBetweenChecks / 60, 2)} minute(s).")
            else:
                print(f"Job has finished running. Job Status is: {status}")
                return status
            
    def refreshRuleSets(self, EnvironmentName):
        """This function refreshes all rulesets in an environment which it is able to refresh. 
           If it is not able to refresh a ruleset, then it simply skips over this ruleset and 
           attempts to refresh the next. It records which rulesets it is able to refresh and 
           which it cannot in the log file. 

        Args:
            EnvironmentName (str): Name of the environment.
        """        
        authKey = self.login()
        environmentID = self._getEnvironment(authKey,EnvironmentName)
        response = self._getRequest(authKey, f"database-rulesets?environment_id={environmentID}")
        response = json.loads(response)
        ruleSetIDList = [ruleSet["databaseRulesetId"] for ruleSet in response["responseList"]]
        
        for ruleSetID in ruleSetIDList: 
            url = f"http://{self.address}/masking/api/v5.1.14/database-rulesets/{ruleSetID}/refresh"
            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': authKey
            }
            response = requests.put(url, headers=headers)
            json_response = response.json()
            try: 
                async_task_id = json_response['asyncTaskId']
            except KeyError:
                print(f"There's a problem with refreshing id: {ruleSetID} \n Message: {json_response}") 
                logging.error(f"There's a problem with refreshing id: {ruleSetID} \n Message: {json_response}")
                print("Skipping checking loop.")
                ERROR = True
            else:
                ERROR = False
            if not ERROR: 
                while True: 
                    response = self._getRequest(authKey, f"async-tasks/{async_task_id}")
                    response = json.loads(response)
                    if response["status"] == "SUCCEEDED": 
                        print(f"Successful for id: {ruleSetID}\n")
                        logging.info(f"Successful for id: {ruleSetID}\n")
                        break 
                    else:
                        print("Not yet Completed, check again in 10 seconds")
                        time.sleep(10) 
    
    @log_timings
    def runMaskingJobStep(self,step,maskingJobName,connectorName=None):
        try: 
            logging.info(f'{self.PROJECT_NAME} STEP {step}: Run Masking Job - {maskingJobName}')
            if connectorName != None: 
                if self.runMaskingJob(self.ENVIRONMENT_NAME,maskingJobName,connectorName):
                    self.send_slack_message(f'{self.PROJECT_NAME} Step {step} is Successful!')
                else: 
                    self.send_slack_message(f'ERROR: {self.PROJECT_NAME} Step {step} has failed. {maskingJobName} has failed.')
                    sys.exit()
            else:
                if self.runMaskingJob(self.ENVIRONMENT_NAME,maskingJobName):
                    self.send_slack_message(f'{self.PROJECT_NAME} Step {step} is Successful!')
                else: 
                    self.send_slack_message(f'ERROR: {self.PROJECT_NAME} Step {step} has failed. {maskingJobName} has failed.')
                    sys.exit()
        except Exception as e: 
            self.send_slack_message(f"ERROR: {self.PROJECT_NAME} Step {step} has failed. An Error occurred: {e}.")
            sys.exit()

    def send_slack_message(self,message):
        if self.slackEndpoint != None:
            payload = '{"text":"%s"}' % message
            response = requests.post(self.slackEndpoint,
                                    data = payload)