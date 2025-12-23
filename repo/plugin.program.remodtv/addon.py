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
import urllib.error
import urllib.parse
from urllib.request import urlopen
from pathlib import Path
from typing import Iterable
from typing import Optional
import subprocess
import xml.etree.ElementTree as ET

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
carp = '1'
### control de fuente
fue_lis = os.path.join(remodtv_addon_datos, 'lista_fue', 'fue_lis.json')
fue_est_file = os.path.join(addons_addon_data, remodtv_addon_id, 'estado_fuentes.json')
### variables para archivos json
rep_sel = '0'
rep_act = 'Por defecto'
fue_act = 'Por defecto'
### carpeta descargas en android
android_carpeta_descargas = Path("/storage/emulated/0/Download")
### parametros lista de menús
BASE_URL = sys.argv[0]
HANDLE = int(sys.argv[1])
ARGS = urllib.parse.parse_qs(sys.argv[2][1:])  ### elimina el '?' inicial
action = ARGS.get('action', [None])[0]
ICON_DIR = os.path.join(remodtv_addon_path, 'recursos', 'imagenes')

### gestión iconos menús
def get_icon_path(fname: str) -> Optional[str]:
    full = os.path.join(ICON_DIR, fname)
    if xbmcvfs.exists(full):
        return full
    xbmc.log(f"REMOD TV – Icono no encontrado: {fname}", xbmc.LOGWARNING)
    return None
    
### Construye una URL interna del addon a partir de un dict
def build_url(query: dict) -> str:
    return BASE_URL + '?' + urllib.parse.urlencode(query)

### lista del menu pirncipal
def lista_menu_principal():
    fue_act = leer_fuente()
    rep_act = leer_rep_ext()
    xbmcplugin.setPluginCategory(HANDLE, "Menú Principal")
    menu_principal = [
        (f"{remodtv_addon_name} versión: {remodtv_addon_version} | Buscar actualizaciones", "info", "info.png", True),
        (f"Fuente Actual: {fue_act} | Reproductor Externo: {rep_act}", "", "list.png", False),
        ("> Instalar y configurar sección TV de Kodi | Reinstalar fuente por defecto", "tv", "tv.png", True),
        ("> Elegir fuente para sección TV de Kodi | Comprobar estado de las fuentes", "fuente", "tv2.png", True),
        ("> Configurar Reproductor Externo | Android y Windows", "rep_ext", "repro.png", True),
        ("> Actualizar TV", "actualizar", "refresh.png", True),
        ("", "", "", False),
        ("> Herramientas y Utilidades", "herr", "herr.png", True)
    ]
    for label, action, icon_file, is_folder in menu_principal:
        if not label.strip():
            continue
        url = build_url({"action": action})
        li = xbmcgui.ListItem(label=label)
        icon_path = get_icon_path(icon_file)
        if icon_path:
            li.setArt({'icon': icon_path, 'thumb': icon_path})
        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=url,
            listitem=li,
            isFolder=is_folder
        )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
 
