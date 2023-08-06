from dataclasses import dataclass, field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.virtualbox.org/"


@dataclass
class AudioAdapter:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    controller: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    driver: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    enabled_out: Optional[bool] = field(
        default=None,
        metadata={
            "name": "enabledOut",
            "type": "Attribute",
        }
    )


@dataclass
class Clipboard:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    mode: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Controller:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Display:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    controller: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    vramsize: Optional[int] = field(
        default=None,
        metadata={
            "name": "VRAMSize",
            "type": "Attribute",
        }
    )


@dataclass
class DragAndDrop:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    mode: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ExtraDataItem:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Group:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class GuestProperty:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Union[int, str, bool]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    timestamp: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    flags: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Hid:
    class Meta:
        name = "HID"
        namespace = "http://www.virtualbox.org/"

    pointing: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pointing",
            "type": "Attribute",
        }
    )


@dataclass
class HardDisk:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    hard_disk: Optional["HardDisk"] = field(
        default=None,
        metadata={
            "name": "HardDisk",
            "type": "Element",
        }
    )


@dataclass
class HardwareVirtExLargePages:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Ioapic:
    class Meta:
        name = "IOAPIC"
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Image:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class InternalNetwork:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class LongMode:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Memory:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    ramsize: Optional[int] = field(
        default=None,
        metadata={
            "name": "RAMSize",
            "type": "Attribute",
        }
    )


@dataclass
class Nat:
    class Meta:
        name = "NAT"
        namespace = "http://www.virtualbox.org/"

    localhost_reachable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "localhost-reachable",
            "type": "Attribute",
        }
    )


@dataclass
class Pae:
    class Meta:
        name = "PAE"
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class SharedFolder:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    host_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "hostPath",
            "type": "Attribute",
        }
    )
    writable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    auto_mount: Optional[bool] = field(
        default=None,
        metadata={
            "name": "autoMount",
            "type": "Attribute",
        }
    )


@dataclass
class Vrdeproperties:
    class Meta:
        name = "VRDEProperties"
        namespace = "http://www.virtualbox.org/"




@dataclass
class Natnetwork:
    class Meta:
        name = "NATNetwork"
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Order:
    position: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    device: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Property:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )






@dataclass
class SmbiosUuidLittleEndian:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

@dataclass
class AttachedDevice:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    passthrough: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    hotpluggable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    port: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    device: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    image: Optional[Image] = field(
        default=None,
        metadata={
            "name": "Image",
            "type": "Element",
        }
    )


@dataclass
class TimeOffset:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

@dataclass
class Bios:
    class Meta:
        name = "BIOS"
        namespace = "http://www.virtualbox.org/"

    ioapic: Optional[Ioapic] = field(
        default=None,
        metadata={
            "name": "IOAPIC",
            "type": "Element",
        }
    )
    time_offset: Optional[TimeOffset] = field(
        default=None,
        metadata={
            "name": "TimeOffset",
            "type": "Element",
        }
    )
    smbios_uuid_little_endian: Optional[SmbiosUuidLittleEndian] = field(
        default=None,
        metadata={
            "name": "SmbiosUuidLittleEndian",
            "type": "Element",
        }
    )


@dataclass
class Boot:
    order: List[Order] = field(
        default_factory=list,
        metadata={
            "name": "Order",
            "type": "Element",
        }
    )


@dataclass
class Cpu:
    class Meta:
        name = "CPU"
        namespace = "http://www.virtualbox.org/"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    pae: Optional[Pae] = field(
        default=None,
        metadata={
            "name": "PAE",
            "type": "Element",
        }
    )
    long_mode: Optional[LongMode] = field(
        default=None,
        metadata={
            "name": "LongMode",
            "type": "Element",
        }
    )
    hardware_virt_ex_large_pages: Optional[HardwareVirtExLargePages] = field(
        default=None,
        metadata={
            "name": "HardwareVirtExLargePages",
            "type": "Element",
        }
    )


@dataclass
class Controllers:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    controller: Optional[Controller] = field(
        default=None,
        metadata={
            "name": "Controller",
            "type": "Element",
        }
    )


@dataclass
class Dvdimages:
    class Meta:
        name = "DVDImages"
        namespace = "http://www.virtualbox.org/"

    image: Optional[Image] = field(
        default=None,
        metadata={
            "name": "Image",
            "type": "Element",
        }
    )


