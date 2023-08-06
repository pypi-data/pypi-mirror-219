**Table of Contents**

- [Installation](#installation)

## Description
Redhat Kernel RDMA QE Python libs and tests.

## Installation

```console
$ dnf install -y python3-pip.noarch
$ pip3 install --user python-rdma-qe
```
## Upgrade
```console
$ pip3 list | grep python-rdma-qe
$ pip3 install -U python-rdma-qe
```
## Uninstallation
```console
$ pip3 uninstall python-rdma-qe
```
## Usage
```console
$ python3
Python 3.9.16 (main, Mar  7 2023, 00:00:00) 
[GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import rdmaqe.rdma.general as g
>>> hca = g.HCA("hfi1_0")
INFO: [2023-06-13 03:25:58] Running: 'ibv_devinfo -d hfi1_0'...
hca_id:	hfi1_0
	transport:			InfiniBand (0)
	fw_ver:				1.27.0
	node_guid:			0011:7501:0167:0fb0
	sys_image_guid:			0011:7501:0167:0fb0
	vendor_id:			0x1175
	vendor_part_id:			9456
	hw_ver:				0x10
	board_id:			Cornelis Omni-Path Host Fabric Interface Adapter 100 Series
	phys_port_cnt:			1
		port:	1
			state:			PORT_ACTIVE (4)
			max_mtu:		4096 (5)
			active_mtu:		4096 (5)
			sm_lid:			5
			port_lid:		6
			port_lmc:		0x00
			link_layer:		InfiniBand
>>> print(hca.get_protocol("1"))
InfiniBand
```
