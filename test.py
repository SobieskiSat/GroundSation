'''
from Communication import Radio
from EventManager import Manager

em=Manager('log.txt')

r=Radio(event_manager=em)

while(True):
    print(r.readline())
'''
def _parse_degrees(nmea_data):
    # Parse a NMEA lat/long data pair 'dddmm.mmmm' into a pure degrees value.
    # Where ddd is the degrees, mm.mmmm is the minutes.
    if nmea_data is None or len(nmea_data) < 3:
        return None
    raw = float(nmea_data)
    deg = raw // 100
    minutes = raw % 100
    return deg + minutes/60

def _parse_int(nmea_data):
    if nmea_data is None or nmea_data == '':
        return None
    return int(nmea_data)

def _parse_float(nmea_data):
    if nmea_data is None or nmea_data == '':
        return None
    return float(nmea_data)
def _parse_sentence():
        # Parse any NMEA sentence that is available.
        # pylint: disable=len-as-condition
        # This needs to be refactored when it can be tested.
        sentence = '$PGTOP,11$PGTO104.711002.88'
        if sentence is None or sentence == b'' or len(sentence) < 1:
            return None
        #sentence = str(sentence, 'ascii').strip()
        # Look for a checksum and validate it if present.
        if len(sentence) > 7 and sentence[-3] == '*':
            # Get included checksum, then calculate it and compare.
            expected = int(sentence[-2:], 16)
            actual = 0
            for i in range(1, len(sentence)-3):
                actual ^= ord(sentence[i])
            if actual != expected:
                return None  # Failed to validate checksum.
            # Remove checksum once validated.
            sentence = sentence[:-3]
        # Parse out the type of sentence (first string after $ up to comma)
        # and then grab the rest as data within the sentence.
        delineator = sentence.find(',')
        if delineator == -1:
            return None  # Invalid sentence, no comma after data type.
        data_type = sentence[1:delineator]
        return (data_type, sentence[delineator+1:])

def _parse_gpgga(args):
    # Parse the arguments (everything after data type) for NMEA GPGGA
    # 3D location fix sentence.
    data = args.split(',')
    if data is None or len(data) != 14:
        return  # Unexpected number of params.
    # Parse fix time.
    time_utc = int(_parse_float(data[0]))
    if time_utc is not None:
        hours = time_utc // 10000
        mins = (time_utc // 100) % 100
        secs = time_utc % 100
        # Set or update time to a friendly python time struct.
        if timestamp_utc is not None:
            timestamp_utc = time.struct_time((
                timestamp_utc.tm_year, timestamp_utc.tm_mon,
                timestamp_utc.tm_mday, hours, mins, secs, 0, 0, -1))
        else:
            timestamp_utc = time.struct_time((0, 0, 0, hours, mins,
                                                   secs, 0, 0, -1))
    # Parse latitude and longitude.
    latitude = _parse_degrees(data[1])
    if latitude is not None and \
       data[2] is not None and data[2].lower() == 's':
        latitude *= -1.0
    longitude = _parse_degrees(data[3])
    if longitude is not None and \
       data[4] is not None and data[4].lower() == 'w':
        longitude *= -1.0
    # Parse out fix quality and other simple numeric values.
    fix_quality = _parse_int(data[5])
    satellites = _parse_int(data[6])
    horizontal_dilution = _parse_float(data[7])
    altitude_m = _parse_float(data[8])
    height_geoid = _parse_float(data[10])

def _parse_gprmc(args):
    # Parse the arguments (everything after data type) for NMEA GPRMC
    # minimum location fix sentence.
    data = args.split(',')
    if data is None or len(data) < 11 or data[0] is None:
        return  # Unexpected number of params.
    # Parse fix time.
    time_utc = int(_parse_float(data[0]))
    if time_utc is not None:
        hours = time_utc // 10000
        mins = (time_utc // 100) % 100
        secs = time_utc % 100
        # Set or update time to a friendly python time struct.
        if timestamp_utc is not None:
            timestamp_utc = time.struct_time((
                timestamp_utc.tm_year, timestamp_utc.tm_mon,
                timestamp_utc.tm_mday, hours, mins, secs, 0, 0, -1))
        else:
            timestamp_utc = time.struct_time((0, 0, 0, hours, mins,
                                                   secs, 0, 0, -1))
    # Parse status (active/fixed or void).
    status = data[1]
    fix_quality = 0
    if status is not None and status.lower() == 'a':
        fix_quality = 1
    # Parse latitude and longitude.
    latitude = _parse_degrees(data[2])
    if latitude is not None and \
       data[3] is not None and data[3].lower() == 's':
        latitude *= -1.0
    longitude = _parse_degrees(data[4])
    if longitude is not None and \
       data[5] is not None and data[5].lower() == 'w':
        longitude *= -1.0
    # Parse out speed and other simple numeric values.
    speed_knots = _parse_float(data[6])
    track_angle_deg = _parse_float(data[7])
    # Parse date.
    if data[8] is not None and len(data[8]) == 6:
        day = int(data[8][0:2])
        month = int(data[8][2:4])
        year = 2000 + int(data[8][4:6])  # Y2k bug, 2 digit date assumption.
                                         # This is a problem with the NMEA
                                         # spec and not this code.
        if timestamp_utc is not None:
            # Replace the timestamp with an updated one.
            # (struct_time is immutable and can't be changed in place)
            timestamp_utc = time.struct_time((year, month, day,
                                                   timestamp_utc.tm_hour,
                                                   timestamp_utc.tm_min,
                                                   timestamp_utc.tm_sec,
                                                   0,
                                                   0,
                                                   -1))
        else:
            # Time hasn't been set so create it.
            timestamp_utc = time.struct_time((year, month, day, 0, 0,
                                                   0, 0, 0, -1))

print(_parse_gprmc(_parse_sentence()))
