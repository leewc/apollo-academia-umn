#include <stdio.h>
#include <errno.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h> //needed for getpwuid
#include <pwd.h> //needed for getting UID
#include <grp.h> //needed for getting group name
#include <time.h> //for time stamps
#include <string.h>
#include <dirent.h>
#include <unistd.h>

/* This is a (very) simple implementatiom of ls -l in C.
    Adapted and improved from Aditya Sarawgi's older, OSX only implementation: 
        https://github.com/truncs/ls-implementation/blob/master/ls.c
 */

void displayFiles(DIR *d);
void displayInfo(char* name);

static const char * months[] 
    = {"Jan", "Feb", "Mar", "Apr", "May", "Jun" \
        "Jul","Aug", "Sep", "Oct", "Nov", "Dec"};

int main(int argc, char** argv)
{
    DIR *directory;
    char buffer[256]; //max file name length does not exceed 255
    if(argc < 2)
    {
        //User did not supply which directory, use current directory
        directory = opendir(".");
        displayFiles(directory);
        return 0;
    }
    
    //Use supplied directory and fetch all files.
    //declare a struct of type stat for current file/dir
    int i = 1; //start at 1 since 0 is the executable
    struct stat current; 
    while(argc > 1)
    {
        if((stat(argv[i], &current) != 0 ))
            perror("Error could not stat file/folder.");
        
        if(S_ISDIR(current.st_mode)) //check file st_mode
        {
            /*current item is a directory. chdir into it and displayFiles then return */
            printf("%s\n", argv[i]);
            
            if(getcwd(buffer, 256) == NULL)
                perror("Could not get directory.");
            if(chdir(argv[i]) != 0)
                perror("Could not chdir into directory.");
            
            directory = opendir("."); 
            displayFiles(directory);
            chdir(buffer); //change back to previous directory
        }
        else 
            //regular file, display contents. 
            displayInfo(argv[i]);
        
        argc--;
    }
    closedir(directory);
    return 0;
}

/* Function that displays the list of files in the directory, and file info */
void displayFiles(DIR *d)
{
    //declare a ptr to a struct of type dirent (returned by readdir) 
    struct dirent *item;
    while((item = readdir(d)) != NULL)
    {
        //d_name is a 256 char array that holds the filename
        //entry returned by readdir is the next dir entry in a stream by dirp (see man 3 readdir)
        displayInfo(item->d_name); 
    }
}

/* Helper funcion that displays information about the file from stat*/
void displayInfo(char *name)
{
    struct stat s;
    
    if(stat(name, &s) != 0)
        perror("Error could not stat file.");
    
    //Find if we are fifo, link, dir
    if(S_ISDIR(s.st_mode))
        printf("d");
    else if(S_ISFIFO(s.st_mode))
        printf("p");
    else if (S_ISLNK(s.st_mode))
        printf("l");
    else
        printf("-");

	
    /*  Print all permissions using bits.
        Wanted to use switch cases but files can have multiple modes, so that will not work.
        We perform bitwise AND on st_mode with the mask, if it equals 1 means it that type.
        multiple if's since a file/dir can have 2 types, this was too lengthy, switched to one line if-else
    */
	printf("%c", (S_IRUSR & s.st_mode) ? 'r' : '-');
	printf("%c", (S_IWUSR & s.st_mode) ? 'w' : '-');
	printf("%c", (S_IXUSR & s.st_mode) ? 'x' : '-');
	printf("%c", (S_IRGRP & s.st_mode) ? 'r' : '-');
	printf("%c", (S_IWGRP & s.st_mode) ? 'w' : '-');
	printf("%c", (S_IXGRP & s.st_mode) ? 'x' : '-');
	printf("%c", (S_IROTH & s.st_mode) ? 'r' : '-');
	printf("%c", (S_IWOTH & s.st_mode ) ? 'w' : '-');
	printf("%c ", (S_IXOTH & s.st_mode) ? 'x' : '-');
	
	//print number of links
    printf("%ld ", (long) s.st_nlink);

    //print name of uid    
    struct passwd *pwd = getpwuid(s.st_uid);
    printf("%8s ", pwd->pw_name);
    
    //print name of grid
    struct group *grid = getgrgid(s.st_gid);
	printf("%8s ", grid->gr_name);

    //print size, 5.0 aligns right by 5 chars    
	printf("%5.0lu ", s.st_size);
    
    //print time
    struct tm *filetime;
    filetime = localtime(&s.st_ctime);

    printf("%s ", months[filetime->tm_mon -1]);
	printf("%02d %02d:%02d ", filetime->tm_mday, filetime->tm_hour, filetime->tm_min);
    
    //finally print the name
    printf("%s\n", name);

}