# abbapi

This project is used to provide an api for ABB and related hardware used by WWD.<br>
* Python requirements found in the requirements.txt file.
* Environment variable: DATAFILE is needed to specify where the data.json file resides.  

This data file is expected to be in the form:
<pre>
{ "sites": [
    {
      "name": "wtp",
      "hmi": {
        "url": "https://red.api.wwddata.com/wtp/",
        "address": "http://192.168.2.123",
        "urlname": "5 Points WTP"
      },
      "abb": {
        "url": "https://.api.wwddata.com/",
        "address": "http://192.168.3.123",
        "urlname": "wtp"
      }
    },
    { ... site 2 ... },
    { ... site 3 ... }
]}
</pre>
