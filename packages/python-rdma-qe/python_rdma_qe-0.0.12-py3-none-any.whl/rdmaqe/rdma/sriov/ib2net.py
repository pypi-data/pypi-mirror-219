def find_pcidev(ibdev):
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