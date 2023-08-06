import os, sys, requests, time, subprocess, mystring
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

def is_docker():
	path = '/proc/self/cgroup'
	return (os.path.exists('/.dockerenv') or os.path.isfile(path) and
			any('docker' in line for line in open(path)))

def wget(url, verify=True):
	to = url.split('/')[-1].replace('%20','_')
	if not os.path.exists(to):
		resp = requests.get(url, allow_redirects=True,verify=verify)
		open(to,'wb').write(resp.content)
	return to

def extract_file_from_zip(local_zipfile, extractedfile):
	import zipfile

	if not os.path.exists(extractedfile):
		cur_folder = os.path.abspath(os.curdir)
		with zipfile.ZipFile(local_zipfile,"r") as zip_ref:
			zip_ref.extractall(cur_folder)
		os.remove(local_zipfile)

	return extractedfile if os.path.exists(extractedfile) else None

def extract_ova_from_zip(local_zipfile):
	if False:
		import zipfile

		ovafile = os.path.basename(local_zipfile).replace('.zip','.ova')
		if not os.path.exists(ovafile):
			cur_folder = os.path.abspath(os.curdir)
			with zipfile.ZipFile(local_zipfile,"r") as zip_ref:
				zip_ref.extractall(cur_folder)
			os.remove(local_zipfile)

		return ovafile if os.path.exists(ovafile) else None
	else:
		return extract_file_from_zip(local_zipfile, os.path.basename(local_zipfile).replace('.zip','.ova'))

def open_port():
	"""
	https://gist.github.com/jdavis/4040223
	"""

	import socket

	sock = socket.socket()
	sock.bind(('', 0))
	x, port = sock.getsockname()
	sock.close()

	return port

def checkPort(port):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = bool(sock.connect_ex(('127.0.0.1', int(port))))
	sock.close()
	return result

def getPort(ports=[], prefix="-p",dup=True):
	if ports is None or ports == []:
		return ''
	if not isinstance(ports, list):
		ports = [ports]
	if prefix is None:
		prefix = ''
	if dup:
		return ' '.join([
			f"{prefix} {port if checkPort(port) else open_port()}:{port}" for port in ports
		])
	else: #Created a flag to support the direct usage of the port instead of linking it to the original port
		return ' '.join([
			f"{prefix} {port if checkPort(port) else open_port()}" for port in ports
		])

cur_dir = lambda: '%cd%' if sys.platform in ['win32', 'cygwin'] else '`pwd`'

