# sriovmng

## About

sriovmng is a tiny tool to make management of SR-IOV based devices a little
easier for those who have a hard time to remember all the necessary paths and
file name in the sysfs filesystem.

## Usage

### List PF devices

```
$ sriovmng.py list
p2p1
p2p2
p5p1
p5p2
$
```

### Show details about PF devices

```
$ sriovmng.py show p2p1
        device: 0x10fb
  sriov_numvfs: 7
        vendor: 0x8086
           vfs: 0000:05:10.0 0000:05:10.2 0000:05:10.4 0000:05:10.6 0000:05:11.0 0000:05:11.2 0000:05:11.4
      pci_addr: 0000:05:00.0
$
```

 * *device*, *vendor*: these are device and vendor IDs
 * *sriov_numvfs*: displays current number of VFs for this devices
 * *vfs*: PCI addresses of the VFs on this device
 * *pci_addr*: PCI address of the device itself

### Getting interface name by PCI address

```
$ sriovmng.py pci_addr_to_ifname 0000:05:10.2
0000:05:10.2: p2p1_1
$ sriovmng.py pci_addr_to_ifname  0000:05:00.0
0000:05:00.0: p2p1
$
```

### Getting PCI address for an interface

```
$ sriovmng.py ifname_to_pci_addr p2p1
p2p1: 0000:05:00.0
$ sriovmng.py ifname_to_pci_addr p2p1_1
p2p1_1: 0000:05:10.2
$
```
