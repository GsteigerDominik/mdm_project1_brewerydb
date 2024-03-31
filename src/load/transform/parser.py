def parse_abv(string):
    return string.replace('ABV', '').replace('\n', '')


def parse_brew_style(string):
    return string.replace('Brew Style', '').replace('\n', '')


def parse_primary_flavor_notes(string):
    return list(filter(None, string.replace('Primary Flavor Notes', '').split()))


def parse_srm(string):
    return string.replace('SRM', '').replace('\n', '')


def parse_ibu(string):
    return string.replace('IBU', '').replace('\n', '')


def parse_serving_temperature(string):
    return string.replace('Serving Temperature', '').replace('\n', '').split()[0]
