#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import logging
import urllib.request
import urllib.error
import urllib.parse
from urllib.request import urlopen
from pathlib import Path
from typing import Optional
import sys
import os
import re
import zipfile
import json
from typing import Iterable
import xml.etree.ElementTree as ET

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
# addons_home = xbmcvfs.translatePath(f'special://home/addons')
addons_home = xbmcvfs.translatePath(f'special://home/addons')
# addons_home = Path(xbmcvfs.translatePath("special://home/addons"))   # raíz de los addons
addons_home = Path(xbmcvfs.translatePath("special://home/addons"))   # raíz de los addons

### special://home/userdata
addons_userdata = xbmcvfs.translatePath(f'special://home/userdata')
### special://home/userdata/addon_data
addons_addon_data = os.path.join(addons_userdata, 'addon_data')
### notis
noti_error_icon = os.path.join(remod_instalador_addon_path, 'recursos', 'imagenes', 'error.png')
noti_ok_icon = os.path.join(remod_instalador_addon_path, 'recursos', 'imagenes', 'ok.png')
noti_icon = os.path.join(remod_instalador_addon_path, 'recursos', 'imagenes', 'info.png')

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
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "icono.png"),
        ("> Sección Deportes", "deportes", "stadium.png"),
        ("> Sección Cine & TV", "cine", "cinema.png"),
        ("> Sección Herramientas", "herramientas", "herramientas.png"),
        ("> Test", "test", "")
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

### lista del menu tv
def lista_menu_deportes():
    ### Cada tupla contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "icono.png"),
        ("> Instalar ReMod TV", "remodtv", "remodtv.png"),
        ("> Instalar [COLOR red]Kodi[/COLOR][COLOR yellow]Spain[/COLOR][COLOR red]Tv[/COLOR]", "kodispaintv", "kodispaintv.png"),
        ("> Instalar AceStream Channels", "acs_channels", "acs_channels.png"),
        ("> Instalar Naranjito", "naranjito", "naranjito.png"),
        ("> Instalar The Loop", "loop", "loop.png"),
        ("> Instalar SportHD", "sporthd", "sporthd.png"),
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

### lista del menu cine
def lista_menu_cine():
    ### Cada tupla contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "icono.png"),
        ("> Instalar Jacktook | Películas & Series Stremio | TV en vivo Ace Stream", "jacktook", "jacktook.png"),
        ("> Instalar [COLOR red]TACONES[/COLOR]", "tacones", "tacones.png"),
        ("> Instalar Balandro", "balandro", "balandro.png"),
        ("> Instalar Magellan", "magellan", "magellan.png"),
        ("> Instalar Alfa", "alfa", "alfa.png"),
        ("> Instalar EspaDaily", "espadaily", "espadaily.png"),
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


### lista del menu herramientas
def lista_menu_herramientas():
    ### Cada tupla contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "icono.png"),
        ("> Instalar EZMaintenance+", "ezmaintenanceplus", "ezmaintenance.png"),
        ("> Instalar Log Viewer", "log_viewer", "log_viewer.png"),
        ("> Instalar Kodi Backup", "backup", "backup.png"),
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
            return True
        except Exception as e:
            xbmc.log(f"REMOD INSTALADOR: Error con {aid}: {e}", level=xbmc.LOGERROR)
            return False

### mostrar changelog
def mostrar_changelog():
    xbmc.log(f"{remod_instalador_addon_name} Mostrando changelog", level=xbmc.LOGINFO)
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
        xbmc.log("REMOD INSTALADOR No hay registro previo. Guardando versión actual", xbmc.LOGINFO)
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
        xbmc.log("REMOD INSTALADOR No hay cambios de versión", xbmc.LOGINFO)

