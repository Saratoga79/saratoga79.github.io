import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import os
import sys

### info del addon remod incluido en la app (special://xbmc)
remod_addon = xbmcaddon.Addon('service.instalador.remod')
remod_addon_id = remod_addon.getAddonInfo('id')
remod_addon_path = remod_addon.getAddonInfo('path')
remod_addon_name = remod_addon.getAddonInfo('name')
remod_autoexec = os.path.join(remod_addon_path, 'autoexec.py')
remod_autoexec_path = xbmcvfs.translatePath(remod_autoexec)
### special://home/addons
addons_home = xbmcvfs.translatePath(f'special://home/addons')
### special://home/userdata
addons_userdata = xbmcvfs.translatePath(f'special://home/userdata')
### special://home/userdata/addon_data
addons_addon_data = os.path.join(addons_userdata, 'addon_data')
remod_ok = os.path.join(addons_home, remod_addon_id, 'remod_off')

xbmc.log(f"REMOD START INICIO", level=xbmc.LOGINFO)
xbmc.executebuiltin(f"Notification({remod_addon_name},Iniciando menú de instalación.,3000,)")

xbmc.log(f"1: {remod_addon}", level=xbmc.LOGINFO)
xbmc.log(f"2: {remod_addon_path}", level=xbmc.LOGINFO)
xbmc.log(f"3: {remod_autoexec}", level=xbmc.LOGINFO)


existe = xbmcvfs.exists(remod_ok)
if existe:
    ### borrando ok
    xbmc.log(f"REMOD Borrando off", level=xbmc.LOGINFO)
    xbmcvfs.delete(remod_ok)
xbmc.log(f"REMOD iniciando", level=xbmc.LOGINFO)      
xbmc.executebuiltin(f"RunScript({remod_autoexec_path})")
xbmc.log(f"REMOD START FIN", level=xbmc.LOGINFO)
sys.exit(0)