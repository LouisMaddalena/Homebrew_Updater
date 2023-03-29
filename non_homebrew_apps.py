import os
import subprocess
import argparse
import shutil

def get_applications_folder_contents():
    applications_path = '/Applications'
    return [app for app in os.listdir(applications_path) if app.endswith('.app')]

def get_homebrew_installed_apps():
    result = subprocess.run(['brew', 'list', '--cask'], capture_output=True, text=True)
    return result.stdout.splitlines()

def search_cask(app_name):
    result = subprocess.run(['brew', 'search', '--casks', app_name], capture_output=True, text=True)
    return result.stdout.splitlines()

def install_cask(cask_name):
    subprocess.run(['brew', 'reinstall', '--cask', cask_name])

def backup_application(app):
    backup_folder = os.path.expanduser('~/Desktop/Applications Backup')
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    app_path = f'/Applications/{app}'
    backup_path = f'{backup_folder}/{app}'
    shutil.move(app_path, backup_path)


def main(args):
    applications = set(get_applications_folder_contents())
    homebrew_apps = set(get_homebrew_installed_apps())

    non_homebrew_apps = applications - homebrew_apps

    if args.check_available:
        print('The following applications are not installed with Homebrew but have a Homebrew Cask available:')
        for app in sorted(non_homebrew_apps):
            app_name = app[:-4]  # Remove the '.app' extension
            matching_casks = search_cask(app_name)
            if matching_casks:
                print(f' - {app} (Cask: {", ".join(matching_casks)})')
    elif args.replace:
        for app in sorted(non_homebrew_apps):
            app_name = app[:-4]  # Remove the '.app' extension
            matching_casks = search_cask(app_name)
            if matching_casks:
                primary_cask = matching_casks[0]
                print(f'Backing up and removing {app}, then installing with Homebrew Cask: {primary_cask}')
                app_path = f'/Applications/{app}'
                try:
                    backup_application(app)  # Add this line to back up the application
                    install_cask(primary_cask)
                except Exception as e:
                    print(f'Failed to remove and replace {app}: {e}')
            else:
                print(f'{app} does not have a matching Homebrew Cask. Skipping.')

    else:
        print('The following applications were not installed with Homebrew:')
        for app in sorted(non_homebrew_apps):
            print(f' - {app}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check which applications were not installed with Homebrew. Provide option to replace applications with homebrew formulae for eaiser updating. ')
    parser.add_argument('--check-available', action='store_true',
                        help='Check which applications are not installed via Homebrew but have a Homebrew Cask available.')
    parser.add_argument('--replace', action='store_true',
                        help='Remove any apps in the Applications folder that are not installed via Homebrew and install them via Homebrew if available.')
    args = parser.parse_args()
    main(args)