### comrpobación de versión
# xbmc.log(f"REMOD INSTALADOR Comprobando actualización", level=xbmc.LOGINFO)
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
        xbmc.log(f"REMOD INSTALADOR Error al renombrar archivo", level=xbmc.LOGERROR)
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
            # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Addon activado,1000)")
            xbmc.log(f"REMOD INSTALADOR Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
            return True
         else:   
            xbmc.sleep(500)
            attempts += 1
    return False
    
# hacer click en yes en diálogo de confirmación
def multiselect_aceptar_confirm(addon_id):
    max_attempts = 20  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
         xbmc.log(f"REMOD INSTALADOR Espereando visibilidad ventana multiselect", level=xbmc.LOGINFO)
         # Verificar si el diálogo de confirmación está visible
         if xbmc.getCondVisibility(f"Window.IsVisible(12000)"):
            xbmc.sleep(100)
            xbmc.log(f"REMOD INSTALADOR Intentando click en botón Acptar para activar multiselect", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Action(Right)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"Action(Right)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"Action(Select)", True)
            xbmc.sleep(1000)
            xbmc.log(f"REMOD INSTALADOR Reintentando click en botón Acptar para activar multiselect", level=xbmc.LOGINFO)
            return True
         else:   
            xbmc.sleep(500)
            attempts += 1
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error activando configuración multiselect,3000,{noti_error_icon})")
    return False
    
# hacer click en yes en diálogo de confirmación
def dialog_aceptar_confirm(addon_id):
    max_attempts = 10  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
        xbmc.log(f"REMOD INSTALADOR Esperando visibilidad para Aceptar diálogo", level=xbmc.LOGINFO)
        # Verificar si el diálogo de confirmación está visible
        if xbmc.getCondVisibility(f"Window.IsVisible(12002)"):
            xbmc.log(f"REMOD INSTALADOR Intentando hacer click en Aceptar diálogo", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Action(Left)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            return True
        else:
            xbmc.log(f"REMOD INSTALADOR No se detecta visibilidad para Aceptar diálogo", level=xbmc.LOGINFO)
            xbmc.sleep(500)
            attempts += 1
        # si ya están añadidos de antes, la pantalla cambia
        if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
            xbmc.log(f"REMOD INSTALADOR Intentando hacer click en Aceptar diálogo 2", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Action(Left)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            return True
        else:
            xbmc.log(f"REMOD INSTALADOR No se detecta visibilidad para Aceptar 2", level=xbmc.LOGINFO)
            xbmc.sleep(500)
            attempts += 1
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error aceptando configuración diálogo,3000,{noti_error_icon})")
    return False

# comprobar addon activado ya
def addon_activado_check(addon_id):
    ### activar addon tras el reinicio
    xbmc.log(f"REMOD INSTALADOR Activando addon descargado {addon_id}", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f'EnableAddon({addon_id})')
    if addon_activacion_confirm(addon_id):
        return True
    else:
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no está activado", level=xbmc.LOGINFO)
        return False


# comprobar addon instalado
def addon_inst_check(addon_id):
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} está instalado", level=xbmc.LOGINFO)
        addon_activado_check(addon_id)
        return True
    else:
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no está instalado", level=xbmc.LOGINFO)
        return False

### desactiva instalación de balandro en cada inicio
rename_to_bak('repository.balandro', 'service.py')

### descarga de zip
def download_direct_zip_from_url(url):
    xbmc.log(f"REMOD INSTALADOR Iniciando download_zip_from_url", level=xbmc.LOGINFO)
    try:
        response = urllib.request.urlopen(url)
        filename = os.path.basename(url)
        # Ruta de la carpeta «packages» dentro del perfil de Kodi
        addon_path = xbmcvfs.translatePath(os.path.join(addons_home, 'packages'))
        # global full_path
        full_path = os.path.join(addon_path, filename)
        # Guardar el contenido recibido
        with open(full_path, "wb") as f:
            f.write(response.read())
            xbmc.log(f"REMOD INSTALADOR Archivo zip descargado", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD INSTALADOR Fin descarga zip directo", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD INSTALADOR Iniciando extracción", level=xbmc.LOGINFO)
        xbmc.sleep(1000)
        xbmc.log(f"REMOD INSTALADOR ZIP guardado en {full_path}", xbmc.LOGINFO)
        ### extrarct
        extract_path = xbmcvfs.translatePath(addons_home)
        # Verificar si el archivo existe
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"El archivo {full_path} no existe")
        # Extraer el archivo ZIP
        with zipfile.ZipFile(full_path, mode="r") as archive:
            archive.extractall(extract_path)
            xbmc.log(f"REMOD INSTALADOR Archivo zip directo extraido", level=xbmc.LOGINFO)
            return True
        xbmc.log(f"REMOD INSTALADOR Fin archivo zip directo", level=xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"REMOD INSTALADOR Error al extraer archivo zip directo", level=xbmc.LOGERROR)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error al extraer archivo zip,3000,{noti_error_icon})")
        return False

### descarga de zip
def download_zip_from_url(url):
    xbmc.log(f"REMOD INSTALADOR Iniciando download_zip_from_url", level=xbmc.LOGINFO)
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
            xbmc.log(f"REMOD INSTALADOR Archivo zip descargado", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD INSTALADOR Fin download_zip_from_url", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD INSTALADOR Iniciando extract_zip", level=xbmc.LOGINFO)
        xbmc.sleep(1000)
        extract_path = xbmcvfs.translatePath(addons_home)
        # Verificar si el archivo existe
        if not os.path.exists(full_path):
            xbmc.log(f"REMOD INSTALADOR El archivo {full_path} no existe", level=xbmc.LOGINFO)
            raise FileNotFoundError(f"El archivo {full_path} no existe")
        # Extraer el archivo ZIP
        with zipfile.ZipFile(full_path, "r") as archive:
            archive.extractall(extract_path)
            xbmc.log(f"REMOD INSTALADOR Archivo zip extraido", level=xbmc.LOGINFO)
            return True
        xbmc.log(f"REMOD INSTALADOR Fin extract_zip", level=xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"REMOD INSTALADOR Error al extraer archivo", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error al extraer archivo,3000,{noti_error_icon})")
        return False

def inst_addon(addon_id):
    ### verificamos que no esté instalado ya
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} está ya instalado. Omitiendo instalación", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},{addon_id} ya instalado,1000)")
        return False
    else:
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no está instalado", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando {addon_id},1000)")
        xbmc.log(f"REMOD INSTALADOR Instalando addon", level=xbmc.LOGINFO)
        instalar = f"InstallAddon({addon_id}, True)"
        xbmc.executebuiltin(instalar)
        xbmc.sleep(500)
        return True

def addon_inst_confirm(addon_id):
    max_attempts = 20  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
        xbmc.log(f"REMOD INSTALADOR Intentando click yes para instalar {addon_id}", level=xbmc.LOGINFO)
        # Verificar si el diálogo de confirmación está visible
        if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
            xbmc.log(f"REMOD INSTALADOR Esperando visibilidad botón yes {addon_id}", level=xbmc.LOGINFO)
            # Simular pulsación del botón Yes
            xbmc.executebuiltin(f"SendClick(11)", True)
            max_attempts2 = 20  # Número máximo de intentos
            attempts2 = 0
            while attempts2 < max_attempts2:
                if xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                    xbmc.log(f"REMOD INSTALADOR Se está instalando {addon_id}", level=xbmc.LOGINFO)
                    max_attempts3 = 200  # Número máximo de intentos
                    attempts3 = 0
                    while attempts3 < max_attempts3:
                        if not xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                            xbmc.log(f"REMOD INSTALADOR instalado {addon_id}", level=xbmc.LOGINFO)
                            return True
                        else:
                            xbmc.log(f"REMOD INSTALADOR Se está terminando de instalar {addon_id}", level=xbmc.LOGINFO)
                            xbmc.sleep(100)
                            attempts3 += 1
                    xbmc.log(f"Tiempo max2 superado {addon_id}", level=xbmc.LOGERROR)
                    return False
                else:
                    xbmc.sleep(500)  # Pequeña pausa entre intentos
                    attempts2 += 1
            xbmc.log(f"Tiempo max superado {addon_id}", level=xbmc.LOGERROR)
            return False    
        xbmc.sleep(500)  # Pequeña pausa entre intentos
        attempts += 1
    return False


