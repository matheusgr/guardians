#include <stdio.h>
#include <string.h>
#include <pwd.h>

#define EXPECT_ID 1000

/* Main program. */
int main ( int argc, char *argv[] )
{
  FILE *f;

  char user[50];
  char filename[100];

  struct passwd *pd;
  
  int i, args;

  args = argc;
  user[0] = '\0';
  filename[0] = '\0';
  if (argc < 3) {
    return 1; // Expecting user and emails
  }
  if (getuid() != EXPECT_ID) {
    return 2; // Security error!
  }

  strncpy(user, argv[1], 49);
  
  pd = getpwnam(user);

  setgid(pd->pw_gid);
  setuid(pd->pw_uid);

  user[49] = '\0';
  strcpy(filename, "/home/");
  strcat(filename, user);
  strcat(filename, "/.forward");
  
  f = fopen(filename, "w");
  
  for (i = 2; i < args; i++) {
    fprintf(f, "%s\n", argv[i]);
  }
  
  fclose(f);
}
