from browser_monitor import BrowserProcessMonitor


def main():
    # Create an instance of BrowserProcessMonitor
    browser_monitor = BrowserProcessMonitor()

    # Get the running browsers
    default_browser = browser_monitor.get_default_browser_name()
    print(f'Default browser: {default_browser}')


if __name__ == '__main__':
    main()