@dataclass
class DisabledModes:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    nat: Optional[Nat] = field(
        default=None,
        metadata={
            "name": "NAT",
            "type": "Element",
        }
    )
    internal_network: Optional[InternalNetwork] = field(
        default=None,
        metadata={
            "name": "InternalNetwork",
            "type": "Element",
        }
    )
    natnetwork: Optional[Natnetwork] = field(
        default=None,
        metadata={
            "name": "NATNetwork",
            "type": "Element",
        }
    )


@dataclass
class ExtraData:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    extra_data_item: List[ExtraDataItem] = field(
        default_factory=list,
        metadata={
            "name": "ExtraDataItem",
            "type": "Element",
        }
    )


@dataclass
class Groups:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    group: Optional[Group] = field(
        default=None,
        metadata={
            "name": "Group",
            "type": "Element",
        }
    )


@dataclass
class GuestProperties:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    guest_property: List[GuestProperty] = field(
        default_factory=list,
        metadata={
            "name": "GuestProperty",
            "type": "Element",
        }
    )


@dataclass
class HardDisks:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    hard_disk: Optional[HardDisk] = field(
        default=None,
        metadata={
            "name": "HardDisk",
            "type": "Element",
        }
    )


@dataclass
class SharedFolders:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    shared_folder: List[SharedFolder] = field(
        default_factory=list,
        metadata={
            "name": "SharedFolder",
            "type": "Element",
        }
    )


@dataclass
class Vrdeproperties:
    class Meta:
        name = "VRDEProperties"
        namespace = "http://www.virtualbox.org/"

    property: List[Property] = field(
        default_factory=list,
        metadata={
            "name": "Property",
            "type": "Element",
        }
    )


@dataclass
class Adapter:
    slot: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    macaddress: Optional[str] = field(
        default=None,
        metadata={
            "name": "MACAddress",
            "type": "Attribute",
        }
    )
    cable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    disabled_modes: Optional[DisabledModes] = field(
        default=None,
        metadata={
            "name": "DisabledModes",
            "type": "Element",
        }
    )
    nat: Optional[Nat] = field(
        default=None,
        metadata={
            "name": "NAT",
            "type": "Element",
        }
    )


@dataclass
class MediaRegistry:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    hard_disks: Optional[HardDisks] = field(
        default=None,
        metadata={
            "name": "HardDisks",
            "type": "Element",
        }
    )
    dvdimages: Optional[Dvdimages] = field(
        default=None,
        metadata={
            "name": "DVDImages",
            "type": "Element",
        }
    )


@dataclass
class Network:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    adapter: Optional[Adapter] = field(
        default=None,
        metadata={
            "name": "Adapter",
            "type": "Element",
        }
    )

@dataclass
class RemoteDisplay:
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    vrdeproperties: Optional[Vrdeproperties] = field(
        default=None,
        metadata={
            "name": "VRDEProperties",
            "type": "Element",
        }
    )


@dataclass
class StorageController:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    port_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PortCount",
            "type": "Attribute",
        }
    )
    use_host_iocache: Optional[bool] = field(
        default=None,
        metadata={
            "name": "useHostIOCache",
            "type": "Attribute",
        }
    )
    bootable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Bootable",
            "type": "Attribute",
        }
    )
    ide0_master_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE0MasterEmulationPort",
            "type": "Attribute",
        }
    )
    ide0_slave_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE0SlaveEmulationPort",
            "type": "Attribute",
        }
    )
    ide1_master_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE1MasterEmulationPort",
            "type": "Attribute",
        }
    )
    ide1_slave_emulation_port: Optional[int] = field(
        default=None,
        metadata={
            "name": "IDE1SlaveEmulationPort",
            "type": "Attribute",
        }
    )
    attached_device: List[AttachedDevice] = field(
        default_factory=list,
        metadata={
            "name": "AttachedDevice",
            "type": "Element",
        }
    )


@dataclass
class Usb:
    class Meta:
        name = "USB"
        namespace = "http://www.virtualbox.org/"

    controllers: Optional[Controllers] = field(
        default=None,
        metadata={
            "name": "Controllers",
            "type": "Element",
        }
    )


@dataclass
class Network:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    adapter: Optional[Adapter] = field(
        default=None,
        metadata={
            "name": "Adapter",
            "type": "Element",
        }
    )


@dataclass
class StorageControllers:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    storage_controller: Optional[StorageController] = field(
        default=None,
        metadata={
            "name": "StorageController",
            "type": "Element",
        }
    )


