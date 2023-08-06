import time
import requests
import json
import threading
import socket

class PERFORMANCE_TEST:
    argumentsValue = {'shouldMeasure':False}
    actionsBeforeCalculation ={}
    calculatedActions ={}
    calculatedActionsPublish =[]
    execution_start_time=0
    execution_end_time=0#time.time()
    uniqueRandom = "224335oho"
    actionPoints = 0
    lock=threading.Lock()

    @staticmethod
    def Start(measure):
            if(measure):
                try:
                    PERFORMANCE_TEST.clearResult()
                    PERFORMANCE_TEST.resolveArguments(measure)
                    PERFORMANCE_TEST.execution_start_time = round(time.time() * 1000)
                except:
                    PERFORMANCE_TEST.clearResult()
            else:
                PERFORMANCE_TEST.argumentsValue = {'shouldMeasure':False}
    
    @staticmethod
    def Stop(publish=False,apiKey = "",version = "",machineName = ""):
        try:
            if (PERFORMANCE_TEST.argumentsValue['shouldMeasure']):
                if (len(PERFORMANCE_TEST.actionsBeforeCalculation) == 0):
                    PERFORMANCE_TEST.clearResult()
                    return []
                PERFORMANCE_TEST.execution_end_time = round(time.time() * 1000)
                PERFORMANCE_TEST.argumentsValue['publish'] = publish
                PERFORMANCE_TEST.calculateActions()
                if (publish):
                    if (version != ""):
                        PERFORMANCE_TEST.argumentsValue['appVersion'] = version
                    else:
                        PERFORMANCE_TEST.argumentsValue['appVersion'] = "1.0"

                    if (machineName != ""):
                        PERFORMANCE_TEST.argumentsValue['machineName'] = machineName
                    else:
                        try:
                            import os
                            PERFORMANCE_TEST.argumentsValue['machineName'] = socket.gethostname()
                        except:
                            PERFORMANCE_TEST.argumentsValue['machineName'] = "Unknown"
                    pub = PERFORMANCE_TEST.publishResult(apiKey)
                    if (pub):
                        return PERFORMANCE_TEST.calculatedActions
                    else:
                        return []
                else:
                    PERFORMANCE_TEST.argumentsValue['shouldMeasure'] = False
                    return PERFORMANCE_TEST.calculatedActions
        except Exception as e:
            PERFORMANCE_TEST.clearResult()
        return []

    @staticmethod
    def ActionStart(name, additionalInfo = "", uniqueIdentifier = ""):
        try:
            if(PERFORMANCE_TEST.argumentsValue['shouldMeasure'] and PERFORMANCE_TEST.actionPoints < 200):
                if(uniqueIdentifier==""):
                    uniqueIdentifier=threading.current_thread().name
                PERFORMANCE_TEST.writeToActionsBeforeCalculation(
                    "start",
                    name,
                    additionalInfo,
                    uniqueIdentifier
                )
        except Exception as e:
            PERFORMANCE_TEST.clearResult()
    
    @staticmethod
    def ActionEnd(name, additionalInfo = "", uniqueIdentifier = ""):
        try:
            if (PERFORMANCE_TEST.argumentsValue['shouldMeasure'] and PERFORMANCE_TEST.actionPoints < 200):
                if(uniqueIdentifier==""):
                    uniqueIdentifier=threading.current_thread().name
                PERFORMANCE_TEST.writeToActionsBeforeCalculation("end", name, additionalInfo, uniqueIdentifier)
        except:
            PERFORMANCE_TEST.clearResult()
    
    @staticmethod
    def publishResult(apiKey):
        url = 'https://api.perfole.com/library/execution'

        executionResult = ExecutionPrivate(machineName = PERFORMANCE_TEST.argumentsValue['machineName'],
                                           startTime = PERFORMANCE_TEST.execution_start_time,
                                           publishTime = PERFORMANCE_TEST.execution_end_time,
                                           duration = PERFORMANCE_TEST.execution_end_time - PERFORMANCE_TEST.execution_start_time,
                                           actions = PERFORMANCE_TEST.calculatedActions,
                                           versionValue = PERFORMANCE_TEST.argumentsValue['appVersion'])
        dataa = requests.post(url, data=json.dumps(executionResult , cls=MyEncoder), headers={'x-api-key': apiKey})
        if(dataa.status_code!=201):
            return False
        else:
            return True

    @staticmethod
    def clearResult():
        PERFORMANCE_TEST.argumentsValue = {}
        PERFORMANCE_TEST.actionsBeforeCalculation ={}
        PERFORMANCE_TEST.calculatedActions ={}
        PERFORMANCE_TEST.calculatedActionsPublish =[]
        PERFORMANCE_TEST.execution_start_time=0
        PERFORMANCE_TEST.execution_end_time=0
        PERFORMANCE_TEST.uniqueRandom = "224335oho"
        PERFORMANCE_TEST.actionPoints = 0

    @staticmethod
    def resolveArguments(measurePerfFromFunction:bool):
        if (measurePerfFromFunction):
            PERFORMANCE_TEST.argumentsValue['shouldMeasure'] = True
        else:
            PERFORMANCE_TEST.argumentsValue['shouldMeasure'] = False
            return False

        return PERFORMANCE_TEST.argumentsValue['shouldMeasure']

    @staticmethod
    def writeToActionsBeforeCalculation(type, actionName, additional_info, unique_identifier):
        currentTime = round(time.time() * 1000)
        actionInfo = Event( tip = type,actionName = actionName,timeVreme = currentTime,unique_identifier = unique_identifier,additional_info = additional_info)
        with PERFORMANCE_TEST.lock:
            if(not actionName in PERFORMANCE_TEST.actionsBeforeCalculation):
                PERFORMANCE_TEST.actionsBeforeCalculation[actionName] = StartEndList([],[])
            if (type == "start"):
                editedStartAction = PERFORMANCE_TEST.actionsBeforeCalculation[actionName].startAction
                editedStartAction.append(actionInfo)
                PERFORMANCE_TEST.actionPoints+=1
            else:
                editedEndAction = PERFORMANCE_TEST.actionsBeforeCalculation[actionName].endAction
                editedEndAction.append(actionInfo)
                PERFORMANCE_TEST.actionPoints+=1

    @staticmethod
    def calculateActions():
        finalLogData = []
 
        for attr, value in PERFORMANCE_TEST.actionsBeforeCalculation.items():
            startActionList = value.startAction
            endActionList = value.endAction

            startActionList.sort(key=lambda x: x.timeVreme, reverse=True)
            endActionList.sort(key=lambda x: x.timeVreme)

            stIdsToRemove = []
            etIdsToRemove = []

            #spajam sa istim ui
            for  eti in endActionList:
                for stId in startActionList:
                    if (eti.unique_identifier == stId.unique_identifier):
                        match = eti
                        endT = match.timeVreme
                        startT = stId.timeVreme
                        doesExistBefore = False
                        for toRemove in etIdsToRemove:
                            if (eti.unique_identifier == toRemove.unique_identifier):
                                if (toRemove.timeVreme > startT):
                                    doesExistBefore=True
                        if (endT > startT and not stId in stIdsToRemove
                            and not match in etIdsToRemove and not doesExistBefore):
                            additional_info = PERFORMANCE_TEST.createadditional_info(stId)
                            additional_info = PERFORMANCE_TEST.createadditional_info(match, additional_info)
                            help = PublishAction(  startTime = stId.timeVreme,
                                endTime = match.timeVreme,
                                duration = match.timeVreme - stId.timeVreme,
                                uniqueIdentifier = stId.unique_identifier,
                                additionalInfo = additional_info,
                                actionName = stId.actionName)
                            stIdsToRemove.append(stId)
                            etIdsToRemove.append(match)
                            finalLogData.append(help)
                            break

            #obrisi spojene akcije sa thredom
            for rem in stIdsToRemove:
                startActionList.remove(rem)

            for rem in etIdsToRemove:
                endActionList.remove(rem)

            # dodaj ostatak nespojenih sa id
            for stime in startActionList:
               # if (not stime.isThreadId):
                PERFORMANCE_TEST.addRemaining(finalLogData, stime, attr)

            for etime in endActionList:
               # if (not etime.isThreadId):
                PERFORMANCE_TEST.addRemaining(finalLogData, etime, attr)
   
        PERFORMANCE_TEST.sortFinalLog(finalLogData)

        PERFORMANCE_TEST.calculatedActions = finalLogData[0:100] if len(finalLogData)>100 else finalLogData
    
    @staticmethod
    def createadditional_info(first, addInfo = ""):
        if (first.tip == "start"):
            addInfo +=  "[" + first.additional_info + "] - " if first.additional_info != "" else ""
        elif (first.tip == "end"):
            if (first.additional_info != "" and addInfo == ""):
                addInfo += "[] - "
            if (first.additional_info == "" and addInfo != ""):
                addInfo += "[]"
            addInfo += "[" + first.additional_info + "]" if first.additional_info != "" else ""
        return addInfo
    
    @staticmethod
    def addRemaining( whereToAdd, actionInfo, action_id):
        addInfo = PERFORMANCE_TEST.createadditional_info(actionInfo)
        help =  PublishAction(uniqueIdentifier = actionInfo.unique_identifier,actionName = actionInfo.actionName,additionalInfo = addInfo)
        if (actionInfo.tip == "start"):
            help.startTime = actionInfo.timeVreme
            help.endTime = 0
            help.additionalInfo = "end event not caught"
        else:
            help.endTime = actionInfo.timeVreme
            help.startTime = 0
            help.additionalInfo = "start event not caught"
        whereToAdd.append(help)
        return whereToAdd

    @staticmethod
    def sortFinalLog(actions):
        actions.sort(key=lambda x: x.startTime if x.startTime>0 else x.endTime)

