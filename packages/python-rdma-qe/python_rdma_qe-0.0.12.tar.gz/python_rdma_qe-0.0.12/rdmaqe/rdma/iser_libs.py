"""iser_libs.py: Module to handle iser related."""

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

from libsan.host.cmdline import run

TARGETCLI_CONFIG = "/etc/target/saveconfig.json"


def lio_enable_iser(tgt_iqn, tpg, portal_ip, portal_port="3260", enable_iser="true"):
    """
    Enable iSER
    @param tgt_iqn:
    @param tpg:
    @param portal_ip:
    @param portal_port:
    @param enable_iser:
    @return:
    """
    cmd = "targetcli /iscsi/{}/{}/portals/{}:{} enable_iser {}".format(
        tgt_iqn,
        tpg,
        portal_ip,
        portal_port,
        enable_iser,
    )
    retcode = run(cmd)
    if retcode != 0:
        print("FAIL: Could not enable iser.")
        return False
    return True


def configure_ib_isert():
    pass


def configure_ib_iser():
    pass
