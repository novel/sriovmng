#!/usr/bin/env python

import sys
import types

import click

import sriovlib


@click.group()
def cli():
    pass


@click.command(short_help='get interface PCI address by its name')
@click.argument('ifname')
def ifname_to_pci_addr(ifname):
    pci_addr = sriovlib.ifname_to_pci_addr(ifname)
    if not pci_addr:
        click.echo('No device found: %s' % ifname, err=True)
        sys.exit(1)

    click.echo("%s: %s" % (ifname, pci_addr))


@click.command(short_help='get interface name by its PCI address')
@click.argument('pci_addr')
def pci_addr_to_ifname(pci_addr):
    ifname = sriovlib.pci_addr_to_ifname(pci_addr)
    if not ifname:
        click.echo('No corresponding device for %s found' % pci_addr,
                   err=True)
        sys.exit(1)
    click.echo("%s: %s" % (pci_addr, ifname))


@click.command(short_help='show details about PF interface')
@click.argument('ifname')
def show(ifname):
    info = sriovlib.show(ifname)
    for k, v in info.iteritems():
        if isinstance(v, types.ListType):
            value = ' '.join(v)
        else:
            value = v
        click.echo("%14s: %s" % (k, value))


@click.command(short_help='show list of PF devices')
def list():
    devices = sriovlib.list()
    for device in devices:
        click.echo("%s" % device)


@click.command(short_help='set number of VFs for PF device')
@click.argument('ifname')
@click.argument('vfs')
def numvfs(ifname, vfs):
    ret = sriovlib.set_numvfs(ifname, vfs)
    if not ret:
        sys.exit(1)


cli.add_command(ifname_to_pci_addr)
cli.add_command(pci_addr_to_ifname)
cli.add_command(show)
cli.add_command(list)
cli.add_command(numvfs)


if "__main__" == __name__:
    cli()
