import os
from datetime import timedelta
from lib.db.cached import cache
from lib.utils.kodi.utils import (
    ADDON_PATH,
    translation,
)
from lib.clients.stremio.constants import (
    TORRENTIO_PROVIDERS_KEY,
    all_torrentio_providers,
)
import xbmcgui

### ReMod
import xbmcvfs
addons_userdata = xbmcvfs.translatePath(f'special://home/userdata')
addons_addon_data = os.path.join(addons_userdata, 'addon_data')
torr_prov_ok = os.path.join(addons_addon_data, 'plugin.instalador.remod', 'torr_prov_ok.json')


def torrentio_toggle_providers(params):
    selected_ids = cache.get(TORRENTIO_PROVIDERS_KEY) or ""
    selected_ids = selected_ids.split(",") if selected_ids else []

    options = []
    # selected_indexes = []
    selected_indexes = [4,5,6]
    for i, (key, name, logo) in enumerate(all_torrentio_providers):
        item = xbmcgui.ListItem(label=name)
        item.setArt(
            {"icon": os.path.join(ADDON_PATH, "resources", "img", "torrentio.png")}
        )
        options.append(item)
        if key in selected_ids:
            selected_indexes.append(i)

    dialog = xbmcgui.Dialog()

    selected = dialog.multiselect(
        translation(90117), options, preselect=selected_indexes, useDetails=True
    )

    if selected is None:
        return
        
    ### ReMod file ok
    with open(torr_prov_ok, 'w') as f:
        f.write('')

    new_selected_ids = [all_torrentio_providers[i][0] for i in selected]
    cache.set(
        TORRENTIO_PROVIDERS_KEY, ",".join(new_selected_ids), timedelta(days=365 * 20)
    )