def lista_menu_fuente():
    estados = fue_cargar_estados()
    xbmcplugin.setPluginCategory(HANDLE, "Menú Fuentes")
    menu_fuente = [
        (f"Fuentes Principales para la sección de TV:", "", "tv2.png", False),
        (f" Direct (Por defecto) | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue1')}", "lis_dir", "1.png", True),
        (f" ACE | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue2')}", "lis_ace", "2.png", True),
        (f" Horus | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue3')}", "lis_hor", "3.png", True),
        (f" ReMod TV | Tipo de eventos: [COLOR blue][ACS][/COLOR] y [COLOR yellow][M3U8][/COLOR] [COLOR yellow](VPN recomendada)[/COLOR] | Estado: {estados.get('fue4')}", "lis_rm", "4.png", True),
        (f" Agenda Deportiva | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue5')}", "lis_eve", "5.png", True),
        (f" Chucky | Tipo de eventos: [COLOR yellow][M3U8][/COLOR] [COLOR yellow](VPN recomendada)[/COLOR] | Estado: {estados.get('fue6')}", "lis_chu", "6.png", True),
        ("Fuentes de Repuesto para la sección de TV:", "", "tv2.png", False),
        (f" Direct | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue11')}", "lis_dir_rep", "1.png", True),
        (f" ACE | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue12')}", "lis_ace_rep", "2.png", True),
        (f" Horus | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue13')}", "lis_hor_rep", "3.png", True),
        ("Fuentes de Repuesto 2 para la sección de TV:", "", "tv2.png", False),
        (f" Direct | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue21')}", "lis_dir_rep2", "1.png", True),
        (f" ACE | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue22')}", "lis_ace_rep2", "2.png", True),
        (f" Horus | Tipo de eventos: [COLOR blue][ACS][/COLOR] | Estado: {estados.get('fue23')}", "lis_hor_rep2", "3.png", True)
    ]
    for label, action, icon_file, is_folder in menu_fuente:
        if not label.strip():
            continue
        url = build_url({"action": action})
        li = xbmcgui.ListItem(label=label)
        icon_path = xbmcvfs.translatePath(os.path.join(remodtv_addon_path, 'recursos', 'imagenes', icon_file))
        li.setArt({'icon': icon_path, 'thumb': icon_path})
        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=url,
            listitem=li,
            isFolder=is_folder
        )
    xbmcplugin.endOfDirectory(HANDLE)

### lista del menu configurar reproductor externo
def lista_menu_rep_ext():
    xbmcplugin.setPluginCategory(HANDLE, "Menú Reproductor Externo")
    menu_rep_ext = [
        (f"Elige la aplicación del Reproductor Externo:", "", "repro.png", False),
        ("Ace Stream Media ReMod | Ace Stream Media McK | org.acestream.media", "pcf0", "android.png", True),
        ("Ace Stream Media ATV | org.acestream.media.atv", "pcf1", "android.png", True),
        ("Ace Stream Media Web | org.acestream.media.web", "pcf2", "android.png", True),
        ("Ace Stream Node | org.acestream.node", "pcf3", "android.png", True),
        ("Ace Stream Node Web | org.acestream.node.web", "pcf4", "android.png", True),
        ("Ace Stream Core | org.acestream.core", "pcf5", "android.png", True),
        ("Ace Stream Core ATV | org.acestream.core.atv", "pcf6", "android.png", True),
        ("Ace Stream Core Web | org.acestream.core.web", "pcf7", "android.png", True),
        ("Ace Stream Live | org.acestream.live", "pcf8", "android.png", True),
        ("Ace Stream Pro Mod | org.acestream.nodf", "pcf15", "android.png", True),
        ("Ace Serve | org.free.aceserve", "pcf12", "android.png", True),
        ("MPVkt | live.mehiz.mpvkt", "pcf9", "android.png", True),
        ("MPV | is.xyz.mpv", "pcf10", "android.png", True),
        ("VLC | org.videolan.vlc", "pcf11", "android.png", True),
        ("Ace Stream oficial", "pcf13", "win.png", True),
        ("VLC y Ace Stream oficial", "pcf14", "win.png", True),        
        ("Restaurar por defecto a como cuando se instaló Kodi", "pcf_rest", "restore.png", True)
    ]
    for label, action, icon_file, is_folder in menu_rep_ext:
        if not label.strip():
            continue
        url = build_url({"action": action})
        li = xbmcgui.ListItem(label=label)
        icon_path = get_icon_path(icon_file)
        if icon_path:
            li.setArt({'icon': icon_path, 'thumb': icon_path})
        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=url,
            listitem=li,
            isFolder=is_folder
        )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
    
