#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import sys
import os
import re
import zipfile
import json
import urllib.request
from urllib.request import urlopen
from typing import Iterable
import subprocess

xbmc.log(f"REMOD TV INICIO", level=xbmc.LOGINFO)
### info del addon remodtv incluido en la app (special://xbmc)
remodtv_addon = xbmcaddon.Addon('plugin.program.remodtv')
remodtv_addon_id = remodtv_addon.getAddonInfo('id')
remodtv_addon_path = remodtv_addon.getAddonInfo('path')
remodtv_addon_name = remodtv_addon.getAddonInfo('name')
remodtv_addon_version = remodtv_addon.getAddonInfo('version')
### ruta caprpeta datos
remodtv_addon_datos = os.path.join(remodtv_addon_path, 'datos')
### special://home/addons
addons_home = xbmcvfs.translatePath(f'special://home/addons')
### special://home/userdata
addons_userdata = xbmcvfs.translatePath(f'special://home/userdata')
### special://home/userdata/addon_data
addons_addon_data = os.path.join(addons_userdata, 'addon_data')
### changelog
changelog = os.path.join(remodtv_addon_path, 'changelog.txt')
### paths fuente
carp = 'dir'
### variables para archivos json
rep_sel = '0'
rep_act = 'Por defecto'
fue_act = 'Por defecto'
    
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
        (f"{remodtv_addon_name} versión: {remodtv_addon_version} | Buscar actualizaciones | Mostrar Changelog", "info", "info.png"),
        ("> Instalar y configurar sección TV de Kodi | Reinstalar fuente por defecto", "tv", "tv.png"),
        ("> Elegir fuente para sección TV de Kodi", "fuente", "tv2.png"),
        ("> Configurar Reproductor Externo | Android y Windows", "rep_ext", "repro.png"),
        ("> Actualizar TV", "actualizar", "update.png")
    ]

    for label, action, icon_file in menu_items:
        url = build_url({"action": action})
        ### Creamos el ListItem
        li = xbmcgui.ListItem(label=label)
        ### Ruta absoluta al icono
        icon_path = xbmcvfs.translatePath(os.path.join(remodtv_addon_path, 'recursos', 'imagenes', icon_file))
        ###  Asignamos el icono
        li.setArt({'icon': icon_path, 'thumb': icon_path})
        ### Indicamos que es una carpeta (un sub‑menú o acción que abre algo)
        xbmcplugin.addDirectoryItem(handle=HANDLE,
                                    url=url,
                                    listitem=li,
                                    isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)
    
