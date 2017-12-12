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
    parser.add_argument('--host', action='store_true', help='Get all the variables about a specific instance')
    self.args = parser.parse_args()

  def search_tags(self):
    hosts = {}
    hosts['_meta'] = { 'hostvars': {} }
    hosts['all'] = {
      "vars": {
        "ansible_user": "ec2-user",
        
      }
    }
    for group in ["tidb", "tikv", "pd","monitoring"]:
      hosts[group+"_servers"] = []
      tag_key = "Type"
      tag_value = [group]
      region = os.environ['REGION']

      ec2 = boto3.resource('ec2', region)

      instances = ec2.instances.filter(Filters=[{'Name': 'tag:'+tag_key, 'Values': tag_value}, {'Name': 'instance-state-name', 'Values': ['running']}])
      for instance in instances:
          if group == "monitoring":
            hosts['grafana_servers'] = []
            hosts['grafana_servers'].append(instance.private_ip_address)
            hosts['_meta']['hostvars'][instance.private_ip_address] = {
             'ansible_ssh_host': instance.private_ip_address
            }
          hosts[group+"_servers"].append(instance.private_ip_address)
          hosts['_meta']['hostvars'][instance.private_ip_address] = {
             'ansible_ssh_host': instance.private_ip_address
          }
    hosts['monitored_servers'] = {'children':['tidb_servers', 'tikv_servers','pd_servers','spark_master','spark_slaves']}
    print json.dumps(hosts, sort_keys=True, indent=2)

SearchEC2Tags()




