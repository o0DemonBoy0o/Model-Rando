import sys, os
import json
import random

#keeping here to look at later
def writemodelOLD(old,new):
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

#Write entries for editing mdlx and adding hd textures
def writemodelFull(oldname,newname,newfile,filedir,hdlist):
    #MDLX (Avoid conflict with Wisdom Form)
    internal = True if filedir == "Extracted" else False
    subfolder = "" 
    if internal:
        subfolder = "obj/"
    
    f.write('- name: obj/'+oldname+'.mdlx\n  method: binarc\n  source:\n')
    subfile = oldname[:4].lower()
    if oldname == 'PO06_PLAYER' or oldname == 'PO07_PLAYER' or oldname == 'PO08_PLAYER' or oldname == 'AL14_PLAYER':
        subfile = 'p_ex'
    f.write('  - name: '+subfile+'\n    type: model\n    method: copy\n    source:\n'+
            '    - name: obj_pc/'+newfile+'.model\n') #Model
    f.write('  - name: tim_\n    type: modeltexture\n    method: copy\n    source:\n'+
            '    - name: obj_pc/'+newfile+'.tim\n') #Texture
    #remastered assets
    for i in range(len(hdlist)):     
        new_file = hdlist[i]
        number = "-"+str(i)+".dds"
        f.write('- method: copy\n  name: remastered/obj/'+oldname+'.mdlx/'+number+'\n  source:\n')
        f.write('  - name: remastered/'+subfolder+newname+'.mdlx/'+new_file+'\n')
        if internal:
            f.write('    type: internal\n')

#write entries for only editing mdlx and use SD textures  
def writemodelOrig(oldname,newfile):
    #MDLX (Avoid conflict with Wisdom Form)
    f.write('- name: obj/'+oldname+'.mdlx\n  method: binarc\n  source:\n')
    subfile = oldname[:4].lower()
    if oldname == 'PO06_PLAYER' or oldname == 'PO07_PLAYER' or oldname == 'PO08_PLAYER' or oldname == 'AL14_PLAYER':
        subfile = 'p_ex'
    f.write('  - name: '+subfile+'\n    type: model\n    method: copy\n    source:\n'+
            '    - name: obj_pc/'+newfile+'.model\n') #Model
    f.write('  - name: tim_\n    type: modeltexture\n    method: copy\n    source:\n'+
            '    - name: obj_pc/'+newfile+'.tim\n') #Texture

#write entries for only raw file replacements (be carful how you use this one)
def writemodelRaw(oldname,newname):
    #MDLX (Avoid conflict with Wisdom Form)
    f.write('- method: copy\n  name: raw/obj/'+oldname+'.mdlx\n  source:\n')
    f.write('  - name: raw/'+newname+'.mdlx\n')

#Get KH2 model filenames
currentDir = sys.argv[0].replace((sys.argv[0].split('\\')[-1]),'')
modellist = json.load(open(currentDir+'modellist_new.json'))

#custom method for getting extra lists. read them from a folder that way you can have multiple different lists. Useful for quicly adding/removing model packs that users may create if desired.
extralists = []
extrasPath = os.path.join(currentDir, "extras")
if os.path.isdir(extrasPath):
    extralists += [d for d in os.listdir(extrasPath) if d.endswith(".json")]

#Write the mod.yml
f = open(currentDir+'mod.yml','w',encoding='utf-8')
f.write('title: Model Rando - PC\n')
f.write('description: Credits to Num for original code. Edits by DA for use on PC Port.\n')
f.write('assets:\n')

#yeah i took quite a bit of inspiration from the seed gen BGM randomizer
for category in modellist:
    for models in modellist[category]:
        shuffledlist = modellist[category][models].copy() #create a copy of model list then shuffle it
        
        for extras in extralists:
            templist = json.load(open(extrasPath+os.sep+extras))
            shuffledlist += templist[category][models]

        print(shuffledlist)
        random.shuffle(shuffledlist)
        
        for i in range(len(modellist[category][models])):
            orig_file = modellist[category][models][i]
            rand_file = shuffledlist[i]
            old_name = orig_file.get("Name") #Old name
            new_name = rand_file.get("Name") #replacement name
            new_type = rand_file.get("Type") #replacement type
            new_file = rand_file.get("File") #replacement file (for .tim and .model)
            if new_type == "Full":
                fileDir = rand_file.get("Directory") #two choices, "Extracted" and "Mod". Extracted will grab hd textures from game extracted files, Mod will grab hd textures from this mod folder.
                HDList = rand_file.get("HDAssets") #list of hd textures. the order of this list should match how the patcher scans the sd file.
                writemodelFull(old_name, new_name, new_file, fileDir, HDList)
            elif new_type == "Orig":
                writemodelOrig(old_name, new_file)
            elif new_type == "Raw":
                writemodelRaw(old_name, new_name)
f.close()