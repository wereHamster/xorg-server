
#ifdef HAVE_DIX_CONFIG_H
#include <dix-config.h>
#endif

#include <arpa/inet.h>

#define swap16(ptr) *ptr = htons(*ptr)
#define swap32(ptr) *ptr = htonl(*ptr)

#include <include/os.h> 
#include <include/extnsionst.h>
#include <include/dixstruct.h>
