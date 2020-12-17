# tinyserv

tinyserv is a relatively simple HTTP server written in python to transfer files
to and from computers on a local network.

The feature roadmap is the following:
- [ ] Sortable columns
- [x] Optional `index.html`/`index.htm` serving
- [x] Hidden file listing
- [ ] File upload
- [ ] Directory/multiple file downloads
- [ ] QR code for connecting (plus reminder of IP in text form)

As you can clearly see not much (nothing) is implemented right now.

It's in no way secure (HTTP only at the moment, probably a lot of ways to break
things), as it shouldn't be run "for a long duration".

tinyserv is licensed under the GPLv3 license.
