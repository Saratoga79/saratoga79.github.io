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
# import subprocess

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
fuent_act = 'Lista Directa'

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
        (f"{remodtv_addon_name} versión: {remodtv_addon_version} | Buscar actualizaciones", "info", "info.png"),
        ("> Instalar y configurar sección TV de Kodi", "tv2", "tv2.png"),
        ("> Elegir fuente para sección TV de Kodi", "fuente", "tv.png"),
        ("", "", ""),
        ("> Actualizar TV", "actualizar", "update.png"),
        # ("", "", ""),
        ("> Configurar Reproductor Externo para AceStream en Android", "res_ext", "repro.png")
        # ("> Configurar Reproductor Externo para ACS en Android", "res_ext", "repro.png"),
        # ("> test", "test", "repro.png"),
        # ("> Desisnstalar sección TV de Kodi", "desins", "tv.png"),
        # ("", "", "")
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
    

### copia los archivos de configuración
def archivos_config():
    xbmc.log(f"REMOD TV Desactivando addons para copiar archivos de configuración.", level=xbmc.LOGINFO)
    ### addons a desactivar para liberar los archivos antes de copiar los nuevos
    # addons = ["plugin.program.iptv.merge", "script.module.slyguy", "pvr.iptvsimple"]
    # addons = ["pvr.iptvsimple"]
    # lista_addons(addons, False)
    ### copiando sources.xml
    # orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'sources.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'sources.xml'))
    # xbmcvfs.copy(orig, dest)
    ### copiando favourites.xml
    # orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'favourites.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'favourites.xml'))
    # xbmcvfs.copy(orig, dest)
    xbmc.log(f"REMOD TV Copiando archivos de configuración inicial.", level=xbmc.LOGINFO)
    ### copiando archivos pvr.iptvsimple para iptv.merge
    # orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'pvr.iptvsimple','instance-settings-1.xml'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'instance-settings-1.xml'))
    ### config sin iptv.merge fuente 1 direct
    orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'pvr.iptvsimple', carp, 'instance-settings-2.xml'))
    dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'instance-settings-1.xml'))
    xbmcvfs.delete(dest)
    xbmcvfs.copy(orig, dest)
    # orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'pvr.iptvsimple', 'settings.xml'))
    dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'pvr.iptvsimple', 'settings.xml'))
    xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    ### copiando archivos script.module.slyguy
    # orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'script.module.slyguy', 'settings.db'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'script.module.slyguy', 'settings.db'))
    # xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    ### copiando archivos plugin.program.iptv.merge
    # orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'plugin.program.iptv.merge', 'data.db'))
    # dest = xbmcvfs.translatePath(os.path.join(addons_addon_data, 'plugin.program.iptv.merge', 'data.db'))
    # xbmcvfs.delete(dest)
    # xbmcvfs.copy(orig, dest)
    ### addons a activar después de copiar los nuevos archivos
    # xbmc.log(f"REMOD TV Activando addons para copiar archivos de configuración.", level=xbmc.LOGINFO)
    # lista_addons(addons, True)
    ### copiando ok
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Archivos de configuración copiados,3000,)")
    xbmc.log(f"{remodtv_addon_name} Archivos de configuración copiados.", level=xbmc.LOGINFO)
    # open(remod_config_ok, "w")

   
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
            xbmc.sleep(500)  # Pequeña pausa entre intentos
            attempts += 1
    return False
   
### descarga de zip
def download_zip_from_url(url):
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Descargando addon.,1000,)")
    xbmc.log(f"REMOD TV Iniciando download_zip_from_url.", level=xbmc.LOGINFO)
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
            xbmc.log(f"REMOD TV Archivo zip descargado.", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD TV Fin download_zip_from_url.", level=xbmc.LOGINFO)
        xbmc.log(f"REMOD TV Iniciando extract_zip.", level=xbmc.LOGINFO)
        xbmc.sleep(1000)
        extract_path = xbmcvfs.translatePath(addons_home)
        # Verificar si el archivo existe
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"El archivo {full_path} no existe")
            return False
        # Extraer el archivo ZIP
        with zipfile.ZipFile(full_path, mode="r") as archive:
            archive.extractall(extract_path)
            xbmc.log(f"REMOD TV Archivo zip extraido.", level=xbmc.LOGINFO)
        return True
        xbmc.log(f"REMOD TV Fin extract_zip.", level=xbmc.LOGINFO)
    except Exception as e:
        xbmc.log(f"REMOD TV Error al extraer archivo.", level=xbmc.LOGINFO)
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al extraer archivo.,3000,)")
        return False
    
    
