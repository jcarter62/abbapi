from flask import Flask, jsonify, request
from abb import Sites, SiteMRR, AllSitesMRR
from applogging import AppLogging
from uiapi import UIHome, UISite


app = Flask(__name__)
log = AppLogging(appname='api', app=app)

@app.route('/')
def home():
    log.log_message(msg='/', req=request)
    return jsonify({})


@app.route('/api/uihome')
def route_api_uihome():
    uihome = UIHome()
    result = {'totalflow': uihome.total_flow, 'mrrflow': uihome.mrr_flow, 'sites': uihome.data}
    return jsonify(result), 200


@app.route('/api/uisite/<site>')
def route_api_uisite(site):
    uisite = UISite(sitename=site)
    data = uisite.data
    return jsonify(data), 200


@app.route('/api/sites/names')
def route_api_sites_names():
    log.log_message(req=request)
    sites = Sites()
    names = sites.names
    result = {'names': names}
    return jsonify(result), 200


@app.route('/api/sites')
def route_api_sites():
    log.log_message(req=request)
    sites = Sites()
    result = {'sites': sites.sites['sites']}
    return jsonify(result), 200


@app.route('/api/site/findby/address/<address>')
def route_site_findbyip(address):
    log.log_message(req=request)
    sites = Sites()
    result = sites.find(by_address=address)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({}), 404


@app.route('/api/site/findby/abbname/<abbname>')
def route_site_findbyabbname(abbname):
    log.log_message(req=request)
    sites = Sites()
    result = sites.find(by_abbname=abbname)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({}), 404


@app.route('/api/site/findby/sortname/<name>')
def route_site_findbyname(name):
    log.log_message(req=request)
    sites = Sites()
    result = sites.find(by_sortname=name)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({}), 404


@app.route('/mrr/<site>')
def route_mrr_site(site):
    log.log_message(req=request)
    site_data = SiteMRR(name=site).record
    if site_data:
        result_code = 200
    else:
        result_code = 404   # not found
    result = {"site": site_data}
    return jsonify(result), result_code


@app.route('/mrr')
def route_mrr():
    log.log_message(req=request)
    mrr = AllSitesMRR()
    mrr_data = mrr.data
    if mrr_data:
        return jsonify({"sites": mrr_data}), 200
    else:
        return jsonify({}), 404


@app.route('/order_summary')
def route_order_summary():
    pass


@app.route('/api')
def route_api():
    def add_to_api_list(ary: list, api, desc):
        ary.append({'api': api, 'description': desc})
        return

    log.log_message(req=request)
    result = []
    add_to_api_list(result, '/api/sites', 'list all sites available')
    add_to_api_list(result, '/api/sites/names', 'List of all site names only')
    add_to_api_list(result, '/api/site/findby/address/<address>', 'Find one record, searching by ip address')
    add_to_api_list(result, '/api/site/findby/abbname/<abbname>', 'Find one record, searching by abb name')
    add_to_api_list(result, '/api/site/findby/sortname/<name>', 'Find one record, searching by sort key name')
    add_to_api_list(result, '/mrr', 'Sites Most Recent Reading')
    add_to_api_list(result, '/mrr/<site>', 'One Site most recent reading.')

    add_to_api_list(result, '/order_summary', 'Get orders summary for all sites')
    add_to_api_list(result, '/order_summary/<site>', 'Get orders summary for one site')
    add_to_api_list(result, '/order_detail', 'Get order details for all sites')
    add_to_api_list(result, '/order_detail/<site>', 'Get order details for one site')
    add_to_api_list(result, '/15min-avg-reading/', 'Get 15 minute average reading')
    add_to_api_list(result, '/15min-avg-reading/<site>', 'Get 15 minute average reading for site')

    return jsonify(result), 200


if __name__ == '__main__':
    app.run()
