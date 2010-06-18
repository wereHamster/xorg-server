
#include <proto/dpms.h>

int
impl_DPMS_GetVersion(ClientPtr client, struct req_DPMS_GetVersion *req, struct rep_DPMS_GetVersion *rep)
{
    rep->server_major_version = xcb_DPMS_Major;
    rep->server_minor_version = xcb_DPMS_Minor;

    return 0;
}