def fuente():
    ### Cada opción contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        (f"Elige la fuente para la sección de TV | Actual: {fue_act}", "fuente", "tv2.png"),
        (" Direct (Por defecto) | http directos", "lis_dir", "1.png"),
        (" ACE | Protocolo acestream://", "lis_ace", "2.png"),
        (" Horus | Para addon Horus", "lis_hor", "3.png"),
        (" ReModTV | [ACS] http directos y [M3U8] | VPN necesaria", "lis_rm", "4.png"),
        (" TVpass | Directos | NBA | NHL | NFL | VPN necesaria", "lis_tvp", "5.png"),
        (" AF1CIONADOS | http directos", "lis_af1", "6.png"),
        (" Eventos Ace Stream | http directos", "lis_eve", "7.png"),
        (" Fuentes de repuesto para la sección de TV:", "fuente", "tv2.png"),
        (" Direct (Por defecto) | http directos", "lis_dir_rep", "1.png"),
        (" ACE | Protocolo acestream://", "lis_ace_rep", "2.png"),
        (" Horus | Para addon Horus", "lis_hor_rep", "3.png")
    ]

    for label, action, icon_file in menu_items:
        url = build_url({"action": action})
        ### Creamos el ListItem
        li = xbmcgui.ListItem(label=label)
        ### Ruta absoluta al icono
        icon_path = xbmcvfs.translatePath(os.path.join(remodtv_addon_path, 'recursos', 'imagenes', icon_file))
        ###  Asignamos el icono
        li.setArt({'icon': icon_path, 'thumb': icon_path})   # thumb también sirve
        ### Indicamos que es una carpeta (un sub‑menú o acción que abre algo)
        xbmcplugin.addDirectoryItem(handle=HANDLE,
                                    url=url,
                                    listitem=li,
                                    isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


### lista del menu configurar reproductor externo
def lista_menu_rep_ext():
    xbmc.log(f"REMOD TV Reproductor actual: {rep_act}", xbmc.LOGINFO)
    ### Cada tupla contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        (f"Elige la aplicación del Reprouctor Externo | Actual: {rep_act}", "rep_ext", "repro.png"),
        ("Ace Stream Media McK | org.acestream.media", "pcf0", "android.png"),
        ("Ace Stream Media ATV | org.acestream.media.atv", "pcf1", "android.png"),
        ("Ace Stream Media Web | org.acestream.media.web", "pcf2", "android.png"),
        ("Ace Stream Node | org.acestream.node", "pcf3", "android.png"),
        ("Ace Stream Node Web | org.acestream.node.web", "pcf4", "android.png"),
        ("Ace Stream Core | org.acestream.core", "pcf5", "android.png"),
        ("Ace Stream Core ATV | org.acestream.core.atv", "pcf6", "android.png"),
        ("Ace Stream Core Web | org.acestream.core.web", "pcf7", "android.png"),
        ("Ace Stream Live | org.acestream.live", "pcf8", "android.png"),
        ("Ace Stream Pro Mod | org.acestream.nodf", "pcf15", "android.png"),
        ("AceServe | org.free.aceserve", "pcf12", "android.png"),
        ("MPVkt | live.mehiz.mpvkt", "pcf9", "android.png"),
        ("MPV | is.xyz.mpv", "pcf10", "android.png"),
        ("VLC | org.videolan.vlc", "pcf11", "android.png"),
        ("Ace Stream oficial", "pcf13", "win.png"),
        ("VLC y Ace Stream oficial", "pcf14", "win.png"),        
        ("Restaurar por defecto a como cuando se instaló Kodi", "pcf_rest", "restore.png")
    ]

    for label, action, icon_file in menu_items:
        url = build_url({"action": action})
        ### Creamos el ListItem
        li = xbmcgui.ListItem(label=label)
        ### Ruta absoluta al icono
        icon_path = xbmcvfs.translatePath(os.path.join(remodtv_addon_path, 'recursos', 'imagenes', icon_file))
        ###  Asignamos el icono
        li.setArt({'icon': icon_path, 'thumb': icon_path})
        ### Indicamos que es una carpeta (un sub‑menú o acción que abre algo)
        xbmcplugin.addDirectoryItem(handle=HANDLE,
                                    url=url,
                                    listitem=li,
                                    isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)
    

### mostrar changelog
def mostrar_changelog():
    xbmc.log(f"{remodtv_addon_name} Mostrando changelog.", level=xbmc.LOGINFO)
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
VERSION_FILE = os.path.join(xbmcvfs.translatePath("special://profile/addon_data/%s" % remodtv_addon_id), "last_version.json")

def leer_ultima_version():
    if not os.path.isfile(VERSION_FILE):
        return None
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("version")
    except Exception as e:
        xbmc.log("REMOD TV Error leyendo versión guardada: %s" % e, xbmc.LOGERROR)
        return None

### control de rep ext
REP_FILE = os.path.join(xbmcvfs.translatePath("special://profile/addon_data/%s" % remodtv_addon_id), "reproductor.json")

def leer_rep_ext():
    if not os.path.isfile(REP_FILE):
        return None
    try:
        with open(REP_FILE, "r") as f:
            ### guardamos en data toda la línea
            data = json.load(f)
            xbmc.log(f"REMOD TV data: {data}", xbmc.LOGINFO)
            ### sacamos de data el valor de reprodcutor
            return data['reprodcutor']
            xbmc.log("REMOD TV Leido: %s" % e, xbmc.LOGERROR)
            return True
    except Exception as e:
        rep_act = data['reprodcutor']
        xbmc.log("REMOD TV Error leyendo reprodcutor externo guardado: %s" % e, xbmc.LOGERROR)
        return None

