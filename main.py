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

tagFiles = input("Append 'Duplicate' to file names?\n\tEnter true or false")
tagFilename = True

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
        print("Total: ",dirSize, " items in folder:\n")

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
seen = []
seenFilePath = []
duplicates = []
#Get list of all duplicates by file name and add the file paths of the duplicates to duplicates set
for idx, x in enumerate(listOfAllImageFiles):
    if x in seen:

        if testPrints:
            print(idx, x, "\n\t", listOfAllImageFilePaths[idx]) #print index and element name
        duplicates.append(listOfAllImageFilePaths[idx])
    else:
        seen.append(x)
        seenFilePath.append(listOfAllImageFilePaths[idx])

#WRITE THE ORIGINAL FILE PATHS AND DUPLICATES TO TEXT FILES

ogFilepaths = directory + '/OriginalFilepaths.txt'
dupFilepathes = directory + '/DuplicateFilepaths.txt'

with open(ogFilepaths, 'w') as fp:
    for item in listOfAllImageFilePaths:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
fp.close()

with open(dupFilepathes, 'w') as fp:
    for item in duplicates:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
fp.close()


#RENAME ALL DUPLICATES TO THE NAME OF THE FOLDER WHERE THE ORIGINAL IS
for d in duplicates:


    source = d

    #file name and path without extension, and the extension separately, e.g. '/path/to/somefile'   ,     '.ext'
    fileNameAndPath, fileExtension = os.path.splitext(d)

    #file path without the file name e.g. my/file/path/
    filePathOnly = os.path.dirname(d)
    #file name only e.g. filename.txt
    fileNameOnly = os.path.basename(d)

    #file name without extension
    fileNameWithoutExtension = os.path.splitext(os.path.basename(fileNameOnly))[0]

    #name of folder file is in e.g. /path/
    fileFolderOnly = os.path.basename(filePathOnly)


    originalSeenIndex = seen.index(fileNameOnly)
    if testPrints:
        print("File first found in file path ",seenFilePath[originalSeenIndex])

    originalFileFolder = os.path.basename(os.path.dirname(seenFilePath[originalSeenIndex]))

    if testPrints:
        print("Original file folder is ", originalFileFolder)



    if tagFilename:
        dest = filePathOnly +"/"+ originalFileFolder + "_" + fileNameWithoutExtension + "_Duplicate" + fileExtension
    else:
        dest = filePathOnly + "/" + originalFileFolder + "_" + fileNameWithoutExtension  + fileExtension

    print ("New file name for duplicate: ",dest)



    #RENAME ALL DUPLICATES FROM SOURCE TO DEST
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



