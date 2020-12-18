# tinyserv

tinyserv is a relatively simple HTTP server written in python to transfer files
to and from computers on a local network.

The feature roadmap is the following:
- [x] Sortable columns
- [x] Optional `index.html`/`index.htm` serving
- [x] Hidden file listing
- [ ] File upload
- [x] Directory/multiple file downloads
- [x] QR code for connecting (plus reminder of IP in text form)
- [ ] Download resume

It's in no way secure (HTTP only at the moment, probably a lot of ways to break
things), as it shouldn't be run "for a long duration".

tinyserv is licensed under the GPLv3 license.
