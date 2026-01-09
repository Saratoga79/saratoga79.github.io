#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "info.png"),
        ("> Sección Deportes", "deportes", "stadium.png"),
        ("> Sección Cine & TV", "cine", "cinema.png"),
        ("> Sección Herramientas", "herramientas", "herramientas.png")
        # ("> Test", "test", ""),
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
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "info.png"),
        ("> Instalar ReMod TV", "remodtv", "remodtv.png"),
        ("> Instalar [COLOR red]Kodi[/COLOR][COLOR yellow]Spain[/COLOR][COLOR red]Tv[/COLOR]", "kodispaintv", "kodispaintv.png"),
        ("> Instalar AceStream Channels", "acs_channels", "acs_channels.png"),
        ("> Instalar StreamedEZ", "streamedez", "streamedez.png")
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
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "info.png"),
        ("> Instalar Jacktook ReMod | Películas & Series Stremio | TV en vivo Ace Stream", "jacktook", "jacktook.png"),
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
        (f"{remod_instalador_addon_name} versión: {remod_instalador_addon_version} | Buscar actualizaciones", "info", "info.png"),
        ("> Instalar EZMaintenance+", "ezmaintenanceplus", "ezmaintenance.png")
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
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Addon activado,1000,)")
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
         xbmc.log(f"REMOD INSTALADOR Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
         # Verificar si el diálogo de confirmación está visible
         if xbmc.getCondVisibility(f"Window.IsVisible(12000)"):
            xbmc.log(f"REMOD INSTALADOR Espereando visibilidad botón yes para activar addon zip", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Action(Right)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"Action(Right)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"Action(Select)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Addon activado,1000,)")
            xbmc.log(f"REMOD INSTALADOR Intentando click yes para activar addon zip", level=xbmc.LOGINFO)
            return True
         else:   
            xbmc.sleep(500)
            attempts += 1
    return False
    
# hacer click en yes en diálogo de confirmación
def dialog_aceptar_confirm(addon_id):
    max_attempts = 5  # Número máximo de intentos
    attempts = 0
    while attempts < max_attempts:
        xbmc.log(f"REMOD INSTALADOR Esperando visibilidad para Aceptar", level=xbmc.LOGINFO)
        # Verificar si el diálogo de confirmación está visible
        if xbmc.getCondVisibility(f"Window.IsVisible(12002)"):
            xbmc.log(f"REMOD INSTALADOR Intentando hacer click en Aceptar", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Action(Left)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            return True
        else:
            xbmc.log(f"REMOD INSTALADOR No se detecta visibilidad para Aceptar", level=xbmc.LOGINFO)
            xbmc.sleep(500)
            attempts += 1
        # si ya están añadidos de antes, la pantalla cambia
        if xbmc.getCondVisibility(f"Window.IsVisible(10100)"):
            xbmc.log(f"REMOD INSTALADOR Intentando hacer click en Aceptar", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Action(Left)", True)
            xbmc.sleep(100)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            xbmc.executebuiltin(f"SendClick(11)", True)
            xbmc.sleep(1000)
            return True
        else:
            xbmc.log(f"REMOD INSTALADOR No se detecta visibilidad para Aceptar", level=xbmc.LOGINFO)
            xbmc.sleep(500)
            attempts += 1
    return False

# comprobar addon activado ya
def addon_activado_check(addon_id):
    ### activar addon tras el reinicio
    existe = xbmcvfs.exists(xbmcvfs.translatePath(os.path.join(addons_home, addon_id, 'ok')))
    if not existe:
        xbmc.log(f"REMOD INSTALADOR Activando {addon_id}", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f'EnableAddon({addon_id})')
        addon_activacion_confirm(addon_id)
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
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addon,1000,)")
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
        xbmc.log(f"REMOD INSTALADOR Fin download_zip_from_url", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD INSTALADOR Iniciando extract_zip", level=xbmc.LOGINFO)
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
            xbmc.log(f"REMOD INSTALADOR Archivo zip extraido", level=xbmc.LOGINFO)
            return True
        xbmc.log(f"REMOD INSTALADOR Fin extract_zip", level=xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"REMOD INSTALADOR Error al extraer archivo", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error al extraer archivo,3000,)")
        return False

### descarga de zip
def download_zip_from_url(url):
    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addon,1000,)")
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
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Error al extraer archivo,3000,)")
        return False

def inst_addon(addon_id):
    ### verificamos que no esté instalado ya
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} está ya instalado. Omitiendo instalación", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},{addon_id} ya instalado,1000,)")
        return False
    else:
        xbmc.log(f"REMOD INSTALADOR El addon {addon_id} no está instalado", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando {addon_id},1000,)")
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
                            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalado,1000,)")
                            return True
                        else:
                            xbmc.log(f"REMOD INSTALADOR Se está terminando de instalar {addon_id}", level=xbmc.LOGINFO)
                            xbmc.sleep(100)
                            attempts3 += 1
                    xbmc.log(f"Tiempo max2 superado {addon_id}", level=xbmc.LOGERROR)
                    xbmc.executebuiltin(f"Notification({remod_instalador_addon_name} {addon_id},Tiempo máximo2 superado,1000,)")
                    # dialog.notification("Recordatorio", "Revisa la configuración del addon.", "info", 0)
                    return False
                else:
                    xbmc.sleep(500)  # Pequeña pausa entre intentos
                    attempts2 += 1
            xbmc.log(f"Tiempo max superado {addon_id}", level=xbmc.LOGERROR)
            xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Tiempo máximo superado {addon_id},1000,)")
            return False    
        xbmc.sleep(500)  # Pequeña pausa entre intentos
        attempts += 1
    return False