def buscar_actualizacion_addons():
    xbmc.log(f"REMOD INSTALADOR Actualizando Addons locales", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f"UpdateLocalAddons()", True)
    xbmc.sleep(1000)

def buscar_actualizacion_repos():
    xbmc.log(f"REMOD INSTALADOR Actualizando Addon Repos", level=xbmc.LOGINFO)
    xbmc.executebuiltin(f"UpdateAddonRepos()", True)
    xbmc.sleep(1000)

def buscar_actualizacion():
    xbmc.log(f"REMOD INSTALADOR Actualizando Repos y Addons...", level=xbmc.LOGINFO)
    buscar_actualizacion_repos()
    buscar_actualizacion_addons()

### instalar dependencias
def instalar_lista_addons(lista_deps):
    for addon_id in lista_deps:
        ### si está instalado y activado
        if addon_instalado_y_activado_comp(addon_id):
            xbmc.log(f"REMOD INSTALADOR {addon_id} ya instalado y activado", level=xbmc.LOGINFO)
            continue
        ### si no lo está, se instala
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no está instalado", level=xbmc.LOGINFO)
        # Construye el comando de instalación
        instalar = f"InstallAddon({addon_id}, True)"
        xbmc.log(f"REMOD INSTALADOR Lanzamos instalación {addon_id}", xbmc.LOGINFO)
        # Ejecuta el comando
        xbmc.executebuiltin(instalar)
        xbmc.log(f"REMOD INSTALADOR Confirmamos instalación botón yes instalación {addon_id}", level=xbmc.LOGINFO)
        if addon_inst_confirm(addon_id):
            xbmc.log(f"REMOD INSTALADOR {addon_id} Fin instalación OK", level=xbmc.LOGINFO)
            xbmc.sleep(1000)
            if addon_instalado_y_activado_comp(addon_id):
                continue
            else:
                xbmc.log(f"REMOD INSTALADOR Error al confirmar instalación o activación {addon_id}", level=xbmc.LOGERROR)
                xbmc.sleep(1000)
                return False
        else:
            xbmc.log(f"REMOD INSTALADOR Error al confirmar instalación {addon_id}", level=xbmc.LOGERROR)
            xbmc.sleep(1000)
            return False
    xbmc.log(f"REMOD INSTALADOR Error instalando lista addons dependencias", level=xbmc.LOGERROR)
    return True
  
  
### instala lista de repos zip desde fuentes
# def descargar_lista_repos_zip(repo_ids,base_urls_ids,lista_patterns):
    # for addon_id, base_url, pattern in zip(repo_ids, base_urls_ids, lista_patterns):
        # if addon_instalado_y_activado_comp(addon_id):
            # continue
            
        # xbmc.log(f"REMOD INSTALADOR Descargando {addon_id}", level=xbmc.LOGINFO)
        ## config func
        # download_path = os.path.join(addons_home, 'packages')
        ## Realizar la solicitud GET
        # xbmc.log(f"REMOD INSTALADOR Buscando {repo_ids} zip", level=xbmc.LOGINFO)
        # with urllib.request.urlopen(base_url) as response:
            # html = response.read().decode()
        ## Buscar el patrón del archivo zip
        # match = re.search(pattern, html)
        # if match:
            # xbmc.log(f"REMOD INSTALADOR Archivo {repo_ids} zip encontrado", level=xbmc.LOGINFO)
            # download_url = f"{base_url}{match.group(0)}"
            # res = download_zip_from_url(download_url)
            # if res:
                # res = addon_inst_confirm(addon_id)
                # if res:
                    # return True
            # else:
                # xbmc.log(f"REMOD INSTALADOR Error {repo_ids} zip no encontrado", level=xbmc.LOGERROR)
                # return False
        # else:
            # xbmc.log(f"REMOD INSTALADOR Archivo {repo_ids} zip no encontrado", level=xbmc.LOGERROR)
            # return False
    # xbmc.log(f"REMOD INSTALADOR Fin descargando lista repos zip desde url", level=xbmc.LOGINFO)
    # return True

  
### instala lista de repos zip desde fuentes
# -*- coding: utf-8 -*-
"""
REMOD INSTALADOR – descarga y extracción de ZIPs de repositorios
Compatible con Kodi Omega 21 (Python 3.9)
"""


################# nuevo extract

addons_home = Path(xbmcvfs.translatePath("special://home/addons"))   # raíz de los addons

# ----------------------------------------------------------------------
# LOGGING (usa el mismo logger que Kodi)
# ----------------------------------------------------------------------
log = logging.getLogger("script.REMOD_INSTALADOR")
log.setLevel(logging.INFO)


# ----------------------------------------------------------------------
# UTILIDADES DE KODI ---------------------------------------------------
# ----------------------------------------------------------------------
def addon_instalado_y_activado_comp(addon_id: str) -> bool:
    """
    Comprueba si un addon está instalado y habilitado.
    """
    addon_path = addons_home / addon_id

    # <-- CORRECCIÓN: .is_dir() en lugar de .isdir() -->
    if not addon_path.is_dir():
        xbmc.log(
            f"REMOD INSTALADOR – {addon_id} no está instalado (carpeta falta).",
            xbmc.LOGINFO,
        )
        return False

    # Estado de habilitación (KODI >= 19)
    enabled = xbmc.getAddonInfo(addon_id, "enabled") == "true"
    if not enabled:
        xbmc.log(
            f"REMOD INSTALADOR – {addon_id} está instalado pero deshabilitado.",
            xbmc.LOGINFO,
        )
    else:
        xbmc.log(
            f"REMOD INSTALADOR – {addon_id} ya está instalado y habilitado.",
            xbmc.LOGINFO,
        )
    return enabled