### control de fuente
FUE_FILE = os.path.join(xbmcvfs.translatePath("special://profile/addon_data/%s" % remodtv_addon_id), "fuente.json")

def leer_fuente():
    if not os.path.isfile(FUE_FILE):
        return None
    try:
        with open(FUE_FILE, "r") as f:
            ### guardamos en data toda la línea
            data = json.load(f)
            xbmc.log(f"REMOD TV data: {data}", xbmc.LOGINFO)
            ### sacamos de data el valor de fuente
            return data['fuente']
            xbmc.log("REMOD TV Leido: %s" % e, xbmc.LOGERROR)
            return True
    except Exception as e:
        fue_act = data['fuente']
        xbmc.log("REMOD TV Error leyendo fuente externo guardado: %s" % e, xbmc.LOGERROR)
        return None

def guardar_version(version):
    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    try:
        with open(VERSION_FILE, "w") as f:
            json.dump({"version": version}, f)
    except Exception as e:
        xbmc.log("REMOD TV Error guardando versión: %s" % e, xbmc.LOGERROR)
        
def guardar_rep_ext(reprodcutor):
    os.makedirs(os.path.dirname(REP_FILE), exist_ok=True)
    try:
        with open(REP_FILE, "w") as f:
            json.dump({"reprodcutor": reprodcutor}, f)
    except Exception as e:
        xbmc.log("REMOD TV Error guardando reproductor externo: %s" % e, xbmc.LOGERROR)

def guardar_fuente(fue_sel):
    os.makedirs(os.path.dirname(FUE_FILE), exist_ok=True)
    try:
        with open(FUE_FILE, "w") as f:
            json.dump({"fuente": fue_sel}, f)
    except Exception as e:
        xbmc.log("REMOD TV Error guardando reproductor externo: %s" % e, xbmc.LOGERROR)

def comp_version():
    version_actual = remodtv_addon_version
    version_anterior = leer_ultima_version()
    xbmc.log("REMOD TV Versión actual: %s" % version_actual, xbmc.LOGINFO)
    if version_anterior is None:
        xbmc.log("REMOD TV No hay registro previo. Guardando versión actual.", xbmc.LOGINFO)
        guardar_version(version_actual)
        return
    xbmc.log("REMOD TV Versión guardada previamente: %s" % version_anterior, xbmc.LOGINFO)
    if version_actual != version_anterior:
        xbmc.log("REMOD TV El addon se ha actualizado", xbmc.LOGINFO)
        ### Modificaciones
        mostrar_changelog()
        xbmcgui.Dialog().notification(f"{remodtv_addon_name}","Actualizado de v%s->[COLOR blue]v%s[/COLOR]" % (version_anterior, version_actual),xbmcgui.NOTIFICATION_INFO,5000)
        ### Finalmente, actualizamos el registro
        guardar_version(version_actual)
    else:
        xbmc.log("REMOD TV No hay cambios de versión.", xbmc.LOGINFO)

### comrpobación de versión
xbmc.log(f"REMOD TV Comprobando actualización.", level=xbmc.LOGINFO)
comp_version()


### copia los archivos de configuración
def archivos_config():
    xbmc.log(f"REMOD TV Desactivando addons para copiar archivos de configuración.", level=xbmc.LOGINFO)
    xbmc.log(f"REMOD TV Copiando archivos de configuración inicial.", level=xbmc.LOGINFO)
    orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'pvr.iptvsimple', carp, 'instance-settings-2.xml'))
    dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'instance-settings-1.xml'))
    xbmcvfs.delete(dest)
    xbmcvfs.copy(orig, dest)
    dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'settings.xml'))
    xbmcvfs.delete(dest)
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Archivos de configuración copiados,3000,)")
    xbmc.log(f"{remodtv_addon_name} Archivos de configuración copiados.", level=xbmc.LOGINFO)

   
