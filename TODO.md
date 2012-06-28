# v1 plans:

## Overview

There will be three main components: API, Web interface, and clients.  Clients for v1 will consist of browsers running bookmarklets.



## Infrastructure

Simple API server to store:

* Users.  For auth, possibly optional.
* Locations.  Individual browsers, can be multiple per device.
* Pages.  URLs (possibly other data) of pages sent between browsers.

v1 will only involve bookmarklets for client interaction.  Primary use case is sending a Page from an iOS/Android device and retrieving it from a desktop/laptop.

Pages can be sent to specific Locations (these Pages would only be accessible by that Location), or possibly/optionally to a "global" @pool Location (accessible by all Locations).  v1 may only have the @pool option, for simplicity of implementation.

### Security

Security should be a high priority.  Imagine if a live-load browser extension were developed (ie, the browser can load pages instantly when they enter its Page pool) and a malicious third party were to gain Page-sending access to your account.  Insta-tab-spam!

Bcrypt, a la [django-bcrypt](https://github.com/dwaiter/django-bcrypt/), will be used for user authentication via the web interface.

Client authentication will be in the form of public/private API keys, probably per-Location.

### Web interface

The API server will have a normal, minimal web frontend integrated for account management via a browser.

#### Functionality

* Manage User
    * Change Password
    * Manage @pool global Page pool
* Manage Locations
    * Add/Remove Locations
    * Rotate keys
    * Manage a location's Page pool
        * Add/Remove Pages



## Technology

### API

#### Python

The API server will need to be fairly easily self-hosted, while maintaining some dignity (ie, NOT PHP).  It will be built using Python.  Aiming for WSGI running on gunicorn/nginx (better/faster) or Apache/mod_wsgi (easier).

#### Framework

Django has a lot of good, appealing tools (database management, forms framework, etc), but involves a lot of work and know-how to deploy, in general.

Microframeworks such as djng (which I tried and liked a bit, but is limited), itty, mnml, etc are generally appealing, but mostly lack community support, maturity, and active development.  And those three specific frameworks each had problems that made them unsuitable for real use (or this use, anyway).

Flask seems the most suitable choice.

#### Persistence

Redis could serve as a suitable persistence engine, but there is concern regarding the permanence of its storage (eg, it forcibly expires keys when it reaches its memory limit).  Pluggable persistence backends a la Django would be ideal, but v1 will likely be redis-specific.

### Web interface

@twitter bootstrap will be used to get a nice-looking, minimal v1 interface.  We have the tools, let's use them.

### Clients

Clients for v1 will consist of bookmarklets, thus written in JavaScript.  Ideally, the same code will work across all browsers, but some specific code may need to be written for specific browses -- eg, one version for mobile devices that uses simple confirmation dialogs, select elements, and other widget behavior vs. another version for desktop browsers that behaves more like a pop-in window.

Hmac-sha256 authentication, described bellow, can be implemented client-side using the scripts at the following urls:

* [JS SHA256](http://antimatter15.com/wp/2010/01/javascript-sha1-and-sha256-in-1-kb/)
* [JS HMAC](http://code.google.com/p/crypto-js/source/browse/tags/3.0.2/src/hmac.js)

Care will have to be taken in bookmarklet authoring to avoid overrunning any "maximum address length" limitations imposed by browsers.

Ideally, the bookmarklet itself will only contain authentication data (public/private keys) and a way to load a script from the API/Web server.  This would greatly reduce the time cost of upgrading the client script (update it server-side, all clients are insta-updated), and reduce the size of the bookmarklet itself.  The only concern is how to get the keys from the bookmarklet to the external script without leaking them to the current page (any "current page" could contain malicious spy code to sneak a peek at your keys >:D ).



## Authentication

Each location will have its own public/private key pair.  This will ease the process of rotating keys in the event of a malicious third party gaining account access via a Location.  Instead of user-level API keys, which would require updating the bookmarklet on each Location, a single set of keys would be rotated, and only the breached Location would have to be updated with the new keys.

v1 API server will support HTTP Basic authentication.  Values used for the "username" and "password" parts have not been decided yet (may be public-key:user-password, public-key:private-key, or something else; it's all base64-decodable, though, which makes it very insecure over HTTP [really only suitable for HTTPS])

Preferrably, hmac-sha256 authentication will be implemented, following the guidelines (optional included) described at [Designing a Secure REST (Web) API without OAuth](http://www.thebuzzmedia.com/designing-a-secure-rest-api-without-oauth-authentication/):

* Given a hash of key:value parameters to be sent:
* Add a parameter "key" with value set to your public key.
* Add a parameter "timestamp" with value set to an integer, current UNIX timestamp with millisecond resolution.
* Order parameters alphabetically; order parameters with multiple values alphabetically by value.
* Combine ordered parameters into a standard urlencoded querystring; parameter-value pairs joined with '=' and separated by '&', with no leading or trailing '&'.
* Prepend this querystring with the target API endpoint path (leading slash, no trailing slash, all-lowercase).
* Prepend the result with the HTTP method/verb (all-uppercase).
* The final result string should be of the format '<HTTPMETHOD></api/path><parameters>'
* Take the hmac-sha256 hash of this string, using your private key
* Add a parameter "hash" with value set to the hexadecimal representation of the hmac-sha256 hash (all-lowercase, no punctuation)
* Send all parameters to the API server.