# def addon_inst_confirm(addon_id: str) -> bool:
    # """
    # Fuerza la recarga del addon recién instalado y verifica que exista.
    # """
    # xbmc.log(
        # f"REMOD INSTALADOR – Actualizando lista de addons tras instalar {addon_id}.",
        # xbmc.LOGINFO,
    # )
    # xbmc.executebuiltin("UpdateLocalAddons")
    # xbmc.sleep(2000)          # 2 s (equivalente a time.sleep(2))

    # if addon_instalado_y_activado_comp(addon_id):
        # xbmc.log(
            # f"REMOD INSTALADOR – Confirmado que {addon_id} está instalado.",
            # xbmc.LOGINFO,
        # )
        # return True
    # else:
        # xbmc.log(
            # f"REMOD INSTALADOR – No se detectó {addon_id} después de la actualización.",
            # xbmc.LOGERROR,
        # )
        # return False


# ----------------------------------------------------------------------
# Helper: abrir URL con User‑Agent y reintentos exponenciales
# ----------------------------------------------------------------------
def _urlopen_with_retry(
    url: str,
    timeout: int = 15,
    max_tries: int = 3,
    backoff: int = 2,
) -> bytes:
    """
    Intenta abrir la URL usando urllib.request.
    Añade una cabecera de navegador y reintenta (exponencial) si falla.
    Devuelve el contenido en bytes.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    req = urllib.request.Request(url, headers=headers)

    for attempt in range(1, max_tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            xbmc.log(
                f"REMOD INSTALADOR – HTTPError {e.code} al acceder a {url} "
                f"(intento {attempt}/{max_tries})",
                xbmc.LOGWARNING,
            )
            if attempt == max_tries:
                raise
        except urllib.error.URLError as e:
            xbmc.log(
                f"REMOD INSTALADOR – URLError {e.reason} al acceder a {url} "
                f"(intento {attempt}/{max_tries})",
                xbmc.LOGWARNING,
            )
            if attempt == max_tries:
                raise

        # backoff está en segundos → convertimos a milisegundos para xbmc.sleep
        xbmc.sleep(backoff ** attempt * 1000)


# ----------------------------------------------------------------------
# Descargar ZIP a un archivo temporal
# ----------------------------------------------------------------------
def download_zip(url: str, dest_dir: Path) -> Optional[Path]:
    """
    Descarga el ZIP indicado y lo guarda en ``dest_dir`` con nombre temporal.
    Devuelve la ruta del archivo o ``None`` si ocurre algún error.
    """
    xbmc.log(f"REMOD INSTALADOR – Iniciando descarga: {url}", xbmc.LOGINFO)

    try:
        data = _urlopen_with_retry(url)
    except Exception as exc:
        xbmc.log(f"REMOD INSTALADOR – Error al descargar {url}: {exc}", xbmc.LOGERROR)
        return None

    filename = Path(urllib.parse.urlparse(url).path).name or "repo.zip"
    tmp_path = dest_dir / f".tmp_{filename}"

    try:
        with open(tmp_path, "wb") as fp:
            fp.write(data)
        xbmc.log(f"REMOD INSTALADOR – ZIP guardado en: {tmp_path}", xbmc.LOGINFO)
        return tmp_path
    except OSError as exc:
        xbmc.log(f"REMOD INSTALADOR – No se pudo escribir {tmp_path}: {exc}", xbmc.LOGERROR)
        return None


# ----------------------------------------------------------------------
# Extraer ZIP directamente en la raíz de los addons
# ----------------------------------------------------------------------
def extract_zip(zip_path: Path, addons_home: Path) -> bool:
    """
    Descomprime ``zip_path`` dentro de la carpeta raíz de los addons
    (``addons_home``).  Devuelve True si la extracción fue exitosa,
    False en caso de error.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad = zf.testzip()
            if bad:
                raise zipfile.BadZipFile(f"Archivo corrupto: {bad}")

            zf.extractall(addons_home)

        xbmc.log(
            f"REMOD INSTALADOR – ZIP extraído en: {addons_home}",
            xbmc.LOGINFO,
        )
        return True

    except (zipfile.BadZipFile, OSError) as exc:
        xbmc.log(
            f"REMOD INSTALADOR – Falló extracción {zip_path}: {exc}",
            xbmc.LOGERROR,
        )
        return False


# ----------------------------------------------------------------------
# Procesar un único repositorio
# ----------------------------------------------------------------------
def process_repo(
    addon_id: str,
    base_url: str,
    pattern: str,
    packages_dir: Path,
) -> bool:
    """
    Busca, descarga y extrae el ZIP que coincide con ``pattern`` en ``base_url``.
    Devuelve True si el proceso termina sin errores.
    """
    # 1️⃣ Ya está instalado/activado?
    if addon_instalado_y_activado_comp(addon_id):
        xbmc.log(f"REMOD INSTALADOR – {addon_id} ya está instalado.", xbmc.LOGINFO)
        return True

    xbmc.log(f"REMOD INSTALADOR – Procesando {addon_id} desde {base_url}", xbmc.LOGINFO)

    # 2️⃣ Obtener HTML de la página
    try:
        html_bytes = _urlopen_with_retry(base_url)
        html = html_bytes.decode(errors="ignore")
    except Exception as exc:
        xbmc.log(f"REMOD INSTALADOR – No se pudo leer {base_url}: {exc}", xbmc.LOGERROR)
        return False

    # 3️⃣ Buscar el nombre del ZIP mediante la expresión regular
    match = re.search(pattern, html)
    if not match:
        xbmc.log(f"REMOD INSTALADOR – Patrón no encontrado en {base_url}", xbmc.LOGERROR)
        return False

    zip_name = match.group(0)
    download_url = f"{base_url.rstrip('/')}/{zip_name.lstrip('/')}"
    xbmc.log(f"REMOD INSTALADOR – URL del ZIP: {download_url}", xbmc.LOGINFO)

    # 4️⃣ Descargar ZIP
    zip_path = download_zip(download_url, packages_dir)
    if not zip_path:
        return False

    # 5️⃣ Extraer ZIP directamente en la raíz de los addons
    ok = extract_zip(zip_path, addons_home)

    # 6️⃣ Limpiar archivo temporal
    try:
        zip_path.unlink()
    except OSError:
        pass

    if not ok:
        return False

    # 7️⃣ Confirmar instalación del addon
    if addon_inst_confirm(addon_id):
        xbmc.log(f"REMOD INSTALADOR – {addon_id} instalado correctamente.", xbmc.LOGINFO)
        return True
    else:
        xbmc.log(f"REMOD INSTALADOR – Falló confirmación de {addon_id}.", xbmc.LOGERROR)
        return False


