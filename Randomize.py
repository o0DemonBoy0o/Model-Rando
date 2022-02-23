import sys
import json
import random

#Functions to write stuff
def writemodel(old,new):
    #MDLX (Avoid conflict with Wisdom Form)
    f.write('- name: obj/'+old+'.mdlx\n  method: binarc\n  source:\n')
    if objtype != 'Enemy':
        subfile = old[:4].lower()
        f.write('  - name: '+subfile+'\n    type: model\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.model\n') #Model
    f.write('  - name: tim_\n    type: modeltexture\n    method: copy\n    source:\n'+
            '    - name: obj/'+new+'.tim\n') #Texture
    #A.FM
    if objtype == 'Party':
        f.write('- name: obj/'+old+'.a.fm\n  method: binarc\n  source:\n')
        f.write('  - name: face\n    type: imgd\n    method: copy\n    source:\n'+
                '    - name: obj/'+new+'.imd\n') #Portrait
        f.write('  - name: face\n    type: seqd\n    method: copy\n    source:\n'+
                '    - name: obj/'+new+'.sqd\n') #Portrait Location
    elif objtype == 'Weapon':
        f.write('- name: obj/'+old+'.a.fm\n  method: copy\n  source:\n'+
                '  - name: obj/'+new+'.a.fm\n') #Particle & Sound Effect

def randomodel(oldmodel):
    global subfile
    newmodel = random.sample(oldmodel,len(oldmodel))
    for i in range(len(oldmodel)):
        subfile = oldmodel[i][:4].lower()
        writemodel(oldmodel[i],newmodel[i])

#Get KH2 model filenames
currentDir = sys.argv[0].replace((sys.argv[0].split('\\')[-1]),'')
objs = json.load(open(currentDir+'modellist.json'))
objsextra = json.load(open(currentDir+'modellistextra.json'))

#Write the mod.yml
f = open(currentDir+'mod.yml','w',encoding='utf-8')
f.write('description: Credits for PandaPyre for Final MiXaV Retexture\n')
f.write('assets:\n')
for objtype in objs:
    obj = objs[objtype]
    for models in obj:
        oldmodels = objs[objtype][models]
        newmodels = oldmodels + objsextra[objtype][models]
        random.shuffle(newmodels)
        for i in range(len(oldmodels)):
            writemodel(oldmodels[i],newmodels[i])

f.close()
