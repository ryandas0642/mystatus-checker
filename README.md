# UT MyStatus Auto-Checker

## Due to popular demand - the solution to all your MyStatus woes is here! This project automatically checks MyStatus for you - no need to type your credentials (apart from the initial set up). Simply follow the steps below and enjoy the convenience - absolutely no technical background is needed whatsoever. 

# Warning: The bottom of this README.md file contains an important security note. Please read this README.md file in its entirety.

# Installing The Project
1. **Installation:**
    - Click on the Green Code Button and select the `Download ZIP` option.
    - Unless you really know what you're doing, I would recommend the project to be installed within the default downloads folder on your platform.
    - Extract the ZIP folder.



# Initial Set-Up

1. **Check your chrome version:**
    - Open a newtab in Google Chrome and type the following: `chrome:version`
    - At the top of the page make sure the chrome version starts with `137`.
    - If that is not the case, update your chrome browser to version `137`. Simply search for `how to update chrome` and then repeat the exercise above. Make sure the version number at the top of the page starts with `137`.

2. **Install Python, add to PATH and ensure PIP is installed**
    - If you do not already have python, do a google search on how to install the latest version of python and add it to PATH. 
    - While you are setting that up make sure you have `pip` installed. Latest versions of python come with `pip` but, if for some reason, you are missing `pip`, please install `pip`.


3. **Update your credentials:**
   - Click on the mystatus-checker-main folder.
   - Navigate to the src folder.
   - Within the src folder, locate and click on the user-creds folder; then find user_credentials.txt file.
   - Enter your username on the first line and your password on the second line. Please ensure that there are no stray spaces or extra lines.
   - Example:
     ```
     xyz12345
     your_password
     ```

# Actually Running The Project


1. **Run the script:**
   - Find the mystatus-checker-main folder. Make sure it's not installed in a protected folder like `C:\Program Files\` or `/usr/local`. As previously mentioned, it is recommended to install this project in the default downloads folder on your platform. 
   - Right click on the folder from the the downloads folder on your platform and click the "open in terminal" option. 
   - Run the following commands:
   ```
   cd mystatus-checker-main/src
   python script.py
   ```
   - The script will automatically set up everything (virtual environment, dependencies) on first run.
   - On subsequent runs, simply repeat this step from the downloads folder.


---

# What Happens Next?
- The script will:
  - Create a virtual environment 
  - Install required dependencies 
  - Launch Chrome and automatically log in to the UT MyStatus portal using your credentials on your behalf.

# Requirements
- Python 3.7 or newer must be installed and available in your PATH.
- Google Chrome browser installed. Version 137 is needed.
- ChromeDriver is included in the `src` folder. If you update Chrome, you may need to update ChromeDriver as well.

# Troubleshooting
- **Python not found?**
  - Download and install Python from [python.org](https://www.python.org/downloads/).
- **Permission errors?**
  - Make sure you have write access to the project folder.
- **ChromeDriver version mismatch?**
  - Download the version 137 from [ChromeDriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/) and replace add the new driver in `src`. Do not delete any of the existing installations - the script will automatically deduce your platform architecture and select the appropriate driver.
- **Other issues?**
  - Copy any error message and reach out to me at `ryan.das.0642@gmail.com`.

---

# Security Note
- Your credentials are stored in plain text in `user_credentials.txt`. Keep this file private and do not share it. Under no circumstances should this project leave your local machine.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---