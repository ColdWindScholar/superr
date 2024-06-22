# **SuperR's Kitchen**
## *by SuperR*

## **FEATURES**

**Extract and create ROM from:**

* Rooted Device  
* Custom Recovery  
* Existing ROM zip  
* system.img/boot.img (and cache.img on Samsung devices)  
* system.ext4.tar/boot.img  
* system.ext4.win/boot.emmc.win (including multi-file .win000, .win001, etc)  
* Moto and other factory firmware zips containing sparsechunk files  
* Zips that contain dat files  
* Zips that contain system.img and boot.img  
* Samsung firmware zips that contain tar.md5 file  
* Official Pixel/Nexus firmware tgz/zip  
* Official Pixel/Nexus preview tgz/zip  
* SpreadTrum fimware that contains pac files  
* system directory that contains symlinks and boot.img  

**Create flashable zips of many varieties including:**

* Full ROM  
* Switch between set_perm (JellyBean-), set_metadata (KitKat+), raw_img, and sparse_dat (Lollipop+)
* boot.img  
* recovery.img  
* Media  
* app, priv-app, and framework, lib  

**Deodex the following:**  

* Pie ROMs  
* Oreo ROMs  
* Nougat ROMs  
* Marshmallow ROMs  
* Lollipop ROMs  
* KitKat and earlier ROMs  

**Root features:**  

* Root/unroot  
* Choose Magisk (add other versions to /tools/root/root_zips directory)  
* Choose SuperSU (add other versions to /tools/root/root_zips directory)  
* Choose system OR systemless root for M+ and Samsung 5.1.1 roms when using SuperSU  
* Add/remove su.d support  

**Boot features:**

* Unpack/repack boot/recovery img (Big Thanks to @osm0sis for Android Image Kitchen!!!)  
* Add/remove insecure boot  
* Remove dm-verity  
* Remove forceencrypt  
* Patch sepolicy for Oreo deodex

**By-name auto-detection from:**

* Device  
* Existing ROM  
* boot.img  
* kernel.elf  
* **OR**...manually enter it  

**mmcblk auto-detection from:**

* recovery.img  

**Kitchen updater:**

* View the last 3 changelogs when an update is available.  
* Update to the latest version  
* Option to check for updates when the kitchen starts  

**Create system.img**  
**Device database for mmcblk devices (currently very small, but will grow over time)**  
**Add devices to the assert**  
**Add custom asserts**  
**Zipalign apks**  
**Debloat ROM**  
**Custom Debloat list**  
**Remove Knox**  
**Add/remove busybox (Big thanks to @osm0sis for his Busybox Installer)**  
**Add/remove user app (/data/app)**  
**Sign zips**  

**Donate version additional features:**

* Cross-platform: Windows, Linux, and Mac are fully supported
* Does not say Built with SuperR's Kitchen in the updater-script  
* Does not replace ro.build.display.id with Built.with.SuperRs.Kitchen  
* Allows you to create a custom entry in the updater-script below the ROM name  
* Removes all the Place holders (#ASSERT, #SYM, #PERM, etc) from the updater-script before zipping.  
* Custom ro.build.display.id  
* Option to convert updater-script to update-binary for all rom zips EXCEPT sparse_dat.  
* Add custom directory to be included in and flashed with rom zip to location of your choice.  
* Ability to choose an apk, decompile, modify it manually, recompile, sign, and move it back to where it came from.  
* Plugin support - Many additional features for specific devices/manufaturers. You can also add your own script to the /kitchen/tools/plugins directory and the kitchen will run it for you.  
* AutoROM - Unattended ROM development using a config file.  
* Create 1:1 system.img with regard to file permissions, capabilities, and contexts.  

## **DEPENDENCIES:**

* Java 8 or higher (and in your PATH if running Windows)

## **USAGE:**

## **Linux/Mac (Terminal):**  

1. Run "superr" from it's location in terminal  
2. Create new project using the menu  
3. Copy ROM zip into the superr_NAME directory of this tool (NAME = the name of your new project).  
   **OR**  
   Copy system.ext4.tar and boot.img into the superr_NAME directory of this tool.  
   **OR**  
   Copy system.ext4.win and boot.emmc.win into the superr_NAME directory of this tool.  
   **OR**  
   Copy system.img and boot.img into the superr_NAME directory of this tool.  
   **OR**  
   Copy official Nexus tgz into the superr_NAME directory of this tool.  
   **OR**  
   Copy Samsung firmware zip into the superr_NAME directory of this tool.  
   **OR**  
   Copy SpreadTrum zip into the superr_NAME directory of this tool.  
   **OR**  
   Copy Moto firmware zip into the superr_NAME directory of this tool.  
   **OR**  
   Leave superr_NAME directory empty to extract from rooted device or custom recovery  
4. Extract for new ROM from the Main menu.  
5. Enjoy!  

**EXAMPLE:**

In your shell, type the following where "/location/of/kitchen" is the directory where the kitchen lives:

```
cd /location/of/kitchen
./superr
```

**OR**

Double-click the superr file and choose "Run in Terminal" if your OS supports it.  

## **Windows:**
```
Double-click superr.exe in the main kitchen directory
```

