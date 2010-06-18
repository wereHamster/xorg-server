/* template: v0.1, bindings: v0.1 */

#include <proto/common.h>

#include <proto/dpms.h>
#include <proto/dpms-impl.h>


/************************************************************
 * Request DPMS:GetVersion, opcode: 0
 */

static void
swap_req_DPMS_GetVersion(struct req_DPMS_GetVersion *req, unsigned long length)
{
    swap16(&req->length);
    swap16(&req->client_major_version);
    swap16(&req->client_minor_version);
}

static void
swap_rep_DPMS_GetVersion(struct rep_DPMS_GetVersion *rep)
{
    swap16(&rep->sequence);
    swap32(&rep->length);
    swap16(&rep->server_major_version);
    swap16(&rep->server_minor_version);
}

static int
wire_DPMS_GetVersion(ClientPtr client)
{
    if (sizeof(struct req_DPMS_GetVersion) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_GetVersion *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_GetVersion(req, client->req_len);

    struct rep_DPMS_GetVersion rep = { .response_type = 1,
        .length = sizeof(struct rep_DPMS_GetVersion),
        .sequence = client->sequence
    };

    int err = impl_DPMS_GetVersion(client, req, &rep);
    if (err < 0)
        return err;

    if (client->swapped)
        swap_rep_DPMS_GetVersion(&rep);

    return WriteToClient(client, sizeof(rep), &rep);
}


/************************************************************
 * Request DPMS:Capable, opcode: 1
 */

static void
swap_req_DPMS_Capable(struct req_DPMS_Capable *req, unsigned long length)
{
    swap16(&req->length);
}

static void
swap_rep_DPMS_Capable(struct rep_DPMS_Capable *rep)
{
    swap16(&rep->sequence);
    swap32(&rep->length);
}

static int
wire_DPMS_Capable(ClientPtr client)
{
    if (sizeof(struct req_DPMS_Capable) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_Capable *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_Capable(req, client->req_len);

    struct rep_DPMS_Capable rep = { .response_type = 1,
        .length = sizeof(struct rep_DPMS_Capable),
        .sequence = client->sequence
    };

    int err = impl_DPMS_Capable(client, req, &rep);
    if (err < 0)
        return err;

    if (client->swapped)
        swap_rep_DPMS_Capable(&rep);

    return WriteToClient(client, sizeof(rep), &rep);
}


/************************************************************
 * Request DPMS:GetTimeouts, opcode: 2
 */

static void
swap_req_DPMS_GetTimeouts(struct req_DPMS_GetTimeouts *req, unsigned long length)
{
    swap16(&req->length);
}

static void
swap_rep_DPMS_GetTimeouts(struct rep_DPMS_GetTimeouts *rep)
{
    swap16(&rep->sequence);
    swap32(&rep->length);
    swap16(&rep->standby_timeout);
    swap16(&rep->suspend_timeout);
    swap16(&rep->off_timeout);
}

static int
wire_DPMS_GetTimeouts(ClientPtr client)
{
    if (sizeof(struct req_DPMS_GetTimeouts) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_GetTimeouts *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_GetTimeouts(req, client->req_len);

    struct rep_DPMS_GetTimeouts rep = { .response_type = 1,
        .length = sizeof(struct rep_DPMS_GetTimeouts),
        .sequence = client->sequence
    };

    int err = impl_DPMS_GetTimeouts(client, req, &rep);
    if (err < 0)
        return err;

    if (client->swapped)
        swap_rep_DPMS_GetTimeouts(&rep);

    return WriteToClient(client, sizeof(rep), &rep);
}


/************************************************************
 * Request DPMS:SetTimeouts, opcode: 3
 */

static void
swap_req_DPMS_SetTimeouts(struct req_DPMS_SetTimeouts *req, unsigned long length)
{
    swap16(&req->length);
    swap16(&req->standby_timeout);
    swap16(&req->suspend_timeout);
    swap16(&req->off_timeout);
}


static int
wire_DPMS_SetTimeouts(ClientPtr client)
{
    if (sizeof(struct req_DPMS_SetTimeouts) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_SetTimeouts *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_SetTimeouts(req, client->req_len);

    return impl_DPMS_SetTimeouts(client, req);
}


/************************************************************
 * Request DPMS:Enable, opcode: 4
 */

static void
swap_req_DPMS_Enable(struct req_DPMS_Enable *req, unsigned long length)
{
    swap16(&req->length);
}


static int
wire_DPMS_Enable(ClientPtr client)
{
    if (sizeof(struct req_DPMS_Enable) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_Enable *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_Enable(req, client->req_len);

    return impl_DPMS_Enable(client, req);
}


/************************************************************
 * Request DPMS:Disable, opcode: 5
 */

static void
swap_req_DPMS_Disable(struct req_DPMS_Disable *req, unsigned long length)
{
    swap16(&req->length);
}


static int
wire_DPMS_Disable(ClientPtr client)
{
    if (sizeof(struct req_DPMS_Disable) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_Disable *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_Disable(req, client->req_len);

    return impl_DPMS_Disable(client, req);
}


/************************************************************
 * Request DPMS:ForceLevel, opcode: 6
 */

static void
swap_req_DPMS_ForceLevel(struct req_DPMS_ForceLevel *req, unsigned long length)
{
    swap16(&req->length);
    swap16(&req->power_level);
}


static int
wire_DPMS_ForceLevel(ClientPtr client)
{
    if (sizeof(struct req_DPMS_ForceLevel) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_ForceLevel *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_ForceLevel(req, client->req_len);

    return impl_DPMS_ForceLevel(client, req);
}


/************************************************************
 * Request DPMS:Info, opcode: 7
 */

static void
swap_req_DPMS_Info(struct req_DPMS_Info *req, unsigned long length)
{
    swap16(&req->length);
}

static void
swap_rep_DPMS_Info(struct rep_DPMS_Info *rep)
{
    swap16(&rep->sequence);
    swap32(&rep->length);
    swap16(&rep->power_level);
}

static int
wire_DPMS_Info(ClientPtr client)
{
    if (sizeof(struct req_DPMS_Info) >> 2 != client->req_len)
        return BadLength;

    struct req_DPMS_Info *req = client->requestBuffer;
    if (client->swapped)
        swap_req_DPMS_Info(req, client->req_len);

    struct rep_DPMS_Info rep = { .response_type = 1,
        .length = sizeof(struct rep_DPMS_Info),
        .sequence = client->sequence
    };

    int err = impl_DPMS_Info(client, req, &rep);
    if (err < 0)
        return err;

    if (client->swapped)
        swap_rep_DPMS_Info(&rep);

    return WriteToClient(client, sizeof(rep), &rep);
}




/************************************************************
 * Request dispatch code
 */

typedef int (*xcb_handler_t)(ClientPtr client);
static xcb_handler_t handler[] = {
    [0] = &wire_DPMS_GetVersion,
    [1] = &wire_DPMS_Capable,
    [2] = &wire_DPMS_GetTimeouts,
    [3] = &wire_DPMS_SetTimeouts,
    [4] = &wire_DPMS_Enable,
    [5] = &wire_DPMS_Disable,
    [6] = &wire_DPMS_ForceLevel,
    [7] = &wire_DPMS_Info,
    [8] = NULL
};

static int
dispatch(ClientPtr client)
{
    unsigned short minor = StandardMinorOpcode(client);
    if (client->swapped)
        swap16(&minor);

    if (!handler[minor])
        return BadRequest;

    return (*handler[minor])(client);
}

void
DPMSExtensionInit(void)
{
    ErrorF("Initializing DPMS\n");
    AddExtension("DPMS", 0, 0,
        &dispatch, &dispatch, NULL, &StandardMinorOpcode);
}
