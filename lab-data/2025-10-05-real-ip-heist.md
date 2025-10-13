---
title: "Real IP Heist"
date: "2025-10-05"
slug: "real-ip-heist"
thumbnail: "/assets/img/realip-thumb.png"
tags: "http,headers,samba,ctf"
excerpt: "Exploit of server trusting X-Forwarded-For/X-Real-IP headers to obtain Admin access and flag."
---

**Problem Statement**

Exploit a server that trusts client-supplied X-Forwarded-For/X-Real-IP headers and gain Admin access to retrieve a flag.

**Approach**

1. Reconnaissance: visit target, find login page and admin endpoint.
2. Inspect client-side JS and network requests; discovered server trusts headers.
3. Use curl to spoof `X-Forwarded-For: 127.0.0.1` and set `access_level=Admin`.
4. Access `/admin` and read the flag.

**Tools Used**

- curl
- browser DevTools
- nmap (if needed)

**Screenshots**
<img width="595" height="400" alt="image" src="https://github.com/user-attachments/assets/f0efead9-5081-424d-933e-f15b3a96c6d3" />


**Key Lessons Learned**

- Never trust client-supplied headers.
- Perform server-side validation and enforce role checks.