@dataclass
class dock:
	"""Class for keeping track of an item in inventory."""
	docker: str = "docker"
	image: str = "frantzme/pythondev:lite"
	ports: list = field(default_factory=list)
	cmd: str = None
	nonet: bool = False
	dind: bool = False
	shared: bool = False
	detach: bool = False
	sudo: bool = False
	remove: bool = True
	mountto: str = "/sync"
	mountfrom: str = None
	name: str = None
	login: bool = False
	loggout: bool = False
	logg: bool = False
	macaddress: str = None
	postClean: bool = False
	preClean: bool = False
	extra: str = None
	save_host_dir: bool = False
	docker_username:str="frantzme"
	docker_id:str=None

	def getDockerImage(self, string, usebaredocker=False):
		if not usebaredocker and "/" not in string:
			use_lite = ":lite" in string
			if "pydev" in string:
				output = f"{self.docker_username}/pythondev:latest"
			elif "pytest" in string:
				output = f"{self.docker_username}/pythontesting:latest"
			else:
				output = f"{self.docker_username}/{string}:latest"
			if use_lite:
				output = output.replace(':latest','') + ":lite"
			output = output.replace(':latest:latest',':latest').replace(':lite:lite',':lite')

			if usebaredocker:
				output = output.replace("{}/".format(docker_username),"")

			return output
		else:
			return string

	def clean(self):
		return "; ".join([
			"{0} kill $({0} ps -a -q)".format(self.docker),
			"{0} kill $({0} ps -q)".format(self.docker),
			"{0} rm $({0} ps -a -q)".format(self.docker),
			"{0} rmi $({0} images -q)".format(self.docker),
			"{0} volume rm $({0} volume ls -q)".format(self.docker),
			"{0} image prune -f".format(self.docker),
			"{0} container prune -f".format(self.docker),
			"{0} builder prune -f -a".format(self.docker)
		])

	def stop_container(self):
		if self.name:
			base = mystring.string("{0} container ls -q --filter name={1}".format(self.docker,self.name))
		elif self.image:
			base = mystring.string("{0} container ls -q --filter ancestor={1}".format(self.docker,self.image))
		else:
			return False

		self.docker_id = base.exec().strip()
		mystring.string("{0} container stop {1}".format(self.docker, self.docker_id)).exec().strip()
		return True

	def stop_volume(self):
		if self.docker_id is None:
			self.stop_container()

		mystring.string("{0} rm -v {1}".format(self.docker, self.docker_id)).exec().strip()
		return True

	def stop_image(self):
		if True:
			images = []
			for image_line in mystring.string("{0} images -a".format("docker")).exec(lines=True):
				if not image_line.empty and "REPOSITORY" not in image_line:
					image_break = mystring.lyst(image_line.split(" ")).trims(lambda x:mystring.string(x).empty)
					images += [{
						"repo":image_break[0],
						"tag":image_break[1],
						"id":image_break[2],
					}]

			to_kill = []
			for image_info in images:
				if self.name:
					print("Not supported yet")
				elif self.image:
					tag = None
					if ":" in self.image:
						image, tag = self.image.split(":")
					if image == image_info['repo'] and (not tag or tag == image_info['tag']):
						to_kill += [image_info['id']]

			for kill in to_kill:
				mystring.string("{0} rmi {1}".format("docker", kill)).exec()
		else:
			if self.docker_id is None:
				self.stop_container()

			mystring.string("{0} rmi {1}".format("docker", self.docker_id)).exec()

		return True

	def kill(self):
		"""
		https://stackoverflow.com/questions/29406871/how-to-filter-docker-process-based-on-image
		https://docs.docker.com/engine/reference/commandline/image_rm/
		https://docs.docker.com/engine/reference/commandline/rmi/
		https://docs.docker.com/engine/reference/commandline/stop/
		https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
		https://contabo.com/blog/how-to-remove-docker-volumes-images-and-containers/
		https://www.ibm.com/docs/en/coss/3.15.4?topic=container-stopping-running
		https://nickjanetakis.com/blog/docker-tip-83-stop-docker-containers-by-name-pattern
		"""
		self.stop_container()
		self.stop_volume()
		self.stop_image()

	def string(self):
		if self.dind or self.shared:
			import platform
			if False and platform.system().lower() == "darwin":  # Mac
				dockerInDocker = "--privileged=true -v /private/var/run/docker.sock:/var/run/docker.sock"
			else:  # if platform.system().lower() == "linux":
				dockerInDocker = "--privileged=true -v /var/run/docker.sock:/var/run/docker.sock"
		else:
			dockerInDocker = ""

		if self.shared:
			exchanged = "-e EXCHANGE_PATH=" + os.path.abspath(os.curdir)
		else:
			exchanged = ""

		no_mount = (self.mountto is None or self.mountto.strip() == '') and (self.mountfrom is None or self.mountfrom.strip() == '')
		dir = cur_dir()
		use_dir = "$EXCHANGE_PATH" if self.shared else (self.mountfrom if self.mountfrom else dir)

		if self.cmd:
			if isinstance(self.cmd, list):
				cmd = ' '.join(self.cmd)
			else:
				cmd = self.cmd 
		else:
			cmd = '/bin/bash'

		network = ""
		if self.nonet:
			network = "--network none" #https://docs.docker.com/network/none/

		my_save_host_dir = ''
		if self.save_host_dir:
			if 'HOSTDIR' in os.environ:
				past_dir,current_dir = os.environ['HOSTDIR'], os.path.abspath(os.curdir).replace('/sync/','')
				my_save_host_dir = '--env="HOSTDIR={0}/{1}"'.format(past_dir,current_dir)
			else:
				my_save_host_dir = '--env="HOSTDIR={0}"'.format(dir)

		return str(self.clean()+";" if self.preClean else "") + "{0} run ".format(self.docker) + " ".join([
			dockerInDocker,
			'--rm' if self.remove else '',
			'-d' if self.detach else '-it',
			'' if no_mount else '-v "{0}:{1}"'.format(use_dir, self.mountto),
			exchanged,
			network,
			getPort(self.ports),
			'--mac-address ' + str(self.macaddress) if self.macaddress else '',
			self.extra if self.extra else '',
			my_save_host_dir,
			self.image,
			cmd
		]) + str(self.clean()+";" if self.postClean else "")

	def __str__(self):
		return self.string()

