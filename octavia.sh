#!/bin/bash

$data_center = List from RD?
$project_name = Text from RD
$lb_name = Text from RD

openstack --os-cloud $data_center --os-project-name $project_name loadbalancer listener list --loadbalancer $lb_name -f json
