def index():
    print("""
          
Practical 1
Configure IP SLA tracking and path control topology.

-------------------------------------------------------------------------------------------------

Practical 2
Implementation of BGP using AS_path attribute. 

-------------------------------------------------------------------------------------------------

Practical 3
Configuring IBGP and EBGP sessions.

-------------------------------------------------------------------------------------------------

Practical 4
Secure Management Plane.

-------------------------------------------------------------------------------------------------

Practical 5
Configure and verify path control using PBR (Policy Based Routing)

-------------------------------------------------------------------------------------------------

Practical 6
Demonstrate Inter Vlan Routing. 
          
-------------------------------------------------------------------------------------------------

Practical 7
Simulating MP LS environment.

Practical 8 ( prog("7") ) 7 and 8 are combined
Simulating VRF (Virtual Routing and Forwarding).         
-------------------------------------------------------------------------------------------------



          """)
          



def prog(num):
    if(num=="1"):
        print(""" 


PRACTICAL 1 IP SLA

Router 1
conf t
int s1/0
ip add 209.165.201.1 255.255.255.0
no sh
int s1/1
ip add 209.165.202.1 255.255.255.0
no sh
int lo0
ip add 192.168.1.1 255.255.255.0
do sh ip int br | include up


Router 2
conf t
int s1/0
ip add 209.165.201.2 255.255.255.0
no sh
int s1/2
ip add 209.165.200.2 255.255.255.0
no sh
do sh ip int br | include up

Router 3
conf t
int s1/1
ip add 209.165.202.3 255.255.255.0
no sh
int s1/2
ip add 209.165.200.3 255.255.255.0
no sh
do sh ip int br | include up


Router 1
ip route 0.0.0.0 0.0.0.0 209.165.201.2

Router 2
router eigrp 1
network 209.165.200.0 0.0.0.255
network 209.165.201.0 0.0.0.255
no auto-summary

Router 3
router eigrp 1
network 209.165.200.0 0.0.0.255
network 209.165.202.0 0.0.0.255
no auto-summary


Router 2
ip route 192.168.1.0 255.255.255.0 209.165.201.1

Router 3
ip route 192.168.1.0 255.255.255.0 209.165.202.1

r1> do ping 209.165.200.3
r2> do ping 192.168.1.1
r3> do ping 209.165.201.1
r3> do ping 192.168.1.1


r1> hostname branch
r2> hostname isp1
r3> hostname isp2

Router 1 Branch
ip sla 11
icmp-echo 209.165.201.2
frequency 10
exit
ip sla schedule 11 life forever start-time now

do sh ip sla configuration 11
do sh ip sla statistics




        
              """) 

        
    elif(num=="2"):
        print("""


PRACTICAL 2

Router 1
conf t
int s1/0 
ip add 192.168.1.1 255.255.255.0
no sh
int s1/1
ip add 172.16.1.1 255.255.255.0
no sh
int lo0
ip add 10.1.1.1 255.255.255.0
do sh ip int br | include up

Router 2
conf t
int s1/0 
ip add 192.168.1.2 255.255.255.0
no sh
int lo0
ip add 10.2.2.2 255.255.255.0
do sh ip int br | include up

Router 3
conf t
int s1/1
ip add 172.16.1.3 255.255.255.0
no sh
int lo0
ip add 10.3.3.3 255.255.255.0
do sh ip int br | include up



Router 1
router bgp 300
neighbor 192.168.1.2 remote-as 100
neighbor 172.16.1.3 remote-as 200
network 10.1.1.0 mask 255.255.255.0


Router 2
router bgp 100
neighbor 192.168.1.1 remote-as 300
network 10.2.2.0 mask 255.255.255.0


Router 3
router bgp 200
neighbor 172.16.1.1 remote-as 300
network 10.3.3.0 mask 255.255.255.0

do show ip bgp summary
do ping 10.3.3.3 source lo0
do ping 10.2.2.2 source lo0


                """)
        
        

    elif(num=="3"):
        print("""


PRACTICAL 3
Step 1: Drag drop Switch / Routers and Config Routers

R1
conf t
int f0/1 
ip add 192.168.1.1 255.255.255.0
no sh
int s1/0
ip add 172.16.1.1 255.255.255.0
no sh
int s1/1
ip add 172.16.5.1 255.255.255.0
no sh
do sh ip int br | include up



R2 
conf t
int f0/0 
ip add 10.10.10.2 255.255.255.0
no sh
int f0/1
ip add 192.168.2.2 255.255.255.0
no sh
int s1/0
ip add 172.16.1.2 255.255.255.0
no sh
do sh ip int br | include up


R3# 
conf t
int f0/0 
ip add 10.10.10.3 255.255.255.0
no sh
int f0/1
ip add 192.168.3.3 255.255.255.0
no sh
int s1/1
ip add 172.16.5.3 255.255.255.0
no sh
do sh ip int br | include up


Step 2: Configure IRP(Interior Routing Protocol [using OSPF]) in autonomous system 65200 (AS65200)
R2
router ospf 1
network 10.10.10.0 0.0.0.255 area 0
network 192.168.2.0 0.0.0.255 area 1

R3
router ospf 1
network 10.10.10.0 0.0.0.255 area 0
network 192.168.3.0 0.0.0.255 area 2


R3> do ping 192.168.2.2
R2> do ping 192.168.3.3


Step 3: IBGP and EBGP configurations 
R1
router bgp 65100 
network 192.168.1.0 
network 172.16.1.0 mask 255.255.255.0
network 172.16.5.0 mask 255.255.255.0
neighbor 172.16.1.2 remote-as 65200 
neighbor 172.16.5.3 remote-as 65200

R2
router bgp 65200 
network 172.16.1.0 mask 255.255.255.0
redistribute ospf 1
neighbor 172.16.1.1 remote-as 65100
neighbor 10.10.10.3 remote-as 65200

R3
router bgp 65200 
network 172.16.5.0 mask 255.255.255.0
redistribute ospf 1
neighbor 172.16.5.1 remote-as 65100 
neighbor 10.10.10.2 remote-as 65200


Step 4: Final output:
do sh ip route
do show ip bgp summary

R1>
do ping 192.168.2.2
do ping 192.168.3.3



                """)
        
    elif(num=="4"):
        print("""


PRACTICAL 4: Secure management plane.

Step 1: Configure IP
R1> 
conf t
int s1/0 
ip add 10.1.1.1 255.255.255.0
no sh
int lo1
ip add 192.168.1.1 255.255.255.0

R2> 
conf t
int s1/0 
ip add 10.1.1.2 255.255.255.0
no sh
int s1/1 
ip add 10.2.2.2 255.255.255.0
no sh

R3> 
conf t
int s1/1 
ip add 10.2.2.3 255.255.255.0
no sh
int lo1
ip add 192.168.2.1 255.255.255.0


Step 2: Configure Static Routing
R1# 
ip route 0.0.0.0 0.0.0.0 10.1.1.2

R2# 
ip route 192.168.1.0 255.255.255.0 10.1.1.1
ip route 192.168.2.0 255.255.255.0 10.2.2.3

R3# 
ip route 0.0.0.0 0.0.0.0 10.2.2.2

R1> do ping 192.168.2.1
R3> do ping 192.168.1.1


Step 3: Secure management access
R1>
hostname r1
enable secret class12345
line console 0
password ciscoconpass
exec-timeout 5 0
login
logging synchronous
exit

line vty 0  4
password ciscovtypass
exec-timeout 5 0
login
exit
line aux 0
no exec
end
do wr

conf t
service password-encryption
banner motd $Unauthorized access not allowed$
exit


R3>
hostname r3
enable secret class12345
line console 0
password ciscoconpass
exec-timeout 5 0
login
logging synchronous
exit

line vty 0 4
password ciscovtypass
exec-timeout 5 0
login
exit
line aux 0
no exec
end
do wr

conf t
service password-encryption
banner motd $Unauthorized access not allowed$
exit


Step 4: Output
r2> telnet 10.1.1.1

             

                """)
    
    elif(num=="5"):
        print("""


PRACTICAL 5: Path Control Using PBR.

Step 1: Configure IP

R1>
conf t
hostname r1
int s1/0
ip add 172.16.12.1 255.255.255.0
bandwidth 128
no sh
int s1/1
ip add 172.16.13.1 255.255.255.0
bandwidth 64
no sh
int lo0
ip add 192.168.1.1 255.255.255.0
exit 
do sh ip int br | include up

R2> 
conf t
hostname r2
int s1/0
ip add 172.16.12.2 255.255.255.0
bandwidth 128
no sh
int s1/2
ip add 172.16.23.2 255.255.255.0
bandwidth 128
no sh
int lo0
ip add 192.168.2.2 255.255.255.0
exit
do sh ip int br | include up

R3> 
conf t
hostname r3
int s1/1
ip add 172.16.13.3 255.255.255.0
bandwidth 64
no sh
int s1/2
ip add 172.16.23.3 255.255.255.0
bandwidth 128
no sh
int s1/3
ip add 172.16.34.3 255.255.255.0
bandwidth 64
no sh
int lo0
ip add 192.168.3.3 255.255.255.0
do sh ip int br | include up

R4> 
conf t
int s1/3
ip add 172.16.34.4 255.255.255.0
bandwidth 64
no sh
int lo0
ip add 192.168.4.1 255.255.255.0
int lo1
ip add 192.168.5.1 255.255.255.0
exit
do sh ip int br | include up


Step 2: Configure EIGRP on all routers.
R1> 
router eigrp 1
network 172.16.12.0 0.0.0.255
network 172.16.13.0 0.0.0.255
network 192.168.1.0
no auto-summary

R2> 
router eigrp 1
network 172.16.12.0 0.0.0.255
network 172.16.23.0 0.0.0.255
network 192.168.2.0
no auto-summary

R3> 
router eigrp 1
network 172.16.13.0 0.0.0.255
network 172.16.23.0 0.0.0.255
network 172.16.34.0 0.0.0.255
network 192.168.3.0
no auto-summary

R4> 
router eigrp 1
network 172.16.34.0 0.0.0.255
network 192.168.4.0
network 192.168.5.0
no auto-summary


Step 3: check the network
'do sh ip route' on all routers

R1> 
do ping 192.168.4.1

R4> 
do ping 192.168.1.1

USE TRACE ROUTE COMMAND TO VERIFY PATH from R4 to R1 using loopback.
R4> 
do traceroute 192.168.1.1 source 192.168.4.1
do traceroute 192.168.1.1 source 192.168.5.1


Step4: Perform PBR on RECEIVING ROUTER
Configure PBR to providepath control all traffic from source 192.168.5.1 should take 
the path R4 -> R3 -> R1, whereas traffic from 192.168.4.1 should take the path 
R4 -> R3 -> R2 -> R1

R3# 
ip access-list standard pbr-acl
permit 192.168.5.0 0.0.0.255
exit

route-map r3-to-r1 permit
match ip address pbr-acl
set ip next-hop 172.16.13.1
exit

int s1/3
ip policy route-map r3-to-r1
end

Step 5: Output
R4> 
do traceroute 192.168.1.1 source 192.168.4.1
do traceroute 192.168.1.1 source 192.168.5.1


              
                """)


    elif(num=="6"):
        print("""

IVR modern networking pract (1).txt
Goto preferences and check for link lights
              
Task1: check VLAN config in each switch
type command for all switches:
en
show vlan br

CHECK IF ALL SWITCHES HAVE SAME VLAN (1002,1003,1004,1005...)

Task2: disable all ports on all the switches
commands for all switches:
conf t 
interface range fa0/1-24
shutdown
interface range gi0/1-2
shutdown

Task3: Perform basic switch configurations like assign name to switches, password to switches as well as gateways.

hostnames: s0, s1 and s2

commands for all switches:
exit
(config)
hostname s0
enable secret class
no ip domain-lookup
ip default-gateway 172.17.99.1
line console 0

password cisco
login
line vty 0 15
password cisco
login
end

Task4: On the interfaces of the switch 2 connect it to the PCs, configure access mode and enable them

commands for s2:
(config)
int fa0/11
switchport mode access
no shutdown

int fa0/12
switchport mode access
no shutdown

int fa0/13
switchport mode access
no shutdown

Task5: Configure IP addresses on the three PCs and the server

PC0-> Desktop -> IP config 
IP: 172.17.10.21 255.255.255.0
Default gateway: 172.17.10.1

PC1-> Desktop -> IP config 
IP: 172.17.20.22 255.255.255.0
Default gateway: 172.17.20.1

PC2-> Desktop -> IP config 
IP: 172.17.30.23 255.255.255.0
Default gateway: 172.17.30.1

Server -> Desktop -> IP config
IP: 172.17.50.254 255.255.255.0
Default gateway: 172.17.50.1

Task6: Configure VTP protocol on the switches.
s0 will be VTP server, s1 & s2 will be VTP client

s0:
Password: cisco
en Password: class
en
Password:
conf t
vtp mode server
vtp domain vsit
vtp password cisco

s1:
Password:
en
Password:
conf t
vtp mode client
vtp domain vsit
vtp password cisco

s2:
en
conf t
vtp mode client
vtp domain vsit
vtp password cisco

              
              
Task7: Configure trunking codes on all connections between switches and enable them

s0:
(config)
int range fa0/1-3
switchport mode trunk
switchport trunk native vlan 99
no shutdown

int range fa0/5-6
switchport mode trunk
switchport trunk native vlan 99
no shutdown

s2:
(config)
int range fa0/3-6
switchport mode trunk
switchport trunk native vlan 99
no sh

s1:
(config)
int range fa0/1-4
switchport mode trunk
switchport trunk native vlan 99
no sh

s0:
(config-if-range)
exit
(config)
hostname management
(config-vlan)
vlan 10
name staff
vlan 20
name students
vlan 30
name guests

exit
do sh vlan br (On s0 and s2)

Task8: Configure interface vlan 99 on all the switches

s0:
(config)
int vlan 99
(config-if)
ip add 172.17.99.11 255.255.255.0
end

s2:
(config)
int vlan 99
(config-if)
ip add 172.17.99.12 255.255.255.0
end

s1:
(config)
int vlan 99
(config-if)
ip add 172.17.99.13 255.255.255.0
end

Task9: Configure vlan 10, vlan 20 and vlan 30 on switch 2

s2:
(config)
int fa0/11
(config-if)
switchport access vlan 10
int fa0/12
switchport access vlan 20
int fa0/13
switchport access vlan 30

Task10: perform configuration on router
Router:
en
conf t
hostname r1
no ip domain-lookup
line console 0
password cisco
login
line vty 0 15
password cisco
login
end

conf t
(config)
enable secret class
int fa0/1
no sh
int fa0/1.1
encapsulation dot1q 1
ip add 172.17.1.1 255.255.255.0
int fa0/1.10
encapsulation dot1q 10
ip add 172.17.10.1 255.255.255.0
int fa0/1.20
encapsulation dot1q 20
ip add 172.17.20.1 255.255.255.0
int fa0/1.30
encapsulation dot1q 30
ip add 172.17.30.1 255.255.255.0
int fa0/1.99
encapsulation dot1q 99 native
ip add 172.17.99.1 255.255.255.0

Task11: ping/deliver packets
from PCs to Server



                """)
        
    elif(num=="7"):
        print("""

Pract 7 and 8 MN mpls vrf.txt
Pract 7 MN

Step 1: Configure routers

R1> conf t
int lo0
ip add 1.1.1.1 255.255.255.255
ip ospf 1 area 0
int f0/0
ip add 10.0.0.1 255.255.255.0
no sh
ip ospf 1 area 0

R2> conf t
int lo0
ip add 2.2.2.2 255.255.255.255
ip ospf 1 area 0
int f0/0
ip add 10.0.0.2 255.255.255.0
no sh
exit
ip ospf 1 area 0
int f0/1
ip add 10.0.1.2 255.255.255.0
no sh
ip ospf 1 area 0

R3> conf t
int lo0
ip add 3.3.3.3 255.255.255.255
ip ospf 1 area 0
int f0/1
ip add 10.0.1.3 255.255.255.0
no sh
ip ospf 1 area 0

Step 2: Verify connection

R1>(config) do sh ip ospf int br
do sh ip int br include up 
do ping 3.3.3.3 source lo0

R3>(config) do sh ip ospf int br
do sh ip int br | include up
do ping 1.1.1.1 source lo0

Step 3: Configure MPLS

(On ALL routers R1, R2 and R3)
R1,R2,R3> router ospf 1
mpls ldp autoconfig

R2> do sh mpls interface
do sh mpls ldp neigh

Step 4: Configuring VPN

R1> do traceroute 3.3.3.3
router bgp 1
neighbor 3.3.3.3 remote-as 1
neighbor 3.3.3.3 update-source lo0
no auto-summary
address-family vpnv4
neighbor 3.3.3.3 activate 

R3> do traceroute 1.1.1.1 
router bgp 1
neighbor 1.1.1.1 remote-as 1
neighbor 1.1.1.1 update-source lo0
no auto-summary
address-family vpnv4
neighbor 1.1.1.1 activate

(on R1 and R3)
R1,R3> do sh bgp vpnv4 unicast all summary

(On R1 and R2)
R1,R2,> do sh ip route

Step 5: Adding Routers and Configuring VRF (Virtual Routing and Forwarding)

DRAG & DROP router R4, R5

R1>
int f0/1
ip add 192.168.1.1 255.255.255.0
no sh
exit
ip vrf RED
rd 4:4
route-target both 4:4
int f0/1
ip vrf forwarding RED
int f0/1
ip add 192.168.1.1 255.255.255.0
ip ospf 2 area 2
do sh ip ospf int br
do sh ip int br | include up

R3>
int f0/0
ip add 172.168.1.3 255.255.255.0
no sh
exit
ip vrf BLUE
rd 5:5
route-target both 5:5
int f0/0
ip vrf forwarding BLUE
int f0/0
ip add 172.168.1.3 255.255.255.0
ip ospf 3 area 3
do sh ip ospf int br
do sh ip int br | include up

R4> conf t
int lo0
ip add 4.4.4.4 255.255.255.255
ip ospf 2 area 2
int f0/1
ip add 192.168.1.4 255.255.255.0
no sh
ip ospf 2 area 2
int lo0
ip ospf 2 area 2
do sh ip ospf int br
do sh ip int br | include up 

R5> conf t
int lo0
ip add 5.5.5.5 255.255.255.255
ip ospf 3 area 3
int f0/0
ip add 172.168.1.5 255.255.255.0
no sh
ip ospf 3 area 3
int lo0
ip ospf 3 area 3
do sh ip ospf int br
do sh ip int br | include up

Step 6: Verfiy connection

R1>(config) do sh ip route vrf RED
R3>(config) do sh ip route vrf BLUE

                """)




    



    else:
        print("invalid input")



