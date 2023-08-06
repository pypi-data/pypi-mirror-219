#!/bin/bash

usage()
{
        echo "$(basename $0) --dev|-d DEV [-h] [-v]"
        echo "-d, --dev                 RDMA device"
        echo "-h, --help                print help message"
        echo "-v, --verbose             print more info"
}
case $1 in
        "-h" | "--help")
                usage
                exit 0
                ;;
esac

dev=""
verbose=0
while test ${#} -gt 0; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            verbose=1
            ;;
        -d|--dev)
            dev=$2
            shift
            ;;
        *)
            break
            ;;
    esac
    shift
done

if [[  -z $dev ]]; then
    usage
    exit 1
fi


function find_pdev() {
  pdevlist=$(ls /sys/bus/pci/devices)

  for pdev in $pdevlist; do
    if [ -d /sys/bus/pci/devices/$pdev/infiniband ]; then
      ibd=$(ls /sys/bus/pci/devices/$pdev/infiniband/)
      if [ "x$ibd" == "x$1" ]; then
        echo -n $pdev
      fi
    fi
  done
}

ibrsc=$(cat /sys/class/infiniband/$d/device/resource)
eths=$(ls /sys/class/net/)
for eth in $eths; do
  filepath_resource=/sys/class/net/$eth/device/resource

  if [ -f $filepath_resource ]; then
    ethrsc=$(cat $filepath_resource)
    if [ "x$ethrsc" == "x$ibrsc" ]; then
      filepath_devid=/sys/class/net/$eth/dev_id
      filepath_devport=/sys/class/net/$eth/dev_port
      if [ -f $filepath_devid ]; then
        port1=0
        if [ -f $filepath_devport ]; then
          port1=$(cat $filepath_devport)
          port1=$(printf "%d" $port1)
        fi

        port=$(cat $filepath_devid)
        port=$(printf "%d" $port)
        if [ $port1 -gt $port ]; then
          port=$port1
        fi

        port=$((port + 1))

        filepath_carrier=/sys/class/net/$eth/carrier

        if [ -f $filepath_carrier ]; then
          link_state=$(cat $filepath_carrier 2>/dev/null)
          if ((link_state == 1)); then
            link_state="Up"
          else
            link_state="Down"
          fi
        else
          link_state="NA"
        fi

        x=$(find_pdev $d)
        if [ "$1" == "-v" ]; then
          filepath_portstate=/sys/class/infiniband/$d/ports/$port/state
          filepath_deviceid=/sys/class/infiniband/$d/device/device
          filepath_fwver=/sys/class/infiniband/$d/fw_ver
          filepath_vpd=/sys/class/infiniband/$d/device/vpd

          # read port state
          if [ -f $filepath_portstate ]; then
            ibstate=$(printf "%-6s" $(cat $filepath_portstate | awk '{print $2}'))
          else
            ibstate="NA"
          fi

          # read device
          if [ -f $filepath_deviceid ]; then
            devid=$(printf "MT%d" $(cat $filepath_deviceid))
          else
            devid="NA"
          fi

          # read FW version
          if [ -f $filepath_fwver ]; then
            fwver=$(cat $filepath_fwver)
          else
            fwver="NA"
          fi

          # read device description and part ID from the VPD
          if [ -f $filepath_vpd ]; then
            tmp=$IFS
            IFS=":"
            vpd_content=$(cat $filepath_vpd)
            devdesc=$(printf "%-15s" $(echo $vpd_content | strings | head -1))
            partid=$(printf "%-11s" $(echo $vpd_content | strings | head -4 | tail -1 | awk '{print $1}'))
            IFS=$tmp
          else
            devdesc=""
            partid="NA"
          fi
          echo "$x $d ($devid - $partid) $devdesc fw $fwver port $port ($ibstate) ==> $eth ($link_state)"
        else
          echo "$d port $port ==> $eth ($link_state)"
        fi
      fi
    fi
  fi
done