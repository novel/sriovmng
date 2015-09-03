import os
import os.path

from sriovlib import exceptions


SYS_PCI_ADDR_PATH = "/sys/bus/pci/devices"
SYS_IFNAME_PATH = "/sys/class/net/"
VFPREFIX = "virtfn"


def _get_dev_path(ifname):
    dev_path = os.path.join(SYS_IFNAME_PATH, ifname)

    if not os.path.exists(dev_path):
        raise exceptions.SriovDeviceNotFound(device=ifname)

    return dev_path


def ifname_to_pci_addr(ifname):
    dev_path = _get_dev_path(ifname)

    pci_dev_link = os.path.join(dev_path, 'device')
    return os.path.split(os.readlink(pci_dev_link))[1]


def pci_addr_to_ifname(pci_addr):
    pci_path = os.path.join(SYS_PCI_ADDR_PATH, pci_addr)

    if not os.path.exists(pci_path):
        return None

    net_dev_path = os.path.join(pci_path, 'net')
    if not os.path.exists(net_dev_path):
        return None

    items = os.listdir(net_dev_path)
    if len(items) < 1:
        return None

    return items[0]


def show(ifname):
    dev_path = _get_dev_path(ifname)

    pci_dev_link = os.path.join(dev_path, 'device')

    info = {}
    for i in ('device', 'vendor', 'sriov_numvfs'):
        path = os.path.join(pci_dev_link, i)
        with open(path, 'r') as f:
            info[i] = f.read().strip()
    info['pci_addr'] = os.path.split(os.readlink(pci_dev_link))[1]
    info['vfs'] = []
    for i in os.listdir(pci_dev_link):
        if i.startswith(VFPREFIX):
            vf_link = os.path.join(pci_dev_link, i)
            vf_addr = os.path.split(os.readlink(vf_link))[1]
            info['vfs'].append(vf_addr)

    return info


def list():
    sriov_devs = []
    devs = os.listdir(SYS_IFNAME_PATH)
    for dev in devs:
        dev_path = os.path.join(SYS_IFNAME_PATH, dev,
                                'device', 'sriov_numvfs')
        if os.path.exists(dev_path):
            sriov_devs.append(dev)

    return sriov_devs


def set_numvfs(ifname, vfs):
    dev_path = _get_dev_path(ifname)

    numvfs_path = os.path.join(dev_path, 'device', 'sriov_numvfs')
    with open(numvfs_path, 'w') as f:
        vfs = int(vfs)
        f.write("%s" % vfs)