def inst_addon(addon_id):
    ### verificamos que no esté instalado ya
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},{addon_id} ya instalado.,1000,)")
        xbmc.log(f"El addon {addon_id} está ya instalado. Desinstalando", level=xbmc.LOGINFO)
        # addons = ["addon_id"]
        # lista_addons(addons, True)
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
            max_attempts2 = 20  # Número máximo de intentos
            attempts2 = 0
            while attempts2 < max_attempts2:
                if xbmc.getCondVisibility(f"Window.IsVisible(10101)"):
                    xbmc.log(f"REMOD TV Se está instalando", level=xbmc.LOGINFO)
                    max_attempts3 = 200  # Número máximo de intentos
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
                    xbmc.sleep(500)  # Pequeña pausa entre intentos
                    attempts2 += 1
            xbmc.log(f"Tiempo max superado {addon_id}.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Tiempo superado.,1000,)")
            return True    
        xbmc.sleep(500)  # Pequeña pausa entre intentos
        attempts += 1
    return False
        
        
# def iptv_update():
    # monitor_pvr_startup(max_total_seconds=60)
    # notify_pvr_status()
    # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Cargando addons.,7500,)")
    # xbmc.sleep(7500)
    # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Actualizando lista TV.,7500,)")
    # xbmc.sleep(7500)
    ### comando iptvmerge para actualizar la lista de TV y Radio
    # urllib.request.urlretrieve("http://127.0.0.1:8096/run_merge")
    # xbmc.log(f"REMOD TV Fin instalación IPTV Simple.", level=xbmc.LOGINFO)

### instala repo, iptv merge y iptv simple. De monento no compatible
# def inst_tv():
    # archivos_config()
    # xbmc.log(f"REMOD TV Instalando repo SlyGuy.", level=xbmc.LOGINFO)
    # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Instalando repo SlyGuy.,1000,)")
    # repo_url = 'https://slyguy.uk/repository.slyguy.zip'
    # addon_id = 'repository.slyguy'
    # addons = ["repository.slyguy"]
    # res = download_zip_from_url(repo_url)
    # if res:
        # xbmc.log(f"REMOD TV Actualizando Addon Repos.", level=xbmc.LOGINFO)
        # xbmc.executebuiltin(f"UpdateAddonRepos()", True)
        # xbmc.sleep(1000)
        # xbmc.log(f"REMOD TV Actualizando Local Addon.", level=xbmc.LOGINFO)
        # xbmc.executebuiltin(f"UpdateLocalAddons()", True)
        # xbmc.sleep(1000)
        # res = lista_addons(addons, True)
        # res = addon_activacion_confirm(addon_id)
        # if res:   
            # addon_id = 'plugin.program.iptv.merge'
            # res = inst_addon(addon_id)
            # if res:
                # res = addon_inst_confirm(addon_id)
                # if res:
                    # addon_id = 'pvr.iptvsimple'
                    # res = inst_addon(addon_id)
                    # if res:
                        # res = addon_inst_confirm(addon_id)
                        # if res:
                            # iptv_update()
                        # else:
                            # xbmc.log(f"REMOD TV Error activando IPTV Simple.", level=xbmc.LOGINFO)
                            # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error activando IPTV Simple.,1000,)")
                    # else:
                        # xbmc.log(f"REMOD TV Error instalando IPTV Simple.", level=xbmc.LOGINFO)
                        # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error instalando IPTV Simple.,1000,)")
                # else:
                    # xbmc.log(f"REMOD TV Error activando IPTV Merge.", level=xbmc.LOGINFO)
                    # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error activando IPTV Merge.,1000,)")
            # else:
                # xbmc.log(f"REMOD TV Error instalando IPTV Merge.", level=xbmc.LOGINFO)
                # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error instalando IPTV Merge.,1000,)")
        # else:
            # xbmc.log(f"REMOD TV Error activando repo SlyGuy.", level=xbmc.LOGINFO)
            # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error activando repo SlyGuy.,1000,)")
    # else:
        # xbmc.log(f"REMOD TV Error instalando repo SlyGuy.", level=xbmc.LOGINFO)
        # xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error instalando repo SlyGuy.,1000,)")

