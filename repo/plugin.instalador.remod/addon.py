#!/usr/bin/env python3
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import urllib.request
from urllib.request import urlopen
import os
import sys
import re
import zipfile
import json
from typing import Iterable

xbmc.log(f"REMOD INSTALADOR INICIO", level=xbmc.LOGINFO)
### info del addon remodiptv incluido en la app (special://xbmc)
remod_addon = xbmcaddon.Addon('plugin.instalador.remod')
remod_addon_id = remod_addon.getAddonInfo('id')
remod_addon_path = remod_addon.getAddonInfo('path')
remod_addon_name = remod_addon.getAddonInfo('name')
remod_addon_version = remod_addon.getAddonInfo('version')
### ruta caprpeta datos
remod_addon_datos = os.path.join(remod_addon_path, 'datos')
### special://home/addons
addons_home = xbmcvfs.translatePath(f'special://home/addons')
# remod_config_ok = xbmcvfs.translatePath(os.path.join(remod_addon_path, 'remod_config_ok'))
# remod_off = xbmcvfs.translatePath(os.path.join(remod_addon_path, 'remod_off'))
### special://home/userdata
addons_userdata = xbmcvfs.translatePath(f'special://home/userdata')
### special://home/userdata/addon_data
addons_addon_data = os.path.join(addons_userdata, 'addon_data')
### changelog
changelog = os.path.join(remod_addon_path, 'changelog.txt')
### info en log
xbmc.log(f"###  INFO REMOD INSTALADOR ADDON ###", level=xbmc.LOGINFO)
xbmc.log(f"Path: {remod_addon_path}", level=xbmc.LOGINFO)
xbmc.log(f"Name: {remod_addon_name}", level=xbmc.LOGINFO)
xbmc.log(f"VerSión: {remod_addon_version}", level=xbmc.LOGINFO)
xbmc.log(f"datos: {remod_addon_datos}", level=xbmc.LOGINFO)
xbmc.log(f"Addons Path: {addons_home}", level=xbmc.LOGINFO)
xbmc.log(f"Addons Userdata: {addons_userdata}", level=xbmc.LOGINFO)
xbmc.log(f"Addons Data: {addons_addon_data}", level=xbmc.LOGINFO)
xbmc.log(f"### INFO REMOD INSTALADOR ADDON ###", level=xbmc.LOGINFO)


### Des/Activación de addons
def addon_act_des(addon_id: str, enable: bool) -> None:
    xbmc.log(f"REMOD INSTALADOR: {'Activando' if enable else 'Desactivando'} {addon_id}",
             level=xbmc.LOGINFO)
    request = ('{'
               '"jsonrpc":"2.0",'
               '"method":"Addons.SetAddonEnabled",'
               f'"params":{{"addonid":"{addon_id}","enabled":{str(enable).lower()}}},'
               '"id":1}'
               )
    xbmc.executeJSONRPC(request)


### lista de addons iterable
def lista_addons(addon_ids: Iterable[str], enable: bool) -> None:
    for aid in addon_ids:
        try:
            addon_act_des(aid, enable)
        except Exception as e:
            xbmc.log(f"REMOD INSTALADOR: Error con {aid}: {e}", level=xbmc.LOGERROR)


