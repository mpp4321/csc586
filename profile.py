import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG

pc = portal.Context()
request = pc.makeRequestRSpec()

tourDescription = \
"""
This profile provides a three-node set to study NFS/SSO. One node will be the LDAP server, one node will be the NFS server, 
and the remaining node is an NFS client. Both NFS nodes will be authenticated using LDAP. 
"""
#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)
prefixForIP = "192.168.1."
link = request.LAN("lan")

# Add a raw PC to the request.
node1 = request.XenVM("webserver")
node1.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
node1.routable_control_ip = "true"

# Install and execute a script that is contained in the repository.
node1.addService(pg.Execute(shell="sh", command="/local/repository/silly.sh"))

node = request.XenVM("observer")
node.routable_control_ip = "true"  
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
iface = node.addInterface("if" + str(i))
iface.component_id = "eth1"
iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
link.addInterface(iface)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
