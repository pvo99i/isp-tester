import ping2
import socket
import argparse
import json
import sqlite3
import datetime
import time
import requests

class pinger_driver:
    def __init__(self, name_, opts):
        self._host = opts['host']
        self._size = int(opts['size'])
        self._name = name_
        self._dest_ip = socket.gethostbyname(self._host)
    def __str__(self):
        return '%s: ping %s with packets of %d' % (self._name, self._host, self._size)
    def name(self):
        return self._name
    def do_test(self):
        res = ping2.single_ping(self._host, self._dest_ip, 3000, 0, self._size, verbose=False)
        return res[0]
    
class http_download_driver:
    def __init__(self, name_, opts):
        self._url = opts['url']
        self._use_credentials = opts['use_credentials'] if 'use_credentials' in opts else False
        self._user = opts['user']
        self._password = opts['password']
        self._name = name_
    def __str__(self):
        return '%s: download from %s %s' % (self._name, self._url, 'with credentials' if self._use_credentials else '')
    def name(self):
        return self._name
    def do_test(self):
        try:
            start_t = time.perf_counter_ns()
            r = requests.get(self._url, allow_redirects=True, verify=False)
            end_t = time.perf_counter_ns()
            elapsed_ns = float(end_t - start_t)
            transferred = int(r.headers['Content-length'])
            return float(transferred * 1000 * 1000 * 1000) / (elapsed_ns)
        except:
            return -1
        
    
def create_driver(driver_type, name, options):
    if driver_type == 'pinger':
        return pinger_driver(name, options)
    if driver_type == 'http_download':
        return http_download_driver(name, options)
    raise "Unknown driver: " + driver_name

def write_start_info(connection):
    connection.execute('INSERT INTO starts (run_date, hostname) VALUES (?, ?)', (datetime.datetime.now(), socket.gethostname()))
    connection.commit()

def open_results_db(path):
    connection = sqlite3.connect(path)
    connection.execute('CREATE TABLE IF NOT EXISTS RESULTS(id INTEGER PRIMARY KEY AUTOINCREMENT, run_date DATETIME, driver VARCHAR(20), score DOUBLE)')
    connection.execute('CREATE TABLE IF NOT EXISTS STARTS(id INTEGER PRIMARY KEY AUTOINCREMENT, run_date DATETIME, hostname VARCHAR(50))')
    connection.commit()    
    return connection

def write_driver_result(connection, driver_name, score):
    connection.execute('INSERT INTO results(run_date, driver, score) VALUES(?, ?, ?)', (datetime.datetime.now(), driver_name, score))
    connection.commit()

def main():
    parser = argparse.ArgumentParser(prog="isp-tester")
    parser.add_argument("--config", required=True)
    parser.add_argument("--user_name")
    parser.add_argument("--password")

    args = parser.parse_args()

    config_json = None
    with open(args.config) as json_data:
        config_json = json.load(json_data)

    drivers = []
    for driver_name in config_json['testers']:
        config = config_json['testers'][driver_name]
        driver_options = config['options']
        driver_options['user'] = args.user_name
        driver_options['password'] = args.password
        driver = create_driver(config['driver'], driver_name, driver_options)
        drivers.append(driver)

    print("Created drivers:")
    for driver in drivers:
        print("%s" % driver)

    out_db = open_results_db(config_json['out_file'])
    write_start_info(out_db)

    while 1:
        for driver in drivers:
            score = driver.do_test()
            print('%s -> %d' % (driver.name(), score))
            write_driver_result(out_db, driver.name(), score)
        time.sleep(config_json['timeout'])
            
    
if __name__ == '__main__':
    main()