# ----------------------------------------------------------------------
# Función principal – recorre toda la lista de repositorios
# ----------------------------------------------------------------------
def descargar_lista_repos_zip(
    repo_ids: list,
    base_urls_ids: list,
    lista_patterns: list,
) -> bool:
    """
    Recorre los repositorios indicados, descarga y extrae sus ZIP.
    Si un addon ya está instalado y activo, lo salta (no lo vuelve a descargar).

    Devuelve True si **todos** los repos fueron procesados sin errores críticos
    (aunque algunos puedan haber sido omitidos porque ya estaban instalados).
    """
    packages_dir = addons_home / "packages"
    packages_dir.mkdir(parents=True, exist_ok=True)

    all_ok = True

    for addon_id, base_url, pattern in zip(repo_ids, base_urls_ids, lista_patterns):
        # --------------------------------------------------------------
        # 1️⃣  COMPROBAR SI YA ESTÁ INSTALADO/Y ACTIVADO
        # --------------------------------------------------------------
        if addon_instalado_y_activado_comp(addon_id):
            xbmc.log(
                f"REMOD INSTALADOR – {addon_id} ya está instalado y activo; se omite.",
                xbmc.LOGINFO,
            )
            # No llamamos a `process_repo`; pasamos al siguiente elemento
            continue

        # --------------------------------------------------------------
        # 2️⃣  PROCESAR REPOSITORIO (descarga + extracción)
        # --------------------------------------------------------------
        if not process_repo(addon_id, base_url, pattern, packages_dir):
            all_ok = False
            xbmc.log(
                f"REMOD INSTALADOR – Problema con {addon_id}; continúo con los demás.",
                xbmc.LOGWARNING,
            )

    xbmc.log("REMOD INSTALADOR – Fin de descarga de lista de repos ZIP.", xbmc.LOGINFO)
    return all_ok

##########



 
### activar lista de repos descargada desde url como zip
def activar_lista_repos_zip(lista_repos):
    for addon_id in lista_repos:
        if addon_instalado_y_activado_comp(addon_id):
            continue
            
        ### verificamos si esta instalado
        xbmc.log(f"REMOD INSTALADOR 0. {addon_id} Comprobando instalación", level=xbmc.LOGINFO)
        if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        # if res:
            xbmc.log(f"REMOD INSTALADOR 1. {addon_id} está ya instalado. Comprobando activación", level=xbmc.LOGINFO)
            addon_act_des(addon_id, True)
         ### Si está desactivado, lo activamos
            ### confirma activación
            addon_activado_check(addon_id)
        else:
            if addon_inst_confirm(addon_id):
                xbmc.log(f"REMOD INSTALADOR 2. Activada Lista de repos zip Fin", level=xbmc.LOGINFO)
                return True
            else:
                xbmc.log(f"REMOD INSTALADOR 3. Error Activando Lista de repos zip, usando otro método", level=xbmc.LOGERROR)
            ### activamos el addon con otro método
                if lista_addons(addon_id, True):
                    xbmc.sleep(1000)
                    if addon_activado_check(addon_id):
                        xbmc.log(f"REMOD INSTALADOR 4. Activada Lista de repos zip Fin", level=xbmc.LOGINFO)
                        return True
                    else:
                        xbmc.log(f"REMOD INSTALADOR 5. Error definitivo activando Lista de repos zip Fin", level=xbmc.LOGERROR)
                        return False
                else:
                    xbmc.log(f"REMOD INSTALADOR 5. Error Activada Lista de repos zip Fin", level=xbmc.LOGERROR)
                    return False
    return True
    
def is_addon_enabled_from_xml(addon_id):
    """
    Busca el archivo addon.xml del addon instalado y comprueba
    si contiene <disabled>true</disabled>.
    Si el nodo <disabled> no está presente o vale 'false', el addon está habilitado.
    """
    try:
        # Instancia del addon – lanza RuntimeError si no está instalado
        addon = xbmcaddon.Addon(addon_id)
    except RuntimeError:
        return False                     # No está instalado

    # Ruta al directorio del addon
    addon_path = addon.getAddonInfo('path')
    xml_path   = os.path.join(addon_path, 'addon.xml')

    if not os.path.isfile(xml_path):
        # En teoría siempre debería existir, pero si falta asumimos deshabilitado
        return False

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        disabled_elem = root.find('disabled')
        if disabled_elem is not None and disabled_elem.text.strip().lower() == 'true':
            return False                 # Marcado como deshabilitado
        return True                      # No está deshabilitado → habilitado
    except Exception:
        # Si ocurre cualquier error de parsing, devolvemos False para ser conservadores
        return False
        
### comprobamos si está instalado y activado antes de descargar e isntalar otra vez        
def addon_instalado_y_activado_comp(addon_id):
    ### comprobar si está instalado
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.log(f"El addon {addon_id} está instalado pero no sabmeos si está activado", level=xbmc.LOGINFO)
        ### comprobar si está activado
        if is_addon_enabled_from_xml(addon_id):
            xbmc.log(f"REMOD INSTALADOR El addon {addon_id} instalado y activado", level=xbmc.LOGINFO)
            return True
        else:
            xbmc.log(f"REMOD INSTALADOR El addon {addon_id} instalado pero desactivado", level=xbmc.LOGERROR)
            return False
    else:
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no instalado", level=xbmc.LOGERROR)
        return False

### acciones del menu principal
if not ARGS:
    # No hay parámetros → menú principal
    lista_menu_principal()
