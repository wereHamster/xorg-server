
#include <proto/dpms.h>
#include <include/globals.h>

int DPMSSet(ClientPtr client, int level);

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
impl_DPMS_SetTimeouts(ClientPtr client, struct req_DPMS_SetTimeouts *req)
{
    DPMSStandbyTime = req->standby_timeout * MILLI_PER_SECOND;
    DPMSSuspendTime = req->suspend_timeout * MILLI_PER_SECOND;
    DPMSOffTime = req->off_timeout * MILLI_PER_SECOND;

    SetScreenSaverTimer();

    return 0;
}


static int
impl_DPMS_Enable(ClientPtr client, struct req_DPMS_Enable *req)
{
    Bool was_enabled = DPMSEnabled;
    if (DPMSCapableFlag) {
        DPMSEnabled = TRUE;
	if (!was_enabled)
            SetScreenSaverTimer();
    }

    return 0;
}

static int
impl_DPMS_Disable(ClientPtr client, struct req_DPMS_Disable *req)
{
    DPMSSet(client, DPMS_DPMSMode_On);
    DPMSEnabled = FALSE;

    return 0;
}

static int
impl_DPMS_ForceLevel(ClientPtr client, struct req_DPMS_ForceLevel *req)
{
    if (!DPMSEnabled)
        return BadMatch;

    /* TODO: generate this validation from the xcb protocol description */
    if (req->power_level != DPMS_DPMSMode_On &&
        req->power_level != DPMS_DPMSMode_Standby &&
        req->power_level != DPMS_DPMSMode_Suspend &&
	req->power_level != DPMS_DPMSMode_Off) {
        client->errorValue = req->power_level;
	return BadValue;
    }

    DPMSSet(client, req->power_level);

    return 0;
}

static int
impl_DPMS_Info(ClientPtr client, struct req_DPMS_Info *req, struct rep_DPMS_Info *rep)
{
    rep->power_level = DPMSPowerLevel;
    rep->state = DPMSEnabled;
    
    return 0;
}
