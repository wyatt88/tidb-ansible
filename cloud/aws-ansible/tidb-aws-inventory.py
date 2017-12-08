#!/usr/bin/env python

import boto3
import os
import argparse
import json

class SearchEC2Tags(object):

  def __init__(self):
    self.parse_args()
    if self.args.list:
      self.search_tags()
    if self.args.host:
      data = {}
      print json.dumps(data, indent=2)

  def parse_args(self):

    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', default=False, help='List instances')
    self.args = parser.parse_args()

  def search_tags(self):
    hosts = {}
    hosts['_meta'] = { 'hostvars': {} }

    for group in ["tidb", "tikv", "pd","monitor"]:
      hosts[group] = []
      tag_key = "Type"
      tag_value = ["group"]
      region = os.environ['REGION']

      ec2 = boto3.resource('ec2', region)

      instances = ec2.instances.filter(Filters=[{'Name': 'tag:'+tag_key, 'Values': tag_value}, {'Name': 'instance-state-name', 'Values': ['running']}])
      for instance in instances:
          hosts[group+"_servers"].append(private_ip_address)
          hosts['_meta']['hostvars'][private_ip_address] = {
             'ansible_ssh_host': instance.private_ip_address

    hosts['monitored_servers'] = {'children':['tidb_servers', 'tikv_servers','pd_servers','spark_master','spark_slaves']}
    print json.dumps(hosts, sort_keys=True, indent=2)

SearchEC2Tags()




