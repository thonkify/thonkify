## Thonkify GAE Server

### Prerequisites

You will need the [Standard Google App Engine SDK for Python][1].
You may also need `lxml`, `webapp2` and some others, though those should be installed
as dependencies of the App Engine SDK.
For Compatibility on Windows, you cannot use a python version higher
than 2.7.9 without [modification to the google app engine sdk files][2].

### Local development

To develop locally, run the following command from the
root of the project folder (not within src):

    dev_appserver.py src

Some additional properties you might want to add are; `--storage_path=dev_data`
to have a structured path to consistenly get storage set up (and not wiped out with a system reboot),
and `--log_level=debug` to dispaly all debug log messages.
You can also look at [run_localserver](./run_localserver) as a reference.

The src/lib folder holds some pre-selected versions of some libraries
(such as pycountry, oauth2client, simplejson, babel and a few others)

 [1]: https://cloud.google.com/appengine/downloads
 [2]: https://code.google.com/p/googleappengine/issues/detail?id=12783#c7