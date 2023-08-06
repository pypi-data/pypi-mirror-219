"""

*****************************
ExergenicsApi.class.py
*****************************

J.CHRISTIAN JAN 2022
Implements the Exergenics API documented at:

    1. Authentication
        https://app.swaggerhub.com/apis/exergenics/getAuthorizationToken/1.0.0

    2. Data Exchange API
        https://app.swaggerhub.com/apis/exergenics/getBuildings/1.0.0
"""

import os
import json
import uuid
import boto3
import inspect
import logging
import requests
import urllib.parse
from sys import exit
from datetime import date, datetime
from logtail import LogtailHandler
from typing import Union
from pytz import timezone


class ExergenicsApi:
    # authentication storage
    username, password, authorizationToken = "", "", None

    # last status and response from a request made
    lastStatus = None
    lastResponse = {}

    # internal counter for iterations
    internalCounter = 0

    # database
    database = "default"

    # Endpoint for authentication
    authEndpoint = "https://auth.exergenicsportal.com"

    # Endpoint for Data Exchange
    exchangeEndpointProduction = "https://api.exergenicsportal.com"
    exchangeEndpointStaging = (
        "https://f31l6pg1zd.execute-api.ap-southeast-2.amazonaws.com/staging"
    )

    # endpoint for Plotly
    plotlyEndpoint = (
        "http://plotlyapiaws-env.eba-ccinzgx8.ap-southeast-2.elasticbeanstalk.com/{}/{}"
    )
    # plotlyEndpoint = "http://127.0.0.1:8000/{}/{}"

    aws_bucketRoot = "https://exergenics-public.s3.ap-southeast-2.amazonaws.com/"
    aws_bucketName = "exergenics-public"

    # The current version of the API being implemented
    apiVersion = 1

    # mode (production,staging)
    mode = "production"
    componentId = "python-wrapper-default"

    # Endpoint Activities
    auth__getAuthorizationToken = "getAuthorizationToken"

    ex__tokenPing = "tokenPing"

    ex__getBuildings = "getBuildings"
    ex__putFile = "putFile"
    ex__getFiles = "getFiles"
    ex__putData = "putData"
    ex__getData = "getData"
    ex__getAllData = "getAllData"
    ex__linkTable = "linkTable"
    ex__deleteFiles = "deleteFiles"
    ex__clearData = "clearData"
    ex__getTreeData = "getTreeData"
    ex__getKeyData = "getKeyData"
    ex__getPlantJobs = "getPlantJobs"
    ex__jobLog = "jobLog"

    ex__getJobs = "getJobs"
    ex__getAutoDataRefreshJobs = "autoDataRefreshJobs"
    ex__JobComplete = "jobStageComplete"
    ex__JobError = "jobStageError"
    ex__JobRunning = "jobStageRunning"
    ex__JobRejected = "jobStageRejected"
    ex__getJob = "getJob"
    ex__getJobData = "getJobData"
    ex__setJobData = "setJobData"
    ex__setStage = "setStage"
    ex__getWeather = "getWeather"
    ex__sendCSVToPortal = "sendCSVToPortal"
    ex__setEquipmentVariableValue = "setEquipmentVariable"
    ex__getEquipmentVariableValue = "getEquipmentVariable"

    ex__getReportData = "getReport"

    slackEndpoint = "https://slack.com/api/chat.postMessage"

    # Constructor - assign credentials
    def __init__(
        self,
        username="",
        password="",
        useProductionApi=True,
        token=None,
        database="default",
    ):
        if token is not None:
            self.authorizationToken = token
        else:
            self.username = username
            self.password = password
            self.authorizationToken = None

        if useProductionApi:
            self.useProductionApi()
        else:
            self.useStagingApi()

        self.database = database

    def usePreProductionDatabase(self):
        self.database = "pre-production"

    def useDefaultDatabase(self):
        self.database = "default"

    def sendSlackMessage(self, text="", channel="bigredbutton"):
        SLACK_TOKEN = os.getenv("SLACK_TOKEN")
        if not SLACK_TOKEN:
            raise Exception("SLACK_TOKEN not found in environment variables!")
        msg = "[{}] {}".format(self.mode, text)
        if self.mode == "staging":
            channel = "{}-staging".format(channel)
        url = "{}".format(self.slackEndpoint, channel, msg)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "Connection": "keepalive",
            "Authorization": "Bearer {}".format(SLACK_TOKEN),
        }
        body = {"channel": channel, "text": msg, "as_user": "bigredbutton"}
        requests.post(self.slackEndpoint, json=body, headers=headers)

    def getTimeNow(self, timestampFormat: str = "%Y_%m_%d_%H%M") -> str:
        """Returns the current date and time in Melbourne the format 'YYYY_MM_DD_HHMM'.

        Returns:
            str: A string representing the current date and time in Melbourne.
        """
        now = datetime.now().astimezone(tz=timezone('Australia/Melbourne'))
        dt_string = now.strftime(timestampFormat)
        return dt_string

    def sendSlackJobUpdate(self, message: str, success: bool, jobId: Union[int, str], module: str, channel: str = "bigredbutton", moduleIcon: str = "", jobType: str = "", bCode: str = "", moduleVersion: str = ""):
        """Creates and sends a formatted message string to Slack channel.

        Args:
            message (str): The message to be sent to a Slack channel.
            success (bool): The job success status.
            jobId (Union[int, str]): The job ID.
            module (str): The module name.
            channel (str, optional): The channel code. Defaults to "bigredbutton".
            moduleIcon (str, optional): The module icon. Defaults to "".
            jobType (str, optional): The type of job. (ex, mv, rw) Defaults to "".
            bCode (str, optional): The building code associated with the job.. Defaults to "".
            moduleVersion (str, optional): The version of module. Defaults to "".

        """
        timestamp = self.getTimeNow(timestampFormat='%d/%m/%Y %H:%M')

        if success:
            status = 'COMPLETED'
            statusIcon = ':white_check_mark:'
        else:
            status = 'FAILED'
            statusIcon = ':x:'

        if moduleVersion:
            moduleVersion = 'v' + moduleVersion

        msg = f'Module: *{module}* {moduleVersion} {moduleIcon}\nStatus: *{status}* {statusIcon}\nJob ID: *{jobId}*\t||\tB-Code: {bCode}\t||\tJob Type: {jobType}\nTime: {timestamp}\n{message}'
        self.sendSlackMessage(text=msg, channel=channel)

        return

    def useProductionApi(self):
        self.mode = "production"

    def useStagingApi(self):
        self.mode = "staging"

    def getExchangeEndpoint(self):
        if self.mode == "production":
            return self.exchangeEndpointProduction
        return self.exchangeEndpointStaging

    # function: doRequest
    # make a request to the endpoint, returning the json body and status code as a tuple.
    def doRequest(self, endpoint, activity, body):
        # print(self.getActivityUrl(endpoint, activity))
        request = requests.post(
            self.getActivityUrl(endpoint, activity),
            json=body,
            headers=self.getHeaders(),
        )
        self.resetCounter()
        return request.status_code, request.json()

    def getWhoAmI(self):
        return "component={};mode={};user={};database={}".format(
            self.componentId, self.mode, self.username, self.database
        )

    def setComponentName(self, componentName):
        self.componentId = componentName

    # function: getHeaders
    # returns a common set of headers each request needs as a minimum or default
    def getHeaders(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "User-Agent": "ExergenicsApi.class.py",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keepalive",
            "apiVersion": str(self.apiVersion),
            "cognitoAuthToken": str(self.authorizationToken),
            "whoAmI": self.getWhoAmI(),
        }

    # function: getActivityUrl
    # combines the base url of the endpoint being accessed with the specific activity to form a complete endpoint
    def getActivityUrl(self, endpoint, activity):
        querystring = "{}/{}".format(endpoint, activity)
        # default database? do no more...
        if self.database == "default":
            return querystring

        # using pre-prod database? tell the api to switch to that on load
        appendage = "?"
        if "?" in querystring:
            appendage = "&"

        return "{}{}{}".format(querystring, appendage, "usePreProductionDatabase=1")

    # function: getBody
    # returns the body element of the last response.
    def getBody(self):
        if self.lastResponse is not None:
            return self.lastResponse["body"]
        return None

    # function: getResponseValue
    # returns the object denoted by a specific 'key' offset from the body of the last response.
    def getResponseValue(self, key):
        if self.getBody() is not None:
            return self.getBody()[key]
        return None

    # function: moreResults
    # does the last response have more results left to show
    def moreResults(self):
        if self.lastStatus != 200:
            return False
        return self.numResults() > self.internalCounter

    # function: nextResult
    def nextResult(self):
        if self.lastResponse is None:
            return None
        if self.lastStatus != 200:
            return None

        packet = self.lastResponse[self.internalCounter]
        self.internalCounter += 1
        return packet

    # function: resetCounter
    # reset the internal counter
    def resetCounter(self):
        self.internalCounter = 0

    # function: numResults
    # the number of results returned from the last api call
    def numResults(self):
        if self.lastResponse is None:
            return 0
        if self.lastStatus != 200:
            return 0
        return len(self.lastResponse)

    """
    ********************************
    Start Endpoint Request Functions
    ********************************
    """

    # function  :   authenticate
    def authenticate(self):
        # attempt token auth
        if self.authorizationToken is not None:
            self.lastStatus, self.lastResponse = self.doRequest(
                self.getExchangeEndpoint(), self.ex__tokenPing, {}
            )
            if self.lastStatus != 200:
                return False
            else:
                return True

        # attempt credential auth
        body = {"username": self.username, "password": self.password}
        self.lastStatus, self.lastResponse = self.doRequest(
            self.authEndpoint, self.auth__getAuthorizationToken, body
        )
        if self.lastResponse is None:
            return False

        if "errorMessage" in self.lastResponse:
            exit("Authentication Error: {}".format(
                self.lastResponse["errorMessage"]))
        if "statusCode" in self.lastResponse:
            if int(self.lastResponse["statusCode"]) != 200:
                exit(
                    "Authentication Error: Status code from server: {}".format(
                        self.lastResponse["statusCode"]
                    )
                )

        self.authorizationToken = self.getResponseValue("authorizationToken")
        if self.authorizationToken is None:
            return False
        return True

    # function  : getBuilding
    # param     : buildingCode
    def getBuildings(self, buildingCode=None):
        activityUrl = self.ex__getBuildings
        if buildingCode is not None:
            activityUrl = "{}?buildingCode={}".format(
                activityUrl, buildingCode)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    # function  : getBuilding
    # param     : buildingCode
    def getWeather(self, buildingCode, distance=20):
        subDomain = "staging"
        if self.mode == "production":
            subDomain = "app"

        req = (
            "https://"
            + subDomain
            + ".exergenicsportal.com/api/ex/index.php?I_AM_LAMBDA=eyJraWQiOiJpRlwvb0dLamdOTjdLMlEwMWNFRndXUkFROWFZWWdKZ3BBZlNOdDJyWWFIQT0iLCJhbGciOiJSUzI1NiJ9&path=/getWeather/"
            + buildingCode
            + '&httpMethod=GET&awsSubscriptionKey=7b786790-6e4e-4310-bfc7-d30aec6beb02&queryStringParameters={"distance":'
            + str(distance)
            + "}&postParams=&whoAmI=getWeatherProduction&"
        )
        request = requests.get(req)
        return request.json()["body"]

    def getReportData(self, jobId):
        activityUrl = "{}/{}".format(self.ex__getReportData, jobId)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return self.lastResponse

    def setEquipmentVariableValue(
        self, plantCode, equipmentTag, variableName, variableValue
    ):
        activityUrl = "{}/{}/{}/?variableName={}&variableValue={}".format(
            self.ex__setEquipmentVariableValue,
            plantCode,
            equipmentTag,
            variableName,
            variableValue,
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return self.lastResponse

    def getEquipmentVariableValue(self, plantCode, equipmentTag, variableName):
        activityUrl = "{}/{}/{}/?variableName={}".format(
            self.ex__getEquipmentVariableValue, plantCode, equipmentTag, variableName
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return self.lastResponse

    def jobLogInfo(self, jobId, message):
        self.jobLog(jobId, "info", message)

    def jobLogWarning(self, jobId, message):
        self.jobLog(jobId, "warn", message)

    def jobLogError(self, jobId, message):
        self.jobLog(jobId, "error", message)

    def jobLogFatal(self, jobId, message):
        self.jobLog(jobId, "fatal", message)

    def jobLog(self, jobId, level, message):
        activityUrl = "{}/{}/{}/?message={}".format(
            self.ex__jobLog, jobId, level, message
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def noResponse(self):
        if self.lastStatus != 200:
            return True
        if self.lastResponse is None:
            return True
        if len(self.lastResponse) == 0:
            return True

    # function  : putFiles
    # param     : plantCode, urlToFile, category, name, equipCode
    def putFile(self, plantCode, urlToFile, category, name, equipCode="", jobId=""):
        activityUrl = (
            "{}/{}/?urlToFile={}&category={}&name={}&equipCode={}&jobId={}".format(
                self.ex__putFile,
                plantCode,
                urllib.parse.quote(urlToFile),
                urllib.parse.quote(category),
                urllib.parse.quote(name),
                urllib.parse.quote(equipCode),
                urllib.parse.quote(jobId),
            )
        )

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    # function  : linkTable
    # param     : plantCode, tableName, category
    def linkTable(self, plantCode, tableName, category):
        activityUrl = "{}/{}/?tableName={}&category={}".format(
            self.ex__linkTable,
            plantCode,
            urllib.parse.quote(tableName),
            urllib.parse.quote(category),
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    # function  : getFiles
    # param     : plantCode
    def getFiles(self, plantCode, category=None, equipCode="", jobId=""):
        if category is not None:
            activityUrl = "{}/{}?category={}&equipCode={}&jobId={}".format(
                self.ex__getFiles, plantCode, category, equipCode, jobId
            )
        else:
            activityUrl = "{}/{}?equipCode={}&jobId={}".format(
                self.ex__getFiles, plantCode, equipCode, jobId
            )

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    # function  : deleteFiles
    # param     : plantCode
    # param     : category
    def deleteFiles(self, plantCode, category, equipCode=""):
        if category is not None:
            activityUrl = "{}/{}?category={}&equipCode={}".format(
                self.ex__deleteFiles, plantCode, category, equipCode
            )
        else:
            activityUrl = "{}/{}?equipCode={}".format(
                self.ex__deleteFiles, plantCode, equipCode
            )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    # function  : putData
    # param     : code (any valid code)
    # param     : fieldName
    # param     : value
    def putData(self, code, fieldName, value):
        sendAs = value
        if isinstance(value, list):
            sendAs = json.dumps(value)

        activityUrl = "{}/{}?field={}&value={}".format(
            self.ex__putData, code, fieldName, sendAs
        )

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def sendCSVToPortal(self, jobId):
        activityUrl = "{}/{}".format(self.ex__sendCSVToPortal, jobId)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False

        return True

    # function  : getData
    # param     : code (any valid code)
    # param     : fieldName
    # param     : value
    def getData(self, code, fieldName):
        activityUrl = "{}/{}?field={}".format(
            self.ex__getData, code, fieldName)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False

        if (
            self.lastResponse["value"][0] == "["
            and self.lastResponse["value"][-1] == "]"
        ):
            return json.loads(self.lastResponse["value"])
        return self.lastResponse["value"]

    # function  : getKeyData
    # param     : code (any valid code)
    # returns all key data associated with a building (currently contacts, files, dates, urls)
    def getKeyData(self, code):
        activityUrl = "{}/{}".format(self.ex__getKeyData, code)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )

        # this endpoint comes in as a json dict, api handler expects array, so cast as array.
        self.lastResponse = [self.lastResponse]

        if self.noResponse():
            return False
        return True

    # function  : getAllData
    # param     : code (any valid code)
    def getAllData(self, code):
        allData = {}
        activityUrl = "{}/{}".format(self.ex__getAllData, code)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        while self.moreResults():
            packet = self.nextResult()
            if len(packet["value"]) == 0:
                allData[packet["field"]] = ""
            else:
                if packet["value"][0] == "[" and packet["value"][-1] == "]":
                    allData[packet["field"]] = json.loads(packet["value"])
                else:
                    allData[packet["field"]] = packet["value"]
        return allData

    # function  : clearData
    # param     : code
    # param     : field
    def clearData(self, code, field=None):
        if field is not None:
            activityUrl = "{}/{}?field={}".format(
                self.ex__clearData, code, field)
        else:
            activityUrl = "{}/{}".format(self.ex__clearData, code)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    # function  : getTreeData
    # param     : treeTag
    def getTreeData(self, treeTag):
        activityUrl = "{}/{}".format(self.ex__getTreeData, treeTag)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def sendToBucket(self, localFile, contentType="text/csv"):
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
            raise Exception(
                "AWS credentials not found in environment variables!")

        # create a new name for this file
        client = boto3.client(
            "s3",
            region_name="ap-southeast-2",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        today = date.today()

        extraArgs = {"ContentType": contentType}
        if (
            localFile.endswith(".html")
            or contentType == "text/html"
            or contentType == "html"
        ):
            extraArgs = {"ContentType": "text/html",
                         "ContentDisposition": "inline"}
        saveAs = "{}/{}/{}/{}__{}".format(
            today.year, today.month, today.day, uuid.uuid4().hex, localFile
        )
        client.upload_file(
            Filename=localFile,
            Bucket=self.aws_bucketName,
            Key=saveAs,
            ExtraArgs=extraArgs,
        )
        return "{}{}".format(self.aws_bucketRoot, saveAs)

    def getJobs(self, stage, status="completed"):
        activityUrl = "{}/{}/{}".format(self.ex__getJobs, stage, status)

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )

        if self.noResponse():
            return False
        return True

    def getJobData(self, jobId, fieldName):
        activityUrl = "{}/{}/?fieldName={}".format(
            self.ex__getJobData, jobId, fieldName
        )

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return self.lastResponse["value"]

    def getAutoDataRefreshJobs(self, date):
        activityUrl = "{}?date={}".format(
            self.ex__getAutoDataRefreshJobs, date)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def getJobsByPlant(self, plantCode):
        activityUrl = "{}/{}".format(self.ex__getPlantJobs, plantCode)

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )

        if self.noResponse():
            return False
        return True

    def setStage(self, jobId, stage, status):
        activityUrl = "{}/{}/{}/{}".format(self.ex__setStage,
                                           jobId, stage, status)

        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )

        if self.noResponse():
            return False
        return True

    def setJobStageComplete(self, jobId):
        activityUrl = "{}/{}".format(self.ex__JobComplete, jobId)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def setJobStageError(self, jobId, errorMessage=None):
        if not errorMessage:
            errorMessage = "No error details were provided"
        activityUrl = "{}/{}?errorMessage={}".format(
            self.ex__JobError, jobId, errorMessage
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def setJobStageRejected(self, jobId, rejectedMessage=None):
        if not rejectedMessage:
            rejectedMessage = "No rejection details were provided"
        activityUrl = "{}/{}?rejectedMessage={}".format(
            self.ex__JobRejected, jobId, rejectedMessage
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def setJobStageRunning(self, jobId, errorMessage=None):
        if not errorMessage:
            errorMessage = "No error details were provided"
        activityUrl = "{}/{}?errorMessage={}".format(
            self.ex__JobRunning, jobId, errorMessage
        )
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def getJob(self, jobId):
        activityUrl = "{}/{}".format(self.ex__getJob, jobId)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(), activityUrl, {}
        )
        if self.noResponse():
            return False
        return True

    def setJobData(self, jobId, fieldName, fieldValue):
        activityUrl = "{}/{}".format(self.ex__setJobData, jobId)
        self.lastStatus, self.lastResponse = self.doRequest(
            self.getExchangeEndpoint(),
            activityUrl,
            {"fieldName": fieldName, "fieldValue": fieldValue},
        )
        if self.noResponse():
            return False
        return True

    def plotlyRequest(
        self, chartType="linechart", params=None, returnValue="urlToLineChart"
    ):
        if params is None:
            params = {}
        getRequest = "?"
        for key in params:
            getRequest = getRequest + "{}={}&".format(key, params[key])
        endpoint = self.plotlyEndpoint.format(
            chartType, getRequest.replace(" ", "%20"))
        request = requests.get(url=endpoint)
        return request.json()[returnValue]

    """
    example csv: http://exergenics-public.s3.ap-southeast-2.amazonaws.com/2021/12/14/df8c76a12b316b4cf67e909524f74395___test-chart.csv
    http://djago-env.eba-ywiepmh3.us-west-2.elasticbeanstalk.com/linechart/?title=Chart Title&xAxisTitle=xAxisTitle&yAxisTitle=yAxisTitle&legendTitle=legendTitle&chartWidth=800&chartHeight=600&url2csv=https://exergenics-public.s3.ap-southeast-2.amazonaws.com/2022/3/4/c85e47fc33404edd89ffb31f449d4046__/tmp/data.csv&

    example get request
    http://djago-env.eba-ywiepmh3.us-west-2.elasticbeanstalk.com/linechart/?legendTitle=legend title here&width=800&height=600&title=Chart Title Here&url2csv=http://exergenics-public.s3.ap-southeast-2.amazonaws.com/2021/12/14/df8c76a12b316b4cf67e909524f74395___test-chart.csv
    """

    def plotlyLineChart(
        self,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)
        return self.plotlyRequest(
            "linechart",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "outputType": outputType,
            },
        )

    def portalChart_lineChart(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyLineChart(
            dataFrame,
            title,
            xAxisTitle,
            yAxisTitle,
            outputType,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyBarChart(
        self,
        dataFrame,
        legendTitle,
        chartWidth,
        chartHeight,
        backgroundColor,
        fontSize,
        fontFamily,
        fontColor,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        titleFont,
        titleColor,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)
        return self.plotlyRequest(
            "barchart",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "outputType": outputType,
            },
            "urlToBarChart",
        )

    def portalChart_barChart(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        legendTitle,
        chartWidth,
        chartHeight,
        backgroundColor,
        fontSize,
        fontFamily,
        fontColor,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        titleFont,
        titleColor,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyBarChart(
            dataFrame,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
            title,
            xAxisTitle,
            yAxisTitle,
            outputType,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyRadarChart(
        self,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)
        return self.plotlyRequest(
            "radarchart",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "outputType": outputType,
            },
            "urlToRadarChart",
        )

    def portalChart_radarChart(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyRadarChart(
            dataFrame,
            title,
            xAxisTitle,
            yAxisTitle,
            outputType,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyScatterPlot(
        self,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)
        return self.plotlyRequest(
            "scatterplot",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "outputType": outputType,
            },
            "urlToScatterPlotChart",
        )

    def portalChart_scatterPlot(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyScatterPlot(
            dataFrame,
            title,
            xAxisTitle,
            yAxisTitle,
            outputType,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyStackedBarGraph(
        self,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)
        return self.plotlyRequest(
            "stackedbargraph",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "outputType": outputType,
            },
            "urlToStackedBarChart",
        )

    def portalChart_stackedbarGraph(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyStackedBarGraph(
            dataFrame,
            title,
            xAxisTitle,
            yAxisTitle,
            outputType,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyHistogram(
        self,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)
        return self.plotlyRequest(
            "histogram",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "outputType": outputType,
            },
            "urlToHistogram",
        )

    def portalChart_histogram(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyHistogram(
            dataFrame,
            title,
            xAxisTitle,
            yAxisTitle,
            outputType,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlySurfacePlot(
        self,
        dataFrame,
        lift,
        load,
        cop,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        zAxisTitle="zAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        tmpFile = "/tmp/data.csv"
        dataFrame.to_csv(tmpFile, index=False, index_label=False)

        tmpLift = "/tmp/lift.csv"
        lift.to_csv(tmpLift, index=False, index_label=False)

        tmpLoad = "/tmp/load.csv"
        load.to_csv(tmpLoad, index=False, index_label=False)

        tmpCop = "/tmp/cop.csv"
        cop.to_csv(tmpCop, index=False, index_label=False)

        return self.plotlyRequest(
            "surfaceplot",
            {
                "title": title,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "zAxisTitle": zAxisTitle,
                "legendTitle": legendTitle,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "url2csv": self.sendToBucket(tmpFile),
                "backgroundColor": backgroundColor,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
                "liftcsv": self.sendToBucket(tmpLift),
                "loadcsv": self.sendToBucket(tmpLoad),
                "copcsv": self.sendToBucket(tmpCop),
                "outputType": outputType,
            },
            "urlToSurfacePlot",
        )

    def portalChart_surfacePlot(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataFrame,
        lift,
        load,
        cop,
        title="title",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        zAxisTitle="zAxisTitle",
        outputType="html",
        legendTitle="legendTitle",
        chartWidth=800,
        chartHeight=600,
        backgroundColor="white",
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlySurfacePlot(
            dataFrame,
            lift,
            load,
            cop,
            title,
            xAxisTitle,
            yAxisTitle,
            zAxisTitle,
            outputType,
            legendTitle,
            chartWidth,
            chartHeight,
            backgroundColor,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyBowlChart2D(
        self,
        data,
        optimalPointX="optimalPointX",
        optimalPointY="optimalPointY",
        title="title",
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        yAxis2Title="yAxis2Title",
        outputType="html",
        backgroundColor="white",
        chartWidth=800,
        chartHeight=600,
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        return self.plotlyRequest(
            "bowlchart2D",
            {
                "dataCSV": data,
                "optimalPointX": optimalPointX,
                "optimalPointY": optimalPointY,
                "title": title,
                "legendTitle": legendTitle,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "yAxis2Title": yAxis2Title,
                "outputType": outputType,
                "backgroundColor": backgroundColor,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
            },
            "urlToBowlChart2D",
        )

    def portalChart_bowlChart2D(
        self,
        plantCode,
        chartName,
        portalCategory,
        data,
        optimalPointX="optimalPointX",
        optimalPointY="optimalPointY",
        title="title",
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        yAxis2Title="yAxis2Title",
        outputType="html",
        backgroundColor="white",
        chartWidth=800,
        chartHeight=600,
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyBowlChart2D(
            data,
            optimalPointX,
            optimalPointY,
            title,
            legendTitle,
            xAxisTitle,
            yAxisTitle,
            yAxis2Title,
            outputType,
            backgroundColor,
            chartWidth,
            chartHeight,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyBowlChart3D(
        self,
        point,
        x,
        y,
        z,
        title="title",
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        zAxisTitle="zAxisTitle",
        outputType="html",
        backgroundColor="white",
        chartWidth=800,
        chartHeight=600,
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
    ):
        return self.plotlyRequest(
            "bowlchart3D",
            {
                "pointCSV": point,
                "xCSV": x,
                "yCSV": y,
                "zCSV": z,
                "title": title,
                "legendTitle": legendTitle,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "zAxisTitle": zAxisTitle,
                "outputType": outputType,
                "backgroundColor": backgroundColor,
                "chartWidth": chartWidth,
                "chartHeight": chartHeight,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
            },
            "urlToBowlChart3D",
        )

    def portalChart_bowlChart3D(
        self,
        plantCode,
        chartName,
        portalCategory,
        point,
        x,
        y,
        z,
        title="title",
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        zAxisTitle="zAxisTitle",
        outputType="html",
        backgroundColor="white",
        chartWidth=800,
        chartHeight=600,
        fontSize=12,
        fontFamily="TimesNewRoman",
        fontColor="black",
        legendFamily="Courier",
        legendSize=12,
        legendColor="black",
        legendBg="LightSteelBlue",
        titleFont="Arial",
        titleColor="black",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyBowlChart3D(
            point,
            x,
            y,
            z,
            title,
            legendTitle,
            xAxisTitle,
            yAxisTitle,
            zAxisTitle,
            outputType,
            backgroundColor,
            chartWidth,
            chartHeight,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyDynamicBowlChart2D(
        self,
        data,
        backgroundColor,
        width,
        height,
        fontSize,
        fontFamily,
        fontColor,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        titleFont,
        titleColor,
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        yAxis2Title="yAxis2Title",
        outputType="html",
    ):
        return self.plotlyRequest(
            "dynamicbowlchart2D",
            {
                "dataJSON": data,
                "legendTitle": legendTitle,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "yAxis2Title": yAxis2Title,
                "outputType": outputType,
                "backgroundColor": backgroundColor,
                "width": width,
                "height": height,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
            },
            "urlToDynamicBowlChart2D",
        )

    def portalChart_dynamicBowlChart2D(
        self,
        plantCode,
        chartName,
        portalCategory,
        data,
        backgroundColor,
        width,
        height,
        fontSize,
        fontFamily,
        fontColor,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        titleFont,
        titleColor,
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        yAxis2Title="yAxis2Title",
        outputType="html",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyDynamicBowlChart2D(
            data,
            backgroundColor,
            width,
            height,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
            legendTitle,
            xAxisTitle,
            yAxisTitle,
            yAxis2Title,
            outputType,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyDynamicBarChart2D(
        self,
        data,
        backgroundColor,
        width,
        height,
        fontSize,
        fontFamily,
        fontColor,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        titleFont,
        titleColor,
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
    ):
        return self.plotlyRequest(
            "dynamicbarchart2D",
            {
                "dataJSON": data,
                "legendTitle": legendTitle,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "outputType": outputType,
                "backgroundColor": backgroundColor,
                "width": width,
                "height": height,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
                "titleFont": titleFont,
                "titleColor": titleColor,
            },
            "urlToDynamicBarChart2D",
        )

    def portalChart_dynamicBarChart2D(
        self,
        plantCode,
        chartName,
        portalCategory,
        data,
        backgroundColor,
        width,
        height,
        fontSize,
        fontFamily,
        fontColor,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        titleFont,
        titleColor,
        legendTitle="legendTitle",
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        outputType="html",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyDynamicBarChart2D(
            data,
            backgroundColor,
            width,
            height,
            fontSize,
            fontFamily,
            fontColor,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            titleFont,
            titleColor,
            legendTitle,
            xAxisTitle,
            yAxisTitle,
            outputType,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def portalChart_generalised3D(
        self,
        plantCode,
        chartName,
        portalCategory,
        dataJSON,
        markerSize,
        backgroundColor,
        width,
        height,
        fontSize,
        fontFamily,
        fontColor,
        legendPosition,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        zAxisTitle="zAxisTitle",
        fileName="fileName",
        equipCode="",
        jobId="",
    ):
        urlToChart = self.plotlyGeneralised3D(
            dataJSON,
            markerSize,
            backgroundColor,
            width,
            height,
            fontSize,
            fontFamily,
            fontColor,
            legendPosition,
            legendFamily,
            legendSize,
            legendColor,
            legendBg,
            xAxisTitle,
            yAxisTitle,
            zAxisTitle,
            fileName,
        )
        self.putFile(plantCode, urlToChart, portalCategory,
                     chartName, equipCode, jobId)
        return urlToChart

    def plotlyGeneralised3D(
        self,
        dataJSON,
        markerSize,
        backgroundColor,
        width,
        height,
        fontSize,
        fontFamily,
        fontColor,
        legendPosition,
        legendFamily,
        legendSize,
        legendColor,
        legendBg,
        xAxisTitle="xAxisTitle",
        yAxisTitle="yAxisTitle",
        zAxisTitle="zAxisTitle",
        fileName="fileName",
    ):
        return self.plotlyRequest(
            "generalised3D",
            {
                "dataJSON": dataJSON,
                "xAxisTitle": xAxisTitle,
                "yAxisTitle": yAxisTitle,
                "zAxisTitle": zAxisTitle,
                "fileName": fileName,
                "markerSize": markerSize,
                "backgroundColor": backgroundColor,
                "width": width,
                "height": height,
                "fontSize": fontSize,
                "fontFamily": fontFamily,
                "fontColor": fontColor,
                "legendPosition": legendPosition,
                "legendFamily": legendFamily,
                "legendSize": legendSize,
                "legendColor": legendColor,
                "legendBg": legendBg,
            },
            "urlToGeneralised3D",
        )


"""
*****************************
ExergenicsLogger.class.py
*****************************

N.WONG FEB 2023
Implements exergenics internal application logging by providing a Logtail interface
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ExergenicsLogger(metaclass=Singleton):
    """Exergenics Logger class to send structured logs directly to https://logtail.com/.

    The Exergenics Logger is built using the Python Singleton pattern and only needed to be initialised
    once and the same instance will be reused throughout the module. To start using the Logger,
    initialise once by providing __init__() arguments and subsequent inovation
    arguments.

    HOW TO USE ExergenicsLogger

    In main function:

    from exergenics import exergenics
    logger = exergenics.ExergenicsLogger('loggerName', 'component', 'subcomponent', 'jobId', 'environment')

    from exergenics import exergenics.ExergenicsLogger as Logger
    logger = Logger('loggerName', 'component', 'subcomponent', 'jobId', 'environment')

    In sub-functions:

    logger = Logger()
    logger.info('message')

    """

    def __init__(
        self,
        loggerName: str,
        component: str = "",
        subComponent: str = "",
        jobId: str = "",
        environment: str = "",
    ):
        """Initialise the logger object

        Parameters
        ----------
        loggerName : str
            Logger name in string format.
        component : str
            Component name in string format.
        subComponent : str
            Sub-component name in string format.
        jobId : str
            Job ID in string format.
        environment : str
            Database environment in string format.
        """
        # Exergenics Logger version number
        self._version = 1.0

        # Configure logtail API key
        API_KEY = os.getenv("LOGTAIL_API_KEY")
        if not API_KEY:
            raise Exception(
                "LOGTAIL_API_KEY not found in environment variables!")

        # Configure logtail logging
        self._handler = LogtailHandler(source_token=API_KEY)
        self._logger = logging.getLogger(loggerName)
        self._logger.handlers = []
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._handler)

        # Custom field to allow filtering
        self._extra = {
            "component": component,
            "sub_component": subComponent,
            "job_id": jobId,
            "environment": environment,
        }

    def _setFunctionName(self) -> None:
        """Retrieve function name from stack and add to logtail _extra field.

        Returns
        -------
        None
        """
        functionName = inspect.stack()[2][3]
        self._extra["function"] = functionName

        return None

    def debug(self, message: str) -> None:
        """Send logs with DEBUG level.

        Parameters
        ----------
        message : str
            Debug log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.debug(message, extra=self._extra)
        return None

    def info(self, message: str) -> None:
        """Send logs with INFO level.

        Parameter
        ---------
        message : str
            Info log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.info(message, extra=self._extra)
        return None

    def warn(self, message: str) -> None:
        """Send logs with WARN level.

        Parameter
        ---------
        message : str
            Warning log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.warning(message, extra=self._extra)
        return None

    def error(self, message: str) -> None:
        """Send logs with ERROR level.

        Parameter
        ---------
        message : str
            Error log message in string format.

        Returns
        -------
        None
        """
        self._setFunctionName()
        self._logger.error(message, extra=self._extra)
        return None

    def getVersion(self) -> str:
        """Get current Exergenic Logger version number.

        Returns
        -------
        str
            Logger version in string
        """
        return str(self._version)


class FeatureToggle:
    """ This class communicate with Exergenics Portal API and fetch feature toggle
    flag for local, staging and production environment. Requires ExergenicsAPI python 
    class. 
    """

    def __init__(self, environment: str):
        """

        Args:
            environment (str): Environment parameter only accepts the following
            possible values: local, staging, production
        """
        if environment not in ['local', 'staging', 'production']:
            raise ValueError(
                'Environment parameter should only be either "local", "staging", or "production"')
        self.environment = environment
        self.api = self._loadAPI()
        self.features = self._loadFeatures()

    def _loadAPI(self):
        api_username = os.getenv('EXERGENICS_API_USERNAME')
        api_password = os.getenv('EXERGENICS_API_PASSWORD')
        api = ExergenicsApi(api_username, api_password, "production")
        if not api.authenticate():
            print("Could not authenticate using credentials supplied.")
            exit(0)
        return api

    def _loadFeatures(self) -> dict:
        features = {}
        self.api.getTreeData('t_feature_toggle')
        while self.api.moreResults():
            feature = self.api.nextResult()
            features[feature['ontology']] = {'local': True if (feature['fields'][1]['fieldValue'] == 'On') else False,
                                             'staging': True if (feature['fields'][2]['fieldValue'] == 'On') else False,
                                             'production': True if (feature['fields'][3]['fieldValue'] == 'On') else False}
        return features

    def _refetchToggle(self) -> None:
        self.features = self._loadFeatures()
        return

    def listFeatures(self) -> list:
        """Return a list of features that contains toggles

        Returns:
            list: List of valid features.
        """
        return list(self.features.keys())

    def isEnabled(self, feature: str) -> bool:
        """Returns flag for whether a specific feature is enabled for the given environment

        Args:
            feature (str): Feature tag in Jira Git branching format.

        Raises:
            ValueError: Error when feature provided is not found in database.

        Returns:
            bool: Feature is enabled. 
        """
        if feature not in self.features.keys():
            raise ValueError("Could not identify feature.")

        return self.features[feature][self.environment]
