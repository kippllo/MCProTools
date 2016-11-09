#MCProTools
#Copyright 2016 Rhett Thompson

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import requests
import base64
import json
import shutil

###can only send one request per minute to Mojang API
username = input("minecraft username:")
r = requests.get("https://api.mojang.com/users/profiles/minecraft/" + username, verify=True)###find out how to add time travel to old skins you used to have, look at Mojang API page here: http://wiki.vg/Mojang_API#UUID_-.3E_Profile_.2B_Skin.2FCape

rJsonData = json.loads(r.text)#Make the text into a dictionary

PlayerInfo = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + rJsonData["id"], verify=True) #Gets the profile info of the player ID
PlayerInfoJsonData = json.loads(PlayerInfo.text)#Makes the PlayerInfo text into a dictionary object


properties = PlayerInfoJsonData["properties"]#makes the "PlayerInfoJsonData"'s entry "properties" into a list
propertiesJsonData = properties[0]#makes the properties's first and only entry into a dictionary #could think of this as propertiesJsonData = json.loads(properties[0]) but the "json.loads" is not necessary because the list entry is alreay a dictionary


valueDecoded = base64.b64decode(propertiesJsonData["value"])# decodes the base64 encoded info(such as the SKIN url) into byte type!!!
valueDecodedUTF8 = valueDecoded.decode("utf-8")#Converts bytes to string


valueDecodedJsonData = json.loads(valueDecodedUTF8)#makes the decoded info into a dictionary

textures = valueDecodedJsonData["textures"]#gets the "textures" sub-dictionary entry from dictionary

SKIN = textures["SKIN"]#gets the "SKIN" sub-dictionary entry from "textures" dictionary

skinURL = SKIN["url"]#Finally gets minecraft user skin url!!!!!!
print("\n"+ "Skin url address: " + skinURL)

skinFile = requests.get(skinURL, verify=True, stream=True) #Downloads skin file

skinFile.raw.decode_content = True #forces it to decompress responses. Source:http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
shutil.copyfileobj(skinFile.raw, open(username + ".png", "wb")) #uses the shutil module to save the file


###P.S. has an error if your skin is set to default