### instala solo iptv simple sin iptv merge
def inst_tv2():
    # archivos_config()
    addons = ["pvr.iptvsimple"]
    addon_id = 'pvr.iptvsimple'
    lista_addons(addons, False)
    xbmc.sleep(1500)
    res = inst_addon(addon_id)
    if res:
        archivos_config()
        res = addon_inst_confirm(addon_id)
        if res:
            lista_addons(addons, True)
            xbmc.sleep(1500)
            # iptv_update()
            xbmc.log(f"REMOD TV IPTV Simple activado.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},IPTV Simple activado.,1000,)")
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},En unos 30s estará disponible la sección TV de Kodi.,5000,)")
        else:
            xbmc.log(f"REMOD TV Error activando IPTV Simple.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error activando IPTV Simple.,3000,)")
    else:
        res = addon_borrar_datos(addon_id)
        if res:
            archivos_config()
            lista_addons(addons, True)
            xbmc.sleep(1500)
            xbmc.log(f"REMOD TV Recargando Addon ya instalando IPTV Simple.", level=xbmc.LOGINFO)
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Recargando IPTV Simple.,1000,)")
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},En unos 30s estará disponible la sección TV de Kodi.,5000,)")


def fuente():
    ### Cada tupla contiene: etiqueta visible, acción, nombre del archivo de icono
    menu_items = [
        # (f"Elige la fuente para la sección de TV | Actual: {fuent_act}", "", "tv.png"),
        (f"Elige la fuente para la sección de TV:", "", "tv.png"),

        ("      1> Lista Directa (Por defecto)\n                Enlaces ACS http directos", "lis_dir", ""),
        ("      2> Lista acestream (ACE)\n              Enlaces ACS protocolo acestream://", "lis_ace", ""),
        ("      3> Lista Horus\n                Enlaces ACS para addon Horus", "lis_hor", "")
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



def actualizar_tv():
    xbmc.executebuiltin(f"Notification({remodtv_addon_name},Reiniciando IPTV Simple.,5000,)")
    addons = ["pvr.iptvsimple"]
    addon_id = 'pvr.iptvsimple'
    res = lista_addons(addons, False)
    xbmc.sleep(1500)
    if res:
        res = lista_addons(addons, True)
        xbmc.sleep(1500)
        if res:
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},En unos 30s estará disponible la sección TV de Kodi.,5000,)")
        else:
            xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al activar IPTV Simple.,5000,)")
    else:
        xbmc.executebuiltin(f"Notification({remodtv_addon_name},Error al desactivar IPTV Simple.,5000,)")
        
        
def buscar_actualización():
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

### desinstlar addons
def addon_desins(addon_id: str, desinstalar: bool) -> None:
    """
    Desinstala (o reinstala) un addon de Kodi mediante JSON‑RPC.

    Parámetros
    ----------
    addon_id : str
        Identificador del addon (por ejemplo, "plugin.video.youtube").
    desinstalar : bool
        True → desinstala el addon.
        False → solo lo desactiva sin eliminarlo (si se quisiera reactivar).
    """

    # Mensaje de registro que indica la acción que se va a ejecutar
    accion = "Desinstalando" if desinstalar else "Desactivando"
    xbmc.log(f"{remodtv_addon_name}: {accion} {addon_id}", level=xbmc.LOGINFO)

    ### Construimos la petición JSON‑RPC
    request = {
        "jsonrpc": "2.0",
        "method": "Addons.Uninstall",
        "params": {
            "addonid": addon_id,
            "uninstall": desinstalar   ### El propio booleano es aceptado por Kodi
        },
        "id": 1
    }

    ### Convertimos el diccionario a cadena JSON y lo enviamos
    xbmc.executeJSONRPC(json.dumps(request))