def buscar_actualizacion_addons():
    xbmc.log(f"REMOD INSTALADOR Actualizando Addons locales", level=xbmc.LOGINFO)
    # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Actualizando Addons...,3000,)")
    xbmc.executebuiltin(f"UpdateLocalAddons()", True)
    # xbmc.sleep(3000)
    return True

def buscar_actualizacion_repos():
    xbmc.log(f"REMOD INSTALADOR Actualizando Addon Repos", level=xbmc.LOGINFO)
    # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Actualizando Repos...,3000,)")
    xbmc.executebuiltin(f"UpdateAddonRepos()", True)
    # xbmc.sleep(3000)
    return True

def buscar_actualizacion():
    xbmc.log(f"REMOD INSTALADOR Actualizando Repos y Addons...", level=xbmc.LOGINFO)
    buscar_actualizacion_repos()
    buscar_actualizacion_addons()

### instalar dependencias
def instalar_lista_addons(lista_deps):
    for addon_id in lista_deps:
        ### si está instalado y activado
        if addon_instalado_y_activado_comp(addon_id):
            xbmc.log(f"REMOD INSTALADOR {addon_id} instalado y activado", level=xbmc.LOGINFO)
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
            # return True
        else:
            xbmc.log(f"REMOD INSTALADOR Error al confirmar instalación {addon_id}", level=xbmc.LOGERROR)
            xbmc.sleep(1000)
            # return False
    xbmc.log(f"REMOD INSTALADOR Error instalando lista addons dependencias", level=xbmc.LOGERROR)
    return False
  
