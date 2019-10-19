<div align="center" id="topOfReadme">
	<h1>EOS | Helios</h1>
	<em>Interact with EOS database</em></br>


<a href="https://github.com/eos-sns/helios/pulls"><img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"></a> <a href="https://github.com/eos-sns/helios/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a> <a href="https://www.python.org/download/releases/3.6.0/"><img src="https://img.shields.io/badge/Python-3.6-blue.svg"></a> <a href="https://saythanks.io/to/sirfoga"><img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg" alt="Say Thanks!" /></a>
</div>


## Use case
Reads and searches EOS database.


## Example
```python
helios = Helios()
query = helios.builder() \
    .with_p0_as(MongoFilters.LESS_THAN, 11) \
    .with_p1_as(MongoFilters.GREATER_THAN, 1) \
    .build()
results = query.execute()
print(results)  # mmmh, not exaclty what I wanted, let's refine

results = results \
    .filter_by({'p0': {'>=': 2}}) \
    .filter_by('p0 > 1 and p2 <= 9')
print(results)  # yess, now let's save and download

results = results.get()  # get raw
disk_path = helios.save_to_disk(results)  # saved in home folder
download_url = helios.download(results)  # now let's download
```


## Install
```bash
$ pip install .
```


### Upgrade
```bash
$ pip install . --upgrade --force-reinstall
```


## Contributing
[Fork](https://github.com/eos-sns/helios/fork) | Patch | Push | [Pull request](https://github.com/eos-sns/helios/pulls)

## Feedback
Suggestions and improvements are [welcome](https://github.com/eos-sns/helios/issues)!


## Authors

| [![sirfoga](https://avatars0.githubusercontent.com/u/14162628?s=128&v=4)](https://github.com/sirfoga "Follow @sirfoga on Github") |
|---|
| [Stefano Fogarollo](https://sirfoga.github.io) |


## License
All of the codebases are **[MIT licensed](https://opensource.org/licenses/MIT)** unless otherwise specified.

**[Back to top](#topOfReadme)**