### lista del menu herramientas
def lista_menu_herramientas():
    xbmcplugin.setPluginCategory(HANDLE, "Menú Herramientas y Utilidades")
    menu_herramientas = [
        ("Herramientas y Utilidades:", "", "herr.png", False),
        ("> Visita Repo ReMod para obtener más información", "nav", "nav.png", True),
        ("Kodi ReMod v251215.0 | org.xbmc.kodi | Actualizado el 15/12/2025:", "", "tool.png", False),
        ("> Descargar Kodi ReMod armeabi-v7a | 32 bits | Android | ATV", "kd32", "download.png", True),
        ("> Descargar Kodi ReMod arm64-v8a | 64 bits | Android | ATV", "kd64", "download.png", True),
        ("Ace Stream Pro ReMod v251216.0 | org.acestream.media | Actualizado el 16/12/2025:", "", "tool.png", False),
        ("> Descargar Ace Stream Pro ReMod armeabi-v7a | 32 bits | Android | ATV", "acs32", "download.png", True),
        ("> Descargar Ace Stream Pro ReMod arm64-v8a | 64 bits | Android | ATV", "acs64", "download.png", True),
        ("Ace Serve v1.5.5 | org.free.aceserve | Actualizado el 28/11/2025:", "", "tool.png", False),
        ("> Descargar Ace Serve armeabi-v7a | 32 bits | Android | ATV", "as32", "download.png", True),
        ("> Descargar Ace Serve arm64-v8a | 64 bits | Android | ATV", "as64", "download.png", True),
        ("WARP | com.cloudflare.onedotonedotonedotone | Actualizado el 17/11/2025:", "", "tool.png", False),
        ("> Descargar WARP Mando Fix para ATV por Jota | 32 bits | 64 bits | Android | ATV", "warp1", "download.png", True)
    ]
    for label, action, icon_file, is_folder in menu_herramientas:
        if not label.strip():
            continue
        url = build_url({"action": action})
        li = xbmcgui.ListItem(label=label)
        icon_path = get_icon_path(icon_file)
        if icon_path:
            li.setArt({'icon': icon_path, 'thumb': icon_path})
        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=url,
            listitem=li,
            isFolder=is_folder
        )
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
    
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
        return True
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
                    return True
                else:
                    xbmc.log(f"REMOD TV Error1 iniciando IPTV Simple.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error iniciando IPTV Simple.,3000,)")
            else:
                xbmc.log(f"REMOD TV Error activando IPTV Simple.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error activando IPTV Simple.,3000,)")
                return False
        else:
            res = addon_borrar_datos(addon_id)
            if res:
                archivos_config()
                lista_addons(addons, True)
                res = pvr_inicio_mon()
                if res:
                    xbmc.log(f"REMOD TV IPTV Simple activado.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Sección de TV recargada.,3000,)")
                    return True
                else:
                    ### url de la fuente caida
                    xbmc.log(f"REMOD TV Error2 iniciando IPTV Simple.", level=xbmc.LOGINFO)
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error iniciando IPTV Simple.,3000,)")
                    return False
            else:
                xbmc.log(f"REMOD TV Error borrando datos IPTV Simple.", level=xbmc.LOGINFO)
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error borrando datos IPTV Simple.,3000,)")
    else:
        xbmc.log(f"REMOD TV Error parando IPTV Simple.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error parando IPTV Simple.,3000,)")


### pvr iniciado = connected / parado = vacio
def pvr_parada_mon():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Parando Sección de TV.,1000,)")
    xbmc.log(f"REMOD TV Esperando parada de PVR", level=xbmc.LOGINFO)
    max_attempts = 5  # Número máximo de intentos = 5s
    attempts = 0
    while attempts < max_attempts:
        pvr_estado = xbmc.getInfoLabel(f"PVR.BackendHost")
        # xbmc.log(f"REMOD TV Estado PVR: {pvr_estado}", level=xbmc.LOGINFO)
        if pvr_estado == '':
            xbmc.log(f"REMOD TV PVR parado", level=xbmc.LOGINFO)
            return True
        else:
            xbmc.sleep(1000)
            attempts += 1
    return False

