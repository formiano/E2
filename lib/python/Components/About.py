from boxbranding import getBoxType, getMachineBuild, getImageVersion
import struct, socket, fcntl, re, sys, os, time
from sys import modules
from boxbranding import getBoxType, getMachineBuild

def getVersionString():
	return getImageVersion()

def getImageVersionString():
	try:
		if os.path.isfile('/var/lib/opkg/status'):
			st = os.stat('/var/lib/opkg/status')
		else:
			st = os.stat('/usr/lib/ipkg/status')
		tm = time.localtime(st.st_mtime)
		if tm.tm_year >= 2011:
			return time.strftime("%Y-%m-%d %H:%M:%S", tm)
	except:
		pass
	return _("unavailable")

def getFlashDateString():
	try:
		return time.strftime(_("%Y-%m-%d %H:%M:%S"), time.localtime(os.path.getatime("/bin")))
	except:
		return _("unknown")

def getEnigmaVersionString():
	from boxbranding import getImageVersion
	enigma_version = getImageVersion()
	if '-(no branch)' in enigma_version:
		enigma_version = enigma_version [:-12]
	return enigma_version

def getGStreamerVersionString():
	try:
		from glob import glob
		gst = [x.split("Version: ") for x in open(glob("/var/lib/opkg/info/gstreamer[0-9].[0-9].control")[0], "r") if x.startswith("Version:")][0]
		return "%s" % gst[1].split("+")[0].replace("\n","")
	except:
		return _("unknown")

def getKernelVersionString():
	try:
		f = open("/proc/version","r")
		kernelversion = f.read().split(' ', 4)[2].split('-',2)[0]
		f.close()
		return kernelversion
	except:
		return _("unknown")
	
def getModelString():
	try:
		file = open("/proc/stb/info/boxtype", "r")
		model = file.readline().strip()
		file.close()
		return model
	except IOError:
		return "unknown"

def getChipSetString():
	if getMachineBuild() in ('dm7080','dm820'):
		return "7435"
	elif getMachineBuild() in ('dm520','dm525'):
		return "73625"
	elif getMachineBuild() in ('dm900','dm920','et13000','sf5008'):
		return "7252S"
	elif getMachineBuild() in ('hd51','vs1500','h7'):
		return "7251S"
	elif getMachineBuild() in ('vuduo4k'):
		return "7278"
	else:
		try:
			f = open('/proc/stb/info/chipset', 'r')
			chipset = f.read()
			f.close()
			return str(chipset.lower().replace('\n','').replace('bcm','').replace('brcm','').replace('sti',''))
		except IOError:
			return "unavailable"

def getCPUSpeedString():
	if getMachineBuild() in ('u41','u42','u43'):
		return "1,0 GHz"
	elif getMachineBuild() in ('dags72604','vusolo4k','vuultimo4k', 'vuzero4k'):
		return "1,5 GHz"
	elif getMachineBuild() in ('formuler1tc','formuler1', 'triplex', 'tiviaraplus'):
		return "1,3 GHz"
	elif getMachineBuild() in ('gbmv200','u51','u52','u53','u532','u533','u54','u55','u56','u5','u5pvr','h9','h9combo','h10','cc1','sf8008','hd60','hd61','i55plus','ustym4kpro','beyonwizv2','viper4k','v8plus','multibox'):
		return "1,6 GHz"
	elif getMachineBuild() in ('vuuno4kse','vuuno4k','dm900','dm920', 'gb7252', 'dags7252','xc7439','8100s'):
		return "1,7 GHz"
	elif getMachineBuild() in ('vuduo4k'):
		return "2,1 GHz"
	elif getMachineBuild() in ('hd51','hd52','sf4008','vs1500','et1x000','h7','et13000','sf5008','osmio4k','osmio4kplus'):
		try:
			import binascii
			f = open('/sys/firmware/devicetree/base/cpus/cpu@0/clock-frequency', 'rb')
			clockfrequency = f.read()
			f.close()
			return "%s MHz" % str(round(int(binascii.hexlify(clockfrequency), 16)/1000000,1))
		except:
			return "1,7 GHz"
	else:
		try:
			file = open('/proc/cpuinfo', 'r')
			lines = file.readlines()
			for x in lines:
				splitted = x.split(': ')
				if len(splitted) > 1:
					splitted[1] = splitted[1].replace('\n','')
					if splitted[0].startswith("cpu MHz"):
						mhz = float(splitted[1].split(' ')[0])
						if mhz and mhz >= 1000:
							mhz = "%s GHz" % str(round(mhz/1000,1))
						else:
							mhz = "%s MHz" % str(round(mhz,1))
			file.close()
			return mhz
		except IOError:
			return "unavailable"
def getCPUArch():
	if "ARM" in getCPUString():
		return getCPUString()
	return _("Mipsel")

