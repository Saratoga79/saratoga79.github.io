#!/usr/bin/env python3
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import urllib.request
from urllib.request import urlopen
import sys
import os
import re
import zipfile
import json
from typing import Iterable

xbmc.log(f"REMOD INSTALADOR INICIO", level=xbmc.LOGINFO)
### info del addon remodiptv incluido en la app (special://xbmc)
remod_instalador_addon = xbmcaddon.Addon('plugin.instalador.remod')
remod_instalador_addon_id = remod_instalador_addon.getAddonInfo('id')
remod_instalador_addon_path = remod_instalador_addon.getAddonInfo('path')
remod_instalador_addon_name = remod_instalador_addon.getAddonInfo('name')
remod_instalador_addon_version = remod_instalador_addon.getAddonInfo('version')
### ruta caprpeta datos
remod_instalador_addon_datos = os.path.join(remod_instalador_addon_path, 'datos')
### special://home/addons
addons_home = xbmcvfs.translatePath(f'special://home/addons')
### special://home/userdata
addons_userdata = xbmcvfs.translatePath(f'special://home/userdata')
### special://home/userdata/addon_data
addons_addon_data = os.path.join(addons_userdata, 'addon_data')
### changelog
changelog = os.path.join(remod_instalador_addon_path, 'changelog.txt')
### info en log
xbmc.log(f"###  INFO REMOD INSTALADOR ADDON ###", level=xbmc.LOGINFO)
xbmc.log(f"Path: {remod_instalador_addon_path}", level=xbmc.LOGINFO)
xbmc.log(f"Name: {remod_instalador_addon_name}", level=xbmc.LOGINFO)
xbmc.log(f"VerSión: {remod_instalador_addon_version}", level=xbmc.LOGINFO)
xbmc.log(f"datos: {remod_instalador_addon_datos}", level=xbmc.LOGINFO)
xbmc.log(f"Addons Path: {addons_home}", level=xbmc.LOGINFO)
xbmc.log(f"Addons Userdata: {addons_userdata}", level=xbmc.LOGINFO)
xbmc.log(f"Addons Data: {addons_addon_data}", level=xbmc.LOGINFO)
xbmc.log(f"### INFO REMOD INSTALADOR ADDON ###", level=xbmc.LOGINFO)

### parametros
BASE_URL = sys.argv[0]
HANDLE = int(sys.argv[1])
ARGS = urllib.parse.parse_qs(sys.argv[2][1:])  ### elimina el '?' inicial

### Construye una URL interna del addon a partir de un dict
def build_url(query):
    return BASE_URL + '?' + urllib.parse.urlencode(query)


### lista del menu pirncipal
def lista_menu_principal():
    ### Cada tupla contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Mostrar Changelog", "info", "info.png"),
        ("> Instalar ReMod TV", "remodtv", "remodtv.png"),
        ("> Instalar [COLOR red]Kodi[/COLOR][COLOR yellow]Spain[/COLOR][COLOR red]Tv[/COLOR]", "ks", "ks.png"),
        ("> Instalar AceStream Channels | AceStream Channels & Horus", "acs_channels", "acs_channels.png"),
        ("> Instalar GreenBall | GreenBall & Horus | [COLOR red]No funciona[/COLOR]", "greenball", "greenball.gif"),
        ("> Instalar [COLOR red]TACONES[/COLOR]", "tacones", "tacones.png"),
        ("> Instalar Balandro", "balandro", "balandro.png"),
        ("> Instalar Magellan", "magellan", "magellan.png"),
        ("> Instalar Alfa", "alfa", "alfa.png"),
        ("> Instalar Moe´s TV | Duff You & Moe´s TV | [COLOR orange]Sin soporte[/COLOR]", "moes", "moes.jpg")
    ]

    for label, action, icon_file in menu_items:
        url = build_url({"action": action})
        ### Creamos el ListItem
        li = xbmcgui.ListItem(label=label)
        ### Ruta absoluta al icono
        icon_path = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_path, 'recursos', 'imagenes', icon_file))
        ###  Asignamos el icono
        li.setArt({'icon': icon_path, 'thumb': icon_path})
        ### Indicamos que es una carpeta (un sub‑menú o acción que abre algo)
        xbmcplugin.addDirectoryItem(handle=HANDLE,
                                    url=url,
                                    listitem=li,
                                    isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


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


### mostrar changelog
def mostrar_changelog():
    xbmc.log(f"{remod_instalador_addon_name} Mostrando changelog.", level=xbmc.LOGINFO)
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
    dlg = xbmcgui.Dialog()
    dlg.textviewer('Changelog', contenido)


### control de versión
VERSION_FILE = os.path.join(xbmcvfs.translatePath("special://profile/addon_data/%s" % remod_instalador_addon_id), "last_version.json")

def leer_ultima_version():
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
    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    try:
        with open(VERSION_FILE, "w") as f:
            json.dump({"version": version}, f)
    except Exception as e:
        xbmc.log("REMOD INSTALADOR Error guardando versión: %s" % e, xbmc.LOGERROR)


def comp_version():
    version_actual = remod_instalador_addon_version
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
        mostrar_changelog()
        xbmcgui.Dialog().notification(f"{remod_instalador_addon_name}","Actualizado de v%s->[COLOR blue]v%s[/COLOR]" % (version_anterior, version_actual),xbmcgui.NOTIFICATION_INFO,5000)
        ### Finalmente, actualizamos el registro
        guardar_version(version_actual)
    else:
        xbmc.log("REMOD INSTALADOR No hay cambios de versión.", xbmc.LOGINFO)

### comrpobación de versión
xbmc.log(f"REMOD INSTALADOR Comprobando actualización.", level=xbmc.LOGINFO)
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
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Addon activado.,1000,)")
            xbmc.log(f"REMOD INSTALADOR Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
            return True
         else:   
            xbmc.sleep(500)
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


### descarga de zip
def download_zip_from_url(url):
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addon.,1000,)")
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
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error al extraer archivo.,3000,)")


