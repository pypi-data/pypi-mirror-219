# infodata' u2python module to work with ..GRAPH... intools 
import sys 
import json 
import msal 

def helloWorld():
     print("hellp from inpython")



def getGraphTokenFromCertificate(path): 
# fonctions pour générer un token Graph avec un certificat
# retourne un objet string json 
# 
# c.f. 
# https://github.com/Azure-Samples/ms-identity-python-daemon/tree/master/2-Call-MsGraph-WithCertificate

     # load config file .json
     # {
     #   "authority": "https://login.microsoftonline.com/infodata.lu",
     #   "tenant_id": "e2a26e34-3...",
     #   "client_id": "15855fc2-...",
     #   "scope": [ "https://graph.microsoft.com/.default" ],
     #   "thumbprint": "9615472D8...",
     #   "private_key_file": "...//9615472D8...//9615472D8....privatekey"
     # }
     
     try:
          f = open(path)
          config = json.load(f)
     except: # catch *all* exceptions
          result = {"errorCode" : "1",
                    "errorFrom" : "json.load({0})".format(path), 
                    "error"     : "{0}".format(sys.exc_info()[0])
                    }
          print(result)
          return json.dumps(result)
     
     # try to connect
     try:
          app = msal.ConfidentialClientApplication(
               config["client_id"], 
               authority=config["authority"],
               client_credential={"thumbprint": config["thumbprint"], 
                              "private_key": open(config['private_key_file']).read()},
               )
     except:
          result = {"errorCode" : "2",
                    "errorFrom" : "msal.ConfidentialClientApplication(authority={authority}, client_credentials=thumbprint={thumbprint}, privatekey={privatekey})".format(authority=config["authority"], thumbprint=config["thumbprint"], privatekey=config['private_key_file']), 
                    "error" : "{0}".format(sys.exc_info()[0])
                    }
          return json.dumps(result)

     # try to get a token
     result = None
     try:
          result = app.acquire_token_for_client(scopes=config["scope"])
     except:
          result = {"errorCode" : "3",
                    "errorFrom" : "app.acquire_token_for_client {scopes}=".format(scopes=config["scope"]) , 
                    "error" : "{0}".format(sys.exc_info()[0])
                    }
          return json.dumps(result)

     return json.dumps(result)
