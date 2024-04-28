import os #directory access
import re #regular expression
import sys #sys.exit()

testPrints = True

listOfAllImageFiles = []
listOfAllImageFilePaths = []

#list of image file types to compare
imgFileTypes = ['.jpg', '.jpeg', '.png', '.pdf']

# Specify the directory path
directory = input("Select directory...")
#/Users/drawmicon/Documents/FanFusion_Comicon


#regular expression check for valid directory
regexMatch = re.compile('^((/[a-zA-Z0-9-_]+)+|/)$')

regexTrue = regexMatch.match(directory)

if(not regexTrue):
    print (directory, " is not a valid directory!")
    sys.exit(1)
else:
    print("Directory found!\n")


#dirExists = os.path.exists(directory)

dirExists = [x[0] for x in os.walk(directory)]

for d in dirExists:
    if not os.path.exists(d):
        print (d, "is NOT a directory")
        exit (1)

print("All directories: ", dirExists)

#Loop through all files in folders
for dirIndex in dirExists:
    if(dirIndex):
        # Open the directory and view its contents
        contents = os.listdir(dirIndex)
        dirSize = len(contents)
        # Print the contents of the directory
        print("Total: ",dirSize, " items:\n")

        #CHECK number of files in all directories, Exclude all folders/directories as items
        #numOfFiles = 0
        #for i in dirExists:
        #    if(not os.path.isdir(i)):
        #        numOfFiles+=1
        #print("Total files: ", numOfFiles)

        #for every file in the directories
        for item in contents:

        #print file/folder name
            if testPrints:
                print(item)

            #check if file is jpg, jpeg, png...
            for fileImgIndex in imgFileTypes:

                #if testPrints:
                 #   print("Checking File Type: ",fileImgIndex)

                #if the file/folder ends with the file type, add to list
                if item.lower().endswith(fileImgIndex):
                    print(item, " is a ", fileImgIndex, "!\n")
                    listOfAllImageFilePaths.append(dirIndex+'/'+item)
                    listOfAllImageFiles.append(item)

                    #rename and move item to duplicate folder

                    #exit for loop
                    break
                else:
                    if testPrints:
                        print("\t","NOT ", fileImgIndex)


    else:
        print (directory, " does NOT exist\n")



if testPrints:
    #print("List of all image files: \n", listOfAllImageFiles, "\n")
    indexer1 = 0
    for filepathz in listOfAllImageFilePaths:
        print("\t", listOfAllImageFiles[indexer1], ": " ,filepathz, "\n")
        indexer1 += 1


#******************************************************************
print ("Duplicates: \n")
seen = set()
duplicates = set()
#Get list of all duplicates by file name and add the file paths of the duplicates to duplicates set
for idx, x in enumerate(listOfAllImageFiles):
    if x in seen:

        if testPrints:
            print(idx, x, "\n\t", listOfAllImageFilePaths[idx]) #print index and element name
            duplicates.add(listOfAllImageFilePaths[idx])
    else:
        seen.add(x)





for d in duplicates:
    source = d

    #file name and path without extension, and the extension separately, e.g. '/path/to/somefile'   ,     '.ext'
    fileNameAndPath, fileExtension = os.path.splitext(d)

    #name of folder file is in e.g. /path/
    fileFolder = os.path.dirname(d)
    #file path without the file name e.g. my/file/path/
    filePathOnly = os.path.dirname(d)
    #file name only e.g. filename.txt
    fileNameOnly = os.path.basename(d)

    dest = fileFolder, fileExtension

    try:
        os.rename(source, dest)
        print("Source path renamed to destination path successfully.")

    # If Source is a file
    # but destination is a directory
    except IsADirectoryError:
        print("Source is a file but destination is a directory.")

    # If source is a directory
    # but destination is a file
    except NotADirectoryError:
        print("Source is a directory but destination is a file.")

    # For permission related errors
    except PermissionError:
        print("Operation not permitted.")

    # For other errors
    except OSError as error:
        print(error)