### instala tacones
def inst_tacones():
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Tacones,1500,)")
    xbmc.log(f"REMOD INSTALADOR Iniciando Instalación Ttacones.", level=xbmc.LOGINFO)
    ### config
    base_url = 'https://konectas.github.io/Addons%20Video/'
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
        xbmc.log(f"REMOD INSTALADOR Fin instalación Tacones.", level=xbmc.LOGINFO)
    
    
### instala Kodispaintv
def inst_kodispaintv():
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando KodiSpainTv.,1500,)")
    xbmc.log(f"REMOD INSTALADOR Iniciando instalación Kodispaintv.", level=xbmc.LOGINFO)
    ### config func
    base_url = 'https://konectas.github.io/Addons%20Video/'
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
        xbmc.log(f"REMOD INSTALADOR Fin instalación kodispaintv.", level=xbmc.LOGINFO)
     
### instala acestream channels
def inst_acs_channels():
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando AceStream Channels.,1500,)")
    xbmc.log(f"REMOD INSTALADOR Iniciando instalación AceStream Channels.", level=xbmc.LOGINFO)
    ### config func
    base_url = 'https://github.com/gtkingbuild/Repo-GTKing/raw/refs/heads/master/omega/zips/plugin.video.acestream_channels/'
    download_path = os.path.join(addons_home, 'packages')
    pattern = r'plugin\.video\.acestream_channels-\d{1,2}\.\d{1,2}\.\d{1,2}\.zip'
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
        xbmc.log(f"REMOD INSTALADOR Fin instalación kodispaintv.", level=xbmc.LOGINFO)
     

def inst_addon(addon_id):
    ### verificamos que no esté instalado ya
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.log(f"El addon {addon_id} está ya instalado. Omitiendo instalación", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},{addon_id} ya instalado.,1000,)")
        return False
    else:
        xbmc.log(f"El addon {addon_id} no está instalado.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando {addon_id}.,1000,)")
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
                            xbmc.log(f"{remod_instalador_addon_name} instalado", level=xbmc.LOGINFO)
                            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalado.,1000,)")
                            return True
                        else:
                            xbmc.log(f"REMOD INSTALADOR Se está terminado de instalar", level=xbmc.LOGINFO)
                            xbmc.sleep(100)
                            attempts3 += 1
                else:
                    xbmc.sleep(500)  # Pequeña pausa entre intentos
                    attempts2 += 1
            xbmc.log(f"Tiempo max superado {addon_id}.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Tiempo superado.,1000,)")
            return True    
        xbmc.sleep(500)  # Pequeña pausa entre intentos
        attempts += 1
    return False


def buscar_actualizacion():
    xbmc.log(f"REMOD TV Actualizando Addon Repos.", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Actualizando Repos...,3000,)")
    xbmc.executebuiltin(f"UpdateAddonRepos()", True)
    xbmc.sleep(3000)
    xbmc.log(f"REMOD TV Actualizando Local Addon.", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Actualizando Addons...,3000,)")
    xbmc.executebuiltin(f"UpdateLocalAddons()", True)
    xbmc.sleep(3000)


### acciones del menu principal
if not ARGS:
    # No hay parámetros → menú principal
    lista_menu_principal()
else:
    action = ARGS.get('action', [None])[0]
    if action == "info":
        buscar_actualizacion()
        mostrar_changelog()
    elif action == "remodtv":
        addon_id = 'plugin.program.remodtv'
        res = inst_addon(addon_id)
        if res:
            res = addon_inst_confirm(addon_id)
            if res:
                dialog = xbmcgui.Dialog()
                ret = dialog.yesno(f"Menú {remod_instalador_addon_name} v{remod_instalador_addon_version}", "¿Quieres instalar y configurar la sección de TV de Kodi?")
                if ret:
                    xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=tv)')
    elif action == "ks":
        inst_kodispaintv()
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addon.,5000,)")
        addon_id = 'plugin.video.kodispaintv'
        addon_inst_check(addon_id)
        xbmc.sleep(1000)
    elif action == "tacones":
        inst_tacones()
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addon.,5000,)")
        addon_id = 'plugin.video.tacones'
        res = addon_inst_check(addon_id)
        xbmc.sleep(1000)
    elif action == "acs_channels":
        inst_acs_channels()
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addon.,5000,)")
        addon_id = 'plugin.video.acestream_channels'
        res = addon_inst_check(addon_id)
        xbmc.sleep(1000)
        # addon_id = 'plugin.video.acestream_channels'
        # res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
        addon_id = 'script.module.horus'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
    elif action == "greenball":
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
    elif action == "balandro":
        addon_id = 'plugin.video.balandro'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
    elif action == "magellan":
        addon_id = 'plugin.video.Magellan_Matrix'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
        addon_id = 'plugin.video.f4mTester'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
    elif action == "alfa":
        addon_id = 'plugin.video.alfa'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
    elif action == "moes":
        addon_id = 'plugin.video.duffyou'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
        addon_id = 'plugin.video.moestv'
        res = inst_addon(addon_id)
        if res:
            addon_inst_confirm(addon_id)
    elif action == "test":
        test()
    else:
        ### Acción desconocida → volver al menú principal
        lista_menu_principal()