else:
    action = ARGS.get('action', [None])[0]
    if action == "info":
        buscar_actualizacion()
    elif action == "deportes":
        lista_menu_deportes()
    elif action == "cine":
        lista_menu_cine()
    elif action == "herramientas":
        lista_menu_herramientas()
        
    elif action == "remodtv":        
        ### descarga addons zip desde url
        lista_repos = ["repository.remod"]
        lista_base_urls = ["https://saratoga79.github.io/"]
        lista_patterns = ["repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.program.remodtv"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando ReMod TV,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación ReMod TV,3000,{noti_ok_icon})")
            xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=tv)')
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación ReMod TV,3000,{noti_error_icon})")
            
    elif action == "kodispaintv":
        lista_repos = ["repository.gujal"]
        lista_base_urls = ["https://gujal00.github.io/"]
        lista_patterns = ["repository\.gujal-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "script.module.six",
            "script.module.kodi-six",
            "script.module.requests",
            "script.module.certifi",
            "script.module.chardet",
            "script.module.idna",
            "script.module.urllib3",
            "script.module.beautifulsoup4",
            "script.module.soupsieve",
            "script.module.html5lib",
            "script.module.webencodings",
            "script.module.dateutil",
            "script.module.websocket",
            "script.module.addon.signals",
            "script.module.pyxbmct",
            "script.module.resolveurl",
            ]
            
        ### instalar addon zip desde url fuente
        if instalar_lista_addons(lista_deps):
            lista_repos = ['plugin.video.kodispaintv']
            lista_base_urls = ["https://konectas.github.io/Addons%20Video/"]
            lista_patterns = ["plugin\.video\.kodispaintv-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando KodispainTv,1000,{noti_icon})")
            descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
            buscar_actualizacion()
            activar_lista_repos_zip(lista_repos)
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación KodispainTv,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación KodispainTv,3000,{noti_error_icon})")
            
    elif action == "tacones":
        ### descarga addons zip desde url
        lista_repos = ["repository.remod"]
        lista_base_urls = ["https://saratoga79.github.io/"]
        lista_patterns = ["repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "script.module.six",
            "script.module.kodi-six",
            "script.module.requests",
            "script.module.certifi",
            "script.module.chardet",
            "script.module.idna",
            "script.module.urllib3",
            "script.module.beautifulsoup4",
            "script.module.soupsieve",
            "script.module.html5lib",
            "script.module.webencodings",
            "script.module.dateutil",
            "script.module.websocket",
            "script.module.addon.signals",
            "script.module.pyxbmct",
            "script.module.resolveurl",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando dependencias,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            lista_repos = ["plugin.video.tacones"]
            lista_base_urls = ["https://konectas.github.io/Addons%20Video/"]
            lista_patterns = ["plugin\.video\.tacones-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando Tacones,1000,{noti_icon})")
            descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
            ### actualizar lista de addons para refrersacar addons descargados
            buscar_actualizacion()
            ### activar addons descargados
            activar_lista_repos_zip(lista_repos)
            ### actualizar lista de repos descargados
            buscar_actualizacion()
        
            ### instalación elementum
            lista_deps = ["plugin.video.elementum"]
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Elementum,1000,{noti_icon})")
            if instalar_lista_addons(lista_deps):
                ### desactivando burst
                addon_set = xbmcaddon.Addon('plugin.video.elementum')
                addon_set.setSettingBool('skip_burst_search', True)
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin instalación Tacones,3000,{noti_ok_icon})")
            else:
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Elementum,3000,{noti_error_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Tacones,3000,{noti_error_icon})")

    elif action == "acs_channels":
        buscar_actualizacion()
        ### descarga addons zip desde url
        lista_repos = [
            "repository.acestream-channels",
            "repository.remod",
            ]
        lista_base_urls = [
            "https://gunter257.github.io/repoachannels/",
            "https://saratoga79.github.io/",
            ]
        lista_patterns = [
            "repository\.acestream-channels\.zip",
            "repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip",        
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "plugin.video.acestream_channels",
            "script.module.horus",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Acestream Channels,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            if xbmc.getCondVisibility('system.platform.android'):
                xbmc.log(f"REMOD INSTALADOR Activando Reproductor Externo en Horus en Android", level=xbmc.LOGINFO)
                addon_set = xbmcaddon.Addon('script.module.horus')
                addon_set.setSettingBool('reproductor_externo', True)
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación AceStream Channels,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Acestream Channels,3000,{noti_error_icon})")
        
    elif action == "balandro":
        ### descarga addons zip desde url
        lista_repos = ["repository.balandro"]
        lista_base_urls = ["https://repobal.github.io/base/"]
        lista_patterns = ["repository\.balandro-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.video.balandro"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Balandro,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Balandro,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Balandro,3000,{noti_error_icon})")
        
    elif action == "magellan":
        ### descarga addons zip desde url
        lista_repos = [
            "repository.magellan",
            "repository.remod",
            ]
        lista_base_urls = [
            "https://euro2000.github.io/magellan.github.io/",
            "https://saratoga79.github.io/",
            ]
        lista_patterns = [
            "repository\.magellan\.zip",
            "repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "script.module.six",
            "script.module.kodi-six",
            "script.module.requests",
            "script.module.dateutil",
            "script.module.websocket",
            "script.module.addon.signals",
            "script.module.beautifulsoup4",
            "script.module.certifi",
            "script.module.chardet",
            "script.module.idna",
            "script.module.urllib3",
            "script.module.html5lib",
            "script.module.pyxbmct",
            "script.module.soupsieve",
            "script.module.webencodings",
            "script.module.resolveurl",
            "plugin.video.Magellan_Matrix",
            "plugin.video.f4mTester",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Magellan,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Magellan,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Magellan,3000,{noti_error_icon})")
        
    elif action == "alfa":
        ### descarga addons zip desde url
        lista_repos = ["repository.alfa-addon"]
        lista_base_urls = ["https://alfa-addon.com/alfa/"]
        lista_patterns = ["repository\.alfa-addon\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.video.alfa"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Alfa,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Alfa,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Alfa,3000,{noti_error_icon})")
        
    elif action == "moes":
        lista_repos = ["repository.remod"]
        lista_base_urls = ["https://saratoga79.github.io/"]
        lista_patterns = ["repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### instalación duffyou y moes
        lista_deps = [
            "plugin.video.duffyou",
            "plugin.video.moestv",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Moe's TV,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Moe's TV,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Moe's TV,3000,{noti_error_icon})")
        
    elif action == "espadaily":
        ### descarga addons zip desde url
        lista_repos = ["repository.espadaily"]
        lista_base_urls = ["https://fullstackcurso.github.io/espadaily/"]
        lista_patterns = ["repository\.espadaily-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.video.espadaily"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando EspaDaily,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación EspaDaily,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación EspaDaily,3000,{noti_error_icon})")
            
    elif action == "jacktook":
        lista_repos = [
            "repository.remod",
            "repository.jacktook",
            ]
        lista_base_urls = [
            "https://saratoga79.github.io/",
            "https://sam-max.github.io/repository.jacktook/",
            ]
        lista_patterns = [
            "repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip",
            "repository\.jacktook-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
                
        ### instalación elementum y jacktook
        lista_deps = ["plugin.video.jacktook"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Jacktook,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Jacktook instalado,1000,{noti_icon})")
            ### configurando ajustes
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Configurando JackTook,3000,{noti_icon})")
            addon_set = xbmcaddon.Addon('plugin.video.jacktook')
            addon_set.setSettingBool('torrentio_enabled', True)
            addon_set.setSettingBool('auto_audio', True)
            addon_set.setSettingBool('auto_subtitle_selection', True)
            addon_set.setSettingBool('super_quick_play', True)
            addon_set.setSettingBool('include_tvshow_specials', True)
            addon_set.setSetting('auto_audio_language', 'Spanish')
            addon_set.setSettingInt('language', 20)
            addon_set.setSetting('subtitle_language', 'Spanish')
            addon_set.setSetting('torrent_client', 'Elementum')      
            xbmc.sleep(1000)
            
            ### desactivamos el addon para copiar
            addons = [
                "script.module.routing",
                "plugin.video.jacktook",
                ]
            lista_addons(addons, False)
            xbmc.sleep(1000)
            
            ### copia seguridad archivos originales jacktook
            xbmc.log(f"REMOD INSTALADOR Haciendo copia de router.py", level=xbmc.LOGINFO)
            orig = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'router.py'))
            dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'router.py.bak'))
            if xbmcvfs.exists(orig):                
                xbmcvfs.copy(orig, dest)
                if xbmcvfs.exists(dest):                
                    xbmcvfs.delete(orig)
                    
            xbmc.log(f"REMOD INSTALADOR Haciendo copia de addon_selection_remod.py", level=xbmc.LOGINFO)
            orig = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'addon_selection.py'))
            dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'addon_selection.py.bak'))
            if xbmcvfs.exists(orig):                
                xbmcvfs.copy(orig, dest)
                if xbmcvfs.exists(dest):                
                    xbmcvfs.delete(orig)
                    
            xbmc.log(f"REMOD INSTALADOR Haciendo copia de utils.py", level=xbmc.LOGINFO)
            orig = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils.py'))
            dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils.py.bak'))
            if xbmcvfs.exists(orig):                
                xbmcvfs.copy(orig, dest)
                if xbmcvfs.exists(dest):                
                    xbmcvfs.delete(orig)
                        
            ### copia archivos remod
            xbmc.log(f"REMOD INSTALADOR Copiando router_remod.py", level=xbmc.LOGINFO)
            orig = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_datos, 'plugin.video.jacktook', 'lib', 'router_remod.py'))
            dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'router.py'))
            xbmcvfs.delete(dest)
            xbmcvfs.copy(orig, dest)
            xbmc.log(f"REMOD INSTALADOR Copiando addon_selection_remod.py", level=xbmc.LOGINFO)
            orig = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_datos, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'addon_selection_remod.py'))
            dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'addon_selection.py'))
            xbmcvfs.delete(dest)
            xbmcvfs.copy(orig, dest)
            xbmc.log(f"REMOD INSTALADOR Copiando utils_remod.py", level=xbmc.LOGINFO)
            orig = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_datos, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils_remod.py'))
            dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils.py'))
            xbmcvfs.delete(dest)
            xbmcvfs.copy(orig, dest)
            
            ### reactivamos el addon tras copiar
            addons = [
                "script.module.routing",
                "plugin.video.jacktook",
                ]
            lista_addons(addons, True)
            xbmc.sleep(1000)
            ### añadir complementos custom stremnio
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=add_ext_custom_stremio_addon)')      
            xbmc.sleep(3000)
            ### añadir proveedores torrentio
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=torrentio_selection)')
            addon_id = ("plugin.video.jacktook")
            dialog_aceptar_confirm(addon_id)
            xbmc.sleep(3000)
            ### activar proveedores torrentio en ajustes
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=torrentio_toggle_providers)')
            addon_id = ("plugin.video.jacktook")
            multiselect_aceptar_confirm(addon_id)      
            xbmc.sleep(5000)
            
            ### instalamos elementum
            lista_deps = ["plugin.video.elementum"]
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Elementum,1000,{noti_icon})")
            if instalar_lista_addons(lista_deps):
                ### desactivando burst
                addon_set = xbmcaddon.Addon('plugin.video.elementum')
                addon_set.setSettingBool('skip_burst_search', True)

                ### desactivamos el addon para restaurar
                addons = [
                    "script.module.routing",
                    "plugin.video.jacktook",
                    ]
                lista_addons(addons, False)        
                xbmc.sleep(1000)
                ### restaura archivos originales jacktook
                xbmc.log(f"REMOD INSTALADOR Restaurando router.py", level=xbmc.LOGINFO)
                orig = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'router.py.bak'))
                dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'router.py'))
                if xbmcvfs.exists(orig):                
                    xbmcvfs.copy(orig, dest)
                    if xbmcvfs.exists(dest):                
                        xbmcvfs.delete(orig)
                        
                xbmc.log(f"REMOD INSTALADOR Restaurando addon_selection_remod.py", level=xbmc.LOGINFO)
                orig = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'addon_selection.py.bak'))
                dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'addon_selection.py'))
                if xbmcvfs.exists(orig):                
                    xbmcvfs.copy(orig, dest)
                    if xbmcvfs.exists(dest):                
                        xbmcvfs.delete(orig)
                        
                xbmc.log(f"REMOD INSTALADOR Restaurando utils.py", level=xbmc.LOGINFO)
                orig = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils.py.bak'))
                dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils.py'))
                if xbmcvfs.exists(orig):                
                    xbmcvfs.copy(orig, dest)
                    if xbmcvfs.exists(dest):                
                        xbmcvfs.delete(orig)
                        
                ### reaactivamos el addon tras restaurar
                addons = [
                    "script.module.routing",
                    "plugin.video.jacktook",
                    ]
                lista_addons(addons, True)        
                xbmc.sleep(1000)
            
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin instalación Jacktook,3000,{noti_ok_icon})")
            else:
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Elementum,3000,{noti_error_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Jacktook,3000,{noti_error_icon})")
                
    elif action == "loop":
        ### descarga addons zip desde url
        lista_repos = ["repository.loop"]
        lista_base_urls = ["https://loopaddon.uk/theloop/"]
        lista_patterns = ["repository\.loop-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando repo The Loop desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "script.module.unidecode",
            "script.module.tzdata",
            "script.module.tzlocal",
            "script.module.backports.zoneinfo",
            "script.module.pyairtable",
            "script.module.defusedxml",
            "script.module.pyamf",
            "script.module.pyjsparser",
            "script.module.jetextractors",
            "script.module.pytz",
            "script.module.future",
            "plugin.video.looptv",
            "plugin.video.dailymotion_com",
            "plugin.video.the-loop",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando The Loop,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación The Loop,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación The Loop,3000,{noti_error_icon})")
        
    elif action == "ezmaintenanceplus":
        ### descarga addons zip desde url
        lista_repos = ["repository.remod"]
        lista_base_urls = ["https://saratoga79.github.io/"]
        lista_patterns = ["repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        if activar_lista_repos_zip(lista_repos):
            ### actualizar lista de repos descargados
            buscar_actualizacion()
            ### instalación de addons desde repo ya instalado
            lista_deps = ["script.ezmaintenanceplus"]
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando EZMaintenance+,1000,{noti_icon})")
            if instalar_lista_addons(lista_deps):
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación EZMaintenance+,3000,{noti_ok_icon})")
            else:
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación EZMaintenance+,3000,{noti_error_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error activando zip descargado,3000,{noti_error_icon})")
        
    elif action == "log_viewer":
        ### instalación de addons desde repo ya instalado
        lista_deps = ["script.logviewer"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Log Viewer,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            ### configuración log viewer
            addon_set = xbmcaddon.Addon('script.logviewer')
            addon_set.setSettingBool('custom_window', True)
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Log Viewer,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Log Viewer,3000,{noti_error_icon})")   
            
    elif action == "backup":
        ### instalación de addons desde repo ya instalado
        lista_deps = ["script.xbmcbackup"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Kodi Backup,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Kodi Backup,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Kodi Backup,3000,{noti_error_icon})")   
            
    elif action == "naranjito":
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "script.module.requests",
            "script.module.simplejson",
            "script.module.kodi-six",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando dependencias,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            ### descarga addons zip desde url
            lista_repos = [
                "plugin.video.Naranjitomatrix",
                "repository.remod",
                ]
            lista_base_urls = [
                "https://whoisnoze.github.io/KRAE/",
                "https://saratoga79.github.io/",
                ]
            lista_patterns = [
                "plugin\.video\.Naranjitomatrix\.zip",
                "repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip",
                ]
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
            descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
            ### actualizar lista de addons para refrersacar addons descargados
            buscar_actualizacion()
            ### activar addons descargados
            if activar_lista_repos_zip(lista_repos):
                ### instalación de addons desde repo ya instalado
                lista_deps = ["script.module.horus"]
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Horus,1000,{noti_icon})")
                if instalar_lista_addons(lista_deps):
                    if xbmc.getCondVisibility('system.platform.android'):
                        xbmc.log(f"REMOD INSTALADOR Activando Reproductor Externo en Horus en Android", level=xbmc.LOGINFO)
                        addon_set = xbmcaddon.Addon('script.module.horus')
                        addon_set.setSettingBool('reproductor_externo', True)
                    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Naranjito,3000,{noti_ok_icon})")
                else:
                    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Naranjito,3000,{noti_error_icon})")
                
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Naranjito,3000,{noti_ok_icon})")
                
            else:
                xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación Naranjito,3000,{noti_error_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalando dependencias Naranjito,3000,{noti_error_icon})")
        
    elif action == "sporthd":
        ### descarga addons zip desde url
        lista_repos = ["repository.bugatsinho"]
        lista_base_urls = ["https://bugatsinho.github.io/"]
        lista_patterns = ["repository\.bugatsinho-\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando zip desde fuente,1000,{noti_icon})")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        activar_lista_repos_zip(lista_repos)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "script.module.dateutil",
            "script.module.six",
            "script.module.requests",
            "plugin.video.sporthdme",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando SportHD,1000,{noti_icon})")
        if instalar_lista_addons(lista_deps):
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación SportHD,3000,{noti_ok_icon})")
        else:
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error instalación SportHD,3000,{noti_error_icon})")
            

    elif action == "test":
        ### añadir complementos custom stremnio
        # xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=add_ext_custom_stremio_addon)')      
        xbmc.sleep(3000)
        ### añadir proveedores torrentio
        # xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=torrentio_selection)')
        addon_id = ("plugin.video.jacktook")
        dialog_aceptar_confirm(addon_id)
        xbmc.sleep(3000)
        ### activar proveedores torrentio en ajustes
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=torrentio_toggle_providers)')
        addon_id = ("plugin.video.jacktook")
        multiselect_aceptar_confirm(addon_id)      
        xbmc.sleep(5000)
            
    
        pass

    else:
        ### Acción desconocida → volver al menú principal
        lista_menu_principal()
