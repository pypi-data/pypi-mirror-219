import re
import subprocess

startupinfo = subprocess.STARTUPINFO()
creationflags = 0 | subprocess.CREATE_NO_WINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def make_folders(adb_path: str, deviceserial: str, path2create: str):
    r"""
    Creates folders on an Android device using the Android Debug Bridge (ADB) tool.

    Args:
        adb_path (str): The path to the ADB executable.
        deviceserial (str): The serial number of the connected Android device.
        path2create (str): The path of the folder to be created on the device.

    Returns:
        bool: True if the folders are created successfully, False otherwise.
    """

    # The function first removes any quotation marks or apostrophes from the adb_path string.
    # It then splits the path2create string using the regular expression r"[\\/]+" to handle different path separators (backslash or forward slash) and remove empty elements.
    # The function iterates over the non-empty path components and constructs the complete path by appending each component.
    # For each path component, it executes the ADB command adb_path -s deviceserial shell mkdir "path" using the subprocess.run function. This creates the corresponding directory on the Android device.
    # If any error occurs during the execution of the ADB command (indicated by non-empty proc.stderr), it prints the error message and breaks out of the loop.
    # If the loop completes successfully (no errors occurred), the function returns True.
    # If an error occurred during the loop execution, the function returns False.

    adb_path_ = adb_path.strip("\" '")
    path = "/"
    for p in [q for q in re.split(r"[\\/]+", path2create) if q]:
        path = path + p + "/"

        proc = subprocess.run(
            f'"{adb_path_}" -s {deviceserial} shell mkdir "{path}"',
            capture_output=True,
            **invisibledict,
            shell=False,
        )
        print(f"Creating: {path}", end="\r")
        # if proc.stderr:
        #     print(proc.stderr)
        #     break



def push_file(adb_path: str, deviceserial: str, file: str, dest: str):
    r"""
    Copies a file from the local machine to an Android device using the Android Debug Bridge (ADB) tool.

    Args:
        adb_path (str): The path to the ADB executable.
        deviceserial (str): The serial number of the connected Android device.
        file (str): The path of the file to be pushed.
        dest (str): The destination path on the Android device.

    Returns:
        bool: True if the file is copied successfully, False otherwise.
    """

    # The function first removes any quotation marks or apostrophes from the adb_path, file, and dest strings.
    # It calls the make_folders function to create the necessary folders on the Android device for the destination path. If the folder creation fails, the function returns False.
    # If the folder creation is successful, it executes the ADB command adb_path -s deviceserial push "file" "dest" using subprocess.run to copy the file to the Android device.
    # If any error occurs during the execution of the ADB command, it prints the error message and returns False.
    # If the file copy is successful, the function returns True.
    adb_path_ = adb_path.strip("\" '")
    file = file.strip("\" '")
    dest = dest.strip("\" '")
    make_folders(adb_path, deviceserial, dest)
    proc = subprocess.run(
        f'"{adb_path_}" -s {deviceserial} push "{file}" "{dest}"',
        capture_output=True,
        **invisibledict,
        shell=False,
    )
    print(f"Copying: {file}", end="\r")
    if proc.stderr:
        print(proc.stderr)
        return False
    return True
