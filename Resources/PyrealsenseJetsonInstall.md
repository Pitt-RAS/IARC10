*Because this is a pain in the ass*
[the video that I got this from](https://www.youtube.com/watch?v=xqroBkpf3lY)
# The Install Process
First, you are going to want to clone this repository
`git clone https://github.com/JetsonHacksNano/installLibrealsense.git`

While it does say there is an install script (`installLibrealsense.sh`), I had issues getting it to work (so it either just doesn't work at all or there's just a skill issue on my part)

Instead, we're going to build it using `buildLibrealsense.sh` because that's how I actually managed to get it working. But first, we're going to have to modify this script a little before it actually works. So `cd` into the `installLibrealsense` directory and edit `buildLibrealsense.sh` using whatever editor you want.
Scroll down until you see the line that starts with (should be line ~135)
```bash
/usr/bin/cmake ../ -DBUILD_EXAMPLES=true -DFORCE_LIBUVC=ON -DBUILD_WITH_CUDA="SUSE_CUDA" # the rest of the line goes on for a while
```
At the end, add the following, separated by a space:
```bash
-DPYTHON_EXECUTABLE=$(which python3)
```
save the script and exit. Now run the script
```bash
./buildLibrealsense.sh -j 2
```
Hopefully, everything will build without issues

Now, the actual library will be installed, but we can't import it yet because it built into a directory that isn't our python path
To remedy this `cd ~` to get to your home folder and edit `.bashrc` with your editor of choice. Towards the bottom, there should be a line that says the following:
```bash
export PYTHONPATH=$PYTHONPATH:/usr/local/lib
```
Change it to say the following:
```bash
export PYTHONPATH=$PYTHONPATH:/usr/local/OFF
```
Now just execute `source ~/.bashrc` to execute the changes made to `.bashrc` The library should now be working

Double check that it's actually working by running
```shell
python3
```
and then seeing if the library will import without issues
```python
>>> import pyrealsense2 as rs
```
Hopefully there should be no errors
