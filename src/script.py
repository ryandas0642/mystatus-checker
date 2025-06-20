import os
import sys
import subprocess
import platform
import time

# --- BOOTSTRAP LOGIC: Ensure venv and dependencies are set up ---
def in_venv():
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )

def ensure_venv_and_deps():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    venv_dir = os.path.join(project_root, 'venv')
    requirements = os.path.join(script_dir, 'requirements.txt')

    # 1. Create venv if not present
    if not in_venv():
        if not os.path.isdir(venv_dir):
            print('Creating virtual environment...')
            subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
        # 2. Activate venv and re-run script
        print('Activating virtual environment and re-running script...')
        if platform.system() == 'Windows':
            python_bin = os.path.join(venv_dir, 'Scripts', 'python.exe')
        else:
            python_bin = os.path.join(venv_dir, 'bin', 'python')
        # Re-run script in venv
        try:
            os.execv(python_bin, [python_bin] + sys.argv)
        except Exception as e:
            print(f"Failed to re-run script in venv: {e}")
            print("Please activate the virtual environment manually and re-run the script:")
            if platform.system() == 'Windows':
                print(f"  {venv_dir}\\Scripts\\activate")
            else:
                print(f"  source {venv_dir}/bin/activate")
            print(f"  python {os.path.basename(__file__)}")
            sys.exit(1)

    # 3. Install dependencies if needed
    try:
        import selenium  # noqa: F401
    except ImportError:
        print('Installing dependencies...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements])
        # After installing, re-run the script to ensure new deps are loaded
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Run the bootstrapper
ensure_venv_and_deps()

# Now safe to import selenium and other dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- USER CONFIGURATION ---
# USERNAME and PASSWORD will be read from src/user-creds/user_credentials.txt (relative to this script)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(script_dir, 'user-creds', 'user_credentials.txt')
    if not os.path.isfile(creds_path):
        raise FileNotFoundError(f"Could not find user_credentials.txt at {creds_path}")
    with open(creds_path, 'r', encoding='utf-8') as cred_file:
        lines = [line.strip() for line in cred_file if line.strip()]
        if len(lines) < 2:
            raise ValueError("user_credentials.txt must have at least two non-empty lines: first for username, second for password.")
        if ' ' in lines[0]:
            raise ValueError("Username (first line) must not contain spaces.")
        USERNAME = lines[0]
        PASSWORD = lines[1]
except Exception as e:
    msg = f"\nERROR: {str(e)}\n\nCorrect format for user_credentials.txt:\n<username> (no spaces)\n<password> (no spaces)\n\nExample:\nxy12345\nMySecretPassword123\n"
    print(msg)
    sys.exit(1)

# Path to your ChromeDriver executable
system = platform.system()
machine = platform.machine().lower()

if system == "Windows":
    CHROMEDRIVER_PATH = os.path.join("src", "chromedriver-win64.exe")
elif system == "Linux":
    CHROMEDRIVER_PATH = os.path.join("src", "chromedriver-linux64")
elif system == "Darwin":
    if "arm" in machine:
        CHROMEDRIVER_PATH = os.path.join("src", "chromedriver-mac-arm64")
    else:
        CHROMEDRIVER_PATH = os.path.join("src", "chromedriver-mac-x64")
else:
    raise RuntimeError(f"Unsupported OS: {system}")

if system != "Windows":
    chromedriver_binaries = [
        os.path.join("src", "chromedriver-mac-x64"),
        os.path.join("src", "chromedriver-mac-arm64"),
        os.path.join("src", "chromedriver-linux64")
    ]
    for binary in chromedriver_binaries:
        try:
            if os.path.exists(binary) and not os.access(binary, os.X_OK):
                os.chmod(binary, 0o755)
        except Exception as e:
            print(f"Error setting executable permission on {binary}: {e}")
            sys.exit(1)

# --- SCRIPT START ---
START_URL = 'https://admissions.utexas.edu/mystatus/'

# Set up Chrome options (optional: run headless)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # Uncomment to run headless

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    # 1. Go to the MyStatus info page
    driver.get(START_URL)

    # 2. Click the "MyStatus" button (update selector if needed)
    # The button is an <a> element with class 'btn linkLock' and text 'MyStatus'
    mystatus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn') and contains(@class, 'linkLock') and contains(., 'MyStatus')]")))
    mystatus_button.click()

    # 3. Switch to the new tab or window if one opens
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    # 4. Wait for the UT EID login form and enter credentials
    # The username field is labeled 'UT EID', but the input's id is likely 'username' or similar. Let's check for both 'username' and 'IDToken1'.
    try:
        username_input = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    except:
        username_input = wait.until(EC.presence_of_element_located((By.ID, 'IDToken1')))
    username_input.clear()
    username_input.send_keys(USERNAME)

    # Password field: try 'password' or 'IDToken2'
    try:
        password_input = driver.find_element(By.ID, 'password')
    except:
        password_input = driver.find_element(By.ID, 'IDToken2')
    password_input.clear()
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)  # Immediately submit the form after entering password

    # As a fallback, try to click the sign in button if still on the login page
    try:
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SIGN IN')]")), timeout=3)
        sign_in_button.click()
    except:
        try:
            sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and (@value='SIGN IN' or @value='Sign In')]")), timeout=3)
            sign_in_button.click()
        except:
            pass  # If both fail, do nothing (ENTER already sent)

    # 5. Wait for the MyStatus portal to load (wait for a known element, e.g., your name or a dashboard element)
    # Here, just wait for the URL to change to the MyStatus dashboard (contains '/portal/mystatus')
    wait.until(lambda d: '/portal/mystatus' in d.current_url)

    # 6. The MyStatus page should now be displayed for the user
    print("MyStatus page loaded. You may now interact with it.")
    time.sleep(60)  # Give user time to view the page before closing (optional)

finally:
    driver.quit()
