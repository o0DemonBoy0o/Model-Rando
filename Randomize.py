import sys
import os
import json
import random

#Functions to write stuff
def writemdlx(): #Avoid conflict with Wisdom Form
    f.write('- name: obj/'+old+'.mdlx\n  method: binarc\n  source:\n')
    f.write('  - name: p_ex\n    type: model\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.model\n') #Model
    f.write('  - name: tim_\n    type: modeltexture\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.tim\n') #Texture
def writeafm():
    f.write('- name: obj/'+old+'.a.fm\n  method: binarc\n  source:\n')
    f.write('  - name: face\n    type: imgd\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.imd\n') #Portrait
    f.write('  - name: face\n    type: seqd\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.sqd\n') #Portrait Location

#Get KH2 model filenames
currentDir = sys.argv[0].replace(os.path.basename(__file__),'')
f = open(currentDir+'modellist.json','r')
models   = json.load(f)
oldsora  = models['Sora']
olddolan = models['Donald']
oldgoffy = models['Goofy']
f.close()

newsora  = random.sample(oldsora ,len(oldsora ))
newdolan = random.sample(olddolan,len(olddolan))
newgoffy = random.sample(oldgoffy,len(oldgoffy))

#Write the mod.yml
f = open(currentDir+'mod.yml','w',encoding='utf-8')
f.write('assets:\n')
for i in range(len(oldsora)):
    old = oldsora[i]
    new = newsora[i]
    writemdlx()
    writeafm()
for i in range(len(olddolan)):
    old = olddolan[i]
    new = newdolan[i]
    writemdlx()
    writeafm()
for i in range(len(oldgoffy)):
    old = oldgoffy[i]
    new = newgoffy[i]
    writemdlx()
    writeafm()

f.close()