### configuración del reproductor externo para ACS en Android
def ele_rep():
    dialog = xbmcgui.Dialog()
    rep = dialog.select(
    f"Elige la aplicación de AceStream que tengas instalada",
    [
        ### 0. Ace Stream Media McK
        "Ace Stream Media McK\n     org.acestream.media",
        ### 1. Ace Stream Media ATV
        "Ace Stream Media ATV\n     org.acestream.media.atv",
        ### 2. Ace Stream Media Web
        "Ace Stream Media Web\n     org.acestream.media.web",
        ### 3. Ace Stream Node
        "Ace Stream Node\n      org.acestream.node",
        ### 4. Ace Stream Node Web
        "Ace Stream Node Web\n      org.acestream.node.web",
        ### 5. Ace Stream Core
        "Ace Stream Core\n      org.acestream.core",
        ### 6. Ace Stream Core ATV
        "Ace Stream Core ATV\n      org.acestream.core.atv",
        ### 7. Ace Stream Core Web
        "Ace Stream Core Web\n      org.acestream.core.web",
        ### 8. Ace Stream Live
        "Ace Stream Live\n      org.acestream.live",
        ### 9. MPVkt
        "MPVkt\n        live.mehiz.mpvkt",
        ### 10. MPV
        "MPV\n      is.xyz.mpv",
        ### 11. VLC
        "VLC\n      org.videolan.vlc",
        ### 12. Ace Serve
        "Ace Serve\n        org.free.aceserve",
        ### 13. Atras
        "< Volver"
    ]
)
    if not rep == 13:
        ### variable de la carpeta
        pcf_path = f"playercorefactory{rep}"
        ### copiando archivo playercorefactory.xml desde la variable de la carpeta
        xbmc.log(f"REMOD TV Copiando archivo {pcf_path}", level=xbmc.LOGINFO)
        orig = xbmcvfs.translatePath(os.path.join(remodtv_addon_datos, 'pcf', pcf_path, 'playercorefactory.xml'))
        dest = xbmcvfs.translatePath(os.path.join(addons_userdata, 'playercorefactory.xml'))
        xbmcvfs.copy(orig, dest)
        dialog = xbmcgui.Dialog()
        ret = dialog.ok(f"{remodtv_addon_name}", "Necesitarás reiniciar Kodi para aplicar los cambios.")


### pruebas ###



### pruebas ###


### acciones del menu principal
if not ARGS:
    # No hay parámetros → menú principal
    lista_menu_principal()
else:
    action = ARGS.get('action', [None])[0]
    if action == "tv2":
        inst_tv2()
    elif action == "fuente":
        fuente()
    elif action == "actualizar":
        actualizar_tv()
    elif action == "info":
        buscar_actualización()
    elif action == "desins":
        addon_id = 'pvr.iptvsimple'
        addon_desins(addon_id, True)
    elif action == "res_ext":
        ele_rep()
    elif action == "lis_dir":
        carp = 'dir'
        fuent_act == 'Lista Directa'
        archivos_config()
        actualizar_tv()
        lista_menu_principal()
    elif action == "lis_ace":
        carp = 'ace'
        fuent_act == 'Lista ACE'
        archivos_config()
        actualizar_tv()
        lista_menu_principal()
    elif action == "lis_hor":
        carp = 'hor'
        fuent_act == 'Lista Horus'
        archivos_config()
        actualizar_tv()
        lista_menu_principal()
    elif action == "test":
        pass
    else:
        ### Acción desconocida → volver al menú principal
        lista_menu_principal()