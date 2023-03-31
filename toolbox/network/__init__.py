import socket
import fcntl
import struct
import platform

################################################################################
def get_network_interfaces():
    interfaces = []
    if platform.system() == "Linux":
        # Linux系统下使用ifconfig命令获取网络接口信息
        import subprocess
        cmd_output = subprocess.check_output("ifconfig").decode()
        for line in cmd_output.split("\n\n"):
            fields = line.strip().split("\n")
            if len(fields) < 1:
                continue
            interface = {}
            interface["name"] = fields[0].split(":")[0]
            for field in fields[1:]:
                if "inet " in field:
                    inet_fields = field.strip().split(" ")
                    interface["ip"] = inet_fields[1]
                    interface["netmask"] = inet_fields[3][5:]
                elif "inet6 " in field:
                    inet_fields = field.strip().split(" ")
                    interface["ipv6"] = inet_fields[1]
                elif "ether " in field:
                    ether_fields = field.strip().split(" ")
                    interface["mac"] = ether_fields[1]
            interfaces.append(interface)
        # 使用route命令获取默认网关信息
        cmd_output = subprocess.check_output("route -n").decode()
        for line in cmd_output.split("\n"):
            fields = line.strip().split()
            if len(fields) == 0:
                continue
            if fields[0] == "0.0.0.0" and fields[1] == "UG":
                gateway = fields[1]
                gateway_interface = fields[-1]
                for interface in interfaces:
                    if interface["name"] == gateway_interface:
                        interface["gateway"] = gateway
                        break
        # 使用resolv.conf文件获取DNS服务器信息
        with open("/etc/resolv.conf", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "nameserver" in line:
                    dns_server = line.strip().split()[1]
                    interfaces[0]["dns"] = dns_server
    elif platform.system() == "Darwin":
        # macOS系统下使用socket库获取网络接口信息
        for interface_name in sorted(socket.if_nameindex(), key=lambda x: x[1]):
            interface = {}
            interface["name"] = interface_name[1]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                ip_address = socket.inet_ntoa(fcntl.ioctl(
                    sock.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', interface_name[0][:15].encode())
                )[20:24])
                interface["ip"] = ip_address
            except OSError:
                pass
            interfaces.append(interface)
        # 使用route命令获取默认网关信息
        cmd_output = subprocess.check_output("route -n get default").decode()
        for line in cmd_output.split("\n"):
            fields = line.strip().split(":")
            if len(fields) != 2:
                continue
            key = fields[0].strip()
            value = fields[1].strip()
            if key == "gateway":
                for interface in interfaces:
                    if "ip" in interface and interface["ip"] == value:
                        interface["gateway"] = value
                        break
        # 使用scutil命令获取DNS服务器信息
        cmd_output = subprocess.check_output("scutil --dns").decode()
        for line in cmd_output.split("\n"):
            fields = line.strip().split(": ")
            if len(fields) != 2:
                continue
            key = fields[0].strip()
            value = fields[1].strip()
            if key == "nameserver":
                interfaces[0]["dns"] = value
    elif platform.system() == "Windows":
        # Windows系统下使用socket库获取网络接口信息
        for interface_name in socket.if_nameindex():
            interface = {}
            interface["name"] = interface_name[1]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                ip_address = socket.inet_ntoa(fcntl.ioctl(
                    sock.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', interface_name[0][:15].encode())
                )[20:24])
                interface["ip"] = ip_address
            except OSError:
                pass
            interfaces.append(interface)
        # 使用netsh命令获取默认网关和DNS服务器信息
        cmd_output = subprocess.check_output("netsh interface ip show config").decode()
        interface

################################################################################
def get_subnet_prefix(ip_address, subnet_mask):
    """将 IP 地址和子网掩码转换成二进制形式"""
    ip_binary = ''.join([bin(int(x)+256)[3:] for x in ip_address.split('.')])
    subnet_binary = ''.join([bin(int(x)+256)[3:] for x in subnet_mask.split('.')])
    
    # 计算子网前缀的二进制表示
    subnet_prefix_binary = ''.join([str(int(ip_binary[i]) and int(subnet_binary[i])) for i in range(32)])
    
    # 将二进制表示转换为十进制形式
    subnet_prefix_decimal = [str(int(subnet_prefix_binary[i:i+8], 2)) for i in range(0, 32, 8)]
    
    # 返回子网前缀的十进制表示
    return '.'.join(subnet_prefix_decimal)

################################################################################
import subprocess

def linux_get_network_interfaces():
    interfaces = []
    command = "ip addr"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode("utf-8")
    lines = output.split("\n")
    interface = {}
    for line in lines:
        if ":" in line and not line.startswith(" "):
            if interface:
                interfaces.append(interface)
                interface = {}
            fields = line.strip().split(": ")
            interface["name"] = fields[1]
        elif "inet " in line:
            fields = line.strip().split()
            interface["ip"] = fields[1].split("/")[0]
            interface["netmask"] = fields[3]
        elif "inet6 " in line:
            fields = line.strip().split()
            interface["ipv6"] = fields[1]
        elif "link/ether" in line:
            fields = line.strip().split()
            interface["mac"] = fields[1]
        elif "brd " in line:
            fields = line.strip().split()
            interface["broadcast"] = fields[2]
    interfaces.append(interface)
    
    command = "ip route"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode("utf-8")
    lines = output.split("\n")
    for line in lines:
        if "default via" in line:
            fields = line.strip().split()
            gateway = fields[2]
            break
        interface["gateway"] = gateway
    return interfaces
