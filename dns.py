import dns.resolver

def dns_lookup(ip_or_domain):
    try:
        # 创建 DNS 解析器
        resolver = dns.resolver.Resolver()

        # 检查输入是否为 IP 地址
        if ip_or_domain.replace('.', '').isdigit():
            # 如果是 IP 地址，直接查询反向 DNS
            reverse_dns_name = dns.reversename.from_address(ip_or_domain)
            result = resolver.query(reverse_dns_name, "PTR")
            for rd in result:
                print(f"Reverse DNS lookup for {ip_or_domain}: {rd.target}")

        else:
            # 如果是域名，则查询各种记录
            # 查询 A 记录（IPv4 地址）
            a_records = resolver.resolve(ip_or_domain, 'A')
            print(f"A Records for {ip_or_domain}:")
            for record in a_records:
                print(record)

            # 查询 AAAA 记录（IPv6 地址）
            aaaa_records = resolver.resolve(ip_or_domain, 'AAAA')
            print(f"AAAA Records for {ip_or_domain}:")
            for record in aaaa_records:
                print(record)

            # 查询 MX 记录（邮件交换服务器）
            mx_records = resolver.resolve(ip_or_domain, 'MX')
            print(f"MX Records for {ip_or_domain}:")
            for record in mx_records:
                print(record)

            # 查询 NS 记录（域名服务器）
            ns_records = resolver.resolve(ip_or_domain, 'NS')
            print(f"NS Records for {ip_or_domain}:")
            for record in ns_records:
                print(record)

    except Exception as e:
        print(f"DNS Lookup failed: {e}")

# 通过用户交互式输入 IP 地址或域名
ip_or_domain = input("Enter IP address or domain name: ")
dns_lookup(ip_or_domain)