### des/activación de addons
def addon_act_des(addon_id: str, enable: bool) -> None:
    xbmc.log(f"REMOD TV: {'Activando' if enable else 'Desactivando'} {addon_id}",
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
            return True
        except Exception as e:
            xbmc.log(f"REMOD TV: Error con {aid}: {e}", level=xbmc.LOGERROR)
            return False

### acer click en yes en diálogo de confirmación
def addon_activacion_confirm(addon_id):
    max_attempts = 10  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
         xbmc.log(f"REMOD TV Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
         # Verificar si el diálogo de confirmación está visible
         if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
            xbmc.log(f"REMOD TV Espereando visibilidad botón yes para activar addon zip", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            xbmcvfs.copy(orig, dest)
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Addon activado.,1000,)")
            xbmc.log(f"REMOD TV Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
            return True
         else:   
            xbmc.sleep(500)
            attempts += 1
    return False
   
### descarga de zip
def download_zip_from_url(url):
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Descargando addon.,1000,)")
    xbmc.log(f"REMOD TV Iniciando download_zip_from_url.", level=xbmc.LOGINFO)
    try:
        ### Realizar la solicitud HTTP GET
        response = urllib.request.urlopen(url)
        ### Extraer el nombre del archivo desde la URL
        filename = url.split('/')[-1]
        ### Ruta donde se guardará el archivo
        addon_path = xbmcvfs.translatePath(os.path.join(addons_home, 'packages'))
        ### global full_path
        full_path = os.path.join(addon_path, filename)
        ### Guardar el archivo en el sistema local
        with open(full_path, 'wb') as f:
            f.write(response.read())
            xbmc.log(f"REMOD TV Archivo zip descargado.", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD TV Fin download_zip_from_url.", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD TV Iniciando extract_zip.", level=xbmc.LOGINFO)
        xbmc.sleep(1000)
        extract_path = xbmcvfs.translatePath(addons_home)
        ### Verificar si el archivo existe
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"El archivo {full_path} no existe")
            return False
        ### Extraer el archivo ZIP
        with zipfile.ZipFile(full_path, mode="r") as archive:
            archive.extractall(extract_path)
            xbmc.log(f"REMOD TV Archivo zip extraido.", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD TV Fin extract_zip.", level=xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"REMOD TV Error al extraer archivo.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al extraer archivo.,3000,)")
        return False
    
    
def inst_addon(addon_id):
    ### verificamos que no esté instalado ya
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},{addon_id} ya instalado.,1000,)")
        xbmc.log(f"El addon {addon_id} está ya instalado. Desinstalando", level=xbmc.LOGINFO)
        return False
    else:
        xbmc.log(f"El addon {addon_id} no está instalado.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Instalando {addon_id}.,1000,)")
        xbmc.log(f"REMOD TV Instalando addon.", level=xbmc.LOGINFO)
        instalar = f"InstallAddon({addon_id}, True)"
        xbmc.executebuiltin(instalar)
        xbmc.sleep(500)
        return True

def addon_inst_confirm(addon_id):
    max_attempts = 10  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
        xbmc.log(f"REMOD TV Intentando click yes", level=xbmc.LOGINFO)
        # Verificar si el diálogo de confirmación está visible
        if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
            xbmc.log(f"REMOD TV Esperando visibilidad botón yes", level=xbmc.LOGINFO)
            # Simular pulsación del botón Yes
            xbmc.executebuiltin(f"SendClick(11)", True)
            max_attempts2 = 20
            attempts2 = 0
            while attempts2 < max_attempts2:
                if xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                    xbmc.log(f"REMOD TV Se está instalando", level=xbmc.LOGINFO)
                    max_attempts3 = 200
                    attempts3 = 0
                    while attempts3 < max_attempts3:
                        if not xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                            xbmc.log(f"{remodtv_addon_name} instalado", level=xbmc.LOGINFO)
                            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Instalado.,1000,)")
                            return True
                        else:
                            xbmc.log(f"REMOD TV Se está terminado de instalar", level=xbmc.LOGINFO)
                            xbmc.sleep(100)
                            attempts3 += 1
                else:
                    xbmc.sleep(500)
                    attempts2 += 1
            xbmc.log(f"Tiempo max superado {addon_id}.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Tiempo superado.,1000,)")
            return True    
        xbmc.sleep(500)
        attempts += 1
    return False
        

