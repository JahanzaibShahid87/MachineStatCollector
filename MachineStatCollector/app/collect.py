""" Contains method for parsing, processing the
 ingested xml and populate the database.
"""

import xml.etree.ElementTree
import util
import database
from database import Session
from database.clients import Client
import runner


logger = util.set_up_logging(__name__)


class Main(object):

    def parse_collect_data(self, file):
        """Given the file of xml parse and get servers and
         process them to get statistics.
        :param file: Xml file of servers
        """
        root = xml.etree.ElementTree.parse(file).getroot()
        for client_tree in root.findall('client'):
            client_id, ip, port, username, password = self.process(client_tree)
            runner.start_runner(client_id, ip, port, username, password)

        logger.info("Machine data collector completed its processing")
        print "Done !!!"

    def process(self, client_tree):
        """Given the client information populate database.
        :param client_tree : Client information
        :return tuple of client info
        """
        username = client_tree.get('username')
        ip = client_tree.get('ip')
        port = client_tree.get('port')
        password = client_tree.get('password')
        email = client_tree.get('email')

        logger.info("processing information for username : {} ,"
                    " ip: {} , port: {}".format(username, ip, port))

        for alert in client_tree.findall("alert"):
            if "memory" in alert.get("type"):
                memory_threshold = alert.get("limit")
            else:
                cpu_threshold = alert.get("limit")

        memory_threshold = int(memory_threshold.split('%')[0])
        cpu_threshold = int(cpu_threshold.split('%')[0])

        clients = Session.query(Client).filter(
            Client.username == username
        ).filter(
            Client.ip == ip
        ).all()

        if len(clients) == 0:
            client = database.add_to_database(
                Client,
                username=username,
                ip=ip,
                email=email,
                port=port,
                memory_limit=memory_threshold,
                cpu_limit=cpu_threshold)
        else:
            try:
                clients[0].cpu_limit = cpu_threshold
                clients[0].memory_limit = memory_threshold
                Session.commit()
            except Exception as e:
                logger.exception(e)
                logger.error("An error occured while updating the information"
                             " of client having id = {}"
                             .format(clients[0].username))

        client_id = clients[0].id if len(clients) > 0 else client.id
        return client_id, ip, port, username, password
