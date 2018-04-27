from sys import argv

script, data_center, project_name, lb_name = argv

print(f"openstack --os-cloud {data_center} --os-project-name {project_name} loadbalancer listener list --loadbalancer {lb_name} -f json")
