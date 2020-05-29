###
# Copyright (c) 2020, mogad0n
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

# my libs
import datetime
from dateutil import parser, tz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# supybot libs
from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('when420')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class when420(callbacks.Plugin):
    """The plugin contains commands relating to blazing culture and it's relation to 420"""
    pass

    def when420(self, irc, msg, args, user_location):
        """<location>

        Sets the location to <location>. Value must be a string
        """
        # convert location to timezone
        geolocator = Nominatim(user_agent="irc_bot_coordinate_finder")
        location = geolocator.geocode(user_location)
        tf = TimezoneFinder()
        latitude, longitude = location.latitude, location.longitude
        timezone = tf.timezone_at(lng=longitude, lat=latitude)

        # Convert timezone to aware datetimes and timedeltas
        now = datetime.datetime.now(tz=tz.gettz(timezone))
        today_420 = now.replace(hour=4, minute=20, second=0, tzinfo=tz.gettz(timezone))
        today_1620 = now.replace(hour=16, minute=20, second=0, tzinfo=tz.gettz(timezone))

        timezone_code = today_420.tzname()

        twelve_td = datetime.timedelta(hours= 12)
        zero_td = datetime.timedelta()

        time_until_today_420 = today_420 - now
        time_until_today_1620 = today_1620 - now

        if time_until_today_420 >= zero_td or time_until_today_1620 >= zero_td:
            # if either 4:20 or 16:20 is later today
            if time_until_today_1620 < twelve_td:
                # if 16:20 will occur sooner than 12hrs
                time_until_next_420 = time_until_today_1620

            else:
                time_until_next_420 = time_until_today_420

        else:
            # else, 4:20 and 16:20 today are already gone, compute tomorrow's
            tomorrow_420 = today_420 + datetime.timedelta(days=1)
            time_until_next_420 = tomorrow_420 - now

        time_until_next_420_seconds = time_until_next_420.total_seconds()

        re = utils.str.format('%T until next 4:20 for %s', time_until_next_420_seconds, timezone_code)
        irc.reply(re)

    when420 = wrap(when420, ['anything'])





Class = when420


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
