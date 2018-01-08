import os
import xml.etree.ElementTree
from app.collect import Main
from database import Session
from database.clients import Client


@given(u'that parse the correct config file {filename}')
def step_impl(context, filename):
    _dir = os.path.dirname(__file__)
    filename = os.path.abspath(os.path.join(_dir, "../", filename))
    context.filename = filename


@then(u'all parameters should match')
def step_impl(context):
    root = xml.etree.ElementTree.parse(context.filename).getroot()
    for client_tree in root.findall('client'):
        context.client_id, context.ip, context.port, context.username, \
            context.password = Main().process(client_tree)
        assert context.ip == "192.168.1.104"
        assert context.port == "22"
        assert context.username == "jahanzaib"
        assert context.password == "mobile"


@then(u'database should populate data')
def step_impl(context):
    clients = Session.query(Client).filter(
        Client.id == context.client_id
    ).one()

    assert str(clients.ip) == "192.168.1.104"
    assert str(clients.port) == "22"
    assert str(clients.username) == "jahanzaib"