### pvr iniciado = connected / parado = vacio
def pvr_inicio_mon():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Iniciando Sección de TV.,1000,)")
    xbmc.log(f"REMOD TV Esperando inicio de PVR", level=xbmc.LOGINFO)
    max_attempts = 90  # Número máximo de intentos = 90s
    attempts = 0
    while attempts < max_attempts:
        pvr_estado = xbmc.getInfoLabel(f"PVR.BackendHost")
        # xbmc.log(f"REMOD TV Estado PVR: {pvr_estado}", level=xbmc.LOGINFO)
        if pvr_estado == 'connected':
            xbmc.log(f"REMOD TV PVR iniciado", level=xbmc.LOGINFO)
            return True
        else:
            xbmc.sleep(1000)
            attempts += 1
    return False

def actualizar_tv():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Reiniciando IPTV Simple.,1000,)")
    addons = ["pvr.iptvsimple"]
    addon_id = 'pvr.iptvsimple'
    ### desactivamos iptvsimple
    res = lista_addons(addons, False)
    if res:
        ### mon parada pvr
        res = pvr_parada_mon()
        if res:
            ### activamos iptvsimple
            res = lista_addons(addons, True)
            if res:
                ### mon inicio pvr
                res = pvr_inicio_mon()
                if res:
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Sección de TV recargada.,3000,)")
                    xbmc.log(f"REMOD TV Sección de TV recargada.", level=xbmc.LOGINFO)
                    return True
                else:
                    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al iniciar sección de TV.,5000,)")
                    xbmc.log(f"REMOD TV Error al iniciar sección de TV.", level=xbmc.LOGINFO)
                    dialog = xbmcgui.Dialog()
                    dialog.ok(f"{remodtv_addon_name}", "Error. Parece que hay algún problema con la Fuente elegida.")
            else:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al activar IPTV Simple.,5000,)")
                xbmc.log(f"REMOD TV Error al activar IPTV Simple.", level=xbmc.LOGINFO)
        else:
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al parar sección de TV.,5000,)")
            xbmc.log(f"REMOD TV Error al parar sección de TV.", level=xbmc.LOGINFO)
    else:
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al desactivar IPTV Simple.,5000,)")
        xbmc.log(f"REMOD TV Error al desactivar IPTV Simple.", level=xbmc.LOGINFO)

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

def monitor_pvr():
    ultimo_estado = None
    monitor = xbmc.Monitor()          # <-- objeto que controla abortRequest

    while not monitor.abortRequested():    # <-- forma correcta de comprobarlo
        # Lee el estado actual del PVR Manager
        estado_actual = xbmc.getInfoLabel('System.PVRManager.State')

        # Si ha cambiado respecto al último valor conocido, actúa
        if estado_actual != ultimo_estado:
            xbmc.log(f'PVR Manager cambió a: {estado_actual}', xbmc.LOGINFO)
        xbmc.sleep(500)
        
def nombre_desde_url(url: str) -> str:
    """Obtiene el nombre del archivo a partir de la URL."""
    return os.path.basename(urllib.parse.urlparse(url).path)

def descargar_apk(url: str) -> Path:
    # Aseguramos que la carpeta exista (por si alguna vez falta)
    android_carpeta_descargas.mkdir(parents=True, exist_ok=True)

    nombre_archivo = nombre_desde_url(url)
    ruta_completa = android_carpeta_descargas / nombre_archivo

    # Descarga en bloques de 8 KB
    with urllib.request.urlopen(url) as resp, open(ruta_completa, "wb") as out_file:
        while True:
            bloque = resp.read(8192)
            if not bloque:
                break
            out_file.write(bloque)

    return ruta_completa


### control del estado de las fuentes
fue_est_file = os.path.join(addons_addon_data, remodtv_addon_id, 'estado_fuentes.json')

