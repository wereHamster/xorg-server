/* template: v0.1, bindings: v0.1 */



enum xcb_DPMS_DPMSMode {
    xcb_DPMS_DPMSMode_On = ,
    xcb_DPMS_DPMSMode_Standby = ,
    xcb_DPMS_DPMSMode_Suspend = ,
    xcb_DPMS_DPMSMode_Off = ,
}


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

int impl_DPMS_GetVersion(ClientPtr client, __req_DPMS_GetVersion *req, __rep_DPMS_GetVersion *rep);

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

int impl_DPMS_Capable(ClientPtr client, __req_DPMS_Capable *req, __rep_DPMS_Capable *rep);

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

int impl_DPMS_GetTimeouts(ClientPtr client, __req_DPMS_GetTimeouts *req, __rep_DPMS_GetTimeouts *rep);

struct req_DPMS_SetTimeouts {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
    uint16_t standby_timeout;
    uint16_t suspend_timeout;
    uint16_t off_timeout;
};

int impl_DPMS_SetTimeouts(ClientPtr client, __req_DPMS_SetTimeouts *req);

struct req_DPMS_Enable {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

int impl_DPMS_Enable(ClientPtr client, __req_DPMS_Enable *req);

struct req_DPMS_Disable {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
};

int impl_DPMS_Disable(ClientPtr client, __req_DPMS_Disable *req);

struct req_DPMS_ForceLevel {
    uint8_t major_opcode;
    uint8_t minor_opcode;
    uint16_t length;
    uint16_t power_level;
};

int impl_DPMS_ForceLevel(ClientPtr client, __req_DPMS_ForceLevel *req);

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

int impl_DPMS_Info(ClientPtr client, __req_DPMS_Info *req, __rep_DPMS_Info *rep);