### instala iptv simple
def inst_tv():
    addons = ["pvr.iptvsimple"]
    addon_id = 'pvr.iptvsimple'
    lista_addons(addons, False)
    res = pvr_parada_mon()
    if res:
        res = inst_addon(addon_id)
        if res:
            archivos_config()
            res = addon_inst_confirm(addon_id)
            if res:
                lista_addons(addons, True)
                res = pvr_inicio_mon()
                if res:
                    xbmc.log(f"REMOD TV IPTV Simple activado.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Sección de TV recargada.,3000,)")
                else:
                    xbmc.log(f"REMOD TV Error1 iniciando IPTV Simple.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error iniciando IPTV Simple.,3000,)")
            else:
                xbmc.log(f"REMOD TV Error activando IPTV Simple.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error activando IPTV Simple.,3000,)")
        else:
            res = addon_borrar_datos(addon_id)
            if res:
                archivos_config()
                lista_addons(addons, True)
                res = pvr_inicio_mon()
                if res:
                    xbmc.log(f"REMOD TV IPTV Simple activado.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Sección de TV recargada.,3000,)")
                else:
                    xbmc.log(f"REMOD TV Error2 iniciando IPTV Simple.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error iniciando IPTV Simple.,3000,)")
            else:
                xbmc.log(f"REMOD TV Error borrando datos IPTV Simple.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error borrando datos IPTV Simple.,3000,)")
    else:
        xbmc.log(f"REMOD TV Error parando IPTV Simple.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error parando IPTV Simple.,3000,)")


### pvr iniciado = connected / parado = vacio
def pvr_parada_mon():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Parando Sección de TV.,1000,)")
    max_attempts = 100  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
        xbmc.log(f"REMOD TV Esperando parada de PVR", level=xbmc.LOGINFO)
        pvr_estado = xbmc.getInfoLabel(f"PVR.BackendHost")
        xbmc.log(f"REMOD TV Estado PVR: {pvr_estado}", level=xbmc.LOGINFO)
        # Verificar si el diálogo de confirmación está visible
        # if not pvr_estado == 'connected':
        if pvr_estado == '':
            xbmc.log(f"REMOD TV PVR parado", level=xbmc.LOGINFO)
            return True
        else:
            xbmc.sleep(3000)
            attempts += 1
    return False


### pvr iniciado = connected / parado = vacio
def pvr_inicio_mon():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Iniciando Sección de TV.,1000,)")
    max_attempts = 100  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
        xbmc.log(f"REMOD TV Esperando inicio de PVR", level=xbmc.LOGINFO)
        pvr_estado = xbmc.getInfoLabel(f"PVR.BackendHost")
        xbmc.log(f"REMOD TV Estado PVR: {pvr_estado}", level=xbmc.LOGINFO)
        # Verificar si el diálogo de confirmación está visible
        if pvr_estado == 'connected':
            xbmc.log(f"REMOD TV PVR iniciado", level=xbmc.LOGINFO)
            return True
        else:
            xbmc.sleep(3000)
            attempts += 1
    return False


def actualizar_tv():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Reiniciando IPTV Simple.,1000,)")
    addons = ["pvr.iptvsimple"]
    addon_id = 'pvr.iptvsimple'
    res = lista_addons(addons, False)
    res = pvr_parada_mon()
    if res:
        res = lista_addons(addons, True)
        if res:
            res = pvr_inicio_mon()
            if res:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Sección de TV recargada.,3000,)")
                return True
            else:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al iniciar IPTV Simple.,5000,)")
        else:
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al activar IPTV Simple.,5000,)")
    else:
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al desactivar IPTV Simple.,5000,)")
       
        
def buscar_actualizacion():
    xbmc.log(f"REMOD TV Actualizando Addon Repos.", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Actualizando Repos...,3000,)")
    xbmc.executebuiltin(f"UpdateAddonRepos()", True)
    xbmc.sleep(3000)
    xbmc.log(f"REMOD TV Actualizando Local Addon.", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Actualizando Addons...,3000,)")
    xbmc.executebuiltin(f"UpdateLocalAddons()", True)
    xbmc.sleep(3000)
    

