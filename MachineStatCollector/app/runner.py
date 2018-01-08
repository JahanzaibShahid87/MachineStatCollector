""" Collect statistics from clients populate database and
 send email alerts if required.
"""

import paramiko
import config
import os
import database
import smtplib
import util
from database import Session
from database.stats import Stats
from database.clients import Client
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


logger = util.set_up_logging(__name__)


def start_runner(client_id, ip, port, username, password):
    try:
        client_id, output = start_collection(
            client_id, ip, port, username, password)
        stats, client, cpu, memory = handle_response(client_id, output)
        check_limit(stats, client, cpu, memory)
    except Exception as e:
        logger.exception(e)


def start_collection(client_id, ip, port, username, password):
    """Given the client information ssh to client
     and get information.
    :param client_id: id of the client inside database
    :param ip: ip of the client
    :param port: port of the client where ssh running
    :param username: username of the client for ssh
    :param password: password of the client for ssh
    """

    ssh_client = paramiko.SSHClient()

    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.load_system_host_keys()
    try:
        ssh_client.connect(ip, port, username, password)
    except Exception as e:
        logger.info(
            "Client having ip {} is down OR make sure ssh server is"
            " installed at client side.").format(ip)
        print "Client having ip {} is down OR make sure ssh server is" \
              " installed at client side.".format(ip)
        raise Exception(e)

    logger.info("ssh connected with {}".format(ip))
    sftp = ssh_client.open_sftp()

    sftp.put(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          config.get("client", "file"))),
             os.path.join(config.get("client", "file_path")))
    sftp.close()

    std_in, std_out, std_err = ssh_client.exec_command(
        "cd /tmp/; chmod u+x get_stats.sh && ./get_stats.sh")

    logger.info("data collected from {}".format(ip))
    output = std_out.readlines()
    ssh_client.close()
    return client_id, output


def handle_response(client_id, output):
    """For give statistics of client populate database.
    :param client_id: id of the client inside database
    :param output: statistics of the client
    """
    cpu = float(output[0])
    memory = float(output[1])
    uptime = output[2]

    stats = database.add_to_database(
        Stats,
        client_id=client_id,
        cpu_usage=cpu,
        memory_usage=memory,
        uptime=uptime)

    client = Session.query(Client).filter(
        Client.id == client_id
    ).one()

    return stats, client, cpu, memory


def check_limit(stats, client, cpu, memory):
    """For given stats check threshold for alert
    :param stats: stats instance of stats table
    :param client: client instance of clients table
    :cpu: last recorded cpu usage of the client
    :memory: last recorded cpu usage of the client
    """

    isemail_send = False
    if memory > client.memory_limit:
        send_email(stats, client, "memory")
        isemail_send = True
        logger.info(
            "Alert email for memory has been"
            " sent for ip {}".format(client.ip))

    if cpu > client.cpu_limit:
        send_email(stats, client, "cpu")
        isemail_send = True
        logger.info(
            "Alert email for cpu has been"
            " sent for ip {}".format(client.ip))

    if not isemail_send:
        logger.info(
            "Everything is good no need to send "
            "an alert email for ip {}".format(client.ip))


def send_email(stats, client, _type):
    """For Given stats of client and type(cpu, memory)
     send alert email.
    :param stats: stats instance of stats table
    :param client: client instance of clients table
    :param _type: type of alert it may be cpu or memory
    """

    fromaddr = config.get("MAIL", "MAIL_SENDER_EMAIL")
    toaddr = client.email

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = get_subject(client)

    body = get_body(stats, client, _type)

    msg.attach(MIMEText(body, 'html'))

    # filename = "NAME OF THE FILE WITH ITS EXTENSION"
    # attachment = open("PATH OF THE FILE", "rb")

    # part = MIMEBase('application', 'octet-stream')
    # part.set_payload((attachment).read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # msg.attach(part)

    server = smtplib.SMTP(config.get("MAIL", "MAIL_SERVER"),
                          config.get("MAIL", "MAIL_PORT"))
    server.starttls()
    # fromaddr = "jahanzaibshahid87@gmail.com"
    server.login(fromaddr, config.get("MAIL", "MAIL_SENDER_PASS"))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def get_subject(client):
    """Given client set subject for email
    :param client: client instance of clients table
    """
    return "Alert for Machine [" + client.ip + "]"


def get_body(stats, client, _type):
    """For Given stats of client and type(cpu, memory)
     set body for email alert.
    :param stats: stats instance of stats table
    :param client: client instance of clients table
    :param _type: type of alert it may be cpu or memory
    """
    if "memory" == _type:
        return """Machine Data Collector found that your threshold for memory has reached.
            <h3>Machine's ip : {}</h3>
            <h4>{} limit: {}%</h4>
            <h4>{} usage reached : {}%</h4>
            """.format(
            client.ip, _type, client.memory_limit, _type, stats.memory_usage)
    else:
        return """Machine Data Collector found that your threshold for cpu has reached.
            <h3>ip : {}</h3>
            <h4>{} limit: {}%</h4>
            <h4>{} usage reached : {}%</h4>
            """.format(
            client.ip, _type, client.cpu_limit, _type, stats.cpu_usage)
