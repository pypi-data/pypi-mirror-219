#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Author: Zhaojuan Guo <zguo@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2023 Red Hat, Inc.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from rdmaqe.rdma.sriov.base_sriov import BaseSriov
from libsan.host.cmdline import run
import libsan.host.linux as linux
import os


class Mlx5IbSriov(BaseSriov):

    def __init__(self, hca_id):
        super().__init__()
        self.hca_id = hca_id
        self.pci_device = self.get_pci_from_hca_id()
        self.total_vf = self.get_total_vf()

    def get_pci_from_hca_id(self):
        # get the pci device associated with a given Infiniband device
        pcidevlist = os.listdir("/sys/bus/pci/devices")

        for pcidev in pcidevlist:
            if os.path.isdir(f"/sys/bus/pci/devices/{pcidev}/infiniband"):
                if os.listdir(f"/sys/bus/pci/devices/{pcidev}/infiniband/") == [self.hca_id]:
                    return pcidev

    def set_total_vf(self, total_vf):
        """
        @param pf_bus: device pci, e.g. 82:00.0
        @param total_vf: maximum number of virtual functions that this device can support
        @return:
        """
        if run("which mstconfig") != 0:
            if not linux.install_package("mstflint"):
                print("FAIL: unable to install package mstflint")
                return False
        cmd = f"mstconfig -d {self.pci_device} -y set SRIOV_EN=1 NUM_OF_VFS={total_vf}"
        if run(cmd) != 0:
            print("FAIL: unable to set total_vf. Please check if the device supports this operation")
            return False
        # reboot the system for the change to take effect
        # run("reboot")
        return True

    def get_total_vf(self):
        """
        @param dev_bus: device pci, e.g. 82:00.0
        @return: maximum number of virtual functions that this device can support
        """
        cmd = "mstconfig -d " + self.pci_device + " q | grep NUM_OF_VFS | awk '{print $2}'"
        retcode, output = run(cmd, return_output=True)
        if retcode == 0:
            return output
        else:
            return None

    def get_num_vf(self):
        # to get the count of vfs
        cmd = f"cat /sys/class/infiniband/{self.hca_id}/device/sriov_numvfs"
        retcode, output = run(cmd, return_output=True)
        if retcode == 0:
            return output
        else:
            return None

    def create_num_vf(self, num_vfs):
        """
        @param num_vfs: number of vfs that users want to create
        @return: true if creation succeeds
        """
        if num_vfs > self.total_vf or num_vfs < 0:
            print(f"WARNING: invalid vf count, the num_vfs should be in [0-{self.total_vf}] ")
            return False
        cmd = f"echo {num_vfs} > /sys/class/infiniband/{self.hca_id}/device/sriov_numvfs"
        if run(cmd):
            return True
        else:
            return False

    @staticmethod
    def get_pf_name_from_pf_bus(pf_bus):
        """
        :param pf_bus: e.g. 0000:c4:00.0
        :return: a list of pf_name, e.g. [mlx5_ib0, mlx5_ib1]
        """
        if not pf_bus:
            return None
        _path = "/sys/bus/pci/devices/{}/net".format(pf_bus)
        try:
            return os.listdir(_path)
        except OSError:
            print('No such device.')
            return None

    @staticmethod
    def get_pf_bus_from_pf_name(pf_name):
        """
        :param pf_name: e.g. mlx5_ib0
        :return: e.g. 0000:07:00.0
        """
        if not pf_name:
            return None
        _cmd_str = "ethtool -i {} | grep bus-info | awk '{{print $2}}'".format(pf_name)
        retcode, output = run(_cmd_str)
        if retcode == 0:
            return output
        else:
            print('No such device.')
            return None

    @staticmethod
    def get_all_vfs_from_pf_bus(pf_bus):
        """
        :param pf_bus: e.g. 0000:07:00.0
        :return: ['ibs2f2v0', 'ibs2f3v1']
        """
        vf_names = []
        _base_dir = "/sys/bus/pci/devices/{}".format(pf_bus)
        try:
            for _vf_path in os.listdir(_base_dir):
                if _vf_path.startswith("virtfn"):
                    print(_vf_path)
                    vf_path = "/sys/bus/pci/devices/{}/{}/net".format(pf_bus, _vf_path)
                    print(vf_path)
                    vf_names = vf_names + os.listdir(vf_path)
            return vf_names
        except OSError:
            return None

    def create_vfs(pf_bus, num):
        """
        Usage: create_vfs("0000:07:00.0", "2")
        Return: None
        """
        _total_path = "/sys/bus/pci/devices/{}/sriov_totalvfs".format(pf_bus)
        with open(_total_path, "r") as ft:
            total_vfs = ft.read()
        if num > total_vfs or num < "1":
            print("VFs number should be between 1 and {}".format(total_vfs))
            return 1

        _num_path = "/sys/bus/pci/devices/{}/sriov_numvfs".format(pf_bus)

        with open(_num_path, "w+") as fn:
            current_num = int(fn.read())
            if current_num > 0:
                fn.write("0")
                fn.read()
            fn.write(num)

    def delete_vfs(pf_bus):
        """
        Usage: delete_vfs("0000:07:00.0")
        :return:  None
        """
        _num_path = "/sys/bus/pci/devices/{}/sriov_numvfs".format(pf_bus)

        with open(_num_path, "w") as fn:
                fn.write("0")

    def get_pf_name_from_vf_name(vf_name):
        """
        :param vf_name: e.g. ibs2f2v0
        :return: ['mlx5_ib0']
        """
        _path = "/sys/class/net/{}/device/physfn/net".format(vf_name)
        try:
            return os.listdir(_path)
        except OSError:
            return None