### instala lista de repos zip desde fuentes
def descargar_lista_repos_zip(repo_ids,base_urls_ids,lista_patterns):
    # xbmc.log(f"REMOD INSTALADOR Descargando lista repos zip desde url", level=xbmc.LOGINFO)
    for addon_id, base_url, pattern in zip(repo_ids, base_urls_ids, lista_patterns):
        # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Comprobando {addon_id} antes de descargar ,1000,)")
        # if not addon_instalado_y_activado_comp(addon_id):
        if addon_instalado_y_activado_comp(addon_id):
            continue
            
        xbmc.log(f"REMOD INSTALADOR Descargando {addon_id}", level=xbmc.LOGINFO)
        ### config func
        download_path = os.path.join(addons_home, 'packages')
        # Realizar la solicitud GET
        xbmc.log(f"REMOD INSTALADOR Buscando archivo zip", level=xbmc.LOGINFO)
        with urllib.request.urlopen(base_url) as response:
            html = response.read().decode()
        # Buscar el patrón del archivo zip
        match = re.search(pattern, html)
        if match:
            xbmc.log(f"REMOD INSTALADOR Archivo zip encontrado", level=xbmc.LOGINFO)
            download_url = f"{base_url}{match.group(0)}"
            res = download_zip_from_url(download_url)
            if res:
                res = addon_inst_confirm(addon_id)
                if res:
                    return True
            else:
                xbmc.log(f"REMOD INSTALADOR Error zip no encontrado", level=xbmc.LOGERROR)
                return False
        else:
            xbmc.log(f"REMOD INSTALADOR Archivo zip no encontrado", level=xbmc.LOGERROR)
            return False
    xbmc.log(f"REMOD INSTALADOR Fin descargando lista repos zip desde url", level=xbmc.LOGINFO)
    return True
 
 
