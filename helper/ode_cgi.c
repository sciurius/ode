/* ode_cgi.c -- Run ode.cgi as me */

/* By running ode 'as me' problems with file access can be avoided.
 *
 * Compile this program and install it setugid as ode-xxx.cgi.
 * Do not forget to adjust the ode_config and .htaccess if necessary.
 */

#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

main( argc, argv, envp )
int argc;
char *argv[];
char *envp[];
{
  char *p = strrchr( argv[0], '/' );
  strcpy( p+1, "ode.cgi" );
  setreuid( geteuid(), geteuid() );
  setregid( getegid(), getegid() );

  if (execve( argv[0], argv, envp ) == -1 ) {
    perror(argv[0]) ;
    exit(1) ;
  }
  /*NOTREACHED*/
}
