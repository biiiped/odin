import os
import subprocess
import glob

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[33m'

"""
# Create SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start the SSH agent
eval "$(ssh-agent -s)"

# Add the private key to the agent
ssh-add ~/.ssh/id_ed25519

# Show your public key
cat ~/.ssh/id_ed25519.pub

# Test connection to GitHub
ssh -T git@github.com
"""
def verifyLevel(limit,whitelist,root_path,assetList):
    # Loop over assets in the root folder
    print(bcolors.OKGREEN+f"looking at  {root_path}"+bcolors.ENDC)
    for asset_name in assetList:
        if limit==0:
            break
        asset_path = os.path.join(root_path, asset_name)
        if not os.path.isdir(asset_path):
            continue

        export_path = os.path.join(asset_path, "Export")
        if not os.path.isdir(export_path):
            continue

        asset_clean = True

        for product_name in os.listdir(export_path):
            if product_name not in whitelist:
                asset_clean = False
                break  # No need to check more products

        if not asset_clean:
            # Open Explorer at the asset's path
            print(bcolors.WARNING+f"asset {asset_name} is not clean: {product_name}"+bcolors.ENDC)
            subprocess.Popen(f'explorer "{export_path}"')
        else:
            print(bcolors.OKBLUE+f"asset {asset_name} is clean"+bcolors.ENDC)
        limit-=1
    
    print('')




propsRootPath = r"I:\intermarche\03_Production\Assets\Props"
propsList=os.listdir(propsRootPath)

envRootPath = r"I:\intermarche\03_Production\Assets\Environment"
envList=os.listdir(envRootPath)

setsRootPath = r"I:\intermarche\03_Production\Assets\Sets"
setsList=os.listdir(setsRootPath)

charsRootPath = r"I:\intermarche\03_Production\Assets\Characters"
charsList=os.listdir(charsRootPath)
charsList.remove('wolf')

whitelistProps = {"Rigging", "USD", "Modeling","toRig","toSubstance","old","Sculpt","products.json","Rigging","_layer_shd_master"}  # <- Replace with your whitelist
verifyLevel(10,whitelistProps,propsRootPath,propsList)
whitelistEnv = {"_layer_mod_master", "USD", "extraPublish","_layer_mod_mayaLayout","old","products.json"}
verifyLevel(10,whitelistEnv,envRootPath,envList)
verifyLevel(10,whitelistProps,setsRootPath,setsList)
whitelistchar = {"_layer_mod_master","FromMeshAI","_layer_shd_master","extraPublish", "Rigging","toRig","USD","old","products.json","_layer_cfx_groom","_layer_cfx_master","_layer_cfx_groomShading","toRig","toSubstance"}
verifyLevel(10,whitelistchar,charsRootPath,charsList)

sequencesRootPath = r"I:\intermarche\03_Production\Shots"
sequences=os.listdir(sequencesRootPath)
sequences.remove('testShot')
whitelistShots = {"_layer_Anim_master","_layer_lgt_lightingHoudini","_layer_lgt_master","_layer_lay_camera","_layer_lay_main","_layer_lay_master","_layer_Lighting_master","_layer_FX_master","USD","old","products.json","cameraToAnim","layoutExtraPublish"}

for sequence in sequences:
    shotRootPath=os.path.join(sequencesRootPath,sequence)
    shotList=os.listdir(shotRootPath)
    if '_sequence' in shotList:
        shotList.remove('_sequence')
    verifyLevel(10,whitelistShots,shotRootPath,shotList)