### activar lista de repos descargada desde url como zip
def activar_lista_repos_zip(lista_repos):
    for addon_id in lista_repos:
        if addon_instalado_y_activado_comp(addon_id):
            continue
            
        ### verificamos si esta instalado
        res = xbmc.getCondVisibility(f'System.HasAddon({addon_id})')
        if res:
            xbmc.log(f"REMOD INSTALADOR 1. El repo {addon_id} está ya instalado. Comprobando activación", level=xbmc.LOGINFO)
            addon_act_des(addon_id, True)
         ### Si está desactivado, lo activamos
            ### confirma activación
            addon_activado_check(addon_id)
            # continue
        if not res:
            res = addon_inst_confirm(addon_id)
            if res:
                xbmc.log(f"REMOD INSTALADOR Activada Lista de repos zip Fin", level=xbmc.LOGINFO)
                return True
            else:
                xbmc.log(f"REMOD INSTALADOR Error Activando Lista de repos zip Fin", level=xbmc.LOGINFO)
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
        # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Ya instalado,500,)")
        xbmc.log(f"El addon {addon_id} está nstalado pero no sabmeos si está activado", level=xbmc.LOGINFO)
        ### comprobar si está activado
        if is_addon_enabled_from_xml(addon_id):
            # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Ya instalado y activado,500,)")
            xbmc.log(f"REMOD INSTALADOR El addon {addon_id} instalado y activado", level=xbmc.LOGINFO)
            return True
        else:
            # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Ya instalado pero desactivado,500,)")
            xbmc.log(f"REMOD INSTALADOR El addon {addon_id} instalado pero desactivado", level=xbmc.LOGERROR)
            return False
    else:
        # xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},No instalado,500,)")
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
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        # xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.program.remodtv"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando ReMod TV,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Espera a que se recargue la sección de TV,1000,)")
        ### instalación seccion de tv
        xbmc.executebuiltin('RunPlugin(plugin://plugin.program.remodtv/?action=tv)')
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación ReMod TV,3000,)")
            
    elif action == "kodispaintv":
        lista_repos = ["repository.gujal"]
        lista_base_urls = ["https://gujal00.github.io/"]
        lista_patterns = ["repository\.gujal-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        # xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
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
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando dependencias,1000,)")
        ### instalar addon zip desde url fuente
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        lista_repos = ['plugin.video.kodispaintv']
        lista_base_urls = ["https://konectas.github.io/Addons%20Video/"]
        lista_patterns = ["plugin\.video\.kodispaintv-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando KodispainTv,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        buscar_actualizacion()
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando KodispainTv,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        buscar_actualizacion()
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación KodispainTv,3000,)")
        
    elif action == "tacones":
        lista_repos = ["repository.elementumorg"]
        ### descarga directa de zip
        url = "https://github.com/ElementumOrg/repository.elementumorg/releases/download/v0.0.7/repository.elementumorg-0.0.7.zip"
        download_direct_zip_from_url(url)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        # descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
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
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando dependencias,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        lista_repos = ["plugin.video.tacones"]
        lista_base_urls = ["https://konectas.github.io/Addons%20Video/"]
        lista_patterns = ["plugin\.video\.tacones-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando Tacones,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando Tacones,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación elementum
        lista_deps = [
            "plugin.video.elementum",
            "script.elementum.burst",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Elementum y Burst,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Elementum y Burst Instaladoa,1000,)")
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Tacones,3000,)")

    elif action == "acs_channels":
        buscar_actualizacion()
        ### descarga addons zip desde url
        lista_repos = [
            "repository.acestream-channels",
            "repository.dregs",
            ]
        lista_base_urls = [
            "https://gunter257.github.io/repoachannels/",
            "https://dregs1.github.io/",
            ]
        lista_patterns = [
            "repository\.acestream-channels\.zip",
            "repository\.dregs-\d{1,3}\.\d{1,3}\.zip",        
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        
        ### instalación de addons desde repo ya instalado
        lista_deps = [
            "plugin.video.acestream_channels",
            "script.module.horus",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Acestream Channels,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.log(f"REMOD INSTALADOR Activando Reproductor Externo en Horus en Android", level=xbmc.LOGINFO)
            addon_set = xbmcaddon.Addon('script.module.horus')
            addon_set.setSettingBool('reproductor_externo', True)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación AceStream Channels,3000,)")
        
    elif action == "balandro":
        ### descarga addons zip desde url
        lista_repos = ["repository.balandro"]
        lista_base_urls = ["https://repobal.github.io/base/"]
        lista_patterns = ["repository\.balandro-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        
        lista_deps = ["plugin.video.balandro"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Balandro,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Balandro,3000,)")
        
    elif action == "magellan":
        ### descarga addons zip desde url
        lista_repos = [
            "repository.magellan",
            "repository.dregs",
            ]
        lista_base_urls = [
            "https://euro2000.github.io/magellan.github.io/",
            "https://dregs1.github.io/",
            ]
        lista_patterns = [
            "repository\.magellan\.zip",
            "repository\.dregs-\d{1,3}\.\d{1,3}\.zip",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
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
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Magellan,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Magellan,3000,)")
        
    elif action == "alfa":
        ### descarga addons zip desde url
        lista_repos = ["repository.alfa-addon"]
        lista_base_urls = ["https://alfa-addon.com/alfa/"]
        lista_patterns = ["repository\.alfa-addon\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.video.alfa"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Alfa,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Alfa,3000,)")
        
    elif action == "moes":
        lista_repos = ["repository.remod"]
        lista_base_urls = ["https://saratoga79.github.io/"]
        lista_patterns = ["repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)      
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
        ### instalación duffyou y moes
        lista_deps = [
            "plugin.video.duffyou",
            "plugin.video.moestv",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Moe's TV,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin instalación Moe's TV,1000,)")
        
    elif action == "espadaily":
        ### descarga addons zip desde url
        lista_repos = ["repository.espadaily"]
        lista_base_urls = ["https://fullstackcurso.github.io/espadaily/"]
        lista_patterns = ["repository\.espadaily-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        xbmc.sleep(1000)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.video.espadaily"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando EspaDaily,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación EspaDaily,3000,)")
            
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
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)      
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
        
        ### instalación elementum y jacktook
        lista_deps = [
            "plugin.video.jacktook",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Jacktook,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Jacktook Instalado,1000,)")
        ### configurando ajustes
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Configurando JackTook,3000,)")
        addon_set = xbmcaddon.Addon('plugin.video.jacktook')
        addon_set.setSettingBool('torrentio_enabled', True)
        addon_set.setSettingBool('auto_audio', True)
        addon_set.setSettingBool('auto_subtitle_selection', True)
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
        xbmc.log(f"REMOD INSTALADOR Copiando archivos...", level=xbmc.LOGINFO)
        orig = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_datos, 'plugin.video.jacktook', 'lib', 'router.py'))
        dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'router.py'))
        xbmcvfs.delete(dest)
        xbmcvfs.copy(orig, dest)
        orig = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_datos, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'ui.py'))
        dest = xbmcvfs.translatePath(os.path.join(addons_home, 'plugin.video.jacktook', 'lib', 'clients', 'stremio', 'ui.py'))
        xbmcvfs.delete(dest)
        xbmcvfs.copy(orig, dest)
        orig = xbmcvfs.translatePath(os.path.join(remod_instalador_addon_datos, 'plugin.video.jacktook', 'lib', 'utils', 'torrentio', 'utils.py'))
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
        xbmc.sleep(1000)
        ### añadir proveedpores torrentio
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=torrentio_selection)')
        addon_id = ("plugin.video.jacktook")
        dialog_aceptar_confirm(addon_id)
        xbmc.sleep(1000)
        ### activar proveedores torrentio en ajustes
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.jacktook/?action=torrentio_toggle_providers)')
        addon_id = ("plugin.video.jacktook")
        multiselect_aceptar_confirm(addon_id)      
        xbmc.sleep(1000)
        
        ### instalamos elementum
        lista_deps = [
            "plugin.video.elementum",
            "script.elementum.burst",
            ]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando Elementum y Burst,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Elementum y Burst Instaladoa,1000,)")
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación Jacktook,3000,)")
        
    elif action == "streamedez":
        ### descarga addons zip desde url
        lista_repos = ["repository.streamedez"]
        lista_base_urls = ["https://blazeymcblaze.github.io/streamedez/"]
        lista_patterns = ["repository\.streamedez-\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando repo StreamedEZ desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando repo repo StreamedEZ,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Repo StreamedEZ activado,1000,)")
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["plugin.video.streamedez"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando StreamedEZ,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación StreamedEZ,3000,)")
        
    elif action == "ezmaintenanceplus":
        ### descarga addons zip desde url
        lista_repos = ["repository.remod"]
        lista_base_urls = ["https://saratoga79.github.io/"]
        lista_patterns = ["repository\.remod-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.zip"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Descargando addons desde fuente,1000,)")
        descargar_lista_repos_zip(lista_repos,lista_base_urls,lista_patterns)
        ### actualizar lista de addons para refrersacar addons descargados
        buscar_actualizacion()
        ### activar addons descargados
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Activando addons descargados,1000,)")
        activar_lista_repos_zip(lista_repos)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin activando addons descargaos,1000,)")
        ### actualizar lista de repos descargados
        buscar_actualizacion()
        ### instalación de addons desde repo ya instalado
        lista_deps = ["script.ezmaintenanceplus"]
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Instalando EZMaintenance+,1000,)")
        instalar_lista_addons(lista_deps)
        xbmc.sleep(1000)
        xbmc.executebuiltin(f"Notification({remod_instalador_addon_name},Fin Instalación EZMaintenance+,3000,)")
        
    elif action == "test":
        addon_id = "script.ezmaintenanceplus"
        # Construye el comando de instalación
        instalar = f"InstallAddon({addon_id}, True)"
        xbmc.log(f"REMOD INSTALADOR Lanzamos instalación {addon_id}", xbmc.LOGINFO)
        # Ejecuta el comando
        xbmc.executebuiltin(instalar)
        xbmc.log(f"REMOD INSTALADOR Confirmamos instalación botón yes instalación {addon_id}", level=xbmc.LOGINFO)
        if addon_inst_confirm(addon_id):
            xbmc.log(f"REMOD INSTALADOR {addon_id} Fin instalación OK", level=xbmc.LOGINFO)
            xbmc.sleep(500)
            # return True
        else:
            xbmc.log(f"REMOD INSTALADOR Error al confirmar instalación {addon_id}", level=xbmc.LOGERROR)
            xbmc.sleep(500)
            # return False
        
        pass

    else:
        ### Acción desconocida → volver al menú principal
        lista_menu_principal()
