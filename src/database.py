# ==================================================================================
#  Copyright (c) 2020 HCL Technologies Limited.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ==================================================================================
import json
import time
from influxdb import InfluxDBClient
from mdclogpy import Logger
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import RequestException, ConnectionError

logger = Logger(name=__name__)
logger.set_level(10)

class DATABASE(object):
    """ 
    DATABASE takes an input as database name. It creates a client connection
    to influxDB and It reads cell-level/slice-level data for a given dabtabase and a measurement.

    Parameters
    ----------
    host: str (default='r4-influxdb.ricplt.svc.cluster.local')
        hostname to connect to InfluxDB
    port: int (default='8086')
        port to connect to InfluxDB
    username: str (default='admin')
        user to connect
    password: str (default='admin')
        password of the use

    """

    def __init__(self, dbname: str = "kpm", user: str = "admin", password: str = "admin", host: str = "ricplt-influxdb.ricplt", port: str = "8086"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.client = None
        self.parse_config()
        self.connect()
    
    def parse_config(self):
        with open("/config/config-file.json") as config_file:
            data = json.load(config_file)
            config = data["influxdb"]

        self.host     = config["host"]
        self.port     = config["port"]
        self.user     = config["user"]
        self.password = config["password"]
        self.dbname   = config["dbname"]

    def connect(self):
        if self.client is not None:
            self.client.close()

        try:
            self.client = InfluxDBClient(self.host, 
                                          port     = self.port, 
                                          username = self.user, 
                                          password = self.password,
                                          database = self.dbname)
            
            version = self.client.request('ping', expected_response_code=204).headers['X-Influxdb-Version']
            logger.info("Conected to Influx Database, InfluxDB version : {}".format(version))
            return True

        except (RequestException, InfluxDBClientError, InfluxDBServerError, ConnectionError):
            logger.error("Failed to establish a new connection with InflulxDB, Please check your url/hostname")
            time.sleep(120)
    
    def read_cell_data(self, RanName: str):
        """

        Parameters
        ----------
        dbname: kpm
        measurement: CellMetrics
        Input: RanName
        Output: DRB.UEThpDl, RRU.PrbAvailDl, RRU.PrbTotDl, RRU.PrbUsedDl
        Num of record: 1

        InfluxQL
        ----------
        select "<field>" from "<measurement>" where "<field>" = [ \'string\' | integer ]

        select * from CellMetrics group by * order by time desc limit 1

        """
        query = 'select "DRB.UEThpDl", "RRU.PrbAvailDl", "RRU.PrbTotDl", "RRU.PrbUsedDl" from CellMetrics where "RanName" = \'{}\' and time > now() - 5s order by time desc limit 1'
        results = self.query(query.format(RanName))
        if results == False:
            return False

        results = list(results.get_points())
        
        # check only one record
        if len(results) != 1:
            return False
        
        result = results[0]

        # organize the format
        data = {
            "DRB_UEThpDl": result["DRB.UEThpDl"],
            "RRU_PrbAvailDl": result["RRU.PrbAvailDl"],
            "RRU_PrbUsedDl": result["RRU.PrbUsedDl"],
            "RRU_PrbTotDl": result["RRU.PrbTotDl"]
        }

        return data

    def read_slice_data(self, RanName: str):
        """

        Parameters
        ----------
        dbname: kpm
        measurement: SliceMetrics
        Input: RanName
        Output: SliceID, RRU.PrbUsedDl.SNSSAI, DRB.UEThpDl.SNSSAI
        Num of record: 1 * Numslice

        InfluxQL
        ----------
        select "<field>" from "<measurement>" where "<field>" = [ \'string\' | integer ]

        select * from CellMetrics order by time desc limit 1

        select * from SliceMetrics where "RanName" = 'gnb_311_048_0000000a' group by * order by time desc limit 1

        """

        query = 'select "DRB.UEThpDl.SNSSAI", "RRU.PrbUsedDl.SNSSAI" from SliceMetrics where "RanName" = \'{}\' and time > now() - 5s group by * order by time desc limit 1'
        results = self.query(query.format(RanName))
        if results == False:
            return False

        results = list(results.items())

        data = []
        for result in results:
            # extract tags and fields
            tags = result[0][1]
            fields = list(result[1])[0]

            # organize the format
            item = {
                "SliceId": tags["SliceID"],
                "DRB_UEThpDl_SNSSAI": fields["DRB.UEThpDl.SNSSAI"],
                "RRU_PrbUsedDl_SNSSAI": fields["RRU.PrbUsedDl.SNSSAI"]
            }
            
            # append to a list
            data.append(item)
        
        return data
            
    def query(self, query):
        try:
            result = self.client.query(query)
        except (RequestException, InfluxDBClientError, InfluxDBServerError, ConnectionError) as e:
            logger.error('Failed to connect to influxdb: {}'.format(e))
            result = False     
        return result

# if __name__ == "__main__":

#     with open("/home/ubuntu/yuehhuan/slicexapp/config/config-file.json") as config_file:
#         data = json.load(config_file)
#         config = data["influxdb"]

#     db = DATABASE(
#         dbname   = config["dbname"],
#         user     = config["user"],
#         password = config["password"],
#         host     = "10.110.239.117",
#         port     = config["port"]
#     )

#     db.connect()
#     slicedata = db.read_slice_data("gnb_311_048_0000000a")
#     print(slicedata)
#     db.read_cell_data("gnb_311_048_0000000a")
