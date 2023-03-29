# Homebrew_Updater
I wanted an application to keep all my mac apps updated. I didn’t want to pay $15, and I already used homebrew for most of my apps.  So I wasted a few hours on this. Way more than $15 worth of time. but hey, here it is. 

The script will check to see which applications have been installed on your machine using homebrew

It will also check to see which applications are on your machine and compare these two lists. 

Of the applications installed on your machine but not installed with Homebrew, it will check to see which ones have homebrew casks available.  

Running the script with --replace as an argument will move the applications that have casks but are not using them to your desktop in a back up folder, and then install them via homebrew.  

Then you can update/upgrade your homebrew as you usually do. (will make an --upgrade and --update option in the near future)


For a list of command line arguments, as always run the script with the -h tag. 
