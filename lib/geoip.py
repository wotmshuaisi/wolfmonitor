import geoip2.database


class GeoIPClient:
    R = geoip2.database.Reader("data/GeoLite2-City.mmdb")
    ip_addr = ""

    def CityObj(self,):
        return self.R.city(self.ip_addr)

    def get_country(self,):
        cobj = self.CityObj()
        return cobj.country.iso_code

    def get_country_code(self,):
        cobj = self.CityObj()
        return cobj.country.name

    def get_city_name(self,):
        cobj = self.CityObj()
        return cobj.subdivisions.most_specific.name

    def get_location(self,):
        cobj = self.CityObj()
        return (cobj.location.latitude, cobj.location.longitude)
