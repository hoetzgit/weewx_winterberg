#
#    Copyright (c) 2009-2015 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

"""User extensions module

This module is imported from the main executable, so anything put here will be
executed before anything else happens. This makes it a good place to put user
extensions.
"""

import locale
# This will use the locale specified by the environment variable 'LANG'
# Other options are possible. See:
# http://docs.python.org/2/library/locale.html#locale.setlocale
locale.setlocale(locale.LC_ALL, '')

import weewx.units

weewx.units.obs_group_dict['sunshineDur'] = 'group_deltatime'

weewx.units.obs_group_dict['temp_garage'] = 'group_temperature'
weewx.units.obs_group_dict['temp_dach'] = 'group_temperature'
weewx.units.obs_group_dict['temp_wohnen'] = 'group_temperature'
weewx.units.obs_group_dict['temp_heizung_vorlauf'] = 'group_temperature'
weewx.units.obs_group_dict['temp_heizung_ruecklauf'] = 'group_temperature'
weewx.units.obs_group_dict['temp_sole_links'] = 'group_temperature'
weewx.units.obs_group_dict['temp_sole_rechts'] = 'group_temperature'
weewx.units.obs_group_dict['temp_boiler'] = 'group_temperature'

weewx.units.obs_group_dict['wasser_schacht_pegel'] = 'group_percent'

weewx.units.obs_group_dict['pv'] = 'group_power'
weewx.units.obs_group_dict['pv_day'] = 'group_energy'
weewx.units.obs_group_dict['pv_day_wh'] = 'group_energy'
weewx.units.obs_group_dict['pv_ost'] = 'group_power'
weewx.units.obs_group_dict['pv_sued'] = 'group_power'
weewx.units.obs_group_dict['pv_west'] = 'group_power'

weewx.units.obs_group_dict['netzbezug'] = 'group_power'
weewx.units.obs_group_dict['netzlieferung'] = 'group_power'
weewx.units.obs_group_dict['eigenverbrauch'] = 'group_power'

weewx.units.obs_group_dict['netzbezug_day_c'] = 'group_energy'
weewx.units.obs_group_dict['netzbezug_day'] = 'group_energy'

weewx.units.obs_group_dict['netzlieferung_day_c'] = 'group_energy'
weewx.units.obs_group_dict['netzlieferung_day'] = 'group_energy'

weewx.units.obs_group_dict['eigenverbrauch_day_c'] = 'group_energy'
weewx.units.obs_group_dict['eigenverbrauch_day'] = 'group_energy'

weewx.units.obs_group_dict['ec_sueden'] = 'group_percent'
weewx.units.obs_group_dict['ec_westen'] = 'group_percent'
weewx.units.obs_group_dict['ec_sueden_t'] = 'group_temperature'
weewx.units.obs_group_dict['ec_westen_t'] = 'group_temperature'
