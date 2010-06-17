/* template: v0.1, bindings: v${data['version']} */

#include <proto/${data['module'].namespace.header}.h>

% for req in data['request']:
<% name = ('_').join(req.name) %>

struct __req_${name} {
% for field in req.fields:
    ${('_').join(field.type.name)} ${field.field_name};
% endfor
};

static void
__swap_req_${name}(struct __req_${name} *req)
{
% for field in [field for field in req.fields if field.wire]:
% if field.type.is_simple and field.type.size > 1:
    __swap${field.type.size * 8}(req->${field.field_name});
% endif
% endfor
}

static int
__wire_${name}(ClientPtr client)
{
    struct __req_${name} *req = client->requestBuffer;
    if (client->swapped)
        __swap_req_${name}(req);

% if not req.reply:
    return __impl_${name}(client, req);
% else:
    struct __rep_${name} rep;
    int err = __impl_${name}(client, req, &rep);
% endif
    if (err)
        return err;
}

% endfor

static struct xcb_ext_t ext {
% for req in data['request']:
    &__wire_${('_').join(req.name)},
% endfor
};

void
${('_').join(data['module'].namespace.prefix)}(void)
{
    xcb_ext_register("${data['module'].namespace.ext_xname}", &ext);
}
