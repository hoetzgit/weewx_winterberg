## celestial module for daylight with Belchertown skin
## Copyright This Manhart
#errorCatcher Echo
## If extended almanac information is available, do extra calculations.
#if $almanac.hasExtras
  #import locale
  #set $sun_azimuth = locale.format_string( "%.1f&deg;", $almanac.sun.az )
  #set $sun_ra = locale.format_string( "%.1f&deg;", $almanac.sun.ra )
  #set $sun_dec = locale.format_string( "%.1f&deg;", $almanac.sun.dec )
  #set $moon_azimuth = locale.format_string( "%.1f&deg;", $almanac.moon.az )
  #set $moon_altitude = locale.format_string( "%.1f&deg;", $almanac.moon.alt )
  #set $moon_ra = locale.format_string( "%.1f&deg;", $almanac.moon.ra )
  #set $moon_dec = locale.format_string( "%.1f&deg;", $almanac.moon.dec )
  #set $sun_altitude = $almanac.sun.alt
  #if $sun_altitude < 0
    #set $sun_None="<i>(%s)</i>" % $obs.label.sun_always_down
    #set $daylight_str = "00:00"
  #else
    #set $sun_None="<i>(%s)</i>" % $obs.label.sun_always_up
    #set $daylight_str = "24:00"
  #end if
  #set $sunrise_ts = $almanac.sun.rise.raw
  #set $sunset_ts = $almanac.sun.set.raw
  #if $sunrise_ts and $sunset_ts
    #set $now = $current.dateTime.raw
    #set $today_daylight = $sunset_ts -  $sunrise_ts
    #set $seconds = $today_daylight
    #set $hours = $seconds // 3600
    #set $seconds %= 3600
    #set $minutes = $seconds // 60
    #set $seconds %= 60
    #set $daylight_str = "%d %s, %d %s, %d %s" % ($hours, $obs.label.hour[0] if ( $hours == 1 ) else $obs.label.hour[1], $minutes, $obs.label.minute[0] if ( $minutes == 1 ) else $obs.label.minute[1], $seconds, $obs.label.second[0] if ( $seconds == 1 ) else $obs.label.second[1])
    #set $daylight_strx = "%dh %dm %ds" % ($hours, $minutes, $seconds)
    #set $yesterday = $now - 24*3600
    #set $yesterday_daylight = $almanac($almanac_time=$yesterday).sun.set.raw - $almanac($almanac_time=$yesterday).sun.rise.raw
    #set $difference = $today_daylight - $yesterday_daylight
    #if $difference
      #set $delta = abs($difference)
      #set $minute_difference = (int($delta) // 60)
      #set $minutes_text = $obs.label.minute[0] if ( $minute_difference == 1 ) else $obs.label.minute[1]
      #set $seconds_text = $obs.label.second[0] if ( int($delta) == 1 ) else $obs.label.second[1]
      #set $amt_str = "%s%d %s" % (str(int($delta) // 60) + ' ' + $minutes_text + ', ' if ($delta // 60) > 0 else '', $delta % 60 if ($delta // 60) > 0 else $delta, $seconds_text)
      #set $amt_strx = "%s%d%s" % (str(int($delta) // 60) + 'm ' + ', ' if ($delta // 60) > 0 else '', $delta % 60 if ($delta // 60) > 0 else $delta, 's')
      #if $difference > 0
        #set $delta_str = "%s %s" % ( $amt_str, $obs.label.more_than_yesterday )
        #set $delta_strx = "+ %s" % ( $amt_strx )
      #else
        #set $delta_str = "%s %s" % ( $amt_str, $obs.label.less_than_yesterday )
        #set $delta_strx = "- %s" % ( $amt_strx )
      #end if
      #set $daylight_str = "%s<br/>%s" % ($daylight_str, $delta_str)
    #end if
  #end if
  #set $sun_altitude = locale.format_string( "%.1f&deg;", $almanac.sun.alt )
#end if
## Compressed for the weewx_data.json file to stay consistent
<div>
  <table cellpadding="0" cellspacing="0">
    <tbody>
      <tr>
        <td>$obs.label.total_daylight</td>
        <td>$daylight_strx</td>
      </tr>
      <tr>
        <td>$obs.label.delta_daylight</td>
        <td>$delta_strx</td>
      </tr>
    </tbody>
  </table>
</div>
