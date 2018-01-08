import os
import xml.etree.ElementTree
from app.collect import Main
from database import Session
from database.clients import Client
from database.stats import Stats
import app


@given(u'that client info {client_id}, {ip}, {port}, {username}, {password}')
def step_impl(context, client_id, ip, port, username, password):
    context.client_id = int(client_id)
    context.ip = ip
    context.port = port
    context.username = username
    context.password = password


@then(u'output should match')
def step_impl(context):
    context.client_id, context.output = app.runner.start_collection(
        context.client_id, context.ip, context.port,
        context.username, context.password
    )

    assert str(context.output[0]) == "2.3"
    assert str(context.output[1]) == "78.7237"
    assert str(
        context.output[2]) == "15:57:19 up  3:28,  1 user,  " \
        "load average: 2.24, 1.93, 1.90 +"


@then(u'All information of client should be popluated in database')
def step_impl(context):
    context.stats, context.client, context.cpu, \
        context.memory = app.runner.handle_response(
            context.client_id, context.output
        )
    assert int(context.stats.client_id) == 1
    assert str(context.stats.cpu_usage) == "2.3"
    assert str(context.stats.memory_usage) == "78.7237"
    assert str(
        context.stats.uptime) == "15:57:19 up  3:28,  1 user,  " \
        "load average: 2.24, 1.93, 1.90 +"


@then(u'subject of email should match')
def step_impl(context):
    subject = app.runner.get_subject(context.client)
    assert subject == "Alert for Machine [" + context.client.ip + "]"


@then(u'body should match for memory with type {_type}')
def step_impl(context, _type):
    body = app.runner.get_body(context.stats, context.client, _type)
    assert body == """Machine Data Collector found that your threshold for memory has reached.
            <h3>Machine's ip : {}</h3>
            <h4>{} limit: {}%</h4>
            <h4>{} usage reached : {}%</h4>
            """.format(
        context.client.ip, _type, context.client.memory_limit, _type,
        context.stats.memory_usage)


@then(u'body should match for cpu with type {_type}')
def step_impl(context, _type):
    body = app.runner.get_body(context.stats, context.client, _type)
    assert body == """Machine Data Collector found that your threshold for cpu has reached.
            <h3>ip : {}</h3>
            <h4>{} limit: {}%</h4>
            <h4>{} usage reached : {}%</h4>
            """.format(
        context.client.ip, _type, context.client.cpu_limit, _type,
        context.stats.cpu_usage)
