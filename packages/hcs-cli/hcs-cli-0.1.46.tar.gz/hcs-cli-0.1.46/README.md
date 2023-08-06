# horizon-cloud-service-cli

[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/vmware-labs/compliance-dashboard-for-kubernetes/blob/main/LICENSE)

## Overview
Command line toolbox for [VMware Horizon Cloud Service (HCS) Next-Gen](https://www.vmware.com/products/horizon-cloud.html). It provides human-friendly operations based on HCS REST API.

## Try it out


### Prerequisites
* Python 3.10+
* Pip3

Refer to [Setup Prerequisites](doc/dev-setup.md#setup-prerequisites) for more details.

### Use the published version on PyPI

#### Mac & Linux

Install the tool
```
pip3 install hcs-cli
```
Use with default public HCS service. 
```
hcs login
```
Run a command, for example, list templates:
```
hcs admin template list
```

## Authentication Methods

For the first time with each profile, it needs authentication.
There are three ways to authenticate:

| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
| hcs login                              | Login with configured credentials, otherwise do an interactive login using browser. |
| hcs login --api-token \<csp-api-token\> | Login with CSP API token. Reference: [Get CSP User API Token](doc/get-csp-user-api-token.md). |
| hcs login --client-id \<client-id\> --client-secret \<client-secret\> [--org \<org-id\>] | Login with OAuth client id/secret. |

To get the current authentication information:
```
hcs login -d
```

## Working with Development Environments
To work with development environments, first create default profiles:
```
hcs profile init --dev
```
Switch between profiles:
```
hcs profile use
```


## Documentation

* [HCS CLI Cheatsheet](doc/hcs-cli-cheatsheet.md)

* [Development Setup](doc/dev-setup.md)

* Based on [Context Programming](https://github.com/nanw1103/context-programming)

  
## Contributing

The horizon-cloud-service-cli project team welcomes contributions from the community. Before you start working with horizon-cloud-service-cli, please read and sign our Contributor License Agreement [CLA](https://cla.vmware.com/cla/1/preview). If you wish to contribute code and you have not signed our CLA, our bot will prompt you to do so when you open a Pull Request. For any questions about the CLA process, please refer to our [FAQ]([https://cla.vmware.com/faq](https://cla.vmware.com/faq)).

## License

Apache 2.0


