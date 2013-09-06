Flask MultiConfig
=============

This is the beginning of a somewhat advanced configuration library for Flask
that mainly tries to separate out the logic for environments and modes.

In doing so, it gives the flexibility to specify varying sources of config
data based not only on the environment the app is running, but also the mode
you would like to simulate.

In other-words:

Development-Local would be one combination of settings / config source
Testing-Local is another
Production-Remote is what you want live
Production-Local is a way to ensure production settings have no errors

Check out the implementation if you're more curious than that. Detailed docs
are a long way off until I have more free time.