# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Extractor por Junji.
#
# Extractor para Kodi es un software libre: puedes redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU, según lo publicado por
# la Free Software Foundation, ya sea la versión 3 de la Licencia, o
# (a tu opción) cualquier versión posterior.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU junto
# con este programa. Si no, consulta <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------------------------------
#
# Exención de Responsabilidad
#
# Este addon solo proporciona acceso a contenido público y legal a través de
# una URL de acceso libre. El usuario es responsable del contenido al que
# accede utilizando este addon. No promovemos ni apoyamos el uso ilegal de 
# este addon.
#
# Por favor, utilice el addon de acuerdo con las leyes locales, y respete 
# los derechos de propiedad intelectual.
#-------------------------------------------------------------------------------


import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlencode, urlparse, parse_qsl
### ReMod
import json
import urllib.request


ADDON = xbmcaddon.Addon()
if len(sys.argv) > 1:
    ADDON_HANDLE = int(sys.argv[1])
else:
    ADDON_HANDLE = -1  # O cualquier otro valor por defecto que consideres seguro

BASE_URL = sys.argv[0]

### ReMod
def get_scraper_url():
    raw_url = "https://raw.githubusercontent.com/Saratoga79/saratoga79.github.io/refs/heads/master/ac_ex/lis.json"
    
    try:
        with urllib.request.urlopen(raw_url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('scraper_url', '')
    except Exception as e:
        # Fallback a valor por defecto si falla
        addon = xbmcaddon.Addon()
        return addon.getSetting('default_scraper_url')

SCRAPER_URL = get_scraper_url()


def is_valid_url(url):
    """Comprueba si una URL es válida."""
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def fetch_html_content(url):
    """Obtiene el contenido HTML de una página dada."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        xbmc.log(f'Error al acceder a la página: {e}', xbmc.LOGERROR)
        return None


def extract_magnets_and_acestreams_from_row(row):
    """Extrae los enlaces Magnet y Acestream de una fila dada."""
    magnets = []
    acestreams = []
    links = row.find_all('a', href=True)

    for link in links:
        href = link.get('href', '')
        if 'magnet:' in href:
            magnet_hash = re.search(r'btih:[a-fA-F0-9]{40}', href)
            if magnet_hash:
                magnets.append(f"magnet:?xt=urn:{magnet_hash.group()}")
        elif 'acestream://' in href:
            acestreams.append(href)

    # Verificar hashes de Acestream directamente
    cols = row.find_all('td')
    if not links and len(cols) >= 2:
        raw_hash = cols[-1].text.strip()
        if len(raw_hash) == 40:  # Verificar si es un hash SHA-1
            acestreams.append(f"acestream://{raw_hash}")

    return magnets, acestreams


def extract_m3u_links(html_content):
    """Extrae enlaces de tipo m3u del contenido HTML."""
    streams = []
    lines = html_content.splitlines()

    current_stream = {}
    for line in lines:
        if line.startswith("#EXTINF:"):
            # Extraer metadatos de la línea #EXTINF
            match = re.search(r'tvg-logo="([^"]*)",(.+)', line)
            if match:
                logo_url, title = match.groups()
                current_stream = {
                    "title": title.strip(),
                    "logo": logo_url.strip(),
                    "links": []
                }
        elif line.startswith("acestream://"):
            # Si es un link acestream, lo añadimos al stream actual
            if current_stream:
                current_stream["links"].append(line.strip())
                streams.append(current_stream)
                current_stream = {}  # Limpiar para el siguiente stream

    return streams

### ReMod
"""
- Mantiene la fecha (dd/mm/yyyy) y todo lo que sigue.
- Elimina cualquier aparición de:
- Devuelve una lista de tuplas: (info_limpia, [lista_de_enlaces])
"""
# ----------------------------------------------------------------------
# 1️⃣ HELPERS GENÉRICOS
# ----------------------------------------------------------------------
def fetch_html_content(url):
    """Descarga la página y devuelve su HTML como texto."""
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:          # pylint: disable=broad-except
        print(f"[fetch_html_content] Error al obtener {url}: {exc}")
        return None


def extract_magnets_and_acestreams_from_row(row):
    """Busca enlaces Magnet y Acestream dentro de una fila <tr>."""
    magnets, acestreams = [], []
    for a in row.find_all("a", href=True):
        href = a["href"]
        if href.startswith("magnet:"):
            m = re.search(r"btih:[a-fA-F0-9]{40}", href)
            if m:
                magnets.append(f"magnet:?xt=urn:{m.group()}")
        elif href.startswith("acestream://"):
            acestreams.append(href)
    return magnets, acestreams


def extract_m3u_links(html_content: str):
    """Busca URLs que terminen en .m3u/.m3u8 dentro del HTML."""
    urls = re.findall(r"(https?://[^\s'\"<>]+\.m3u8?)", html_content, re.I)
    result = []
    for idx, url in enumerate(urls, start=1):
        result.append({"title": f"M3U Stream #{idx}", "links": [url]})
    return result


# ----------------------------------------------------------------------
# 2️⃣ LIMPIEZA ESPECÍFICA DE TEXTO
# ----------------------------------------------------------------------
def clean_unwanted_segments(text: str) -> str:
    """
    Elimina cualquier bloque de transmisión que pueda aparecer.
    El patrón es flexible para cubrir:
    """
    # Normalizamos espacios duros que a veces aparecen en HTML
    text = text.replace("\xa0", " ")

    # Bloque completo (con “Ronda … VER PARTIDO”)
    # full_pattern = (
        # r"Ronda\s+Masters\s+Indian\s+Wells"
        # r"(?:\s*2ª\s*Ronda){0,2}"
        # r"\s*ATP\s+Tennis\s+TV\s*[·\.]?\s*"
        # r"Movistar\s+Plus\+"
        # r"(?:\s*$$M7$$)?\s*"
        # r":\s*VER\s+PARTIDO\s*[·\.]?"
    # )

    # Prefijo aislado (solo la parte de transmisión)
    # prefix_pattern = (
        # r"ATP\s+Tennis\s+TV\s*[·\.]?\s*"
        # r"Movistar\s+Plus\+"
        # r"(?:\s*$$M7$$)?\s*"
        # r":\s*VER\s+PARTIDO\s*[·\.]?"
    # )

    # text = re.sub(full_pattern,   "", text, flags=re.IGNORECASE)
    # text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE)

    return text.strip()


def keep_from_date(text: str) -> str:
    """
    1️⃣ Busca la primera fecha con formato dd/mm/yyyy.
    2️⃣ Devuelve la sub‑cadena a partir de esa fecha.
    3️⃣ Aplica `clean_unwanted_segments` para quitar cualquier bloque de transmisión.
    Si no hay fecha, simplemente limpia el texto completo.
    """
    text = text.replace("\xa0", " ")
    m = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
    if not m:
        return clean_unwanted_segments(text.strip())

    after_date = text[m.start():].strip()
    return clean_unwanted_segments(after_date)


# ----------------------------------------------------------------------
# 3️⃣ FUNCIÓN PRINCIPAL
# ----------------------------------------------------------------------
def extract_stream_info(url: str):
    """
    Extrae información de streams (Magnet / Acestream) de la página indicada.
    - Mantiene solo la fecha y lo que sigue.
    - Elimina cualquier bloque de transmisión no deseado.
    - Devuelve: [(info_limpia, [lista_de_enlaces]), ...]
    """
    html = fetch_html_content(url)
    if not html:
        return []   # nada que procesar

    soup = BeautifulSoup(html, "html.parser")
    streams = []

    # --------------------------------------------------------------
    # 1️⃣ Tablas (<table>) – caso más habitual
    # --------------------------------------------------------------
    for table in soup.find_all("table"):
        rows = table.find_all("tr")[1:]          # saltamos la fila de cabecera
        for row in rows:
            # cols = row.find_all("td")[1:]
            cols = [col for i, col in enumerate(row.find_all("td")) if i != 3]
            
            if len(cols) >= 2:                  # al menos una columna útil + la de acciones
                raw_info = "|".join(col.text.strip() for col in cols[:-1])
                stream_info = keep_from_date(raw_info)

                magnets, acestreams = extract_magnets_and_acestreams_from_row(row)
                if magnets or acestreams:
                    streams.append((stream_info, magnets + acestreams))

    # --------------------------------------------------------------
    # 2️⃣ Listas <ul>/<li> – enlaces Magnet fuera de tablas
    # --------------------------------------------------------------
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            for a in li.find_all("a", href=True):
                href = a["href"]
                if href.startswith("magnet:"):
                    m = re.search(r"btih:[a-fA-F0-9]{40}", href)
                    if m:
                        magnet_clean = f"magnet:?xt=urn:{m.group()}"
                        title_raw = li.get_text(separator=" ", strip=True)
                        title = keep_from_date(title_raw)
                        streams.append((title, [magnet_clean]))

    # --------------------------------------------------------------
    # 3️⃣ Enlaces .m3u/.m3u8 (si la página los incluye)
    # --------------------------------------------------------------
    for block in extract_m3u_links(html):
        streams.append((block["title"], block["links"]))

    return streams


# ----------------------------------------------------------------------
# 4️⃣ EJEMPLO DE USO (puedes comentar/eliminar en producción)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
    # URL real (no el prefijo view‑source:)
    # target_url = SCRAPER_URL

# resultados = extract_stream_info(SCRAPER_URL)

# if not resultados:
    # print("No se encontraron streams.")
# else:
    # for idx, (info, links) in enumerate(resultados, start=1):
        # print(f"\n[{idx}] INFO : {info}")
        # for link in links:
            # print(f"     → {link}")### ReMod

def build_url(query):
    """Construye una URL con los parámetros proporcionados."""
    return f'{BASE_URL}?{urlencode(query)}'


def prompt_for_url():
    """Muestra un cuadro de diálogo para solicitar una nueva URL y la guarda en los ajustes."""
    ### current_url = ADDON.getSetting('scraper_url')
    ### ReMod
    current_url = scraper_url
    ###d ialog = xbmcgui.Dialog()
    
    ### warning_message = (
        # "ADVERTENCIA: Asegúrese de que la URL proporcionada cumple con las leyes de su país. "
        # "No apoyamos ni promovemos el acceso a contenido ilegal."
    # )
    ### dialog.ok("Advertencia Legal", warning_message)
    
    # new_url = dialog.input("Introduce la nueva URL a escanear", defaultt=current_url, type=xbmcgui.INPUT_ALPHANUM)
    new_url = current_url

    # Si no se introduce una nueva URL, usar la anterior
    if not new_url:
        new_url = current_url

    if is_valid_url(new_url):
        # Guardar la nueva URL en los ajustes
        # ADDON.setSetting('scraper_url', new_url)
        # xbmcgui.Dialog().notification("URL actualizada", f"Se ha cambiado a: {new_url}", xbmcgui.NOTIFICATION_INFO, 3000)
        
        # Forzar la actualización del directorio actual
        xbmc.executebuiltin('Container.Refresh')
    else:
        xbmcgui.Dialog().notification("Error", "La URL proporcionada no es válida.", xbmcgui.NOTIFICATION_ERROR, 3000)


def list_main_menu():
    """Crea el menú principal con las opciones para ver streams y cambiar la URL."""
    # Opción para ver streams en la página secundaria
    list_item_streams = xbmcgui.ListItem(label="Ver streams")
    xbmcplugin.addDirectoryItem(
        handle=ADDON_HANDLE, 
        url=build_url({'action': 'view_streams'}), 
        listitem=list_item_streams, 
        isFolder=True
    )
    
    # Opción para cambiar la URL sin mostrar la URL actual
    list_item_url = xbmcgui.ListItem(label="Cambiar o actualizar URL de origen")
    list_item_url.setArt({'icon': 'DefaultAddonsUpdates.png'})  # Icono para cambiar URL
    xbmcplugin.addDirectoryItem(
        handle=ADDON_HANDLE, 
        url=build_url({'action': 'change_url'}), 
        listitem=list_item_url, 
        isFolder=False
    )

    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def list_streams():
    """Lista los streams en la interfaz de Kodi en la página secundaria."""
    if not is_valid_url(SCRAPER_URL):
        xbmcgui.Dialog().ok("Error", "La URL proporcionada no es válida.")
        return

    streams = extract_stream_info(SCRAPER_URL)

    for stream_info, links in streams:
        for link in links:
            list_item = xbmcgui.ListItem(label=stream_info)
            list_item.setInfo("video", {"title": stream_info})

            if link.startswith("#"):
                # Comentario, no es reproducible
                xbmcplugin.addDirectoryItem(
                    handle=ADDON_HANDLE, url=link, listitem=list_item, isFolder=False
                )
            else:
                # Verificar tipo de enlace (magnet o acestream) y personalizar el ícono
                if link.startswith("magnet:"):
                    magnet_hash = re.search(r'btih:([a-fA-F0-9]{40})', link)
                    if magnet_hash:
                        infohash = magnet_hash.group(1)
                        new_link = f"plugin://script.module.horus?action=play&infohash={infohash}"
                    else:
                        new_link = link
                    list_item.setArt({'icon': 'special://home/addons/plugin.video.acs_extractor/resources/media/Magnet.png'})
                elif link.startswith("acestream://"):
                    acestream_id = link.split("://")[1]
                    new_link = f"plugin://script.module.horus?action=play&id={acestream_id}"
                    list_item.setArt({'icon': 'special://home/addons/plugin.video.acs_extractor/resources/media/Acestream.png'})
                else:
                    new_link = link
                    list_item.setArt({'icon': 'DefaultVideo.png'})

                list_item.setProperty("IsPlayable", "true")
                xbmcplugin.addDirectoryItem(
                    handle=ADDON_HANDLE, url=new_link, listitem=list_item, isFolder=False
                )

    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def router(paramstring):
    """Lógica del enrutador para manejar las acciones y el menú principal."""
    params = dict(parse_qsl(paramstring))
    action = params.get('action')

    if action == 'view_streams':
        list_streams()  # Muestra los streams en la página secundaria
    # elif action == 'change_url':
        # prompt_for_url()  # Cambia la URL
    else:
        # list_main_menu()  # Muestra el menú principal
        list_streams()  # Muestra lista de eventos


if __name__ == '__main__':
    if len(sys.argv) > 2:
        router(sys.argv[2][1:])
    else:
        router('')