### copia los archivos de configuración
# def archivos_config():
    # xbmc.log(f"REMOD INSTALADOR Desactivando addons para copiar archivos de configuración.", level=xbmc.LOGINFO)
    ### addons a desactivar para liberar los archivos antes de copiar los nuevos
    # addons = ["script.module.slyguy", "plugin.program.iptv.merge", "pvr.iptvsimple"]
    # lista_addons(addons, False)
    ### copiando sources.xml
    # orig = xbmcvfs.translatePath(os.path.join(remod_addon_datos, 'sources.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'sources.xml'))
    # xbmcvfs.copy(orig, dest)
    ### copiando favourites.xml
    # orig = xbmcvfs.translatePath(os.path.join(remod_addon_datos, 'favourites.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'favourites.xml'))
    # xbmcvfs.copy(orig, dest)
    # xbmc.log(f"REMOD INSTALADOR Copiando archivos de configuración inicial.", level=xbmc.LOGINFO)
    # copiando archivos pvr.iptvsimple
    # orig = xbmcvfs.translatePath(os.path.join(remod_addon_datos, 'pvr.iptvsimple','instance-settings-1.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'instance-settings-1.xml'))
    # xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    # orig = xbmcvfs.translatePath(os.path.join(remod_addon_datos, 'pvr.iptvsimple', 'settings.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'settings.xml'))
    # xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    # copiando archivos script.module.slyguy
    # orig = xbmcvfs.translatePath(os.path.join(remod_addon_datos, 'script.module.slyguy', 'settings.db'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'script.module.slyguy', 'settings.db'))
    # xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    # copiando archivos plugin.program.iptv.merge
    # orig = xbmcvfs.translatePath(os.path.join(remod_addon_datos, 'plugin.program.iptv.merge', 'data.db'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'plugin.program.iptv.merge', 'data.db'))
    # xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    ### addons a activar después de copiar los nuevos archivos
    # xbmc.log(f"REMOD INSTALADOR Activando addons para copiar archivos de configuración.", level=xbmc.LOGINFO)
    # lista_addons(addons, True)
    ### copiando ok
    # xbmc.executebuiltin(f"Notification({remod_addon_name},Archivos del instalador copiados,1000,)")
    # xbmc.log(f"{remod_addon_name} Archivos de instalador copiados.", level=xbmc.LOGINFO)
    # open(remod_config_ok, "w")


### Comprobamos si es el primer inicio tras instalar Kodi o tras borrar datos e instalamod los archivos de configuración. Si no, no hacer nada
# existe_remod_config_ok = xbmcvfs.exists(remod_config_ok)
# if not existe_remod_config_ok:
    # archivos_config()