@dataclass
class vb:
	"""Class for keeping track of an item in inventory."""
	vmname: str = "takenname"
	username: str = None
	ovafile: str = None
	disablehosttime: bool = True
	disablenetwork: bool = True
	biosoffset: str = None
	vmdate: str = None
	network: bool = False
	cpu: int = 2
	ram: int = 4096
	sharedfolder: str = None
	uploadfiles:list = field(default_factory=list)
	vboxmanage: str = "VBoxManage"
	vb_path: str = None
	headless: bool = True
	#cmds_to_exe_with_network:list = field(default_factory=list)
	#cmds_to_exe_without_network:list = field(default_factory=list)

	def on(self,headless:bool=True):
		cmd = "{0} startvm {1}".format(self.vboxmanage,self.vmname)
		if self.headless:
			cmd += " --type headless"

		mystring.string(cmd).exec()

	def vbexe(self, cmd):
		string = "{0} guestcontrol {1} run ".format(self.vboxmanage, self.vmname)
		
		if self.username:
			string += " --username {0} ".format(self.username)

		string += str(" --exe \"C:\\Windows\\System32\\cmd.exe\" -- cmd.exe/arg0 /C '" + cmd.replace("'","\'") + "'")
		mystring.string(string).exec()

	def snapshot_take(self,snapshotname):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} take {2}".format(self.vboxmanage,self.vmname, snapshotname)).exec()

	def snapshot_load(self,snapshotname):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} restore {2}".format(self.vboxmanage,self.vmname, snapshotname)).exec()

	def snapshot_list(self):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} list".format(self.vboxmanage,self.vmname)).exec()

	def snapshot_delete(self,snapshotname):
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} delete {2}".format(self.vboxmanage,self.vmname, snapshotname)).exec()

	def export_to_ova(self,ovaname):
		#https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
		mystring.string("{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage,self.vmname, ovaname)).exec()

	def __shared_folder(self, folder):
		mystring.string("{0}  sharedfolder add {1} --name \"{1}_SharedFolder\" --hostpath \"{2}\" --automount".format(self.vboxmanage, self.vmname, folder)).exec()

	def add_snapshot_folder(self, snapshot_folder):
		if False:
			import datetime, uuid
			from copy import deepcopy as dc
			from pathlib import Path
			import sdock.vbgen as vb_struct

			#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-showvminfo.html
			#VBoxManage showvminfo <X> --machinereadable

			machine_info = mystring.string(
				"{0} showvminfo {1} --machinereadable".format(self.vboxmanage, self.vmname), lines=True
			).exec()
			config_file = None
			for machine_info_line in machine_info:
				machine_info_line = machine_info_line.strip()
				if machine_info_line.startswith("CfgFile"):
					print(machine_info_line)
					config_file = machine_info_line.replace("CfgFile=",'').replace('"','').strip()

			parser = XmlParser()
			og_config = parser.from_path(Path(config_file), vb_struct.VirtualBox)
			
			#Fix the VMDK Potential
			save_files,vdi_file = [],None
			vmdk_files = []
			for filename in os.scandir(snapshot_folder):
				if os.path.isfile(filename.path):
					if filename.name.endswith('.sav'):
						save_files += [filename.path]
					if filename.name.endswith('.vdi'):
						vdi_file = filename.path
					if filename.name.endswith('.vmdk'):
						vmdk_files += [filename.path]
				print(filename.name)
			print(vdi_file)

			"""
			VDI located in StorageControllers-attachedDevice-Image (uuid):> {06509f60-d51f-4ce4-97ed-f83cff79d93e}
			Also located in Machine -> MediaRegistry -> HardDisks -> HardDisk
			"""

			#https://www.tutorialspoint.com/How-to-sort-a-Python-date-string-list
			save_files.sort(key=lambda date: datetime.datetime.strptime('-'.join(date.replace('Snapshots/','').replace('.sav','').split("-")[:-1]), "%Y-%m-%dT%H-%M-%S"))

			copy_hardware=dc(og_config.machine.hardware)
			#save_files.reverse()
			ini_snapshot = vb_struct.Snapshot(
					uuid = "{"+str(uuid.uuid4())+"}",
					name = "SnapShot := 0",
					#time_stamp=save_file_date,
					#state_file=X,
					hardware=copy_hardware,
				)

			new_storage_controller = vb_struct.StorageController(
				name="SATA",
				type="AHCI",
				port_count=1,
				use_host_iocache=False,
				bootable=True,
				ide0_master_emulation_port=0,
				ide0_slave_emulation_port=1,
				ide1_master_emulation_port=2,
				ide1_slave_emulation_port=3,
				# attached_device=""
			)
			new_storage_controller.attached_device.append(vb_struct.AttachedDevice(
				type="HardDisk",
				hotpluggable=False,
				port=0,
				device=0,
				image=vb_struct.Image(
					uuid=os.path.basename(vdi_file).replace(".vdi", "")
				)
			))
			#ini_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller

			#og_config.machine.current_snapshot = ini_snapshot.uuid
			og_config.machine.snapshot = ini_snapshot

			last_snapshot = ini_snapshot


			for save_file in save_files:
				save_file_date = save_file.replace('.sav','')
				temp_snapshot = vb_struct.Snapshot(
					uuid = "{"+str(uuid.uuid4())+"}",
					name = "SnapShot := {0}".format(save_file_date),
					time_stamp=save_file_date,
					#state_file=X,
					hardware=copy_hardware,
				)

				if save_file == save_files[-1]: #LAST ITERATION
					og_config.machine.current_snapshot = temp_snapshot.uuid

					new_storage_controller = vb_struct.StorageController(
						name="SATA",
						type="AHCI",
						port_count=1,
						use_host_iocache=False,
						bootable=True,
						ide0_master_emulation_port=0,
						ide0_slave_emulation_port=1,
						ide1_master_emulation_port=2,
						ide1_slave_emulation_port=3,
						#attached_device=""
					)
					new_storage_controller.attached_device.append(vb_struct.AttachedDevice(
						type="HardDisk",
						hotpluggable=False,
						port=0,
						device=0,
						image=vb_struct.Image(
							uuid=os.path.basename(vdi_file).replace(".vdi","")
						)
					))

					temp_snapshot.hardware.storage_controllers.storage_controller = new_storage_controller
					og_config.machine.current_snapshot = temp_snapshot.uuid
					last_snapshot.snapshots = vb_struct.Snapshots(
						snapshot=[temp_snapshot]
					)

					last_snapshot = temp_snapshot
				else:
					last_snapshot.snapshots = vb_struct.Snapshots(
						[temp_snapshot]
					)
					last_snapshot = temp_snapshot

			og_config.machine.media_registry.hard_disks.hard_disk.hard_disk = vb_struct.HardDisk(
				uuid=os.path.basename(vdi_file).replace(".vdi",""),
				location=vdi_file,
				format="vdi"
			)
			config = SerializerConfig(pretty_print=True)
			serializer = XmlSerializer(config=config)
			og_config_string = serializer.render(og_config)

			for remove,replacewith in [
				('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ',None),
				(' xsi:type="ns0:Snapshot"',None),
				('<ns0:','<'),
				('</ns0:','</'),
				('xmlns:ns0','xmlns'),
			]:
				og_config_string = og_config_string.replace(remove,replacewith or '')


			os.system("cp {0} {0}.OG".format(config_file))
			with open(config_file,"w+") as writer:
				writer.write(og_config_string)

	def import_ova(self, ovafile):
		self.ovafile = ovafile

		mystring.string("{0}  import {1} --vsys 0 --vmname {2} --ostype \"Windows10\" --cpus {3} --memory {4}".format(self.vboxmanage, self.ovafile, self.vmname, self.cpu, self.ram)).exec()

	def disable(self):
		if self.disablehosttime:
			mystring.string("{0} setextradata {1} VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled 1".format(self.vboxmanage, self.vmname)).exec()

		if self.biosoffset:
			mystring.string("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.vmname, self.biosoffset)).exec()

		if self.vmdate:
			ms = round((self.vmdate - datetime.now().date()).total_seconds()*1000)

			mystring.string("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vboxmanage, self.vmname, ms)).exec()

		if self.network is None or self.disablenetwork:
			network = "null"
		mystring.string("{0} modifyvm {1} --nic1 {2}".format(self.vboxmanage, self.vmname, network)).exec()

	def prep(self):
		if self.ovafile:
			self.import_ova(self.ovafile)

		self.disable()
		if self.sharedfolder:
			self.__shared_folder(self.sharedfolder)
		
		for file in list(self.uploadfiles):
			self.uploadfile(file)

		if False:			
			self.start()
			for cmd in self.cmds_to_exe_with_network:
				self.vbexe(cmd)

			#Disable the Network
			mystring.string("{0} modifyvm {1} --nic1 null".format(self.vboxmanage, self.vmname)).exec()
			for cmd in self.cmds_to_exe_without_network:
				self.vbexe(cmd)

			#Turn on the Network
			mystring.string("{0} modifyvm {1} --nic1 nat".format(self.vboxmanage, self.vmname)).exec()
			self.stop()
		
		self.disable()

	def run(self, headless:bool = True):
		self.prep()
		self.on(headless)
	
	def __enter__(self):
		self.run(True)
	
	def off(self):
		mystring.string("{0} controlvm {1} poweroff".format(self.vboxmanage, self.vmname)).exec()

	def __exit__(self, type, value, traceback):
		self.stop()
	
	def uploadfile(self, file:str):
		mystring.string("{0} guestcontrol {1} copyto {2} --target-directory=c:/Users/{3}/Desktop/ --user \"{3}\"".format(self.vboxmanage, self.vmname, file, self.username)).exec()
	
	def clean(self, deletefiles:bool=True):
		cmd = "{0} unregistervm {1}".format(self.vboxmanage, self.vmname)

		if deletefiles:
			cmd += " --delete"
			if self.ovafile:
				os.remove(self.ovafile)

		mystring.string(cmd).exec()
	
	def destroy(self, deletefiles:bool=True):
		self.clean(deletefiles)

@dataclass
class vagrant(object):
	vagrant_base:str = "talisker/windows10pro",
	disablehosttime: bool = True,
	disablenetwork: bool = True,
	vmdate: str = None,
	cpu: int = 2,
	ram: int = 4096,
	uploadfiles: list = None,
	choco_packages:list =  None,
	python_packages:list =  None,
	scripts_to_run:str =  None,
	vb_path: str = None,
	vb_box_exe: str = "VBoxManage"
	headless: bool = True
	save_files:list = None

	def __post_init__(self):
		if self.uploadfiles is None or type(self.uploadfiles) is tuple:
			self.uploadfiles = []

		if self.choco_packages is None or type(self.choco_packages) is tuple:
			self.choco_packages = []

		if self.python_packages is None or type(self.python_packages) is tuple:
			self.python_packages = []

		if self.scripts_to_run is None or type(self.scripts_to_run) is tuple:
			self.scripts_to_run = []

		if self.save_files is None or type(self.save_files) is tuple:
			self.save_files = []
		
		if self.vmdate is None or type(self.vmdate) is tuple:
			self.vmdate = None

	@property
	def vagrant_name(self):
		if not self.vb_path:
			return

		vag_name = None

		folder_name = os.path.basename(os.path.abspath(os.curdir))
		for item in os.listdir(self.vb_path):
			if not os.path.isfile(item) and folder_name in item:
				vag_name = item.split('/')[-1].strip()

		return vag_name

	def snapshot_take(self,snapshotname):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} take {2}".format(self.vboxmanage,vb_name, snapshotname)).exec()

	def snapshot_load(self,snapshotname):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} restore {2}".format(self.vboxmanage,vb_name, snapshotname)).exec()

	def snapshot_list(self):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} list".format(self.vboxmanage,vb_name)).exec()

	def snapshot_delete(self,snapshotname):
		vb_name = self.vagrant_name
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html
		mystring.string("{0} snapshot {1} delete {2}".format(self.vboxmanage,vb_name, snapshotname)).exec()

	def export_to_ova(self,ovaname):
		vb_name = self.vagrant_name
		#https://www.techrepublic.com/article/how-to-import-and-export-virtualbox-appliances-from-the-command-line/
		#https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html
		mystring.string("{0} export {1} --ovf10 --options manifest,iso,nomacs -o {2}".format(self.vboxmanage,vb_name, ovaname)).exec()

	#https://jd-bots.com/2021/05/15/how-to-run-powershell-script-on-windows-startup/
	#https://stackoverflow.com/questions/20575257/how-do-i-run-a-powershell-script-when-the-computer-starts
	def create_runner(self):
		with open("on_login.cmd","w+") as writer:
			writer.write("""powershell -windowstyle hidden C:\\\\Users\\\\vagrant\\\\Desktop\\\\on_start.ps1""")
		return "on_login.cmd"

	def write_startup_file(self):
		contents = []
		if self.vmdate:
			diff_days = (self.vmdate - datetime.now().date()).days
			contents += [
				"Set-Date -Date (Get-Date).AddDays({0})".format(diff_days)
			]

		if self.disablenetwork:
			contents += [
				"""Disable-NetAdapter -Name "*" -Confirm:$false """
			]

		with open("on_start.ps1", "w+") as writer:
			writer.write("""
{0}
""".format(
	"\n".join(contents)
))
		return "on_start.ps1"

	def add_file(self, foil, directory="C:\\\\Users\\\\vagrant\\\\Desktop"):
		return """ win10.vm.provision "file", source: "{0}", destination: "{1}\\\\{0}" """.format(foil, directory)


	def prep(self):
		self.uploadfiles = list(self.uploadfiles)	
		self.uploadfiles += [self.write_startup_file()]
		uploading_file_strings = []
		for foil in self.uploadfiles:
			uploading_file_strings += [self.add_file(foil)]

		uploading_file_strings += [
			self.add_file(self.create_runner(),"""C:\\\\Users\\\\vagrant\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup""")
		]

		scripts = []
		for script in self.scripts_to_run:
			if script:
				scripts += [
					"""win10.vm.provision "shell", inline: <<-SHELL
{0}
SHELL""".format(script)
				]
		
		if self.python_packages != []:
			self.choco_packages += [
				"python38"
			]

		if self.choco_packages:
			choco_script = """win10.vm.provision "shell", inline: <<-SHELL
[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"
iex (wget 'https://chocolatey.org/install.ps1' -UseBasicParsing)
"""

			for choco_package in set(self.choco_packages):
				choco_script += """choco install -y {0} \n""".format(choco_package)	
			
			choco_script += """
SHELL"""

			scripts += [choco_script]

		if self.python_packages != []:
			scripts += [
					""" win10.vm.provision :shell, :inline => "C:\\\\Python38\\\\python -m pip install --upgrade pip {0} " """.format(" ".join(self.python_packages))
			]

		virtualbox_scripts = [
			"vb.gui = {0}".format("false" if self.headless else "true")
		]

		if self.disablehosttime:
			virtualbox_scripts += [
				"""vb.customize [ "guestproperty", "set", :id, "/VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled", 1 ] """
			]

		if len(virtualbox_scripts) > 0:
			virtualbox_scripting = """
config.vm.provider 'virtualbox' do |vb|
{0}
end
""".format("\n".join(virtualbox_scripts))

		contents = """# -*- mode: ruby -*- 
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
	config.vm.define "win10" do |win10| 
    	win10.vm.box = "{0}"
		{1}
		{2}
		{3}
	end
end
""".format(
	self.vagrant_base,
	"\n".join(uploading_file_strings),
	"\n".join(scripts),
	virtualbox_scripting
)
		with open("Vagrantfile", "w+") as vagrantfile:
			vagrantfile.write(contents)

	def on(self):
		mystring.string(""" vagrant up""").exec()

	def resume(self):
		if self.vagrant_name.strip() is not None and self.vagrant_name.strip() != '':
			if self.vmdate:
				diff_days = (self.vmdate - datetime.now().date())
				ms = round(diff_days.total_seconds()*1000)
				mystring.string("{0} modifyvm {1} --biossystemtimeoffset {2}".format(self.vb_box_exe, self.vagrant_name, ms)).exec()

			cmd = "{0} startvm {1}".format(self.vb_box_exe,self.vagrant_name)
			if self.headless:
				cmd += " --type headless"

			mystring.string(cmd).exec()
		else:
			print("Vagrant VM hasn't been created yet")

	def off(self):
		self.vagrant_name
		mystring.string("{0} controlvm {1} poweroff".format(self.vb_box_exe, self.vagrant_name)).exec()
	
	def destroy(self,emptyflag=False):
		self.vagrant_name
		mystring.string(""" vagrant destroy -f """).exec()
		for foil in ["Vagrant", "on_start*", "on_login*"]:
			mystring.string("rm {0}".format(foil)).exec()
		mystring.string("yes|rm -r .vagrant/").exec()
		for foil in list(self.uploadfiles):
			if foil not in self.save_files:
				mystring.string("rm {0}".format(foil)).exec()

	def clean(self,emptyflag=False):
		self.destroy(emptyflag)


def install_docker(save_file:bool=False):
	#https://docs.docker.com/engine/install/ubuntu/
	for string in [
		"curl -fsSL https://get.docker.com -o get-docker.sh",
		"sudo sh ./get-docker.sh --dry-run",
		'echo "Done"' if save_file else "echo \"Done\" && rm get-docker.sh"
	]:
		try:
			mystring.string(string).exec()
		except: pass