def getCPUString():
	if getMachineBuild() in ('vuduo4k','osmio4k','osmio4kplus','dags72604','vuuno4kse','vuuno4k', 'vuultimo4k','vusolo4k', 'vuzero4k', 'hd51', 'hd52', 'sf4008', 'dm900','dm920', 'gb7252', 'dags7252', 'vs1500', 'et1x000', 'xc7439','h7','8100s','et13000','sf5008'):
		return "Broadcom"
	elif getMachineBuild() in ('gbmv200','u41','u42','u43','u51','u52','u53','u532','u533','u54','u55','u56','u5','u5pvr','h9','h9combo','h10','cc1','sf8008','hd60','hd61','i55plus','ustym4kpro','beyonwizv2','viper4k','v8plus','multibox'):
		return "Hisilicon"
	else:
		try:
			system="unknown"
			file = open('/proc/cpuinfo', 'r')
			lines = file.readlines()
			for x in lines:
				splitted = x.split(': ')
				if len(splitted) > 1:
					splitted[1] = splitted[1].replace('\n','')
					if splitted[0].startswith("system type"):
						system = splitted[1].split(' ')[0]
					elif splitted[0].startswith("Processor"):
						system = splitted[1].split(' ')[0]
			file.close()
			return system
		except IOError:
			return "unavailable"

def getCpuCoresString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("processor"):
					if getMachineBuild() in ('gbmv200','u51','u52','u53','u532','u533','u54','u55','u56','vuultimo4k','u5','u5pvr','h9','h9combo','h10','alien5','cc1','sf8008','hd60','hd61','i55plus','ustym4kpro','beyonwizv2','viper4k','v8plus','vuduo4k','multibox'):
						cores = 4
					elif getMachineBuild() in ('u41','u42','u43'):
						cores = 2
					elif int(splitted[1]) > 0:
						cores = 2
					else:
						cores = 1
		file.close()
		return cores
	except IOError:
		return "unavailable"

def getImageTypeString():
	try:
		image_type = open("/etc/issue").readlines()[-2].strip()[:-6]
		return image_type.capitalize()
	except:
		return _("undefined")

def _ifinfo(sock, addr, ifname):
	iface = struct.pack('256s', ifname[:15])
	info  = fcntl.ioctl(sock.fileno(), addr, iface)
	if addr == 0x8927:
		return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1].upper()
	else:
		return socket.inet_ntoa(info[20:24])

def getIfConfig(ifname):
	ifreq = {'ifname': ifname}
	infos = {}
	sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# offsets defined in /usr/include/linux/sockios.h on linux 2.6
	infos['addr']    = 0x8915 # SIOCGIFADDR
	infos['brdaddr'] = 0x8919 # SIOCGIFBRDADDR
	infos['hwaddr']  = 0x8927 # SIOCSIFHWADDR
	infos['netmask'] = 0x891b # SIOCGIFNETMASK
	try:
		print "in TRYYYYYYY", ifname
		for k,v in infos.items():
			print infos.items()
			ifreq[k] = _ifinfo(sock, v, ifname)
	except:
		print "IN EXCEEEEEEEEPT", ifname
		pass
	sock.close()
	return ifreq

def getIfTransferredData(ifname):
	f = open('/proc/net/dev', 'r')
	for line in f:
		if ifname in line:
			data = line.split('%s:' % ifname)[1].split()
			rx_bytes, tx_bytes = (data[0], data[8])
			f.close()
			return rx_bytes, tx_bytes

def getDriverInstalledDate():
	try:
		from glob import glob
		try:
			driver = [x.split("-")[-2:-1][0][-8:] for x in open(glob("/var/lib/opkg/info/*-dvb-modules-*.control")[0], "r") if x.startswith("Version:")][0]
			return  "%s-%s-%s" % (driver[:4], driver[4:6], driver[6:])
		except:
			driver = [x.split("Version:") for x in open(glob("/var/lib/opkg/info/*-dvb-proxy-*.control")[0], "r") if x.startswith("Version:")][0]
			return  "%s" % driver[1].replace("\n","")
	except:
		return _("unknown")

def getPythonVersionString():
	try:
		import commands
		status, output = commands.getstatusoutput("python -V")
		return output.split(' ')[1]
	except:
		return _("unknown")

def getIsBroadcom():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("Hardware"):
					system = splitted[1].split(' ')[0]
				elif splitted[0].startswith("system type"):
					if splitted[1].split(' ')[0].startswith('BCM'):
						system = 'Broadcom'
		file.close()
		if 'Broadcom' in system:
			return True
		else:
			return False
	except:
		return False

def GetIPsFromNetworkInterfaces():
	import socket, fcntl, struct, array, sys
	is_64bits = sys.maxsize > 2**32
	struct_size = 40 if is_64bits else 32
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	max_possible = 8 # initial value
	while True:
		_bytes = max_possible * struct_size
		names = array.array('B')
		for i in range(0, _bytes):
			names.append(0)
		outbytes = struct.unpack('iL', fcntl.ioctl(
			s.fileno(),
			0x8912,  # SIOCGIFCONF
			struct.pack('iL', _bytes, names.buffer_info()[0])
		))[0]
		if outbytes == _bytes:
			max_possible *= 2
		else:
			break
	namestr = names.tostring()
	ifaces = []
	for i in range(0, outbytes, struct_size):
		iface_name = bytes.decode(namestr[i:i+16]).split('\0', 1)[0].encode('ascii')
		if iface_name != 'lo':
			iface_addr = socket.inet_ntoa(namestr[i+20:i+24])
			ifaces.append((iface_name, iface_addr))
	return ifaces
# For modules that do "from About import about"
about = sys.modules[__name__]
