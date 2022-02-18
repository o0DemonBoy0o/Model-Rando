import sys
import json
import random

#Functions to write stuff
def writemodel(old,new):
    #MDLX (Avoid conflict with Wisdom Form)
    f.write('- name: obj/'+old+'.mdlx\n  method: binarc\n  source:\n')
    f.write('  - name: '+subfile+'\n    type: model\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.model\n') #Model
    f.write('  - name: tim_\n    type: modeltexture\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.tim\n') #Texture
    #A.FM
    if old[:4] == 'W_EX':
        f.write('- name: obj/'+old+'.a.fm\n  method: copy\n  source:\n'+
                '  - name: obj/'+new+'.a.fm\n')
        return
    f.write('- name: obj/'+old+'.a.fm\n  method: binarc\n  source:\n')
    f.write('  - name: face\n    type: imgd\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.imd\n') #Portrait
    f.write('  - name: face\n    type: seqd\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.sqd\n') #Portrait Location

def randomodel(oldmodel):
    global subfile
    newmodel = random.sample(oldmodel,len(oldmodel))
    for i in range(len(oldmodel)):
        subfile = oldmodel[i][:4].lower()
        writemodel(oldmodel[i],newmodel[i])

#Get KH2 model filenames
currentDir = sys.argv[0].replace((sys.argv[0].split('\\')[-1]),'')
f = open(currentDir+'modellist.json','r')
models   = json.load(f)
f.close()

#Write the mod.yml
f = open(currentDir+'mod.yml','w',encoding='utf-8')
f.write('assets:\n')
for char in models:
    model = models[char]
    randomodel(model)

f.close()
