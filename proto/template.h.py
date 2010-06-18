/* template: v0.1, bindings: v${version} */

<% define = '__PROTO_%s__' % ('_').join(module.namespace.prefix[1:]).upper() %>

#ifndef ${define}
#define ${define}

#include <stdint.h>
#include <include/dix.h>

#define ${('_').join(module.namespace.prefix)}_Major ${module.namespace.major_version}
#define ${('_').join(module.namespace.prefix)}_Minor ${module.namespace.minor_version}

% for value in module.imports:
#include <proto/${value[1]}.h>
% endfor

% for (type, name) in simple:
typedef ${('_').join(type.name).lower()} ${('_').join(name).lower()}_t; 
% endfor

% for (type, name) in enum:
enum ${('_').join(name)} {
% for val in type.values:
    ${('_').join(name)}_${val[0]} = ${val[1]},
% endfor
}
% endfor

% for req in request:
<% name = ('_').join(req.name[1:]) %>
struct req_${name} {
% for field in req.fields:
    ${('_').join(field.type.name)} ${field.field_name};
% endfor
};

% if req.reply:
struct rep_${name} {
% for field in req.reply.fields:
    ${('_').join(field.type.name)} ${field.field_name};
% endfor
};

static int
impl_${name}(ClientPtr client, struct req_${name} *req, struct rep_${name} *rep);
% else:
static int
impl_${name}(ClientPtr client, struct req_${name} *req);
% endif
% endfor

#endif /* ${define} */