### mostrar changelog
def mostrar_changelog():
    xbmc.log(f"{remod_addon_name} Mostrando changelog.", level=xbmc.LOGINFO)
    try:
        with open(changelog, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        xbmcgui.Dialog().notification(
            addon.getAddonInfo('name'),
            f'No se pudo leer changelog.txt: {e}',
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return
    # Muestra el texto en un visor de diálogos
    dlg = xbmcgui.Dialog()
    dlg.textviewer('Changelog', contenido)


### control de versión
VERSION_FILE = os.path.join(xbmcvfs.translatePath("special://profile/addon_data/%s" % remod_addon_id), "last_version.json")

def leer_ultima_version():
    """Lee la versión que guardamos la última vez que se ejecutó el script."""
    if not os.path.isfile(VERSION_FILE):
        return None
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("version")
    except Exception as e:
        xbmc.log("REMOD INSTALADOR Error leyendo versión guardada: %s" % e, xbmc.LOGERROR)
        return None


def guardar_version(version):
    """Guarda la versión actual para la próxima comparación."""
    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    try:
        with open(VERSION_FILE, "w") as f:
            json.dump({"version": version}, f)
    except Exception as e:
        xbmc.log("REMOD INSTALADOR Error guardando versión: %s" % e, xbmc.LOGERROR)


def comp_version():
    # version_actual = obtener_version_instalada()
    version_actual = remod_addon_version
    version_anterior = leer_ultima_version()

    xbmc.log("REMOD INSTALADOR Versión actual: %s" % version_actual, xbmc.LOGINFO)

    if version_anterior is None:
        xbmc.log("REMOD INSTALADOR No hay registro previo. Guardando versión actual.", xbmc.LOGINFO)
        guardar_version(version_actual)
        return

    xbmc.log("REMOD INSTALADOR Versión guardada previamente: %s" % version_anterior, xbmc.LOGINFO)

    if version_actual != version_anterior:
        xbmc.log("REMOD INSTALADOR El addon se ha actualizado", xbmc.LOGINFO)
        ### Modificaciones
        # xbmcvfs.delete(remod_config_ok)
        # xbmcvfs.delete(remod_off)
        mostrar_changelog()
        xbmcgui.Dialog().notification(f"{remod_addon_name}","Actualizado de v%s->[COLOR blue]v%s[/COLOR]" % (version_anterior, version_actual),xbmcgui.NOTIFICATION_INFO,5000)
        # Finalmente, actualizamos el registro
        guardar_version(version_actual)
    else:
        xbmc.log("REMOD INSTALADOR No hay cambios de versión.", xbmc.LOGINFO)

### comrpobación de versión
comp_version()


# desactiva la instalación de balandro en cada inicio
def rename_to_bak(addon_id, filename):
    ### Renombra un archivo dentro de un addon a .bak
    try:
        original_file = os.path.join(addons_home, addon_id, filename)
        backup_file = os.path.join(addons_home, f'{filename}.bak')
        # Verificar si el archivo original existe
        if not os.path.exists(original_file):
            xbmc.log(f"REMOD INSTALADOR Archivo {original_file} no encontrado", level=xbmc.LOGINFO)
            return False
            # Renombrar el archivo
            os.rename(original_file, backup_file)
            xbmc.log(f"REMOD INSTALADOR Archivo {original_file} renombrado a {backup_file}", level=xbmc.LOGINFO)
            return True
    except Exception as e:
        print(f"Error al renombrar archivo: {str(e)}")
        return False


# hacer click en yes en diálogo de confirmación
def addon_activacion_confirm(addon_id):
    max_attempts = 10  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
         xbmc.log(f"REMOD INSTALADOR Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
         # Verificar si el diálogo de confirmación está visible
         if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
            xbmc.log(f"REMOD INSTALADOR Espereando visibilidad botón yes para activar addon zip", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            ### copiando ok
            # orig = xbmcvfs.translatePath(remod_off)
            # dest = xbmcvfs.translatePath(os.path.join(addons_home, addon_id, 'ok'))
            # xbmcvfs.copy(orig, dest)
            xbmc.executebuiltin(f"Notification({remod_addon_name},Addon activado.,1000,)")
            xbmc.log(f"REMOD INSTALADOR Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
            return True
         else:   
            xbmc.sleep(500)  # Pequeña pausa entre intentos
            attempts += 1
    return False


# comprobar addon activado ya
def addon_activado_check(addon_id):
    ### activar addon tras el reinicio
    existe = xbmcvfs.exists(xbmcvfs.translatePath(os.path.join(addons_home, addon_id, 'ok')))
    if not existe:
        xbmc.log(f"REMOD INSTALADOR Activando {addon_id}.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f'EnableAddon({addon_id})')
        addon_activacion_confirm(addon_id)
        return True
    else:
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no está activado.", level=xbmc.LOGINFO)
        return False


# comprobar addon instalado
def addon_inst_check(addon_id):
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.log(f"El addon {addon_id} está instalado.", level=xbmc.LOGINFO)
        addon_activado_check(addon_id)
        return True
    else:
        xbmc.log(f"El addon {addon_id} no está instalado.", level=xbmc.LOGINFO)
        return False


### desactiva instalación de balandro en cada inicio
rename_to_bak('repository.balandro', 'service.py')


def menu_principal():
    ### descarga de zip
    def download_zip_from_url(url):
        xbmc.executebuiltin(f"Notification({remod_addon_name},Descargando addon.,1000,)")
        xbmc.log(f"REMOD INSTALADOR Iniciando download_zip_from_url.", level=xbmc.LOGINFO)
        try:
            # Realizar la solicitud HTTP GET
            response = urllib.request.urlopen(url)
            # Extraer el nombre del archivo desde la URL
            filename = url.split('/')[-1]
            # Ruta donde se guardará el archivo
            addon_path = xbmcvfs.translatePath(os.path.join(addons_home, 'packages'))
            # global full_path
            full_path = os.path.join(addon_path, filename)
            # Guardar el archivo en el sistema local
            with open(full_path, 'wb') as f:
                f.write(response.read())
                xbmc.log(f"REMOD INSTALADOR Archivo zip descargado.", level=xbmc.LOGINFO)
            xbmc.log(f"REMOD INSTALADOR Fin download_zip_from_url.", level=xbmc.LOGINFO)
            xbmc.log(f"REMOD INSTALADOR Iniciando extract_zip.", level=xbmc.LOGINFO)
            xbmc.sleep(1000)
            extract_path = xbmcvfs.translatePath(addons_home)
            # Verificar si el archivo existe
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"El archivo {full_path} no existe")
            # Extraer el archivo ZIP
            with zipfile.ZipFile(full_path, mode="r") as archive:
                archive.extractall(extract_path)
                xbmc.log(f"REMOD INSTALADOR Archivo zip extraido.", level=xbmc.LOGINFO)
                return True
            xbmc.log(f"REMOD INSTALADOR Fin extract_zip.", level=xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"REMOD INSTALADOR Error al extraer archivo.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remod_addon_name},Error al extraer archivo.,3000,)")


    ### instala tacones
    def inst_tacones():
        xbmc.executebuiltin(f"Notification({remod_addon_name},Instalando Tacones,1500,)")
        xbmc.log(f"REMOD INSTALADOR Iniciando inst_tacones.", level=xbmc.LOGINFO)
        ### config
        base_url = 'https://konectas.github.io/Addons%20Video/'
        # download_path = 'special://home/addons/packages/' # cambiar xbmc / home según addon interno en la app o instalo como addon normal
        download_path = os.path.join(addons_home, 'packages')
        pattern = r'plugin\.video\.tacones-\d{1,2}\.\d{1,2}\.\d{1,2}\.zip'
        # Realizar la solicitud GET
        with urllib.request.urlopen(base_url) as response:
            html = response.read().decode()
        # Buscar el patrón del archivo zip
        match = re.search(pattern, html)
        if match:
            download_url = f"{base_url}{match.group(0)}"
            download_zip_from_url(download_url)
            xbmc.sleep(1000)
            xbmc.log(f"REMOD INSTALADOR Actualizando Addon Repos.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"UpdateAddonRepos()", True)
            xbmc.sleep(1000)
            xbmc.log(f"REMOD INSTALADOR Actualizando Local Addon.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"UpdateLocalAddons()", True)
            xbmc.sleep(1000)
            # xbmc.executebuiltin("ReloadSkin()", True)
            xbmc.log(f"REMOD INSTALADOR Fin instalación Tacones.", level=xbmc.LOGINFO)
        
        
    ### instala Kodispaintv
    def inst_kodispaintv():
        xbmc.executebuiltin(f"Notification({remod_addon_name},Instalando KodiSpainTv.,1500,)")
        xbmc.log(f"REMOD INSTALADOR Iniciando inst_kodispaintv.", level=xbmc.LOGINFO)
        ### config func
        base_url = 'https://konectas.github.io/Addons%20Video/'
        # download_path = 'special://home/addons/packages/' # cambiar xbmc / home según addon interno en la app o instalo como addon normal
        download_path = os.path.join(addons_home, 'packages')
        pattern = r'plugin\.video\.kodispaintv-\d{1,2}\.\d{1,2}\.\d{1,2}\.zip'
        # Realizar la solicitud GET
        xbmc.log(f"REMOD INSTALADOR Buscando archivo zip.", level=xbmc.LOGINFO)
        with urllib.request.urlopen(base_url) as response:
            html = response.read().decode()
        # Buscar el patrón del archivo zip
        match = re.search(pattern, html)
        if match:
            xbmc.log(f"REMOD INSTALADOR Archivo encontrado zip.", level=xbmc.LOGINFO)
            download_url = f"{base_url}{match.group(0)}"
            download_zip_from_url(download_url)
            xbmc.sleep(1000)
            xbmc.log(f"REMOD INSTALADOR Actualizando Addon Repos.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"UpdateAddonRepos()", True)
            xbmc.sleep(1000)
            xbmc.log(f"REMOD INSTALADOR Actualizando Local Addon.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"UpdateLocalAddons()", True)
            xbmc.sleep(1000)
            # xbmc.executebuiltin("ReloadSkin()", True)
            xbmc.log(f"REMOD INSTALADOR Fin instalación kodispaintv.", level=xbmc.LOGINFO)
         
    
    def inst_addon(addon_id):
        ### verificamos que no esté instalado ya
        if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
            xbmc.log(f"El addon {addon_id} está ya instalado. Omitiendo instalación", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remod_addon_name},{addon_id} ya instalado.,1000,)")
            return False
        else:
            xbmc.log(f"El addon {addon_id} no está instalado.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remod_addon_name},Instalando {addon_id}.,1000,)")
            xbmc.log(f"REMOD INSTALADOR Instalando addon.", level=xbmc.LOGINFO)
            instalar = f"InstallAddon({addon_id}, True)"
            xbmc.executebuiltin(instalar)
            xbmc.sleep(500)
            return True
        
    
    def addon_inst_confirm(addon_id):
        max_attempts = 10  # Número máximo de intentos
        attempts = 0
        while attempts < max_attempts:
            xbmc.log(f"REMOD INSTALADOR Intentando click yes", level=xbmc.LOGINFO)
            # Verificar si el diálogo de confirmación está visible
            if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
                xbmc.log(f"REMOD INSTALADOR Esperando visibilidad botón yes", level=xbmc.LOGINFO)
                # Simular pulsación del botón Yes
                xbmc.executebuiltin(f"SendClick(11)", True)
                max_attempts2 = 20  # Número máximo de intentos
                attempts2 = 0
                while attempts2 < max_attempts2:
                    if xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                        xbmc.log(f"REMOD INSTALADOR Se está instalando", level=xbmc.LOGINFO)
                        max_attempts3 = 200  # Número máximo de intentos
                        attempts3 = 0
                        while attempts3 < max_attempts3:
                            if not xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                                xbmc.log(f"{remod_addon_name} instalado", level=xbmc.LOGINFO)
                                xbmc.executebuiltin(f"Notification({remod_addon_name},Instalado.,1000,)")
                                return True
                            else:
                                xbmc.log(f"REMOD INSTALADOR Se está terminado de instalar", level=xbmc.LOGINFO)
                                xbmc.sleep(100)
                                attempts3 += 1
                    else:
                        xbmc.sleep(500)  # Pequeña pausa entre intentos
                        attempts2 += 1
                xbmc.log(f"Tiempo max superado {addon_id}.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"Notification({remod_addon_name},Tiempo superado.,1000,)")
                return True    
            xbmc.sleep(500)  # Pequeña pausa entre intentos
            attempts += 1
        return False
        
        
    def iptv_update():
        xbmc.executebuiltin(f"Notification({remod_addon_name},Cargando addons.,7500,)")
        xbmc.sleep(7500)
        ## run merge
        xbmc.executebuiltin(f"Notification({remod_addon_name},Actualizando lista TV.,7500,)")
        xbmc.sleep(7500)
        ### comando iptvmerge para actualizar la lista de TV y Radio
        # urllib.request.urlretrieve("http://127.0.0.1:8096/run_merge")
        xbmc.log(f"REMOD INSTALADOR Fin inst_iptvmerge.", level=xbmc.LOGINFO)

    
    ret = 99
    while ret == 99:
        xbmc.log(f"REMOD INSTALADOR Inicio menú de instalación de addons.", level=xbmc.LOGINFO)
        dialog = xbmcgui.Dialog()
        ret = dialog.select(
        f"Menú {remod_addon_name} v{remod_addon_version}",
        [
            ### 0. Configurar sección TV
            "> Instalar ReMod TV",
            ### 1. Instalar KodiSpainTv
            "> Instalar [COLOR red]Kodi[/COLOR][COLOR yellow]Spain[/COLOR][COLOR red]Tv[/COLOR]",
            ### 2. Instalar TACONES
            "> Instalar [COLOR red]TACONES[/COLOR]",
            ### 3. Instalar AceStream Channels
            "> Instalar AceStream Channels\n        AceStream Channels & Horus",
            ### 4. Instalar AceStream Channels
            "> Instalar GreenBall\n        GreenBall & Horus",
            ### 5. Instalar Balandro
            "> Instalar Balandro",
            ### 6. Instalar Magellan
            "> Instalar Magellan\n       Magellan & f4mTester",
            ### 7. Instalar Alfa
            "> Instalar Alfa",
            ### 8. Instalar Moe´s TV
            "> Instalar Moe´s TV\n        Duff You & Moe´s TV",
            ### 9. Salir
            "[COLOR red]x Salir[/COLOR]"
        ]
    )
        if ret == 0: # remodtv
            addon_id = 'plugin.program.remodtv'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            ret = 99
        if ret == 1: # kodispaintv
            inst_kodispaintv()
            dialog = xbmcgui.Dialog()
            xbmc.executebuiltin(f"Notification({remod_addon_name},Activando addon.,5000,)")
            # activación kodispaintv
            addon_id = 'plugin.video.kodispaintv'
            addon_inst_check(addon_id)
            xbmc.sleep(1000)
            ret = 99
        if ret == 2: # Tacones
            inst_tacones()
            dialog = xbmcgui.Dialog()
            xbmc.executebuiltin(f"Notification({remod_addon_name},Activando addon.,5000,)")
            # activación tacones
            addon_id = 'plugin.video.tacones'
            addon_inst_check(addon_id)
            xbmc.sleep(1000)
            ret = 99
        if ret == 3: # AceChannels
            addon_id = 'plugin.video.acestream_channels'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            addon_id = 'script.module.horus'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            ret = 99
            
        if ret == 4: # GreenBall
            repo_url = 'https://ajsm90.github.io/greenball.repo/repo/zips/repository.greenball/repository.greenball-1.0.0.zip'
            addon_id = 'repository.greenball'
            addons = ["repository.greenball"]
            res = download_zip_from_url(repo_url)
            if res:
                xbmc.log(f"REMOD INSTALADOR Actualizando Addon Repos.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"UpdateAddonRepos()", True)
                xbmc.sleep(1000)
                xbmc.log(f"REMOD INSTALADOR Actualizando Local Addon.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"UpdateLocalAddons()", True)
                xbmc.sleep(1000)
                lista_addons(addons, True)
                addon_activacion_confirm(addon_id)
                if res:
                    addon_id = 'plugin.video.GreenBall'
                    res = inst_addon(addon_id)
                    if res:
                        addon_inst_confirm(addon_id)
                        if res:
                            addon_id = 'script.module.horus'
                            res = inst_addon(addon_id)
                            if res:
                                addon_inst_confirm(addon_id)
            ret = 99
        if ret == 5: # Balandro
            addon_id = 'plugin.video.balandro'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            ret = 99
        if ret == 6: # magellan
            addon_id = 'plugin.video.Magellan_Matrix'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            addon_id = 'plugin.video.f4mTester'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            ret = 99
        if ret == 7: # Alfa
            addon_id = 'plugin.video.alfa'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            ret = 99
        if ret == 8: # Moes
            addon_id = 'plugin.video.duffyou'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            addon_id = 'plugin.video.moestv'
            res = inst_addon(addon_id)
            if res:
                addon_inst_confirm(addon_id)
            ret = 99
        if ret == 9: # salir
            # dialog = xbmcgui.Dialog()
            # ret = dialog.yesno(f"Menú {remod_addon_name} v{remod_addon_version}", "¿Quieres desactivar este menú y no verlo más?\n\nEstará accesible en Favoritos.")
            # if not ret:
                # existe = xbmcvfs.exists(remod_off)
                # if existe:
                    # xbmcvfs.delete(remod_off)
                    # xbmc.executebuiltin("ReloadSkin()", True)
            # if ret:
                # xbmc.executebuiltin(f"Notification({remod_addon_name},Desactivando menú de instalación.,1000,)")
                # open(remod_off, "w")
                # xbmc.log(f"REMOD INSTALADOR Desactivando menú de instalación", level=xbmc.LOGINFO)
            # xbmc.executebuiltin("ReloadSkin()", True)
            xbmc.log(f"REMOD INSTALADOR FIN", level=xbmc.LOGINFO)
            # sys.exit(0)



### menu principal run
menu_principal()
xbmc.log(f"REMOD INSTALADOR FIN", level=xbmc.LOGINFO)
# sys.exit(0)