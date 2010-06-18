/* template: v0.1, bindings: v${version} */

#include <proto/common.h>

#include <proto/${module.namespace.header}.h>
#include <proto/${module.namespace.header}-impl.h>

% for req in request:
<% name = ('_').join(req.name[1:]) %>
/************************************************************
 * Request ${(':').join(req.name[1:])}, opcode: ${req.opcode}
 */

static void
swap_req_${name}(struct req_${name} *req, unsigned long length)
{
% for field in [field for field in req.fields if field.wire]:
% if field.type.is_simple and field.type.size > 1:
    swap${field.type.size * 8}(&req->${field.field_name});
% endif
% endfor
}

% if req.reply:
static void
swap_rep_${name}(struct rep_${name} *rep)
{
% for field in [field for field in req.reply.fields if field.wire]:
% if field.type.is_simple and field.type.size > 1:
    swap${field.type.size * 8}(&rep->${field.field_name});
% endif
% endfor
}
% endif

static int
wire_${name}(ClientPtr client)
{
% if req.fixed_size():
    if (sizeof(struct req_${name}) >> 2 != client->req_len)
        return BadLength;
% else:
    if (sizeof(struct req_${name}) >> 2 > client->req_len)
        return BadLength;
% endif

    struct req_${name} *req = client->requestBuffer;
    if (client->swapped)
        swap_req_${name}(req, client->req_len);

% if not req.reply:
    return impl_${name}(client, req);
% else:
    struct rep_${name} rep = { .response_type = 1,
        .length = sizeof(struct rep_${name}),
        .sequence = client->sequence
    };

    int err = impl_${name}(client, req, &rep);
    if (err < 0)
        return err;

    if (client->swapped)
        swap_rep_${name}(&rep);

    return WriteToClient(client, sizeof(rep), &rep);
% endif
}

% endfor



/************************************************************
 * Request dispatch code
 */

typedef int (*xcb_handler_t)(ClientPtr client);
static xcb_handler_t handler[] = {
% for req in request:
    [${req.opcode}] = &wire_${('_').join(req.name[1:])},
% endfor
    [${len(request)}] = NULL
};

static int
dispatch(ClientPtr client)
{
    unsigned short minor = StandardMinorOpcode(client);
    if (!handler[minor])
        return BadRequest;

    return (*handler[minor])(client);
}

void
${module.namespace.prefix[1]}ExtensionInit(void)
{
    ErrorF("Initializing ${module.namespace.prefix[1]}\n");
    AddExtension("${module.namespace.ext_xname}", 0, 0,
        &dispatch, &dispatch, NULL, &StandardMinorOpcode);
}
