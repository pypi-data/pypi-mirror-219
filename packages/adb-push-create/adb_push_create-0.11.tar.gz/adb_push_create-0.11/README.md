# creates [nested] folders and pushes files with ADB

## Tested against Windows 10 / Python 3.10 / Anaconda 

### pip install adb-push-create

```python
from adb_push_create import push_file,make_folders
adb_path = r"C:\ProgramData\chocolatey\bin\adb.exe"
deviceserial = "xxxx"
make_folders(adb_path, deviceserial,path2create='/sdcard/DCIM/0/12/4')
copyok = push_file(
    adb_path=adb_path,
    deviceserial=deviceserial,
    file=r"C:\xdf - Copy.m4v",
    dest="/sdcard/DCIM/0/12/4/12/4/5", # path does not exist yet
)
print(copyok)
True
```

Contribution
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.

License
This project is licensed under the MIT License.