def addon_borrar_datos(addon_id):
    addons = ["pvr.iptvsimple"]
    lista_addons(addons, False)
    xbmc.sleep(1500)
    dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, addon_id))
    for nombre in os.listdir(dest):
        # Nos quedamos solo con los que terminan en .xml (ignoramos mayúsculas/minúsculas)
        if nombre.lower().endswith('.xml'):
            ruta_completa = os.path.join(dest, nombre)
            try:
                os.remove(ruta_completa)  # <‑‑ borrado
                return True
            except Exception as e:
                xbmcgui.Dialog().notification(
                    "Error al borrar XML",
                    f"{nombre}: {e}",
                    xbmcgui.NOTIFICATION_ERROR,
                    4000
                )


### configuración del reproductor externo para ACS en Android
def ele_rep(rep_sel):
    xbmc.log(f"REMOD TV Configuración Reproductor Externo", level=xbmc.LOGINFO)
    if rep_sel == 'rest_pcf':
        ### Borramos pcf para dejarlo por defecto
        xbmc.log(f"REMOD TV Borrando playercorefactory.xml", level=xbmc.LOGINFO)
        dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'playercorefactory.xml'))
        xbmcvfs.delete(dest)
        dialog = xbmcgui.Dialog()
        dialog.ok(f"{remodtv_addon_name}", "Restaurado. Necesitarás reiniciar Kodi para aplicar los cambios.")
    
    else:
        ### variable de la carpeta
        pcf_path = f"playercorefactory{rep_sel}"
        ### copiando archivo playercorefactory.xml desde la variable de la carpeta
        xbmc.log(f"REMOD TV Copiando archivo {pcf_path}", level=xbmc.LOGINFO)
        orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'pcf', pcf_path, 'playercorefactory.xml'))
        dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'playercorefactory.xml'))
        xbmcvfs.copy(orig, dest)
        dialog = xbmcgui.Dialog()
        dialog.ok(f"{remodtv_addon_name}", f"Configurado. Necesitarás reiniciar Kodi para aplicar los cambios.")


### activar sección TV si no está activada (homemenunotvbutton = True = Sección desactivada)
def act_ajuste(ajuste_id):
    ajuste_check = xbmc.getCondVisibility(f'Skin.HasSetting({ajuste_id})') == 1
    if ajuste_check:
        xbmc.executebuiltin(f'Skin.SetBool({ajuste_id},false)')


### test ###


def manejar_cambio_estado(nuevo_estado):
    if nuevo_estado == 'Starting':
        xbmc.log('PVR está arrancando…', xbmc.LOGNOTICE)
    elif nuevo_estado == 'Started':
        xbmc.log('PVR ya está activo.', xbmc.LOGNOTICE)
    elif nuevo_estado == 'Stopping':
        xbmc.log('PVR se está deteniendo.', xbmc.LOGNOTICE)
    elif nuevo_estado == 'Stopped':
        xbmc.log('PVR está detenido.', xbmc.LOGNOTICE)
    else:
        xbmc.log(f'Estado PVR desconocido: {nuevo_estado}', xbmc.LOGWARNING)
        return False


# ----------------------------------------------------------------------
# Bucle principal de monitorización.
# ----------------------------------------------------------------------
def monitor_pvr():
    ultimo_estado = None
    monitor = xbmc.Monitor()          # <-- objeto que controla abortRequest

    while not monitor.abortRequested():    # <-- forma correcta de comprobarlo
        # Lee el estado actual del PVR Manager
        estado_actual = xbmc.getInfoLabel('System.PVRManager.State')

        # Si ha cambiado respecto al último valor conocido, actúa
        if estado_actual != ultimo_estado:
            xbmc.log(f'PVR Manager cambió a: {estado_actual}', xbmc.LOGINFO)
            # manejar_cambio_estado(estado_actual)
            # ultimo_estado = estado_actual

        # Espera medio segundo antes de volver a consultar.
        # Puedes ajustar este intervalo según la reactividad que necesites.
        xbmc.sleep(500)   # 0.5 s
        
        
###

### acciones del menu principal
if not ARGS:
    # No hay parámetros → menú principal
    lista_menu_principal()
