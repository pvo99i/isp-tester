# isp-tester
Software for testing Internet Service Provider (ISP_

# How to install with mac-ports

1. Install python38
```
$ sudo port install python38
$ sudo port select --set python3 python38
```

2. install pip3
```
$ sudo port install py38-pip
```

3. install requests package
```
$ sudo pip-3.8 install requests --trusted-host  pypi.org  --trusted-host files.pythonhosted.org
```

# How to install with home-brew (Optional due tools can be already installed)
1. Install Apple Command Line Tools
```
xcode-select --install
```
2. Install python-3.8
```
$ brew install python@3.8
$ echo 'export PATH="/usr/local/opt/python@3.8/bin:$PATH"' >> ~/.bash_profile
$ source ~/.bash_profile
```
3. Install requests package
```
$ pip3 install requests --trusted-host  pypi.org  --trusted-host files.pythonhosted.org
```
# How to run

```
$ sudo python3.8 start.py --config PATH_TO_CONFIG --user_name MY_USER_NAME --password MY_SUPER_PASSWORD
```
