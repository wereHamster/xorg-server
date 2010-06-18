/* template: v0.1, bindings: v0.1 */



#ifndef __PROTO_DPMS__
#define __PROTO_DPMS__

#include <stdint.h>
#include <include/dix.h>

#define xcb_DPMS_Major 0
#define xcb_DPMS_Minor 0



struct req_DPMS_GetVersion {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
    uint16_t client_major_version;
    uint16_t client_minor_version;
};

struct rep_DPMS_GetVersion {
    uint8_t response_type;
    uint8_t pad0;
    uint16_t sequence;
    uint32_t length;
    uint16_t server_major_version;
    uint16_t server_minor_version;
};

static int
impl_DPMS_GetVersion(ClientPtr client, struct req_DPMS_GetVersion *req, struct rep_DPMS_GetVersion *rep);

struct req_DPMS_Capable {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

struct rep_DPMS_Capable {
    uint8_t response_type;
    uint8_t pad0;
    uint16_t sequence;
    uint32_t length;
    uint8_t capable;
    uint8_t pad1;
};

static int
impl_DPMS_Capable(ClientPtr client, struct req_DPMS_Capable *req, struct rep_DPMS_Capable *rep);

struct req_DPMS_GetTimeouts {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

struct rep_DPMS_GetTimeouts {
    uint8_t response_type;
    uint8_t pad0;
    uint16_t sequence;
    uint32_t length;
    uint16_t standby_timeout;
    uint16_t suspend_timeout;
    uint16_t off_timeout;
    uint8_t pad1;
};

static int
impl_DPMS_GetTimeouts(ClientPtr client, struct req_DPMS_GetTimeouts *req, struct rep_DPMS_GetTimeouts *rep);

struct req_DPMS_SetTimeouts {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
    uint16_t standby_timeout;
    uint16_t suspend_timeout;
    uint16_t off_timeout;
};

static int
impl_DPMS_SetTimeouts(ClientPtr client, struct req_DPMS_SetTimeouts *req);

struct req_DPMS_Enable {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

static int
impl_DPMS_Enable(ClientPtr client, struct req_DPMS_Enable *req);

struct req_DPMS_Disable {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

static int
impl_DPMS_Disable(ClientPtr client, struct req_DPMS_Disable *req);

struct req_DPMS_ForceLevel {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
    uint16_t power_level;
};

static int
impl_DPMS_ForceLevel(ClientPtr client, struct req_DPMS_ForceLevel *req);

struct req_DPMS_Info {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

struct rep_DPMS_Info {
    uint8_t response_type;
    uint8_t pad0;
    uint16_t sequence;
    uint32_t length;
    uint16_t power_level;
    uint8_t state;
    uint8_t pad1;
};

static int
impl_DPMS_Info(ClientPtr client, struct req_DPMS_Info *req, struct rep_DPMS_Info *rep);

#endif /* __PROTO_DPMS__ */