else:
    action = ARGS.get('action', [None])[0]
    if action == "tv":
        carp = 'dir'
        inst_tv()
        ### activar seección TV en menú principal
        ajuste_id = "homemenunotvbutton"
        act_ajuste(ajuste_id)
        fue_sel = '1 Direct'
        guardar_fuente(fue_sel)
    elif action == "fuente":
        fue_act = leer_fuente()
        fuente()
    elif action == "actualizar":
        actualizar_tv()
        ajuste_id = "homemenunotvbutton"
        act_ajuste(ajuste_id)
    elif action == "info":
        res = buscar_actualizacion()
        if not res:
            mostrar_changelog()
    elif action == "rep_ext":
        rep_act = leer_rep_ext()
        lista_menu_rep_ext()
        
    elif action == "lis_dir":
        carp = 'dir'
        archivos_config()
        actualizar_tv()
        fue_sel = '1 Direct'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_dir_rep":
        carp = 'dir_rep'
        archivos_config()
        actualizar_tv()
        fue_sel = '1 Direct Repuesto'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_ace":
        carp = 'ace'
        archivos_config()
        actualizar_tv()
        fue_sel = '2 ACE'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_ace_rep":
        carp = 'ace_rep'
        archivos_config()
        actualizar_tv()
        fue_sel = '2 ACE Repuesto'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_hor":
        carp = 'hor'
        archivos_config()
        actualizar_tv()
        fue_sel = '3 Horus'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_hor_rep":
        carp = 'hor_rep'
        archivos_config()
        actualizar_tv()
        fue_sel = '3 Horus Repuesto'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_rm":
        carp = 'rm'
        archivos_config()
        actualizar_tv()
        fue_sel = '4 ReModTV'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_tvp":
        carp = 'tvp'
        archivos_config()
        actualizar_tv()
        fue_sel = '5 TVpass'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_af1":
        carp = 'af1'
        archivos_config()
        actualizar_tv()
        fue_sel = '6 AF1CIONADOS'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
    elif action == "lis_eve":
        carp = 'eve'
        archivos_config()
        actualizar_tv()
        fue_sel = '7 Eventos'
        guardar_fuente(fue_sel)
        fue_act = leer_fuente()
        
    elif action == "pcf0":
        rep_sel = '0'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media McK'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf1":
        rep_sel = '1'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media ATV'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf2":
        rep_sel = '2'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media Web'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf3":
        rep_sel = '3'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media Node'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf4":
        rep_sel = '4'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media Node Web'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf5":
        rep_sel = '5'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media Core'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf6":
        rep_sel = '6'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media Core ATV'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf7":
        rep_sel = '7'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media Core Web'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf8":
        rep_sel = '8'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Live'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf9":
        rep_sel = '9'
        ele_rep(rep_sel)
        reproductor = 'MPVkt'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf10":
        rep_sel = '10'
        ele_rep(rep_sel)
        reproductor = 'MPV'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf11":
        rep_sel = '11'
        ele_rep(rep_sel)
        reproductor = 'VLC'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf12":
        rep_sel = '12'
        ele_rep(rep_sel)
        reproductor = 'AceServe'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf13":
        rep_sel = '13'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream oficial'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf14":
        rep_sel = '14'
        ele_rep(rep_sel)
        reproductor = 'VLC y Ace Stream oficial'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf15":
        rep_sel = '15'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Pro Mod'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
    elif action == "pcf_rest":
        rep_sel = 'rest_pcf'
        ele_rep(rep_sel)
        reproductor = 'Por defecto de Kodi'
        guardar_rep_ext(reproductor)
        rep_act = leer_rep_ext()
        
    elif action == "test":
        # actualizar_tv()
        # monitor_pvr()
        # avtivado = connected / desactivado = vació
        pvr_estado = xbmc.getInfoLabel(f"PVR.BackendHost")
        xbmc.log(f"REMOD TV Estado PVR: {pvr_estado}", level=xbmc.LOGINFO)
        
        pass
    else:
        ### Acción desconocida → volver al menú principal
        lista_menu_principal()