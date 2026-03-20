---
name: http-api-generator
description: from webpage give by url, auto generate information need by uapi package
---

# http-api-generator

grabs api description from provider's webpage, and build uapi module api data

## rule
all the data in output will convert by jinja2 engine, 
so in output we need follow the jinja2 rule to 
## usage
input:
{
	"url": provider's url to the API
}

output:
{
	"baseurl":		# base url for api
	"path":			# path for the api
	"headers"		# yaml str for header
```

