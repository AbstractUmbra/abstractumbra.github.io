---
layout: post
title: "SSL Woes on Windows hosts"
date: 2022-06-15 12:00:00 +0100
categories: discord.py
---
First and foremost, you should know that the below fix is *absolutely no longer necessary*.
It was created for a time between this issue occurring and Windows having to release a hotfix in the form of being bundled with "Security updates" for their OSes.

Now, onto what actually happened:-

The issue was announced and disclosed [here](https://support.sectigo.com/Com_KnowledgeDetailPage?Id=kA03l00000117LT).

In essence, the root CA for Sectigo - a company who handles SSL Certificate creation and updates for numerous businesses worldwide - expired. This means that all ssl certificates they issued using this root CA were no longer valid.

Think of it like a company who makes locks, but they use a single device to make random, unique locks for a multitude of doors/cases/windows, and this device is suddenly broken and all these locks no longer work.

After investigating around [I found the location to download their new root CA](https://crt.sh/?id=2835394) before Windows had a chance to release any patch for it.
Other systems were affected much less as the `ca-certificates` repo/package was updated within an hour or so and they just had to update using their package manager (think Linux or MacOS).

The error shown to the end user was *very* similar to this:-
`[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1108)`
There are similar errors from using the ssl module, but note the `certificate has expired` section, as this is key.

As such we began issuing help messages within the discord.py server to download and install this certificate on your local machine.
It is signed, verified and entirely secure - all the details necessary to confirm this yourself are in the download link shown earlier. If you don't understand PKI, it's simple enough to look up what a root CA does and how to verify authenticity. Always question random things people on the internet want you to download!

As previously stated, this is no longer necessary at all. If you're having SSL errors on Windows still, try the usual things:-

- Check system time is accurate (alternatively use a good NTP solution like Google)
- Check the `certifi` Python package is installed on your system and up to date.
- Open the url you're trying to access in a browser to view a more verbose error.
