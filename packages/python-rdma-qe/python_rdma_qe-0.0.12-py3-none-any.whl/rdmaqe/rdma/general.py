#!/usr/bin/env python

"""roce.py: Module to check or configure RDMA. """

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

import os
import json
import re
from libsan.host.cmdline import run

RDMA_BASE = '/sys/class/infiniband'
DEV_INFO_JSON = "/tmp/devinfo.json"


class HCA:
    def __init__(self, hca_id):
        self.hca_id = hca_id
        if ibv_devinfo_2_json(dev=hca_id) == 0:
            self.devinfo_json = DEV_INFO_JSON
        else:
            print("Error: Generating to json file failed.")
            return 1

    def get_port_num(self):
        """
        @return: how many physical ports?
        """
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id]["phys_port_cnt"]

    def get_state(self, port):
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id][port]["state"]

    def get_transport(self):
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id]["transport"]

    def get_link_layer(self, port):
        with open(DEV_INFO_JSON, "r") as info:
            return json.load(info)[self.hca_id][port]["link_layer"]

    def get_protocol(self, port=1):
        """
        @param port: port number, the default is 1.
        @return: the protocol of the specified port, it is iWARP, RoCE or InfiniBand.
        """
        transport = self.get_transport()
        link_layer = self.get_link_layer(port)
        if re.search("iWARP", transport, re.I) and re.search("Ethernet", link_layer, re.I):
            protocol = "iWARP"
        elif re.search("InfiniBand", transport, re.I) and re.search("Ethernet", link_layer, re.I):
            protocol = "RoCE"
        elif re.search("InfiniBand", transport, re.I) and re.search("InfiniBand", link_layer, re.I):
            protocol = "InfiniBand"

        return protocol


def is_rdma_device() -> bool:
    """
    Check if it contains RDMA devices
    @return: True if yes; False if no
    """
    return os.path.exists(RDMA_BASE)


def is_opa_device() -> bool:
    """
    Check if it contains OPA device
    :return:
    True: if yes
    False: if no
    """
    if is_rdma_device():
        for _ in os.listdir("/sys/class/infiniband"):
            if "hfi" in _:
                return True
            else:
                continue

    return False


def get_ibdev():
    # return: ['mlx5_1', 'mlx5_0']
    _ibdev = []
    for dev in os.listdir(RDMA_BASE):
        _ibdev.append(dev)

    return _ibdev


def get_netdev_from_ibdev(ibdev):
    """
    :param dev: ibdev, like mlx5_0
    :return: netdev list, like ['mlx5_roce']
    """
    if not ibdev:
        return None
    _netdev = []
    _dir = '/sys/class/infiniband/{}/device/net/'.format(ibdev)
    for dev in os.listdir(_dir):
        _netdev.append(dev)

    return _netdev


def find_pcidev(ibdev):
    """
    Get the pci device associated with a given Infiniband device
    @param ibdev: ibdev
    @return: pci device
    """
    pdev_list = os.listdir('/sys/bus/pci/devices')
    for pdev in pdev_list:
        if os.path.isdir(f'/sys/bus/pci/devices/{pdev}/infiniband'):
            ibd_list = os.listdir(f'/sys/bus/pci/devices/{pdev}/infiniband')
            if len(ibd_list) > 0 and ibd_list[0] == ibdev:
                return pdev
    return None


