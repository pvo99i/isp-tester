# isp-tester
Software for testing Internet Service Provider (ISP_

# How to install

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

# How to run

```
$sudo python start.py --config PATH_TO_CONFIG --user_name MY_USER_NAME --password MY_SUPER_PASSWORD
```
