import time
import requests
import json
import uuid

#constants
RECONIFY_TRACKER = 'https://track.reconify.com/track'
RECONIFY_UPLOADER = 'https://track.reconify.com/upload'
RECONIFY_MODULE_VERSION = '1.0.2'

#private variables 
__appKey = None
__apiKey = None
__debug = False
__tracker = RECONIFY_TRACKER
__uploader = RECONIFY_UPLOADER
__user = {}
__session = ''
__sessionTimeout = ''
__trackImages = True

def __logInteraction(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction')
    payload = {
        "reconify" :{
            "format": 'openai',
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": type,
            "version": RECONIFY_MODULE_VERSION,
        },
        "request": input,
        "response": output,
        "user": __user,
        "session": __session,
        "sessionTimeout": __sessionTimeout,
        "timestamps": {
            "request": timestampIn,
            "response": timestampOut
        },
    }
    if __debug:
        print('Sending payload: ', payload)
    try:
        requests.post(__tracker, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('Send error: ', err)

    return

def __uploadImage(payload):
    if __debug:
        print('uploading image')
    
    try:
        requests.post(__uploader, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('upload error: ', err)
    return

def __logInteractionWithImageData(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction with image data')

    _copy = output.copy()
    n = len(_copy.get('data'))
    filenames = []
    randomId = str(uuid.uuid4())
    for i in range(n):
        filenames.append(f"{randomId}-{_copy.get('created')}-{i}.png")
    _copy['data'] = filenames
    __logInteraction(input, {'data':_copy}, timestampIn, timestampOut, type)

    #send each image
    for i in range(n):
        __uploadImage({
        "reconify" :{
            "format": 'openai',
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": 'image_upload',
            "version": RECONIFY_MODULE_VERSION,
        },
        "upload": {
            "filename": filenames[i],
            "type": 'response-image',
            'data': output.get('data')[i],
            'format': 'b64_json'
        }
        })

    return

def config (openai, appKey, apiKey, **options):
    global __appKey
    global __apiKey
    global __debug
    global __tracker
    global __uploader
    global __user
    global __session
    global __sessionTimeout
    global __trackImages

    __appKey = appKey
    __apiKey = apiKey
    if __appKey is None or __apiKey is None:
        raise Exception('An appKey and apiKey are required')
    #optional overides
    if 'debug' in options and options.get('debug') == True:
        __debug = True

    if 'tracker' in options:
        __tracker = options.get('tracker')

    if 'uploader' in options:
        __uploader = options.get('uploader')

    if 'trackImages' in options and options.get('trackImages') == False:
        __trackImages = False

    #override chat create
    openai.ChatCompletion.originalCreate = openai.ChatCompletion.create
    def __reconifyCreateChatCompletion(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = openai.ChatCompletion.originalCreate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'chat')
        return response 
    openai.ChatCompletion.create = __reconifyCreateChatCompletion 

    #override completion create
    openai.Completion.originalCreate = openai.Completion.create
    def __reconifyCreateCompletion(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = openai.Completion.originalCreate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'completion')
        return response 
    openai.Completion.create = __reconifyCreateCompletion

    #override image create
    openai.Image.originalCreateImage = openai.Image.create
    def __reconifyCreateImage(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = openai.Image.originalCreateImage(*args, **kwargs)
        tsOut = round(time.time()*1000)
        if __trackImages:
            if 'response_format' not in kwargs or kwargs.get('response_format') == 'url':
                __logInteraction(kwargs, response, tsIn, tsOut, 'image')
            else:
                __logInteractionWithImageData(kwargs, response, tsIn, tsOut, 'image')
        
        return response 
    openai.Image.create = __reconifyCreateImage
    return

def setUser(user):
    global __user
    __user = user

def setSession(session):
    global __session
    __session = session

def setSessionTimeout(sessionTimeout):
    global __sessionTimeout
    __sessionTimeout = sessionTimeout