class Event:
    tip =""
    actionName=""
    timeVreme=0
    unique_identifier=""
    additional_info =""
 
    def __init__(self, tip, actionName, timeVreme, unique_identifier, additional_info):
        self.tip = tip
        self.actionName = actionName
        self.timeVreme=timeVreme
        self.unique_identifier=unique_identifier
        self.additional_info=additional_info


class StartEndList:

    startAction=[]
    endAction=[]
    def __init__(self, startAction, endAction):
        self.startAction=startAction
        self.endAction=endAction

class PerfAction:
    Duration =0
    AdditionalInfo =''
    UniqueIdentifier=''
    Name =''

    def __init__(self, Duration, AdditionalInfo, UniqueIdentifier, Name):
        self.Duration=Duration
        self.AdditionalInfo=AdditionalInfo
        self.UniqueIdentifier=UniqueIdentifier
        self.Name=Name

class ExecutionPrivate:
    startTime=0
    publishTime =0
    machineName =''
    versionValue =''
    duration=0
    actions =[]
    def __init__(self, startTime, publishTime, machineName, versionValue, duration, actions):
        self.startTime=startTime
        self.publishTime=publishTime
        self.machineName=machineName
        self.versionValue=versionValue
        self.duration=duration
        self.actions=actions
    
    def reprJson(self):
        return dict(startTime=self.startTime, publishTime=self.publishTime, machineName=self.machineName, versionValue=self.versionValue, duration=self.duration, actions=self.actions)


class PublishAction:

    actionName=''
    startTime =0
    endTime=0
    duration=0
    additionalInfo =''
    uniqueIdentifier=''

    def __init__(self, actionName, uniqueIdentifier, startTime=0, endTime=0, additionalInfo='', duration=0):
        self.actionName=actionName
        self.startTime=startTime
        self.endTime=endTime
        self.duration=duration
        self.additionalInfo=additionalInfo
        self.uniqueIdentifier=uniqueIdentifier

    def reprJson(self):
        return dict(actionName=self.actionName, startTime=self.startTime, endTime=self.endTime, duration=self.duration, additionalInfo=self.additionalInfo, uniqueIdentifier=self.uniqueIdentifier)

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "reprJson"):
            return o.reprJson()
        else:
            return super().default(o)