def crear_variables_url_desde_json():
    try:
        with open(fue_lis, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        xbmc.log(f"PVR Manager → Error al leer {fue_lis}: {exc}", xbmc.LOGERROR)
        return

    for nombre, info in data.items():
        url = info.get("url", "")
        globals()[nombre] = url
        xbmc.log(f"PVR Manager → Variable {nombre} = {url}", xbmc.LOGDEBUG)

def fue_comprobar_y_guardar_estados():
    try:
        with open(fue_lis, "r", encoding="utf-8") as fp:
            lista_raw = json.load(fp)
        xbmc.log(f"PVR Manager → Lista de URLs cargada ({len(lista_raw)} fuentes)", xbmc.LOGINFO)
    except Exception as exc:
        xbmc.log(f"PVR Manager → Error al leer {fue_lis}: {exc}", xbmc.LOGERROR)
        return
    resultados = {}
    for nombre, info in lista_raw.items():
        url = info.get("url", "")
        if not url:
            xbmc.log(f"PVR Manager [{nombre}] Sin URL → marcado como 'Desconocido'",
                     xbmc.LOGWARNING)
            resultados[nombre] = {
                "url": "",
                "codigo": "Sin URL",
                "descripcion": "Desconocido"
            }
            continue

        codigo = obtener_estado(url)
        descripcion = texto_desde_codigo(codigo)

        resultados[nombre] = {
            "url": url,
            "codigo": codigo,
            "descripcion": descripcion,
        }

        # ---- Variable dinámica opcional (legacy) ----
        globals()[f"{nombre}_est"] = descripcion

        xbmc.log(
            f"PVR Manager [{nombre}] Estado: {descripcion} (código {codigo})",
            xbmc.LOGINFO,
        )

    try:
        with open(fue_est_file, "w", encoding="utf-8") as fp:
            json.dump(resultados, fp, ensure_ascii=False, indent=2)
        xbmc.log(f"PVR Manager → Estados guardados en {fue_est_file}", xbmc.LOGINFO)
    except Exception as exc:
        xbmc.log(f"PVR Manager → Error al guardar JSON: {exc}", xbmc.LOGERROR)


def fue_cargar_estados():
    defaults = {f"fue{i}": "Desconocido" for i in range(1, 14)}   # 1‑13

    try:
        with open(fue_est_file, "r", encoding="utf-8") as fp:
            raw = json.load(fp)                                 # diccionario anidado

        # Extraemos únicamente la clave 'descripcion' de cada fuente
        estados = {}
        for clave, info in raw.items():
            # `info` es otro dict con keys: url, codigo, descripcion
            descripcion = info.get("descripcion", "Desconocido")
            estados[clave] = descripcion

        # Rellenamos con defaults por si falta alguna clave
        for k, d in defaults.items():
            estados.setdefault(k, d)

        xbmc.log(f"PVR Manager → Estados procesados: {estados}", xbmc.LOGINFO)
        return estados

    except Exception as exc:
        xbmc.log(f"PVR Manager → Error al leer JSON: {exc}", xbmc.LOGERROR)
        return defaults
        xbmc.log(f"PVR Manager → Estados finales: {traducidos}", xbmc.LOGINFO)
        return traducidos

    except Exception as exc:
        xbmc.log(f"PVR Manager → Error al leer JSON: {exc}", xbmc.LOGERROR)
        return defaults
        
        
def texto_desde_codigo(codigo):
    try:
        codigo_int = int(codigo)          # Normalizamos a entero cuando sea posible
    except (ValueError, TypeError):
        return str(codigo)                # Ya es texto de error

    mapa = {
        200: "Disponible",
        301: "Movido permanentemente",
        302: "Redirigido temporalmente",
        400: "Petición incorrecta",
        401: "No autorizado",
        403: "Prohibido",
        404: "No encontrado",
        408: "Tiempo de espera agotado",
        500: "Error interno del servidor",
        502: "Puerta de enlace incorrecta",
        503: "Servicio no disponible",
        504: "Tiempo de espera de puerta de enlace agotado",
    }
    return mapa.get(codigo_int, f"Código {codigo_int}")

def obtener_estado(url, timeout=5):
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        # "Origin": "https://addons.kodi.tv",   # opcional, ayuda a algunos gateways
    }

    req = urllib.request.Request(url, headers=DEFAULT_HEADERS, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode()          # 200, 301, …
    except urllib.error.HTTPError as e:
        return e.code                     # 404, 403, …
    except urllib.error.URLError as e:
        return f"URLError {e.reason}"
    except Exception as e:
        return f"Error inesperado: {e}"
        
### test

### test        
    
# ----------------------------------------------------------------------
#  ENTRADA PRINCIPAL DEL ADDON
# ----------------------------------------------------------------------
if not ARGS:
    lista_menu_principal()
else:
    action = ARGS.get('action', [None])[0]
    # lista_menu_principal()
    if action == "tv":
        carp = '1'
        res = inst_tv()
        if res:
            # activar seección TV en menú principal
            ajuste_id = "homemenunotvbutton"
            act_ajuste(ajuste_id)
            fue_sel = '1 Direct'
            guardar_fuente(fue_sel)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_dir_rep)')
    ### menú principal selección fuente
    elif action == "fuente":
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Comprobando fuentes...,3000,)")
        fue_comprobar_y_guardar_estados()
        fue_act = leer_fuente()
        lista_menu_fuente()
    ### menú principal iactualizar tv
    elif action == "actualizar":
        res = actualizar_tv()
        if res:
            ajuste_id = "homemenunotvbutton"
            act_ajuste(ajuste_id)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_dir_rep)')
    ### menú principal buscar actuazliación
    elif action == "info":
        res = buscar_actualizacion()
    ### menú principal selección reproductor externo
    elif action == "rep_ext":
        rep_act = leer_rep_ext()
        lista_menu_rep_ext()
    ### menú principal herramientas
    elif action == "herr":
        lista_menu_herramientas()
    ### menú selección fuente 1
    elif action == "lis_dir":
        carp = '1'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '1 Direct'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_dir_rep)')
    ### menú selección fuente 11
    elif action == "lis_dir_rep":
        carp = '11'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '1 Direct Repuesto'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto 2?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto 2,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_dir_rep2)')
    ### menú selección fuente 21
    elif action == "lis_dir_rep2":
        carp = '21'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '1 Direct Repuesto 2'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
    ### menú selección fuente 2
    elif action == "lis_ace":
        carp = '2'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '2 ACE'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_ace_rep)')            
    ### menú selección fuente 12
    elif action == "lis_ace_rep":
        carp = '12'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '2 ACE Repuesto'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto 2?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto 2,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_ace_rep2)')
    ### menú selección fuente 22
    elif action == "lis_ace_rep2":
        carp = '22'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '2 ACE Repuesto 2'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
    ### menú selección fuente 3
    elif action == "lis_hor":
        carp = '3'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '3 Horus'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_hor_rep)')
    ### menú selección fuente 13
    elif action == "lis_hor_rep":
        carp = '13'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '3 Horus Repuesto'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"¿Quieres probar con la Fuente de Repuesto 2?")
            if ret:
                xbmc.executebuiltin(f"Notification({remodtv_addon_name},Probando con la Fuente de Repuesto 2,3000,)")
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=lis_hor_rep2)')
    ### menú selección fuente 23
    elif action == "lis_hor_rep2":
        carp = '23'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '3 Horus Repuesto 2'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
    ### menú selección fuente 4
    elif action == "lis_rm":
        carp = '4'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '4 ReMod TV'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
    ### menú selección fuente 5
    elif action == "lis_eve":
        carp = '5'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '5 Agenda Deportiva'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
    ### menú selección fuente 6
    elif action == "lis_chu":
        carp = '6'
        archivos_config()
        res = actualizar_tv()
        if res:
            fue_sel = '6 Chucky'
            guardar_fuente(fue_sel)
            fue_act = leer_fuente()
            dialog = xbmcgui.Dialog()
            dialog.ok(f"{remodtv_addon_name}", f"Fuente actual: {fue_act}")
    ### menu selección de reprodcutor externo 0
    elif action == "pcf0":
        rep_sel = '0'
        ele_rep(rep_sel)
        reproductor = 'Ace Stream Media ReMod | Ace Stream Media McK'
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
        reproductor = 'Ace Serve'
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
    ### menú herramientas abrir repo en navegador
    elif action == "nav":
        url = "https://saratoga79.github.io/"
        if xbmc.getCondVisibility('system.platform.windows'):
            subprocess.run(f'start "" "{url}"', shell=True, check=False)
        elif xbmc.getCondVisibility('system.platform.android'):
            comando = f'StartAndroidActivity("","android.intent.action.VIEW","","{url}")'
            xbmc.executebuiltin(comando)
        else:
            import webbrowser
            webbrowser.open(url)
    ### menú herramientas descargar kodi 32
    elif action == "kd32":
        if xbmc.getCondVisibility('system.platform.android'):
            url_descarga = (
                "https://www.dropbox.com/scl/fi/j5tyjlwg9qf8s273r16wk/"
                "kodi-21.3-Omega-armeabi-v7a-ReMod-v251215.0.apk?"
                "rlkey=uf1gp0e0jx8w4iaqa84sqstzf&st=u59jxckr&dl=1"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    ### menú herramientas descargar kodi 64
    elif action == "kd64":
        if xbmc.getCondVisibility('system.platform.android'):
            url_descarga = (
                "https://www.dropbox.com/scl/fi/tv25gdfivbnpo9luy1fdi/"
                "kodi-21.3-Omega-arm64-v8a-ReMod-v251215.0.apk?"
                "rlkey=72nlc73l1sjt24n1pytrl4ckv&st=9a1iowld&dl=1"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    ### menú herramientas descargar acs 32
    elif action == "acs32":
        if xbmc.getCondVisibility('system.platform.android'):
            url_descarga = (
                "https://www.dropbox.com/scl/fi/y13hcp0vc2j13aanhhx6m/"
                "Ace-Stream-Pro-3.2.14.5-ReMod-251216.0-armeabi-v7a.apk?"
                "rlkey=bnbzzhf2f9soc0ktvt401f6zy&st=mqgagjkh&dl=1"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    ### menú herramientas descargar acs 64
    elif action == "acs64":
        if xbmc.getCondVisibility('system.platform.android'):
            url_descarga = (
                "https://www.dropbox.com/scl/fi/1iujzli1pg2iizzvh1a36/"
                "Ace-Stream-Pro-3.2.14.5-ReMod-251216.0-arm64-v8a.apk?"
                "rlkey=4dca432egrhu65g8jp0k0eaaw&st=p44zonoz&dl=1"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    ### menú herramientas descargar ace serve 32
    elif action == "as32":
        if xbmc.getCondVisibility('system.platform.android'):
            
            url_descarga = (
                "https://saratoga79.github.io/apps/android/AS/"
                "org.free.aceserve-1.5.5-arm.apk"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    ### menú herramientas descargar ace serve 64
    elif action == "as64":
        if xbmc.getCondVisibility('system.platform.android'):
            url_descarga = (
                "https://saratoga79.github.io/apps/android/AS/"
                "org.free.aceserve-1.5.5-arm64.apk"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    ### menú herramientas descargar warp
    elif action == "warp1":
        if xbmc.getCondVisibility('system.platform.android'):
            url_descarga = (
                "https://www.dropbox.com/scl/fi/ldfhghh1wr7wa4sc4e216/"
                "1.1.1.1_Warp.6.38.5.Mando.ATV.fix.apk?"
                "rlkey=qy1s2do2zq1uon7gzsi56tzs6&st=4cesoko8&dl=1"
            )

            try:
                apk_path = descargar_apk(url_descarga)
                dialog = xbmcgui.Dialog()
                dialog.ok(f"{remodtv_addon_name}", f"Archivo descargado en la carpeta Download de la memoria interna.")
            except Exception as e:
                xbmc.log(f"REMOD TV Error de descarga", level=xbmc.LOGINFO)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno(f"{remodtv_addon_name}", f"Solo para dispositivos Android/ATV.\n\n¿Quieres visitar Repo ReMod como alternativa?")
            if ret:
                xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=nav)')
    else:
        # Acción desconocida → volver al menú principal
        lista_menu_principal()
    
    
