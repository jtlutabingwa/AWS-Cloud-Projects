# EC2 Web Server
 
Launched an EC2 instance on AWS and deployed a custom static web page using Nginx. This was my first hands-on cloud project to get familiar with core AWS services.
 
## Overview
 
| | |
|---|---|
| **Services Used** | EC2, VPC, Security Groups |
| **Instance Type** | t2.micro (Free Tier) |
| **OS** | Amazon Linux 2023 |
| **Web Server** | Nginx |
 
## Architecture
 
```
User (Browser)
     │
     │  HTTP (port 80)
     ▼
┌──────────────┐
│  Security    │  ← Port 22 (SSH, my IP only)
│  Group       │  ← Port 80 (HTTP, anywhere)
└──────┬───────┘
       ▼
┌──────────────┐
│  EC2         │
│  t2.micro    │
│              │
│  Amazon      │
│  Linux 2023  │
│              │
│  Nginx       │
└──────────────┘
```
 
## What I Did
 
### Set Up the Security Group
 
Created a security group called `web-server-sg` to act as a firewall for the instance. Opened port 22 for SSH (restricted to my IP) and port 80 for HTTP (open to anyone).
 
<img src="images/01-security-group-setup.png" alt="Security Group Setup" width="600">
 
<img src="images/02-inbound-rules.png" alt="Inbound Rules" width="600">
 
### Launched the Instance and SSH'd In
 
Spun up a `t2.micro` instance running Amazon Linux 2023, then connected via SSH from Git Bash.
 
<img src="images/03-ssh-and-install.png" alt="SSH and Nginx Install" width="600">
 
### Installed Nginx
 
Ran the install and started the service:
 
```bash
sudo dnf update -y
sudo dnf install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```
 
<img src="images/04-nginx-running.png" alt="Nginx Running" width="600">
 
Hit the public IP in a browser and got the default Nginx welcome page:
 
<img src="images/05-nginx-welcome.png" alt="Nginx Welcome Page" width="600">
 
### Deployed a Custom Page
 
Replaced the default page with a custom HTML page styled with a dark gradient background and a glassmorphism card.
 
<img src="images/07-html-code.png" alt="HTML on the Server" width="600">
 
<img src="images/06-custom-page.png" alt="Custom Page Live" width="600">
 
## What I Learned
 
- How to launch and connect to an EC2 instance via SSH
- Security Groups control what traffic can reach an instance — they're basically cloud firewalls
- `systemctl` manages services on Amazon Linux (start, stop, enable on boot)
- Nginx serves static files out of `/usr/share/nginx/html/` by default
- Public IPs change on stop/start unless you attach an Elastic IP
- Always terminate or stop resources when done to avoid charges
