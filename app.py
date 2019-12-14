from flask import Flask, jsonify, request
from abbsites import AbbSites
from applogging import AppLogging

app = Flask(__name__)
log = AppLogging(appname='api', app=app)

@app.route('/')
def home():
    log.log_message(msg='/', req=request )
    return jsonify({})


@app.route('/api/sites/names')
def route_api_sites_names():
    sites = AbbSites()
    names = sites.names
    result = {'names': names}
    return jsonify(result), 200


@app.route('/api/sites')
def route_api_sites():
    sites = AbbSites()
    result = {'sites': sites.sites['sites']}
    return jsonify(result), 200


@app.route('/api/site/findby/address/<address>')
def route_site_findbyip(address):
    sites = AbbSites()
    result = sites.find(by_address=address)
    return jsonify(result), 200


@app.route('/api/site/findby/abbname/<abbname>')
def route_site_findbyabbname(abbname):
    sites = AbbSites()
    result = sites.find(by_abbname=abbname)
    return jsonify(result), 200


@app.route('/api/site/findby/sortname/<name>')
def route_site_findbyname(name):
    sites = AbbSites()
    result = sites.find(by_sortname=name)
    return jsonify(result), 200


@app.route('/api')
def route_api():
    def add_to_api_list(ary: list, api, desc):
        ary.append({'api': api, 'description': desc})
        return

    result = []
    add_to_api_list(result, '/api/sites', 'list all sites available')
    add_to_api_list(result, '/api/sites/names', 'List of all site names only')
    add_to_api_list(result, '/api/site/findby/address/<address>', 'Find one record, searching by ip address')
    add_to_api_list(result, '/api/site/findby/abbname/<abbname>', 'Find one record, searching by abb name')
    add_to_api_list(result, '/api/site/findby/sortname/<name>', 'Find one record, searching by sort key name')

    return jsonify(result), 200


if __name__ == '__main__':
    app.run()