@dataclass
class Hardware:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    cpu: Optional[Cpu] = field(
        default=None,
        metadata={
            "name": "CPU",
            "type": "Element",
        }
    )
    memory: Optional[Memory] = field(
        default=None,
        metadata={
            "name": "Memory",
            "type": "Element",
        }
    )
    boot: Optional[Boot] = field(
        default=None,
        metadata={
            "name": "Boot",
            "type": "Element",
        }
    )
    remote_display: Optional[RemoteDisplay] = field(
        default=None,
        metadata={
            "name": "RemoteDisplay",
            "type": "Element",
        }
    )
    hid: Optional[Hid] = field(
        default=None,
        metadata={
            "name": "HID",
            "type": "Element",
        }
    )
    display: Optional[Display] = field(
        default=None,
        metadata={
            "name": "Display",
            "type": "Element",
        }
    )
    bios: Optional[Bios] = field(
        default=None,
        metadata={
            "name": "BIOS",
            "type": "Element",
        }
    )
    usb: Optional[Usb] = field(
        default=None,
        metadata={
            "name": "USB",
            "type": "Element",
        }
    )
    network: Optional[Network] = field(
        default=None,
        metadata={
            "name": "Network",
            "type": "Element",
        }
    )
    audio_adapter: Optional[AudioAdapter] = field(
        default=None,
        metadata={
            "name": "AudioAdapter",
            "type": "Element",
        }
    )
    shared_folders: Optional[SharedFolders] = field(
        default=None,
        metadata={
            "name": "SharedFolders",
            "type": "Element",
        }
    )
    clipboard: Optional[Clipboard] = field(
        default=None,
        metadata={
            "name": "Clipboard",
            "type": "Element",
        }
    )
    drag_and_drop: Optional[DragAndDrop] = field(
        default=None,
        metadata={
            "name": "DragAndDrop",
            "type": "Element",
        }
    )
    guest_properties: Optional[GuestProperties] = field(
        default=None,
        metadata={
            "name": "GuestProperties",
            "type": "Element",
        }
    )
    storage_controllers: Optional[StorageControllers] = field(
        default=None,
        metadata={
            "name": "StorageControllers",
            "type": "Element",
        }
    )

@dataclass
class Snapshots:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    snapshot: List[object] = field(
        default=list,
        metadata={
            "name": "Snapshot",
            "type": "Element",
        }
    )

@dataclass
class Snapshot:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    time_stamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "timeStamp",
            "type": "Attribute",
        }
    )
    state_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "stateFile",
            "type": "Attribute",
        }
    )
    hardware: Optional[Hardware] = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
        }
    )
    snapshots: Optional[Snapshots] = field(
        default=None,
        metadata={
            "name": "Snapshots",
            "type": "Element",
        }
    )


@dataclass
class Machine:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ostype: Optional[str] = field(
        default=None,
        metadata={
            "name": "OSType",
            "type": "Attribute",
        }
    )
    state_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "stateFile",
            "type": "Attribute",
        }
    )
    current_snapshot: Optional[str] = field(
        default=None,
        metadata={
            "name": "currentSnapshot",
            "type": "Attribute",
        }
    )
    snapshot_folder: Optional[str] = field(
        default=None,
        metadata={
            "name": "snapshotFolder",
            "type": "Attribute",
        }
    )
    current_state_modified: Optional[bool] = field(
        default=None,
        metadata={
            "name": "currentStateModified",
            "type": "Attribute",
        }
    )
    last_state_change: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastStateChange",
            "type": "Attribute",
        }
    )
    aborted: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    media_registry: Optional[MediaRegistry] = field(
        default=None,
        metadata={
            "name": "MediaRegistry",
            "type": "Element",
        }
    )
    extra_data: Optional[ExtraData] = field(
        default=None,
        metadata={
            "name": "ExtraData",
            "type": "Element",
        }
    )
    snapshot: Optional[Snapshot] = field(
        default=None,
        metadata={
            "name": "Snapshot",
            "type": "Element",
        }
    )
    hardware: Optional[Hardware] = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
        }
    )
    groups: Optional[Groups] = field(
        default=None,
        metadata={
            "name": "Groups",
            "type": "Element",
        }
    )


@dataclass
class VirtualBox:
    class Meta:
        namespace = "http://www.virtualbox.org/"

    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    machine: Optional[Machine] = field(
        default=None,
        metadata={
            "name": "Machine",
            "type": "Element",
        }
    )
