
#include <proto/dpms.h>
#include <include/globals.h>

static int
impl_DPMS_GetVersion(ClientPtr client, struct req_DPMS_GetVersion *req, struct rep_DPMS_GetVersion *rep)
{
    rep->server_major_version = xcb_DPMS_Major;
    rep->server_minor_version = xcb_DPMS_Minor;

    return 0;
}

static int
impl_DPMS_Capable(ClientPtr client, struct req_DPMS_Capable *req, struct rep_DPMS_Capable *rep)
{
    rep->capable = DPMSCapableFlag;

    return 0;
}

static int
impl_DPMS_GetTimeouts(ClientPtr client, struct req_DPMS_GetTimeouts *req, struct rep_DPMS_GetTimeouts *rep)
{
    rep->standby_timeout = DPMSStandbyTime / MILLI_PER_SECOND;
    rep->suspend_timeout = DPMSSuspendTime / MILLI_PER_SECOND;
    rep->off_timeout = DPMSOffTime / MILLI_PER_SECOND;

    return 0;
}

static int
impl_DPMS_Info(ClientPtr client, struct req_DPMS_Info *req, struct rep_DPMS_Info *rep)
{
    rep->power_level = DPMSPowerLevel;
    rep->state = DPMSEnabled;
    
    return 0;
}