def ibdev2netdev(ibdev, verbose=False):
    with open(f"/sys/class/infiniband/{ibdev}/device/resource") as ibrsc_file:
        ibrsc = ibrsc_file.read().strip()

    eths = os.listdir('/sys/class/net')

    for eth in eths:
        filepath_resource = f"/sys/class/net/{eth}/device/resource"

        if os.path.isfile(filepath_resource):
            with open(filepath_resource) as ethrsc_file:
                ethrsc = ethrsc_file.read().strip()

            if ethrsc == ibrsc:
                filepath_devid = f"/sys/class/net/{eth}/dev_id"
                filepath_devport = f"/sys/class/net/{eth}/dev_port"

                if os.path.isfile(filepath_devid):
                    port1 = 0
                    if os.path.isfile(filepath_devport):
                        with open(filepath_devport) as port1_file:
                            port1 = int(port1_file.read().strip())

                    with open(filepath_devid) as port_file:
                        port = int(port_file.read()[2:].strip())

                    if port1 > port:
                        port = port1

                    port += 1

                    filepath_carrier = f"/sys/class/net/{eth}/carrier"

                    if os.path.isfile(filepath_carrier):
                        with open(filepath_carrier) as link_state_file:
                            link_state = "Up" if int(link_state_file.read()) == 1 else "Down"
                    else:
                        link_state = "NA"

                    x = find_pcidev(ibdev)

                    if verbose is True:
                        filepath_portstate = f"/sys/class/infiniband/{ibdev}/ports/{port}/state"
                        filepath_deviceid = f"/sys/class/infiniband/{ibdev}/device/device"
                        filepath_fwver = f"/sys/class/infiniband/{ibdev}/fw_ver"
                        filepath_vpd = f"/sys/class/infiniband/{ibdev}/device/vpd"

                        if os.path.isfile(filepath_portstate):
                            with open(filepath_portstate) as ibstate_file:
                                ibstate = ibstate_file.read().split()[1]
                        else:
                            ibstate = "NA"

                        if os.path.isfile(filepath_deviceid):
                            with open(filepath_deviceid) as devid_file:
                                devid = f"MT{devid_file.read().strip()}"
                        else:
                            devid = "NA"

                        if os.path.isfile(filepath_fwver):
                            with open(filepath_fwver) as fwver_file:
                                fwver = fwver_file.read().strip()
                        else:
                            fwver = "NA"

                        if os.path.isfile(filepath_vpd):
                            with open(filepath_vpd, encoding='unicode_escape') as vpd_file:
                                vpd_content = vpd_file.read().strip()
                                vpd_lines = vpd_content.split(':')
                                devdesc = vpd_lines[0].strip() if len(vpd_lines) > 0 else ""
                                partid = vpd_lines[3].split()[0].strip() if len(vpd_lines) > 3 else "NA"
                        else:
                            devdesc = ""
                            partid = "NA"
                        print(
                            f"{x} {ibdev} ({devid} - {partid}) {devdesc} fw {fwver} port {port} ({ibstate}) ==> {eth} ({link_state})")
                    else:
                        print(f"{ibdev} port {port} ==> {eth} ({link_state})")


def ibv_devinfo_2_json(dev=None, port=None):
    """
    Convert the output of utility ibv_devinfo to json
    @param dev: hca_id, like mlx5_0
    @param port: the port number, 1 is the first port
    @return:
    """
    if dev is not None and port is not None:
        _cmd = "ibv_devinfo -d " + dev + " -i " + port
    elif dev is None and port is not None:
        _cmd = "ibv_devinfo -i " + port
    elif dev is not None and port is None:
        _cmd = "ibv_devinfo -d " + dev
    else:
        _cmd = "ibv_devinfo"

    retcode, devinfo = run(_cmd, return_output=True)
    if retcode == 0:
        data = {}
        pre_hca_id_list = []
        current_hca_id = None
        current_port = None

        for line in devinfo.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('hca_id:'):
                current_hca_id = line.split('hca_id:')[1].strip()
                data[current_hca_id] = {}
            elif line.startswith('port:'):
                current_port = line.split('port:')[1].strip()
                data[current_hca_id][current_port] = {}
            else:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if current_hca_id not in pre_hca_id_list:
                    current_port = None
                    pre_hca_id_list.append(current_hca_id)
                if current_port is None:
                    data[current_hca_id][key] = value.strip()
                else:
                    data[current_hca_id][current_port][key] = value.strip()

        with open(DEV_INFO_JSON, 'w') as f:
            json.dump(data, f, indent=4)

    return retcode


def create_bond(con_name=None, ifname=None, options=None, **kwargs):
    """
    Create network bond
    @param con_name: connection name
    @param ifname: interface name
    @param options: bond options, like options="mode=active-backup,miimon=1000"
    @param kwargs: interfaces that will be attached to the bonding device
    @return: True if creating bond succeeded.
    """
    if con_name is None:
        con_name = "bond0"
    if ifname is None:
        ifname = "bond0"
    _cmd = f'nmcli connection add type bond con-name {con_name} ifname {ifname}'
    if options is not None:
        _cmd = _cmd + f' bond.options {options}'
    if run(_cmd) != 0:
        return False
    # add slave
    for i in kwargs.values():
        _cmd = f"ifenslave {ifname} {i}"
        if run(_cmd) != 0:
            return False
    _cmd = f"nmcli connection up {con_name}"
    if run(_cmd) != 0:
        return False
    return True


def delete_connection(con_name):
    """
    Delete NetworkManager connection using nmcli
    @param con_name: conncetion name
    @return: True if deleting connection succeeds
    """
    _cmd = "nmcli connection delete %s" % con_name
    retcode, output = run(_cmd, return_output=True, verbose=False)
    if retcode != 0:
        print("FAIL: Unable to delete the conn %s" % con_name)
        return False
    print(output)
    return True
