from astropy.time import Time

def mjd_to_utc(mjd):
    # Convert MJD to UTC using astropy
    time = Time(mjd, format='mjd', scale='utc')
    # Return the UTC datetime
    return time.utc.iso

# Example usage
mjd = 60000.0  # Replace this with your MJD value
utc_time = mjd_to_utc(mjd)
print("UTC Time:", utc_time)
